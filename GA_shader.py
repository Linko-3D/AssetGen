import bpy, os
from math import *
from .GA_material import MAT_texture_new


# - EMISSIVE- ///////////////////////

def DEF_emissiveShader_add(context,size,name ):

    bpy.context.scene.render.engine = 'CYCLES'

    tex = MAT_texture_new(name+"_"+"emissive",size, 'Raw')

    mat = bpy.data.materials.get(name+"_"+"EMISSIVE")

    if  mat is None:
       mat = bpy.data.materials.new(name+"_"+"EMISSIVE")
     
       # Enable 'Use nodes':
       mat.use_nodes = True
       nt = mat.node_tree
       nodes = nt.nodes
       links = nt.links
       
       d_image   = nodes.new("ShaderNodeTexImage")
       
       d_image.location = (150,600)
       
       d_image.image = tex

    bpy.context.scene.render.engine = 'BLENDER_RENDER'


    return True

# - SURFACE NOISE- ///////////////////////

def DEF_surface_add(context):

        scene = bpy.context.scene
        myscene = context.scene.ga_property
        q_surface = 0
        q_red = 0
        c_mixArray = []

        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.space_data.viewport_shade = 'MATERIAL'

        ob = bpy.context.active_object

        #if not exist materiaal
        if len(ob.data.materials) == 0:
           q_difcolor = [0.8,0.8,0.8]
           mat = bpy.data.materials.new(name="Material")
           ob.data.materials.append(mat) 
        else: 
           q_difcolor = bpy.context.object.active_material.diffuse_color
           mat = bpy.context.active_object.active_material


        # Enable 'Use nodes':
        mat.use_nodes = True
        nt = mat.node_tree
        nodes = nt.nodes
        links = nt.links

        # clear
        while(nodes): nodes.remove(nodes[0])

        


        d_0 = nodes.new("ShaderNodeBsdfDiffuse")
        d_0.location = (0,0)
        d_0.inputs[0].default_value[0] = q_difcolor[0]
        d_0.inputs[0].default_value[1] = q_difcolor[1]
        d_0.inputs[0].default_value[2] = q_difcolor[2]


        d_10 = nodes.new("ShaderNodeOutputMaterial")
        d_10.location = (1200,0)

        links.new( d_10.inputs[0], d_0.outputs['BSDF'])


        if myscene.T_surface_noise == True:
           q_surface = q_surface + 1
           q_red = q_red - 250

           d_2 = nodes.new("ShaderNodeTexCoord")
           d_2.location = (0,q_red )

           d_3 = nodes.new("ShaderNodeTexNoise")
           d_3.location = (200,q_red )
           d_3.inputs[1].default_value = 10
           d_3.inputs[2].default_value = 16
           d_3.inputs[3].default_value = 0

           d_4 = nodes.new("ShaderNodeMath")
           d_4.location = (400,q_red )
           d_4.operation = 'MULTIPLY'
           d_4.inputs[1].default_value = 0.1

           links.new( d_2.outputs["Object"], d_3.inputs[0])
           links.new( d_3.outputs["Color"], d_4.inputs[0])

           c_mixArray.append(d_4.name)


        if myscene.T_surface_rock == True:
           q_surface = q_surface + 1
           q_red = q_red - 300

           d1_2 = nodes.new("ShaderNodeTexCoord")
           d1_2.location = (0,q_red )

           d1_3 = nodes.new("ShaderNodeTexNoise")
           d1_3.location = (200,q_red )
           d1_3.inputs[1].default_value = 1
           d1_3.inputs[2].default_value = 16
           d1_3.inputs[3].default_value = 0

           d1_4 = nodes.new("ShaderNodeTexVoronoi")
           d1_4.location = (400,q_red )
           d1_4.inputs["Scale"].default_value = 4.5


           d1_5 = nodes.new("ShaderNodeMath")
           d1_5.location = (600,q_red )
           d1_5.operation = 'MULTIPLY'
           d1_5.inputs[1].default_value = -0.5


           links.new( d1_2.outputs["Object"], d1_3.inputs[0])
           links.new( d1_3.outputs["Color"], d1_4.inputs[0])
           links.new( d1_4.outputs["Color"], d1_5.inputs[0])

           c_mixArray.append(d1_5.name)

        if myscene.T_surface_sand_waves == True:
           q_surface = q_surface + 1
           q_red = q_red - 300

           d2_2 = nodes.new("ShaderNodeTexCoord")
           d2_2.location = (0,q_red )

           d2_3 = nodes.new("ShaderNodeMapping")
           d2_3.location = (200,q_red )
           d2_3.rotation[2] = -0.785398

           d2_4 = nodes.new("ShaderNodeTexWave")
           d2_4.location = (600,q_red )
           d2_4.inputs[1].default_value = 3
           d2_4.inputs[2].default_value = 9
           d2_4.inputs[3].default_value = 16
           d2_4.inputs[4].default_value = 1

           d2_5 = nodes.new("ShaderNodeMath")
           d2_5.location = (800,q_red )
           d2_5.operation = 'MULTIPLY'
           d2_5.inputs[1].default_value = 0.1



           d2_6 = nodes.new("ShaderNodeTexNoise")
           d2_6.location = (600,q_red -300 )
           d2_6.inputs[1].default_value = 1000
           d2_6.inputs[2].default_value = 16
           d2_6.inputs[3].default_value = 0


           d2_7 = nodes.new("ShaderNodeMath")
           d2_7.location = (800,q_red -300)
           d2_7.operation = 'MULTIPLY'
           d2_7.inputs[1].default_value = 0.01


           d2_8 = nodes.new("ShaderNodeMath")
           d2_8.location = (1000,q_red )
           d2_8.operation = 'ADD'
           d2_8.inputs[1].default_value = 0.01



           links.new( d2_2.outputs["Object"], d2_3.inputs[0])
           links.new( d2_3.outputs["Vector"], d2_4.inputs["Vector"])
           links.new( d2_3.outputs["Vector"], d2_6.inputs["Vector"])

           links.new( d2_4.outputs["Color"], d2_5.inputs[0])
           links.new( d2_6.outputs["Color"], d2_7.inputs[0])

           links.new( d2_5.outputs["Value"], d2_8.inputs[0])
           links.new( d2_7.outputs["Value"], d2_8.inputs[1])


           c_mixArray.append(d2_8.name)

        if myscene.T_surface_wood_bark == True:
           q_surface = q_surface + 1
           q_red = q_red - 500
           q_col = -400

           d3_2 = nodes.new("ShaderNodeTexCoord")
           d3_2.location = (q_col +0,q_red )

           d3_3 = nodes.new("ShaderNodeMapping")
           d3_3.location = (q_col + 200,q_red )
           d3_3.scale[0] = 10
           d3_3.scale[1] = 10

           d3_4 = nodes.new("ShaderNodeTexNoise")
           d3_4.location = (q_col + 600,q_red )
           d3_4.inputs[1].default_value = 10
           d3_4.inputs[2].default_value = 16
           d3_4.inputs[3].default_value = 0

           d3_5 = nodes.new("ShaderNodeValToRGB")
           d3_5.location = (q_col + 800,q_red )
           d3_5.color_ramp.elements[0].position = 0
           d3_5.color_ramp.elements[1].position = 0.55

           d3_6 = nodes.new("ShaderNodeMath")
           d3_6.location = (q_col + 1200,q_red )
           d3_6.operation = 'MULTIPLY'
           d3_6.inputs[1].default_value = 0.2

           d3_7 = nodes.new("ShaderNodeMath")
           d3_7.location = (q_col + 1400,q_red )
           d3_7.operation = 'ADD'
 

           d3_8 = nodes.new("ShaderNodeTexNoise")
           d3_8.location = (q_col + 200,q_red -300 )
           d3_8.inputs[1].default_value = 50
           d3_8.inputs[2].default_value = 16
           d3_8.inputs[3].default_value = 0

           d3_9 = nodes.new("ShaderNodeMath")
           d3_9.location = (q_col + 400,q_red -300 )
           d3_9.operation = 'MULTIPLY'
           d3_9.inputs[1].default_value = 0.075


           links.new( d3_2.outputs["Object"], d3_3.inputs[0])
           links.new( d3_3.outputs["Vector"], d3_4.inputs["Vector"])
           links.new( d3_4.outputs["Fac"], d3_5.inputs["Fac"])
           links.new( d3_5.outputs["Color"], d3_6.inputs[0])
           links.new( d3_6.outputs["Value"], d3_7.inputs[0])

           links.new( d3_2.outputs["Object"], d3_8.inputs[0])
           links.new( d3_8.outputs["Color"], d3_9.inputs[0])

           links.new( d3_6.outputs["Value"], d3_7.inputs[0])
           links.new( d3_9.outputs["Value"], d3_7.inputs[1])


           c_mixArray.append(d3_7.name)



        c_addArray = []
        if len(c_mixArray) > 0:

           q_red = 0
           q_col = 900
           q_prolaz = 0
           for i in range(0,len(c_mixArray )):

              q_prolaz = q_prolaz + 1

              q_red = q_red - 250
              

              if q_prolaz == 1:

                 b_1 = nodes.new("ShaderNodeMath")
                 b_1.location = (q_col,q_red )
                 b_1.operation = 'ADD'
                 b_1.inputs[0].default_value = 0
                 b_1.inputs[1].default_value = 0

                 if len(c_addArray) > 0:
                    links.new( 
                      nodes[c_addArray[len(c_addArray)-1]].outputs['Value'],
                      b_1.inputs[0])

                    links.new( nodes[c_mixArray[i]].outputs['Value'],
                      b_1.inputs[1])
                 else:
                    links.new( nodes[c_mixArray[i]].outputs['Value'],
                      b_1.inputs[0])

                 

                 c_addArray.append(b_1.name)
                 q_col = q_col+300
      
              else:
                 links.new( nodes[c_mixArray[i]].outputs['Value'],
                      b_1.inputs[1])
                 q_prolaz = 0


           links.new( b_1.outputs['Value'], d_10.inputs[2])


        return True


