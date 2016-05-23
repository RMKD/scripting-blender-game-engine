import socket
import pickle
from bge import logic
from helpers import BlenderObjectProxy
#NOTE when sending pickle.dumps set protocol=2 to allow python 2-3 interoperability

class Server:
    def __init__(self, host="", port=9999):
        print('initializing server', host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
        #self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        for p in range(port, port+100):
            try:
                self.socket.bind((host, p))
                break
            except:
                print('%s failed, trying %s' % (p, p+1) )

        self.entities = {}
        self.addr_user = {}

    def handle_user_messages(self):
        while True:
            try:
                #print('listening')
                data, addr = self.socket.recvfrom(1024)
                print(pickle.loads(data),'from',addr)

                code, msg = pickle.loads(data)

                if not addr in self.addr_user:

                    #user = User(data.decode())
                    #print(data.decode())

                    scene = logic.getCurrentScene()
                    #print(scene.objects)
                    spawner = scene.objects["spawner"]
                    avatar = scene.addObject("avatar", spawner)
                    # avatar.children[0]["Text"] = user.name
                    # avatar["user"] = user

                    self.addr_user[addr] = {}
                    self.socket.sendto(pickle.dumps( ('welcome', msg), protocol=2), addr)
                if (code == 'device_state'):
                    for other_client in self.addr_user:
                        #self.socket.sendto(pickle.dumps( ('server_%s' % code, msg), protocol=2), other_client)
                        if(other_client == addr):
                            continue
                        self.socket.sendto(pickle.dumps( ('server_%s' % code, msg), protocol=2), other_client)
                if (code == 'blender'):
                    for other_client in self.addr_user:
                        if(other_client == addr):
                            continue
                        self.socket.sendto(pickle.dumps( ('server_%s' % code, msg), protocol=2), other_client)
                if (code == 'object'):
                    print('broadcasting object', msg)
                    obj = msg
                    if obj.id not in self.entities:
                        scene = logic.getCurrentScene()
                        new_object = scene.addObject(obj.prefab)
                        new_object.position = obj.position
                        self.entities[obj.id] = new_object
                    else:
                        self.entities[obj.id].position = obj.position
                        self.entities[obj.id].roation = obj.rotation
                    for other_client in self.addr_user:
                        if(other_client == addr):
                            continue
                        self.socket.sendto(pickle.dumps( (code, msg), protocol=2), other_client)
                if(code == 'command'):
                    for other_client in self.addr_user:
                        if(other_client == addr):
                            continue
                        self.socket.sendto(pickle.dumps( (code, msg), protocol=2), other_client)

            except socket.error  as e:
                #print('socket error', e)
                #catch this error silently - it lets use use a non-blocking socket
                break

    def handle_world_updates(self):
        world_state = {(gobj.name, gobj['user'].name): list(gobj.worldPosition) for gobj in scene.objects if gobj.name is 'avatar'}
        for addr in self.addr_user:
            self.socket.sendto(pickle.dumps(state), addr)

# intialize the server for modules to be called from
server = Server(port=9999)


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
