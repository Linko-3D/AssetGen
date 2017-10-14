import bpy,os, shutil
from bpy.props import IntProperty, BoolProperty, FloatProperty, EnumProperty, PointerProperty
from bpy.types import Menu, Panel, AddonPreferences, PropertyGroup, UIList
from rna_prop_ui import PropertyPanel




class PANEL_GameTools(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"  
    bl_label = "Game Asset Tools"  
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


        #File export obj
        if myscene.gui_active_panel != "fileexport":
           self.layout.operator('ga_button.fileexport_on', icon=icon_expand)
        else:
           self.layout.operator('ga_button.fileexport_off', icon=icon_collapse)
           box_ga = layout.box()
           bcol_ga = box_ga.column(align=True)

           row1 = bcol_ga.row()
           row1.prop(myscene , 'DT_exp', expand=True)
           bcol_ga.row().separator()
           bcol_ga.row().separator()

           bcol_ga.prop(myscene , 'DT_pathobj')
           bcol_ga.row().separator()
           bcol_ga.row().separator()
           bcol_ga.prop(myscene , 'DT_exportcenterpos')
           bcol_ga.prop(myscene , 'DT_exporttexture')
           bcol_ga.prop(myscene , 'DT_exportpathtexture')

           bcol_ga.row().separator()
           bcol_ga.row().separator()
           bcol_ga.operator("ga_tools.export", icon='EXPORT')
           bcol_ga.row().separator()

        #NtoC
        if myscene.gui_active_panel != "NtoC":
           self.layout.operator('ga_button.ntoc_on', icon=icon_expand)
        else:
           self.layout.operator('ga_button.ntoc_off', icon=icon_collapse)
           box1_ga = layout.box()
           bcol1_ga = box1_ga.column(align=True)

           bcol1_ga.prop(myscene , 'DT_pathntoc')
           bcol1_ga.row().separator()
           bcol1_ga.row().separator()
           bcol1_ga.prop(myscene , 'T_ntoc')
           bcol1_ga.prop(myscene , 'T_ntocrel')
           bcol1_ga.row().separator()
           bcol1_ga.row().separator()
           bcol1_ga.prop(myscene , 'T_curvature_shadows') 
           bcol1_ga.row().separator()
           bcol1_ga.row().separator()
 
           bcol1_ga.operator("ga_tools.ntoc", icon='EXPORT')
           bcol1_ga.row().separator()

        #Resimetrize
        if myscene.gui_active_panel != "Resim":
           self.layout.operator('ga_button.resim_on', icon=icon_expand)
        else:
           self.layout.operator('ga_button.resim_off', icon=icon_collapse)
           box1_ga = layout.box()
           bcol1_ga = box1_ga.column(align=True)


           bcol1_ga.label(text="Axis:")
           bcol1_ga.prop(myscene , 'T_symmet_clip')
           bcol1_ga.row().separator()
           bcol1_ga.prop(myscene , 'T_symmet_X')
           bcol1_ga.row().separator()
           bcol1_ga.prop(myscene , 'T_symmet_Y')
           bcol1_ga.row().separator()
           bcol1_ga.prop(myscene , 'T_symmet_Z')
           bcol1_ga.row().separator()
           bcol1_ga.row().separator()

           bcol1_ga.operator("ga_tools.resimetrize", icon='EXPORT')
           bcol1_ga.row().separator()


        #Normalize
        if myscene.gui_active_panel != "Normalize":
           self.layout.operator('ga_button.normalize_on', icon=icon_expand)
        else:
           self.layout.operator('ga_button.normalize_off', icon=icon_collapse)
           box1_ga = layout.box()
           bcol1_ga = box1_ga.column(align=True)

           bcol1_ga.prop(myscene , 'T_pathnormalize')
           bcol1_ga.row().separator()
           bcol1_ga.row().separator()

           bcol1_ga.label(text="Shannels:")
           bcol1_ga.prop(myscene , 'T_normalize_R')
           bcol1_ga.row().separator()
           bcol1_ga.prop(myscene , 'T_normalize_G')
           bcol1_ga.row().separator()
           bcol1_ga.prop(myscene , 'T_normalize_B')
           bcol1_ga.row().separator()
           bcol1_ga.row().separator()

           bcol1_ga.operator("ga_tools.normalize", icon='EXPORT')
           bcol1_ga.row().separator()

        #Quick decimation
        if myscene.gui_active_panel != "Decimation":
           self.layout.operator('ga_button.decimation_on', icon=icon_expand)
        else:
           self.layout.operator('ga_button.decimation_off', icon=icon_collapse)
           box1_ga = layout.box()
           bcol1_ga = box1_ga.column(align=True)


           bcol1_ga.prop(myscene , 'T_decimate_qratio')
           bcol1_ga.row().separator()
           bcol1_ga.row().separator()
           bcol1_ga.prop(myscene , 'T_decimate_ratio')
           bcol1_ga.prop(myscene , 'T_decimate_polycount')
           bcol1_ga.row().separator()
           bcol1_ga.row().separator()


           bcol1_ga.operator("ga_tools.qdecimation", icon='EXPORT')
           bcol1_ga.row().separator()






        layout.row().separator()
        col_gt = layout.column(align=True)
        col_gt.operator("ga_tools.polish_sculpt")
        col_gt.operator("ga_tools.2d_mesh")
        col_gt.operator("ga_tools.make_tileable_texture")
        col_gt.operator("ga_tools.make_generate_box")
        layout.row().separator()
        #col_gt.operator("ga_tools.ga_import_material")
        layout.row().separator()


# - Decimation ------------------------------------------------
class ButtonDecimationOff(bpy.types.Operator):
    bl_label = 'Quick decimation'
    bl_idname = 'ga_button.decimation_off'
    bl_context = 'objectmode'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        context.scene.ga_property.gui_active_panel = "None"
        return {'FINISHED'}

class ButtonDecimationOn(bpy.types.Operator):
    bl_label = 'Quick decimation'
    bl_idname = 'ga_button.decimation_on'
    bl_context = 'objectmode'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        context.scene.ga_property.gui_active_panel = 'Decimation'
        return {'FINISHED'}


class QDecimation(bpy.types.Operator):
    bl_idname = "ga_tools.qdecimation"
    bl_label = "Quick decimation"

    def execute(self, context):

       myscene = context.scene.ga_property

       bpy.ops.object.modifier_add(type='TRIANGULATE')
       bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Triangulate")

       obj = bpy.context.active_object
       HP_polycount = len(obj.data.polygons)

       decimation = (myscene.T_decimate_polycount / HP_polycount)

       bpy.ops.object.modifier_add(type='DECIMATE')

       if myscene.T_decimate_qratio == True:
         bpy.context.object.modifiers["Decimate"].ratio = myscene.T_decimate_ratio
       else:
         bpy.context.object.modifiers["Decimate"].ratio = decimation

       bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
       bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")


       return {'FINISHED'}



# - Normalize ------------------------------------------------
class ButtonNormalizeOff(bpy.types.Operator):
    bl_label = 'Normalize'
    bl_idname = 'ga_button.normalize_off'
    bl_context = 'objectmode'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        context.scene.ga_property.gui_active_panel = "None"
        return {'FINISHED'}

class ButtonNormalizeOn(bpy.types.Operator):
    bl_label = 'Normalize'
    bl_idname = 'ga_button.normalize_on'
    bl_context = 'objectmode'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        context.scene.ga_property.gui_active_panel = 'Normalize'
        return {'FINISHED'}


class Normalize(bpy.types.Operator):
    bl_idname = "ga_tools.normalize"
    bl_label = "Normalize"

    def execute(self, context):

       # ucitaj scenu
       scene = bpy.context.scene
       scene.use_nodes = True

       nodes = scene.node_tree.nodes
       links = scene.node_tree.links

       myscene = context.scene.ga_property


       # clear
       ##############################
       while(nodes): nodes.remove(nodes[0])


       # add image 
       ##############################
       q_i = bpy.data.images.load(myscene.T_pathnormalize, check_existing=False)
       #q_i.colorspace_settings.name = 'Linear'


       c_imgNORMAL = scene.node_tree.nodes.new('CompositorNodeImage')
       c_imgNORMAL.image = q_i
       c_imgNORMAL.location = (-300 ,0)


       # add rgba
       #################################
       c_rgb = scene.node_tree.nodes.new('CompositorNodeSepRGBA')
       c_rgb.location = (0 ,0)

       # add normalize
       #################################
       c_norm1 = scene.node_tree.nodes.new('CompositorNodeNormalize')
       c_norm1.location = (300 ,100)

       c_norm2 = scene.node_tree.nodes.new('CompositorNodeNormalize')
       c_norm2.location = (300 ,0)

       c_norm3 = scene.node_tree.nodes.new('CompositorNodeNormalize')
       c_norm3.location = (300 ,-100)


       # add rgbacombine
       #################################
       c_combrgb = scene.node_tree.nodes.new('CompositorNodeCombRGBA')
       c_combrgb.location = (500 ,0)



       # add NodeViewer
       ##############################
       c_view = scene.node_tree.nodes.new('CompositorNodeViewer')
       c_view.location = (700,0)  


       if myscene.T_normalize_R == True:
          c_norm1.mute = False
       else:
          c_norm1.mute = True

       if myscene.T_normalize_G == True:
          c_norm2.mute = False
       else:
          c_norm2.mute = True

       if myscene.T_normalize_B == True:
          c_norm3.mute = False
       else:
          c_norm3.mute = True



       links.new( c_imgNORMAL.outputs['Image'],
                  c_rgb.inputs['Image'])

       links.new( c_rgb.outputs['R'],
                  c_norm1.inputs['Value'])
       links.new( c_rgb.outputs['G'],
                  c_norm2.inputs['Value'])
       links.new( c_rgb.outputs['B'],
                  c_norm3.inputs['Value'])
   

       links.new( c_norm1.outputs['Value'],
                  c_combrgb.inputs[0])
       links.new( c_norm2.outputs['Value'],
                  c_combrgb.inputs[1])
       links.new( c_norm3.outputs['Value'],
                  c_combrgb.inputs[2])


       links.new( c_combrgb.outputs['Image'],
                  c_view.inputs['Image'])


       # Ako je otvoren NODE_EDITOT
       #  prebaci ga u composite
       ############################
       editorcheck = False
       for area in bpy.context.screen.areas :
           if area.type == 'NODE_EDITOR' :
               if area.spaces.active.tree_type != 'CompositorNodeTree':
                   area.spaces.active.tree_type = 'CompositorNodeTree'
               editorcheck = True

       # Ako nije otvoren NODE_EDITOT
       #  u postojecem prvo NODE EDITOR
       #  pa split
       #  pa VIEW 3D
       # prebaci u composite
       ############################
       if editorcheck == False:
          try:
           bpy.context.area.type='NODE_EDITOR'
           bpy.ops.screen.area_split(factor=0.5)
           bpy.context.area.type='VIEW_3D'

           for area in bpy.context.screen.areas :
               if area.type == 'NODE_EDITOR' :
                   if area.spaces.active.tree_type != 'CompositorNodeTree':
                       area.spaces.active.tree_type = 'CompositorNodeTree'
          except:
           pass





       return {'FINISHED'}



# - Resimetrize ------------------------------------------------
class ButtonResimOff(bpy.types.Operator):
    bl_label = 'Symmetrize'
    bl_idname = 'ga_button.resim_off'
    bl_context = 'objectmode'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        context.scene.ga_property.gui_active_panel = "None"
        return {'FINISHED'}

class ButtonResimOn(bpy.types.Operator):
    bl_label = 'Symmetrize'
    bl_idname = 'ga_button.resim_on'
    bl_context = 'objectmode'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        context.scene.ga_property.gui_active_panel = 'Resim'
        return {'FINISHED'}


class Resimetrize(bpy.types.Operator):
    bl_idname = "ga_tools.resimetrize"
    bl_label = "Symmetrize"

    def execute(self, context):

       myscene = context.scene.ga_property

       ##################

       
       bpy.ops.object.mode_set(mode = 'OBJECT')
       bpy.ops.object.convert(target='MESH')

       bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

       for obj in bpy.context.selected_objects:
    
           bpy.context.scene.objects.active = obj

           if myscene.T_symmet_X == True:

              bpy.ops.object.mode_set(mode = 'OBJECT')

              bpy.context.object.location[0] = 0

              bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
              bpy.ops.object.mode_set(mode = 'EDIT')
              bpy.ops.mesh.select_all(action = 'SELECT')
              bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_inner=True, clear_outer=False, xstart=376, xend=381, ystart=133, yend=62)

              bpy.ops.mesh.select_mode(type="FACE")
              bpy.ops.mesh.delete(type='FACE')

              bpy.ops.mesh.select_all(action = 'SELECT')
              bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_inner=True, clear_outer=False, xstart=376, xend=381, ystart=133, yend=62)

              bpy.ops.mesh.select_all(action = 'SELECT')
        
              bpy.ops.object.mode_set(mode = 'OBJECT')
        
    
           if myscene.T_symmet_Y == True :
              bpy.ops.object.mode_set(mode = 'OBJECT')

              bpy.context.object.location[0] = 0

              bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
              bpy.ops.object.mode_set(mode = 'EDIT')
              bpy.ops.mesh.select_all(action = 'SELECT')
              bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(0, 1, 0), clear_inner=True, clear_outer=False, xstart=283, xend=350, ystart=372, yend=372)

              bpy.ops.mesh.select_mode(type="FACE")
              bpy.ops.mesh.delete(type='FACE')

              bpy.ops.mesh.select_all(action = 'SELECT')
              bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(0, 1, 0), clear_inner=True, clear_outer=False, xstart=283, xend=350, ystart=372, yend=372)


              bpy.ops.mesh.select_all(action = 'SELECT')
        
              bpy.ops.object.mode_set(mode = 'OBJECT')
        
        
           if myscene.T_symmet_Z == True :

              bpy.ops.object.mode_set(mode = 'OBJECT')

              bpy.context.object.location[0] = 0

              bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
              bpy.ops.object.mode_set(mode = 'EDIT')
              bpy.ops.mesh.select_all(action = 'SELECT')
              bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(0, 0, 1), clear_inner=True, clear_outer=False, xstart=539, xend=597, ystart=336, yend=336)

              bpy.ops.mesh.select_mode(type="FACE")
              bpy.ops.mesh.delete(type='FACE')

              bpy.ops.mesh.select_all(action = 'SELECT')
              bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(0, 0, 1), clear_inner=True, clear_outer=False, xstart=539, xend=597, ystart=336, yend=336)


              bpy.ops.mesh.select_all(action = 'SELECT')
        
              bpy.ops.object.mode_set(mode = 'OBJECT')
        
        
           bpy.ops.object.modifier_add(type='MIRROR')
           bpy.context.object.modifiers["Mirror"].use_x = False

           if myscene.T_symmet_X == True :
              bpy.context.object.modifiers["Mirror"].use_x = True
        
           if myscene.T_symmet_Y == True :
              bpy.context.object.modifiers["Mirror"].use_y = True        
        
           if myscene.T_symmet_Z == True :
              bpy.context.object.modifiers["Mirror"].use_z = True
            

           if myscene.T_symmet_clip == True:
              bpy.context.object.modifiers["Mirror"].use_clip = True



       return {'FINISHED'}


