import bpy
from bpy.types import (Operator)

from ..managers.fcurve import FCurveManager

class THREECONNECTOR_OT_FCurveAccessorRename(Operator):
    bl_idname = 'object.threeconnector_fcurve_asccessor_rename'
    bl_label="Rename accessor"
    bl_options = {'REGISTER', 'UNDO'}
    
    accessor_name: bpy.props.StringProperty(name="accessor name", default="" )
    
    def invoke(self, context = None, event = None ):
        self.accessor_name = ''
        return bpy.context.window_manager.invoke_props_dialog(self)
        
    def execute(self, context):
        for fcurve in bpy.context.selected_editable_fcurves:
            fcurve_id = FCurveManager.getFCurveId(fcurve, True)
            for curveData in bpy.context.scene.three_connector.fcurve_list:
                if( curveData.name == fcurve_id ):
                    curveData.accessor = self.accessor_name

        bpy.context.area.tag_redraw()
        
        return {'FINISHED'}