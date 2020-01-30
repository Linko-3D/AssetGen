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

import bpy

bl_info = {
    "name" : "AssetGen",
    "author" : "Srdan Ignjatovic aka zero025 (kica025@gmail.com) and Bekhoucha Danyl aka Linko (dbekhouc@gmail.com)",
    "version": (1, 0, 0),
    "blender" : (2, 80, 0),
    "location" : "View3D",
    "description" : "AssetGen is a free add-on (GPL License) that automates the tasks to get game assets ready for video games from an High Poly model.",
    "warning" : "",
    "wiki_url": "https://github.com/Linko-3D/AssetGen",
    "tracker_url": "https://github.com/Linko-3D/AssetGen/issues",
    "category" : "Game Tool"
}


from . import GA_user_interface
from . import GA_tools
from . import GA


class GA_Props(bpy.types.PropertyGroup):

   ga_file : bpy.props.EnumProperty(
        items=[('obj', 'obj', 'obj file format'),
		('glb', 'glb', 'glb file format'),
               ('glTF', 'glTF', 'glTF file format'),],
        description="Choose the file format between obj, glb (binary packed - recommended) or glTF (unpacked)",
        default='glb'
   )

   ga_unreal : bpy.props.BoolProperty(
        name = 'To Unreal Engine',
        description = "Will fix the scale and orientation to export to Unreal Engine 4",
        default = False
   )

   ga_path : bpy.props.StringProperty(
        name="Path", 
        description = "Indicate the path to your game asset folder",
        default='//',
        subtype = 'DIR_PATH'
   )   

   ga_baketextures : bpy.props.BoolProperty(
        name = 'Bake Textures',
        description = "Will bake your textures, if disabled it will set your low poly to flat shading and disable Unfold Half. Disabling it is ideal to send low poly models with flat base colors. You can also use this to generate your low poly, edit the UVs then use Selected to Active.",
        default = True
   )

   ga_textureX : bpy.props.EnumProperty(
        items=[('256', '256', '256 px resolution'),
               ('512', '512', '512 px resolution'),
               ('1K', '1K', '1K px resolution'),
               ('2K', '2K', '2K px resolution'),
               ('4K', '4K', '4K px resolution')],
        description="Choose the texture resolution in X (width)",
        default='512'
   )
   
   ga_textureY : bpy.props.EnumProperty(
        items=[('256', '256', '256 px resolution'),
               ('512', '512', '512 px resolution'),
               ('1K', '1K', '1K px resolution'),
               ('2K', '2K', '2K px resolution'),
               ('4K', '4K', '4K px resolution')],
        description="Choose the texture resolution in Y (height)",
        default='512'
   )
   
   ga_samplecount : bpy.props.IntProperty(
        name="Sample Count",
		description = "Increasing this value will reduce the noise on your texture for the Ambient Occlusion and SSS, but it will increase the baking time",
        default=16,
        min = 1		
   )  

   ga_remesh : bpy.props.BoolProperty(
        name = 'Remesh',
        description = "Will perform a remesh to merge every meshes and remove every intersections",
        default = True
   )

   ga_voxelsize : bpy.props.FloatProperty(
        name = 'Voxel Size',
        description = "The amount of temporary extrusion used on your low poly during the baking. A value too low will reveal intersections, a value too high can create new intersections between concave shapes and generate wavy edges. After generating your low poly if the result isn't correct, use the Solidify modifier on the low poly, change the offset to 1 and tweak the thickness by holding shift until it envelops the high poly to find the right value, then generate your asset again",
        default = 0.01,
        min = 0.001,
        max = 10
   )       
   
   ga_ao : bpy.props.BoolProperty(
        name = 'Bake AO',
        description = "Will bake the AO map separately ideal for PBR materials. Do not include an AO node in your base color shader",
        default = False
   )

   ga_unfoldhalf : bpy.props.BoolProperty(
        name = 'Unfold Half by Symmetry',
        description = "Will generate an UV Map for the half right of the low poly to double the quality of the texture",
        default = False
   )
   
   ga_selectedtoactive : bpy.props.BoolProperty(
        name = 'Selected to Active',
        description = "Will use your own low poly and UV Map, the active selection must be your low poly",
        default = False
   )   
   

   ga_calculateLods : bpy.props.BoolProperty(
        name = 'Calculate LODs',
        description = "Your LODs will automatically be calculated relative to the LOD0 like this: LOD1: 50%; LOD2: 25%, LOD3: 12.5%",
        default = True
   )
   
   ga_LOD0 : bpy.props.IntProperty(name="LOD0 (tris)", default=1000,min=1)     
   ga_LOD1 : bpy.props.IntProperty(name="LOD1 (tris)", default=0,min=0)    
   ga_LOD2 : bpy.props.IntProperty(name="LOD2 (tris)", default=0,min=0)    
   ga_LOD3 : bpy.props.IntProperty(name="LOD3 (tris)", default=0,min=0)       

   ga_imposter : bpy.props.BoolProperty(
        name = 'Imposter Cards',
        description = "Displays your high poly on multiple planes. Enable Backface Culling in the viewport to display it.",
        default = False
   )   
   
   ga_showoutput : bpy.props.BoolProperty(
        name = 'Show output in Blender',
        description = "Display your output in Blender",
        default = True
   )   

   ga_smoothHP : bpy.props.BoolProperty(
        name = 'Smooth High Poly',
        description = "Will apply a smooth shading on your high poly",
        default = True
   )

   ga_smoothLP : bpy.props.BoolProperty(
        name = 'Smooth Low Poly',
        description = "Will apply a smooth shading on your low poly",
        default = True
   )
   
   ga_bakelighting : bpy.props.BoolProperty(
        name = 'Bake Lighting/Shading',
        description = "The lighting and shading information will be baked, this is useful if you have emissive materials",
        default = False
   )    

   ga_cagesize : bpy.props.FloatProperty(
        name = 'Cage Size',
        description = "The amount of temporary extrusion used on your low poly during the baking. A value too low will reveal intersections, a value too high can create new intersections between concave shapes and generate wavy edges. After generating your low poly if the result isn't correct, use the Solidify modifier on the low poly, change the offset to 1 and tweak the thickness by holding shift until it envelops the high poly to find the right value, then generate your asset again",
        default = 0.03,
        min = 0,
        max = 1		
   )       
   
   ga_edgepadding : bpy.props.IntProperty(
        name = 'Edge Padding',
        description = "The amount of pixels that goes beyond the UV seam. A value too low can reveal the seam, a value too high takes more time to calculate",
        default = 8,
        min = 0,
        max = 64
   )   

   ga_uvmargin : bpy.props.FloatProperty(
        name = 'UV Margin',
        description = "The space between each UV islands. A value too low won't allow to have enough edge padding for the texture beyond the seams",
        default = 0.01,
        min = 0,
        max = 64		
   )  

   ga_uvangle : bpy.props.IntProperty(
        name = 'UV Angle',
        description = "The step angle where your UV Map must create an UV Seam. If the value is too low the UV Map will contain many individual faces, the game engine will need more calculations to display your textures. A value too high could create overlapping and not optimize the texel density (space available) resulting in a low texture quality",
        default = 66,
        min = 1,
        max = 89		
   )

   ga_centerXY : bpy.props.BoolProperty(
        name = 'Center XY',
        description = "Center your game asset in the X and Y axis before exporting it, this makes it easier to manipulate it in the game engine (you can also have a collection of high polys in the Blender scene in different positions)",
        default = False
   )    

   ga_ontheground : bpy.props.BoolProperty(
        name = 'On the Ground',
        description = "Move your asset on the ground",
        default = False
   )
   
   ga_removeinside : bpy.props.BoolProperty(
        name = 'Remove Inside',
        description = "The addon will perform an Union boolean between every meshes that aren't merged (connected vertices), this will remove the geometry inside your model before calculating the polycount and performing an UV Mapping",
        default = False
   )    

   ga_groundao : bpy.props.BoolProperty(
        name = 'Ground AO',
        description = "Before the baking, the addon will generate a plane at the height of the grid to generate Ambient Occlusion like if the object were standing on the ground. Use it with every static meshes that lays on the ground",
        default = False
   )    
   
   ga_removeunderground : bpy.props.BoolProperty(
        name = 'Remove Underground',
        description = "Everything bellow the grid will be removed, this will save triangles that won't be visible bellow your model",
        default = False
   )   

