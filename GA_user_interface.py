import bpy
from bpy.props import IntProperty, BoolProperty, FloatProperty, EnumProperty, PointerProperty
from bpy.types import Menu, Panel, AddonPreferences, PropertyGroup, UIList
from rna_prop_ui import PropertyPanel



class GA_generatePanel(bpy.types.Panel):
    bl_idname = "ga.generate"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"  
    bl_label = "Game Asset Generator"  
    bl_category = "AssetGen" 
 


    def draw(self, context):
        icon_expand = "DISCLOSURE_TRI_RIGHT"
        icon_collapse = "DISCLOSURE_TRI_DOWN"

        layout = self.layout
        myscene = context.scene.ga_property
  
        col_ga = layout.column(align=True)
   
        #Texture Resolutions
        col_ga.label(text="Resolution X (Width)", icon='TEXTURE_DATA')
        row = col_ga.row()
        row.prop(myscene , 'ga_textureX', expand=True)
        col_ga.row().separator()
		
        col_ga.label(text="Resolution Y (Height)", icon='TEXTURE_DATA')
        row = col_ga.row()
        row.prop(myscene , 'ga_textureY', expand=True)
        col_ga.row().separator()
		
        row = col_ga.row()		
        row.prop(myscene , "ga_samplecount")
        col_ga.row().separator()	
		
        row = col_ga.row()		
        row.prop(myscene , "ga_unfoldhalf")
        col_ga.row().separator()

        row = col_ga.row()		
        row.prop(myscene , "ga_selectedtoactive")
        col_ga.row().separator()

        row = col_ga.row()		
        row.prop(myscene , "ga_calculateLods")
        col_ga.row().separator()		
		
        row = col_ga.row()		
        row.prop(myscene , "ga_LOD0")
        col_ga.row().separator()		
		
        col1_ga = layout.column(align=True)
        col1_ga.scale_y = 1.5
        col1_ga.operator("scene.ga_start", icon="FILE_REFRESH")
        layout.row().separator()
		

        col_ga.row().separator()
		
class GA_advancedPanel(bpy.types.Panel):
    bl_idname = "ga.advanced"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"  
    bl_label = "Advanced Settings"  
    bl_category = "AssetGen" 
 


    def draw(self, context):

        layout = self.layout
        myscene = context.scene.ga_property
  
        col_ga = layout.column(align=True)
   
 
        col_ga.row().separator()		