# - Normal To Curvature ------------------------------------------------
class ButtonNtoCOff(bpy.types.Operator):
    bl_label = 'Normal to Curvature'
    bl_idname = 'ga_button.ntoc_off'
    bl_context = 'objectmode'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        context.scene.ga_property.gui_active_panel = "None"
        return {'FINISHED'}

class ButtonNtoCOn(bpy.types.Operator):
    bl_label = 'Normal to Curvature'
    bl_idname = 'ga_button.ntoc_on'
    bl_context = 'objectmode'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        context.scene.ga_property.gui_active_panel = 'NtoC'
        return {'FINISHED'}


class NtoC(bpy.types.Operator):
    bl_idname = "ga_tools.ntoc"
    bl_label = "Generate curvature"
    filename_ext = ".fbx"
    filter_glob = bpy.props.StringProperty(
        default="*.json",
        options={'HIDDEN'},
        )
    bl_context = 'objectmode'


    def execute(self, context):

       # ucitaj scenu
       scene = bpy.context.scene
       scene.use_nodes = True

       nodes = scene.node_tree.nodes
       links = scene.node_tree.links

       myscene = context.scene.ga_property


       # clear
       ##############################
       while(nodes): nodes.remove(nodes[0])


       # add image NORMAL
       ##############################
       q_i = bpy.data.images.load(myscene.DT_pathntoc, check_existing=False)
       q_i.colorspace_settings.name = 'Linear'


       c_imgNORMAL = scene.node_tree.nodes.new('CompositorNodeImage')
       c_imgNORMAL.image = q_i
       c_imgNORMAL.location = (-300 ,0)


       # add image CURVATURE pixelwidth
       #################################
       c_imgCURVpixelwidth = scene.node_tree.nodes.new('CompositorNodeValue')
       c_imgCURVpixelwidth.location = (-300 ,-300)
       c_imgCURVpixelwidth.outputs[0].default_value = myscene.T_ntoc
       c_imgCURVpixelwidth.name = "Pixel width"
       c_imgCURVpixelwidth.label = "Pixel width"


       # add image CURVATURE shadow
       #################################
       c_imgCURVshadow = scene.node_tree.nodes.new('CompositorNodeValue')
       c_imgCURVshadow.location = (-300 ,-500)
       c_imgCURVshadow.name = "Shadows"
       c_imgCURVshadow.label = "Shadows"

       if myscene.T_curvature_shadows == True:
          c_imgCURVshadow.outputs[0].default_value = 1
       else:
          c_imgCURVshadow.outputs[0].default_value = 0

       


       # add NodeViewer
       ##############################
       c_view = scene.node_tree.nodes.new('CompositorNodeViewer')
       c_view.location = (400,0)  

       
       # clear all node_groups

       qnode = bpy.data.node_groups.get("Normal to Curvature")
       if  qnode is not None:
           bpy.data.node_groups.remove(qnode, do_unlink=True)


       GM_create_curvature_group("Normal to Curvature",myscene.T_ntocrel)

       c_curvgroup = scene.node_tree.nodes.new('CompositorNodeGroup')
       c_curvgroup.location = (0,0)  
       c_curvgroup.node_tree = bpy.data.node_groups["Normal to Curvature"]

       links.new( c_imgNORMAL.outputs['Image'],
                  c_curvgroup.inputs['Image'])
       links.new( c_imgCURVpixelwidth.outputs['Value'],
                  c_curvgroup.inputs[1])
       links.new( c_imgCURVshadow.outputs['Value'],
                  c_curvgroup.inputs[2])

       links.new( c_curvgroup.outputs['Image'],
                  c_view.inputs['Image'])

       return {'FINISHED'}

