import  bpy, os ,time, random

from .GA_material import DEF_material_add
from .GA_material import DEF_pbrShader_add


class GA_Start(bpy.types.Operator):
	"""Will generate your game asset, Blender will freeze for few seconds. Follow the process in Window > System Console. IMPORTANT: the diffuse map can only be baked from an Emissive shader"""

	bl_idname = "scene.ga_start"
	bl_label = "Generate Asset"
	bl_options = {'REGISTER', 'UNDO'}


	def execute(self, context):

		#TEMP FORCE CPU
		bpy.context.scene.cycles.device = 'CPU'


		myscene = context.scene.ga_property

		# Click Run Script to convert your selected high poly to a game asset
		# Your shader must use an Emissive node
		
		size = [1024, 1024]

		if myscene.ga_textureX == '256':
			size[0] = 256

		if myscene.ga_textureX == '512':
			size[0] = 512

		if myscene.ga_textureX == '1K':
			size[0] = 1024

		if myscene.ga_textureX == '2K':
			size[0] = 2048

		if myscene.ga_textureX == '4K':
			size[0] = 4096

		if myscene.ga_textureY == '256':
			size[1] = 256

		if myscene.ga_textureY == '512':
			size[1] = 512

		if myscene.ga_textureY == '1K':
			size[1] = 1024

		if myscene.ga_textureY == '2K':
			size[1] = 2048

		if myscene.ga_textureY == '4K':
			size[1] = 4096
		
		
		
		LOD0 = myscene.ga_LOD0 
		LOD1 = myscene.ga_LOD1	
		LOD2 = myscene.ga_LOD2
		LOD3 = myscene.ga_LOD3		
		
		selected_to_active = myscene.ga_selectedtoactive
		unfold_half = myscene.ga_unfoldhalf
		calculate_LODs = myscene.ga_calculateLods		
		ground_AO = myscene.ga_groundao		
		remove_inside = myscene.ga_removeinside
		uv_angle = myscene.ga_uvangle
		uv_margin = myscene.ga_uvmargin
		cage_size = myscene.ga_cagesize
		edge_padding = myscene.ga_edgepadding		
		rmv_underground = myscene.ga_removeunderground
		convex_hull = myscene.ga_convexmesh
		smooth = myscene.ga_smooth

		
		center_X = 0
		center_Y = 0
		center_Z = 0

		bake_textures = myscene.ga_baketextures
		
		bake_AO = myscene.ga_ao

		name = bpy.context.object.name
		samples = myscene.ga_samplecount
		split_convex = 0
		
		path = bpy.path.abspath(myscene.ga_path)



		if calculate_LODs == 1:
			LOD1 = LOD0 / 2
			LOD2 = LOD0 / 4
			LOD3 = LOD0 / 8

		if convex_hull and split_convex == 1:
			remove_inside = 1
			


		#TEST
		
		print(myscene.ga_file)
		
		# EXECUTION

		print("\n- ASSETGEN IS RUNNING -\n")
		then = time.time() #Start the timer to see how long it takes to execute the script

		# Duplicate

		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		if selected_to_active == 1:
    
			print("\n> Selected to Active mode enabled\n")

			#Check if the low poly has UVs
			print("\n> Info: the low poly has no UV Map, performing a Smart UV Project\n")
			bpy.ops.uv.smart_project(angle_limit=uv_angle, island_margin=uv_margin) # Perform smart UV projection

			bpy.context.object.name = "tmpLP"

		if selected_to_active == 0:
		
			print("Generating the low poly...")
		
			bpy.ops.object.convert(target='MESH')
			bpy.ops.object.join()
    
			bpy.context.object.data.use_auto_smooth = False
			
			if smooth == 1:
				bpy.ops.object.shade_smooth()


			bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

			bpy.context.object.name = "tmpHP"
			
			if unfold_half == 1:
				bpy.ops.object.modifier_add(type='MIRROR')
				bpy.context.object.modifiers["Mirror"].use_bisect_axis[0] = True
				bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")

			# Generating the low poly

			bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

			bpy.context.object.name = "tmpLP"

			## Remove every material slots on the low poly

			for ob in bpy.context.selected_editable_objects:
				ob.active_material_index = 0
				for i in range(len(ob.material_slots)):
					bpy.ops.object.material_slot_remove({'object': ob})


			# Remove Underground

			if rmv_underground == 1:
				print("\n> Removing parts of the low poly bellow the grid")
				bpy.ops.object.mode_set(mode = 'EDIT')
                
				bpy.ops.mesh.select_all(action = 'SELECT')

				bpy.ops.mesh.bisect(plane_co=(0.00102639, 0.0334111, 0), plane_no=(0, 0, 0.999663), use_fill=False, clear_inner=True, xstart=295, xend=444, ystart=464, yend=461)

				bpy.ops.mesh.select_all(action = 'SELECT')
    
			## Cleaning low poly

			bpy.ops.object.mode_set(mode = 'EDIT')
			bpy.ops.mesh.select_all(action = 'SELECT')

			bpy.ops.mesh.remove_doubles()
			bpy.ops.mesh.delete_loose()
			bpy.ops.mesh.select_all(action = 'SELECT')

			# Convex Hull

			if convex_hull == 1:
				if split_convex == 1:
					bpy.ops.mesh.separate(type='LOOSE')
					bpy.ops.object.mode_set(mode = 'OBJECT')
					for obj in bpy.context.selected_objects:
						bpy.context.scene.objects.active = obj

						bpy.ops.object.mode_set(mode = 'EDIT')
						bpy.ops.mesh.select_all(action = 'SELECT')
						bpy.ops.mesh.convex_hull()
						bpy.ops.object.mode_set(mode = 'OBJECT')

					bpy.ops.object.join()
				else:
					bpy.ops.mesh.convex_hull()


			bpy.ops.object.mode_set(mode = 'OBJECT')

			# Cleaning flat surfaces

			bpy.ops.object.mode_set(mode = 'EDIT')
			bpy.ops.mesh.select_all(action = 'SELECT')

			bpy.ops.mesh.dissolve_limited()

			bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')

			bpy.ops.object.mode_set(mode = 'OBJECT')

			# Decimation 1
    
			bpy.ops.object.modifier_add(type='TRIANGULATE')
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Triangulate")


			mesh_polycount = len(bpy.context.active_object.data.polygons)

			bpy.ops.object.modifier_add(type='DECIMATE')
			bpy.context.object.modifiers["Decimate"].ratio = LOD0 / mesh_polycount
			bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")

			if remove_inside == 1:
				# Fill holes

				bpy.ops.object.mode_set(mode = 'EDIT') 
				bpy.ops.mesh.select_all(action = 'DESELECT')
				bpy.ops.mesh.select_mode(type="EDGE")

				bpy.ops.mesh.select_non_manifold()
				bpy.ops.mesh.edge_face_add()

				bpy.ops.mesh.select_all(action = 'SELECT')

				bpy.ops.mesh.separate(type='LOOSE')
				bpy.ops.object.mode_set(mode = 'OBJECT')

				i = 0

				for obj in bpy.context.selected_objects:
					bpy.context.view_layer.objects.active = obj

					i = i + 1
					bpy.context.object.name = "tmpLP" + str(i)

				print("Info: Union boolean applied on", i, "meshes")


				bpy.ops.object.select_all(action= 'DESELECT')
				bpy.ops.object.select_pattern(pattern="tmpLP" + str(i))
				bpy.context.view_layer.objects.active  = bpy.data .objects["tmpLP" + str(i)]

				bpy.ops.object.mode_set(mode = 'EDIT')
				bpy.ops.mesh.select_all(action = 'SELECT')
				bpy.ops.object.mode_set(mode = 'OBJECT')

				while i > 1:
					i = i - 1
					bpy.ops.object.select_pattern(pattern="tmpLP" + str(i))
					bpy.ops.object.join()
					bpy.ops.object.mode_set(mode = 'EDIT')

					bpy.ops.mesh.intersect_boolean(operation='UNION')
					bpy.ops.mesh.select_all(action = 'SELECT')
					bpy.ops.object.mode_set(mode = 'OBJECT')

				bpy.context.object.name = "tmpLP"

			# Decimation 2

			bpy.ops.object.modifier_add(type='TRIANGULATE')
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Triangulate")

			mesh_polycount = len(bpy.context.active_object.data.polygons)

			bpy.ops.object.modifier_add(type='DECIMATE')
			bpy.context.object.modifiers["Decimate"].ratio = LOD0 / mesh_polycount
			bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")

			if unfold_half == 1:
				bpy.ops.object.select_all(action = 'DESELECT')
				bpy.ops.object.select_pattern(pattern="tmpLP")

				bpy.ops.object.mode_set(mode = 'EDIT')
				bpy.ops.mesh.select_all(action = 'SELECT')

				bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_inner=True, clear_outer=False, xstart=849, xend=849, ystart=637, yend=473)
				bpy.ops.object.mode_set(mode = 'OBJECT')
			
			bpy.ops.object.mode_set(mode = 'EDIT')
			bpy.ops.mesh.select_all(action = 'SELECT')
			bpy.ops.mesh.remove_doubles(threshold=0.001)
			bpy.ops.object.mode_set(mode = 'OBJECT')

