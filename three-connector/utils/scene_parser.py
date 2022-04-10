import bpy

from ..managers.fcurve import FCurveManager

class SceneParser:

    # Parse Keyframe ----------------------

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

    def get_fcurve_coord(self, fcurve: bpy.types.FCurve ):

        items = "xyzw"

        if fcurve.data_path == 'location':
            items = "xzyw"

        if fcurve.data_path == 'rotation_euler':
            items = "xzyw"

        if fcurve.data_path == 'scale':
            items = "xzyw"

        index = fcurve.array_index
        if 0 <= index and index <= 4:
            return items[fcurve.array_index]
        else:
            return None

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

    # Parse F-Curve ----------------------

    def parse_fcurve(self, fcurve: bpy.types.FCurve ):

        parsed_fcurve = {
            "name": "none",
            "axis": "none",
            "keyframes": None
        }

        fcurveId = FCurveManager.getFCurveId(fcurve, True)

        invert = fcurveId.find( 'location_z' ) > -1 or fcurveId.find( 'rotation_euler_z' ) > -1
        parsed_fcurve['keyframes'] = self.parse_keyframe_list(fcurve.keyframe_points, invert)
        
        for fcurve_prop in bpy.context.scene.three_connector.fcurve_list:
            if( fcurve_prop.name == fcurveId):
                parsed_fcurve["name"] = fcurve_prop.accessor
                parsed_fcurve["axis"] = fcurve_prop.axis
                
        return parsed_fcurve
    
    # Parse Action ----------------------

    def parse_action(self, action: bpy.types.Action ):

        fcurve_accessor_list = []
        
        for fcurve in action.fcurves:
            fcurveId = FCurveManager.getFCurveId(fcurve, True)
            for fcurve_prop in bpy.context.scene.three_connector.fcurve_list:
                if( fcurve_prop.name == fcurveId):
                    fcurve_accessor_list.append(fcurve_prop.name)
                
        return {
            "name": action.name_full,
            "fcurves": fcurve_accessor_list
        }

    #  Object List ----------------------

    def get_object_list(self):
        objects = bpy.data.objects

        parsed_objects = []

        for object in objects:
            object_data = {
                "name": object.name,
                "actions": []
            }

            object_animation_data = object.animation_data
            
            if object_animation_data:
                object_data["actions"].append( object_animation_data.action.name_full )

            for matSlot in object.material_slots:
                mat_animation_data = matSlot.material.node_tree.animation_data
                if object_animation_data:
                    object_data["actions"].append( mat_animation_data.action.name_full )

            if len(object_data["actions"])  > 0:
                parsed_objects.append(object_data)

        return parsed_objects

    #  Action List ----------------------

    def get_action_list(self):
        parsed_action_list = []

        for action in bpy.data.actions:
            parsed_action_list.append( self.parse_action(action) )
        
        return parsed_action_list

    #  Action List ----------------------

    def get_fcurve_list(self):
        parse_fcurve_list = []

        actionList: list[bpy.types.Action] = bpy.data.actions
        for action in actionList:
            
            curveList: list[bpy.types.FCurve] = action.fcurves
            for fcurve in curveList:
                parse_fcurve_list.append( self.parse_fcurve(fcurve) )
        
        return parse_fcurve_list
    
    #  API ----------------------

    def get_animation_date(self):
        animation_data = {
            "objects": self.get_object_list(),
            "actions": self.get_action_list(),
            "fcurves": self.get_fcurve_list(),
        }
        return animation_data
