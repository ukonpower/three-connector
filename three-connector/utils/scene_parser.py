from tokenize import String
import bpy
import re

class SceneParser:

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

    def get_fcurve_coord(self, fcurve: bpy.types.FCurve ):

        # coord
        
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

    #  action - object

    def parse_action_object(self, object: bpy.types.Object, action: bpy.types.Action ):

        parsed_fcurves = []
        
        for fcurve in action.fcurves:

            curve_name = fcurve.data_path

            # coord

            coord = self.get_fcurve_coord(fcurve)
            
            if coord:
                curve_name += '_' + coord
                
            # frames

            frames = self.parse_keyframe_list(fcurve.keyframe_points, curve_name.find( 'location_z' ) > -1 or curve_name.find( 'rotation_euler_z' ) > -1)

            parsed_fcurves.append({
                "name": curve_name,
                "frames": frames
            })

        return {
            "name": action.name_full,
            "curves": parsed_fcurves
        }

    #  action - material

    def get_node_name_by_data_path(self, data_path: String):
        node_name_match = re.search(r'(?<=nodes\[\").*?(?=\"\])', data_path)
        if node_name_match:
            return node_name_match.group()
        return None

    def get_input_index_by_datapath(self, data_path: String):
        node_name_match = re.search(r'(?<=inputs\[).*?(?=\])', data_path)
        if node_name_match:
            return node_name_match.group()
        return None

    def get_output_index_by_datapath(self, data_path: String):
        node_name_match = re.search(r'(?<=outputs\[).*?(?=\])', data_path)
        if node_name_match:
            return node_name_match.group()
        return None

    def parse_action_material(self, material: bpy.types.Material, action: bpy.types.Action ):

        action_name = material.name

        parsed_fcurves = []
        
        for fcurve in action.fcurves:

            curve_name = ""

            # node name?
            
            node_name = self.get_node_name_by_data_path(fcurve.data_path)

            if node_name != None:
                node = material.node_tree.nodes[node_name]

                # inputs | outpus ?

                input_index = self.get_input_index_by_datapath(fcurve.data_path)
                output_index = self.get_output_index_by_datapath(fcurve.data_path)

                if input_index != None:
                    node_name += '_' + node.inputs[int(input_index)].name

                elif output_index != None:
                    node_name += '_' + node.outputs[int(output_index)].name

                curve_name = node_name
            
            # coord
            
            coord = self.get_fcurve_coord(fcurve)

            if coord:
                curve_name += '_' + coord

            # frames

            frames = self.parse_keyframe_list(fcurve.keyframe_points, False )

            parsed_fcurves.append({
                "name": curve_name,
                "frames": frames
            })
        
        action_parsed = {
            "name": action_name,
            "curves": parsed_fcurves
        }

        return action_parsed

    #  Objects ----------------------

    def parse_object_list(self, objects: list[bpy.types.Object]):
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

    def get_actions(self):
        actions = []
        
        # object action

        for object in bpy.data.objects:
            object_animation_data = object.animation_data
            
            if object_animation_data:
                actions.append( self.parse_action_object( object, object_animation_data.action ) )

        for mat in bpy.data.materials:
            if mat.node_tree:
                mat_animation_data = mat.node_tree.animation_data

                if mat_animation_data:
                    actions.append( self.parse_action_material( mat, mat_animation_data.action ) )
        
        # material action
        return actions

    #  API ----------------------

    def get_animation_date(self):
        animation_data = {
            "actions": self.get_actions(),
            "objects": self.parse_object_list(bpy.data.objects)
        }
        return animation_data
