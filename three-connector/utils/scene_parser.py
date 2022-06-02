from ast import Str
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

    def get_fcurve_axis(self, fcurveId: str, axis: str):

        axisList = 'xyzw'

        if( not fcurveId.find( 'Shader NodetreeAction' ) > -1 ):
            axisList = 'xzyw'

        axisIndex = axisList.find(axis)

        if( axisIndex > -1 ):
            return 'xyzw'[axisIndex]

        return axis

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
            "axis": "scaler",
            "keyframes": None
        }

        fcurveId = FCurveManager.get_fcurve_id(fcurve, True)

        invert = fcurveId.find( 'location_y' ) > -1 or fcurveId.find( 'rotation_euler_y' ) > -1
        parsed_fcurve['keyframes'] = self.parse_keyframe_list(fcurve.keyframe_points, invert)

        for fcurve_prop in bpy.context.scene.three_connector.fcurve_list:
            if( fcurve_prop.name == fcurveId):
                parsed_fcurve["axis"] = self.get_fcurve_axis( fcurveId, fcurve_prop.axis )
                break
                
        return parsed_fcurve
    
    # Parse Action ----------------------

    def parse_action(self, action: bpy.types.Action ):

        parsed_fcurve_list = dict()
        
        for fcurve in action.fcurves:
            for fcurve_prop in bpy.context.scene.three_connector.fcurve_list:
                fcurveId = FCurveManager.get_fcurve_id(fcurve, True)
                if( fcurve_prop.name == fcurveId ):
                    if( fcurve_prop.accessor in parsed_fcurve_list ):
                        parsed_fcurve_list[fcurve_prop.accessor].append(self.parse_fcurve(fcurve))
                    else:
                        parsed_fcurve_list[fcurve_prop.accessor] = [self.parse_fcurve(fcurve)]
                
        return {
            "name": action.name_full,
            "fcurve_groups": parsed_fcurve_list
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
                if object_animation_data.action != None:
                    object_data["actions"].append( object_animation_data.action.name_full )

            for matSlot in object.material_slots:
                mat_animation_data = matSlot.material.node_tree.animation_data
                if mat_animation_data:
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
        }
        return animation_data