# - GRADIENT- ///////////////////////

def DEF_gradientShader_add(context,size,name ):

    bpy.context.scene.render.engine = 'CYCLES'

    tex = MAT_texture_new(name+"_"+"gradient",size, 'Raw')

    mat = bpy.data.materials.get(name+"_"+"GRADIENT")

    if  mat is None:
       mat = bpy.data.materials.new(name+"_"+"GRADIENT")
     
       # Enable 'Use nodes':
       mat.use_nodes = True
       nt = mat.node_tree
       nodes = nt.nodes
       links = nt.links

       # clear
       while(nodes): nodes.remove(nodes[0])

       d_image   = nodes.new("ShaderNodeTexImage")    
       d_image.location = (150,500)    
       d_image.image = tex

       d_texcor = nodes.new("ShaderNodeTexCoord")
       d_texcor.location = (0,0)    

       d_bri = nodes.new("ShaderNodeBrightContrast")
       d_bri.location = (200,0)    

       d_map = nodes.new("ShaderNodeMapping")
       d_map.location = (400,0)    
       d_map.rotation[1] = 1.5708

       d_tgra = nodes.new("ShaderNodeTexGradient")
       d_tgra.location = (800,0)    
       d_tgra.gradient_type = 'QUADRATIC'


       d_emission = nodes.new("ShaderNodeEmission")
       d_emission.location = (1000,0)

       d_output   = nodes.new("ShaderNodeOutputMaterial")
       d_output.location = (1200,0)
    
       links.new( d_output.inputs['Surface'], d_emission.outputs['Emission'])
       links.new( d_emission.inputs['Color'], d_tgra.outputs['Color'])
       links.new( d_tgra.inputs['Vector'], d_map.outputs['Vector'])
       links.new( d_map.inputs['Vector'], d_bri.outputs['Color'])
       links.new( d_bri.inputs['Color'], d_texcor.outputs['Generated'])


    bpy.context.scene.render.engine = 'BLENDER_RENDER'


    return True




