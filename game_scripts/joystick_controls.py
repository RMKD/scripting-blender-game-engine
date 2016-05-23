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
attach_script(my_avatar, 'JOYSTICK', 'joystick_controls.py', sensor_name='my_xbox_controller')

'''

VALUE_MAX=32768.0

def ignore_deadzone(n, values):
    '''
    Use some value to treat a wide range of values in the middle (when at rest) as zero
    '''
    return [v if abs(v) > abs(n) else 0 for v in values]

'''
Blender joystick sensors make the following functions and values available to the sensor object:

    ['axis', 'axisSingle', 'axisValues', 'button', 'connected', 'executePriority', 'frequency', 'getButtonActiveList', 'getButtonStatus', 'hat',
    'hatSingle', 'hatValues', 'index', 'invalid', 'invert', 'level', 'name', 'neg_ticks', 'numAxis', 'numButtons', 'numHats', 'owner', 'pos_ticks',
    'positive', 'reset', 'skippedTicks', 'status', 'tap', 'threshold', 'triggered', 'useNegPulseMode', 'usePosPulseMode']

'''

def main():
    scene = logic.getCurrentScene()
    controller = logic.getCurrentController()
    obj = controller.owner

    if('my_xbox_controller' not in controller.owner.sensors):
        return
    # assumes a keyboard sensor has been created named 'my_keyboard' with use_pulse_true_level = True
    xbc = controller.owner.sensors['my_xbox_controller']

    # make sure
    if len(xbc.axisValues) is not 6:
        return

    #handle the joystick and trigger axes
    left_x, left_y, left_trigger, right_x, right_y, right_trigger = ignore_deadzone(6000, xbc.axisValues)
    print(left_x, left_y, left_trigger, right_x, right_y, right_trigger , left_y/VALUE_MAX)

    # set the rotation with a damper from the right stick. args = ([x,y,z], use_local_coordinates])
    obj.applyRotation([0, 0, -right_x/VALUE_MAX * 0.02], True)

    #set the movement with the left stick, args = ([x,y,z], use_local_coordinates])
    obj.applyMovement([0, -left_y/VALUE_MAX * 0.08, 0], True)

    #handle the dpad / hat
    for dpad in xbc.hatValues:
        if dpad is 0:
            pass #the default state
        elif dpad is 1:
            print('N')
        elif dpad is 2:
            print('E')
        elif dpad is 3:
            print('NE')
        elif dpad is 4:
            print('S')
        elif dpad is 6:
            print('SE')
        elif dpad is 8:
            print('W')
        elif dpad is 9:
            print('NW')
        elif dpad is 12:
            print('SW')
        else:
            print(dpad, 'is not yet assigned')

    #handle the buttons
    for button in xbc.getButtonActiveList():
        if button is 0:
            print('A')
            if obj.position.z <= 50:
                obj.position.z += 0.1
        elif button is 1:
            print('B')
        elif button is 2:
            print('X')
        elif button is 3:
            print('Y')
        elif button is 4:
            print('LB')
        elif button is 5:
            print('RB')
        elif button is 6:
            print('BACK')
        elif button is 7:
            print('START')
        else:
            print(button, 'is not yet assigned')

    '''
    for button down use logic.KX_INPUT_JUST_ACTIVATED (resolves to 1)
    for button hold use logic.KX_INPUT_ACTIVE (resolves to 2)
    for button up use logic.KX_INPUT_JUST_RELEASED (resolves to 3)
    '''
    if(xbc.status == logic.KX_INPUT_JUST_ACTIVATED):
        print('use this section to do things only when a button is first pressed')
    if(xbc.status == logic.KX_INPUT_ACTIVE):
        print('use this section to do things only when a button is held')
    if(xbc.status == logic.KX_INPUT_JUST_RELEASED):
        print('use this section to do things only when a button is released')

main()
