#This states the metadata for the plugin
bl_info = {
    "name": "AssetGen",
    "author": "Srđan Ignjatović (kica025@gmail.com) and Danyl Bekhoucha (dbekhouc@gmaiL.com)",
    "version": (0, 1),
    "blender": (2, 78),
    "api": 39347,
    "location": "3D View > Object Mode > Tools > AssetGen",
    "description": "Game development tools",
    "warning": "Beta",
    "tracker_url": "",
    "category": "Object"
}

if "bpy" in locals():
    import imp
    imp.reload(GA_user_interface)
    imp.reload(GM_user_interface)
    imp.reload(GT_user_interface)
    imp.reload(GA_material)
    imp.reload(GA_shader)
    imp.reload(GA_composite)
    imp.reload(GM_def)
    imp.reload(GA)
else:
    from . import GA_user_interface
    from . import GM_user_interface
    from . import GT_user_interface
    from . import GA_material
    from . import GA_shader
    from . import GA_composite
    from . import GM_def
    from . import GA
    
import bpy
from .GA_shader import DEF_surface_add


def def_curvature_Update(self, context):
    if self.T_curvature == True:
       self.T_normal = True
def def_normal_Update(self, context):
    if self.T_normal == False:
       self.T_curvature = False


def def_surface(self, context):
       DEF_surface_add(context)





