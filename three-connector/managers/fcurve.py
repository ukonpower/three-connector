import bpy;
import re;

class ThreeConnectorFCurveProperty(bpy.types.PropertyGroup):
	index: bpy.props.IntProperty(default=0)
	data_path: bpy.props.StringProperty(default='')
	accessor: bpy.props.StringProperty(default='')
	axis: bpy.props.EnumProperty(
		name="axis",
        description="value axis",
        items=[
			( "x", "X", "" ),
			( "y", "Y", "" ),
			( "z", "Z", "" ),
			( "w", "W", "" ),
			( "scalar", "Scalar", "" )
		],
		default='scalar'
	)

class FCurveManager:
	@classmethod
	def getFCurveId(cls, fcurve: bpy.types.FCurve, axis: bool = False):
		result = fcurve.data_path

		actionName = re.search(r'(?<=\(\").*?(?=\"\))', str(fcurve.id_data))
		if actionName:
			result = actionName.group() + '_' + result
		else:
			result = "unknown" + "_" + result

		if axis:
			result += '_' + 'xyzw'[fcurve.array_index]
			
		return  result
	
	@classmethod
	def update(cls):

		# bpy.context.scene.three_connector.fcurve_list.clear()

		actionList: list[bpy.types.Action] = bpy.data.actions
		for action in actionList:
			
			curveList: list[bpy.types.FCurve] = action.fcurves
			for fcurve in curveList:
				
				exist = False
				curveId = cls.getFCurveId(fcurve, True)

				for curveData in bpy.context.scene.three_connector.fcurve_list:
					if( curveData.name == curveId ):
						exist = True
						break

				if( not exist ):
					item = bpy.context.scene.three_connector.fcurve_list.add()
					item.name = curveId
					item.index = fcurve.array_index
					item.data_path = fcurve.data_path
					item.accessor = cls.getFCurveId(fcurve)
					item.axis = 'xyzw'[fcurve.array_index]