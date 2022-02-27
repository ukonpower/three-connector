if "bpy" in locals():
    import imp
    imp.reload(WS)
else:
    from .ws_server import WS;

import bpy

ws = WS()

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
            ws.stop_server()
            op_cls.__running = False
        else:
            ws.start_server('localhost', 3100)
            bpy.app.handlers.frame_change_pre.append(self.on_change_frame)
            op_cls.__running = True

        return {'FINISHED'}