# - OPACITY- ///////////////////////

def DEF_opacityShader_add(context,size,name ):

    bpy.context.scene.render.engine = 'CYCLES'

    tex = MAT_texture_new(name+"_"+"opacity",size, 'Raw', False)

    mat = bpy.data.materials.get(name+"_"+"OPACITY")

    if  mat is None:
       mat = bpy.data.materials.new(name+"_"+"OPACITY")
     
       # Enable 'Use nodes':
       mat.use_nodes = True
       nt = mat.node_tree
       nodes = nt.nodes
       links = nt.links

       # clear
       while(nodes): nodes.remove(nodes[0])

       d_image   = nodes.new("ShaderNodeTexImage")    
       d_image.location = (150,0)    
       d_image.image = tex


       d_emission = nodes.new("ShaderNodeEmission")
       d_emission.location = (300,0)
       d_emission.inputs[0].default_value = (1, 1, 1, 1)

       d_output   = nodes.new("ShaderNodeOutputMaterial")
       d_output.location = (600,0)
    
       links.new( d_output.inputs['Surface'], d_emission.outputs['Emission'])

    bpy.context.scene.render.engine = 'BLENDER_RENDER'


    return True



# - BENT- ///////////////////////

def DEF_bentShader_add(context,size,name ):

    bpy.context.scene.render.engine = 'CYCLES'

    tex = MAT_texture_new(name+"_"+"bent",size, 'Raw')

    mat = bpy.data.materials.get(name+"_"+"BENT")

    if  mat is None:
       mat = bpy.data.materials.new(name+"_"+"BENT")
     
       # Enable 'Use nodes':
       mat.use_nodes = True
       nt = mat.node_tree
       nodes = nt.nodes
       links = nt.links
       
       d_image   = nodes.new("ShaderNodeTexImage")
       
       d_image.location = (150,600)
       
       d_image.image = tex

    bpy.context.scene.render.engine = 'BLENDER_RENDER'


    return True


