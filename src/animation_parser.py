import bpy

class AnimationParser:

    # parse ----------------------

    def get_fcurve_name(self, fcurve: bpy.types.FCurve ):
        items = "xyzw"
        index = fcurve.array_index

        if 0 <= index and index <= 4:
            return fcurve.data_path + '_' + items[fcurve.array_index]
        else:
            return fcurve.data_path

    def parse_keyframe(self, keyframe: bpy.types.Keyframe):
        parsed_keyframe = {
                "c": keyframe.co,
                "h_l": keyframe.handle_left,
                "h_r": keyframe.handle_right,
                "e": keyframe.easing,
                "i": keyframe.interpolation
        }
        return parsed_keyframe

    def parse_fcurve(self, fcurve: bpy.types.FCurve ):
        curve_parsed = {
            "name": self.get_fcurve_name(fcurve),
            "frames": self.parse_keyframe_list(fcurve.keyframe_points)
        }
            
        return curve_parsed

    # parse list ----------------------

    def parse_keyframe_list(self, keyframes: list[bpy.types.Keyframe]):
        parsed_keyframes = []
        for keyframe in keyframes:
            parsed_keyframes.append(self.parse_keyframe_list(keyframe))

    def parse_action(self, action: bpy.types.Action ):
        action_parsed = {
            "name": action.name,
            "curves": self.parse_fcurves_list(action.fcurves)
        }
        return action_parsed

    def parse_fcurves_list(self, fcurves: list[bpy.types.FCurve] ):
        parsed_fcurves = []
        for curve in fcurves:
            parsed_fcurve = self.parse_fcurve(curve)
            parsed_fcurves.append(parsed_fcurve)
        return parsed_fcurves

    def parse_action_list(self, actions: list[bpy.types.Action] ):
        parsed_actions = []
        for action in actions:
            parsed_action = self.parse_action(action)
            parsed_actions.append(parsed_action)

        return parsed_actions

    #  API ----------------------

    def get_animation_date(self):
        animation_data = {
            "actions": self.parse_action_list(bpy.data.actions)
        }
        
        return animation_data
