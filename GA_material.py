import bpy

# //////////////////- Bake Material- ///////////////////////

def DEF_material_add(context,size,name,type ):

    q_name = name+"_"+type

    tex = MAT_texture_new(q_name,size, 'sRGB')

    mat = bpy.data.materials.get("Bake")

    if  mat is None:
       mat = bpy.data.materials.new("Bake")
     
    # Enable 'Use nodes':
    mat.use_nodes = True
    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links
	   
	# clear
    while(nodes): nodes.remove(nodes[0])
       
    d_image   = nodes.new("ShaderNodeTexImage")
       
    d_image.location = (150,600)
       
    d_image.image = tex

    return True
	
	
	
#//////////////////// - PBR- ///////////////////////

def DEF_pbrShader_add(context,size,name ):

    mat = bpy.data.materials.get(name+"_"+"PBR")
    
    bpy.context.scene.render.engine = 'CYCLES'
	
    if  mat is None:
			
        # Add PBR Material
        mat = bpy.data.materials.new(name=name+"_"+"PBR")
		
		
    #Add basecolor
    ###############
    I_basecolor = bpy.data.images.get(name+"_"+"baseColor")

	#Add roughness
    ###############
    I_Roughness = bpy.data.images.get(name+"_"+"roughness")	

	#Add normal
    ###############
    I_Normal = bpy.data.images.get(name+"_"+"normal")			


    # Enable 'Use nodes':
    mat.use_nodes = True
    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links

    # clear
    while(nodes): nodes.remove(nodes[0])

       
    d_1   = nodes.new("ShaderNodeBsdfPrincipled")
    d_1.location = (400,200)


    d_image_basecolor = nodes.new("ShaderNodeTexImage")
    d_image_basecolor.location = (-250,350)
    d_image_basecolor.image = I_basecolor

    links.new( d_1.inputs[0], d_image_basecolor.outputs['Color'])

    d_image_metallic = nodes.new("ShaderNodeTexImage")
    d_image_metallic.location = (-400,75)

    d_image_roughness = nodes.new("ShaderNodeTexImage")
    d_image_roughness.location = (-400,-175)
    d_image_roughness.image = I_Roughness
    #d_image_roughness.color_space = 'NONE'
    links.new( d_1.inputs[7], d_image_roughness.outputs['Color'])


    d_image = nodes.new("ShaderNodeTexImage")
    d_image.location = (-100,-350)
    d_image.image = I_Normal 
    d_image.color_space = 'NONE'

    
    d_2   = nodes.new("ShaderNodeNormalMap")
    d_2.location = (200,-350)

    links.new( d_2.inputs['Color'], d_image.outputs['Color'])

    links.new( d_1.inputs['Normal'], d_2.outputs['Normal'])


    d_5   = nodes.new("ShaderNodeOutputMaterial")
    d_5.location = (900,400)

    links.new( d_5.inputs['Surface'], d_1.outputs[0])

    return True 	
	
	
	
#/////////////////////////////////////////////////////////////////////////////////////////////	
	
def MAT_texture_new(name,size, colorspc, q_alpha = True):
  

    tex = bpy.data.images.get(name)

    if  tex is None:
        tex = bpy.data.images.new(name, width=size[0], height=size[1], alpha = q_alpha)
        tex.colorspace_settings.name = colorspc
    else:
        #change resolution texture in datablock
        tex.source = 'GENERATED'
        tex.colorspace_settings.name = colorspc
        tex.generated_width = size[0]
        tex.generated_height = size[1]

    return tex