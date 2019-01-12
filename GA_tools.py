import  bpy


class GA_Tools_Stylized(bpy.types.Operator):

	bl_idname = "scene.ga_toolsstylized"
	bl_label = "Stylized"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
        
 
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
		
class GA_Tools_Optimize(bpy.types.Operator):

	bl_idname = "scene.ga_tooloptimize"
	bl_label = "Optimize"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
        
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
        
		bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
		bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

		bpy.ops.object.modifier_add(type='MIRROR')
		bpy.context.object.modifiers["Mirror"].use_bisect_axis[0] = True
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")

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