<<<<<<< HEAD
			## Cleaning low poly 2

			bpy.ops.object.mode_set(mode = 'EDIT')
			bpy.ops.mesh.select_all(action = 'SELECT')

			bpy.ops.mesh.remove_doubles()
			bpy.ops.mesh.delete_loose()
			bpy.ops.mesh.select_all(action = 'SELECT')
			bpy.ops.object.mode_set(mode = 'OBJECT')
			
			bpy.ops.object.modifier_add(type='EDGE_SPLIT')

			
=======
>>>>>>> parent of 1223224... clean low poly
			# Unfold UVs

			bpy.ops.uv.smart_project(angle_limit=uv_angle, island_margin=uv_margin)


			if unfold_half == 1:
				bpy.ops.object.modifier_add(type='MIRROR')
				bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")


			# Fixing the baking distortions

			if convex_hull == 1:
				bpy.ops.object.modifier_add(type='EDGE_SPLIT')
				bpy.context.object.modifiers["EdgeSplit"].split_angle = 0.802851


			bpy.ops.object.mode_set(mode = 'EDIT')
			bpy.ops.mesh.select_all(action = 'SELECT')
			bpy.ops.object.mode_set(mode = 'OBJECT')
			
			bpy.ops.object.shade_smooth()


		# Add the ground if enabled

		if ground_AO == 1:
			bpy.ops.object.select_all(action = 'DESELECT')
			bpy.ops.object.select_pattern(pattern="tmpHP")
			bpy.context.view_layer.objects.active  = bpy.data.objects["tmpHP"]
			
			bpy.ops.object.mode_set(mode = 'EDIT')
			
			bpy.ops.mesh.primitive_plane_add(size=2, view_align=False, enter_editmode=False, location=(0, 0, 0))
			bpy.ops.transform.resize(value=(100, 100, 100), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
			bpy.ops.object.mode_set(mode = 'OBJECT')

			bpy.ops.object.select_all(action = 'DESELECT')
			bpy.ops.object.select_pattern(pattern="tmpLP")
			bpy.context.view_layer.objects.active  = bpy.data.objects["tmpLP"]

		# Baking #########################################################################################################################

		bpy.context.scene.render.engine = 'CYCLES'



		# Detect if the High Poly has a material, if not assing the Base Texture grayscale

		bpy.ops.object.select_all(action = 'DESELECT')
		bpy.ops.object.select_pattern(pattern="tmpHP")
		#todo bpy.context.scene.objects.active = bpy.data.objects["tmpHP"]

		#if len(bpy.context.active_object.data.materials) == 0:
		#	bpy.data.objects['tmpHP'].active_material = bpy.data.materials["Base Texture"]

		bpy.ops.object.select_pattern(pattern="tmpLP")
		#todo bpy.context.scene.objects.active = bpy.data.objects["tmpLP"]

		if bake_textures == 1:
		
			bpy.context.scene.cycles.samples = samples
		
			## Base color bake

			print("\nBaking the base color map...")
			
			#Create Material
			DEF_material_add(context,size,name,"baseColor")	

			bpy.data.objects['tmpLP'].active_material = bpy.data.materials["Bake"]
			
			bpy.ops.object.bake(type="DIFFUSE", use_selected_to_active = True, use_cage = False, cage_extrusion = cage_size, margin = edge_padding, use_clear = True, pass_filter=set({'COLOR'}))

			## Normal map bake

			print("\nBaking the normal map...")
			
			#Create Material
			DEF_material_add(context,size,name,"normal")

			bpy.data.objects['tmpLP'].active_material = bpy.data.materials["Bake"]
			bpy.ops.object.bake(type="NORMAL", normal_space ='TANGENT', use_selected_to_active = True, use_cage = False, cage_extrusion = cage_size, margin = edge_padding, use_clear = True)
			
			## AO map bake
			
			if bake_AO == 1:
				print("\nBaking the ambient occclusion map...")
				
				#Create Material
				DEF_material_add(context,size,name,"ambientOcclusion")

				bpy.data.objects['tmpLP'].active_material = bpy.data.materials["Bake"]
				bpy.ops.object.bake(type="AO", use_selected_to_active = True, use_cage = False, cage_extrusion = cage_size, margin = edge_padding, use_clear = True)

			## Roughness map bake

			print("\nBaking the roughness map...")
			
			#Create Material
			DEF_material_add(context,size,name,"roughness")

			bpy.data.objects['tmpLP'].active_material = bpy.data.materials["Bake"]
			bpy.ops.object.bake(type="ROUGHNESS", use_selected_to_active = True, use_cage = False, cage_extrusion = cage_size, margin = edge_padding, use_clear = True)

		# Finalizing
		
		bpy.ops.object.modifier_remove(modifier="EdgeSplit")
		
		print("")
		
		#Create Material
		if bake_textures == 1:
			DEF_pbrShader_add(context,size,name)

			bpy.data.objects['tmpLP'].active_material = bpy.data.materials[name+"_"+"PBR"]

		# Delete the ground        
		if ground_AO == 1:
			bpy.ops.object.select_all(action = 'DESELECT')
			bpy.ops.object.select_pattern(pattern="ground_AO")
			bpy.ops.object.delete(use_global=False)

		## Delete the high poly

		bpy.ops.object.select_all(action = 'DESELECT')
		bpy.ops.object.select_pattern(pattern="tmpHP")

		bpy.ops.object.delete(use_global=False)


		bpy.ops.object.select_pattern(pattern="tmpLP")

		# Clean the LODs with the same names

		bpy.ops.object.select_all(action = 'DESELECT')

		bpy.ops.object.select_pattern(pattern= name + "_LOD0")
		bpy.ops.object.delete(use_global=False)

		bpy.ops.object.select_pattern(pattern= name + "_LOD1")
		bpy.ops.object.delete(use_global=False)

		bpy.ops.object.select_pattern(pattern= name + "_LOD2")
		bpy.ops.object.delete(use_global=False)

		bpy.ops.object.select_pattern(pattern= name + "_LOD3")
		bpy.ops.object.delete(use_global=False)

		bpy.ops.object.select_pattern(pattern= "tmpLP")

		# Name the game assets

		bpy.context.object.name = name + "_LOD0"
		bpy.context.object.data.name = name + "_LOD0"

		bpy.ops.object.modifier_remove(modifier="Bevel")

		# >>>>>>>>>>>>>>>>> EXPORT THE MESH
		if bake_textures == 1:
			if myscene.ga_file == "glb":
				bpy.ops.export_scene.gltf(export_format='GLB', export_selected=True, filepath=os.path.join(path, name))
			if myscene.ga_file == "glTF":
				bpy.ops.export_scene.gltf(export_format='GLTF_SEPARATE', export_selected=True, filepath=os.path.join(path, name))
			if myscene.ga_file == "obj":
				extension = bpy.context.object.name + ".obj"
				bpy.ops.export_scene.obj(filepath=os.path.join(path, extension), use_selection=True)

		
		print("Asset", name, "exported to", path)


		print("\nMesh infos:")

		print("LOD0:", len(bpy.context.active_object.data.polygons), "tris")
		
		
		# Center position
		
		if center_X == 1:
			bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
			bpy.context.object.location[0] = 0

		if center_Y == 1:
			bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
			bpy.context.object.location[1] = 0

		if center_Z == 1:
			bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
			bpy.context.object.location[2] = 0

		bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

		if LOD1 > 0:
			## LOD1

			bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, True, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})

			mesh_polycount = len(bpy.context.active_object.data.polygons)

			bpy.ops.object.modifier_add(type='DECIMATE')
			bpy.context.object.modifiers["Decimate"].ratio = LOD1 / mesh_polycount
			bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")

			bpy.context.object.name = name + "_LOD1"
			bpy.context.object.data.name = name + "_LOD1"

			print("LOD1:", len(bpy.context.active_object.data.polygons), "tris")

		if LOD2 > 0:
			## LOD2

			bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, True, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})

			mesh_polycount = len(bpy.context.active_object.data.polygons)

			bpy.ops.object.modifier_add(type='DECIMATE')
			bpy.context.object.modifiers["Decimate"].ratio = LOD2 / mesh_polycount
			bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")

			bpy.context.object.name = name + "_LOD2"
			bpy.context.object.data.name = name + "_LOD2"

			print("LOD2:", len(bpy.context.active_object.data.polygons), "tris")

		if LOD3 > 0:
			## LOD3

			bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, True, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})

			mesh_polycount = len(bpy.context.active_object.data.polygons)

			bpy.ops.object.modifier_add(type='DECIMATE')
			bpy.context.object.modifiers["Decimate"].ratio = LOD3 / mesh_polycount
			bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")

			bpy.context.object.name = name + "_LOD3"
			bpy.context.object.data.name = name + "_LOD3"

			print("LOD2:", len(bpy.context.active_object.data.polygons), "tris")
		
		bpy.ops.object.select_pattern(pattern=name + "_LOD0")
		bpy.ops.object.select_pattern(pattern=name + "_LOD1")
		bpy.ops.object.select_pattern(pattern=name + "_LOD2")
		bpy.ops.object.select_pattern(pattern=name + "_LOD3")
		
		if myscene.ga_file == "fbx":
			extension = bpy.context.object.name + ".fbx"
			bpy.ops.export_scene.fbx(filepath=os.path.join(path, extension), use_selection=True)
		
		#Offset
		bpy.ops.object.select_all(action = 'DESELECT')
		
		bpy.ops.object.select_pattern(pattern=name + "_LOD0")
		bpy.ops.transform.translate(value=(0, 5, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.object.select_all(action = 'DESELECT')
		
		bpy.ops.object.select_pattern(pattern=name + "_LOD1")
		bpy.ops.transform.translate(value=(0, 10, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.object.select_all(action = 'DESELECT')
		
		bpy.ops.object.select_pattern(pattern=name + "_LOD2")
		bpy.ops.transform.translate(value=(0, 13, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.object.select_all(action = 'DESELECT')
		
		bpy.ops.object.select_pattern(pattern=name + "_LOD3")
		bpy.ops.transform.translate(value=(0, 16, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.object.select_all(action = 'DESELECT')

		if myscene.ga_showoutput == 0:
			bpy.ops.object.select_all(action = 'DESELECT')

			bpy.ops.object.select_pattern(pattern= name + "_LOD0")
			bpy.ops.object.delete(use_global=False)

			bpy.ops.object.select_pattern(pattern= name + "_LOD1")
			bpy.ops.object.delete(use_global=False)

			bpy.ops.object.select_pattern(pattern= name + "_LOD2")
			bpy.ops.object.delete(use_global=False)

			bpy.ops.object.select_pattern(pattern= name + "_LOD3")
			bpy.ops.object.delete(use_global=False)

		bpy.ops.object.select_all(action = 'DESELECT')
		bpy.ops.object.select_pattern(pattern= name)
		bpy.context.view_layer.objects.active  = bpy.data.objects[name]

		bpy.context.scene.eevee.use_ssr = True
		bpy.context.scene.eevee.use_gtao = True

		#The lines bellow are here to refresh the SSR in case it was disabled before
		bpy.context.scene.render.engine = 'BLENDER_EEVEE'
		bpy.context.scene.render.engine = 'CYCLES'

		now = time.time() #Time after it finished
		print("\nAsset generated in", now-then, "seconds\n\n")

		return {'FINISHED'}