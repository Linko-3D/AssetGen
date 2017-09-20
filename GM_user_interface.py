import bpy,os,colorsys
from bpy.props import FloatVectorProperty, IntProperty, BoolProperty, FloatProperty, EnumProperty, PointerProperty,StringProperty,CollectionProperty
from bpy.types import Menu, Panel, AddonPreferences, PropertyGroup, UIList
from rna_prop_ui import PropertyPanel

from mathutils import Color



class PANEL_GameMaterial(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"  
    bl_label = "Game Asset Materials"  
    bl_category = "AssetGen"
    bl_options = {'DEFAULT_CLOSED'}  


    def draw(self, context):

        q_gaenabled = True
        q_err = ""
        scene = context.scene
        q_mat = scene.gmmateriali
        q_mat_select = scene.gmselect

        layout = self.layout


        #Provera greske
        #####################################
        if len(bpy.context.selected_objects) != 1:
           q_err = "Not selected object !!!"
        else:
           if bpy.context.object.active_material.name[-4:] != "_PBR":
              q_err = "You must generate your asset before editing the Albedo"


        if scene.D_gradientcolor== 'Presets':
           q_material_name = context.scene.dandy_thumbs_mats_metals
        else:
           q_material_name = "Custom gradient"


        # Greyscale options 
        ######################################

        col = layout.column(align=True)
        box_GS = col.box()
        rowGS = box_GS.row()
        rowGS.label(text="Greyscale options:")
        subrowGS = rowGS.column(align=True)
        subrowGS.prop(scene, 'D_curv')
        subrowGS.prop(scene, 'D_ao')
        subrowGS.prop(scene, 'D_shad')

        # Effects options 
        ######################################

        col = layout.column(align=True)
        box_GS = col.box()
        rowGS = box_GS.row()
        rowGS.label(text="Effects:")

        subcolGS = box_GS.column(align=True)
        subrowGS = subcolGS.row(align=True)
        subrowGS.prop(scene, 'D_effectcolordust',text="")
        subrowGS = subrowGS.row(align=True)
        subrowGS.prop(scene, 'D_effectdust')

        #subcolGS = box_GS.column(align=True)
        subrowGS = subcolGS.row(align=True)
        subrowGS.prop(scene, 'D_effectcolorgrunge',text="")
        subrowGS = subrowGS.row(align=True)
        subrowGS.prop(scene, 'D_effectgrunge')

        #subcolGS = box_GS.column(align=True)
        subrowGS = subcolGS.row(align=True)
        subrowGS.prop(scene, 'D_effectcolorsnow',text="")
        subrowGS = subrowGS.row(align=True)
        subrowGS.prop(scene, 'D_effectsnow')




        # Add/Remove button
        col = layout.column(align=True)

        row = col.row(align=True)
        row.scale_y = 1.2

        props = row.operator("gm.material_add")
        props.name = q_material_name 
    

        props1 = row.operator("gm.material_update")
        props1.name = q_material_name 




        # PREVIEW

        if scene.D_gradientcolor== 'Presets':
           row = col.row()
           row.scale_y = 1.32

           row.template_icon_view(scene, "dandy_thumbs_mats_metals", show_labels=True)

           q_material_name = context.scene.dandy_thumbs_mats_metals

        else:

           box1_ga = col.box()
           box1_ga.template_color_picker(q_mat_select , "use_colorselect", value_slider=True, cubic=False)

           row1 = box1_ga.row()
           row1.prop(q_mat_select , "use_colorselect", text="")

           row2 = col.row(align=True)
           row2.prop(q_mat_select, 'use_gra_select', expand=True)

           #q_material_name = " R:"+str(round(q_mat_select.use_colorselect[0],3)) + " G:" + str(round(q_mat_select.use_colorselect[1],3)) + " B:" + str(round(q_mat_select.use_colorselect[2],3))


        col.separator()
        col.separator()

        row = col.row()
        row.prop(scene , 'D_gradientcolor', expand=True)
        


        # Material Name
        row = col.row(align=True)
        row.alignment = 'CENTER'
        row.label(q_material_name)


        #list material
        ##############
        i = 0
        col = layout.column(align=True)

        for layer_idx in q_mat :
            
            q_select = layer_idx.use_select             

            row = col.row(align=True)

            # SELECT
            icon = 'RESTRICT_VIEW_OFF' if q_select else 'RESTRICT_VIEW_ON'
            row.operator("gm.material_select", text="", icon=icon, emboss=True).layer_idx = i

            # COLOR
            sub = row.row(align=True)
            #if layer_idx.use_mask_enable == False:
            #   sub.enabled = True
            #else:

            if layer_idx.name== 'Custom gradient':
               sub.enabled = True
               sub.prop(layer_idx , "use_color1", text="",icon=icon)
               sub.prop(layer_idx , "use_color5", text="",icon=icon)

            else:
               sub.enabled = False
               sub.prop(layer_idx , "use_color3", text="",icon=icon)



            # NAME
            row.operator("gm.material_select", text=layer_idx.name, emboss=True).layer_idx = i


            # MASK
            icon = 'MOD_MASK' 
            row.prop(layer_idx,'use_mask_enable',icon=icon,toggle=True, emboss=True)

            # COLOR
            sub = row.row(align=True)
            if layer_idx.use_mask_enable == False:
               sub.enabled = False
            else:
               sub.enabled = True
            sub.prop(layer_idx , "use_mask", text="",icon=icon)

            # ADVANCED
            icon = 'TRIA_UP' if layer_idx.use_advanced_enable else 'TRIA_DOWN'
            row.operator("gm.material_advanced", text="", emboss=True, icon=icon).layer_idx = i

            # ADVANCED PANEL
            if layer_idx.use_advanced_enable:

                #BUMP
                icon = 'LAYER_ACTIVE' if layer_idx.use_advanced_layer_Bump_enable else 'LAYER_USED'
                subrow = col.row(align=True)
                subrow.scale_y = 1.1
                subrow.label(text="Bump effect", icon=icon )
                subrow.prop(layer_idx, 'use_advanced_layer_Bump',emboss=False)
                subrow.prop(layer_idx, 'use_advanced_layer_Bump_enable')

                #CURVATURE
                icon = 'LAYER_ACTIVE' if layer_idx.use_advanced_layer_Curvature_enable else 'LAYER_USED'
                subrow = col.row(align=True)
                subrow.scale_y = 1.1
                subrow.label(text="Curvature effect", icon=icon )
                subrow.prop(layer_idx, 'use_advanced_layer_Curvature',emboss=False)
                subrow.prop(layer_idx, 'use_advanced_layer_Curvature_enable')





            # REMOVE
            icon = 'PANEL_CLOSE' 
            row.operator("gm.material_remove", text="", emboss=True, icon=icon).layer_idx = i

            i = i + 1



        # generate_textures button
        layout.row().separator()
        col_start = layout.column(align=True)

        row = col_start.row(align=True)
        row.scale_y = 1.5
        row.operator("gm.generate_textures", icon="FILE_REFRESH")
        layout.row().separator()


        # Blender render/Cycles
        col_start = layout.column(align=True)

        row = col_start.row(align=True)
        row.prop(scene , 'D_renderengine', expand=True)




        # GM enable/disable
        #if q_gaenabled == True:
            #col_start .enabled = True
        #else:
            #col_start .enabled = False

        if q_err  != "": 
               # Display Error
               col = layout.column(align=True)
               row = col.row(align=True)
               row.alignment = 'CENTER'
               row.label(text=q_err , icon='ERROR')
               layout.row().separator()
               q_gaenabled = False
               col_start .enabled = False



# ADVANCED
##############################################

class GM_material_advanced(bpy.types.Operator):
    bl_idname = "gm.material_advanced"
    bl_label = "Select"

    layer_idx = IntProperty()

    def execute(self, context):
        layer_idx = self.layer_idx

        q_mat = context.scene.gmmateriali 


        #print(layer_idx ,q_mat[layer_idx].use_advanced_enable)

        if q_mat[layer_idx].use_advanced_enable == True:
           q_mat[layer_idx].use_advanced_enable = False
        else:
           q_mat[layer_idx].use_advanced_enable = True


        return {'FINISHED'}


# SELECT
##############################################

class GM_material_select(bpy.types.Operator):
    bl_idname = "gm.material_select"
    bl_label = "Select"

    layer_idx = IntProperty()

    def invoke(self, context, event):

        if event.ctrl:
           if bpy.context.object.active_material.use_textures[4] == False:
              bpy.context.object.active_material.use_textures[4] = True
              bpy.context.object.active_material.use_shadeless = True
           else:
              bpy.context.object.active_material.use_textures[4] = False
              bpy.context.object.active_material.use_shadeless = False
     
        self.execute(context)
        return {'FINISHED'}

    def execute(self, context):
        layer_idx = self.layer_idx

        q_mat = context.scene.gmmateriali 
        q_mat_select = context.scene.gmselect


        for q_idx in q_mat :
            q_idx.use_select = False

        q_mat[layer_idx].use_select = True

        if q_mat[layer_idx].name == "Custom gradient":
           q_mat_select.use_colorselect = q_mat[layer_idx].use_color3
           context.scene.D_gradientcolor = 'Custom gradient'
        else:
           context.scene.dandy_thumbs_mats_metals = q_mat[layer_idx].name
           context.scene.D_gradientcolor = 'Presets'

        return {'FINISHED'}




# ADD
##############################################

class GM_material_add(bpy.types.Operator):
    bl_idname = "gm.material_add"
    bl_label = "Add"

    name = StringProperty()

    def execute(self, context):

        q_mat = context.scene.gmmateriali 
        q_mat_select = context.scene.gmselect

        q_mat.add()

        i = 0
        for q_idx in q_mat:
            q_idx.use_select = False
            i = i + 1

        q_mat[i-1].use_select = True
        q_mat[i-1].name = self.name


        q_mat[i-1].use_point1 = q_mat_select.use_point1
        q_mat[i-1].use_color1 = q_mat_select.use_color1
        q_mat[i-1].use_point2 = q_mat_select.use_point2
        q_mat[i-1].use_color2 = q_mat_select.use_color2
        q_mat[i-1].use_point3 = q_mat_select.use_point3
        q_mat[i-1].use_color3 = q_mat_select.use_color3
        q_mat[i-1].use_point4 = q_mat_select.use_point4
        q_mat[i-1].use_color4 = q_mat_select.use_color4
        q_mat[i-1].use_point5 = q_mat_select.use_point5
        q_mat[i-1].use_color5 = q_mat_select.use_color5




        return {'FINISHED'}


# REMOVE
##############################################

class GM_material_remove(bpy.types.Operator):
    bl_idname = "gm.material_remove"
    bl_label = "Remove"

    layer_idx = IntProperty()

    def execute(self, context):
        layer_idx = self.layer_idx

        q_mat = context.scene.gmmateriali 
        q_mat.remove(layer_idx )

        i = 0
        for q_idx in q_mat:
            q_idx.use_select = False
            i = i + 1
        if i > 0:
            q_mat[i-1].use_select = True

        return {'FINISHED'}


# UPDATE
##############################################

class GM_material_update(bpy.types.Operator):
    bl_idname = "gm.material_update"
    bl_label = "Update"

    name = StringProperty()

    def execute(self, context):
        q_mat = context.scene.gmmateriali 
        q_mat_select = context.scene.gmselect


        for q_idx in q_mat :
            if q_idx.use_select == True:
               q_idx.name = self.name

               q_idx.use_point1 = q_mat_select.use_point1
               q_idx.use_color1 = q_mat_select.use_color1
               q_idx.use_point2 = q_mat_select.use_point2
               q_idx.use_color2 = q_mat_select.use_color2
               q_idx.use_point3 = q_mat_select.use_point3
               q_idx.use_color3 = q_mat_select.use_color3
               q_idx.use_point4 = q_mat_select.use_point4
               q_idx.use_color4 = q_mat_select.use_color4
               q_idx.use_point5 = q_mat_select.use_point5
               q_idx.use_color5 = q_mat_select.use_color5





        return {'FINISHED'}

# Generate textures
##############################################

class GM_generate_textures1(bpy.types.Operator):
    bl_idname = "gm.generate_textures1"
    bl_label = "Generate textures"

    def execute(self, context):

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


        # ucitaj scenu
        scene = bpy.context.scene
        scene.frame_current = 1

        # aktiviraj use_node
        scene.use_nodes = True

        nodes = scene.node_tree.nodes
        links = scene.node_tree.links
        q_activeobj = bpy.context.active_object.name
        q_nodepos = 0


        # clear
        ##############################
        while(nodes): nodes.remove(nodes[0])

        # add image pointiness
        ##############################
        c_img = scene.node_tree.nodes.new('CompositorNodeImage')
        c_img.image = bpy.data.images.get(q_activeobj[:-4]+"pointiness")
        c_img.location = (q_nodepos-100 ,-200)  

        # add image MASK
        ##############################
        c_imgID = scene.node_tree.nodes.new('CompositorNodeImage')
        c_imgID.image = bpy.data.images.get(q_activeobj[:-4]+"mask")
        c_imgID.location = (q_nodepos-100 ,-600)

        # add image NORMAL
        ##############################
        c_imgNORMAL = scene.node_tree.nodes.new('CompositorNodeImage')
        c_imgNORMAL.image = bpy.data.images.get(q_activeobj[:-4]+"normal")
        c_imgNORMAL.location = (q_nodepos-100 ,-1000)

        # add image CURVATURE Value
        ##############################
        c_imgCURVvalue = scene.node_tree.nodes.new('CompositorNodeValue')
        c_imgCURVvalue.location = (q_nodepos-100 ,-1300)





        # DO WHILE
        ##############################
        filepath = os.path.join(os.path.dirname(__file__), 
               "thumbs" + os.sep ) + "material.ga"

        c_mat = context.scene.gmmateriali 
        c_name = ""

        c_rampArray = []
        c_mixArray = []
        c_keyArray = []
        c_invArray = []
        c_maskArray = []


        for c_idx in c_mat :
            c_name= c_idx.name

            ga = open(filepath, "r")
            lines = ga.readlines()

            prolaz = 0
            pozicija = 0

            for i, line in enumerate(lines):

               if prolaz == 1:

                  # position
                  if line[:11] == "   position":

                     if pozicija >= len(c_ramp.color_ramp.elements):
                        c_ramp.color_ramp.elements.new(pozicija)

                     c_ramp.color_ramp.elements[pozicija].position = float(line[12:-1])
                     pozicija = pozicija + 1 


                  # colorR
                  if line[:9] == "   colorR":
                     c_ramp.color_ramp.elements[pozicija-1].color[0] = float(line[10:-1])

                  # colorG
                  if line[:9] == "   colorG":
                     c_ramp.color_ramp.elements[pozicija-1].color[1] = float(line[10:-1])

                  # colorB
                  if line[:9] == "   colorB":
                     c_ramp.color_ramp.elements[pozicija-1].color[2] = float(line[10:-1])

                  # colorA
                  if line[:9] == "   colorA":
                     c_ramp.color_ramp.elements[pozicija-1].color[3] = float(line[10:-1])



                  

               if line[0:4] == "NAME":
                  # ako postoji
                  if line[:-1] == "NAME="+c_name:

                     # add FRAME ramp
                     c_frame = scene.node_tree.nodes.new('NodeFrame')
                     c_frame.label = line[5:-1] 

                     # add COLORRAMP
                     q_nodepos += 250
                     c_ramp = scene.node_tree.nodes.new('CompositorNodeValToRGB')
                     c_ramp.location = (q_nodepos ,0)  
                     c_ramp.parent = c_frame

                     c_rampArray.append(c_ramp.name)

                     # add MIX
                     q_nodepos += 350
                     c_mix = scene.node_tree.nodes.new('CompositorNodeMixRGB')
                     c_mix.location = (q_nodepos ,-300)  

                     c_mixArray.append(c_mix.name)


                     # add FRAME mask
                     c_framemask = scene.node_tree.nodes.new('NodeFrame')
                     c_framemask.label = "Mask" 



                     # add ChromKEY
                     c_chrma = scene.node_tree.nodes.new(
                               'CompositorNodeChromaMatte')
                     c_chrma.location = (q_nodepos -400 ,-600)  
                     c_chrma.parent = c_framemask 


                     if c_idx.use_mask_enable:
                        c_chrma.inputs['Key Color'].default_value[0] = c_idx.use_mask[0] 
                        c_chrma.inputs['Key Color'].default_value[1] = c_idx.use_mask[1] 
                        c_chrma.inputs['Key Color'].default_value[2] = c_idx.use_mask[2] 
                        c_maskArray.append(True)
                     else:
                        c_maskArray.append(False)


                     c_keyArray.append(c_chrma.name)


                     # add INVERT
                     c_inv = scene.node_tree.nodes.new(
                               'CompositorNodeInvert')
                     c_inv.location = (q_nodepos -200 ,-600)  
                     c_inv.parent = c_framemask 
                     c_invArray.append(c_inv.name)

                     links.new( c_chrma.outputs['Matte'],
                               c_inv.inputs['Color'])



                     prolaz = 1
                  else:
                     prolaz = 0



            ga.close()




        # add NodeViewer
        ##############################
        q_nodepos += 350
        c_view = scene.node_tree.nodes.new('CompositorNodeViewer')
        c_view.location = (q_nodepos ,0)  


        # add File Output
        ##############################
        c_out1 = scene.node_tree.nodes.new('CompositorNodeOutputFile')
        c_out1.location = (q_nodepos ,-200)  
        c_out1.base_path = "//"
        c_out1.format.file_format = 'TARGA'

        c_out1.file_slots[0].path = q_activeobj[:-4]+"albedo####"


        # add LINK
        ###############################
        links.new( c_img.outputs['Image'],
                   scene.node_tree.nodes[c_mixArray[0]].inputs[1])


        for i in range(0,len(c_mixArray )):
           links.new( c_img.outputs['Image'],
                   scene.node_tree.nodes[c_rampArray[i]].inputs['Fac'])

           links.new( scene.node_tree.nodes[c_rampArray[i]].outputs['Image'],
                   scene.node_tree.nodes[c_mixArray[i]].inputs[2])
           if i < len(c_mixArray )-1:
              links.new( scene.node_tree.nodes[c_mixArray[i]].outputs['Image'],
                   scene.node_tree.nodes[c_mixArray[i+1]].inputs[1])
           else:
              links.new( scene.node_tree.nodes[c_mixArray[i]].outputs['Image'],
                   c_view.inputs['Image'])
              links.new( scene.node_tree.nodes[c_mixArray[i]].outputs['Image'],
                   c_out1.inputs['Image'])


           #mask
           links.new( c_imgID.outputs['Image'],
                   scene.node_tree.nodes[c_keyArray[i]].inputs['Image'])

           if c_maskArray[i]:
              links.new( scene.node_tree.nodes[c_invArray[i]].outputs['Color'],
                      scene.node_tree.nodes[c_mixArray[i]].inputs['Fac'])



        #Save the maps by doing a render

        bpy.context.scene.render.resolution_x = 4
        bpy.context.scene.render.resolution_y = 4


        bpy.ops.render.render(use_viewport=True)

        bpy.context.scene.render.resolution_x = 1920
        bpy.context.scene.render.resolution_y = 1080


        bpy.context.scene.render.engine = 'BLENDER_RENDER'


        #rename file
        ################################

        q_filepath = os.path.join(os.path.dirname( bpy.data.filepath  )
, q_activeobj[:-4]+"albedo.tga")

        q_filepathnew = os.path.join(os.path.dirname( bpy.data.filepath  )
, q_activeobj[:-4]+"albedo0001.tga")



        if os.path.exists(q_filepath):
           os.remove(q_filepath)

        os.rename(q_filepathnew , q_filepath)

        bpy.data.images[q_activeobj[:-4]+"albedo"].reload()


        # disable 4 slot mask 
        # texture file
        ################################

        bpy.context.object.active_material.use_textures[4] = False
        bpy.context.object.active_material.use_shadeless = False


        return {'FINISHED'}



def GM_create_curvature_group(q_name):




   test_group = bpy.data.node_groups.new(q_name, 'CompositorNodeTree')

   # create group inputs
   group_inputs = test_group.nodes.new('NodeGroupInput')
   group_inputs.location = (-350,0)
   test_group.inputs.new('NodeSocketColor','Image')
   test_group.inputs.new('NodeSocketFloat','Value')

   # create group outputs
   group_outputs = test_group.nodes.new('NodeGroupOutput')
   group_outputs.location = (3000,0)
   test_group.outputs.new('NodeSocketColor','Image')



   a1 = test_group.nodes.new('CompositorNodeMath')
   a1.operation = 'DIVIDE'
   a1.inputs[0].default_value = 1
   a1.inputs[1].default_value = 2.2


   a2 = test_group.nodes.new('CompositorNodeGamma')
   a2.location = (300 ,200)

   test_group.links.new( a1.outputs['Value'],a2.inputs['Gamma'])

   test_group.links.new( group_inputs.outputs['Image'],a2.inputs['Image'])

   a3 = test_group.nodes.new('CompositorNodeSepRGBA')
   a3.location = (500 ,200)

   test_group.links.new( a2.outputs['Image'],a3.inputs['Image'])


   t1 = test_group.nodes.new('CompositorNodeTranslate')
   t1.location = (800 ,500)

   t2 = test_group.nodes.new('CompositorNodeTranslate')
   t2.location = (800 ,300)

   t3 = test_group.nodes.new('CompositorNodeTranslate')
   t3.location = (800 ,100)

   t4 = test_group.nodes.new('CompositorNodeTranslate')
   t4.location = (800 ,-100)


   test_group.links.new( a3.outputs['R'],t1.inputs['Image'])
   test_group.links.new( a3.outputs['R'],t2.inputs['Image'])
   test_group.links.new( a3.outputs['G'],t3.inputs['Image'])
   test_group.links.new( a3.outputs['G'],t4.inputs['Image'])


   a4 = test_group.nodes.new('CompositorNodeMixRGB')
   a4.location = (1100 ,500)
   a4.blend_type = 'SUBTRACT'


   test_group.links.new( t1.outputs['Image'],a4.inputs[1])
   test_group.links.new( t2.outputs['Image'],a4.inputs[2])


   a5 = test_group.nodes.new('CompositorNodeMath')
   a5.location = (1400 ,500)
   a5.operation = 'ADD'
   a5.inputs[0].default_value = 1
   a5.inputs[1].default_value = 0.5

   test_group.links.new( a4.outputs['Image'],a5.inputs[0])


   a6 = test_group.nodes.new('CompositorNodeMixRGB')
   a6.location = (1100 ,200)
   a6.blend_type = 'SUBTRACT'

   test_group.links.new( t3.outputs['Image'],a6.inputs[1])
   test_group.links.new( t4.outputs['Image'],a6.inputs[2])

   a7 = test_group.nodes.new('CompositorNodeMath')
   a7.location = (1400 ,200)
   a7.operation = 'ADD'
   a7.inputs[0].default_value = 1
   a7.inputs[1].default_value = 0.5

   test_group.links.new( a6.outputs['Image'],a7.inputs[0])


   a8 = test_group.nodes.new('CompositorNodeInvert')
   a8.location = (1600 ,200)

   test_group.links.new( a7.outputs['Value'],a8.inputs['Color'])


   a9 = test_group.nodes.new('CompositorNodeMixRGB')
   a9.location = (1900 ,300)
   a9.blend_type = 'OVERLAY'


   test_group.links.new( a5.outputs['Value'],a9.inputs[1])
   test_group.links.new( a8.outputs['Color'],a9.inputs[2])


   a10 = test_group.nodes.new('CompositorNodeGamma')
   a10.location = (2200 ,300)
   a10.inputs[1].default_value = 2.2

   test_group.links.new( a9.outputs['Image'],a10.inputs['Image'])


   a11 = test_group.nodes.new('CompositorNodeBlur')
   a11.location = (2500 ,300)
   a11.use_relative = True
   a11.factor_x = 0.5
   a11.factor_y = 0.5


   test_group.links.new( a10.outputs['Image'],a11.inputs['Image'])
   test_group.links.new( a11.outputs['Image'],group_outputs.inputs['Image'])



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

   test_group.links.new( b1.outputs['Value'],b2.inputs[0])

   test_group.links.new( b2.outputs['Value'],t1.inputs['X'])
   test_group.links.new( b2.outputs['Value'],t4.inputs['Y'])
   test_group.links.new( b1.outputs['Value'],t2.inputs['X'])
   test_group.links.new( b1.outputs['Value'],t3.inputs['Y'])


# Generate textures
##############################################

class GM_generate_textures(bpy.types.Operator):
    bl_idname = "gm.generate_textures"
    bl_label = " Generate Albedo"

    def execute(self, context):


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


        # ucitaj scenu
        scene = bpy.context.scene
        scene.frame_current = 1

        # aktiviraj use_node
        scene.use_nodes = True

        nodes = scene.node_tree.nodes
        links = scene.node_tree.links
        q_activeobj = bpy.context.active_object.name
        q_nodepos = 0


        # clear
        ##############################
        while(nodes): nodes.remove(nodes[0])

        # add image curvature
        ##############################
        c_img = scene.node_tree.nodes.new('CompositorNodeImage')
        c_img.image = bpy.data.images.get(q_activeobj[:-4]+"curvature")
        c_img.location = (q_nodepos-1000 ,-200)  
        c_img.label = "Curvature"


        # add image AO
        ##############################
        c_imgAO = scene.node_tree.nodes.new('CompositorNodeImage')
        c_imgAO.image = bpy.data.images.get(q_activeobj[:-4]+"ambient_occlusion")
        c_imgAO.location = (q_nodepos-1000 ,-500)  
        c_imgAO.label = "AO"

        # add image Normal map
        ##############################
        c_imgNORMAL = scene.node_tree.nodes.new('CompositorNodeImage')
        c_imgNORMAL.image = bpy.data.images.get(q_activeobj[:-4]+"normal")
        c_imgNORMAL.location = (q_nodepos-1000 ,-800)  
        c_imgNORMAL.label = "Normal map"

        c_RGBA = scene.node_tree.nodes.new('CompositorNodeSepRGBA')
        c_RGBA.location = (q_nodepos-700 ,-800)  

        links.new( c_imgNORMAL.outputs['Image'],
                               c_RGBA.inputs[0])

        # add image Bent
        ##############################
        c_imgBENT = scene.node_tree.nodes.new('CompositorNodeImage')
        c_imgBENT.image = bpy.data.images.get(q_activeobj[:-4]+"bent")
        c_imgBENT.location = (q_nodepos-1000 ,-1200)  
        c_imgBENT.label = "Bent"


        # add image MASK
        ##############################
        c_imgID = scene.node_tree.nodes.new('CompositorNodeImage')
        c_imgID.image = bpy.data.images.get(q_activeobj[:-4]+"mask")
        c_imgID.location = (q_nodepos-100 ,-600)
        c_imgID.label = "Mask"


        # add FRAME Enable curvature
        ##############################
        c_frameEC = scene.node_tree.nodes.new('NodeFrame')
        c_frameEC.label = "Enable curvature"

        c_mixEC = scene.node_tree.nodes.new('CompositorNodeMixRGB')
        c_mixEC.location = (q_nodepos -800,-230)  
        c_mixEC.parent = c_frameEC
        c_mixEC.inputs[1].default_value = (0.499458, 0.499458, 0.499458, 1)
        c_mixEC.inputs[0].default_value = scene.D_curv

        links.new( c_img.outputs['Image'],
                               c_mixEC.inputs[2])


        # add FRAME Enable AO
        ##############################
        c_frameAO = scene.node_tree.nodes.new('NodeFrame')
        c_frameAO.label = "Enable AO"

        c_mixAO = scene.node_tree.nodes.new('CompositorNodeMixRGB')
        c_mixAO.location = (q_nodepos -550,-230)  
        c_mixAO.parent = c_frameAO
        c_mixAO.blend_type = 'SOFT_LIGHT'
        c_mixAO.inputs[0].default_value = scene.D_ao


        links.new( c_mixEC.outputs['Image'],
                               c_mixAO.inputs[1])
        links.new( c_imgAO.outputs['Image'],
                               c_mixAO.inputs[2])

        # add FRAME Enable Shadows
        ##############################
        c_frameSHADOWS = scene.node_tree.nodes.new('NodeFrame')
        c_frameSHADOWS.label = "Enable Shadows"

        c_mixSHADOWS = scene.node_tree.nodes.new('CompositorNodeMixRGB')
        c_mixSHADOWS.location = (q_nodepos -300,-230)  
        c_mixSHADOWS.parent = c_frameSHADOWS
        c_mixSHADOWS.blend_type = 'MULTIPLY'
        c_mixSHADOWS.inputs[0].default_value = scene.D_shad

        links.new( c_mixAO.outputs['Image'],
                               c_mixSHADOWS.inputs[1])
        links.new( c_RGBA.outputs['B'],
                               c_mixSHADOWS.inputs[2])



        # add ROUTE
        ##############################
        c_mixROUTE = scene.node_tree.nodes.new('NodeReroute')
        c_mixROUTE.location = (q_nodepos -50,-250)  

        links.new( c_mixSHADOWS.outputs['Image'],
                               c_mixROUTE.inputs[0])



        # DO WHILE
        ##############################

        c_mat = context.scene.gmmateriali 
        c_name = ""


        

        c_rampArray = []
        c_mixArray = []
        c_mixcolArray = []
        c_keyArray = []
        c_invArray = []
        c_maskArray = []


        for c_idx in c_mat :
            c_name= c_idx.name


            # add FRAME ramp
            c_frame = scene.node_tree.nodes.new('NodeFrame')
            c_frame.label = c_name

            if c_name == "Custom gradient":

               # add COLORRAMP
               q_nodepos += 200
               c_ramp = scene.node_tree.nodes.new('CompositorNodeValToRGB')
               c_ramp.location = (q_nodepos ,0)  
               c_ramp.parent = c_frame
               aaa = c_ramp.color_ramp            
               aaa.color_mode = 'HSV'
               c_ramp.color_ramp.hue_interpolation = 'NEAR'

               c_ramp.color_ramp.elements[0].position = c_idx.use_point1
               c_ramp.color_ramp.elements[0].color[0] = c_idx.use_color1[0]
               c_ramp.color_ramp.elements[0].color[1] = c_idx.use_color1[1]
               c_ramp.color_ramp.elements[0].color[2] = c_idx.use_color1[2]
               c_ramp.color_ramp.elements[0].color[3] = 1

               c_ramp.color_ramp.elements.new(1)
               c_ramp.color_ramp.elements[1].position = c_idx.use_point5
               c_ramp.color_ramp.elements[1].color[0] = c_idx.use_color5[0]
               c_ramp.color_ramp.elements[1].color[1] = c_idx.use_color5[1]
               c_ramp.color_ramp.elements[1].color[2] = c_idx.use_color5[2]
               c_ramp.color_ramp.elements[1].color[3] = 1

            
            else:

               # add COLORRAMP
               q_nodepos += 200
               c_ramp = scene.node_tree.nodes.new('CompositorNodeValToRGB')
               c_ramp.location = (q_nodepos ,0)  
               c_ramp.parent = c_frame
               aaa1 = c_ramp.color_ramp            
               aaa1.color_mode = 'RGB'


               c_ramp.color_ramp.elements[0].position = c_idx.use_point1
               c_ramp.color_ramp.elements[0].color[0] = c_idx.use_color1[0]
               c_ramp.color_ramp.elements[0].color[1] = c_idx.use_color1[1]
               c_ramp.color_ramp.elements[0].color[2] = c_idx.use_color1[2]
               c_ramp.color_ramp.elements[0].color[3] = 1


               c_ramp.color_ramp.elements[1].position = c_idx.use_point2
               c_ramp.color_ramp.elements[1].color[0] = c_idx.use_color2[0]
               c_ramp.color_ramp.elements[1].color[1] = c_idx.use_color2[1]
               c_ramp.color_ramp.elements[1].color[2] = c_idx.use_color2[2]
               c_ramp.color_ramp.elements[1].color[3] = 1

               c_ramp.color_ramp.elements.new(2)
               c_ramp.color_ramp.elements[2].position = c_idx.use_point3
               c_ramp.color_ramp.elements[2].color[0] = c_idx.use_color3[0]
               c_ramp.color_ramp.elements[2].color[1] = c_idx.use_color3[1]
               c_ramp.color_ramp.elements[2].color[2] = c_idx.use_color3[2]
               c_ramp.color_ramp.elements[2].color[3] = 1

               c_ramp.color_ramp.elements.new(3)
               c_ramp.color_ramp.elements[3].position = c_idx.use_point4
               c_ramp.color_ramp.elements[3].color[0] = c_idx.use_color4[0]
               c_ramp.color_ramp.elements[3].color[1] = c_idx.use_color4[1]
               c_ramp.color_ramp.elements[3].color[2] = c_idx.use_color4[2]
               c_ramp.color_ramp.elements[3].color[3] = 1

               c_ramp.color_ramp.elements.new(4)
               c_ramp.color_ramp.elements[4].position = c_idx.use_point5
               c_ramp.color_ramp.elements[4].color[0] = c_idx.use_color5[0]
               c_ramp.color_ramp.elements[4].color[1] = c_idx.use_color5[1]
               c_ramp.color_ramp.elements[4].color[2] = c_idx.use_color5[2]
               c_ramp.color_ramp.elements[4].color[3] = 1

            c_rampArray.append(c_ramp.name)


            # add COLOR MIX
            q_nodepos += 350
            c_mixcol = scene.node_tree.nodes.new('CompositorNodeMixRGB')
            c_mixcol.blend_type = 'VALUE'

            if c_name == "Custom gradient":
               c_mixcol.mute = False
            else:
               c_mixcol.mute = True


            c_mixcol.location = (q_nodepos ,-40)  

            c_mixcolArray.append(c_mixcol.name)


            # add MIX
            q_nodepos += 350
            c_mix = scene.node_tree.nodes.new('CompositorNodeMixRGB')
            c_mix.location = (q_nodepos ,-300)  

            c_mixArray.append(c_mix.name)


            # add FRAME mask
            c_framemask = scene.node_tree.nodes.new('NodeFrame')
            c_framemask.label = "Mask" 

            # add ChromKEY
            c_chrma = scene.node_tree.nodes.new(
                               'CompositorNodeChromaMatte')
            c_chrma.location = (q_nodepos -400 ,-600)  
            c_chrma.parent = c_framemask 


            if c_idx.use_mask_enable:
               c_chrma.inputs['Key Color'].default_value[0] = c_idx.use_mask[0] 
               c_chrma.inputs['Key Color'].default_value[1] = c_idx.use_mask[1] 
               c_chrma.inputs['Key Color'].default_value[2] = c_idx.use_mask[2] 
               c_maskArray.append(True)
            else:
               c_maskArray.append(False)

            c_keyArray.append(c_chrma.name)


            # add INVERT
            c_inv = scene.node_tree.nodes.new(
                              'CompositorNodeInvert')
            c_inv.location = (q_nodepos -200 ,-600)  
            c_inv.parent = c_framemask 
            c_invArray.append(c_inv.name)

            links.new( c_chrma.outputs['Matte'],
                               c_inv.inputs['Color'])





        # add ROUTE
        ##############################
        q_nodepos += 350
        c_endROUTE = scene.node_tree.nodes.new('NodeReroute')
        c_endROUTE.location = (q_nodepos ,-250)  

        # add NodeViewer
        ##############################
        q_nodepos += 350
        c_view = scene.node_tree.nodes.new('CompositorNodeViewer')
        c_view.location = (q_nodepos ,0)  


        # add File Output
        ##############################
        c_out1 = scene.node_tree.nodes.new('CompositorNodeOutputFile')
        c_out1.location = (q_nodepos ,-200)  
        c_out1.base_path = "//"
        c_out1.format.file_format = 'TARGA'

        c_out1.file_slots[0].path = q_activeobj[:-4]+"albedo####"
  



        # add LINK
        ###############################
        links.new( c_mixROUTE.outputs[0],
                   scene.node_tree.nodes[c_mixArray[0]].inputs[1])



        for i in range(0,len(c_mixArray )):
           links.new( c_mixROUTE.outputs[0],
                   scene.node_tree.nodes[c_rampArray[i]].inputs['Fac'])

           links.new( c_mixROUTE.outputs[0],
                   scene.node_tree.nodes[c_mixcolArray[i]].inputs[2])


           links.new( scene.node_tree.nodes[c_rampArray[i]].outputs['Image'],
                   scene.node_tree.nodes[c_mixcolArray[i]].inputs[1])
           links.new( scene.node_tree.nodes[c_mixcolArray[i]].outputs['Image'],
                   scene.node_tree.nodes[c_mixArray[i]].inputs[2])

           if i < len(c_mixArray )-1:
              links.new( scene.node_tree.nodes[c_mixArray[i]].outputs['Image'],
                   scene.node_tree.nodes[c_mixArray[i+1]].inputs[1])
           else:
              links.new( scene.node_tree.nodes[c_mixArray[i]].outputs['Image'],
                   c_endROUTE.inputs[0])



           #mask
           links.new( c_imgID.outputs['Image'],
                   scene.node_tree.nodes[c_keyArray[i]].inputs['Image'])
           links.new( c_imgID.outputs['Alpha'],
                   c_view.inputs['Alpha'])




           if c_maskArray[i]:
              links.new( scene.node_tree.nodes[c_invArray[i]].outputs['Color'],
                      scene.node_tree.nodes[c_mixArray[i]].inputs['Fac'])


        # add EFFECTS
        ###############################

        # add FRAME GRUNGE
        c_frameGRUNGE = scene.node_tree.nodes.new('NodeFrame')
        c_frameGRUNGE.label = "Grunge"

        q_nodepos += 350
        c_mixGRUNGE = scene.node_tree.nodes.new('CompositorNodeMixRGB')
        c_mixGRUNGE.location = (q_nodepos ,-250)  
        c_mixGRUNGE.parent = c_frameGRUNGE
        c_mixGRUNGE.blend_type = 'MIX'
        c_mixGRUNGE.inputs[0].default_value = scene.D_effectgrunge

        # add COLORRAMP
        c_ramp = scene.node_tree.nodes.new('CompositorNodeValToRGB')
        c_ramp.location = (q_nodepos - 500 ,-600)  

        c_ramp.color_ramp.elements[0].position = 0.6
        c_ramp.color_ramp.elements[0].color[0] = 0.75
        c_ramp.color_ramp.elements[0].color[1] = 0.75
        c_ramp.color_ramp.elements[0].color[2] = 0.75
        c_ramp.color_ramp.elements[0].color[3] = 1

        c_ramp.color_ramp.elements[1].position = 0.968
        c_ramp.color_ramp.elements[1].color[0] = 1
        c_ramp.color_ramp.elements[1].color[1] = 1
        c_ramp.color_ramp.elements[1].color[2] = 1
        c_ramp.color_ramp.elements[1].color[3] = 1


        c_ramp.color_ramp.elements.new(1)
        c_ramp.color_ramp.elements[2].position = 1
        c_ramp.color_ramp.elements[2].color[0] = 0
        c_ramp.color_ramp.elements[2].color[1] = 0
        c_ramp.color_ramp.elements[2].color[2] = 0
        c_ramp.color_ramp.elements[2].color[3] = 1

        c_mixGRUNGE1 = scene.node_tree.nodes.new('CompositorNodeMixRGB')
        c_mixGRUNGE1.location = (q_nodepos -200 ,-600)  
        c_mixGRUNGE1.blend_type = 'MIX'
        c_mixGRUNGE1.inputs[2].default_value = scene.D_effectcolorgrunge


        links.new( c_endROUTE.outputs[0],
                   c_mixGRUNGE1.inputs[1])
        links.new( c_ramp.outputs['Image'],
                   c_mixGRUNGE1.inputs[0])
        links.new( c_mixGRUNGE1.outputs['Image'],
                   c_mixGRUNGE.inputs[2])
        links.new( c_endROUTE.outputs[0],
                 c_mixGRUNGE.inputs[1])
        links.new( c_imgAO.outputs[0],
                 c_ramp.inputs[0])


        # add FRAME DUST
        c_frameDUST = scene.node_tree.nodes.new('NodeFrame')
        c_frameDUST.label = "Dust"

        q_nodepos += 650
        c_mixDUST = scene.node_tree.nodes.new('CompositorNodeMixRGB')
        c_mixDUST.location = (q_nodepos   ,-250)  
        c_mixDUST.parent = c_frameDUST
        c_mixDUST.blend_type = 'MIX'
        c_mixDUST.inputs[0].default_value = scene.D_effectdust


        c_RGBADUST = scene.node_tree.nodes.new('CompositorNodeSepRGBA')
        c_RGBADUST.location = (q_nodepos-600 ,-600)  

        c_ramp = scene.node_tree.nodes.new('CompositorNodeValToRGB')
        c_ramp.location = (q_nodepos - 400 ,-600)  

        c_ramp.color_ramp.elements[0].position = 0.8
        c_ramp.color_ramp.elements[0].color[0] = 0
        c_ramp.color_ramp.elements[0].color[1] = 0
        c_ramp.color_ramp.elements[0].color[2] = 0
        c_ramp.color_ramp.elements[0].color[3] = 1

        c_ramp.color_ramp.elements.new(1)
        c_ramp.color_ramp.elements[1].position = 1
        c_ramp.color_ramp.elements[1].color[0] = 0.75
        c_ramp.color_ramp.elements[1].color[1] = 0.75
        c_ramp.color_ramp.elements[1].color[2] = 0.75
        c_ramp.color_ramp.elements[1].color[3] = 1

        c_mixDUST1 = scene.node_tree.nodes.new('CompositorNodeMixRGB')
        c_mixDUST1.location = (q_nodepos -100,-600)  
        c_mixDUST1.blend_type = 'MIX'
        c_mixDUST1.inputs[2].default_value = scene.D_effectcolordust

        links.new( c_imgBENT.outputs[0],
                 c_RGBADUST.inputs[0])
        links.new( c_RGBADUST.outputs["G"],
                 c_ramp.inputs[0])
        links.new( c_ramp.outputs[0],
                 c_mixDUST1.inputs[0])
        links.new( c_mixDUST1.outputs[0],
                 c_mixDUST.inputs[2])

        links.new( c_mixGRUNGE.outputs[0],
                 c_mixDUST.inputs[1])
        links.new( c_mixGRUNGE.outputs[0],
                 c_mixDUST1.inputs[1])

        # add FRAME SNOW
        c_frameSNOW = scene.node_tree.nodes.new('NodeFrame')
        c_frameSNOW.label = "Snow"

        q_nodepos += 700
        c_mixSNOW = scene.node_tree.nodes.new('CompositorNodeMixRGB')
        c_mixSNOW.location = (q_nodepos   ,-250)  
        c_mixSNOW.parent = c_frameSNOW
        c_mixSNOW.blend_type = 'MIX'
        c_mixSNOW.inputs[0].default_value = scene.D_effectsnow

        c_RGBASNOW= scene.node_tree.nodes.new('CompositorNodeSepRGBA')
        c_RGBASNOW.location = (q_nodepos-600 ,-600)  

        c_ramp = scene.node_tree.nodes.new('CompositorNodeValToRGB')
        c_ramp.location = (q_nodepos - 400 ,-600)  

        c_ramp.color_ramp.elements[0].position = 0.2
        c_ramp.color_ramp.elements[0].color[0] = 0
        c_ramp.color_ramp.elements[0].color[1] = 0
        c_ramp.color_ramp.elements[0].color[2] = 0
        c_ramp.color_ramp.elements[0].color[3] = 1

        c_ramp.color_ramp.elements.new(1)
        c_ramp.color_ramp.elements[1].position = 1
        c_ramp.color_ramp.elements[1].color[0] = 1
        c_ramp.color_ramp.elements[1].color[1] = 1
        c_ramp.color_ramp.elements[1].color[2] = 1
        c_ramp.color_ramp.elements[1].color[3] = 1

        c_mixSNOW1 = scene.node_tree.nodes.new('CompositorNodeMixRGB')
        c_mixSNOW1.location = (q_nodepos -100,-600)  
        c_mixSNOW1.blend_type = 'MIX'
        c_mixSNOW1.inputs[2].default_value = scene.D_effectcolorsnow

        links.new( c_imgBENT.outputs[0],
                 c_RGBASNOW.inputs[0])
        links.new( c_RGBASNOW.outputs["G"],
                 c_ramp.inputs[0])
        links.new( c_ramp.outputs[0],
                 c_mixSNOW1.inputs[0])
        links.new( c_mixSNOW1.outputs[0],
                 c_mixSNOW.inputs[2])

        links.new( c_mixDUST.outputs[0],
                 c_mixSNOW.inputs[1])
        links.new( c_mixDUST.outputs[0],
                 c_mixSNOW1.inputs[1])


        # add NodeViewer
        ##############################
        q_nodepos += 350
        c_view.location = (q_nodepos ,0)  


        # add File Output
        ##############################
        c_out1.location = (q_nodepos ,-200)  

        links.new( c_mixSNOW.outputs[0],
                 c_view.inputs['Image'])
        links.new( c_mixSNOW.outputs[0],
                 c_out1.inputs['Image'])



        #Save the maps by doing a render

        bpy.context.scene.render.resolution_x = 4
        bpy.context.scene.render.resolution_y = 4


        bpy.ops.render.render(use_viewport=True)

        bpy.context.scene.render.resolution_x = 1920
        bpy.context.scene.render.resolution_y = 1080


        bpy.context.scene.render.engine = 'BLENDER_RENDER'


        #rename file
        ################################

        q_filepath = os.path.join(os.path.dirname( bpy.data.filepath  )
, q_activeobj[:-4]+"albedo.tga")

        q_filepathnew = os.path.join(os.path.dirname( bpy.data.filepath  )
, q_activeobj[:-4]+"albedo0001.tga")



        if os.path.exists(q_filepath):
           os.remove(q_filepath)

        os.rename(q_filepathnew , q_filepath)

        bpy.data.images[q_activeobj[:-4]+"albedo"].reload()


        # disable 4 slot mask 
        # texture file
        ################################

        bpy.context.object.active_material.use_textures[4] = False
        bpy.context.object.active_material.use_shadeless = False



        return {'FINISHED'}