#######################################
# File export 
#######################################
class ButtonFileExportOff(bpy.types.Operator):
    bl_label = 'Export asset'
    bl_idname = 'ga_button.fileexport_off'
    bl_description = 'Close export settings'
    bl_context = 'objectmode'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        context.scene.ga_property.gui_active_panel = "None"
        return {'FINISHED'}

class ButtonFileExportOn(bpy.types.Operator):
    bl_label = 'Export asset'
    bl_idname = 'ga_button.fileexport_on'
    bl_description = 'Open export settings'
    bl_context = 'objectmode'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        context.scene.ga_property.gui_active_panel = 'fileexport'
        return {'FINISHED'}

class ExpObj(bpy.types.Operator):
    """Export"""
    bl_idname = "ga_tools.export"
    bl_label = "Export"
    filename_ext = ".fbx"
    filter_glob = bpy.props.StringProperty(
        default="*.json",
        options={'HIDDEN'},
        )
    bl_context = 'objectmode'

    def execute(self, context):

        active_object = bpy.context.active_object
        name = active_object.name
        objname = name + ".fbx" 

        target_file = bpy.path.abspath(context.scene.ga_property.DT_pathobj) + '\\' + objname 
        target_directory0 = os.path.dirname(target_file )
        target_directory1 = os.path.dirname( 
                            context.scene.ga_property.DT_exportpathtexture )
        target_directory2 = os.path.realpath( 
                            context.scene.ga_property.DT_exportpathtexture )



        if context.scene.ga_property.DT_exportcenterpos == True:
           bpy.ops.object.location_clear(clear_delta=False)

        if context.scene.ga_property.DT_exporttexture == True:

           mypresets = os.path.abspath(target_directory0 + 
                                    target_directory2)

           if not os.path.exists(mypresets):
              os.makedirs(mypresets)  


        bpy.ops.export_scene.fbx(
            filepath=target_file, 
            use_selection = True
        )


 
        srcfile = bpy.path.abspath(os.path.dirname(bpy.data.filepath ) )


        shutil.copy(srcfile + "\\"+ name[:-4] + "albedo.tga" , mypresets )
        shutil.copy(srcfile + "\\"+ name[:-4] + "normal.tga" , mypresets )
        shutil.copy(srcfile + "\\"+ name[:-4] + "ambient_occlusion.tga" , mypresets )

      
        return {'FINISHED'}


