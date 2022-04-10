import bpy
import json

from bpy.types import (Operator)

from ..utils.scene_parser import SceneParser

class THREECONNECTOR_OT_ExportSceneData(Operator):
    bl_idname = 'object.threeconnector_export_scene'
    bl_label = 'Accept'
    
    def execute(self, context):
        scene = bpy.context.scene
        data = SceneParser().get_animation_date()
        path = scene.three_connector.export_scene_data_path

        with open( path, mode='wt', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)
            
        return {'FINISHED'}

