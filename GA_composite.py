import bpy, os
from math import *
from .GA_material import MAT_texture_new



# - denoising - ///////////////////////

def DEF_denoising(context,size,name ):


       #tex = MAT_texture_new(name+"_"+"curvature",size, 'Raw')
   

       # ucitaj scenu
       scene = bpy.context.scene

       scene.use_nodes = True

       nodes = scene.node_tree.nodes
       links = scene.node_tree.links

       myscene = context.scene.ga_property


       # clear
       ##############################
       while(nodes): nodes.remove(nodes[0])


       # get image NORMAL
       ##############################
       q_i = bpy.data.images.get(name+"_"+"normal")       
       c_imgNORMAL = scene.node_tree.nodes.new('CompositorNodeImage')
       c_imgNORMAL.image = q_i
       c_imgNORMAL.location = (0 ,-300)

       # get image AO
       ##############################
       q_a = bpy.data.images.get(name+"_"+"ambient_occlusion")       
       c_imgAO = scene.node_tree.nodes.new('CompositorNodeImage')
       c_imgAO.image = q_a
       c_imgAO.location = (0 ,0)


       # add Blur
       ##############################
       c_blur = scene.node_tree.nodes.new('CompositorNodeBilateralblur')
       c_blur.location = (200,0)  
       c_blur.sigma_color  = myscene.T_ao_colorsigma
       c_blur.sigma_space  = myscene.T_ao_spacesigma



       # add NodeViewer
       ##############################
       c_view = scene.node_tree.nodes.new('CompositorNodeViewer')
       c_view.location = (600,0)  


       

       links.new( c_imgAO.outputs['Image'],
                  c_blur.inputs['Image'])
       links.new( c_imgNORMAL.outputs['Image'],
                  c_blur.inputs['Determinator'])
       links.new( c_blur.outputs['Image'],
                  c_view.inputs['Image'])




       bpy.ops.render.render()


       return True


# - NORMAL TO CURVATURE- ///////////////////////

def DEF_NormalToCurvature(context,size,name ):


       tex = MAT_texture_new(name+"_"+"curvature",size, 'Raw')
   

       # ucitaj scenu
       scene = bpy.context.scene

       scene.use_nodes = True

       nodes = scene.node_tree.nodes
       links = scene.node_tree.links

       myscene = context.scene.ga_property


       # clear
       ##############################
       while(nodes): nodes.remove(nodes[0])


       # get image NORMAL
       ##############################
       q_i = bpy.data.images.get(name+"_"+"normal")       
       #q_i.colorspace_settings.name = 'Linear'


       c_imgNORMAL = scene.node_tree.nodes.new('CompositorNodeImage')
       c_imgNORMAL.image = q_i
       c_imgNORMAL.location = (-300 ,0)

       # add image CURVATURE pixelwidth
       #################################
       c_imgCURVpixelwidth = scene.node_tree.nodes.new('CompositorNodeValue')
       c_imgCURVpixelwidth.location = (-300 ,-300)
       c_imgCURVpixelwidth.outputs[0].default_value = myscene.T_curvature_pixelwidth
       c_imgCURVpixelwidth.name = "Pixel width"
       c_imgCURVpixelwidth.label = "Pixel width"


       # add image CURVATURE shadow
       #################################
       c_imgCURVshadow = scene.node_tree.nodes.new('CompositorNodeValue')
       c_imgCURVshadow.location = (-300 ,-500)
       c_imgCURVshadow.name = "Shadows"
       c_imgCURVshadow.label = "Shadows"


       c_imgCURVshadow.outputs[0].default_value = 0


       # add NodeViewer
       ##############################
       c_view = scene.node_tree.nodes.new('CompositorNodeViewer')
       c_view.location = (400,0)  


       
       # clear all node_groups

       qnode = bpy.data.node_groups.get("Normal to Curvature")
       if  qnode is not None:
           bpy.data.node_groups.remove(qnode, do_unlink=True)


       GM_create_curvature_group("Normal to Curvature",myscene.T_curvature_blur)



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


       bpy.ops.render.render()


       return True






def GM_create_curvature_group(q_name,T_ntocrel):




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