# Settings
class GA_Property(bpy.types.PropertyGroup):

    gui_active_panel = bpy.props.StringProperty(
        name="gui_active_panel", 
        default="None"
    )

    
    #GAME ASSET
    ############

    D_texture = bpy.props.EnumProperty(
        items=[('256', '256', '256  resolution'),
               ('512', '512', '512 resolution'),
               ('1K', '1K', '1k resolution'),
               ('2K', '2K', '2k resolution'),
               ('4K', '4K', '3k resolution')],
        #update=def_Texture_Update,
        description="Choose texture resolution",
        default='2K'
    )

    D_selected_to_active= bpy.props.BoolProperty(
        name = 'Selected to active',
        description = "Use this if you have a low poly already. Your low poly must be the active selection",
        default = False
    )

    D_name = bpy.props.StringProperty(
        name="Name", 
        description = "Prefix name of your game asset and textures",
        default="game_asset"
    )

    D_LOD0 = bpy.props.IntProperty(
        name = 'LOD0',
        description = "Polycount of the LOD0 (closest to the camera)",
        default = 1000,
        min = 1,
        max = 100000
    )
    D_LOD1 = bpy.props.IntProperty(
        name = 'LOD1',
        description = "Polycount of the LOD1 (in average 60% of the LOD0)",
        default = 0,
        min = 0,
        max = 100000
    )
    D_LOD2 = bpy.props.IntProperty(
        name = 'LOD2',
        description = "Polycount of the LOD1 (in average 30% of the LOD0)",
        default = 0,
        min = 0,
        max = 100000
    )

    D_cage_size = bpy.props.FloatProperty(
        name = 'Cage size',
        description = "",
        default = 0.05,
        min = 0.00,
        max = 1.00
    )
    D_edge_padding = bpy.props.FloatProperty(
        name = 'Edge padding',
        description = "",
        default = 16,
        min = 0.00,
        max = 100.00
    )
    D_uv_margin = bpy.props.FloatProperty(
        name = 'UV margin',
        description = "",
        default = 0.005,
        min = 0.000,
        max = 1.000
    )
    D_uv_angle = bpy.props.FloatProperty(
        name = 'UV angle',
        description = "",
        default = 45,
        min = 0,
        max = 89
    )
    D_samples = bpy.props.IntProperty(
        name = 'Samples',
        description = "Quality of the Ambient Occlusion, other textures use 1 sample",
        default = 32,
        min = 0,
        max = 100000
    )


    DT_pathobj = bpy.props.StringProperty(
        name="File path", 
        description = "Choose where to save the file",
        default='',
        subtype = 'DIR_PATH'
    )
    DT_pathntoc = bpy.props.StringProperty(
        name="Nor path", 
        description = "Open a Tangent Space Normal map",
        default='',
        subtype = 'FILE_PATH'
    )

    D_create_envelop = bpy.props.BoolProperty(
        name = 'Create envelop',
        description = "Will try to remove every intersections of separated meshes",
        default = True
    )
    D_groundAO = bpy.props.BoolProperty(
        name = 'Ground AO',
        description = "Generate ambient occlusion from the grid, ideal from static meshes that stand on the ground",
        default = False
    )

    D_removeunderground = bpy.props.BoolProperty(
        name = 'Remove underground',
        description = "Remove the invisible part of the mesh that intersect with the ground to avoid waste of polygons and texture space",
        default = False
    )


    D_unfoldhalf = bpy.props.BoolProperty(
        name = 'Unfold Half',
        description = "Unfold half of your asset in +X, ideal for symmetrical assets to save texture space",
        default = False
    )

    ##################################



    T_mask = bpy.props.BoolProperty(
        name = 'Mask',
        description = "The mask map will bake the colors of your asset and use it as a mask to apply different material with the Game Asset Material tool ",
        default = True
    )
    T_albedo = bpy.props.BoolProperty(
        name = 'Albedo',
        default = False
    )
    T_normal  = bpy.props.BoolProperty(
        name = 'Normal',
        update=def_normal_Update,
        default = True
    )
    T_ao = bpy.props.BoolProperty(
        name = 'Ambient Occlusion',
        default = True
    )
    T_pointiness = bpy.props.BoolProperty(
        name = 'Pointiness',
        default = False
    )
    T_roughness = bpy.props.BoolProperty(
        name = 'Roughness',
        default = False
    )
    T_bent = bpy.props.BoolProperty(
        name = 'Bent',
        default = False
    )
    T_gradient = bpy.props.BoolProperty(
        name = 'Gradient',
        default = False
    )
    T_opacity = bpy.props.BoolProperty(
        name = 'Opacity',
        default = False
    )
    T_curvature = bpy.props.BoolProperty(
        name = 'Curvature',
        update=def_curvature_Update,
        default = True
    )


    T_curvature_pixelwidth = bpy.props.IntProperty(
        name = 'Pixel width',
        description = "",
        default = 1,
        min = 1,
        max = 8
    )
    T_curvature_shadows = bpy.props.BoolProperty(
        name = 'Shadows',
        default = False
    )
    T_curvature_blur = bpy.props.FloatProperty(
        name = 'Blur',
        default = 0,
        min = 0.000,
        max = 1.000
    )


    T_surface_noise = bpy.props.BoolProperty(
        name = 'Noise',
        update=def_surface,
        default = False
    )
    T_surface_rock = bpy.props.BoolProperty(
        name = 'Rock',
        update=def_surface,
        default = False
    )
    T_surface_sand  = bpy.props.BoolProperty(
        name = 'Sand waves',
        update=def_surface,
        default = False
    )
    T_surface_woodbark  = bpy.props.BoolProperty(
        name = 'Wood bark',
        update=def_surface,
        default = False
    )





    T_ntoc = bpy.props.IntProperty(
        name = 'Width(px)',
        description = "",
        default = 1,
        min = 1,
        max = 100
    )

    T_ntocrel = bpy.props.FloatProperty(
        name = 'Relative blur',
        default = 0,
        min = 0.000,
        max = 10.000
    )

    T_symmet_X = bpy.props.BoolProperty(
        name = 'X',
        default = True
    )
    T_symmet_Y = bpy.props.BoolProperty(
        name = 'Y',
        default = False
    )
    T_symmet_Z = bpy.props.BoolProperty(
        name = 'Z',
        default = False
    )



 


def register():
    bpy.utils.register_module(__name__)
   
    GM_def.register()

    bpy.types.Scene.ga_property = bpy.props.PointerProperty(type=GA_Property)


def unregister():
    bpy.utils.unregister_module(__name__)


    GM_def.unregister()

    del bpy.types.Scene.ga_property 

if __name__ == "__main__":
    register()

print(">>>>>>>>>>> Import Finished", __name__, "<<<<<<<<<<<<")
