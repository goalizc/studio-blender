import math

from bpy.props import IntProperty, FloatProperty, EnumProperty
from bpy.types import Operator

from sbstudio.plugin.utils.evaluator import get_position_of_object

__all__ = ("SkybrushFrameDelayOperator", )

class SkybrushFrameDelayOperator(Operator):
    bl_idname = "skybrush.frame_delay"
    bl_label = "Frame Delay"
    bl_description = (
        "Delay processing of selected frames according to the selected strategy"
    )
    bl_options = {"REGISTER", "UNDO"}

    reference_frame = IntProperty(
        name="Reference frame",
        description="Use this frame as a reference to take distance parameters during processing."
    )

    direction = EnumProperty(
        name="Direction",
        items=[
            ("UP", "Z+", ""),
            ("DOWN", "Z-", ""),
            ("LEFT", "X+", ""),
            ("RIGHT", "X-", ""),
            ("FORWARD", "Y+", ""),
            ("BACKWARD", "Y-", ""),
        ],
        default="UP"
    )

    unit_distance = FloatProperty(
        name="Unit distance",
        description="Unit distance of frame delay",
        unit="LENGTH",
        default=1,
        min=0,
        soft_min=0,
        soft_max=100,
    )

    delay_frames = IntProperty(
        name="Delay frames",
        description="Number of frames of delay per unit distance",
        default=1,
        min=0,
        soft_min=0,
        soft_max=100,
    )

    def invoke(self, context, event):
        self.reference_frame = context.scene.frame_current
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        key, offset = self.get_tool_function()
        objects = sorted(context.selected_objects, key=key)
        if objects:
            head, head_position = objects[0], get_position_of_object(objects[0])
            for obj in objects[1:]:
                obj_position = get_position_of_object(obj)
                self.move_selected_frames(obj, offset(head_position, obj_position))

        return {"FINISHED"}

    def get_tool_function(self):
        if self.direction == "UP":
            key = lambda obj:  get_position_of_object(obj)[2]
        elif self.direction == "DOWN":
            key = lambda obj: -get_position_of_object(obj)[2]
        elif self.direction == "LEFT":
            key = lambda obj: -get_position_of_object(obj)[0]
        elif self.direction == "RIGHT":
            key = lambda obj:  get_position_of_object(obj)[0]
        elif self.direction == "FORWARD":
            key = lambda obj:  get_position_of_object(obj)[1]
        elif self.direction == "BACKWARD":
            key = lambda obj: -get_position_of_object(obj)[1]

        level = self.delay_frames / self.unit_distance
        if self.direction == "UP" or self.direction == "DOWN":
            offset = lambda a, b: math.ceil(abs(a[2] - b[2]) * level)
        elif self.direction == "LEFT" or self.direction == "RIGHT":
            offset = lambda a, b: math.ceil(abs(a[0] - b[0]) * level)
        elif self.direction == "FORWARD" or self.direction == "BACKWARD":
            offset = lambda a, b: math.ceil(abs(a[1] - b[1]) * level)

        return key, offset

    def move_selected_frames(self, obj, offset):
        if offset == 0:
            return
        for fcurve in obj.animation_data.action.fcurves:
            for p in [p for p in fcurve.keyframe_points if p.select_control_point]:
                p.co.x += offset
                p.handle_left.x += offset
                p.handle_right.x += offset
        for mat_slot in obj.material_slots:
            if mat_slot.material and mat_slot.material.use_nodes and mat_slot.material.node_tree.animation_data is not None:
                for fcurve in mat_slot.material.node_tree.animation_data.action.fcurves:
                    for p in [p for p in fcurve.keyframe_points if p.select_control_point]:
                        p.co.x += offset
                        p.handle_left.x += offset
                        p.handle_right.x += offset