#######################################
# Polish sculpt
#######################################
class Polish_sculpt(bpy.types.Operator):
    bl_label = 'Polish sculpt'
    bl_idname = 'ga_tools.polish_sculpt'
    bl_description = 'Make flat surfaces and crisp edges (need a cleanup after running the script and the symmetry could be lost)'
    bl_context = 'objectmode'

    def execute(self, context):

        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.convert(target='MESH')

        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.context.object.modifiers["Decimate"].ratio = 0.03
        bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True

        bpy.ops.object.modifier_add(type='BEVEL')
        bpy.context.object.modifiers["Bevel"].segments = 2
        bpy.context.object.modifiers["Bevel"].profile = 1
        bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'

        bpy.ops.object.modifier_remove(modifier="Subsurf")
        bpy.ops.object.subdivision_set(level=2)

        bpy.ops.object.convert(target='MESH')

        bpy.ops.object.shade_smooth()

        return {'FINISHED'}

#######################################
# 2D Mesh
#######################################
class Mesh_2D(bpy.types.Operator):
    bl_label = '2D mesh'
    bl_idname = 'ga_tools.2d_mesh'
    bl_description = 'Use it to define the shape of a weapon by placing vertices in side view'
    bl_context = 'objectmode'

    def execute(self, context):

        bpy.ops.mesh.primitive_plane_add(view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

        bpy.ops.object.shade_smooth()

        bpy.ops.object.modifier_add(type='TRIANGULATE')

        bpy.ops.object.modifier_add(type='SOLIDIFY')
        bpy.context.object.modifiers["Solidify"].thickness = 0.07
        bpy.context.object.modifiers["Solidify"].offset = 0

        bpy.ops.object.modifier_add(type='BEVEL')
        bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
        bpy.context.object.modifiers["Bevel"].angle_limit = 1.55334
        bpy.context.object.modifiers["Bevel"].width = 0.03
        bpy.context.object.modifiers["Bevel"].profile = 1
        bpy.context.object.modifiers["Bevel"].use_clamp_overlap = False
        bpy.context.object.modifiers["Bevel"].loop_slide = False
        
        bpy.ops.object.modifier_add(type='BEVEL')
        bpy.context.object.modifiers["Bevel.001"].width = 0.001
        bpy.context.object.modifiers["Bevel.001"].limit_method = 'ANGLE'
        bpy.context.object.modifiers["Bevel.001"].angle_limit = 0.628319
        
        bpy.ops.object.subdivision_set(level=4)
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.delete(type='VERT')

        return {'FINISHED'}



#######################################
# Make tileable texture
#######################################
class Make_tileable_texture(bpy.types.Operator):
    bl_label = 'Make tileable texture'
    bl_idname = 'ga_tools.make_tileable_texture'
    bl_description = 'Add a configured plane to allow you tu sculpt a tielable texture'
    bl_context = 'objectmode'

    def execute(self, context):


        bpy.ops.mesh.primitive_plane_add(view_align=False, enter_editmode=False, location=(0, 0, 1), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.delete(type='ONLY_FACE')
        bpy.ops.object.mode_set(mode = 'OBJECT')

        bpy.ops.mesh.primitive_plane_add(view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.transform.resize(value=(2, 2, 2), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        #should go to top orthographic view and zoom on the selection


        bpy.ops.object.mode_set(mode = 'SCULPT')

        #to change with an enable command
        bpy.ops.sculpt.dynamic_topology_toggle()

        bpy.context.scene.tool_settings.sculpt.tile_x = True
        bpy.context.scene.tool_settings.sculpt.tile_y = True
        bpy.context.scene.tool_settings.sculpt.tile_z = True
        bpy.context.scene.tool_settings.sculpt.tile_offset[1] = 2
        bpy.context.scene.tool_settings.sculpt.tile_offset[2] = 2
        bpy.context.scene.tool_settings.sculpt.tile_offset[0] = 2



        return {'FINISHED'}


#######################################
# Make Generate_Box
#######################################
class Make_Generate_Box(bpy.types.Operator):
    bl_label = 'Generate Box'
    bl_idname = 'ga_tools.make_generate_box'
    bl_description = 'Generate a box from a plane. You can then edit one faces to change every sides of the box'
    bl_context = 'objectmode'

    def execute(self, context):

        bpy.ops.object.mode_set(mode = 'OBJECT')

        bpy.ops.object.location_clear()

        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        bpy.ops.transform.translate(value=(0, -1, 1), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=0.522654)
        bpy.ops.transform.rotate(value=-1.5708, axis=(-1, -2.22045e-016, -4.93038e-032), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=0.522654)

        bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
        bpy.ops.transform.translate(value=(-1, 1, 0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=0.522654)
        bpy.ops.transform.rotate(value=1.5708, axis=(-0, 1.49012e-008, -1), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=0.522654)

        bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
        bpy.ops.transform.translate(value=(1, 1, 0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=0.522654)
        bpy.ops.transform.rotate(value=1.5708, axis=(-0, 1.49012e-008, -1), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=0.522654)

        bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
        bpy.ops.transform.translate(value=(1, -1, 0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=0.522654)
        bpy.ops.transform.rotate(value=1.5708, axis=(-0, 1.49012e-008, -1), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=0.522654)

        bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
        bpy.ops.transform.translate(value=(-1, 0, -1), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=0.522654)
        bpy.ops.transform.rotate(value=1.5708, axis=(-0, 1, 1.34359e-007), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=0.522654)

        bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
        bpy.ops.transform.translate(value=(-0, -0, 2), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=0.522654)
        bpy.ops.transform.rotate(value=3.14159, axis=(-0, 1, 1.34359e-007), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=0.522654)


        return {'FINISHED'}



#######################################
# Import New Material
#######################################
class GT_Import_Material(bpy.types.Operator):
    bl_label = 'Import new material'
    bl_idname = 'ga_tools.ga_import_material'
    bl_description = 'Import new material'
    bl_context = 'objectmode'

    def execute(self, context):

        filepathdb = os.path.join(os.path.dirname(__file__), 
               "thumbs" + os.sep ) + "material.ga"

        nodesField = bpy.context.scene.node_tree
        framenodes = nodesField.nodes.active

        if nodesField.nodes.active.type == "FRAME":

          # REMOVE OLD MATERIAL
          #######################
          with  open(filepathdb , "r+") as f:
             t = f.read()
             to_delete = "NAME="+framenodes.label
             f.seek(0)
    
             for line in t.split("\n"):

                if line[:1] != " ":
                   if line == to_delete:
                      prolaz = 1
                   else:
                      prolaz = 0
          
                if prolaz == 0:
                   f.write(line + "\n")
                   f.truncate()       

          # ADD NEW MATERIAL
          #######################

          for n in nodesField.nodes:
          
             if n.parent == framenodes:
         
                if n.type == "VALTORGB":

                   ga = open(filepathdb , "a+")
                   ga.write("NAME="+framenodes.label+"\n")
          
                   ga.write(" VALTORGB="+n.name+"\n")
          
                   for e in n.color_ramp.elements:
                      ga.write("   position="+str(e.position)+"\n")
                      ga.write("   colorR="+str(e.color[0])+"\n")
                      ga.write("   colorG="+str(e.color[1])+"\n")
                      ga.write("   colorB="+str(e.color[2])+"\n")
                      ga.write("   colorA="+str(e.color[3])+"\n")

                   ga.write("   fac="+str(n.inputs[0].default_value)+"")
              
                   ga.close() 

        q_mat = bpy.types.Scene.dandy_thumbs_mats_metals
        #q_mat.items = GM_generate_previews(True)

        #bpy.types.Scene.reload()

        return {'FINISHED'}



def GM_generate_previews(metals):

    previews = GM_preview_collections["tmp_material_all"]
    image_location = previews.images_location
    GM_enum_items = []

    #path DB
    filepathdb = os.path.join(os.path.dirname(__file__), 
               "thumbs" + os.sep ) + "material.ga"

    gaDB = open(filepathdb, "r")
    lines = gaDB.readlines()


    for i, line in enumerate(lines):
        q_name = line[0:4]

        if q_name == "NAME":
           q_name = line[5:-1]
           print(q_name)
       
           filepathIMG = os.path.join(image_location, q_name )
           thumb = previews.load(filepathIMG, filepathIMG, 'IMAGE')
  
        
           GM_enum_items.append((q_name, q_name , "", thumb.icon_id, i ))


    GM_enum_items.sort()

    return GM_enum_items

def GM_create_curvature_group(q_name,T_ntocrel):

   test_group = bpy.data.node_groups.new(q_name, 'CompositorNodeTree')

   # create group inputs
   group_inputs = test_group.nodes.new('NodeGroupInput')
   group_inputs.location = (-350,0)
   test_group.inputs.new('NodeSocketColor','Image')
   #test_group.inputs.new('NodeSocketFloat','Value')
   test_group.inputs.new('NodeSocketFloat','Pixel width')
   test_group.inputs.new('NodeSocketFloat','Shadows')
   test_group.inputs[1].default_value = 1
   test_group.inputs[2].default_value = 1


   # create group outputs
   group_outputs = test_group.nodes.new('NodeGroupOutput')
   group_outputs.location = (3000,0)
   test_group.outputs.new('NodeSocketColor','Image')



   a3 = test_group.nodes.new('CompositorNodeSepRGBA')
   a3.location = (500 ,200)
   a3.name = "a3"
   a3.label = "a3"


   test_group.links.new( group_inputs.outputs['Image'],a3.inputs['Image'])


   t1 = test_group.nodes.new('CompositorNodeTranslate')
   t1.location = (800 ,500)

   t2 = test_group.nodes.new('CompositorNodeTranslate')
   t2.location = (800 ,300)

   t3 = test_group.nodes.new('CompositorNodeTranslate')
   t3.location = (800 ,100)

   t4 = test_group.nodes.new('CompositorNodeTranslate')
   t4.location = (800 ,-100)

   #t5 = test_group.nodes.new('CompositorNodeTranslate')
   #t5.location = (800 ,-300)

   #t6 = test_group.nodes.new('CompositorNodeTranslate')
   #t6.location = (800 ,-500)




   test_group.links.new( a3.outputs['R'],t1.inputs['Image'])
   test_group.links.new( a3.outputs['R'],t2.inputs['Image'])
   test_group.links.new( a3.outputs['G'],t3.inputs['Image'])
   test_group.links.new( a3.outputs['G'],t4.inputs['Image'])

   #test_group.links.new( a3.outputs['G'],t5.inputs['Image'])


   a02 = test_group.nodes.new('CompositorNodeMixRGB')
   a02.name = "a02"
   a02.label = "a02"
   a02.location = (1300 ,200)
   a02.blend_type = 'MIX'





   a4 = test_group.nodes.new('CompositorNodeMixRGB')
   a4.location = (1100 ,500)
   a4.name = "a4"
   a4.label = "a4"
   a4.blend_type = 'SUBTRACT'


   test_group.links.new( t1.outputs['Image'],a4.inputs[1])
   test_group.links.new( t2.outputs['Image'],a4.inputs[2])


   a5 = test_group.nodes.new('CompositorNodeMath')
   a5.location = (1400 ,500)
   a5.name = "a5"
   a5.label = "a5"
   a5.operation = 'ADD'
   a5.inputs[0].default_value = 1
   a5.inputs[1].default_value = 0.5

   test_group.links.new( a4.outputs['Image'],a5.inputs[0])


   a6 = test_group.nodes.new('CompositorNodeMixRGB')
   a6.name = "a6"
   a6.label = "a6"
   a6.location = (1100 ,200)
   a6.blend_type = 'SUBTRACT'

   test_group.links.new( t3.outputs['Image'],a6.inputs[2])
   test_group.links.new( t4.outputs['Image'],a6.inputs[1])

   a7 = test_group.nodes.new('CompositorNodeMath')
   a7.location = (1500 ,200)
   a7.name = "a7"
   a7.label = "a7"
   a7.operation = 'ADD'
   a7.inputs[0].default_value = 1
   a7.inputs[1].default_value = 0.5

   test_group.links.new( a6.outputs['Image'],a02.inputs[2])
   test_group.links.new( a02.outputs['Image'],a7.inputs[0])



   #a8 = test_group.nodes.new('CompositorNodeInvert')
   #a8.location = (1600 ,200)

   


   a9 = test_group.nodes.new('CompositorNodeMixRGB')
   a9.location = (1900 ,300)
   a9.name = "a9"
   a9.label = "a9"
   a9.blend_type = 'OVERLAY'


   test_group.links.new( a5.outputs['Value'],a9.inputs[1])
   test_group.links.new( a7.outputs['Value'],a9.inputs[2])

   a10 = test_group.nodes.new('CompositorNodeGamma')
   a10.location = (2600 ,300)
   a10.name = "a10"
   a10.label = "a10"
   a10.inputs[1].default_value = 2.2


   a11 = test_group.nodes.new('CompositorNodeBlur')
   a11.location = (2200 ,300)
   a11.name = "a11"
   a11.label = "a11"
   a11.use_relative = True
   a11.factor_x = T_ntocrel
   a11.factor_y = T_ntocrel

   a12 = test_group.nodes.new('CompositorNodeMixRGB')
   a12.location = (2400 ,300)
   a12.name = "a12"
   a12.label = "a12"
   a12.blend_type = 'MULTIPLY'



   test_group.links.new( a9.outputs['Image'],a11.inputs['Image'])
   test_group.links.new( a11.outputs['Image'],a12.inputs[1])
   test_group.links.new( a12.outputs['Image'],a10.inputs['Image'])
   test_group.links.new( a10.outputs['Image'],group_outputs.inputs['Image'])
   test_group.links.new( a3.outputs['B'],a12.inputs[2])




   b1 = test_group.nodes.new('CompositorNodeMath')
   b1.location = (0 ,500)
   b1.operation = 'DIVIDE' 
   b1.inputs[0].default_value = 1
   b1.inputs[1].default_value = 2.0


   b2 = test_group.nodes.new('CompositorNodeMath')
   b2.location = (300 ,500)
   b2.operation = 'MULTIPLY'
   b2.inputs[0].default_value = 1
   b2.inputs[1].default_value = -1.0

   test_group.links.new( group_inputs.outputs['Pixel width'],b1.inputs[0])
   test_group.links.new( group_inputs.outputs['Shadows'],a12.inputs["Fac"])

   test_group.links.new( b1.outputs['Value'],b2.inputs[0])

   test_group.links.new( b2.outputs['Value'],t1.inputs['X'])
   test_group.links.new( b2.outputs['Value'],t4.inputs['Y'])
   test_group.links.new( b1.outputs['Value'],t2.inputs['X'])
   test_group.links.new( b1.outputs['Value'],t3.inputs['Y'])

   #test_group.links.new( b2.outputs['Value'],t6.inputs['Y'])
   #test_group.links.new( b1.outputs['Value'],t5.inputs['Y'])


   # Ako je otvoren NODE_EDITOT
   #  prebaci ga u composite
   ############################
   editorcheck = False
   for area in bpy.context.screen.areas :
       if area.type == 'NODE_EDITOR' :
           if area.spaces.active.tree_type != 'CompositorNodeTree':
               area.spaces.active.tree_type = 'CompositorNodeTree'
           editorcheck = True

   # Ako nije otvoren NODE_EDITOT
   #  u postojecem prvo NODE EDITOR
   #  pa split
   #  pa VIEW 3D
   # prebaci u composite
   ############################
   if editorcheck == False:
      try:
           bpy.context.area.type='NODE_EDITOR'
           bpy.ops.screen.area_split(factor=0.5)
           bpy.context.area.type='VIEW_3D'

           for area in bpy.context.screen.areas :
               if area.type == 'NODE_EDITOR' :
                   if area.spaces.active.tree_type != 'CompositorNodeTree':
                       area.spaces.active.tree_type = 'CompositorNodeTree'
      except:
           pass


