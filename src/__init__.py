bl_info = {
    "name" : "Three Connector",
    "author" : "ukonpower",
    "description" : "",
    "blender" : (2, 93, 8),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import bpy
from . import auto_load

auto_load.init()

class THREECONNECTOR_OT_SyncTimeLine(bpy.types.Operator):

    bl_idname = "object.threeconnector_timeline"
    bl_label = "タイムラインを同期"
    bl_description = "タイムラインをwebsocketで送信します。"
    
    __running = False

    @classmethod
    def is_running(cls):
        return cls.__running
    
    def on_change_frame(self, scene, any ):
        print("Frame Change", scene.frame_current)
        
    def invoke(self, context, event):
        op_cls = THREECONNECTOR_OT_SyncTimeLine

        bpy.app.handlers.frame_change_pre.clear()

        if( op_cls.is_running() ):
            op_cls.__running = False
        else:
            bpy.app.handlers.frame_change_pre.append(self.on_change_frame)
            op_cls.__running = True

        return {'FINISHED'}

# UI
class THREECONNECTOR_PT_SyncTimeLine(bpy.types.Panel):

    bl_label = "タイムラインを同期"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Three Connector"

    def draw(self, context):
        op_cls = THREECONNECTOR_OT_SyncTimeLine

        layout = self.layout
        # [開始] / [停止] ボタンを追加
        if not op_cls.is_running():
            layout.operator(op_cls.bl_idname, text="開始", icon="PLAY")
        else:
            layout.operator(op_cls.bl_idname, text="終了", icon="PAUSE")

auto_load.ordered_classes = [
    THREECONNECTOR_OT_SyncTimeLine,
    THREECONNECTOR_PT_SyncTimeLine,
]

def register():
    auto_load.register()

def unregister():
    auto_load.unregister()
