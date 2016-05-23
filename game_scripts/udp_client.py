from random import randrange
from time import sleep

import socket
import pickle
from bge import logic

from helpers import BlenderObjectProxy, setOrientationByEuler

def run_in_game():
    '''
    use this for building clients that are a standalone game executable

    '''
    print("im running as a client!")

    msg = ('register', ('ShipPrefab', 0, 0, 0, 0, 0, 0) )
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_ip = '0.0.0.0'
    server_port = 9999
    dest = (server_ip, server_port)
    s.sendto(pickle.dumps(msg), dest)
    scene = logic.getCurrentScene()
    cam = scene.objects['OverheadCamera']
    
    spawner = scene.objects["spawner"]
    avatar = scene.addObject("avatar", spawner)
    new_cam = scene.addObject("client_camera", spawner)
    #new_cam.applyRotation([90,0,0], True)
    setOrientationByEuler(new_cam, (80,0,0)

    #new_cam.worldOrientation = [[0.0, 0.0,1.0], [ 1.0, 0.0, 0.0], [0.0, 0.5, 0.0]]
    new_cam.setParent(avatar)
    #print(scene.objects, logic.getSceneList(), cam, dir(new_cam))
    scene.active_camera = scene.objects["client_camera"]
    #print(scene.objects, scene.objects['avatar'], dir(avatar))
    while False:
        try:
            print('receiving')
            data, addr = s.recvfrom(1024)
            print(pickle.loads(data))
            scene.active_camera = scene.objects["avatar_camera"]
        except socket.error  as e:
            print('socket error', e)
            break
    
    #cam.endObject()
    #pass

def run_outside_game():
    '''
    use this if you just want to send datagrams to a a server instance and have them affect the game world
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_ip = '192.168.1.101'
    server_port = 7777
    dest = (server_ip, server_port)

    msg = ('device_state', ('device_id-%s' % randrange(0,100), 0, 0, 0, 0, 0, 0))
    #msg = ('register',('hello%s' %str(randrange(-5,5) ), 0, 3, 45))
    try:
        pass
        #p = grovepi.analogRead(2) #potentiometer
        #led = 5
        #print('grove', p, led)
        #grovepi.pinMode(led,"OUTPUT")
        #grovepi.analogWrite(led,p/4)
        #msg = ('device_state',('grove-01', 0, 0, 0, 0, 0, p))
    except Exception as e:
        print('could not load grove data', e)

    while True:
        try:
            print('sending', msg)
            #s.sendto(pickle.dumps(msg), dest)
            obj = BlenderObjectProxy('object_id_%s' % randrange(0,5), (randrange(-5,5), randrange(-5,5), randrange(-5,5) ))
            #s.sendto(obj.serialize(), dest)
            s.sendto(pickle.dumps(msg), dest)
            sleep(3)
        except socket.error  as e:
            print('socket error', e)
            break

        try:
            print('receiving')
            data, addr = s.recvfrom(1024)
            print(pickle.loads(data))

        except socket.error  as e:
            print('socket error', e)
            break

if __name__ == '__main__':
    run_outside_game()
