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

import  bpy


class GA_PT_Tools_HighPoly(bpy.types.Operator):

	bl_idname = "scene.ga_toolshighpoly"
	bl_label = "High Poly Conversion"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		for obj in bpy.context.selected_objects:
			bpy.context.view_layer.objects.active = obj

			bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

			bpy.context.active_object.modifiers.new("Bevel", 'BEVEL')
			bpy.context.object.modifiers["Bevel"].segments = 2
			bpy.context.object.modifiers["Bevel"].width = 0.005
			bpy.context.object.modifiers["Bevel"].angle_limit = 0.610865

			bpy.context.object.modifiers["Bevel"].use_clamp_overlap = False

			bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'

			bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
			bpy.context.object.modifiers["Subdivision"].levels = 2
			bpy.context.object.modifiers["Subdivision"].render_levels = 2

			bpy.ops.object.shade_smooth()

		return {'FINISHED'}

class GA_PT_Tools_Wear(bpy.types.Operator):

	bl_idname = "scene.ga_toolswear"
	bl_label = "Edge Wear"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
        
		bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

		bpy.context.active_object.modifiers.new("Remesh", 'REMESH')
		bpy.context.object.modifiers["Remesh"].octree_depth = 6
		bpy.context.object.modifiers["Remesh"].use_smooth_shade = True
	
		bpy.context.active_object.modifiers.new("Decimate", 'DECIMATE')
		bpy.context.object.modifiers["Decimate"].ratio = 0.3

		bpy.context.active_object.modifiers.new("Decimate", 'DECIMATE')
		bpy.context.object.modifiers["Decimate.001"].decimate_type = 'UNSUBDIV'
		bpy.context.object.modifiers["Decimate.001"].iterations = 1

		bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 3
		bpy.context.object.modifiers["Subdivision"].render_levels = 3

		return {'FINISHED'}

class GA_PT_Tools_Apply(bpy.types.Operator):

	bl_idname = "scene.ga_toolapply"
	bl_label = "Apply Meshes"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.object.convert(target='MESH')

		return {'FINISHED'}

class GA_PT_Tools_ResymX(bpy.types.Operator):

	bl_idname = "scene.ga_toolresymx"
	bl_label = "Resym X"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		for obj in bpy.context.selected_objects:
			bpy.context.view_layer.objects.active = obj
			
			bpy.ops.object.transform_apply(location=True, rotation=True, scale=False)

			bpy.context.active_object.modifiers.new("Mirror", 'MIRROR')
			bpy.context.object.modifiers["Mirror"].use_bisect_axis[0] = True
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")

		return {'FINISHED'}

class GA_PT_Tools_CutHalf(bpy.types.Operator):

	bl_idname = "scene.ga_toolcuthalf"
	bl_label = "Cut Half"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.mesh.select_all(action = 'SELECT')

		bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_inner=True, xstart=746, xend=746, ystart=431, yend=377)

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.object.mode_set(mode = 'OBJECT')

		return {'FINISHED'}

class GA_PT_Tools_FixNormals(bpy.types.Operator):

	bl_idname = "scene.ga_toolfixnormals"
	bl_label = "Fix Normals"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.normals_make_consistent(inside=False)

		bpy.ops.object.mode_set(mode = 'OBJECT')

		return {'FINISHED'}

class GA_PT_Tools_FlipNormals(bpy.types.Operator):

	bl_idname = "scene.ga_toolflipnormals"
	bl_label = "Flip Normals"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.flip_normals()

		bpy.ops.object.mode_set(mode = 'OBJECT')

		return {'FINISHED'}

class GA_PT_Tools_Union(bpy.types.Operator):

	bl_idname = "scene.ga_toolunion"
	bl_label = "Union/Fill/Fix"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.object.convert(target='MESH')
		bpy.ops.object.join()

		bpy.ops.object.mode_set(mode = 'EDIT') 
		bpy.ops.mesh.select_all(action = 'DESELECT')
		bpy.ops.mesh.select_mode(type="EDGE")

		bpy.ops.mesh.select_non_manifold()
		bpy.ops.mesh.edge_face_add()
		bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
		
		bpy.ops.mesh.select_loose()
		bpy.ops.mesh.delete(type='EDGE')

		bpy.ops.mesh.select_all(action = 'SELECT')
		
		bpy.ops.mesh.normals_make_consistent(inside=False)

		bpy.ops.mesh.separate(type='LOOSE')
		bpy.ops.object.mode_set(mode = 'OBJECT')

		i = 0

		for obj in bpy.context.selected_objects:
			bpy.context.view_layer.objects.active = obj

			i = i + 1
			bpy.context.object.name = "Mesh" + str(i)

		print("Info: Union boolean applied on", i, "meshes")

		bpy.ops.object.select_all(action= 'DESELECT')
		bpy.ops.object.select_pattern(pattern="Mesh" + str(i))
		bpy.context.view_layer.objects.active  = bpy.data .objects["Mesh" + str(i)]

		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.object.mode_set(mode = 'OBJECT')

		while i > 1:
			i = i - 1
			bpy.ops.object.select_pattern(pattern="Mesh" + str(i))
			bpy.ops.object.join()
			bpy.ops.object.mode_set(mode = 'EDIT')

			bpy.ops.mesh.intersect_boolean(operation='UNION')
			bpy.ops.mesh.select_all(action = 'SELECT')
			bpy.ops.object.mode_set(mode = 'OBJECT')

		return {'FINISHED'}

class GA_PT_Tools_Dyntopo(bpy.types.Operator):

	bl_idname = "scene.ga_tooldyntopo"
	bl_label = "Dyntopo"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.object.convert(target='MESH')
		bpy.ops.object.join()
		
		bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

		bpy.ops.object.mode_set(mode = 'SCULPT')
		bpy.ops.sculpt.dynamic_topology_toggle()
		
		bpy.context.scene.tool_settings.unified_paint_settings.size = 100
		bpy.context.scene.tool_settings.sculpt.detail_size = 8
		bpy.context.scene.tool_settings.unified_paint_settings.use_unified_strength = True
		bpy.context.scene.tool_settings.unified_paint_settings.strength = 1

		return {'FINISHED'}

