import bpy

bl_info = {
    "name" : "AssetGen",
    "author" : "Srdan Ignjatovic aka zero025 (kica025@gmail.com) and Bekhoucha Danyl aka Linko (dbekhouc@gmail.com)",
    "description" : "",
    "blender" : (2, 80, 0),
    "location" : "",
    "warning" : "",
    "category" : "Game Tool"
}


from . import GA_user_interface
from . import GA_tools
from . import GA


class GA_Props(bpy.types.PropertyGroup):

   ga_autoexportglb : bpy.props.BoolProperty(
        name = 'Auto Export .glb',
        description = "After generating your game asset, the addon will automatically export a .glb. Set the path to the asset folder of your game project",
        default = False
   )
   
   ga_pathglb : bpy.props.StringProperty(
        name="Path", 
        description = "Choose where to save your file",
        default='',
        subtype = 'DIR_PATH'
   )   

   ga_textureX : bpy.props.EnumProperty(
        items=[('256', '256', '256  resolution'),
               ('512', '512', '512 resolution'),
               ('1K', '1K', '1k resolution'),
               ('2K', '2K', '2k resolution'),
               ('4K', '4K', '3k resolution')],
        description="Choose the texture resolution in Y (width)",
        default='512'
   )
   
   ga_textureY : bpy.props.EnumProperty(
        items=[('256', '256', '256  resolution'),
               ('512', '512', '512 resolution'),
               ('1K', '1K', '1k resolution'),
               ('2K', '2K', '2k resolution'),
               ('4K', '4K', '3k resolution')],
        description="Choose the texture resolution in Y (height)",
        default='512'
   )
   
   ga_samplecount : bpy.props.IntProperty(
        name="Sample Count",
		description = "Increasing this value will reduce the noise on your texture for the Ambient Occlusion and SSS, but it will increase the baking time",
        default=8,
        min = 1		
   )  
   
   ga_unfoldhalf : bpy.props.BoolProperty(
        name = 'Unfold Half',
        description = "Will generate an UV Map for the half right of the low poly to double the quality of the texture",
        default = True
   )
   
   ga_selectedtoactive : bpy.props.BoolProperty(
        name = 'Selected to Active',
        description = "NOT WORKING YET - Will use your own low poly and UV Map, the active selection must be your low poly",
        default = False
   )   

   ga_calculateLods : bpy.props.BoolProperty(
        name = 'Calculate LODs',
        description = "Your LODs will automatically be calculated like this: LOD1: 50%; LOD2: 25%, LOD3: 12.5%",
        default = True
   )     
   
   ga_LOD0 : bpy.props.IntProperty(name="LOD0 (tris)", default=1000,min=1)     
   ga_LOD1 : bpy.props.IntProperty(name="LOD1 (tris)", default=0,min=0)    
   ga_LOD2 : bpy.props.IntProperty(name="LOD2 (tris)", default=0,min=0)    
   ga_LOD3 : bpy.props.IntProperty(name="LOD3 (tris)", default=0,min=0)       
   
   ga_cagesize : bpy.props.FloatProperty(
        name = 'Cage Size',
        description = "The amount of temporary extrusion used on your low poly during the baking. A value too low will reveal intersections, a value too high can create new intersections between concave shapes and generate wavy edges. After generating your low poly if the result isn't correct, use the Solidify modifier on the low poly, change the offset to 1 and tweak the thickness by holding shift until it envelops the high poly to find the right value, then generate your asset again",
        default = 0.015,
        min = 0,
        max = 1		
   )       
   
   ga_edgepadding : bpy.props.IntProperty(
        name = 'Edge Padding',
        description = "The amount of pixels that goes beyond the UV seam. A value too low can reveal the seam, a value too high takes more time to calculate. If you generate a billboard imposter card use a value of 0",
        default = 16,
        min = 0,
        max = 64		
   )   

   ga_uvmargin : bpy.props.FloatProperty(
        name = 'UV Margin',
        description = "The space between each UV islands. A value too low won't allow to have enough edge padding for the texture beyond the seams",
        default = 0.01,
        min = 0,
        max = 64		
   )  

   ga_uvangle : bpy.props.IntProperty(
        name = 'UV Angle',
        description = "The step angle where your UV Map must create an UV Seam. If the value is too low the the UV Map will contain many individual faces, the game engine will need more calculation to display your texture. A value too high could create overlapping and not optimize the texel density (space available) resulting in a low texture quality",
        default = 45,
        min = 1,
        max = 89		
   )   

   ga_removeinside : bpy.props.BoolProperty(
        name = 'Remove Inside',
        description = "NOT WORKING YET - The addon will perform an Union boolean between every meshes that aren't merged (connected vertices), this will remove the geometry inside your model before calculating the polycount and performing an UV Mapping",
        default = False
   )    

   ga_groundao : bpy.props.BoolProperty(
        name = 'Ground AO',
        description = "NOT WORKING YET - Before the baking, the addon will generate a plane at the height of the grid to generate Ambient Occlusion like if the object were standing on the ground. Use it with every static meshes that lays on the ground",
        default = False
   )    
   
   ga_removeunderground : bpy.props.BoolProperty(
        name = 'Remove Underground',
        description = "Evertyhing bellow the grid will be removed, this will save triangles that won't be visible bellow your model",
        default = False
   )   
   
   ga_convexmesh : bpy.props.BoolProperty(
        name = 'Convex Mesh',
        description = "Every concave shapes will be delete, this allws to create low poly with very low polycount that surrounds your high poly, this is ideal for mobile games",
        default = False
   )         
   
   
classes = [
    GA_Props,
    GA_user_interface.GA_generatePanel,
    GA_user_interface.GA_advancedPanel,
    GA_user_interface.GA_toolsPanel,	
    GA.GA_Start,
    GA_tools.GA_Tools_Stylized,	
    GA_tools.GA_Tools_Wear,		
    GA_tools.GA_Tools_Optimize,		
    GA_tools.GA_Tools_ResymX,		
    GA_tools.GA_Tools_Axe,	
]


def register():
    print("register")
    for c in classes:
        bpy.utils.register_class(c)
		
    bpy.types.Scene.ga_property = bpy.props.PointerProperty(type=GA_Props)
 

def unregister():
    print("unregister")
	
    del bpy.types.Scene.ga_property

    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
