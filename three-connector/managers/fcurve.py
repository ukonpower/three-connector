import bpy;
import re;

class ThreeConnectorFCurveData(bpy.types.PropertyGroup):
	index: bpy.props.IntProperty(default=0)
	accessor: bpy.props.StringProperty(default='')
	axis: bpy.props.EnumProperty(
		name="axis",
        description="value axis",
        items=[
			( "x", "X", "" ),
			( "y", "Y", "" ),
			( "z", "Z", "" ),
			( "w", "W", "" ),
			( "none", "None", "" )
		],
		default='none'
	)

class FCurveManager:
	@classmethod
	def getFCurveId(cls, fcurve: bpy.types.FCurve):
		result = fcurve.data_path + '_' + 'xyzw'[fcurve.array_index]
		actionName = re.search(r'(?<=\(\").*?(?=\"\))', str(fcurve.id_data))

		if actionName:
			result = actionName.group() + '_' + result
			
		return  result
	
	@classmethod
	def update(cls):
		actionList: list[bpy.types.Action] = bpy.data.actions
		for action in actionList:
			
			curveList: list[bpy.types.FCurve] = action.fcurves
			for fcurve in curveList:

				exist = False
				curveDataName = cls.getFCurveId(fcurve)

				for curveData in bpy.context.scene.three_connector.fcurve_list:
					if( curveData.name == curveDataName ):
						exist = True
						break
				
				if( not exist ):
					item = bpy.context.scene.three_connector.fcurve_list.add()
					item.name = curveDataName
					item.accessor = curveDataName
