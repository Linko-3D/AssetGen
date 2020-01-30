#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import  bpy, os ,time, random

from .GA_material import DEF_material_add
from .GA_material import DEF_pbrShader_add


class GA_Start(bpy.types.Operator):
	"""Will generate your game asset, Blender will freeze for few seconds. Follow the process in Window > System Console. IMPORTANT: the diffuse map can only be baked from an Emissive shader"""

	bl_idname = "scene.ga_start"
	bl_label = "Generate Asset"
	bl_options = {'REGISTER', 'UNDO'}


	def execute(self, context):

		myscene = context.scene.ga_property
	
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
		smoothHP = myscene.ga_smoothHP
		smoothLP = myscene.ga_smoothLP
		imposter = myscene.ga_imposter
		remesh = myscene.ga_remesh

		

		bake_textures = myscene.ga_baketextures
		
		bake_AO = myscene.ga_ao

		name = bpy.context.object.name
		samples = myscene.ga_samplecount

		path = bpy.path.abspath(myscene.ga_path)

		if calculate_LODs == 1:
			LOD1 = LOD0 / 2
			LOD2 = LOD0 / 4
			LOD3 = LOD0 / 8

		if selected_to_active == 1:
			imposter = 0
		
		if imposter == 1:
			selected_to_active = 2
			edge_padding = 0
			LOD1 = 0
			LOD2 = 0
			LOD3 = 0
		
		# EXECUTION

		print("\n- ASSETGEN IS RUNNING -\n")
		then = time.time() #Start the timer to see how long it takes to execute the script

		
		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
		bpy.context.scene.frame_set(1)

		if selected_to_active == 1:
			

			if len(bpy.context.selected_objects) > 1: #check how many meshes are selected, if one is selected, selected_to_active mode is disabled

				print("Selected to Active mode enabled\n")
				
				bpy.context.active_object.name = "tmpLP"

				obs = []
				for ob in bpy.context.selected_editable_objects:
					if ob.type == 'MESH' and ob != bpy.context.active_object:
						obs.append(ob)

				if len(obs) > 0:
					c = {}
					c["object"] = c["active_object"] = obs[0]
					c["selected_objects"] = c["selected_editable_objects"] = obs
					bpy.ops.object.join(c)

					obs[0].name = "tmpHP"
				
				bpy.ops.object.select_all(action = 'DESELECT')
				bpy.ops.object.select_pattern(pattern="tmpHP")
				bpy.context.view_layer.objects.active  = bpy.data.objects["tmpHP"]
				
				if smoothHP == 1:
					bpy.ops.object.shade_smooth()
				else:
					bpy.ops.object.shade_flat()
				
				bpy.ops.object.select_all(action = 'DESELECT')
				bpy.ops.object.select_pattern(pattern="tmpLP")
				bpy.context.view_layer.objects.active  = bpy.data.objects["tmpLP"]
				
				if smoothLP == 1:
					bpy.ops.object.shade_smooth()
				else:
					bpy.ops.object.shade_flat()					
				

				#Check if the low poly has UVs
				if not len( bpy.context.object.data.uv_layers ):
					print("> Info: the low poly has no UV Map, performing a Smart UV Project\n")
					#bpy.ops.uv.smart_project(angle_limit=uv_angle, island_margin=uv_margin) # Perform smart UV projection
				
			else:
				print("Selected to Active mode disabled (two meshes must be selected)\n")
				selected_to_active = 0


		if selected_to_active == 0:
		
			print("Generating the low poly...")
			
			bpy.ops.object.convert(target='MESH')
			bpy.ops.object.join()

			if smoothHP == 1:
				bpy.ops.object.shade_smooth()
			else:
				bpy.ops.object.shade_flat()

			bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

			bpy.context.object.name = "tmpHP"
			#bpy.data.objects["tmpHP"].animation_data_clear()
		
			if unfold_half == 1:
				bpy.context.active_object.modifiers.new("Mirror", 'MIRROR')
				bpy.context.object.modifiers["Mirror"].use_bisect_axis[0] = True
				bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")
			
			if myscene.ga_ontheground == 1:
				lowest_pt = min([(bpy.context.object.matrix_world  @ v.co).z for v in bpy.context.object.data.vertices])
				bpy.context.object.location.z -= lowest_pt

			# Generating the low poly

			bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
			
			bpy.context.object.name = "tmpLP"
			if remesh:
				print("Remeshing...")
				bpy.context.object.data.remesh_voxel_size = myscene.ga_voxelsize
				#bpy.context.object.data.use_remesh_fix_poles = False
				#bpy.context.object.data.use_remesh_smooth_normals = True
				#bpy.context.object.data.use_remesh_preserve_volume = False
				bpy.ops.object.voxel_remesh()
				print("Remesh complete")

			## Remove every material slots on the low poly only if the bake_textures mode is enabled

			if bake_textures == 1:
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
			bpy.ops.object.mode_set(mode = 'OBJECT')
		

		if selected_to_active == 0:
			## Cleaning low poly 1

			bpy.ops.object.mode_set(mode = 'EDIT')
			bpy.ops.mesh.select_all(action = 'SELECT')

			bpy.ops.mesh.remove_doubles()
			bpy.ops.mesh.delete_loose()
			bpy.ops.mesh.select_all(action = 'SELECT')
			

			bpy.ops.object.mode_set(mode = 'OBJECT')

			# Cleaning flat surfaces

			bpy.ops.object.mode_set(mode = 'EDIT')
			bpy.ops.mesh.select_all(action = 'SELECT')

			bpy.ops.mesh.dissolve_limited()

			bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')

			bpy.ops.object.mode_set(mode = 'OBJECT')

			# Decimation 1
    
			bpy.context.active_object.modifiers.new("Triangulate", 'TRIANGULATE')
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Triangulate")


			mesh_polycount = len(bpy.context.active_object.data.polygons)

			bpy.context.active_object.modifiers.new("Decimate", 'DECIMATE')
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
				bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
				
				bpy.ops.mesh.select_loose()
				bpy.ops.mesh.delete(type='EDGE')

				bpy.ops.mesh.select_all(action = 'SELECT')

				bpy.ops.mesh.separate(type='LOOSE')
				bpy.ops.object.mode_set(mode = 'OBJECT')

				i = 0

				for obj in bpy.context.selected_objects:
					bpy.context.view_layer.objects.active = obj

					i = i + 1
					bpy.context.object.name = "tmpLP" + str(i)

				print("\nInfo: Union boolean applied on", i, "meshes\n")


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

			bpy.context.active_object.modifiers.new("Triangulate", 'TRIANGULATE')
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Triangulate")

			mesh_polycount = len(bpy.context.active_object.data.polygons)

			bpy.context.active_object.modifiers.new("Decimate", 'DECIMATE')
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

			## Cleaning low poly 2

			bpy.ops.object.mode_set(mode = 'EDIT')
			bpy.ops.mesh.select_all(action = 'SELECT')

			bpy.ops.mesh.remove_doubles()
			bpy.ops.mesh.delete_loose()
			bpy.ops.mesh.select_all(action = 'SELECT')
			bpy.ops.object.mode_set(mode = 'OBJECT')
			
			# Unfold UVs

			bpy.ops.uv.smart_project(angle_limit=uv_angle, island_margin=uv_margin)

			if unfold_half == 1:
				bpy.context.active_object.modifiers.new("Mirror", 'MIRROR')
				bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")

			if smoothLP == 1:
				bpy.ops.object.shade_smooth()
			else:
				bpy.ops.object.shade_flat()

		# Add the ground if enabled

		if ground_AO == 1:
			bpy.ops.object.select_all(action = 'DESELECT')
			bpy.ops.object.select_pattern(pattern="tmpHP")
			bpy.context.view_layer.objects.active  = bpy.data.objects["tmpHP"]
			
			bpy.ops.object.mode_set(mode = 'EDIT')
			
			bpy.ops.mesh.primitive_plane_add(size=2, view_align=False, enter_editmode=False, location=(0, 0, 0))
			bpy.ops.transform.resize(value=(100, 100, 100), constraint_axis=(False, False, False), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
			bpy.ops.object.mode_set(mode = 'OBJECT')

			bpy.ops.object.select_all(action = 'DESELECT')
			bpy.ops.object.select_pattern(pattern="tmpLP")
			bpy.context.view_layer.objects.active = bpy.data.objects["tmpLP"]

		
		if selected_to_active == 2: #imposter cards creation
		
			bpy.ops.object.convert(target='MESH')
			bpy.ops.object.join()
		
			bpy.context.active_object.name = "tmpHP"
			
			scale = 1.5

			bpy.ops.mesh.primitive_plane_add(view_align=False, enter_editmode=False, location=(0, 0, 0))
			bpy.ops.object.mode_set(mode = 'EDIT')
			
			bpy.ops.transform.resize(value=(scale, scale, scale), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

			bpy.ops.transform.translate(value=(0, 0, 10), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)



			bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
			bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

			bpy.ops.transform.translate(value=(10, 0.0929842, -10), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
			
			
			bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='VIEW', orient_matrix=((-1, -0, 0), (0, 1.34359e-07, -1), (-0, 1, 1.34359e-07)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

			bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(-10, 0, -10), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
			bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='VIEW', orient_matrix=((-1, 0, -0), (0, 1.34359e-07, -1), (-0, 1, 1.34359e-07)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

			bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
			bpy.ops.transform.translate(value=(-10, -0, 10), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
			bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='VIEW', orient_matrix=((-1, 0, -0), (0, 1.34359e-07, -1), (-0, 1, 1.34359e-07)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

			bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
			bpy.ops.transform.translate(value=(10, -10, -0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
			bpy.ops.transform.rotate(value=-1.5708, orient_axis='Z', orient_type='VIEW', orient_matrix=((-1, 0, -0), (0, -1, -0), (-0, 0, -1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

			bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
			bpy.ops.transform.translate(value=(-0, 20, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
			bpy.ops.transform.rotate(value=3.14159, orient_axis='Z', orient_type='VIEW', orient_matrix=((-1, 0, -0), (0, -1, -0), (-0, 0, -1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

			bpy.ops.mesh.select_all(action = 'SELECT')

			bpy.ops.object.mode_set(mode = 'OBJECT')
			
			bpy.context.active_object.name = "tmpLP"

			bpy.ops.uv.smart_project()
					
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
		bpy.context.view_layer.objects.active = bpy.data.objects["tmpLP"]

		if bake_textures == 1:

			bpy.context.scene.cycles.samples = samples
		


			## Normal map bake

			print("\nBaking the normal map...")
			
			#Create Material
			DEF_material_add(context,size,name,"N")

			bpy.data.objects['tmpLP'].active_material = bpy.data.materials["Bake"]
			bpy.ops.object.bake(type="NORMAL", normal_space ='TANGENT', use_selected_to_active = True, use_cage = False, cage_extrusion = cage_size, margin = edge_padding, use_clear = True)
			
			## AO map bake
			
			if bake_AO == 1:
				print("\nBaking the ambient occclusion map...")
				
				#Create Material
				DEF_material_add(context,size,name,"AO")

				bpy.data.objects['tmpLP'].active_material = bpy.data.materials["Bake"]
				bpy.ops.object.bake(type="AO", use_selected_to_active = True, use_cage = False, cage_extrusion = cage_size, margin = edge_padding, use_clear = True)

			## Metallic map bake

			print("\nBaking the metallic map...")
			
			#Create Material
			DEF_material_add(context,size,name,"M")

			bpy.data.objects['tmpLP'].active_material = bpy.data.materials["Bake"]
			bpy.ops.object.bake(type="EMIT", use_selected_to_active = True, use_cage = False, cage_extrusion = cage_size, margin = edge_padding, use_clear = True)


			## Roughness map bake

			print("\nBaking the roughness map...")
			
			#Create Material
			DEF_material_add(context,size,name,"R")

			bpy.data.objects['tmpLP'].active_material = bpy.data.materials["Bake"]
			bpy.ops.object.bake(type="ROUGHNESS", use_selected_to_active = True, use_cage = False, cage_extrusion = cage_size, margin = edge_padding, use_clear = True)
			
			## Base color bake

			print("\nBaking the diffuse map...")
			
			#Create Material
			DEF_material_add(context,size,name,"A")	

			bpy.data.objects['tmpLP'].active_material = bpy.data.materials["Bake"]
			
			if myscene.ga_bakelighting == 0:
				bpy.ops.object.bake(type="DIFFUSE", use_selected_to_active = True, use_cage = False, cage_extrusion = cage_size, margin = edge_padding, use_clear = True, pass_filter=set({'COLOR'}))
			else:
				bpy.ops.object.bake(type="COMBINED", use_selected_to_active = True, use_cage = False, cage_extrusion = cage_size, margin = edge_padding, use_clear = True)
			
			print("\n")

		# Finalizing
		
		#Create Material
		if bake_textures == 1:
			DEF_pbrShader_add(context,size,name)

			bpy.data.objects['tmpLP'].active_material = bpy.data.materials["M_" + name]

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
		
		if selected_to_active == 2: # Merge the imposter cards
			bpy.ops.object.mode_set(mode = 'EDIT')
			
			bpy.ops.mesh.select_all(action = 'SELECT')

			bpy.ops.mesh.separate(type='LOOSE')

			bpy.ops.object.mode_set(mode = 'OBJECT')

			bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
			bpy.ops.object.location_clear(clear_delta=False)

			bpy.ops.object.join()

			

		# Remove the previous the LODs with the same names to update the result

		bpy.ops.object.select_all(action = 'DESELECT')

		bpy.ops.object.select_pattern(pattern= "SM_" + name + "_LOD0")
		bpy.ops.object.delete(use_global=False)

		bpy.ops.object.select_pattern(pattern= "SM_" + name + "_LOD1")
		bpy.ops.object.delete(use_global=False)

		bpy.ops.object.select_pattern(pattern= "SM_" + name + "_LOD2")
		bpy.ops.object.delete(use_global=False)

		bpy.ops.object.select_pattern(pattern= "SM_" + name + "_LOD3")
		bpy.ops.object.delete(use_global=False)

		bpy.ops.object.select_pattern(pattern= "tmpLP")

		# Name the game assets

		bpy.context.object.name = "SM_" + name + "_LOD0"
		bpy.context.object.data.name = "SM_" + name + "_LOD0"

		bpy.ops.object.modifier_remove(modifier="Bevel")
		
		# Center position
		
		if myscene.ga_centerXY == 1:
			bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
			bpy.context.object.location[0] = 0
			bpy.context.object.location[1] = 0

		# Change settings depending on the game engine
		
		if myscene.ga_unreal == 1:
		
			bpy.context.object.rotation_euler[0] = 1.5708
			bpy.context.object.rotation_euler[1] = 1.5708

			bpy.ops.transform.resize(value=(100, 100, 100), constraint_axis=(False, False, False), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

		# >>>>>>>>>>>>>>>>> EXPORT THE MESH
		if myscene.ga_file == "obj":
			bpy.ops.export_scene.obj(filepath=os.path.join(path, "SM_" + name + ".obj"), use_selection=True)
		if myscene.ga_file == "glb":
			bpy.ops.export_scene.gltf(export_format='GLB', export_selected=True, filepath=os.path.join(path, "SM_" + name))
		if myscene.ga_file == "glTF":
			bpy.ops.export_scene.gltf(export_format='GLTF_SEPARATE', export_selected=True, filepath=os.path.join(path, "SM_" + name))

		
		print("Asset", name, "exported to", path)
		

		bpy.ops.object.rotation_clear(clear_delta=False)
		bpy.ops.object.scale_clear(clear_delta=False)

		print("\nMesh infos:")

		print("LOD0:", len(bpy.context.active_object.data.polygons), "tris")


		bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

		if LOD1 > 0:
			## LOD1

			bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

			mesh_polycount = len(bpy.context.active_object.data.polygons)

			bpy.context.active_object.modifiers.new("Decimate", 'DECIMATE')
			bpy.context.object.modifiers["Decimate"].ratio = LOD1 / mesh_polycount
			bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")

			bpy.context.object.name = "SM_" + name + "_LOD1"
			bpy.context.object.data.name = "SM_" + name + "_LOD1"

			print("LOD1:", len(bpy.context.active_object.data.polygons), "tris")

		if LOD2 > 0:
			## LOD2

			bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

			mesh_polycount = len(bpy.context.active_object.data.polygons)

			bpy.context.active_object.modifiers.new("Decimate", 'DECIMATE')
			bpy.context.object.modifiers["Decimate"].ratio = LOD2 / mesh_polycount
			bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")

			bpy.context.object.name = "SM_" + name + "_LOD2"
			bpy.context.object.data.name = "SM_" + name + "_LOD2"

			print("LOD2:", len(bpy.context.active_object.data.polygons), "tris")

		if LOD3 > 0:
			## LOD3

			bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

			mesh_polycount = len(bpy.context.active_object.data.polygons)

			bpy.context.active_object.modifiers.new("Decimate", 'DECIMATE')
			bpy.context.object.modifiers["Decimate"].ratio = LOD3 / mesh_polycount
			bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")

			bpy.context.object.name = "SM_" + name + "_LOD3"
			bpy.context.object.data.name = "SM_" + name + "_LOD3"

			print("LOD2:", len(bpy.context.active_object.data.polygons), "tris")
		
		# Select every LODs to export in FBX
		
		bpy.ops.object.select_pattern(pattern= "SM_" + name + "_LOD0")
		bpy.ops.object.select_pattern(pattern= "SM_" + name + "_LOD1")
		bpy.ops.object.select_pattern(pattern= "SM_" + name + "_LOD2")
		bpy.ops.object.select_pattern(pattern= "SM_" + name + "_LOD3")
		
		if myscene.ga_file == "fbx":
			extension = bpy.context.object.name + ".fbx"
			bpy.ops.export_scene.fbx(filepath=os.path.join(path, extension), use_selection=True)
		
		# Moving the LODs behing the high poly
		bpy.ops.object.select_all(action = 'DESELECT')
		
		bpy.ops.object.select_pattern(pattern="SM_" + name + "_LOD0")
		bpy.ops.transform.translate(value=(0, 5, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		bpy.ops.object.select_all(action = 'DESELECT')
		
		bpy.ops.object.select_pattern(pattern="SM_" + name + "_LOD1")
		bpy.ops.transform.translate(value=(0, 10, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		bpy.ops.object.select_all(action = 'DESELECT')
		
		bpy.ops.object.select_pattern(pattern="SM_" + name + "_LOD2")
		bpy.ops.transform.translate(value=(0, 13, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		bpy.ops.object.select_all(action = 'DESELECT')
		
		bpy.ops.object.select_pattern(pattern="SM_" + name + "_LOD3")
		bpy.ops.transform.translate(value=(0, 16, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		bpy.ops.object.select_all(action = 'DESELECT')

		# If Show Output is set to false, delete the LODs

		if myscene.ga_showoutput == 0:
			bpy.ops.object.select_all(action = 'DESELECT')

			bpy.ops.object.select_pattern(pattern= "SM_" + name + "_LOD0")
			bpy.ops.object.delete(use_global=False)

			bpy.ops.object.select_pattern(pattern= "SM_" + name + "_LOD1")
			bpy.ops.object.delete(use_global=False)

			bpy.ops.object.select_pattern(pattern= "SM_" + name + "_LOD2")
			bpy.ops.object.delete(use_global=False)

			bpy.ops.object.select_pattern(pattern= "SM_" + name + "_LOD3")
			bpy.ops.object.delete(use_global=False)

		bpy.ops.object.select_all(action = 'DESELECT')
		bpy.ops.object.select_pattern(pattern= name)
		bpy.context.view_layer.objects.active  = bpy.data.objects[name]

		now = time.time() #Time after it finished
		print("\nAsset generated in", now-then, "seconds\n\n")

		return {'FINISHED'}