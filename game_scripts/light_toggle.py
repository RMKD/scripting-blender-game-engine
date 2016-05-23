from bge import logic

def trigger():
    controller = logic.getCurrentController()
    obj = controller.owner
    msg = controller.sensors['Message']
    if(msg.triggered):
        obj.spotsize = 45.0

def loop():
    controller = logic.getCurrentController()
    obj = controller.owner
    if obj.spotsize > 0:
        obj.spotsize -= 0.5
      
def follow():
    controller = logic.getCurrentController()
    obj = controller.owner
    scene = logic.getCurrentScene()
    focus = scene.objects['ControllerTestCone']
    axis = 2
    direction = obj.getVectTo(focus.position)
    obj.alignAxisToVect(-direction[1], axis, 0.5)
