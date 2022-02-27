bl_info = {
    "name" : "Three Connector",
    "author" : "ukonpower",
    "description" : "",
    "blender" : (2, 93, 8),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

# if "bpy" in locals():
#     import imp
#     imp.reload(auto_load)
# else:
from . import auto_load

auto_load.init()

def register():
    auto_load.register()

def unregister():
    auto_load.unregister()
