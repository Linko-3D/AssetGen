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

   ga_textureX : bpy.props.EnumProperty(
        items=[('256', '256', '256  resolution'),
               ('512', '512', '512 resolution'),
               ('1K', '1K', '1k resolution'),
               ('2K', '2K', '2k resolution'),
               ('4K', '4K', '3k resolution')],
        description="Choose texture resolution X",
        default='512'
   )
   
   ga_textureY : bpy.props.EnumProperty(
        items=[('256', '256', '256  resolution'),
               ('512', '512', '512 resolution'),
               ('1K', '1K', '1k resolution'),
               ('2K', '2K', '2k resolution'),
               ('4K', '4K', '3k resolution')],
        description="Choose texture resolution Y",
        default='512'
   )
   
   ga_samplecount : bpy.props.IntProperty(
        name="Sample Count", 
        default=8,
        min = 1		
   )  
   
   ga_unfoldhalf : bpy.props.BoolProperty(
        name = 'Unfold Half',
        description = "Will generate an UV Map for the half right of the low poly",
        default = True
   )
   
   ga_selectedtoactive : bpy.props.BoolProperty(
        name = 'Selected to Active',
        description = "Will use your active selection as the low poly",
        default = False
   )   

   ga_calculateLods : bpy.props.BoolProperty(
        name = 'Calculate LODs',
        description = "Your LODs will automatically be calculated: LOD1: 50%; LOD2: 25%, LOD3: 12.5%",
        default = True
   )     
   
   ga_LOD0 : bpy.props.IntProperty(name="LOD0 (tris)", default=500,min=1)     
   ga_LOD1 : bpy.props.IntProperty(name="LOD1 (tris)", default=0,min=0)    
   ga_LOD2 : bpy.props.IntProperty(name="LOD2 (tris)", default=0,min=0)    
   ga_LOD3 : bpy.props.IntProperty(name="LOD3 (tris)", default=0,min=0)       
   
   ga_cagesize : bpy.props.FloatProperty(
        name = 'Cage Size',
        description = "",
        default = 0.1,
        min = 0,
        max = 1		
   )       
   
   ga_edgepadding : bpy.props.IntProperty(
        name = 'Edge Padding',
        description = "",
        default = 16,
        min = 0,
        max = 64		
   )   

   ga_uvmargin : bpy.props.FloatProperty(
        name = 'UV Margin',
        description = "",
        default = 0.01,
        min = 0,
        max = 64		
   )  

   ga_uvangle : bpy.props.IntProperty(
        name = 'UV Angle',
        description = "",
        default = 45,
        min = 1,
        max = 89		
   )   

   ga_removeinside : bpy.props.BoolProperty(
        name = 'Remove Inside',
        description = "",
        default = False
   )    

   ga_groundao : bpy.props.BoolProperty(
        name = 'Ground AO',
        description = "",
        default = False
   )    
   
   ga_removeunderground : bpy.props.BoolProperty(
        name = 'Remove Underground',
        description = "",
        default = False
   )   
   
   ga_convexmesh : bpy.props.BoolProperty(
        name = 'Convex Mesh',
        description = "",
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
    GA_tools.GA_Tools_ResumX,		
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
