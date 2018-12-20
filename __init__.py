import bpy

bl_info = {
    "name" : "AssetGen",
    "author" : "??????????",
    "description" : "",
    "blender" : (2, 80, 0),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}


from . import GA_user_interface
from . import GA


class GA_Props(bpy.types.PropertyGroup):
   # sbsim_targetrig : StringProperty(name="Name of the target rig", default="")  
   # sbsim_start_frame : IntProperty(name="Simulation Start Frame", default=1)  
   # sbsim_end_frame : IntProperty(name="Simulation End Frame", default=250)  
   # sbsim_stiffness : FloatProperty(name="Stiffness", default=0.5)  
   # sbsim_bonelayer : IntProperty(name="Bone Layer", default=24)  

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
   
   ga_samplecount : bpy.props.IntProperty(name="Sample Count", default=8)  
   
   ga_unfoldhalf : bpy.props.BoolProperty(
        name = 'Unfold Half',
        description = "Will generate an UV Map for half of the low poly",
        default = True
   )
   
   ga_selectedtoactive : bpy.props.BoolProperty(
        name = 'Selected to Active',
        description = "You active selection must be your low poly",
        default = False
   )   

   ga_calculateLods : bpy.props.BoolProperty(
        name = 'Calculate LODs',
        description = "Your LODs will automatically be calculated: LOD1: 50%; LOD2: 25%, LOD3: 12.5%",
        default = True
   )     
   
   ga_LOD0 : bpy.props.IntProperty(name="LOD0 (tris)", default=500)     
   
classes = [
    GA_Props,
    GA_user_interface.GA_generatePanel,
    GA_user_interface.GA_advancedPanel,
    GA.GA_Start,		
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