#//////////////////// - POINTINESS - ///////////////////////

def DEF_pointinessShader_add(context,size,name ):

    tex = MAT_texture_new(name+"_"+"pointiness",size, 'Raw')

    mat = bpy.data.materials.get(name+"_"+"POINTINESS")

    if mat is None:
       mat = bpy.data.materials.new(name+"_"+"POINTINESS")
     
       # Enable 'Use nodes':
       mat.use_nodes = True
       nt = mat.node_tree
       nodes = nt.nodes
       links = nt.links
       
       # clear
       while(nodes): nodes.remove(nodes[0])

       d_geometry  = nodes.new("ShaderNodeNewGeometry")
       d_colorramp = nodes.new("ShaderNodeValToRGB")
       d_emission = nodes.new("ShaderNodeEmission")
       d_output   = nodes.new("ShaderNodeOutputMaterial")
       d_image   = nodes.new("ShaderNodeTexImage")
       
       d_geometry.location = (-100,-100)
       d_colorramp.location = (200,-100)      
       d_emission.location = (500,-100)
       d_output.location = (700,-100)
       d_image.location = (300,300)

       d_image.image = tex
       d_colorramp.color_ramp.elements[0].position = 0.4
       d_colorramp.color_ramp.elements[1].position = 0.6

       links.new( d_output.inputs['Surface'], d_emission.outputs['Emission'])
       links.new( d_emission.inputs['Color'], d_colorramp.outputs['Color'])
       links.new( d_colorramp.inputs['Fac'], d_geometry.outputs['Pointiness'])


    return True



# //////////////////- AMBIENT OCCLUSION- ///////////////////////

def DEF_ambientocclusionShader_add(context,size,name ):

    tex = MAT_texture_new(name+"_"+"ambient_occlusion",size, 'sRGB')

    mat = bpy.data.materials.get(name+"_"+"AMBIENT OCCLUSION")

    if  mat is None:
       mat = bpy.data.materials.new(name+"_"+"AMBIENT OCCLUSION")
     
       # Enable 'Use nodes':
       mat.use_nodes = True
       nt = mat.node_tree
       nodes = nt.nodes
       links = nt.links
       
       d_image   = nodes.new("ShaderNodeTexImage")
       
       d_image.location = (150,600)
       
       d_image.image = tex

    return True


#//////////////////// - ALBEDO- ///////////////////////

def DEF_albedoShader_add(context,size,name ):

    tex = MAT_texture_new(name+"_"+"albedo",size, 'sRGB')

    mat = bpy.data.materials.get(name+"_"+"ALBEDO")

    if  mat is None:
       mat = bpy.data.materials.new(name+"_"+"ALBEDO")
     
       # Enable 'Use nodes':
       mat.use_nodes = True
       nt = mat.node_tree
       nodes = nt.nodes
       links = nt.links
       
       d_image   = nodes.new("ShaderNodeTexImage")
       
       d_image.location = (150,600)
       
       d_image.image = tex

    return True



#//////////////////// - NORMAL- ///////////////////////

def DEF_normalShader_add(context,size,name ):

    tex = MAT_texture_new(name+"_"+"normal",size, 'Raw')

    mat = bpy.data.materials.get(name+"_"+"NORMAL")

    if  mat is None:
       mat = bpy.data.materials.new(name+"_"+"NORMAL")
     
       # Enable 'Use nodes':
       mat.use_nodes = True
       nt = mat.node_tree
       nodes = nt.nodes
       links = nt.links
       
       d_image   = nodes.new("ShaderNodeTexImage")
       
       d_image.location = (150,600)
       
       d_image.image = tex

    return True

