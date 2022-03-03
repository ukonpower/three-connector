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
    
    def on_change_frame(self, scene: bpy.types.Scene, any ):
        cls = THREECONNECTOR_OT_Sync

        frameData = {
            'start': scene.frame_start,
            'end': scene.frame_end,
            'current': scene.frame_current
        }
        
        cls.ws.broadcast(frameData)
    
    def on_save(self, scene: bpy.types.Scene ):
        parser = AnimationParser()
        parser.get_animation_date()

    def start(self):
        cls = THREECONNECTOR_OT_Sync
        cls.ws.start_server('localhost', 3100)
        cls.running = True
        
        bpy.app.handlers.frame_change_pre.append(self.on_change_frame)
        bpy.app.handlers.save_pre.append(cls.on_save)
            
    def stop(self):
        cls = THREECONNECTOR_OT_Sync
        cls.ws.stop_server()
        cls.running = False

    def execute(self, context: bpy.types.Context):
        cls = THREECONNECTOR_OT_Sync

        bpy.app.handlers.frame_change_pre.clear()
        bpy.app.handlers.save_pre.clear()
        
        if( cls.is_running() ):
            self.stop()
        else:
            self.start()

        return {'FINISHED'}