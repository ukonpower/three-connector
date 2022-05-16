import bpy
import json

from bpy_extras.io_utils import ExportHelper
from bpy.types import (Operator)
from bpy.props import (StringProperty, BoolProperty)

from ..utils.scene_parser import SceneParser

class THREECONNECTOR_OT_ExportSceneDataPath(Operator, ExportHelper):
    bl_idname = 'object.threeconnector_export_scene_path'
    bl_label = 'Accept'
    bl_options = {'UNDO'}
 
    filename_ext = '.json'

    filter_glob: StringProperty(
        default='*.json',
        options={'HIDDEN'}
    )

    path_relative: BoolProperty(
        name='Relative Path',
        description='',
        default=True
    )
 
    def execute(self, context):
        scene = bpy.context.scene
        path = self.filepath

        if( self.path_relative ):
            path = bpy.path.relpath(path)

        scene.three_connector.export_scene_data_path = path
        
        return {'FINISHED'}

class THREECONNECTOR_OT_ExportSceneData(Operator):
    bl_idname = 'object.threeconnector_export_scene'
    bl_label = 'Accept'
    
    def execute(self, context):
        scene = bpy.context.scene
        data = SceneParser().get_animation_date()
        path = bpy.path.abspath(scene.three_connector.export_scene_data_path)

        with open( path, mode='wt', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)
            
        return {'FINISHED'}

