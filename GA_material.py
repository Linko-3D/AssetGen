import bpy, os
from math import *


def MAT_texture_new(name,size, colorspc, q_alpha = True):
  

    tex = bpy.data.images.get(name)

    if  tex is None:
        tex = bpy.data.images.new(name, width=size[0], height=size[1], alpha = q_alpha)
        tex.colorspace_settings.name = colorspc
    else:
        #change resolution texture in datablock
        tex.source = 'GENERATED'
        tex.colorspace_settings.name = colorspc
        tex.generated_width = size[0]
        tex.generated_height = size[1]

    return tex





# - Remove - ///////////////////////

def DEF_remove_all():

    # Remove all object 5. layer
    bpy.context.scene.layers[1] = True
    bpy.context.scene.layers[0] = False

    bpy.ops.object.select_all(action = 'SELECT')
    bpy.ops.object.delete(use_global=False)

    bpy.context.scene.layers[0] = True
    bpy.context.scene.layers[1] = False


# - Save image- ///////////////////////


def DEF_image_save( name ):

    bpy.context.scene.render.image_settings.file_format = 'TARGA'


    #bump
    ###########
    image = bpy.data.images[name+"_"+"bump"]
    image.file_format = 'TARGA'
    path = os.path.join(os.path.dirname( bpy.data.filepath  )
, name+"_"+"bump.tga")

    image.save_render(path , bpy.context.scene)
    image.colorspace_settings.name = 'Linear'
    image.filepath = "//"+name+"_"+"bump"+".tga"
    image.source = 'FILE'



    #curvature
    ###########
    image = bpy.data.images["Viewer Node"]
    image.file_format = 'TARGA'
    path = os.path.join(os.path.dirname( bpy.data.filepath  ), name+"_"+"curvature.tga")

    image.save_render(path , bpy.context.scene)


    image1 = bpy.data.images[name+"_"+"curvature"]
    image1.colorspace_settings.name = 'Linear'
    image1.filepath = "//"+name+"_"+"curvature"+".tga"
    image1.source = 'FILE'



    #pointiness
    ###########
    image = bpy.data.images[name+"_"+"pointiness"]
    image.file_format = 'TARGA'
    path = os.path.join(os.path.dirname( bpy.data.filepath  )
, name+"_"+"pointiness.tga")

    image.save_render(path , bpy.context.scene)
    image.colorspace_settings.name = 'Linear'
    image.filepath = "//"+name+"_"+"pointiness"+".tga"
    image.source = 'FILE'



    #normal
    #########
    image = bpy.data.images[name+"_"+"normal"]
    image.file_format = 'TARGA'
    path = os.path.join(os.path.dirname( bpy.data.filepath  )
, name+"_"+"normal.tga")

    image.save_render(path , bpy.context.scene)
    image.colorspace_settings.name = 'Linear'
    image.filepath = "//"+name+"_"+"normal"+".tga"
    image.source = 'FILE'



    bpy.context.scene.render.image_settings.file_format = 'TARGA'



    #ambient_occlusion
    ##################
    image = bpy.data.images[name+"_"+"ambient_occlusion"]
    image.file_format = 'TARGA'
    path = os.path.join(os.path.dirname( bpy.data.filepath  )
, name+"_"+"ambient_occlusion.tga")

    image.save_render(path , bpy.context.scene)
    image.colorspace_settings.name = 'Linear'
    image.filepath = "//"+name+"_"+"ambient_occlusion"+".tga"
    image.source = 'FILE'




    #albedo
    ##################
    image = bpy.data.images[name+"_"+"albedo"]
    image.file_format = 'TARGA'
    path = os.path.join(os.path.dirname( bpy.data.filepath  )
, name+"_"+"albedo.tga")

    image.save_render(path , bpy.context.scene)
    image.colorspace_settings.name = 'sRGB'
    image.filepath = "//"+name+"_"+"albedo"+".tga"
    image.source = 'FILE'



    #roughness
    ##################
    image = bpy.data.images[name+"_"+"roughness"]
    image.file_format = 'TARGA'
    path = os.path.join(os.path.dirname( bpy.data.filepath  )
, name+"_"+"roughness.tga")

    image.save_render(path , bpy.context.scene)
    image.colorspace_settings.name = 'Linear'
    image.filepath = "//"+name+"_"+"roughness"+".tga"
    image.source = 'FILE'



    #albedo_details
    ##################
    image = bpy.data.images[name+"_"+"albedo_details"]
    image.file_format = 'TARGA'
    path = os.path.join(os.path.dirname( bpy.data.filepath  )
, name+"_"+"albedo_details.tga")

    image.save_render(path , bpy.context.scene)
    image.colorspace_settings.name = 'sRGB'
    image.filepath = "//"+name+"_"+"albedo_details"+".tga"
    image.source = 'FILE'


    #diffuse
    ##################  
    image = bpy.data.images[name+"_"+"diffuse"]
    image.file_format = 'TARGA'
    path = os.path.join(os.path.dirname( bpy.data.filepath  )
, name+"_"+"diffuse.tga")

    image.save_render(path , bpy.context.scene)
    image.colorspace_settings.name = 'sRGB'
    image.filepath = "//"+name+"_"+"diffuse"+".tga"
    image.source = 'FILE'


    #mask
    ##################   
    image = bpy.data.images[name+"_"+"mask"]
    image.file_format = 'TARGA'
    path = os.path.join(os.path.dirname( bpy.data.filepath  )
, name+"_"+"mask.tga")

    image.save_render(path , bpy.context.scene)
    image.colorspace_settings.name = 'sRGB'
    image.filepath = "//"+name+"_"+"mask"+".tga"
    image.source = 'FILE'


    #bent
    ##################   
    image = bpy.data.images[name+"_"+"bent"]
    image.file_format = 'TARGA'
    path = os.path.join(os.path.dirname( bpy.data.filepath  )
, name+"_"+"bent.tga")

    image.save_render(path , bpy.context.scene)
    image.colorspace_settings.name = 'Linear'
    image.filepath = "//"+name+"_"+"bent"+".tga"
    image.source = 'FILE'

    #opacity
    ##################   
    image = bpy.data.images[name+"_"+"opacity"]
    image.file_format = 'TARGA'
    path = os.path.join(os.path.dirname( bpy.data.filepath  )
, name+"_"+"opacity.tga")

    image.save_render(path , bpy.context.scene)
    image.colorspace_settings.name = 'Linear'
    image.filepath = "//"+name+"_"+"opacity"+".tga"
    image.source = 'FILE'

    #gradient
    ##################   
    image = bpy.data.images[name+"_"+"gradient"]
    image.file_format = 'TARGA'
    path = os.path.join(os.path.dirname( bpy.data.filepath  )
, name+"_"+"gradient.tga")

    image.save_render(path , bpy.context.scene)
    image.colorspace_settings.name = 'Linear'
    image.filepath = "//"+name+"_"+"gradient"+".tga"
    image.source = 'FILE'



    bpy.context.scene.render.image_settings.file_format = 'TARGA'

    return True


