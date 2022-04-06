import bpy

# properties

from .properties import ThreeConnectorProperties

def register():
    bpy.types.Scene.three_connector = bpy.props.PointerProperty(type=ThreeConnectorProperties)

def unregister():
    del bpy.types.Scene.three_connector