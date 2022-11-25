from cgitb import text
import bpy

from ..managers.fcurve import FCurveManager
from ..operators.fcurve_accessor import THREECONNECTOR_OT_FCurveAccessorCreate, THREECONNECTOR_OT_FCurveAccessorRename

class THREECONNECTOR_PT_FCurve(bpy.types.Panel):

    bl_label = 'Three Connector'
    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'F-Curve'

    def draw(self, context):
        layout = self.layout
        layout.label(text='Curves')

        for fcurve in bpy.context.selected_editable_fcurves:
            fcurve_id = FCurveManager.get_fcurve_id(fcurve, True)

            clm = layout.column()
            box = clm.box()
            box.label(text=fcurve_id)

            found = False
            
            for curveData in bpy.context.scene.three_connector.fcurve_list:
                if( curveData.name == fcurve_id ):
                    row = box.row()
                    row.prop(curveData, 'accessor' )
                    row.prop(curveData, 'axis', text='axis')
                    found = True
                    break
            
            if not found:
                creator = box.operator( THREECONNECTOR_OT_FCurveAccessorCreate.bl_idname, text='Create' )
                creator.fcurve_id = fcurve_id

        layout.label(text='Controls')
        layout.operator( THREECONNECTOR_OT_FCurveAccessorRename.bl_idname, text='Rename Accessors' )
