import bpy

# sync

from ..operators.sync import (THREECONNECTOR_OT_Sync)

# exports

from ..operators.export_gltf import (THREECONNECTOR_OT_ExportGLTF)
from ..operators.export_scene_data import (THREECONNECTOR_OT_ExportSceneData)

class THREECONNECTOR_PT_MainControls(bpy.types.Panel):

    bl_label = 'Three Connector'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Three Connector'

    def draw(self, context):
        scene = context.scene
        # sync
        syncCls = THREECONNECTOR_OT_Sync
        layout = self.layout
        layout.label(text='Sync')
        col = layout.column()
        col.prop(scene.three_connector,'sync_port', text='port')
        if syncCls.is_running():
            col.enabled = False
            layout.operator(syncCls.bl_idname, text='Syncing...', icon='PAUSE', depress=True)
        else:
            col.enabled = True
            layout.operator(syncCls.bl_idname, text='Sync', icon='PLAY')
        layout.separator()

        # gltf
        layout.label(text='glTF')
        layout.prop(scene.three_connector,'export_gltf_export_on_save', text='export on save')
        layout.prop(scene.three_connector,'export_gltf_preset_list', text='preset')

        layout.prop( scene.three_connector, 'export_gltf_path' )
        layout.operator(THREECONNECTOR_OT_ExportGLTF.bl_idname, text='Export glTF (glb)' )

        # sceneData
        layout.label(text='Scene data')
        layout.prop( scene.three_connector, 'export_scene_data_path' )
        layout.operator(THREECONNECTOR_OT_ExportSceneData.bl_idname, text='Export scene data' )