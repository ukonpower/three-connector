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

        fcurves = bpy.context.selected_editable_fcurves

        for fcurve in fcurves:
            fcurve.id_data
            layout.prop(fcurve, "accessor", text="name")
