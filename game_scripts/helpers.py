import pickle
from math import radians
class BlenderObjectProxy(object):
    id = ''
    position = (0,0,0)
    euler_rotation = (0,0,0)
    prefab = ''

    def __init__(self, id='test', position=(0,0,0), euler_rotation=(0,0,0), prefab='Cube', from_serialized=None):
        if(from_serialized):
            self = BlenderObjectProxy(id, position, euler_rotation, prefab)
        else:
            self.id = id
            self.position = position
            self.euler_rotation = euler_rotation
            self.prefab = prefab

    def serialize(self):
        # (id, position, euler, prefab)
        #return pickle.dumps(('object',(self.id, self.position, self.euler_rotation, self.prefab)))
        #return pickle.dumps(('object',(self.id, self.position, self.euler_rotation, self.prefab)), protocol=2)
        return pickle.dumps(('object', self),  protocol=2)

    def deserialize(self, data):
        msg_type, data = pickle.loads(data)
        if msg_type is 'object':
            return BlenderObjectProxy(data)
        else:
            return None

def setOrientationByEuler(obj, euler=(0,0,0)):
    #xyz = new_cam.worldOrientation.to_euler()
    #xyz[0] = radians(80)
    #new_cam.worldOrientation = xyz.to_matrix()
    obj.worldOrientation = (radians(euler[0]),radians(euler[1]),radians(euler[2]))
    return obj


def send_message(key, value, recipient_name):
    bge.logic.sendMessage(key, value, recipient_name)

def main():
    #create at least one object to ensure the class is available within the engine
    b = BlenderObjectProxy()

if __name__=='__main__':
    main()
