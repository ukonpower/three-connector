import os
import bpy

from .managers.fcurve import ThreeConnectorFCurveData

def get_gltf_presets(scene, context):
    items = []

    preset_path_list = bpy.utils.preset_paths('operator/export_scene.gltf/')

    if(len(preset_path_list) <= 0):
        return []
    
    preset_path = preset_path_list[0]
    file_list = os.listdir(preset_path)
    
    for file in file_list:
        if file.find( '.py' ) > -1:
            items.append(( os.path.join(preset_path, file), file.replace('.py', ''), file))

    return items

class ThreeConnectorProperties(bpy.types.PropertyGroup):
    sync_port: bpy.props.IntProperty(name="port", default=3100)
    export_gltf_path: bpy.props.StringProperty(name="path", default="./")
    export_gltf_preset_list: bpy.props.EnumProperty(
        name="preset",
        description="gltf export preset",
        items=get_gltf_presets,
    )
    export_gltf_export_on_save: bpy.props.BoolProperty(name="export on save", default=False)
    export_json_path: bpy.props.StringProperty(name="path", default="./")
    fcurve_list: bpy.props.CollectionProperty(type=ThreeConnectorFCurveData, name="fcurve")

    def register():
        bpy.types.Scene.three_connector = bpy.props.PointerProperty(type=ThreeConnectorProperties)
        print( bpy.context)

    def unregister():
        bpy.context.scene.three_connector.fcurve_list.clear()
        del bpy.types.Scene.three_connector