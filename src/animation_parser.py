import bpy

class AnimationParser:

    # parse ----------------------

    def parse_vector(self, vector):
        parsed_vector = {}
        if hasattr( vector,"x" ):
            parsed_vector["x"] = vector.x
        if hasattr( vector,"y" ):
            parsed_vector["y"] = vector.y
        if hasattr( vector,"z" ):
            parsed_vector["z"] = vector.z
        if hasattr( vector,"w" ):
            parsed_vector["w"] = vector.w
            
        return parsed_vector

    def get_fcurve_name(self, fcurve: bpy.types.FCurve ):
        items = "xyzw"

        if fcurve.data_path == 'location':
            items = "xzyw"

        if fcurve.data_path == 'rotation_euler':
            items = "xzyw"

        if fcurve.data_path == 'scale':
            items = "xzyw"
        
        index = fcurve.array_index
        if 0 <= index and index <= 4:
            return fcurve.data_path + '_' + items[fcurve.array_index]
        else:
            return fcurve.data_path

    #  keyframe

    def parse_keyframe(self, keyframe: bpy.types.Keyframe):
        parsed_keyframe = {
                "c": self.parse_vector(keyframe.co),
                "h_l": self.parse_vector(keyframe.handle_left),
                "h_r": self.parse_vector(keyframe.handle_right),
                "e": keyframe.easing,
                "i": keyframe.interpolation
        }
        return parsed_keyframe

    def parse_keyframe_list(self, keyframes: list[bpy.types.Keyframe], invert: bool ):
        parsed_keyframes = []
        for keyframe in keyframes:
            parsed_keyframe = self.parse_keyframe(keyframe)

            if invert:
                parsed_keyframe["c"]["y"] *= -1
                parsed_keyframe["h_l"]["y"] *= -1
                parsed_keyframe["h_r"]["y"] *= -1

            parsed_keyframes.append(parsed_keyframe)
                
        return parsed_keyframes

    #  fcurve
    
    def parse_fcurve(self, fcurve: bpy.types.FCurve ):

        curveName = self.get_fcurve_name(fcurve)
        frames = self.parse_keyframe_list(fcurve.keyframe_points, curveName.find( 'location_z' ) > -1 or curveName.find( 'rotation_euler_z' ) > -1)
        
        curve_parsed = {
            "name": curveName,
            "frames": frames
        }

        return curve_parsed

    def parse_fcurves_list(self, fcurves: list[bpy.types.FCurve] ):
        parsed_fcurves = []
        for curve in fcurves:
            parsed_fcurve = self.parse_fcurve(curve)
            parsed_fcurves.append(parsed_fcurve)
        return parsed_fcurves

    #  action

    def parse_action(self, action: bpy.types.Action ):
        action_parsed = {
            "name": action.name_full,
            "curves": self.parse_fcurves_list(action.fcurves)
        }
        return action_parsed


    def parse_action_list(self, actions: list[bpy.types.Action] ):
        parsed_actions = []
        for action in actions:
            parsed_action = self.parse_action(action)
            parsed_actions.append(parsed_action)

        return parsed_actions

    #  Objects ----------------------

    def paser_object_list(self, objects: list[bpy.types.Object]):
        objects = bpy.data.objects

        parsed_objects = []

        for object in objects:
            object_data = {
                "name": object.name,
                "actions": []
            }

            animation_data = object.animation_data
            
            if animation_data:
                object_data["actions"].append( animation_data.action.name_full )
                parsed_objects.append(object_data)

        return parsed_objects

    #  API ----------------------

    def get_animation_date(self):
        animation_data = {
            "actions": self.parse_action_list(bpy.data.actions),
            "objects": self.paser_object_list(bpy.data.objects)
        }
        return animation_data
