import socket
import pickle
from bge import logic
from helpers import BlenderObjectProxy, setOrientationByEuler
#NOTE when sending pickle.dumps set protocol=2 to allow python 2-3 interoperability

def serialize_object(obj, id):
    print('obj', obj, id)
    print(obj.orientation)
    x, y, z = obj.position
    a, b, c = obj.orientation
    print(a,b,c)
    return pickle.dumps( ('object', (obj.name, id, (x, y, z), [x for x in a], [y for y in b], [z for z in c] ) ))


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
        
        self.entities = {}
        self.addr_user = {}
        scene = logic.getCurrentScene()
        scene.objects['NetworkManager'].children[0]["Text"] = '%s:%s' % (host, p)

    #def __del__(self):
    #    print ("destructor")   
    #    self.socket.shutdown(2)
    #    self.socket.close()     

    def handle_user_messages(self):
        scene = logic.getCurrentScene()
        while True:
      
            try:
                #print('listening')
                data, addr = self.socket.recvfrom(1024)
                print(pickle.loads(data),'from',addr)

                code, msg = pickle.loads(data)

                if not addr in self.addr_user:
                    spawner = scene.objects["spawner"]
                    avatar = scene.addObject("avatar", spawner)
                    
                    scene.active_camera = scene.cameras['OverheadCamera']
                    # avatar.children[0]["Text"] = user.name
                    # avatar["user"] = user

                    client_id = 'client-%s' % addr[1]
                    self.addr_user[addr] = {'id': client_id}
 
                    self.socket.sendto(pickle.dumps( ('welcome', client_id), protocol=2), addr)
                    self.entities[addr] = avatar
                if (code == 'device_state'):
                    for other_client in self.addr_user:
                        #self.socket.sendto(pickle.dumps( ('server_%s' % code, msg), protocol=2), other_client)
                        if(other_client == addr):
                            continue
                        self.socket.sendto(pickle.dumps( ('server_%s' % code, msg), protocol=2), other_client)
                if (code == 'object'):
                    print('received object', msg)
                    name, id, position, quaternion = msg
                    if name not in self.entities:         
                        #this is a new network object  
                        new_object = scene.addObject(name)
                        new_object.position = position            
                        self.entities[name] = new_object
                    else:
                        self.entities[name].position = position
                        self.entities[name].setOrientation(quaternion)
                    for other_client in self.addr_user:
                        if(other_client == addr):
                            continue
                        self.socket.sendto(pickle.dumps( (code, msg), protocol=2), other_client)

            except socket.error  as e:
                #print('socket error', e)
                #catch this error silently - it lets use use a non-blocking socket
                break

    def handle_world_updates(self):
        scene = logic.getCurrentScene()
        for addr in self.addr_user:
            for source_addr, obj in self.entities.items():
                if(addr == source_addr):
                    continue
                uuid = "%s-%s" % (obj.name, source_addr[1])
                self.socket.sendto(serialize_object(obj,uuid), addr)

# intialize the server for modules to be called from
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


if __name__ == '__main__':
    listen()
    broadcast()
