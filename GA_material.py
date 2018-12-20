import bpy

# //////////////////- Bake Material- ///////////////////////

def DEF_baseColor_add(context,size,name ):

    q_name = name+"_"+"basecolor"

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