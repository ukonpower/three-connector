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
	def get_fcurve_id(cls, fcurve: bpy.types.FCurve, axis: bool = False):
		result = fcurve.data_path

		actionName = re.search(r'(?<=\(\").*?(?=\"\))', str(fcurve.id_data))
		if actionName:
			result = actionName.group() + '_' + result
		else:
			result = "unknown" + "_" + result

		if axis:
			result += '_' + 'xyzw'[fcurve.array_index]
			
		return  result

	def get_fcurve(cls, fcurve_id: str ):

		actionList: list[bpy.types.Action] = bpy.data.actions
		for action in actionList:
			
			curveList: list[bpy.types.FCurve] = action.fcurves
			
			for curve in curveList:
				if( FCurveManager.get_fcurve_id(curve, True) == fcurve_id ):
					return curve