import  bpy


class GA_Tools_Stylized(bpy.types.Operator):

	bl_idname = "scene.ga_toolsstylized"
	bl_label = "Stylized"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		for obj in bpy.context.selected_objects:
			bpy.context.view_layer.objects.active = obj

			bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

			bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
			bpy.context.object.modifiers["SimpleDeform"].deform_method = 'TAPER'
			bpy.context.object.modifiers["SimpleDeform"].factor = -0.05
			bpy.context.object.modifiers["SimpleDeform"].deform_axis = 'Z'

			bpy.ops.object.modifier_add(type='BEVEL')
			bpy.context.object.modifiers["Bevel"].segments = 2
			bpy.context.object.modifiers["Bevel"].width = 0.025

			bpy.context.object.modifiers["Bevel"].use_clamp_overlap = False

			bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'

			bpy.ops.object.modifier_add(type='SUBSURF')
			bpy.context.object.modifiers["Subdivision"].levels = 3
			bpy.context.object.modifiers["Subdivision"].render_levels = 3

			bpy.ops.object.shade_smooth()

		return {'FINISHED'}
		
class GA_Tools_Wear(bpy.types.Operator):

	bl_idname = "scene.ga_toolswear"
	bl_label = "Wear"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
        
		bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

		bpy.ops.object.modifier_add(type='REMESH')
		bpy.context.object.modifiers["Remesh"].octree_depth = 6
		bpy.context.object.modifiers["Remesh"].use_smooth_shade = True
	
		bpy.ops.object.modifier_add(type='DECIMATE')
		bpy.context.object.modifiers["Decimate"].ratio = 0.3

		bpy.ops.object.modifier_add(type='DECIMATE')
		bpy.context.object.modifiers["Decimate.001"].decimate_type = 'UNSUBDIV'
		bpy.context.object.modifiers["Decimate.001"].iterations = 1

		bpy.ops.object.modifier_add(type='SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 3
		bpy.context.object.modifiers["Subdivision"].render_levels = 3

		return {'FINISHED'}

class GA_Tools_Apply(bpy.types.Operator):

	bl_idname = "scene.ga_toolapply"
	bl_label = "Apply Meshes"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.object.convert(target='MESH')

		return {'FINISHED'}

class GA_Tools_Smooth(bpy.types.Operator):

	bl_idname = "scene.ga_toolsmooth"
	bl_label = "Smooth"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.object.shade_smooth()

		return {'FINISHED'}
		
class GA_Tools_Flat(bpy.types.Operator):

	bl_idname = "scene.ga_toolflat"
	bl_label = "Flat"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.object.shade_flat()

		return {'FINISHED'}

class GA_Tools_OnTheGround(bpy.types.Operator):

	bl_idname = "scene.ga_toolontheground"
	bl_label = "On The Ground"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		lowest_pt = min([(bpy.context.object.matrix_world  @ v.co).z for v in bpy.context.object.data.vertices])
		bpy.context.object.location.z -= lowest_pt

		return {'FINISHED'}

class GA_Tools_SVerts(bpy.types.Operator):

	bl_idname = "scene.ga_toolsverts"
	bl_label = "Smooth Vertices"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.vertices_smooth(repeat=2)
		bpy.ops.object.mode_set(mode = 'OBJECT')

		return {'FINISHED'}

class GA_Tools_FixNormals(bpy.types.Operator):

	bl_idname = "scene.ga_toolfixnormals"
	bl_label = "Fix Normals"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.normals_make_consistent(inside=False)

		bpy.ops.object.mode_set(mode = 'OBJECT')

		return {'FINISHED'}

class GA_Tools_Union(bpy.types.Operator):

	bl_idname = "scene.ga_toolunion"
	bl_label = "Union Boolean"
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

class GA_Tools_Dyntopo(bpy.types.Operator):

	bl_idname = "scene.ga_tooldyntopo"
	bl_label = "Dyntopo"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.object.convert(target='MESH')
		bpy.ops.object.join()
		
		bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


		bpy.ops.object.mode_set(mode = 'SCULPT')
		bpy.ops.sculpt.dynamic_topology_toggle()

		bpy.context.scene.tool_settings.sculpt.detail_size = 6
		bpy.context.scene.tool_settings.unified_paint_settings.use_unified_strength = True
		bpy.context.scene.tool_settings.unified_paint_settings.strength = 1

		return {'FINISHED'}

class GA_Tools_Optimize(bpy.types.Operator):

	bl_idname = "scene.ga_tooloptimize"
	bl_label = "Optimize"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		for obj in bpy.context.selected_objects:
			bpy.context.view_layer.objects.active = obj
			
			bpy.ops.object.convert(target='MESH')

			bpy.ops.object.modifier_add(type='DECIMATE')
			bpy.context.object.modifiers["Decimate"].ratio = 0.7
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")

		return {'FINISHED'}			

class GA_Tools_ResymX(bpy.types.Operator):

	bl_idname = "scene.ga_toolresymx"
	bl_label = "Resym X"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		for obj in bpy.context.selected_objects:
			bpy.context.view_layer.objects.active = obj
			
			bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
			bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

			bpy.ops.object.modifier_add(type='MIRROR')
			bpy.context.object.modifiers["Mirror"].use_bisect_axis[0] = True
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")

		return {'FINISHED'}

class GA_Tools_DissolveUnnecessary(bpy.types.Operator):

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


class GA_Tools_BoltCubic(bpy.types.Operator):

	bl_idname = "scene.ga_toolboltcubic"
	bl_label = "Bolt Cubic"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.mesh.primitive_plane_add(view_align=False, enter_editmode=False, location=(0, 0, 1))

		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.mesh.merge(type='CENTER')

		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, -1, -1), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 1, -1), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 1, 1), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, -1, 1), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(1, 7.54979e-008, -1), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.edge_face_add()
		bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.ops.object.modifier_add(type='MIRROR')
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")


		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.mesh.remove_doubles()
		bpy.ops.mesh.normals_make_consistent(inside=False)
		bpy.ops.object.mode_set(mode = 'OBJECT')


		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')

		bpy.ops.transform.resize(value=(0.1, 0.1, 0.1), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

		bpy.ops.object.modifier_add(type='BEVEL')
		bpy.context.object.modifiers["Bevel"].width = 0.01
		bpy.context.object.modifiers["Bevel"].segments = 2


		bpy.ops.object.modifier_add(type='SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 2

		bpy.ops.object.shade_smooth()

		return {'FINISHED'}

class GA_Tools_Chain(bpy.types.Operator):

	bl_idname = "scene.ga_toolchain"
	bl_label = "Chain"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
        
		bpy.ops.mesh.primitive_torus_add(view_align=False, location=(0, 0, 0), rotation=(0, 0, 0), major_segments=6, minor_segments=6, major_radius=1, minor_radius=0.4, abso_major_rad=1.25, abso_minor_rad=0.75)

		bpy.context.object.rotation_euler[0] = 1.5708
		bpy.context.object.rotation_euler[1] = 0.523599
		bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.mesh.bisect(plane_co=(1, 0, 0), plane_no=(0, 0, 1), use_fill=False, clear_inner=True, clear_outer=False, xstart=1087, xend=1232, ystart=470, yend=472)
		bpy.ops.mesh.select_all(action='INVERT')

		bpy.ops.transform.translate(value=(0, 0, 0.5), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

		bpy.ops.mesh.select_all(action = 'SELECT')

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.ops.object.modifier_add(type='MIRROR')
		bpy.context.object.modifiers["Mirror"].use_axis[0] = False
		bpy.context.object.modifiers["Mirror"].use_axis[2] = True
		bpy.context.object.modifiers["Mirror"].use_clip = True

		bpy.ops.object.modifier_add(type='BEVEL')
		bpy.context.object.modifiers["Bevel"].use_clamp_overlap = False
		bpy.context.object.modifiers["Bevel"].width = 0.005

		bpy.ops.object.modifier_add(type='SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 2

		bpy.ops.transform.resize(value=(0.1, 0.1, 0.1), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

		bpy.ops.object.shade_smooth()

		return {'FINISHED'}

class GA_Tools_ExtrudedShape(bpy.types.Operator):

	bl_idname = "scene.ga_toolextrudedshape"
	bl_label = "Extruded Shape"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		bpy.ops.mesh.primitive_plane_add(size=2, view_align=False, enter_editmode=False, location=(0, 0, 0))

		bpy.context.object.name = "motif"

		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.mesh.merge(type='CENTER')

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.context.object.rotation_euler[0] = 0.00174533

		bpy.ops.object.modifier_add(type='SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 4

		bpy.ops.object.modifier_add(type='SKIN')
		bpy.context.object.modifiers["Skin"].use_smooth_shade = True

		bpy.ops.object.modifier_add(type='BEVEL')
		bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel"].use_clamp_overlap = False
		bpy.context.object.modifiers["Bevel"].width = 0.04

		bpy.ops.object.modifier_add(type='SUBSURF')
		bpy.context.object.modifiers["Subdivision.001"].levels = 3

		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')

		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.mesh.select_mode(type="VERT")

		bpy.ops.mesh.select_all(action = 'SELECT')

		bpy.ops.transform.skin_resize(value=(0.3, 0.3, 0.3), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

		return {'FINISHED'}

class GA_Tools_Ring(bpy.types.Operator):

	bl_idname = "scene.ga_toolring"
	bl_label = "Ring"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.mesh.primitive_torus_add(view_align=False, location=(0, 0, 0), rotation=(1.5708, 0, 0), major_segments=4, minor_segments=4, major_radius=1, minor_radius=0.4, abso_major_rad=1.25, abso_minor_rad=0.75)
		bpy.ops.transform.resize(value=(0.2, 0.2, 0.2), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

		bpy.ops.object.modifier_add(type='BEVEL')
		bpy.context.object.modifiers["Bevel"].width = 0.01
		bpy.context.object.modifiers["Bevel"].segments = 2
		bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel"].use_clamp_overlap = False

		bpy.ops.object.modifier_add(type='SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 2

		bpy.ops.object.shade_smooth()

		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')

		return {'FINISHED'}

class GA_Tools_Strap(bpy.types.Operator):

	bl_idname = "scene.ga_toolstrap"
	bl_label = "Strap"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.curve.primitive_bezier_circle_add(view_align=False, enter_editmode=False, location=(0, 0, 0))
		bpy.context.object.data.resolution_u = 64
		bpy.context.object.data.fill_mode = 'FULL'
		bpy.context.object.data.extrude = 0.1
		bpy.context.object.data.bevel_depth = 0.02

		bpy.ops.transform.resize(value=(0.5, 0.5, 0.5), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.curve.handle_type_set(type='ALIGNED')
		bpy.ops.object.mode_set(mode = 'OBJECT')

		return {'FINISHED'}

class GA_Tools_Axe(bpy.types.Operator):

	bl_idname = "scene.ga_toolaxe"
	bl_label = "Axe"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
        
		#Deformer

		bpy.ops.object.add(type='LATTICE', view_align=False, enter_editmode=False, location=(0, 0, 0.375))

		bpy.context.object.data.points_w = 4

		bpy.context.object.scale[0] = 0.1

		bpy.context.object.scale[1] = 0.1

		bpy.context.object.name = "AxeEditor"

		# Strap

		bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, view_align=False, enter_editmode=False, location=(0, 0, 0))

		bpy.ops.transform.resize(value=(0.05, 0.05, 0.04), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

		bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
		bpy.context.object.modifiers["SimpleDeform"].deform_method = 'TAPER'
		bpy.context.object.modifiers["SimpleDeform"].deform_axis = 'Y'
		bpy.context.object.modifiers["SimpleDeform"].factor = 0.75
		bpy.context.object.modifiers["SimpleDeform"].lock_x = True


		bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
		bpy.context.object.modifiers["SimpleDeform.001"].deform_method = 'TAPER'
		bpy.context.object.modifiers["SimpleDeform.001"].deform_axis = 'Z'
		bpy.context.object.modifiers["SimpleDeform.001"].factor = -0.25

		bpy.ops.object.modifier_add(type='BEVEL')
		bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel"].width = 0.015
		bpy.context.object.modifiers["Bevel"].segments = 2

		bpy.ops.object.modifier_add(type='SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 2


		bpy.context.object.name = "Strap"

		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0.07), "constraint_axis":(False, False, True), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.context.object.modifiers["SimpleDeform"].factor = -0.75

		bpy.ops.object.select_pattern(pattern="Strap")

		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0.14), "constraint_axis":(False, False, True), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.object.select_pattern(pattern="Strap.001")
		bpy.ops.object.select_pattern(pattern="Strap")

		bpy.ops.object.convert(target='MESH')
		bpy.ops.object.join()
		bpy.context.object.name = "Strap"



		bpy.ops.object.shade_smooth()

		# Main

		bpy.ops.mesh.primitive_cylinder_add(view_align=False, enter_editmode=False, location=(0, 0, 0.375))

		bpy.ops.transform.resize(value=(0.04, 0.04, 0.5), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

		bpy.context.object.name = "AxeBase"

		bpy.ops.mesh.primitive_cylinder_add(view_align=False, enter_editmode=False, location=(0, 0, 0.818853))

		bpy.ops.transform.resize(value=(0.055, 0.055, 0.025), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

		bpy.ops.object.select_pattern(pattern="AxeBase")
		bpy.ops.object.join()


		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

		bpy.ops.object.modifier_add(type='BEVEL')
		bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel"].segments = 2
		bpy.context.object.modifiers["Bevel"].profile = 1
		bpy.context.object.modifiers["Bevel"].width = 0.01
		bpy.context.object.modifiers["Bevel"].angle_limit = 0.785398

		bpy.ops.object.modifier_add(type='SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 4
		bpy.context.object.modifiers["Subdivision"].render_levels = 4

		bpy.ops.object.convert(target='MESH')

		bpy.ops.object.select_pattern(pattern="Strap")
		bpy.ops.object.join()
		bpy.context.object.name = "AxeBase"

		bpy.ops.object.modifier_add(type='LATTICE')
		bpy.context.object.modifiers["Lattice"].object = bpy.data.objects["AxeEditor"]


		#AxeBlade

		bpy.ops.mesh.primitive_plane_add(view_align=False, enter_editmode=False, location=(0, -0.269897, 0.9255))



		bpy.ops.object.mode_set(mode = 'EDIT')


		bpy.ops.mesh.merge(type='CENTER')

		bpy.ops.mesh.select_mode(type="VERT")

		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(2.47638e-10, 0.0780657, -0.0765976), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-3.42268e-10, 0.0573154, -0.0218145), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(2.40561e-10, 0.212529, -0.0413638), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-9.62075e-11, -0.00180802, -0.0891602), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-1.2189e-10, -0.110631, -0.00950289), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(2.16133e-10, -0.101079, -0.0457134), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(3.21695e-10, 0.0279483, -0.0739753), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-3.06656e-10, 0.0292209, -0.0647398), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-1.98725e-10, -0.0769222, 0.0127718), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-1.38058e-10, -0.0681638, 0.0318949), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(2.18559e-10, -0.0734853, 0.0693971), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(2.13181e-10, -0.0133702, 0.101631), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-2.24659e-10, 0.0121764, 0.115206), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.edge_face_add()

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.ops.object.modifier_add(type='SOLIDIFY')
		bpy.context.object.modifiers["Solidify"].thickness = 0.04
		bpy.context.object.modifiers["Solidify"].offset = 0
		bpy.context.object.modifiers["Solidify"].show_on_cage = True


		bpy.ops.object.modifier_add(type='BEVEL')
		bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel"].width = 0.015
		bpy.context.object.modifiers["Bevel"].angle_limit = 0.785398


		bpy.ops.object.modifier_add(type='BEVEL')
		bpy.context.object.modifiers["Bevel.001"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel.001"].width = 0.001
		bpy.context.object.modifiers["Bevel.001"].angle_limit = 0.698132


		bpy.ops.object.modifier_add(type='TRIANGULATE')

		bpy.ops.object.modifier_add(type='SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 2

		bpy.ops.object.shade_smooth()
		bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')


		bpy.context.object.name = "AxeBlade"

		bpy.ops.object.select_all(action = 'DESELECT')

		bpy.ops.object.select_pattern(pattern="AxeEditor")
  


		return {'FINISHED'}

class GA_Tools_Sword(bpy.types.Operator):

	bl_idname = "scene.ga_toolsword"
	bl_label = "Sword"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		bpy.ops.mesh.primitive_plane_add(size=2, view_align=False, enter_editmode=False, location=(3.37511e-06, -1.11759e-08, 0.109301))
		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.mesh.merge(type='CENTER')

		bpy.ops.mesh.select_mode(type="VERT")

		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.121359, 0, 0.0474132), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(-0.0300433, 5.71785e-008, 0.0220003), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(-0.0132741, -4.07694e-009, 0.0540008), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, -4.312e-008, 0.571141), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.0176937, -9.42212e-009, 0.1248), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(-0.0957351, -1.40763e-008, 0.186446), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})


		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.edge_face_add()

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.ops.object.modifier_add(type='MIRROR')
		bpy.context.object.modifiers["Mirror"].use_bisect_axis[0] = True
		bpy.context.object.modifiers["Mirror"].use_clip = True

		bpy.ops.object.modifier_add(type='SOLIDIFY')
		bpy.context.object.modifiers["Solidify"].offset = 0
		bpy.context.object.modifiers["Solidify"].thickness = 0.028
		bpy.context.object.modifiers["Solidify"].show_on_cage = True


		bpy.ops.object.modifier_add(type='BEVEL')
		bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel"].width = 0.012
		bpy.context.object.modifiers["Bevel"].use_clamp_overlap = False

		bpy.ops.object.modifier_add(type='BEVEL')
		bpy.context.object.modifiers["Bevel.001"].use_clamp_overlap = False
		bpy.context.object.modifiers["Bevel.001"].width = 0.003

		bpy.ops.object.modifier_add(type='SUBSURF')
		bpy.context.object.modifiers["Subdivision"].levels = 2

		bpy.context.object.name = "sword_blade"

		# Hand

		bpy.ops.mesh.primitive_plane_add(size=2, view_align=False, enter_editmode=False, location=(3.37511e-06, 2.77613e-08, 0.2723))

		bpy.ops.object.mode_set(mode = 'EDIT')

		bpy.ops.mesh.merge(type='CENTER')

		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.0585713, 8.68674e-009, -0.115059), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.0361917, 1.67184e-010, -0.00221449), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.0427634, -2.03823e-009, 0.0269972), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.0208174, -2.1996e-009, 0.0291346), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.0300255, 4.06311e-009, -0.0538175), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(-0.156343, 5.46802e-009, -0.0724261), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.00240966, 6.47707e-009, -0.0857914), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(-0.00847854, 8.12588e-009, -0.107631), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.00841911, 1.71005e-009, -0.0226504), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0.0215938, 1.0422e-009, -0.0138043), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(-0.00817733, 2.36718e-009, -0.0313544), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(-0.0235766, 1.98995e-009, -0.0263575), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(-0.0242162, 5.09147e-010, -0.00674379), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

		bpy.ops.mesh.select_all(action = 'SELECT')
		bpy.ops.mesh.edge_face_add()

		bpy.ops.object.mode_set(mode = 'OBJECT')

		bpy.ops.object.modifier_add(type='MIRROR')
		bpy.context.object.modifiers["Mirror"].use_bisect_axis[0] = True
		bpy.context.object.modifiers["Mirror"].use_clip = True

		bpy.ops.object.modifier_add(type='SOLIDIFY')
		bpy.context.object.modifiers["Solidify"].offset = 0
		bpy.context.object.modifiers["Solidify"].thickness = 0.05
		bpy.context.object.modifiers["Solidify"].show_on_cage = True


		bpy.ops.object.modifier_add(type='BEVEL')
		bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
		bpy.context.object.modifiers["Bevel"].use_clamp_overlap = False
		bpy.context.object.modifiers["Bevel"].width = 0.015


		return {'FINISHED'}