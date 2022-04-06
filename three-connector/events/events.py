import bpy;
from bpy.app.handlers import persistent
from .fcurve_updator import FCurveUpdator

@persistent
def update():
    FCurveUpdator.update()
    
def register():
	bpy.app.handlers.depsgraph_update_post.append(update)

def unregister():
	try:
		bpy.app.handlers.depsgraph_update_post.remove(update)
	except ValueError:
		pass