class GA_PT_Tools_Subsurf(bpy.types.Operator):

	bl_idname = "scene.ga_toolsubsurf"
	bl_label = "Subsurf"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		bpy.ops.object.subdivision_set(level=1, relative=False)
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivision")

		return {'FINISHED'}

class GA_PT_Tools_Optimize(bpy.types.Operator):

	bl_idname = "scene.ga_tooloptimize"
	bl_label = "Reduce Polycount"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		for obj in bpy.context.selected_objects:
			bpy.context.view_layer.objects.active = obj
			
			bpy.ops.object.convert(target='MESH')

			bpy.context.active_object.modifiers.new("Decimate", 'DECIMATE')
			bpy.context.object.modifiers["Decimate"].ratio = 0.7
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")

		return {'FINISHED'}			

class GA_PT_Tools_DissolveUnnecessary(bpy.types.Operator):

	bl_idname = "scene.ga_tooldissolveunnecessary"
	bl_label = "Dissolve Unnecessary"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.dissolve_limited()
		bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
		bpy.ops.mesh.tris_convert_to_quads()

		bpy.ops.object.mode_set(mode = 'OBJECT')

		return {'FINISHED'}

class GA_PT_Tools_OnTheGround(bpy.types.Operator):

	bl_idname = "scene.ga_toolontheground"
	bl_label = "On The Ground"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		lowest_pt = min([(bpy.context.object.matrix_world  @ v.co).z for v in bpy.context.object.data.vertices])
		bpy.context.object.location.z -= lowest_pt

		return {'FINISHED'}

