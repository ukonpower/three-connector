import bpy
from bpy.types import (Operator)
from bpy.app.handlers import persistent

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

    @classmethod
    @persistent
    def on_save(cls = None, scene: bpy.types.Scene = None):
        scene = bpy.context.scene
        if scene.three_connector.export_gltf_export_on_save:
            cls.export()
