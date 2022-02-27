if "bpy" in locals():
    import imp
    imp.reload(THREECONNECTOR_OT_SyncTimeLine)
else:
    from .sync_timeline_ot import THREECONNECTOR_OT_SyncTimeLine

import bpy

class THREECONNECTOR_PT_SyncTimeLine(bpy.types.Panel):

    bl_label = "タイムラインを同期"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Three Connector"

    def draw(self, context):
        op_cls = THREECONNECTOR_OT_SyncTimeLine
        
        layout = self.layout
        if not op_cls.is_running():
            layout.operator(op_cls.bl_idname, text="開始", icon="PLAY")
        else:
            layout.operator(op_cls.bl_idname, text="終了", icon="PAUSE")