classes = [
    GA_Props,
    GA_user_interface.GA_PT_generatePanel,
    GA_user_interface.GA_PT_advancedPanel,
    GA_user_interface.GA_PT_toolsPanel,
    GA.GA_Start,
    GA_tools.GA_PT_Tools_HighPoly,
    GA_tools.GA_PT_Tools_Wear,

	GA_tools.GA_PT_Tools_Apply,
    GA_tools.GA_PT_Tools_ResymX,
    GA_tools.GA_PT_Tools_CutHalf,
	GA_tools.GA_PT_Tools_FixNormals,
	GA_tools.GA_PT_Tools_FlipNormals,
	GA_tools.GA_PT_Tools_Union,
	GA_tools.GA_PT_Tools_Dyntopo,
	GA_tools.GA_PT_Tools_Subsurf,
    GA_tools.GA_PT_Tools_Optimize,
    GA_tools.GA_PT_Tools_DissolveUnnecessary,
    GA_tools.GA_PT_Tools_Polycount,
	GA_tools.GA_PT_Tools_OnTheGround,
    GA_tools.GA_PT_Tools_UnrealTransforms,

	GA_tools.GA_PT_Tools_BaseMesh,
	GA_tools.GA_PT_Tools_BoltCubic,
	GA_tools.GA_PT_Tools_BoltCylinder,
	GA_tools.GA_PT_Tools_ChainHexagon,
	GA_tools.GA_PT_Tools_ChainSquare,
	GA_tools.GA_PT_Tools_Crack,
	GA_tools.GA_PT_Tools_ExtrudedCurve,
	GA_tools.GA_PT_Tools_ExtrudedMesh,
	GA_tools.GA_PT_Tools_Hair,
	GA_tools.GA_PT_Tools_RingCircle,
	GA_tools.GA_PT_Tools_RingSquare,
	GA_tools.GA_PT_Tools_Rope,
	GA_tools.GA_PT_Tools_StrapCircle,
	GA_tools.GA_PT_Tools_StrapHandle,
	GA_tools.GA_PT_Tools_StrapLine,

    GA_tools.GA_PT_Tools_Axe,
	GA_tools.GA_PT_Tools_Shield,
	GA_tools.GA_PT_Tools_Shoulder,
    GA_tools.GA_PT_Tools_Sword,
	
    GA_tools.GA_PT_Tools_Potion,
]


def register():
    print("register")
    for c in classes:
        bpy.utils.register_class(c)
		
    bpy.types.Scene.ga_property = bpy.props.PointerProperty(type=GA_Props)
 

def unregister():
    print("unregister")
	
    del bpy.types.Scene.ga_property

    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
