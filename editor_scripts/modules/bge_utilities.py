import bpy
from math import radians

'''
The easiest way to use the functions in this script is to import it as as Addon. You can also make it accessible to the blender python console by specifying its location in File > User Preferences > File. Set the Scripts file to the editor_scripts directory.
'''

def make(primitive='cube', location=(0,0,0), rotation=None, scale=None, physics='STATIC'):
    if(primitive == 'cube'):
        bpy.ops.mesh.primitive_cube_add(location=location)
    elif(primitive == 'cone'):
        bpy.ops.mesh.primitive_cone_add(location=location)
    obj = bpy.context.active_object
    if(rotation):
        #convert degrees to radians
        obj.rotation_euler = [radians(degree) for degree in rotation]
    if(scale):
        obj.scale = scale
    if(physics):
        obj.game.physics_type = physics
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    return obj

def make_cube(location=(0,0,0), rotation=None, scale=None, physics='STATIC'):
    '''
    ex: c = make_cube()
        c.position = (3, 5, 1)
    ex2: c = make_cube((3,5,1), (0,90,45))
    '''
    return make('cube', location, rotation, scale, physics)

def make_cone(location=(0,0,0), rotation=None, scale=None, physics='STATIC'):
    '''
    ex: c = make_cone()
    ex2: c = make_cone(rotation=(90,0,-180), scale=(1,1,2), location=(0,0,3))
    ex3: c = make_cone(physics='DYNAMIC')
    '''
    return make('cone', location, rotation, scale, physics)


def track_to(camera_object, point=(0,0,0)):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=point)
    point_of_interest = bpy.context.active_object
    point_of_interest.name = 'camera_tracks_here'
    camera_object.constraints["Track To"].name = "Track To"
    bpy.ops.object.constraint_add(type='TRACK_TO')
    bpy.context.object.constraints["Track To"].target = point_of_interest
    bpy.context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'

def add_property(obj, name, type='FLOAT',value=0):
    # to add a property
    obj.game_property_new(name=name, type=type, value=value)
    obj.show_debug = True


def add_key_to_move(obj, key, axis, amount):
    '''
    Attach a keypress to an object's motion (for axis x=0, y=1, z=2)
    '''
    bpy.ops.logic.sensor_add(type='KEYBOARD', name=key)
    sensor = obj.game.sensors[-1]
    sensor.key = key
    sensor.show_expanded = False
    bpy.ops.logic.actuator_add(type='MOTION')
    actuator = obj.game.actuators[-1]
    actuator.offset_location[axis] = amount
    actuator.show_expanded = False
    bpy.ops.logic.controller_add(object=obj.name)
    controller = obj.game.controllers[-1]
    sensor.link(controller)
    actuator.link(controller)

def add_key_to_rotate(obj, key, axis, amount):
    '''
    Attach a keypress to an object's rotation (for axis x=0, y=1, z=2)
    '''
    bpy.ops.logic.sensor_add(type='KEYBOARD', name=key)
    sensor = obj.game.sensors[-1]
    sensor.key = key
    sensor.show_expanded = False
    bpy.ops.logic.actuator_add(type='MOTION')
    actuator = obj.game.actuators[-1]
    actuator.offset_rotation[axis] = amount
    actuator.show_expanded = False
    bpy.ops.logic.controller_add(object=obj.name)
    controller = obj.game.controllers[-1]
    sensor.link(controller)
    actuator.link(controller)

def setup_keyboard_controller(obj):
    '''
    sets up up a keyboard as a basic motion controller
    if you don't have a reference to the object you can get it with bpy.data.objects['my-object-name']
    '''
    add_key_to_move(obj, 'W', axis=1, amount=1)
    add_key_to_move(obj, 'A', axis=0, amount=-1)
    add_key_to_move(obj, 'S', axis=1, amount=-1)
    add_key_to_move(obj, 'D', axis=0, amount=1)

    add_key_to_rotate(obj, 'J', axis=2, amount=-0.0174533)
    add_key_to_move(obj, 'K', axis=2, amount=+5)
    add_key_to_rotate(obj, 'L', axis=2, amount=0.0174533)

def attach_script(obj, sensor_type='ALWAYS', script_name='my_blend_script.py', sensor_name='my_sensor', controller_name='py_controller'):
    '''
    attaches a script to an object (assumes the script has already been linked in the Blender editor)
    ex: my_avatar = make_cube()
        attach_script(my_avatar, 'KEYBOARD', 'wasd_controls.py', sensor_name='my_keyboard')
    '''
    bpy.ops.logic.sensor_add(type=sensor_type, name=sensor_name, object=obj.name)
    sensor = obj.game.sensors[-1] #default is sensor_type.title()
    sensor.use_pulse_true_level = True
    if sensor_type is 'KEYBOARD':
        sensor.use_all_keys = True
    elif sensor_type is 'MOUSE':
        sensor.mouse_event = 'MOVEMENT'
    elif sensor_type is 'JOYSTICK':
        sensor.use_all_events = True
    bpy.ops.logic.controller_add(type='PYTHON', name=controller_name, object=obj.name)
    controller = obj.game.controllers[-1] # default is sensor_type.title()
    controller.text = bpy.data.texts[script_name]
    sensor.link(controller)
    return True

def run_general_setup():
    '''
    some general things to set up for scripting with the blender game engine
    '''
    bpy.context.scene.game_settings.material_mode = 'GLSL'
    bpy.context.scene.render.engine = 'BLENDER_GAME'
    bpy.context.scene.world.mist_settings.use_mist = True

def run_game():
    bpy.ops.view3d.game_start()

def run_standalone():
    bpy.ops.wm.blenderplayer_start()


# some boilerplate to make this importable via the User Preferences addon menuS
bl_info = {
    "name": "Blender Game Engine Editor Tools ",
    "description": "This is a toolset to make it easier to attach and manipulate game engine artifacts with python commands in the console.",
    "author": "R. M. Keelan Downton",
    "version": (0, 1),
    "blender": (2, 77, 0),
    "location": "View3D > Object > Game Engine",
    "warning": "experimental", # used for warning icon and text in addons panel
    "wiki_url": "https://github.com/RMKD/scripting-blender-game-engine",
    "tracker_url": "https://github.com/RMKD/scripting-blender-game-engine/issues",
    "support": "COMMUNITY",
    "category": "Game Engine"
    }

def register():
    print('register')

def unregister():
    print('unregister')

if __name__ == '__main__':
    register()
