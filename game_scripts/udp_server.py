import socket
import pickle
from bge import logic
from helpers import setOrientationByEuler, encode_object_message
#NOTE when sending pickle.dumps set protocol=2 to allow python 2-3 interoperability

class Server:
    def __init__(self, host="", port=9999):
        print('initializing server', host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
        #self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind on some socket in the range 9999-10099
        for p in range(port, port+100):
            try:
                self.socket.bind((host, p))
                self.host = host
                self.port = p
                break
            except:
                print('%s failed, trying %s' % (p, p+1) )
        
        self.network_objects= {}
        self.addr_user = {}
        
        #on init, render the selected ip and port in the view
        scene = logic.getCurrentScene()
        scene.objects['NetworkManager'].children[0]["Text"] = '%s:%s' % (host, p)

    def handle_user_messages(self):
        scene = logic.getCurrentScene()
        while True:
            try:
                data, addr = self.socket.recvfrom(1024)
                
                print(pickle.loads(data),'from',addr)

                code, msg = pickle.loads(data)

                if not addr in self.addr_user:
                    spawner = scene.objects["spawner"]
                    avatar = scene.addObject("avatar", spawner)
                    
                    scene.active_camera = scene.cameras['OverheadCamera']
                    # avatar.children[0]["Text"] = user.name
                    

                    client_id = 'client-%s' % addr[1]
                    avatar["user"] = client_id
                    self.addr_user[addr] = {'id': client_id}
 
                    self.socket.sendto(pickle.dumps( ('welcome', client_id), protocol=2), addr)
                    self.network_objects[addr] = avatar

                if (code == 'object'):                    
                    name, user, position, euler_rotation = msg
                    print('received object', name, user, position, euler_rotation)
                    
                    if addr not in self.network_objects:         
                        #this is a new network object so add it to the scene and the network_objects 
                        new_object = scene.addObject(name)
                        new_object.position = position            
                        self.network_objects[addr] = new_object
                    else:
                        new_object = self.network_objects[addr]
                        new_object.position = position
                        setOrientationByEuler(new_object, euler_rotation)

                if (code == 'device_state'):
                    for other_client in self.addr_user:
                        #self.socket.sendto(pickle.dumps( ('server_%s' % code, msg), protocol=2), other_client)
                        if(other_client == addr):
                            continue
                        self.socket.sendto(pickle.dumps( ('server_%s' % code, msg), protocol=2), other_client)

            except socket.error  as e:
                #print('socket error', e)
                #catch this error silently - it lets you use a non-blocking socket
                break

    def handle_world_updates(self):
        '''
        Use this to broadcast all objects that are tracked in self.network_objects to all the clients
        '''
        scene = logic.getCurrentScene()
        for addr in self.addr_user:
            for source_addr, obj in self.network_objects.items():
                #print(addr, source_addr, obj.name, addr[1] == source_addr[1])
                if(addr[1] == source_addr[1]):
                    continue
                self.socket.sendto(encode_object_message(obj), addr)
                print('sending', obj.name, obj.position, 'to',addr)
                
# intialize the server for modules to be called from the logic editor
server = Server()

def listen():
    '''
    call this function as a module in a python controller
    - attach to an Always sensor with use_pulse_true_level set to True
    - set the tick_skip value (Skip) to determine how often the loop is called (helps optimize network traffic)

    it calls a server function to listen for packets from users, and handle them appropriately
    '''
    server.handle_user_messages()

def broadcast():
    '''
    call this function as a module in a python controller
    - attach to an Always sensor with use_pulse_true_level set to True
    - set the tick_skip value (Skip) to determine how often the loop is called  (helps optimize network traffic)

    it calls a server function to send world state updates to clients
    '''
    server.handle_world_updates()


