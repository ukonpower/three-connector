import os
import bpy

def get_gltf_presets(scene, context):
    items = []

    preset_path = bpy.utils.preset_paths('operator/export_scene.gltf/')[0]
    file_list = os.listdir(preset_path)
    
    for file in file_list:
        if file.find( '.py' ) > -1:
            items.append(( os.path.join(preset_path, file), file.replace('.py', ''), file))

    return items

class ThreeConnectorProperties(bpy.types.PropertyGroup):
    export_gltf_path: bpy.props.StringProperty(name="path", default="./")
    export_gltf_preset_list: bpy.props.EnumProperty(
        name="preset",
        description="gltf export preset",
        items=get_gltf_presets,
    )
    export_gltf_export_on_save: bpy.props.BoolProperty(name="export on save", default=False)
    export_json_path: bpy.props.StringProperty(name="path", default="./")
