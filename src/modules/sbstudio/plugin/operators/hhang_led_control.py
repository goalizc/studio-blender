import bpy
from random import shuffle
from bpy.types import Operator
from bpy.props import EnumProperty
from sbstudio.plugin.panels import HHangLEDControlPanel, LightEffectsPanel
from sbstudio.plugin.plugin_helpers import register_panel, unregister_panel
from sbstudio.plugin.selection import get_selected_drones
from sbstudio.plugin.utils.evaluator import create_position_evaluator
from sbstudio.plugin.colors import create_keyframe_for_color_of_drone

__all__ = (
    "UseHHangLEDControlOperator",
    "HHangLEDControlGenerateOperator",
    "HHangLEDControlApplyOperator"
)

class UseHHangLEDControlOperator(Operator):
    bl_idname = 'skybrush.use_hhang_led_control'
    bl_label = 'Generate'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.skybrush.hhang_led_control_generate()
        unregister_panel(LightEffectsPanel)
        register_panel(HHangLEDControlPanel)
        register_panel(LightEffectsPanel)
        bpy.types.Scene.used_hhang_led_control = True
        return {"FINISHED"}

class HHangLEDControlGenerateOperator(Operator):
    bl_idname = 'skybrush.hhang_led_control_generate'
    bl_label = 'Generate'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hhang_led_control = context.scene.skybrush.hhang_led_control
        if not hhang_led_control.texture:
            hhang_led_control.texture = bpy.data.textures.new(name="HHangLedControl", type="IMAGE")
            hhang_led_control.texture.use_color_ramp = True
            hhang_led_control.texture.image = None
        return {'FINISHED'}

class HHangLEDControlApplyOperator(Operator):
    bl_idname = 'skybrush.hhang_led_control_apply'
    bl_label = 'Apply'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        color = context.scene.skybrush.hhang_led_control.color
        for drone in get_selected_drones():
            create_keyframe_for_color_of_drone(drone, color)
        return {'FINISHED'}

class HHangLEDControlGradientOperator(Operator):
    bl_idname = 'skybrush.hhang_led_control_gradient'
    bl_label = 'Gradient'
    bl_options = {'REGISTER', 'UNDO'}

    gradient_mode = EnumProperty(
        name="Order in gradient",
        items=[
            ("DEFAULT", "Default", "", 1),
            ("RANDOM", "Random", "", 2),
            ("X", "X coordinate", "", 3),
            ("Y", "Y coordinate", "", 4),
            ("Z", "Z coordinate", "", 5),
            ("DISTANCE", "Distance from 3D cursor", "", 6),
        ],
        default="DISTANCE",
    )

    def execute(self, context):
        color_ramp = context.scene.skybrush.hhang_led_control.texture.color_ramp
        selection = get_selected_drones()
        num_selected = len(selection)
        if not num_selected:
            self.report({"INFO"}, "Select some drones first to apply colors")
            return {"CANCELLED"}

        for index, drone in enumerate(self._sort_selection(selection, context)):
            ratio = index / (num_selected - 1) if num_selected > 1 else 0.5
            color = color_ramp.evaluate(ratio)[:3]
            create_keyframe_for_color_of_drone(drone, color)

        return {"FINISHED"}

    def _sort_selection(self, selection, context):
        if self.gradient_mode == "DEFAULT":
            return selection

        if self.gradient_mode == "RANDOM":
            shuffle(selection)
            return selection

        with create_position_evaluator() as get_positions_of:
            positions = get_positions_of(selection)

        if self.gradient_mode == "X":
            priorities = [point[0] for point in positions]
        elif self.gradient_mode == "Y":
            priorities = [point[1] for point in positions]
        elif self.gradient_mode == "Z":
            priorities = [point[2] for point in positions]
        elif self.gradient_mode == "DISTANCE":
            cl = tuple(context.scene.cursor.location)
            priorities = [(cl[0] - p[0]) ** 2 + (cl[1] - p[1]) ** 2 + (cl[2] - p[2]) ** 2
                            for p in positions ]
        else:
            return selection

        order = list(range(len(selection)))
        order.sort(key=priorities.__getitem__)

        return [selection[i] for i in order]
