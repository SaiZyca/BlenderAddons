
bl_info = {
    "name" : "Blender Render Elements",
    "author" : "Sai Ling",
    "description": "Blender Render Elements",
    "version": (0, 0, 1),
    "blender" : (2, 80, 0),
    "location": "Node Editor Toolbar or Shift-W",
    "warning" : "",
    "wiki_url": "https://hackmd.io/@Sai",
    "category" : "Generic"
}

import bpy
import importlib
from . import addon_classes

importlib.reload(addon_classes)


classes = (
    addon_classes.ELEMENT_PT_main,
    addon_classes.ELEMENT_PT_data,
    addon_classes.ELEMENT_PT_lights,
    addon_classes.ELEMENT_PT_cryptomatte,
    addon_classes.ELEMENT_PT_other,
    )
    

# Registration

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # bpy.types.Scene.BlenderRenderElement_setting = bpy.props.PointerProperty(type=addon_classes.BlenderPassManager_properties)
    print ("Blender Render Elements coming")

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    # del bpy.types.Scene.BlenderRenderElement_setting
    
    print ("Blender Render Elements leaving")