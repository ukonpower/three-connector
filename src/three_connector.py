import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.types import (Operator)
from bpy.props import StringProperty

import os
from .ws_server import WS
from src.animation_parser import AnimationParser

class ThreeConnectorProperties(bpy.types.PropertyGroup):
    gltf_path: bpy.props.StringProperty(name="fle path", default="./")
    gltf_preset: bpy.props.StringProperty(name="preset", default="simple")

class THREECONNECTOR_PT_Sync(bpy.types.Panel):

    bl_label = "Three Connector"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Three Connector"

    def draw(self, context):
        scene = context.scene
        # sync
        syncCls = THREECONNECTOR_OT_Sync
        layout = self.layout
        if not syncCls.is_running():
            layout.operator(syncCls.bl_idname, text="同期開始", icon="PLAY")
        else:
            layout.operator(syncCls.bl_idname, text="同期中", icon="PAUSE", depress=True)
        layout.separator()

        # glb path
        gltfExportPathCls = THREECONNECTOR_OT_GLTFExportPath
        gltfExportCls = THREECONNECTOR_OT_GLTFExport
        
        layout.label(text="glTF Export")
        layout.prop( scene.three_connector, "gltf_preset" )
        gltfLayoutLow = layout.row(align=True)
        gltfLayoutLow.prop( scene.three_connector, "gltf_path" )
        gltfLayoutLow.operator( gltfExportPathCls.bl_idname, text="", icon="FILE_FOLDER" )
        layout.operator(gltfExportCls.bl_idname, text="Export" )

class THREECONNECTOR_OT_GLTFExportPath(Operator, ImportHelper):
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
        scene.three_connector.gltf_path = self.filepath
        return {'FINISHED'}

class THREECONNECTOR_OT_GLTFExport(Operator):
    bl_idname = 'object.threeconnector_export_gltf'
    bl_label = 'Accept'
    
    def execute(self, context):
        scene = bpy.context.scene
        filename = scene.three_connector.gltf_preset
        filepath = scene.three_connector.gltf_path

        # https://blenderartists.org/t/using-fbx-export-presets-when-exporting-from-a-script/1162914/2

        preset_path = bpy.utils.preset_paths('operator/export_scene.gltf/')[0]
        presetpath = os.path.join(preset_path, filename) 
        if presetpath:
            class Container(object):
                __slots__ = ('__dict__',)

            op = Container()
            file = open(presetpath + '.py', 'r')

            # storing the values from the preset on the class
            for line in file.readlines()[3::]:
                exec(line, globals(), locals())

            # set gltf path
            op.filepath = filepath
            
            # pass class dictionary to the operator
            kwargs = op.__dict__
            bpy.ops.export_scene.gltf(**kwargs)
        
        return {'FINISHED'}

class THREECONNECTOR_OT_Sync(bpy.types.Operator):

    bl_idname = "object.threeconnector_sync"
    bl_label = "Three.jsと同期"
    bl_description = "シーン・タイムラインをThree.jsと同期します"
    
    ws = WS()
    running = False

    # frame
    sended_frame = None

    @classmethod
    def is_running(cls):
        return cls.running
    
    @classmethod
    def register(cls):
        print('register')

    @classmethod
    def unregister(cls):
        print('unregister')
        cls.ws.stop_server()
        cls.running = False
        bpy.app.handlers.save_pre.clear()

    @classmethod
    def get_frame(cls):
        scene = bpy.context.scene
        return {
            'start': scene.frame_start,
            'end': scene.frame_end,
            'current': scene.frame_current
        }

    @classmethod
    def get_animation(cls):
        return AnimationParser().get_animation_date()

    @classmethod
    def on_change_frame(cls, scene: bpy.types.Scene, any ):
        frame_data = cls.get_frame()
        if frame_data["current"] != cls.sended_frame:
            cls.ws.broadcast("sync/frame", frame_data)
            cls.sended_frame = frame_data["current"]

    @classmethod
    def on_save(cls, scene: bpy.types.Scene, any ):
        animation_data = cls.get_animation()
        cls.ws.broadcast("sync/animation", animation_data)

    @classmethod
    async def on_connect(cls, websocket):
        frame_data = cls.get_frame()
        animation_data = cls.get_animation()
        await cls.ws.send(websocket, "sync/frame", frame_data)
        await cls.ws.send(websocket, "sync/animation", animation_data)
        
    def start(self):
        cls = THREECONNECTOR_OT_Sync
        cls.ws.start_server('localhost', 3100)
        cls.running = True
        
        bpy.app.handlers.frame_change_pre.append(cls.on_change_frame)
        bpy.app.handlers.save_pre.append(cls.on_save)
            
    def stop(self):
        cls = THREECONNECTOR_OT_Sync
        cls.ws.stop_server()
        cls.running = False

    def execute(self, context: bpy.types.Context):
        cls = THREECONNECTOR_OT_Sync
        bpy.app.handlers.frame_change_pre.clear()
        bpy.app.handlers.save_pre.clear()

        cls.ws.on_connect = cls.on_connect

        if( cls.is_running() ):
            self.stop()
        else:
            self.start()

        return {'FINISHED'}

def register():
    bpy.types.Scene.three_connector = bpy.props.PointerProperty(type=ThreeConnectorProperties)

def unregister():
    del bpy.types.Scene.three_connector