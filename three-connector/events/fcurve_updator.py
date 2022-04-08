import bpy;

class FCurveUpdator:

	@classmethod
	def update(cls):
		for action in bpy.data.actions:
			for fcurve in action.fcurves:
				for curveData in bpy.context.scene.three_connector.fcurve_list:
					if( curveData.name == fcurve.data_path ):
						return
				item = bpy.context.scene.three_connector.fcurve_list.add()
				item.name = str(fcurve.data_path)
				item.value = ""
				print(fcurve.data_path)

	@classmethod
	def register(cls):
		print('')
		
	@classmethod
	def unregister(cls):
		print('')