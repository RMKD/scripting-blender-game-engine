from random import randrange
from time import sleep

import socket
import pickle
from bge import logic

from helpers import BlenderObjectProxy, setOrientationByEuler

def serialize_object(obj, id):
    print('obj', obj, id)
    print(obj.orientation)
    x, y, z = obj.position
    a, b, c = obj.orientation
    print(a,b,c)
    return pickle.dumps( ('object', (obj.name, id, [x, y, z], [[x for x in a], [y for y in b], [z for z in c]] ) ))


class Client():
    def __init__(self, server_ip="0.0.0.0", server_port=9999):
        msg = ('register', ('ShipPrefab', 0, 0, 0, 0, 0, 0) )
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
        server_ip = '192.168.1.101'
        server_port = 10003
        self.dest = (server_ip, server_port)
        print('sending to', self.dest)
        self.socket.sendto(pickle.dumps(msg), self.dest)
        self.network_objects = []
        self.client_id = ''
        
    def handle_server_messages(self):
        scene = logic.getCurrentScene()
        while True:
            try:
                print('receiving')
                data, addr = self.socket.recvfrom(1024)
                
                #if welcome, spawn avatar and attach camera
                #if 
                print(pickle.loads(data))
                code, msg = pickle.loads(data)
                
                if(code == "welcome"):
                    print('server welcomes us!', msg)
                    self.client_id = msg 
                    #server will send and
                    spawner = scene.objects["spawner"]
                    avatar = scene.addObject("avatar", spawner)
                    cam = scene.cameras['Camera']
                    print ('cam', dir(avatar), cam)
                    self.network_objects.append(avatar)
                    print('network objects', self.network_objects)
                elif(code == 'object'):
                    name, id, x, y, z, xr, xy, xz = msg
                    #obj = scene.objects[name]
                    print('OBJ', name)
                else:                    
                    print('unknown', code, msg)
                #scene.active_camera = scene.cameras["client_camera"]
            except socket.error  as e:
                #print('socket error', e)
                break
    
    def send_update(self):
        for obj in self.network_objects:            
            uuid = "%s-%s" % (obj.name, self.client_id)
            print('sending', serialize_object(obj, uuid))
            self.socket.sendto(serialize_object(obj, uuid), self.dest)      

client = Client()

def listen():
    client.handle_server_messages()
    
def broadcast():
    client.send_update()

#if __name__ == '__main__':
#    run_outside_game()
