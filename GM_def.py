# Import
import bpy
import os,colorsys,mathutils
from bpy.props import *
from bpy.types import Panel, Operator, Menu,PropertyGroup
from bpy.utils import previews
from bpy.types import WindowManager


GM_preview_collections = {}



# Functions ###############################################################################


def GM_generate_previews(metals):

    previews = GM_preview_collections["tmp_material_all"]
    image_location = previews.images_location
    GM_enum_items = []

    #path DB
    filepathdb = os.path.join(os.path.dirname(__file__), 
               "materials" + os.sep ) + "material.ga"

    gaDB = open(filepathdb, "r")
    lines = gaDB.readlines()


    for i, line in enumerate(lines):
        q_name = line[0:4]

        if q_name == "NAME":
           q_name = line[5:-1]
       
           filepathIMG = os.path.join(image_location, q_name )
           thumb = previews.load(filepathIMG, filepathIMG, 'IMAGE')
  
        
           GM_enum_items.append((q_name, q_name , "", thumb.icon_id, i ))


    GM_enum_items.sort()


    return GM_enum_items



def GM_append_material(self, context):

    q_mat_select = context.scene.gmselect

    
    node_name = context.scene.dandy_materials_mats_metals

    filepath = os.path.join(os.path.dirname(__file__), 
               "materials" + os.sep ) + "material.ga"

    gpl = open(filepath, "r")
    lines = gpl.readlines()

    prolaz = 0
    pozicija = 0

    for i, line in enumerate(lines):
        

        if prolaz == 1:
           
           if pozicija == 0:
  
              # position
              if line[:11] == "   position":  
                 q_mat_select.use_point1 = float(line[12:-1])

              # colorR
              if line[:9] == "   colorR":
                 q_mat_select.use_color1[0] = float(line[10:-1])

              # colorG
              if line[:9] == "   colorG":
                 q_mat_select.use_color1[1] = float(line[10:-1])

              # colorB
              if line[:9] == "   colorB":
                 q_mat_select.use_color1[2] = float(line[10:-1])

              # colorA
              if line[:9] == "   colorA":
                 #q_mat_select.use_color1[3] = float(line[10:-1])
                 pozicija = pozicija + 1 

           elif pozicija == 1:
              # position
              if line[:11] == "   position":  
                 q_mat_select.use_point2 = float(line[12:-1])

              # colorR
              if line[:9] == "   colorR":
                 q_mat_select.use_color2[0] = float(line[10:-1])

              # colorG
              if line[:9] == "   colorG":
                 q_mat_select.use_color2[1] = float(line[10:-1])

              # colorB
              if line[:9] == "   colorB":
                 q_mat_select.use_color2[2] = float(line[10:-1])

              # colorA
              if line[:9] == "   colorA":
                 #q_mat_select.use_color2[3] = float(line[10:-1])
                 pozicija = pozicija + 1 

           elif pozicija == 2:
              # position
              if line[:11] == "   position":  
                 q_mat_select.use_point3 = float(line[12:-1])

              # colorR
              if line[:9] == "   colorR":
                 q_mat_select.use_color3[0] = float(line[10:-1])

              # colorG
              if line[:9] == "   colorG":
                 q_mat_select.use_color3[1] = float(line[10:-1])

              # colorB
              if line[:9] == "   colorB":
                 q_mat_select.use_color3[2] = float(line[10:-1])

              # colorA
              if line[:9] == "   colorA":
                 #q_mat_select.use_color3[3] = float(line[10:-1])
                 pozicija = pozicija + 1 

           elif pozicija == 3:
              # position
              if line[:11] == "   position":  
                 q_mat_select.use_point4 = float(line[12:-1])

              # colorR
              if line[:9] == "   colorR":
                 q_mat_select.use_color4[0] = float(line[10:-1])

              # colorG
              if line[:9] == "   colorG":
                 q_mat_select.use_color4[1] = float(line[10:-1])

              # colorB
              if line[:9] == "   colorB":
                 q_mat_select.use_color4[2] = float(line[10:-1])

              # colorA
              if line[:9] == "   colorA":
                 #q_mat_select.use_color4[3] = float(line[10:-1])
                 pozicija = pozicija + 1 

           elif pozicija == 4:
              # position
              if line[:11] == "   position":  
                 q_mat_select.use_point5 = float(line[12:-1])

              # colorR
              if line[:9] == "   colorR":
                 q_mat_select.use_color5[0] = float(line[10:-1])

              # colorG
              if line[:9] == "   colorG":
                 q_mat_select.use_color5[1] = float(line[10:-1])

              # colorB
              if line[:9] == "   colorB":
                 q_mat_select.use_color5[2] = float(line[10:-1])

              # colorA
              if line[:9] == "   colorA":
                 #q_mat_select.use_color5[3] = float(line[10:-1])
                 pozicija = pozicija + 1 




        if line[0:4] == "NAME":
           # ako postoji
           if line[:-1] == "NAME="+node_name:
               prolaz = 1
           else:
               prolaz = 0

    gpl.close()




