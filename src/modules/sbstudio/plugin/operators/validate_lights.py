import collections
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
    interval = IntProperty(name="检测区间（帧）", default=20, min=10)
    percentage = IntProperty(name="占百分比", default=50, min=10, max=100)

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

        result, history, limit = [], {}, np.array(
            [self.limit_r, self.limit_g, self.limit_b]
        )
        frame_buffer = collections.deque(maxlen=self.interval)
        frame_indices = collections.deque(maxlen=self.interval)

        with suspended_safety_checks(), ConsoleWindow():
            current_frame, last_frame = frame_range
            while current_frame < last_frame:
                current_frame += 1
                print(f"[Validate] Current Frame: {current_frame}/{last_frame}\r", end="")
                lights = self.get_lights(context, current_frame, drones)
                frame_buffer.append(lights)
                frame_indices.append(current_frame)

                if len(frame_buffer) >= self.interval:
                    threshold = int(
                        math.ceil(self.interval * self.percentage / 100)
                    )
                    for idx in range(len(drones)):
                        exceed_count = 0
                        max_val = 0.0
                        max_frame = 0
                        for frame_lights, frame_idx in zip(frame_buffer, frame_indices):
                            if np.all(frame_lights[idx] > limit):
                                exceed_count += 1
                                val = float(np.max(frame_lights[idx]))
                                if val > max_val:
                                    max_val = val
                                    max_frame = frame_idx
                        if exceed_count >= threshold:
                            if idx not in history:
                                history[idx] = (max_frame, max_val)
                                result.append((idx, history[idx]))
                            elif max_val > history[idx][1]:
                                history[idx] = (max_frame, max_val)
                        elif idx in history:
                            history.pop(idx)

            print()
            bpy.types.Scene.validate_lights_result = {
                "drones": drones,
                "lights_result": result,
            }
            context.scene.frame_set(frame_current)

        return {"FINISHED"}

    def get_lights(self, context, frame, drones):
        context.scene.frame_set(frame)
        return np.array([get_int_255_color(drone) for drone in drones])