class GA_PT_Tools_UnrealTransforms(bpy.types.Operator):

	bl_idname = "scene.ga_unrealtransforms"
	bl_label = "Unreal Transforms"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.context.object.rotation_euler[0] = 1.5708
		bpy.context.object.rotation_euler[1] = 1.5708

		bpy.ops.transform.resize(value=(100, 100, 100), constraint_axis=(False, False, False), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

		return {'FINISHED'}

class GA_PT_Tools_Polycount(bpy.types.Operator):

	bl_idname = "scene.ga_toolpolycount"
	bl_label = "Get polycount"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
        
		for obj in bpy.context.selected_objects:
			bpy.context.view_layer.objects.active = obj
			
			bpy.context.object.name = str(len(bpy.context.active_object.data.polygons))

		return {'FINISHED'}

class GA_PT_Tools_BaseMesh(bpy.types.Operator):

	bl_idname = "scene.ga_toolbasemesh"
	bl_label = "Base Mesh"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, location=(0, 0, 0))
		bpy.ops.object.subdivision_set(level=2, relative=False)
		bpy.ops.object.convert(target='MESH')

		bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
		bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')

		bpy.ops.transform.resize(value=(0.15, 0.15, 0.15), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

		bpy.ops.object.mode_set(mode = 'EDIT')
					
		bpy.ops.mesh.select_all(action = 'SELECT')

		bpy.ops.transform.tosphere(value=1, mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

		bpy.ops.object.mode_set(mode = 'OBJECT')
		
		bpy.context.object.name = "Base Mesh"

		return {'FINISHED'}

class GA_PT_Tools_BoltCubic(bpy.types.Operator):

	bl_idname = "scene.ga_toolboltcubic"
	bl_label = "Bolt Cubic"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.mesh.primitive_plane_add(enter_editmode=False, location=(0, 0, 1))

		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.mesh.select_mode(type="VERT")
		bpy.ops.mesh.merge(type='CENTER')

		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, -1, -1), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 1, -1), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 1, 1), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, -1, 1), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(1, 7.54979e-008, -1), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.edge_face_add()
		bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.active_object.modifiers.new("Mirror", 'MIRROR')
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")


		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.mesh.remove_doubles()
		bpy.ops.mesh.normals_make_consistent(inside=False)
		bpy.ops.object.mode_set(mode = 'OBJECT')


		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')

		bpy.ops.transform.resize(value=(0.05, 0.05, 0.05), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

		bpy.context.active_object.modifiers.new("Bevel", 'BEVEL')
		bpy.context.object.modifiers["Bevel"].width = 0.005
		bpy.context.object.modifiers["Bevel"].segments = 2


		bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 2

		bpy.ops.object.shade_smooth()
		
		bpy.context.object.name = "Bolt Cubic"

		return {'FINISHED'}

class GA_PT_Tools_BoltCylinder(bpy.types.Operator):

	bl_idname = "scene.ga_toolboltcylinder"
	bl_label = "Bolt Cylinder"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.mesh.primitive_circle_add(vertices=8, enter_editmode=False, location=(0, 0, 0))
		bpy.ops.transform.resize(value=(0.04, 0.04, 0.04), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
		bpy.ops.object.mode_set(mode = 'EDIT')                    

		bpy.ops.mesh.edge_face_add()
		bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')

		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 0.0309654), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.transform.resize(value=(0.73, 0.73, 0.73), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')

		bpy.ops.mesh.select_all(action = 'SELECT')

		bpy.ops.mesh.normals_make_consistent(inside=False)
		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.active_object.modifiers.new("Bevel", 'BEVEL')
		bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel"].angle_limit = 0.785398
		bpy.context.object.modifiers["Bevel"].width = 0.005
		bpy.context.object.modifiers["Bevel"].segments = 2

		bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 2

		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
		
		bpy.ops.object.mode_set(mode = 'EDIT') 
		bpy.ops.transform.translate(value=(0, 0, 0.0126573), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		bpy.ops.object.mode_set(mode = 'OBJECT')
		
		bpy.ops.object.shade_smooth()
		
		bpy.context.object.name = "Bolt Cylinder"

		return {'FINISHED'}

class GA_PT_Tools_ChainHexagon(bpy.types.Operator):

	bl_idname = "scene.ga_toolchainhexagon"
	bl_label = "Chain Hexagon"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		bpy.ops.mesh.primitive_torus_add(location=(0, 0, 0), rotation=(0, 0, 0), major_segments=6, minor_segments=6, major_radius=1, minor_radius=0.4, abso_major_rad=1.25, abso_minor_rad=0.75)

		bpy.context.object.rotation_euler[0] = 1.5708
		bpy.context.object.rotation_euler[1] = 0.523599
		bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.mesh.select_mode(type="VERT")
		bpy.ops.mesh.bisect(plane_co=(1, 0, 0), plane_no=(0, 0, 1), use_fill=False, clear_inner=True, clear_outer=False, xstart=1087, xend=1232, ystart=470, yend=472)
		bpy.ops.mesh.select_all(action='INVERT')

		bpy.ops.transform.translate(value=(0, 0, 0.5), constraint_axis=(False, False, True), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

		bpy.ops.mesh.select_all(action = 'SELECT')

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.active_object.modifiers.new("Mirror", 'MIRROR')
		bpy.context.object.modifiers["Mirror"].use_axis[0] = False
		bpy.context.object.modifiers["Mirror"].use_axis[2] = True
		bpy.context.object.modifiers["Mirror"].use_clip = True
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")
		
		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0, 0, -2.2), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.transform.rotate(value=-1.5708, orient_axis='Z', orient_type='VIEW', orient_matrix=((-1, 0, 0), (0, -1, -0), (-0, 0, -1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.active_object.modifiers.new("Bevel", 'BEVEL')
		bpy.context.object.modifiers["Bevel"].use_clamp_overlap = False
		bpy.context.object.modifiers["Bevel"].width = 0.001

		bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 2
		
		bpy.context.active_object.modifiers.new("Array", 'ARRAY')
		bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 0
		bpy.context.object.modifiers["Array"].relative_offset_displace[2] = -0.75
		
		bpy.ops.object.modifier_add(type='CURVE')

		bpy.ops.transform.resize(value=(0.036, 0.036, 0.036), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
		
		

		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')

		bpy.ops.object.shade_smooth()
		
		bpy.context.object.name = "Chain Hexagon"

		return {'FINISHED'}

class GA_PT_Tools_ChainSquare(bpy.types.Operator):

	bl_idname = "scene.ga_toolchainsquare"
	bl_label = "Chain Square"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		bpy.ops.mesh.primitive_torus_add(location=(0, 0, 0), rotation=(0, 0, 0), major_segments=4, minor_segments=6, major_radius=1, minor_radius=0.45, abso_major_rad=1.25, abso_minor_rad=0.75)
		
		bpy.context.object.rotation_euler[0] = 1.5708
		bpy.context.object.rotation_euler[1] = 0.785398
		
		bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.mesh.select_mode(type="VERT")

		bpy.ops.mesh.bisect(plane_co=(1, 0, 0), plane_no=(0, 0, 1), use_fill=False, clear_inner=True, clear_outer=False, xstart=1087, xend=1232, ystart=470, yend=472)
		bpy.ops.mesh.select_all(action='INVERT')

		bpy.ops.transform.translate(value=(0, 0, 0.5), constraint_axis=(False, False, True), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		

		bpy.ops.mesh.select_all(action = 'SELECT')

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.active_object.modifiers.new("Mirror", 'MIRROR')
		bpy.context.object.modifiers["Mirror"].use_axis[0] = False
		bpy.context.object.modifiers["Mirror"].use_axis[2] = True
		bpy.context.object.modifiers["Mirror"].use_clip = True

		bpy.context.active_object.modifiers.new("Bevel", 'BEVEL')
		bpy.context.object.modifiers["Bevel"].use_clamp_overlap = False
		bpy.context.object.modifiers["Bevel"].width = 0.001

		bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 2

		bpy.ops.transform.resize(value=(0.036, 0.036, 0.036), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
		
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")

		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')

		bpy.ops.object.shade_smooth()

		bpy.context.object.name = "Chain Square"

		return {'FINISHED'}

class GA_PT_Tools_Crack(bpy.types.Operator):

	bl_idname = "scene.ga_toolcrack"
	bl_label = "Crack Boolean"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, location=(0, 0, 0))

		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.mesh.select_mode(type="VERT")
							
		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.merge(type='CENTER')

		bpy.ops.transform.translate(value=(2.91038e-10, -1.19567e-10, -0.00840229), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(3.05311e-16, -0.0110057, 0.000306666), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, -0.0386974, 0.00337183), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, -0.0248929, 0.00231325), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, -0.01811, 0.00165713), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, -0.0162515, 0.00128817), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.000760137, 0.000605941, 1.90648e-06), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-8.21659e-07, 0.0155581, -0.00117957), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(2.89395e-05, 0.0182741, -0.00165832), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.000399211, 0.0249536, -0.00217473), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.000492366, 0.0386664, -0.00316083), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(4.94388e-05, 0.0108993, -0.000300644), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.edge_face_add()
		bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
		bpy.ops.mesh.tris_convert_to_quads()

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.object.name = "tmpPart1"

		bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, location=(0, 0, 0))

		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.mesh.select_mode(type="VERT")
							
		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.merge(type='CENTER')

		bpy.ops.transform.translate(value=(0.00172927, -1.19572e-10, -0.00793743), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-4.94379e-05, -0.0108994, 0.000300643), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.000492366, -0.0386664, 0.00316083), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.000399211, -0.0249535, 0.00217473), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-2.89395e-05, -0.0182741, 0.00165832), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(8.21659e-07, -0.0155581, 0.00117957), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.000558638, 0.000909664, 1.34708e-05), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.00364322, 0.0140618, -1.59717e-05), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.00498601, 0.0192433, -7.5071e-06), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.00663937, 0.026988, -3.09502e-06), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.00768523, 0.0376021, 1.43662e-06), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.000803819, 0.00954673, 1.44259e-05), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.edge_face_add()
		bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
		bpy.ops.mesh.tris_convert_to_quads()

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.object.name = "tmpPart2"

		bpy.ops.object.select_pattern(pattern="tmpPart1")

		bpy.ops.object.join()
		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.mesh.remove_doubles()
		bpy.ops.mesh.normals_make_consistent(inside=False)
		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.ops.object.shade_smooth()

		bpy.context.active_object.modifiers.new("Mirror", 'MIRROR')
		bpy.context.object.modifiers["Mirror"].use_axis[1] = True
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")

		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.mesh.select_all(action = 'DESELECT')

		bpy.ops.mesh.select_non_manifold()
		bpy.ops.mesh.edge_face_add()

		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-1.61627e-16, -8.03529e-16, 0.000704463), "orient_type":'NORMAL', "orient_matrix":((-0.979746, -0.200243, -3.54901e-10), (0.200243, -0.979746, 7.13482e-11), (-3.62e-10, -1.16347e-12, 1)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-1.61627e-16, -8.03529e-16, 0.000704463), "orient_type":'NORMAL', "orient_matrix":((-0.979746, -0.200243, -3.54901e-10), (0.200243, -0.979746, 7.13482e-11), (-3.62e-10, -1.16347e-12, 1)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 2
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivision")
		
		bpy.ops.transform.resize(value=(2, 2, 5), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
		
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
		bpy.ops.object.shade_smooth()
		bpy.context.object.name = "Crack Boolean"
		return {'FINISHED'}

class GA_PT_Tools_ExtrudedCurve(bpy.types.Operator):

	bl_idname = "scene.ga_toolextrudedcurve"
	bl_label = "Extruded Curve"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.curve.primitive_nurbs_path_add(radius=1, enter_editmode=False, location=(0, 0, 0))
		bpy.ops.curve.primitive_nurbs_path_add(radius=0.5, enter_editmode=False, location=(0.00421777, -0.35954, 1.70905))
		bpy.context.object.data.bevel_depth = 0.05
		bpy.context.object.data.bevel_resolution = 6
		bpy.context.object.data.resolution_u = 20
		
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
		
		bpy.context.object.name = "Extruded Curve"

		return {'FINISHED'}

class GA_PT_Tools_ExtrudedMesh(bpy.types.Operator):

	bl_idname = "scene.ga_toolextrudedmesh"
	bl_label = "Extruded Mesh"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, location=(0, 0, 0))

		bpy.context.object.name = "motif"

		bpy.ops.object.mode_set(mode = 'EDIT')
		
		bpy.ops.mesh.select_mode(type="VERT")

		bpy.ops.mesh.merge(type='CENTER')

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 4

		bpy.context.active_object.modifiers.new("Skin", 'SKIN')
		bpy.context.object.modifiers["Skin"].use_smooth_shade = True

		bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
		bpy.context.object.modifiers["Subdivision.001"].levels = 3

		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')

		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.mesh.select_all(action = 'SELECT')

		bpy.ops.transform.skin_resize(value=(0.25, 0.25, 0.25), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.object.skin_root_mark()
		
		bpy.context.object.name = "Extruded Mesh"

		return {'FINISHED'}

class GA_PT_Tools_Hair(bpy.types.Operator):

	bl_idname = "scene.ga_toolhair"
	bl_label = "Hair/Fur"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		# Hair Strand

		bpy.ops.curve.primitive_bezier_curve_add(radius=1, enter_editmode=False, location=(0, 0, 0))


		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')

		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.transform.translate(value=(1, 0, 0), constraint_axis=(True, False, False), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.transform.rotate(value=-1.5708, orient_axis='Z', orient_type='VIEW', orient_matrix=((-4.93038e-32, -1, -2.22045e-16), (-2.22045e-16, -4.93038e-32, -1), (-1, -2.22045e-16, -4.93038e-32)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.ops.transform.resize(value=(0.15, 0.15, 0.15), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.curve.de_select_first()
		bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='VIEW', orient_matrix=((-1, -0, 0), (0, 1.34359e-07, -1), (-0, 1, 1.34359e-07)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

		bpy.ops.transform.translate(value=(-0.25, 0, -0.2), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.object.data.resolution_u = 64

		bpy.context.object.name = "HairStrand"

		# Hair Taper

		bpy.ops.curve.primitive_bezier_curve_add(radius=1, enter_editmode=False, location=(0, 0, 0))
		bpy.ops.transform.resize(value=(0.15, 0.15, 0.15), orient_type='VIEW', orient_matrix=((-0.410029, -0.911976, 0.0132648), (0.401743, -0.193644, -0.895045), (-0.818828, 0.361665, -0.445779)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.context.object.location[1] = -0.8

		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.curve.de_select_last()
		bpy.ops.transform.rotate(value=0.610865, orient_axis='Z', orient_type='VIEW', orient_matrix=((-1, 0, -0), (0, -1, 0), (-0, 0, -1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

		bpy.ops.transform.translate(value=(0, 0.04, 0), constraint_axis=(False, True, False), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.curve.de_select_last()


		bpy.ops.curve.de_select_first()
		bpy.ops.transform.rotate(value=0.436332, orient_axis='Z', orient_type='VIEW', orient_matrix=((-1, 0, -0), (0, -1, -0), (-0, 0, -1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)


		bpy.ops.object.mode_set(mode = 'OBJECT')
		bpy.context.object.name = "HairTaper"

		# Hair Bevel

		bpy.ops.curve.primitive_bezier_circle_add(radius=1, enter_editmode=False, location=(0, 0, 0))

		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.curve.handle_type_set(type='VECTOR')
		bpy.ops.transform.resize(value=(0.1, 0.1, 0.1), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.transform.resize(value=(1, 0.35, 1), constraint_axis=(False, True, False), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.curve.handle_type_set(type='AUTOMATIC')
		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.ops.transform.translate(value=(0, -1, 0), constraint_axis=(False, True, False), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

		bpy.context.object.name = "HairBevel"

		# Import curves

		bpy.ops.object.select_all(action = 'DESELECT')
		bpy.ops.object.select_pattern(pattern="HairStrand")
		bpy.context.view_layer.objects.active  = bpy.data.objects["HairStrand"]

		bpy.context.object.data.taper_object = bpy.data.objects["HairTaper"]
		bpy.context.object.data.bevel_object = bpy.data.objects["HairBevel"]

		bpy.ops.object.mode_set(mode = 'EDIT')
		
		return {'FINISHED'}

class GA_PT_Tools_RingCircle(bpy.types.Operator):

	bl_idname = "scene.ga_toolringcircle"
	bl_label = "Ring Circle"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.mesh.primitive_torus_add(location=(-0.00227314, -0.0087918, -0.013097), rotation=(0, 0, 0), major_segments=12, minor_segments=4, major_radius=1, minor_radius=0.3, abso_major_rad=1.25, abso_minor_rad=0.75)

		bpy.ops.transform.rotate(value=-1.5708, orient_axis='Z', orient_type='VIEW', orient_matrix=((-4.93038e-32, -1, -2.22045e-16), (-2.22045e-16, -4.93038e-32, -1), (-1, -2.22045e-16, -4.93038e-32)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		bpy.ops.transform.resize(value=(0.05, 0.05, 0.05), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

		bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

		bpy.context.active_object.modifiers.new("Bevel", 'BEVEL')
		bpy.context.object.modifiers["Bevel"].width = 0.001
		bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'

		bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 2

		bpy.ops.object.shade_smooth()
		
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
		
		bpy.context.object.name = "Ring Circle"
		return {'FINISHED'}

class GA_PT_Tools_RingSquare(bpy.types.Operator):

	bl_idname = "scene.ga_toolringsquare"
	bl_label = "Ring Square"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.mesh.primitive_torus_add(location=(0, 0, 0), rotation=(1.5708, 0, 0), major_segments=4, minor_segments=4, major_radius=1, minor_radius=0.4, abso_major_rad=1.25, abso_minor_rad=0.75)
		bpy.ops.transform.resize(value=(0.05, 0.05, 0.05), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

		bpy.context.active_object.modifiers.new("Bevel", 'BEVEL')
		bpy.context.object.modifiers["Bevel"].width = 0.005
		bpy.context.object.modifiers["Bevel"].segments = 2
		bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel"].use_clamp_overlap = False

		bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 2

		bpy.ops.object.shade_smooth()

		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
		
		bpy.context.object.name = "Ring Square"

		return {'FINISHED'}

class GA_PT_Tools_Rope(bpy.types.Operator):

	bl_idname = "scene.ga_toolrope"
	bl_label = "Rope"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.mesh.primitive_plane_add(enter_editmode=False, location=(0, 0, 0))

		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.mesh.select_mode(type="VERT")
		bpy.ops.mesh.merge(type='CENTER')

		bpy.ops.transform.translate(value=(-1, 0, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.707107, 0.292893, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.292893, 0.707107, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.292893, 0.707107, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.707107, 0.292893, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.707107, -0.292893, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.292893, -0.707107, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.292893, 0.707107, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.707107, 0.292893, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.707107, -0.292893, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.292893, -0.707107, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.292893, -0.707107, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.707107, -0.292893, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.707107, -0.292893, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.292893, -0.707107, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.292893, -0.707107, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.707107, -0.292893, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.707107, 0.292893, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.292893, 0.707107, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.292893, -0.707107, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.707107, -0.292893, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.707107, 0.292893, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.292893, 0.707107, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.292893, 0.707107, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.707107, 0.292893, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.mesh.select_all(action = 'SELECT')

		bpy.ops.mesh.remove_doubles()

		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 4), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.ops.object.modifier_add(type='SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 2

		bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
		bpy.context.object.modifiers["SimpleDeform"].deform_axis = 'Z'
		bpy.context.object.modifiers["SimpleDeform"].angle = 1.5708

		bpy.ops.object.modifier_add(type='ARRAY')
		bpy.context.object.modifiers["Array"].count = 10
		bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 0
		bpy.context.object.modifiers["Array"].relative_offset_displace[2] = 1


		bpy.ops.object.modifier_add(type='CURVE')
		bpy.context.object.modifiers["Curve"].deform_axis = 'POS_Z'

		bpy.ops.transform.resize(value=(0.025, 0.025, 0.025), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

		bpy.ops.object.shade_smooth()

		return {'FINISHED'}
		
class GA_PT_Tools_StrapCircle(bpy.types.Operator):

	bl_idname = "scene.ga_toolstrapcircle"
	bl_label = "Strap Circle"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.curve.primitive_bezier_circle_add(enter_editmode=False, location=(0, 0, 0))
		bpy.context.object.data.resolution_u = 3
		bpy.context.object.data.fill_mode = 'FULL'
		bpy.context.object.data.extrude = 0.05
		bpy.context.object.data.bevel_depth = 0.01
		bpy.context.object.data.bevel_resolution = 1

		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.transform.resize(value=(0.25, 0.25, 0.25), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		bpy.ops.curve.handle_type_set(type='ALIGNED')
		bpy.ops.object.mode_set(mode = 'OBJECT')
		
		bpy.ops.object.modifier_add(type='SUBSURF')
		bpy.context.object.modifiers["Subdivision"].render_levels = 2
		bpy.context.object.modifiers["Subdivision"].levels = 2

		
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')

		bpy.context.object.name = "Strap Circle"

		return {'FINISHED'}

class GA_PT_Tools_StrapHandle(bpy.types.Operator):

	bl_idname = "scene.ga_toolstraphandle"
	bl_label = "Strap Handle"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, enter_editmode=False, location=(0, 0, 0))

		bpy.ops.transform.resize(value=(0.05, 0.05, 0.04), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

		bpy.context.active_object.modifiers.new("SimpleDeform", 'SIMPLE_DEFORM')
		bpy.context.object.modifiers["SimpleDeform"].deform_method = 'TAPER'
		bpy.context.object.modifiers["SimpleDeform"].deform_axis = 'Y'
		bpy.context.object.modifiers["SimpleDeform"].factor = 0.75
		bpy.context.object.modifiers["SimpleDeform"].lock_x = True


		bpy.context.active_object.modifiers.new("SimpleDeform", 'SIMPLE_DEFORM')
		bpy.context.object.modifiers["SimpleDeform.001"].deform_method = 'TAPER'
		bpy.context.object.modifiers["SimpleDeform.001"].deform_axis = 'Z'
		bpy.context.object.modifiers["SimpleDeform.001"].factor = -0.25

		bpy.context.active_object.modifiers.new("Bevel", 'BEVEL')
		bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel"].width = 0.015
		bpy.context.object.modifiers["Bevel"].segments = 2

		bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 2

		bpy.context.object.name = "tmpStrap"

		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0.07), "constraint_axis":(False, False, True), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.context.object.modifiers["SimpleDeform"].factor = -0.75

		bpy.ops.object.select_pattern(pattern="tmpStrap")

		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0.14), "constraint_axis":(False, False, True), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.object.select_pattern(pattern="tmpStrap.001")
		bpy.ops.object.select_pattern(pattern="tmpStrap")

		bpy.ops.object.convert(target='MESH')
		bpy.ops.object.join()
		bpy.ops.object.shade_smooth()

		bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
		bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')


		bpy.context.object.name = "Strap Handle"

		return {'FINISHED'}

class GA_PT_Tools_StrapLine(bpy.types.Operator):

	bl_idname = "scene.ga_toolstrapline"
	bl_label = "Strap Line"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.curve.primitive_nurbs_path_add(radius=1, enter_editmode=False, location=(0.921556, -0.107272, 1))
		bpy.context.object.data.resolution_u = 64
		bpy.context.object.data.fill_mode = 'FULL'
		bpy.context.object.data.extrude = 0.1
		bpy.context.object.data.bevel_depth = 0.02

		bpy.ops.transform.resize(value=(0.5, 0.5, 0.5), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.transform.resize(value=(0.5, 0.5, 0.5), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		bpy.ops.object.mode_set(mode = 'OBJECT')
		
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')

		bpy.context.object.name = "Strap Line"

		return {'FINISHED'}

class GA_PT_Tools_Axe(bpy.types.Operator):

	bl_idname = "scene.ga_toolaxe"
	bl_label = "Axe"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):        

		#Deformer

		bpy.ops.object.add(type='LATTICE', enter_editmode=False, location=(0, 0, 0.375))

		bpy.context.object.data.points_w = 4

		bpy.context.object.scale[0] = 0.1

		bpy.context.object.scale[1] = 0.1

		bpy.context.object.name = "AxeEditor"

		# Strap

		bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, enter_editmode=False, location=(0, 0, 0))

		bpy.ops.transform.resize(value=(0.05, 0.05, 0.04), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

		bpy.context.active_object.modifiers.new("SimpleDeform", 'SIMPLE_DEFORM')
		bpy.context.object.modifiers["SimpleDeform"].deform_method = 'TAPER'
		bpy.context.object.modifiers["SimpleDeform"].deform_axis = 'Y'
		bpy.context.object.modifiers["SimpleDeform"].factor = 0.75
		bpy.context.object.modifiers["SimpleDeform"].lock_x = True


		bpy.context.active_object.modifiers.new("SimpleDeform", 'SIMPLE_DEFORM')
		bpy.context.object.modifiers["SimpleDeform.001"].deform_method = 'TAPER'
		bpy.context.object.modifiers["SimpleDeform.001"].deform_axis = 'Z'
		bpy.context.object.modifiers["SimpleDeform.001"].factor = -0.25

		bpy.context.active_object.modifiers.new("Bevel", 'BEVEL')
		bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel"].width = 0.015
		bpy.context.object.modifiers["Bevel"].segments = 2

		bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 2

		bpy.context.object.name = "StrapAxe"

		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0.07), "constraint_axis":(False, False, True), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.context.object.modifiers["SimpleDeform"].factor = -0.75

		bpy.ops.object.select_pattern(pattern="StrapAxe")

		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0.14), "constraint_axis":(False, False, True), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.object.select_pattern(pattern="StrapAxe.001")
		bpy.ops.object.select_pattern(pattern="StrapAxe")

		bpy.ops.object.convert(target='MESH')
		bpy.ops.object.join()
		bpy.context.object.name = "StrapAxe"

		bpy.ops.object.shade_smooth()

		# Main

		bpy.ops.mesh.primitive_cylinder_add(enter_editmode=False, location=(0, 0, 0.375))

		bpy.ops.transform.resize(value=(0.04, 0.04, 0.5), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

		bpy.context.object.name = "AxeBase"

		bpy.ops.mesh.primitive_cylinder_add(enter_editmode=False, location=(0, 0, 0.818853))

		bpy.ops.transform.resize(value=(0.055, 0.055, 0.025), orient_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

		bpy.ops.object.select_pattern(pattern="AxeBase")
		bpy.ops.object.join()


		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

		bpy.context.active_object.modifiers.new("Bevel", 'BEVEL')
		bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel"].segments = 2
		bpy.context.object.modifiers["Bevel"].profile = 1
		bpy.context.object.modifiers["Bevel"].width = 0.01
		bpy.context.object.modifiers["Bevel"].angle_limit = 0.785398

		bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 4
		bpy.context.object.modifiers["Subdivision"].render_levels = 4

		bpy.ops.object.convert(target='MESH')

		bpy.ops.object.select_pattern(pattern="StrapAxe")
		bpy.ops.object.join()
		bpy.context.object.name = "AxeBase"

		bpy.context.active_object.modifiers.new("Lattice", 'LATTICE')
		bpy.context.object.modifiers["Lattice"].object = bpy.data.objects["AxeEditor"]


		#AxeBlade

		bpy.ops.mesh.primitive_plane_add(enter_editmode=False, location=(0, -0.269897, 0.9255))

		bpy.ops.object.mode_set(mode = 'EDIT')
		
		bpy.ops.mesh.select_mode(type="VERT")

		bpy.ops.mesh.merge(type='CENTER')

		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(2.47638e-10, 0.0780657, -0.0765976), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-3.42268e-10, 0.0573154, -0.0218145), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(2.40561e-10, 0.212529, -0.0413638), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-9.62075e-11, -0.00180802, -0.0891602), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-1.2189e-10, -0.110631, -0.00950289), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(2.16133e-10, -0.101079, -0.0457134), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(3.21695e-10, 0.0279483, -0.0739753), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-3.06656e-10, 0.0292209, -0.0647398), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-1.98725e-10, -0.0769222, 0.0127718), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-1.38058e-10, -0.0681638, 0.0318949), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(2.18559e-10, -0.0734853, 0.0693971), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(2.13181e-10, -0.0133702, 0.101631), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-2.24659e-10, 0.0121764, 0.115206), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.edge_face_add()

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.active_object.modifiers.new("Solidify", 'SOLIDIFY')
		bpy.context.object.modifiers["Solidify"].thickness = 0.04
		bpy.context.object.modifiers["Solidify"].offset = 0
		bpy.context.object.modifiers["Solidify"].show_on_cage = True

		bpy.context.active_object.modifiers.new("Bevel", 'BEVEL')
		bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel"].width = 0.015
		bpy.context.object.modifiers["Bevel"].angle_limit = 0.785398

		bpy.context.active_object.modifiers.new("Bevel", 'BEVEL')
		bpy.context.object.modifiers["Bevel.001"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel.001"].width = 0.001
		bpy.context.object.modifiers["Bevel.001"].angle_limit = 0.698132

		bpy.context.active_object.modifiers.new("Triangulate", 'TRIANGULATE')

		bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 2

		bpy.ops.object.shade_smooth()
		bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

		bpy.context.object.name = "AxeBlade"

		bpy.ops.object.select_all(action = 'DESELECT')

		bpy.ops.object.select_pattern(pattern="AxeEditor")
  
		return {'FINISHED'}

class GA_PT_Tools_Shield(bpy.types.Operator):

	bl_idname = "scene.ga_toolshield"
	bl_label = "Shield"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.mesh.primitive_circle_add(vertices=16, enter_editmode=False, location=(0, 0, 0))

		bpy.ops.transform.rotate(value=-1.5708, orient_axis='Z', orient_type='VIEW', orient_matrix=((-4.93038e-32, -1, -2.22045e-16), (-2.22045e-16, -4.93038e-32, -1), (-1, -2.22045e-16, -4.93038e-32)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

		bpy.context.object.scale[0] = 0.335
		bpy.context.object.scale[1] = 0.333
		bpy.context.object.scale[2] = 0.335

		bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0, -0.0543865, -0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, True, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.transform.resize(value=(0.864, 0.864, 0.84), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0, -0.0348987, -0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, True, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.transform.resize(value=(0.683, 0.68, 0.67), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, -0.0151977, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, True, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.transform.resize(value=(0.653, 0.653, 0.635), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

		bpy.ops.mesh.edge_face_add()

		bpy.ops.mesh.inset(thickness=0.1, depth=-.01)

		bpy.ops.mesh.select_all(action = 'SELECT')

		bpy.ops.mesh.normals_make_consistent(inside=False)

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.active_object.modifiers.new("Solidify", 'SOLIDIFY')
		bpy.context.object.modifiers["Solidify"].thickness = 0.03

		bpy.context.active_object.modifiers.new("Bevel", 'BEVEL')
		bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel"].width = 0.003
		bpy.context.object.modifiers["Bevel"].angle_limit = 0.785398

		bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 2
		
		bpy.ops.object.shade_smooth()
		
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
		
		bpy.context.object.name = "Shield"

		return {'FINISHED'}
		
class GA_PT_Tools_Shoulder(bpy.types.Operator):

	bl_idname = "scene.ga_toolshoulder"
	bl_label = "Shoulder Guard"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, location=(0, 0, 0))
		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.mesh.select_mode(type="VERT")
		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.merge(type='CENTER')

		bpy.ops.transform.translate(value=(-0.0826497, -1.94363e-09, 0.0772539), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.0623267, 2.22045e-16, -0.0235535), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.0928321, 0, -0.0398878), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.056581, 0, -0.0449664), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.025281, 0, -0.0269958), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.0493649, -0.0814961, 0.0125206), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.0156111, 0.0162923, 0.0268505), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.030259, 0.0219638, 0.0338485), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.0694205, -0.0227891, 0.0259963), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.0826899, 0.000881597, 0.0211338), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.edge_face_add()
		bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
		bpy.ops.mesh.tris_convert_to_quads()

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.object.name = "tmpPart1"

		bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, location=(0, 0, 0))
		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.mesh.select_mode(type="VERT")
		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.merge(type='CENTER')

		bpy.ops.transform.translate(value=(-0.0929743, -0.0651475, 0.0622001), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.0826899, -0.000881605, -0.0211338), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.0694205, 0.0227891, -0.0259963), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.030259, -0.0219638, -0.0338485), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.0958697, -0.0579801, 0.00283617), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.118561, -0.0123266, 0.0176725), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.edge_face_add()
		bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
		bpy.ops.mesh.tris_convert_to_quads()

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.object.name = "tmpPart2"

		bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, location=(0, 0, 0))
		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.mesh.select_mode(type="VERT")
		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.merge(type='CENTER')

		bpy.ops.transform.translate(value=(-0.125035, -0.135511, 0.0017302), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.11856, 0.0123271, -0.0176725), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.0958697, 0.0579801, -0.00283617), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.0156111, -0.0162923, -0.0268505), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.108337, -0.0533254, -0.000413325), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.138605, -0.0143577, 0.0246369), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.edge_face_add()
		bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
		bpy.ops.mesh.tris_convert_to_quads()

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.object.name = "tmpPart3"

		bpy.ops.object.select_pattern(pattern="tmpPart1")
		bpy.ops.object.select_pattern(pattern="tmpPart2")

		bpy.ops.object.join()
		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.mesh.remove_doubles()
		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.active_object.modifiers.new("Mirror", 'MIRROR')
		bpy.context.object.modifiers["Mirror"].use_axis[0] = False
		bpy.context.object.modifiers["Mirror"].use_axis[1] = True
		bpy.context.object.modifiers["Mirror"].use_clip = True

		bpy.context.active_object.modifiers.new("Solidify", 'SOLIDIFY')
		bpy.context.object.modifiers["Solidify"].thickness = 0.03

		bpy.context.active_object.modifiers.new("Bevel", 'BEVEL')
		bpy.context.object.modifiers["Bevel"].width = 0.003
		bpy.context.object.modifiers["Bevel"].segments = 2
		bpy.context.object.modifiers["Bevel"].profile = 1
		bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel"].angle_limit = 1.48353

		bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
		bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 3

		bpy.context.object.name = "Shoulder Guard"
		
		bpy.ops.object.shade_smooth()

		return {'FINISHED'}
		
class GA_PT_Tools_Sword(bpy.types.Operator):

	bl_idname = "scene.ga_toolsword"
	bl_label = "Sword"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, location=(3.37511e-06, -1.11759e-08, 0.109301))
		bpy.ops.object.mode_set(mode = 'EDIT')
		
		bpy.ops.mesh.select_mode(type="VERT")

		bpy.ops.mesh.merge(type='CENTER')

		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.121359, 0, 0.0474132), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(-0.0300433, 5.71785e-008, 0.0220003), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(-0.0132741, -4.07694e-009, 0.0540008), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, -4.312e-008, 0.571141), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.0176937, -9.42212e-009, 0.1248), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(-0.0957351, -1.40763e-008, 0.186446), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})


		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.edge_face_add()

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.active_object.modifiers.new("Mirror", 'MIRROR')
		bpy.context.object.modifiers["Mirror"].use_bisect_axis[0] = True
		bpy.context.object.modifiers["Mirror"].use_clip = True

		bpy.context.active_object.modifiers.new("Solidify", 'SOLIDIFY')
		bpy.context.object.modifiers["Solidify"].offset = 0
		bpy.context.object.modifiers["Solidify"].thickness = 0.028
		bpy.context.object.modifiers["Solidify"].show_on_cage = True


		bpy.context.active_object.modifiers.new("Bevel", 'BEVEL')
		bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel"].width = 0.012
		bpy.context.object.modifiers["Bevel"].use_clamp_overlap = False

		bpy.context.active_object.modifiers.new("Bevel", 'BEVEL')
		bpy.context.object.modifiers["Bevel.001"].use_clamp_overlap = False
		bpy.context.object.modifiers["Bevel.001"].width = 0.003

		bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 2

		bpy.context.object.name = "Sword Blade"

		# Hand

		bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, location=(3.37511e-06, 2.77613e-08, 0.2723))

		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.mesh.merge(type='CENTER')

		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.0585713, 8.68674e-009, -0.115059), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.0361917, 1.67184e-010, -0.00221449), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.0427634, -2.03823e-009, 0.0269972), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.0208174, -2.1996e-009, 0.0291346), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.0300255, 4.06311e-009, -0.0538175), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(-0.156343, 5.46802e-009, -0.0724261), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.00240966, 6.47707e-009, -0.0857914), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(-0.00847854, 8.12588e-009, -0.107631), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.00841911, 1.71005e-009, -0.0226504), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.0215938, 1.0422e-009, -0.0138043), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(-0.00817733, 2.36718e-009, -0.0313544), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(-0.0235766, 1.98995e-009, -0.0263575), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(-0.0242162, 5.09147e-010, -0.00674379), "constraint_axis":(False, False, False), "orient_type":'GLOBAL', "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.edge_face_add()

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.active_object.modifiers.new("Mirror", 'MIRROR')
		bpy.context.object.modifiers["Mirror"].use_bisect_axis[0] = True
		bpy.context.object.modifiers["Mirror"].use_clip = True

		bpy.context.active_object.modifiers.new("Solidify", 'SOLIDIFY')
		bpy.context.object.modifiers["Solidify"].offset = 0
		bpy.context.object.modifiers["Solidify"].thickness = 0.05
		bpy.context.object.modifiers["Solidify"].show_on_cage = True


		bpy.context.active_object.modifiers.new("Bevel", 'BEVEL')
		bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel"].use_clamp_overlap = False
		bpy.context.object.modifiers["Bevel"].width = 0.015
		
		bpy.context.object.name = "Crossguard"

		return {'FINISHED'}

