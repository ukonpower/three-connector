import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.types import (Operator)
from bpy.props import StringProperty

import os

class THREECONNECTOR_OT_ExportGLTFPath(Operator, ImportHelper):
    bl_idname = 'object.threeconnector_export_glb_path'
    bl_label = 'Accept'
    bl_options = {'PRESET', 'UNDO'}
 
    filename_ext = '.glb'

    filter_glob: StringProperty(
        default='*.glb',
        options={'HIDDEN'}
    )
 
    def execute(self, context):
        scene = bpy.context.scene
        scene.three_connector.export_gltf_path = self.filepath
        return {'FINISHED'}

class THREECONNECTOR_OT_ExportGLTF(Operator):
    bl_idname = 'object.threeconnector_export_gltf'
    bl_label = 'Accept'
    
    @classmethod
    def export(self):
        scene = bpy.context.scene
        preset_name = scene.three_connector.export_gltf_preset_list

        # https://blenderartists.org/t/using-fbx-export-presets-when-exporting-from-a-script/1162914/2

        if preset_name:
            class Container(object):
                __slots__ = ('__dict__',)

            op = Container()
            file = open(preset_name, 'r')

            # storing the values from the preset on the class
            for line in file.readlines()[3::]:
                exec(line, globals(), locals())

            # set gltf path
            op.filepath = scene.three_connector.export_gltf_path
            
            # pass class dictionary to the operator
            kwargs = op.__dict__
            bpy.ops.export_scene.gltf(**kwargs)
    
    def execute(self, context):
        self.export()
        return {'FINISHED'}

    def on_save(cls, scene: bpy.types.Scene):
        cls = THREECONNECTOR_OT_ExportGLTF
        scene = bpy.context.scene
        if scene.three_connector.export_gltf_export_on_save:
            cls.export()

    def register():
        cls = THREECONNECTOR_OT_ExportGLTF
        bpy.app.handlers.save_post.append(cls.on_save)

    def unregister():
        cls = THREECONNECTOR_OT_ExportGLTF

        try:
            bpy.app.handlers.save_post.remove(cls.on_save)
        except ValueError:
            pass

