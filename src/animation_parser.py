import bpy

class AnimationParser:

    def __init__(self):
        print( bpy )

    def track(self, object: bpy.types.Object):
        anim_data = object.animation_data
        
        if( anim_data ):
            curves = anim_data.action.fcurves
            for curve in curves:
                print( curve )
            # for track in anim_data.nla_tracks:
            #     print( track )

    def get_animation_date(self):
        context = bpy.context
        
        for obj in bpy.data.objects:
            self.track(obj)