class GA_PT_Tools_Potion(bpy.types.Operator):

	bl_idname = "scene.ga_toolpotion"
	bl_label = "Potion"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, location=(0, 0, 0))

		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.mesh.select_mode(type="VERT")
							
		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.merge(type='CENTER')

		bpy.ops.transform.translate(value=(0, 1.79503e-08, -0.110178), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.037855, -1.6354e-09, 0.010038), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.027786, -4.47497e-09, 0.027467), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.010391, -6.13934e-09, 0.037683), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.009974, -6.11474e-09, 0.037532), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.042801, -6.84462e-09, 0.042012), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.001182, -6.86727e-09, 0.042151), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.018228, -1.21506e-09, 0.007458), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.003453, -2.62042e-09, 0.016084), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.039214, 3.59118e-08, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.active_object.modifiers.new("Screw", 'SCREW')
		bpy.context.object.modifiers["Screw"].steps = 8
		bpy.context.object.modifiers["Screw"].use_merge_vertices = True
		bpy.context.object.modifiers["Screw"].use_normal_flip = True

		bpy.context.active_object.modifiers.new("Bevel", 'BEVEL')
		bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel"].width = 0.003
		bpy.context.object.modifiers["Bevel"].angle_limit = 0.785398

		bpy.context.active_object.modifiers.new("Subdivision", 'SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 3
		
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
		
		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.mesh.select_mode(type="VERT")
							
		bpy.ops.mesh.select_all(action = 'SELECT')

		bpy.ops.transform.translate(value=(0.0377, 0, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

		bpy.ops.object.mode_set(mode = 'OBJECT')
		
		bpy.context.object.name = "Potion"

		bpy.ops.object.shade_smooth()

		return {'FINISHED'}