import bpy
from sbstudio.plugin.constants import Collections

class SkybrushDeselectKeyframesOperator(bpy.types.Operator):
    bl_idname = 'skybrush.deselect_keyframes'
    bl_label = '取消选中关键帧'
    bl_description = '取消选中指定关键帧'
    bl_options = {'REGISTER', 'UNDO'}

    is_color = bpy.props.BoolProperty(default=True, options={"HIDDEN"})

    def execute(self, context):
        drones = Collections.find_drones(create=False)
        if not drones:
            return {"CANCELLED"}
        for drone in drones.objects:
            if not (drone.animation_data and drone.animation_data.action):
                continue
            for fcurve in drone.animation_data.action.fcurves:
                if ("color" == fcurve.data_path) ^ (not self.is_color):
                    for keyframe_point in fcurve.keyframe_points:
                        keyframe_point.select_control_point = False
                        keyframe_point.select_left_handle = False
                        keyframe_point.select_right_handle = False
        return {"FINISHED"}