##################################################


def GM_change_lib(self, context):

    q_mat_select = context.scene.gmselect
    
    if self.D_gradientcolor == 'Custom gradient':
       q_mat_select.use_point1 = 0 
       q_mat_select.use_point5 = 1
       q_mat_select.use_color1 = [0,0,1]
       q_mat_select.use_color5 = [1,1,0.214]
       q_mat_select.use_gra_select = "Cold color"
    else:
       GM_append_material(self, context)


def GM_change_engine(self, context):

    
    if self.D_renderengine == 'Blender Render':
        bpy.context.scene.render.engine = 'BLENDER_RENDER'
        bpy.context.object.active_material.use_nodes = False
    else:
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.object.active_material.use_nodes = True





def GM_color_select(self, context):

    if self.use_gra_select == "Cold color":
       self.use_colorselect = self.use_color1
    else:
       self.use_colorselect = self.use_color5


def GM_selectcolor_update(self, context):

    self.use_point1 = 0 
    self.use_point2 = 0
    self.use_point3 = 0 
    self.use_point4 = 0 
    self.use_point5 = 1

    if self.use_gra_select == "Cold color":
       self.use_color1 = self.use_colorselect
    else:
       self.use_color5 = self.use_colorselect



# Class #############################################################################

class gm_Select(PropertyGroup):

    use_gra_select = bpy.props.EnumProperty(
        items=[('Cold color', 'Cold color', 'Cold color'),
               ('Warm color', 'Warm color', 'Warm color')],
        description="Choose color",
        update=GM_color_select,
        default='Cold color'
    )




    use_colorselect = FloatVectorProperty(
        name="Select color",
        subtype="COLOR",
        default=(1,1,1),
        min=0, 
        max=1,
        update=GM_selectcolor_update
    )


    name = StringProperty(name="Layer Name",
        default="Default")  

    use_point1 = bpy.props.FloatProperty(
        name = 'Point1',
        default = 0,
        min = 0,
        max = 1
    )
    use_color1 = FloatVectorProperty(
        name="Color1",
        subtype="COLOR",
        default=(1,1,1),
        min=0, 
        max=1
    )
    use_point2 = bpy.props.FloatProperty(
        name = 'Point2',
        default = 0,
        min = 0,
        max = 1
    )
    use_color2 = FloatVectorProperty(
        name="Color2",
        subtype="COLOR",
        default=(1,1,1),
        min=0, 
        max=1
    )
    use_point3 = bpy.props.FloatProperty(
        name = 'Point3',
        default = 0,
        min = 0,
        max = 1
    )
    use_color3 = FloatVectorProperty(
        name="Color3",
        subtype="COLOR",
        default=(1.00,1.00,1.00),
        precision = 3,
        min=0.00, 
        max=1.00
    )
    use_point4 = bpy.props.FloatProperty(
        name = 'Point4',
        default = 0,
        min = 0,
        max = 1
    )
    use_color4 = FloatVectorProperty(
        name="Color4",
        subtype="COLOR",
        default=(1,1,1),
        min=0, 
        max=1
    )
    use_point5 = bpy.props.FloatProperty(
        name = 'Point5',
        default = 0,
        min = 0,
        max = 1
    )
    use_color5 = FloatVectorProperty(
        name="Color5",
        subtype="COLOR",
        default=(1,1,1),
        min=0, 
        max=1
    )
  


