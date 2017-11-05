import bpy
from bpy.props import IntProperty, BoolProperty, FloatProperty, EnumProperty, PointerProperty
from bpy.types import Menu, Panel, AddonPreferences, PropertyGroup, UIList
from rna_prop_ui import PropertyPanel



class PANEL_GameAsset(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"  
    bl_label = "Game Asset Generator"  
    bl_category = "AssetGen" 
    bl_options = {'DEFAULT_CLOSED'}  


    def draw(self, context):
        icon_expand = "DISCLOSURE_TRI_RIGHT"
        icon_collapse = "DISCLOSURE_TRI_DOWN"

        #Local value
        #####################################
        q_gaenabled = True
        layout = self.layout
        myscene = context.scene.ga_property
        q_err = ""


        #Provera greske
        #####################################
        if len(bpy.context.selected_objects) == 0:
           q_err = "At least one mesh must be selected"

        if myscene.D_selected_to_active == True and len(bpy.context.selected_objects) < 2: 
           q_err = "Select at least two meshes, the active selection must be the low poly"

        for ob in bpy.context.selected_objects:
           if ob.type != 'MESH':
              q_err = "The selected object isn't a mesh"




        if q_err  != "": 
               # Display Error
               col = layout.column(align=True)
               row = col.row(align=True)
               row.alignment = 'CENTER'
               row.label(text=q_err , icon='ERROR')
               layout.row().separator()
               q_gaenabled = False


        # Draw 
        ######################################
        col_ga = layout.column(align=True)
        col0_ga = layout.column(align=True)


        #Texture Resolutions
        col_ga.label(text="Standard Texture Resolutions", icon='TEXTURE_DATA')
        row = col_ga.row()
        row.prop(myscene , 'D_texture', expand=True)
        col_ga.row().separator()
        col_ga.row().separator()

        col0_ga.prop(myscene , 'D_selected_to_active')
        col0_ga.row().separator()
        col0_ga.row().separator()

        #Basic Lod
        box_ga = layout.box()
        box_ga.label("Basic settings:")
        bcol_ga = box_ga.column(align=True)
        bcol_ga.prop(myscene , 'D_name')
        bcol_ga.row().separator()
        bcol_ga.row().separator()

        if myscene.D_selected_to_active == True:
           bcol_ga = box_ga.column(align=True)
           bcol_ga.prop(myscene , "D_LOD1")
           bcol_ga.prop(myscene , "D_LOD2")
           bcol_ga.prop(myscene , "D_LOD3")
        else:
           bcol_ga = box_ga.column(align=True)
           bcol_ga.prop(myscene , "D_LOD0")
           bcol_ga.prop(myscene , "D_LOD1")
           bcol_ga.prop(myscene , 'D_LOD2')
           bcol_ga.prop(myscene , 'D_LOD3')
        bcol_ga.row().separator()
        bcol_ga.row().separator()


        #Advanced Lod
        if myscene.gui_active_panel != "advancedLod":
           self.layout.operator('ga_button.advanced_on', icon=icon_expand)
        else:
           self.layout.operator('ga_button.advanced_off', icon=icon_collapse)
           box_gaa = layout.box()
           bcol_gaa = box_gaa.column(align=True)

           bcol_gaa.prop(myscene , 'D_cage_size') 
           bcol_gaa.prop(myscene , 'D_edge_padding') 
           bcol_gaa.prop(myscene , 'D_uv_margin') 
           bcol_gaa.prop(myscene , 'D_uv_angle')
           bcol_gaa.prop(myscene , 'D_samples') 
           bcol_gaa.row().separator()
           bcol_gaa.row().separator()

           bcol_gaa.prop(myscene , 'D_create_envelop') 
           bcol_gaa.prop(myscene , 'D_unfoldhalf') 

           bcol_gaa.prop(myscene , 'D_groundAO') 
           bcol_gaa.prop(myscene , 'D_removeunderground') 


        #Texture
        if myscene.gui_active_panel != "textureLod":
           self.layout.operator('ga_button.texture_on', icon=icon_expand)
        else:
           self.layout.operator('ga_button.texture_off', icon=icon_collapse)


           # texture
           box1_gaa = layout.box()
           bcol1_gaa = box1_gaa.column(align=True)
           bcol1_gaa.prop(myscene , 'T_mask') 
           bcol1_gaa.prop(myscene , 'T_albedo') 
           bcol1_gaa.prop(myscene , 'T_normal') 
           bcol1_gaa.prop(myscene , 'T_ao')
           
           bcol1_gaa.prop(myscene , 'T_curvature') 

           box1_gab = bcol1_gaa.box()
           bcol1_gab = box1_gab.column(align=True)

           bcol1_gab.prop(myscene , 'T_curvature_pixelwidth')
           bcol1_gab.prop(myscene , 'T_curvature_blur')
           #bcol1_gab.prop(myscene , 'T_curvature_shadows')  
           
           bcol1_gaa.prop(myscene , 'T_pointiness') 
           bcol1_gaa.prop(myscene , 'T_bent') 
           bcol1_gaa.prop(myscene , 'T_gradient') 
           bcol1_gaa.prop(myscene , 'T_opacity')

           # Curvature enabled
           if myscene.T_curvature== True:
              bcol1_gab.enabled = True
           else:
              bcol1_gab.enabled = False



        #Surface detail
        if myscene.gui_active_panel != "surfacedetail":
           self.layout.operator('ga_button.surface_on', icon=icon_expand)
        else:
           self.layout.operator('ga_button.surface_off', icon=icon_collapse)


           # surface box
           box1_gaa = layout.box()
           bcol1_gaa = box1_gaa.column(align=True)
           bcol1_gaa.prop(myscene , 'T_surface_noise') 
           bcol1_gaa.prop(myscene , 'T_surface_rock') 
           bcol1_gaa.prop(myscene , 'T_surface_sand_waves') 
           bcol1_gaa.prop(myscene , 'T_surface_wood_bark') 



        col1_ga = layout.column(align=True)
        col1_ga.scale_y = 1.5
        col1_ga.operator("scene.ga_start", icon="FILE_REFRESH")
        layout.row().separator()

        
        # GA enable/disable
        if q_gaenabled == True:
            #col_ga.enabled = True
            col1_ga.enabled = True
            #box_ga.enabled = True

        else:
            #col_ga.enabled = False
            col1_ga.enabled = False
            #box_ga.enabled = False




class ButtonAdvancedOff(bpy.types.Operator):
    bl_label = 'Advanced settings'
    bl_idname = 'ga_button.advanced_off'
    bl_description = 'Close advanced settings'
    bl_context = 'objectmode'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        context.scene.ga_property.gui_active_panel = "None"
        return {'FINISHED'}

class ButtonAdvancedOn(bpy.types.Operator):
    bl_label = 'Advanced settings'
    bl_idname = 'ga_button.advanced_on'
    bl_description = 'Open advanced settings'
    bl_context = 'objectmode'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        context.scene.ga_property.gui_active_panel = 'advancedLod'
        return {'FINISHED'}

class ButtonTextureOff(bpy.types.Operator):
    bl_label = 'Texture settings'
    bl_idname = 'ga_button.texture_off'
    bl_description = 'Close texture settings'
    bl_context = 'objectmode'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        context.scene.ga_property.gui_active_panel = "None"
        return {'FINISHED'}

class ButtonTextureOn(bpy.types.Operator):
    bl_label = 'Texture settings'
    bl_idname = 'ga_button.texture_on'
    bl_description = 'Open texture settings'
    bl_context = 'objectmode'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        context.scene.ga_property.gui_active_panel = 'textureLod'
        return {'FINISHED'}

class ButtonSurfaceOff(bpy.types.Operator):
    bl_label = 'Surface details'
    bl_idname = 'ga_button.surface_off'
    bl_description = 'Close surface details'
    bl_context = 'objectmode'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        context.scene.ga_property.gui_active_panel = "None"
        return {'FINISHED'}

class ButtonSurfaceOn(bpy.types.Operator):
    bl_label = 'Surface details'
    bl_idname = 'ga_button.surface_on'
    bl_description = 'Open surface details'
    bl_context = 'objectmode'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        context.scene.ga_property.gui_active_panel = 'surfacedetail'
        return {'FINISHED'}


