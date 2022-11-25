import bpy
from bpy.types import (Operator)

from ..managers.fcurve import FCurveManager

class THREECONNECTOR_OT_FCurveAccessorCreate(Operator):
	bl_idname = 'object.threeconnector_fcurve_asccessor_create'
	bl_label="Create Accessor"
	bl_options = {'REGISTER', 'UNDO'}
	
	fcurve_id: bpy.props.StringProperty(name="fcurve id", default="" )
		
	def execute(self, context):

		fcurve = FCurveManager.get_fcurve(self.fcurve_id)

		exist = False
			
		for curveData in bpy.context.scene.three_connector.fcurve_list:
			if( curveData.name == self.fcurve_id ):
				exist = True
				break
			
		if( not exist and fcurve != None ):
			item = bpy.context.scene.three_connector.fcurve_list.add()
			item.name = self.fcurve_id
			item.index = fcurve.array_index
			item.data_path = fcurve.data_path
			item.accessor = FCurveManager.get_fcurve_id(fcurve)
			item.axis = 'xyzw'[fcurve.array_index]

		return {'FINISHED'}

class THREECONNECTOR_OT_FCurveAccessorRename(Operator):
	bl_idname = 'object.threeconnector_fcurve_asccessor_rename'
	bl_label="Rename Accessor"
	bl_options = {'REGISTER', 'UNDO'}
	
	accessor_name: bpy.props.StringProperty(name="accessor name", default="" )
	
	fcurve_id: bpy.props.StringProperty(name="fcurve id", default="" )
	
	def invoke(self, context = None, event = None ):
		self.accessor_name = ''
		return bpy.context.window_manager.invoke_props_dialog(self)
		
	def execute(self, context):
		for fcurve in bpy.context.selected_editable_fcurves:
			fcurve_id = FCurveManager.get_fcurve_id(fcurve, True)
			for curveData in bpy.context.scene.three_connector.fcurve_list:
				if( curveData.name == fcurve_id ):
					curveData.accessor = self.accessor_name

		bpy.context.area.tag_redraw()
		
		return {'FINISHED'}


class THREECONNECTOR_OT_FCurveAccessorDelete(Operator):
	bl_idname = 'object.threeconnector_fcurve_asccessor_delete'
	bl_label="Delete Accessor"
	bl_options = {'REGISTER', 'UNDO'}
	
	accessor_name: bpy.props.StringProperty(name="accessor name", default="" )
		
	def execute(self, context):
		for fcurve in bpy.context.selected_editable_fcurves:
			fcurve_id = FCurveManager.get_fcurve_id(fcurve, True)
			for curveData in bpy.context.scene.three_connector.fcurve_list:
				if( curveData.name == fcurve_id ):
					curveData.accessor = self.accessor_name

		bpy.context.area.tag_redraw()
		
		return {'FINISHED'}