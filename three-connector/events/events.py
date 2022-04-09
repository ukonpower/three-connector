import bpy;
from bpy.app.handlers import persistent
from ..managers.fcurve import FCurveManager

@persistent
def update(scene, context):
	FCurveManager.update()
    
def register():
	bpy.app.handlers.depsgraph_update_post.append(update)

def unregister():
	try:
		bpy.app.handlers.depsgraph_update_post.remove(update)
	except ValueError:
		pass
