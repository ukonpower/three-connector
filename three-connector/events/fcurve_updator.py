import bpy;

class FCurveUpdator:

	@classmethod
	def create_prop(self, curve: bpy.types.FCurve):
		_
		# if( hasattr(curve, 'accessor') ):
		# 	curve.accessor = bpy.props.StringProperty(name=curve.data_path, default=curve.data_path)

	@classmethod
	def update():
		curves = bpy.data.curves
		for curve in curves:
			FCurveUpdator.create_prop(curve)