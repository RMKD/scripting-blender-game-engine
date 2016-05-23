from bge import logic, events

'''
def make_cube():
    bpy.ops.mesh.primitive_cube_add()
    obj = bpy.context.active_object
    return obj

def attach_script(obj, sensor_type='ALWAYS', script_name='my_blend_script.py', sensor_name='my_sensor', controller_name='py_controller'):
    bpy.ops.logic.sensor_add(type=sensor_type, name=sensor_name)
    sensor = obj.game.sensors[-1]
    sensor.use_pulse_true_level = True
    sensor.use_all_keys = True
    bpy.ops.logic.controller_add(type='PYTHON', name=controller_name, object=obj.name)
    controller = obj.game.controllers[-1]
    controller.text = bpy.data.texts[script_name]
    sensor.link(controller)
    return True

my_avatar = make_cube()
attach_script(my_avatar, 'KEYBOARD', 'wasd_controls.py', sensor_name='my_keyboard')

'''


def main():
    scene = logic.getCurrentScene()
    controller = logic.getCurrentController()
    obj = controller.owner

    # assumes a keyboard sensor has been created named 'my_keyboard' with use_pulse_true_level = True
    kb = controller.owner.sensors['my_keyboard']

    for key, status in kb.events:
        '''
        for keydown use logic.KX_INPUT_JUST_ACTIVATED (resolves to 1)
        for keypressed use logic.KX_INPUT_ACTIVE (resolves to 2)
        for keyup use logic.KX_INPUT_JUST_RELEASED (resolves to 3)
        '''
        if(status == logic.KX_INPUT_ACTIVE):
            if key is events.ENTERKEY:
                pass
            elif (key == events.SPACEKEY):
                pass
            elif key is events.WKEY or key is events.UPARROWKEY:
                #use applyMovement((x,y,z), use_local) to orient in relation to the object
                obj.applyMovement((0,0.1,0), True)
            elif key is events.AKEY or key is events.LEFTARROWKEY:
                obj.applyMovement((-0.1,0,0), True)
            elif key is events.SKEY or key is events.DOWNARROWKEY:
                obj.applyMovement((0,-0.1,0), True)
            elif key is events.DKEY or key is events.RIGHTARROWKEY:
                obj.applyMovement((0.1,0,0), True)
            elif key is events.JKEY:
                obj.applyRotation((0,0,0.02))
            elif key is events.KKEY:
                print(dir(obj))
                obj.applyMovement((0,0,0.2))
            elif key is events.LKEY:
                obj.applyRotation((0,0,-0.02))
            elif key is events.F1KEY:
                pass
            else:
                '''
                to see what else you can use to sense keys, uncomment the next line
                '''
                # print('your other options are', dir(events))
                pass

main()
