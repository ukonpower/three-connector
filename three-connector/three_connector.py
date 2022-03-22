import bpy

# properties

from .properties import ThreeConnectorProperties

# sync

from .operators.sync import (THREECONNECTOR_OT_Sync)

# exports

from .operators.export_gltf import (THREECONNECTOR_OT_ExportGLTF, THREECONNECTOR_OT_ExportGLTFPath)
from .operators.export_json import (THREECONNECTOR_OT_ExportJson, THREECONNECTOR_OT_ExportJsonPath)

class THREECONNECTOR_PT_Controls(bpy.types.Panel):

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
            layout.operator(syncCls.bl_idname, text="Sync", icon="PLAY")
        else:
            layout.operator(syncCls.bl_idname, text="Syncing...", icon="PAUSE", depress=True)
        layout.separator()

        # gltf
        exportGltfPathCls = THREECONNECTOR_OT_ExportGLTFPath
        exportGltfCls = THREECONNECTOR_OT_ExportGLTF
        
        layout.label(text="glTF")
        layout.prop(scene.three_connector,"export_gltf_export_on_save", text="export on save")
        layout.prop(scene.three_connector,"export_gltf_preset_list", text="preset")

        gltfLayoutLow = layout.row(align=True)
        gltfLayoutLow.prop( scene.three_connector, "export_gltf_path" )
        gltfLayoutLow.operator( exportGltfPathCls.bl_idname, text="", icon="FILE_FOLDER" )
        layout.operator(exportGltfCls.bl_idname, text="Export glTF (glb)" )

        # json
        
        exportJsonPathCls = THREECONNECTOR_OT_ExportJsonPath
        exportJsonCls = THREECONNECTOR_OT_ExportJson
        
        layout.label(text="JSON")
        gltfLayoutLow = layout.row(align=True)
        gltfLayoutLow.prop( scene.three_connector, "export_json_path" )
        gltfLayoutLow.operator( exportJsonPathCls.bl_idname, text="", icon="FILE_FOLDER" )
        layout.operator(exportJsonCls.bl_idname, text="Export json" )

def register():
    bpy.types.Scene.three_connector = bpy.props.PointerProperty(type=ThreeConnectorProperties)

def unregister():
    del bpy.types.Scene.three_connector