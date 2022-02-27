if "bpy" in locals():
    import imp
    imp.reload(WS)
else:
    from .ws_server import WS;

import bpy

class THREECONNECTOR_OT_SyncTimeLine(bpy.types.Operator):

    bl_idname = "object.threeconnector_timeline"
    bl_label = "タイムラインを同期"
    bl_description = "タイムラインをwebsocketで送信します。"
    
    running = False
    ws = WS()

    @classmethod
    def is_running(cls):
        return cls.running
    
    def on_change_frame(self, scene, any ):
        cls = THREECONNECTOR_OT_SyncTimeLine
        cls.ws.broadcast(str(scene.frame_current))
        
    def invoke(self, context, event):
        cls = THREECONNECTOR_OT_SyncTimeLine
        
        bpy.app.handlers.frame_change_pre.clear()
        
        if( cls.is_running() ):
            cls.ws.stop_server()
            cls.running = False
        else:
            cls.ws.start_server('localhost', 3100)
            bpy.app.handlers.frame_change_pre.append(self.on_change_frame)
            cls.running = True

        return {'FINISHED'}

    def unregister():
        cls = THREECONNECTOR_OT_SyncTimeLine
        cls.ws.stop_server()
        cls.running = False