#//////////////////// - METALLIC- ///////////////////////

def DEF_metallicShader_add(context,size,name ):

    tex = MAT_texture_new(name+"_"+"metallic",size, 'Raw')

    tex.colorspace_settings.name = 'Linear'
    tex.filepath = "//"+name+"_"+"metallic"+".tga"
    tex.source = 'FILE'



    mat = bpy.data.materials.get(name+"_"+"METALLIC")

    if  mat is None:
       mat = bpy.data.materials.new(name+"_"+"METALLIC")
     
       # Enable 'Use nodes':
       mat.use_nodes = True
       nt = mat.node_tree
       nodes = nt.nodes
       links = nt.links
       
       d_image   = nodes.new("ShaderNodeTexImage")
       
       d_image.location = (150,600)
       
       d_image.image = tex



    return True

#//////////////////// - ROUGHNESS- ///////////////////////

def DEF_roughnessShader_add(context,size,name ):

    tex = MAT_texture_new(name+"_"+"roughness",size, 'Raw')

    tex.colorspace_settings.name = 'Linear'
    tex.filepath = "//"+name+"_"+"roughness"+".tga"
    tex.source = 'FILE'


    mat = bpy.data.materials.get(name+"_"+"ROUGHNESS")

    if  mat is None:
       mat = bpy.data.materials.new(name+"_"+"ROUGHNESS")
     
       # Enable 'Use nodes':
       mat.use_nodes = True
       nt = mat.node_tree
       nodes = nt.nodes
       links = nt.links
       
       d_image   = nodes.new("ShaderNodeTexImage")
       
       d_image.location = (150,600)
       
       d_image.image = tex

    return True



#//////////////////// - MASK- ///////////////////////

def DEF_maskShader_add(context,size,name ):

    tex = MAT_texture_new(name+"_"+"mask",size, 'sRGB')

    mat = bpy.data.materials.get(name+"_"+"MASK")

    if  mat is None:
       mat = bpy.data.materials.new(name+"_"+"MASK")
     
       # Enable 'Use nodes':
       mat.use_nodes = True
       nt = mat.node_tree
       nodes = nt.nodes
       links = nt.links

       # clear
       while(nodes): nodes.remove(nodes[0])

       
       d_image   = nodes.new("ShaderNodeTexImage")    
       d_image.location = (150,400)    
       d_image.image = tex


       #I_albedo = bpy.data.images.get(name+"_"+"albedo")
       #d_1   = nodes.new("ShaderNodeTexImage")    
       #d_1.location = (0,0)
       #d_1.image = I_albedo 

       #d_emission = nodes.new("ShaderNodeEmission")
       #d_emission.location = (300,0)

       d_dif = nodes.new("ShaderNodeBsdfDiffuse")
       d_dif.location = (300,0)


       d_output   = nodes.new("ShaderNodeOutputMaterial")
       d_output.location = (600,0)
    
       links.new( d_output.inputs['Surface'], d_dif.outputs['BSDF'])


    return True


#//////////////////// - PBR- ///////////////////////

