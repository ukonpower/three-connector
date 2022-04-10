from cgitb import text
import bpy

from ..managers.fcurve import FCurveManager
from ..operators.fcurve_accessor import THREECONNECTOR_OT_FCurveAccessorRename

class THREECONNECTOR_PT_FCurve(bpy.types.Panel):

    bl_label = 'Three Connector'
    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'F-Curve'

    def draw(self, context):
        layout = self.layout

        for fcurve in bpy.context.selected_editable_fcurves:
            fcurve_id = FCurveManager.getFCurveId(fcurve, True)
            for curveData in bpy.context.scene.three_connector.fcurve_list:
                if( curveData.name == fcurve_id ):
                    layout.label(text=curveData.name)
                    layout.prop(curveData, 'accessor', text='accessor')
                    layout.prop(curveData, 'axis', text='axis')

        layout.operator( THREECONNECTOR_OT_FCurveAccessorRename.bl_idname, text='Rename accessors' )
