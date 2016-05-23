# code source: http://www.cgmasters.net/free-tutorials/fps-mouselook-script-plus-real-text/

'''
Documentation from Keelan Downton:

This script expects a Camera object which is the child of an object of focus.

if you do not have this set up, you can run the following in the editor python console:
import bpy
def make_cube():
    bpy.ops.mesh.primitive_cube_add()
    obj = bpy.context.active_object
    return obj

def attach_script(obj, sensor_type='ALWAYS', script_name='my_blend_script.py', sensor_name='my_sensor', controller_name='py_controller'):
    bpy.ops.logic.sensor_add(type=sensor_type, name=sensor_name, object=obj.name)
    sensor = obj.game.sensors[-1] #default is sensor_type.title()
    sensor.use_pulse_true_level = True
    if sensor_type is 'KEYBOARD':
        sensor.use_all_keys = True
    elif sensor_type is 'MOUSE':
        sensor.mouse_event = 'MOVEMENT'
    bpy.ops.logic.controller_add(type='PYTHON', name=controller_name, object=obj.name)
    controller = obj.game.controllers[-1] # default is sensor_type.title()
    controller.text = bpy.data.texts[script_name]
    sensor.link(controller)
    return True


c = make_cube()
cam = bpy.context.scene.objects['Camera']
cam.parent = c
attach_script(cam, sensor_type='MOUSE', script_name='mouse_controls.py')
attach_script(cam, sensor_type='ALWAYS', script_name='mouse_controls.py')

#if you want to move around, attach a keyboard controller to the parent cube
attach_script(c, sensor_type='KEYBOARD', script_name='keyboard_controls.py', sensor_name='my_keyboard')
'''

import bge
from bge import render as r
import math

cont = bge.logic.getCurrentController()
own = cont.owner
mouse = cont.sensors["Mouse"]
parent = own.parent

#set speed for camera movement
sensitivity = 0.05

#set camera rotation limits
high_limit = 180
low_limit = 0

h = r.getWindowHeight()//2
w = r.getWindowWidth()//2
x = (h - mouse.position[0])*sensitivity
y = (w - mouse.position[1])*sensitivity

if own["startup"]:
    r.setMousePosition(h, w)
    own ["startup"] = False
else:
    rot = own.localOrientation.to_euler()
    pitch = abs(math.degrees(rot[0]))
    if high_limit > (pitch+y) > low_limit:
        pitch += y
    elif (pitch+y) < low_limit:
        pitch = low_limit
    elif (pitch+y) > high_limit:
        pitch = high_limit
    rot[0] = math.radians(pitch)
    own.localOrientation = rot.to_matrix()

    parentRot = parent.localOrientation.to_euler()
    yaw = math.degrees(parentRot[2]) + x
    parentRot[2] = math.radians(yaw)
    parent.localOrientation = parentRot.to_matrix()

    r.setMousePosition(h, w)
