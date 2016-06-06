'''
This script loads new images into a game engine texture dynamically. 

This can be useful for damage effects as well as streaming raw images (such as from a remote camera).

It assumes a material and image texture has already been added to the object. 

This is necessary to ensure memory is allocated for the additional images you will load into the texture. 
'''

import bge

controller = bge.logic.getCurrentController()
obj = controller.owner

def load_dynamic_texture(obj, filename, localpath='/', material_name=None):
    #get a reference to the material for the texture to be replaced
    if(material_name):
        # find the named material's id (an integer for its index) - materials are stored with an MA prefix
        material_id = bge.texture.materialID(obj, 'MA%s' % material_name)
    else:
        # otherwise, assume the first (0th) material's texture is the one to replace
        material_id = 0
        
    # get a variable pointing to the relevant texture
    object_texture = bge.texture.Texture(obj, material_id)
    
    # build the full path to the image
    path = bge.logic.expandPath('/%s' % filename)    
    
    # replace the image by assigning a the new image to its source
    object_texture.source = bge.texture.ImageFFmpeg(path)
    
    # call refresh to reload the image
    object_texture.refresh(True)
    
    # assign the texture to a global object (otherwise it will disappear after this loop completes)
    bge.logic.my_dynamic_texture = object_texture


# many examples will use this syntax to initialize video - for an image series you can use the else clause to handle additional changes
# (uncommment the print lines to see its behavior)
if not hasattr(bge.logic, 'my_dynamic_texture'):
    #print('first time')
    bge.logic.my_dynamic_texture = []
    load_dynamic_texture(obj, '/my-awesome-image-002.jpg')    
else:
    #print('additional_times')
    load_dynamic_texture(obj, '/my-awesome-image-003.jpg')    
