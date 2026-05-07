import math
import numpy as np
import bpy

from bpy.props import BoolProperty, IntProperty
from bpy.types import Operator
from sbstudio.api.console import ConsoleWindow
from sbstudio.plugin.props.frame_range import FrameRangeProperty, resolve_frame_range
from sbstudio.plugin.colors import get_color_of_drone
from sbstudio.plugin.tasks.safety_check import suspended_safety_checks
from .utils import get_drones_to_export

__all__ = ("ValidateLightsOperator",)

def linear_2_gamma(value: float) -> float:
    if value <= 0.0:
        return 0.0
    elif value <= 0.0031308:
        return 12.92 * value
    elif value < 1.0:
        return 1.055 * math.pow(value, 0.4166667) - 0.055
    else:
        return math.pow(value, 0.45454545)

def get_int_255_color(drone) -> list[int]:
    return [max(0, min(255, int(linear_2_gamma(c) * 255 + 0.5))) for c in get_color_of_drone(drone)[:3]]

class ValidateLightsOperator(Operator):
    bl_idname = "skybrush.validate_lights"
    bl_label = "Validate Lights"
    bl_description = "Validates the lights of the drones in a given frame range."

    limit_r = IntProperty(name="R通道最大亮度", default=250, min=0, max=255)
    limit_g = IntProperty(name="G通道最大亮度", default=250, min=0, max=255)
    limit_b = IntProperty(name="B通道最大亮度", default=250, min=0, max=255)

    # validate all drones or only selected ones
    selected_only = BoolProperty(
        name="Selection only",
        default=False,
        description=(
            "Validate only the selected drones. "
            "Uncheck to export all drones, irrespectively of the selection."
        ),
    )

    # frame range source
    frame_range = FrameRangeProperty()

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        frame_current = context.scene.frame_current
        drones = get_drones_to_export(selected_only=self.selected_only)
        frame_range = resolve_frame_range(self.frame_range)
        if frame_range is None:
            self.report({"ERROR"}, "Selected frame range is empty")
            return {"CANCELLED"}

        result, history, limit = [], {}, np.array([self.limit_r, self.limit_g, self.limit_b])
        with suspended_safety_checks(), ConsoleWindow():
            current_frame, last_frame = frame_range
            while current_frame < last_frame:
                current_frame += 1
                print(f"[Validate] Current Frame: {current_frame}/{last_frame}\r", end="")
                lights = self.get_lights(context, current_frame, drones)
                mask = np.all(lights > limit, axis=1)
                indices = np.where(mask)[0]
                max_values = np.max(lights[mask], axis=1)
                for i in list(history.keys() - set(indices)):
                    result.append((i, history[i]))
                    history.pop(i)
                for idx, val in zip(indices, max_values):
                    if idx not in history or val > history[idx][1]:
                        history[idx] = (current_frame, val)
            print()
            result.extend(history.items())
            bpy.types.Scene.validate_lights_result = {
                "drones": drones,
                "lights_result": result,
            }
            context.scene.frame_set(frame_current)

        return {"FINISHED"}

    def get_lights(self, context, frame, drones):
        context.scene.frame_set(frame)
        return np.array([get_int_255_color(drone) for drone in drones])