def DEF_pbrShader_add(context,size,name ):

    M_pbr = bpy.data.materials.get(name+"_"+"PBR")

    if  M_pbr is None:

        # Add PBR Material
        mat = bpy.data.materials.new(name=name+"_"+"PBR")
    
        mat.use_transparency = True
        mat.alpha = 0
        mat.specular_alpha = 0
        mat.diffuse_intensity = 1


        #Add METALLIC
        ############

        I_metallic = bpy.data.images.get(name+"_"+"metallic")

        #Add ROUGHNESS
        ############

        I_roughness = bpy.data.images.get(name+"_"+"roughness")



        #Add ALBEDO
        ############

        I_albedo = bpy.data.images.get(name+"_"+"albedo")


        A_tex = bpy.data.textures.new(name+"_"+"Albedo", 'IMAGE')
        A_tex.image = I_albedo


        slot = mat.texture_slots.add()
        slot.texture = A_tex
        slot.use_map_alpha = True    
    
        slot.blend_type = 'MIX'


        #Add Curvature
        ############

        I_Curvature = bpy.data.images.get(name+"_"+"pointiness")


        A_tex = bpy.data.textures.new(name+"_"+"Curvature", 'IMAGE')
        A_tex.image = I_Curvature


        #Add Ambient Occlusion
        ############

        I_ao = bpy.data.images.get(name+"_"+"ambient_occlusion")


        A_tex = bpy.data.textures.new(name+"_"+"Ambient_Occlusion", 'IMAGE')
        A_tex.image = I_ao


        slot = mat.texture_slots.add()
        slot.texture = A_tex
        slot.use_map_specular = True
        slot.use_map_color_spec = True
        slot.use_map_hardness = True
    
        slot.blend_type = 'MULTIPLY'


        #Add Normal
        ############

        I_Normal = bpy.data.images.get(name+"_"+"normal")

        A_tex = bpy.data.textures.new(name+"_"+"Normal", 'IMAGE')
        A_tex.image = I_Normal
        A_tex.use_normal_map = True

        slot = mat.texture_slots.add()
        slot.texture = A_tex
        slot.use_map_color_diffuse = False
        slot.use_map_normal = True


        slot.blend_type = 'MIX'

        #Blank slot
        ############

        slot = mat.texture_slots.add()

        #Add Mask
        ############

        I_Mask = bpy.data.images.get(name+"_"+"mask")

        A_tex = bpy.data.textures.new(name+"_"+"Mask", 'IMAGE')
        A_tex.image = I_Mask 

        slot = mat.texture_slots.add()
        slot.texture = A_tex
        slot.use_map_color_diffuse = True

        slot.blend_type = 'MIX'
        
        mat.use_textures[4] = False


        # CYCLES
        ##################################################
        bpy.context.scene.render.engine = 'CYCLES'

        # Enable 'Use nodes':
        mat.use_nodes = True
        nt = mat.node_tree
        nodes = nt.nodes
        links = nt.links

        # clear
        while(nodes): nodes.remove(nodes[0])

        
       
        d_1   = nodes.new("ShaderNodeBsdfPrincipled")
        d_1.location = (400,200)


        d_imagea   = nodes.new("ShaderNodeTexImage")
        d_imagea.location = (0,1200)
        d_imagea.image = I_albedo 

        links.new( d_1.inputs[0], d_imagea.outputs['Color'])

        d_imagem   = nodes.new("ShaderNodeTexImage")
        d_imagem.location = (0,900)
        d_imagem.image = I_metallic 
        d_imagem.color_space = 'NONE'

        links.new( d_1.inputs[4], d_imagem.outputs['Color'])

        d_imager   = nodes.new("ShaderNodeTexImage")
        d_imager.location = (0,600)
        d_imager.image = I_roughness 
        d_imager.color_space = 'NONE'
		
        links.new( d_1.inputs[7], d_imager.outputs['Color'])




        #d_image   = nodes.new("ShaderNodeTexImage")
        #d_image.location = (0,300)
        #d_image.color_space = 'NONE'

        #links.new( d_1.inputs[7], d_image.outputs['Color'])

        d_image   = nodes.new("ShaderNodeTexImage")
        d_image.location = (0,0)
        d_image.image = I_Normal 
        d_image.color_space = 'NONE'


        d_2   = nodes.new("ShaderNodeNormalMap")
        d_2.location = (200,-100)

        links.new( d_2.inputs['Color'], d_image.outputs['Color'])

        links.new( d_1.inputs['Normal'], d_2.outputs['Normal'])


        d_3   = nodes.new("ShaderNodeMixShader")
        d_3.location = (600,600)


        d_4   = nodes.new("ShaderNodeBsdfTransparent")
        d_4.location = (400,400)



        d_5   = nodes.new("ShaderNodeOutputMaterial")
        d_5.location = (900,400)

        links.new( d_5.inputs['Surface'], d_3.outputs['Shader'])
        links.new( d_3.inputs[1], d_4.outputs['BSDF'])
        links.new( d_3.inputs[2], d_1.outputs['BSDF'])
        links.new( d_3.inputs[0], d_imagea.outputs['Alpha'])


        mat.use_nodes = False
        bpy.context.scene.render.engine = 'BLENDER_RENDER'

    return True




#//////////////////// - Remove - ///////////////////////

def DEF_remove_all():

    # Remove all object 5. layer
    bpy.context.scene.layers[1] = True
    bpy.context.scene.layers[0] = False

    bpy.ops.object.select_all(action = 'SELECT')
    bpy.ops.object.delete(use_global=False)

    bpy.context.scene.layers[0] = True
    bpy.context.scene.layers[1] = False




