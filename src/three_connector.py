from this import d
import bpy

from .ws_server import WS;
from src.animation_parser import AnimationParser

class THREECONNECTOR_PT_Sync(bpy.types.Panel):

    bl_label = "Three Connector"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Three Connector"

    def draw(self, context):
        op_cls = THREECONNECTOR_OT_Sync
        
        layout = self.layout
        if not op_cls.is_running():
            layout.operator(op_cls.bl_idname, text="同期開始", icon="PLAY")
        else:
            layout.operator(op_cls.bl_idname, text="同期中", icon="PAUSE", depress=True)

class THREECONNECTOR_OT_Sync(bpy.types.Operator):

    bl_idname = "object.threeconnector_sync"
    bl_label = "Three.jsと同期"
    bl_description = "シーン・タイムラインをThree.jsと同期します"
    
    ws = WS()
    running = False

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
        cls.ws.broadcast("sync/frame", frame_data)

    @classmethod
    def on_save(cls, scene: bpy.types.Scene ):
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