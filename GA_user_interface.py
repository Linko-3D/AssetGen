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
        col_ga.label(text="File Format")
        row = col_ga.row()
        row.prop(myscene , 'ga_file', expand=True)
        col_ga.row().separator()

        row = col_ga.row()		
        row.prop(myscene , "ga_unreal")
        col_ga.row().separator()

        row = col_ga.row()
        row.prop(myscene , 'ga_path', expand=True)
        col_ga.row().separator()		

        row = col_ga.row()		
        row.prop(myscene , "ga_baketextures")
        col_ga.row().separator()

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
        row.prop(myscene , "ga_ao")
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
		

        col_ga = layout.column(align=True)
        if myscene.ga_calculateLods == False and myscene.ga_selectedtoactive == False:
           col_ga.prop(myscene , 'ga_LOD0') 		 
           col_ga.prop(myscene , 'ga_LOD1') 
           col_ga.prop(myscene , 'ga_LOD2') 
           col_ga.prop(myscene , 'ga_LOD3') 
           col_ga.row().separator()
           row = col_ga.row()		
           row.prop(myscene , "ga_imposter")
           col_ga.row().separator()   
        elif myscene.ga_calculateLods == False and myscene.ga_selectedtoactive == True:
           col_ga.prop(myscene , 'ga_LOD1') 
           col_ga.prop(myscene , 'ga_LOD2') 
           col_ga.prop(myscene , 'ga_LOD3') 
           col_ga.row().separator()
        elif myscene.ga_calculateLods == True and myscene.ga_selectedtoactive == False:
           col_ga.prop(myscene , 'ga_LOD0') 		  
           col_ga.row().separator()		   
           row = col_ga.row()		
           row.prop(myscene , "ga_imposter")
           col_ga.row().separator() 

        row = col_ga.row()		
        row.prop(myscene , "ga_showoutput")
        col_ga.row().separator()
		
        col1_ga = layout.column(align=True)
        col1_ga.scale_y = 1.5
        col1_ga.operator("scene.ga_start", icon="FILE_REFRESH")
        col_ga.row().separator()
		
class GA_advancedPanel(bpy.types.Panel):
    bl_idname = "ga.advanced"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"  
    bl_label = "Advanced Settings"  
    bl_category = "AssetGen" 
    bl_options = {'DEFAULT_CLOSED'}   


    def draw(self, context):

        layout = self.layout
        myscene = context.scene.ga_property
  
        col_ga = layout.column(align=True)

        row = col_ga.row()
        row.prop(myscene , "ga_smoothHP")
        col_ga.row().separator()

        row = col_ga.row()
        row.prop(myscene , "ga_smoothLP")
        col_ga.row().separator()

        row = col_ga.row()		
        row.prop(myscene , "ga_centerXY")
        col_ga.row().separator()
		
        row = col_ga.row()		
        row.prop(myscene , "ga_ontheground")
        col_ga.row().separator()	

        col_ga.prop(myscene , 'ga_cagesize') 
        col_ga.prop(myscene , 'ga_edgepadding') 
        col_ga.prop(myscene , 'ga_uvmargin') 
        col_ga.prop(myscene , 'ga_uvangle')
        col_ga.row().separator()		

        row = col_ga.row()		
        row.prop(myscene , "ga_removeinside")
        col_ga.row().separator()	

        row = col_ga.row()		
        row.prop(myscene , "ga_groundao")
        col_ga.row().separator()

        row = col_ga.row()		
        row.prop(myscene , "ga_removeunderground")
        col_ga.row().separator()
		
        col_ga.row().separator()		
		
class GA_toolsPanel(bpy.types.Panel):
    bl_idname = "ga.tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"  
    bl_label = "Tools"  
    bl_category = "AssetGen" 
    bl_options = {'DEFAULT_CLOSED'}   


    def draw(self, context):

        layout = self.layout
        myscene = context.scene.ga_property

		
		#-----------------------------------------------------------
        col_ga = layout.column(align=True)		
        col_ga.label(text="Effects:")		
		
        col1_ga = layout.column(align=True)
        col1_ga.scale_y = 1.0
        col1_ga.operator("scene.ga_toolshighpoly", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_toolpolish", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_toolswear", icon="FILE_REFRESH")			

		#-----------------------------------------------------------	
        col_ga = layout.column(align=True)		
        col_ga.label(text="Quick Operations:")		
		
        col1_ga = layout.column(align=True)
        col1_ga.scale_y = 1.0
        col1_ga.operator("scene.ga_toolapply", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_toolresymx", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_toolfixnormals", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_toolflipnormals", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_toolunion", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_tooldyntopo", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_tooloptimize", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_tooldissolveunnecessary", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_toolontheground", icon="FILE_REFRESH")
		#-----------------------------------------------------------	
        col_ga = layout.column(align=True)		
        col_ga.label(text="Simple Meshes:")		
		
        col1_ga = layout.column(align=True)
        col1_ga.scale_y = 1.0
        col1_ga.operator("scene.ga_toolbasemesh", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_toolboltcubic", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_toolchain1", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_toolchain2", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_toolcrack", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_toolextrudedshape", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_toolhair", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_toolring", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_toolstrap", icon="FILE_REFRESH")

		#-----------------------------------------------------------	
        col_ga = layout.column(align=True)		
        col_ga.label(text="Weapons:")		
		
        col1_ga = layout.column(align=True)
        col1_ga.scale_y = 1.0
        col1_ga.operator("scene.ga_toolaxe", icon="FILE_REFRESH")
        #col1_ga.operator("scene.ga_toolshield", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_toolshoulder", icon="FILE_REFRESH")
        col1_ga.operator("scene.ga_toolsword", icon="FILE_REFRESH")
		
		#-----------------------------------------------------------	
        col_ga = layout.column(align=True)		
        col_ga.label(text="Accessories:")		
		
        col1_ga = layout.column(align=True)
        col1_ga.scale_y = 1.0
        col1_ga.operator("scene.ga_toolpotion", icon="FILE_REFRESH")