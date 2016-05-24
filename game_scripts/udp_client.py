from random import randrange
from time import sleep

import socket
import pickle
from bge import logic

from helpers import setOrientationByEuler, encode_object_message

class Client():
    def __init__(self, server_ip="0.0.0.0", server_port=9999, prefab_name='Cube'):
        msg = ('register', (prefab_name, 0, 0, 0, 0, 0, 0) )
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
        self.dest = (server_ip, server_port)
        print('sending to', self.dest)
        self.socket.sendto(pickle.dumps(msg), self.dest)
        self.network_objects = {}
        self.client_id = ''
        
    def handle_server_messages(self):
        scene = logic.getCurrentScene()
        while True:
            try:
                print('receiving')
                data, addr = self.socket.recvfrom(1024)
                
                print(pickle.loads(data))
                code, msg = pickle.loads(data)
                
                #process the decoded message and take appropriate action
                if(code == "welcome"):
                    print('server welcomes us!', msg)
                    self.client_id = msg 
                    #server will send and
                    spawner = scene.objects["spawner"]
                    avatar = scene.addObject("avatar", spawner)
                    avatar['user'] = msg
                    cam = scene.cameras['Camera']
                    print ('cam', dir(avatar), cam)
                    self.network_objects[msg] = avatar
                    print('network objects', self.network_objects)
                elif(code == 'object'):
                    name, user, position, euler_rotation = msg
                    print('received object', name, position, euler_rotation)
                    if(name in scene.objects):
                        print('object exists')
                        obj = scene.objects[name]                        
                    else:
                        # object needs to be instantiated
                        print('unknown object')
                        spawner = scene.objects["spawner"]
                        obj = scene.addObject(name, spawner)
                    obj.position = position    
                    setOrientationByEuler(obj, euler_rotation)
                
                else:                    
                    print('unknown', code, msg)
                #scene.active_camera = scene.cameras["client_camera"]
            except socket.error  as e:
                #print('socket error', e)
                break
    
    def send_update(self):
        for source_addr, obj in self.network_objects.items():           
            print('sending', obj.name, obj.position)
            self.socket.sendto(encode_object_message(obj), self.dest)      

client = Client(server_ip='127.0.0.1', server_port=9999, prefab_name='ShipPrefab')

def listen():
    client.handle_server_messages()
    
def broadcast():
    client.send_update()

#if __name__ == '__main__':
#    run_outside_game()
