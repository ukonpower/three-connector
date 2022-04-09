import bpy

# fcurve updator

from ..managers.fcurve import FCurveManager

class THREECONNECTOR_PT_FCurve(bpy.types.Panel):

    bl_label = 'Three Connector'
    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'F-Curve'

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        for fcurve in bpy.context.selected_editable_fcurves:
            for curveData in bpy.context.scene.three_connector.fcurve_list:
                if( curveData.name == FCurveManager.getFCurveId(fcurve) ):
                    layout.label(text=curveData.name)
                    layout.prop(curveData, 'accessor', text='accessor')
                    layout.prop(curveData, 'axis', text='axis')
