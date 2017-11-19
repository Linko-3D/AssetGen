#This states the metadata for the plugin
bl_info = {
    "name": "AssetGen",
    "author": "Developed by Srdan Ignjatovic aka zero025 (kica025@gmail.com) and surpervised by Danyl Bekhoucha aka Linko (dbekhouc@gmaiL.com)",
    "version": (0, 1),
    "blender": (2, 79),
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
        default='1K'
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
        description = "Maximum polycount of the LOD0 (closest to the camera). AssetGen will reduce this polycount if it detects unacessary edges",
        default = 1000,
        min = 1,
        max = 100000
    )
    D_LOD1 = bpy.props.IntProperty(
        name = 'LOD1',
        description = "Maximum polycount  of the LOD1 (in average 50% of the LOD0)",
        default = 0,
        min = 0,
        max = 100000
    )
    D_LOD2 = bpy.props.IntProperty(
        name = 'LOD2',
        description = "Maximum polycount  of the LOD2 (in average 25% of the LOD0)",
        default = 0,
        min = 0,
        max = 100000
    )
    D_LOD3 = bpy.props.IntProperty(
        name = 'LOD3',
        description = "Maximum polycount  of the LOD3 (in average 12.5% of the LOD0)",
        default = 0,
        min = 0,
        max = 100000
    )

    D_cage_size = bpy.props.FloatProperty(
        name = 'Cage size',
        description = "Size (inflate) of the low poly during the baking to avoid intersecting with the high poly",
        default = 0.1,
        min = 0.00,
        max = 1.00
    )
    D_edge_padding = bpy.props.FloatProperty(
        name = 'Edge padding',
        description = "Number of pixels that goes above your UV seams",
        default = 16,
        min = 0.00,
        max = 100.00
    )
    D_uv_margin = bpy.props.FloatProperty(
        name = 'UV margin',
        description = "Space between UVs islands",
        default = 0.03,
        min = 0.000,
        max = 1.000
    )
    D_uv_angle = bpy.props.FloatProperty(
        name = 'UV angle',
        description = "Define at which angle from the world space a seam must be added. Lower value = more chunks and less perfs, higher = potential overlapping and lose in Texel density.",
        default = 45,
        min = 0,
        max = 89
    )
    D_samples = bpy.props.IntProperty(
        name = 'Samples',
        description = "Quality of the ambient occlusion, normal map and bent map. Other textures use 1 sample",
        default = 16,
        min = 0,
        max = 100000
    )


    DT_exp = bpy.props.EnumProperty(
        items=[('FBX', 'FBX', 'FBX'),
               ('OBJ', 'OBJ', 'OBJ')],
        description="Choose export file",
        default='OBJ'
    )


    DT_pathobj = bpy.props.StringProperty(
        name="Mesh path", 
        description = "Choose where to save your file",
        default='',
        subtype = 'DIR_PATH'
    )
    DT_pathntoc = bpy.props.StringProperty(
        name="Nor path", 
        description = "Open a Tangent Space Normal map",
        default='',
        subtype = 'FILE_PATH'
    )
    DT_exportcenterpos = bpy.props.BoolProperty(
        name = 'Center position',
        description = "Center position",
        default = True
    )
    DT_exporttexture = bpy.props.BoolProperty(
        name = 'Textures in a subfolder',
        description = "Texture in subfolder",
        default = True
    )

    DT_exportpathtexture = bpy.props.StringProperty(
        name="Textures", 
        description = "Texture in subfolder.",
        default='//Textures',
        subtype = 'DIR_PATH'
    )



    D_create_envelop = bpy.props.BoolProperty(
        name = 'Create envelop',
        description = "Will try to remove every intersections of separated meshes. Can bug with smalls meshes or not intersecting enough",
        default = True
    )
    D_groundAO = bpy.props.BoolProperty(
        name = 'Ground AO',
        description = "Generate ambient occlusion from the grid, ideal for static meshes that stand on the ground",
        default = False
    )

    D_removeunderground = bpy.props.BoolProperty(
        name = 'Remove underground',
        description = "Remove the invisible part of the mesh that intersect with the ground (grid) to avoid waste of polygons and texture space",
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
        description = "The mask map will bake the colors of your asset and use it as a mask to apply different gradients with the Game Asset Material tool",
        default = True
    )
    T_albedo = bpy.props.BoolProperty(
        name = 'Albedo',
        description = "Bakes the color of the high poly ideal for scanned assets otherwise it iss recommended to do the albedo after the low poly",
        default = False
    )
    T_normal  = bpy.props.BoolProperty(
        name = 'Normal',
        description = "Will keep every details of your hight poly",
        update=def_normal_Update,
        default = True
    )

    T_ao = bpy.props.BoolProperty(
        name = 'Ambient Occlusion',
        description = "Generates shadows on parts close to each others, works on any lighting conditions",
        default = True
    )
    T_ao_denoising = bpy.props.BoolProperty(
        name = 'Activate denoising',
        description = "",
        default = True
    )
    T_ao_colorsigma = bpy.props.FloatProperty(
        name = 'Color Sigma',
        description = "",
        default = 0.1,
        min = 0,
        max = 3
    )
    T_ao_spacesigma = bpy.props.FloatProperty(
        name = 'Space Sigma',
        description = "",
        default = 3,
        min = 0,
        max = 30
    )




    T_pointiness = bpy.props.BoolProperty(
        name = 'Pointiness',
        description = "Generates a vertex based curvature map (quality depends on the polycount of the high poly)",
        default = False
    )
    T_bent = bpy.props.BoolProperty(
        name = 'Bent',
        description = "Bake the orientation of the faces from the world space. It is used to create effects (dust, snow, etc) and fake top lighting in non-PBR games",
        default = True
    )
    T_gradient = bpy.props.BoolProperty(
        name = 'Gradient',
        description = "Bake a dark bottom and white top of your object. This method is often used in stylized games especially view from top",
        default = False
    )
    T_opacity = bpy.props.BoolProperty(
        name = 'Opacity',
        description = "Bake in white non opaque part and black parts that needs to be transparent. Most game engines can read the opacity directly on the Albedo",
        default = False
    )
    T_curvature = bpy.props.BoolProperty(
        name = 'Curvature',
        description = "This effect will composite the normal map to generate a greyscale with convex shapes in white and concave in dark",
        update=def_curvature_Update,
        default = True
    )


    T_curvature_pixelwidth = bpy.props.IntProperty(
        name = 'Pixel width',
        description = "The width in pixel of the white lines generated from concave shapes and black from convex shapes. Increasing this value can be useful to bake a sprite from an high poly to a plane",
        default = 1,
        min = 1,
        max = 8
    )
    T_curvature_shadows = bpy.props.BoolProperty(
        name = 'Shadows',
        description = "",
        default = False
    )
    T_curvature_blur = bpy.props.FloatProperty(
        name = 'Blur',
        description = "Amount of relative blur to avoid getting aliasing and/or lines too contrasted",
        default = 0,
        min = 0.000,
        max = 1.000
    )
    T_surface_noise = bpy.props.BoolProperty(
        name = 'Noise',
        description = "",
        update=def_surface,
        default = False
    )
    T_surface_rock = bpy.props.BoolProperty(
        name = 'Rock',
        description = "",
        update=def_surface,
        default = False
    )
    T_surface_sand_waves  = bpy.props.BoolProperty(
        name = 'Sand waves',
        description = "",
        update=def_surface,
        default = False
    )
    T_surface_wood_bark  = bpy.props.BoolProperty(
        name = 'Wood bark',
        description = "",
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

    T_symmet_clip= bpy.props.BoolProperty(
        name = 'Clipping',
        default = False
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

    T_normalize_R = bpy.props.BoolProperty(
        name = 'R',
        default = True
    )
    T_normalize_G = bpy.props.BoolProperty(
        name = 'G',
        default = True
    )
    T_normalize_B = bpy.props.BoolProperty(
        name = 'B',
        default = True
    )
    T_pathnormalize = bpy.props.StringProperty(
        name="Image", 
        description = "Open image",
        default='',
        subtype = 'FILE_PATH'
    )

    T_decimate_qratio = bpy.props.BoolProperty(
        name = 'Use ratio',
        default = True
    )
    T_decimate_ratio = bpy.props.FloatProperty(
        name = 'Ratio',
        default = 0.8,
        min = 0.000,
        max = 1.000
    )
    T_decimate_polycount = bpy.props.IntProperty(
        name = 'Polycount',
        default = 1000,
        min = 1,
        max = 100000
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

print("> ", __name__, "imported successfully")