class gmMateriali(PropertyGroup):


    name = StringProperty(name="Layer Name",
        default="Default")    

    use_select = BoolProperty(name="Material Select", 
        default=False)

    use_mask = FloatVectorProperty(
        name="Mask",
        description="Mask", 
        subtype="COLOR",
        default=(1,1,1),
        min=0, 
        max=1
    )
    use_mask_enable = bpy.props.BoolProperty(
        name = '',
        default = False
    )

    use_point1 = bpy.props.FloatProperty(
        name = 'Point1',
        default = 0,
        min = 0,
        max = 1
    )
    use_color1 = FloatVectorProperty(
        name="Color1",
        subtype="COLOR",
        default=(1,1,1),
        min=0, 
        max=1
    )
    use_point2 = bpy.props.FloatProperty(
        name = 'Point2',
        default = 0,
        min = 0,
        max = 1
    )
    use_color2 = FloatVectorProperty(
        name="Color2",
        subtype="COLOR",
        default=(1,1,1),
        min=0, 
        max=1
    )
    use_point3 = bpy.props.FloatProperty(
        name = 'Point3',
        default = 0,
        min = 0,
        max = 1
    )
    use_color3 = FloatVectorProperty(
        name="Color3",
        subtype="COLOR",
        default=(1.00,1.00,1.00),
        precision = 3,
        min=0.00, 
        max=1.00
    )
    use_point4 = bpy.props.FloatProperty(
        name = 'Point4',
        default = 0,
        min = 0,
        max = 1
    )
    use_color4 = FloatVectorProperty(
        name="Color4",
        subtype="COLOR",
        default=(1,1,1),
        min=0, 
        max=1
    )
    use_point5 = bpy.props.FloatProperty(
        name = 'Point5',
        default = 0,
        min = 0,
        max = 1
    )
    use_color5 = FloatVectorProperty(
        name="Color5",
        subtype="COLOR",
        default=(1,1,1),
        min=0, 
        max=1
    )







    use_advanced_enable = bpy.props.BoolProperty(
        name = '',
        default = False
    )


    use_advanced_layer_Bump_enable = bpy.props.BoolProperty(
        name = '',
        default = False
    )

    use_advanced_layer_Bump = bpy.props.FloatProperty(
        name = 'Val',
        description = "",
        default = 0.500,
        min = 0.000,
        max = 1.000
    )

    use_advanced_layer_Curvature_enable = bpy.props.BoolProperty(
        name = '',
        default = False
    )

    use_advanced_layer_Curvature = bpy.props.FloatProperty(
        name = 'Val',
        description = "",
        default = 0.500,
        min = 0.000,
        max = 1.000
    )







# Register #############################################################################

# Register
def register():

    GM_previews_mat_metals = bpy.utils.previews.new()
    GM_previews_mat_metals.images_location = os.path.join(os.path.dirname(__file__), "materials" + os.sep + 'm')


    GM_preview_collections['tmp_material_all'] = GM_previews_mat_metals
    
    bpy.types.Scene.dandy_materials_mats_metals = bpy.props.EnumProperty(
        items=GM_generate_previews(True),
        description="Select the material you want to use",
        update=GM_append_material,
        default='Base sRGB'
    )

    bpy.types.Scene.gmmateriali = CollectionProperty(type=gmMateriali)
    bpy.types.Scene.gmselect = PointerProperty(type=gm_Select)


    bpy.types.Scene.D_renderengine = bpy.props.EnumProperty(
        items=[('Blender Render', 'Blender Render', 'Blender render'),
               ('Cycles Render', 'Cycles Render', 'Cycles Render')],
        description="Choose render engine",
        update=GM_change_engine,
        default='Blender Render'
    )

    bpy.types.Scene.D_gradientcolor = bpy.props.EnumProperty(
        items=[('Presets', 'Presets', 'Presets'),
               ('Custom gradient', 'Custom gradient', 'Custom gradient')],
        description="Choose color",
        update=GM_change_lib,
        default='Presets'
    )

    bpy.types.Scene.D_curv = bpy.props.FloatProperty(
        name = 'Curvature',
        default = 1,
        min = 0,
        max = 1
    )
    bpy.types.Scene.D_ao = bpy.props.FloatProperty(
        name = 'AO',
        default = 0,
        min = 0,
        max = 1
    )
    bpy.types.Scene.D_shad = bpy.props.FloatProperty(
        name = 'Shadows',
        default = 0,
        min = 0,
        max = 1
    )

    bpy.types.Scene.D_effectdust = bpy.props.FloatProperty(
        name = 'Dust',
        default = 0,
        min = 0,
        max = 1
    )
    bpy.types.Scene.D_effectcolordust = FloatVectorProperty(
        name="Dust color",
        subtype="COLOR",
        default=(0.392,0.332,0.262,1),
        min=0, 
        max=1,
        size = 4
    )

    bpy.types.Scene.D_effectgrunge = bpy.props.FloatProperty(
        name = 'Grunge',
        default = 0,
        min = 0,
        max = 1
    )
    bpy.types.Scene.D_effectcolorgrunge = FloatVectorProperty(
        name="Grunge color",
        subtype="COLOR",
        default=(0.107,0.084,0.080,1),
        min=0, 
        max=1,
        size=4
    )


    bpy.types.Scene.D_effectsnow = bpy.props.FloatProperty(
        name = 'Snow',
        default = 0,
        min = 0,
        max = 1
    )
    bpy.types.Scene.D_effectcolorsnow = FloatVectorProperty(
        name="Snow color",
        subtype="COLOR",
        default=(0.839,0.831,0.880,1),
        min=0, 
        max=1,
        size = 4
    )




# Unregister
def unregister():
    for preview in GM_preview_collections.values():
        bpy.utils.previews.remove(preview)
    GM_preview_collections.clear()

    del bpy.types.Scene.dandy_materials_mats_metals
    del bpy.types.Scene.gmmateriali 
    del bpy.types.Scene.gmselect 

    del bpy.types.Scene.D_renderengine 
    del bpy.types.Scene.D_gradientcolor 













