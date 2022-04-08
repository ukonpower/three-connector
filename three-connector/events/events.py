import bpy;
from bpy.app.handlers import persistent

from .fcurve_updator import FCurveUpdator

@persistent
def update(scene, context):
    FCurveUpdator.update()
    
def register():
	FCurveUpdator.register()
	bpy.app.handlers.depsgraph_update_post.append(update)

def unregister():
	FCurveUpdator.unregister()

	try:
		bpy.app.handlers.depsgraph_update_post.remove(update)
	except ValueError:
		pass