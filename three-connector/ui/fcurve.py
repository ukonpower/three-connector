from cgitb import text
import time
import bpy

# properties

from ..properties import ThreeConnectorProperties

class THREECONNECTOR_PT_FCurve(bpy.types.Panel):

    bl_label = "Three Connector"
    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'
    bl_category = "F-Curve"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.label(text="Accessor")

        for curve in bpy.context.selected_editable_fcurves:
            for curveData in bpy.context.scene.three_connector.fcurve_list:
                if( curveData.name == curve.data_path ):
                    layout.prop(curveData, "value", text=curve.data_path)
