import bpy
import math
import time
import numpy as np

from bpy.props import IntProperty, FloatProperty
from bpy.types import Operator

from sbstudio.api.console import ConsoleWindow
from sbstudio.plugin.constants import Collections
from sbstudio.plugin.utils.evaluator import get_position_of_object

__all__ = ("SkybrushCalculateSafePathOperator", )

MARGIN = 0.03

def find_nearby_objects(positions, min_distance):
    num_objects = len(positions)
    distances = np.sqrt(((positions[:, np.newaxis] - positions)**2).sum(axis=2))
    upper_triangle_mask = np.triu(np.ones((num_objects, num_objects), dtype=bool), k=1)
    too_close = np.where((distances < min_distance) & upper_triangle_mask)
    return [(i, j, distances[i, j]) for i, j in zip(too_close[0], too_close[1])]

def adjust_object_positions(objects, min_distance):
    positions = np.array([get_position_of_object(obj) for obj in objects], dtype=np.float64)
    adjusted_indices = set()

    while True:
        nearby_pairs = find_nearby_objects(positions, min_distance)
        if not nearby_pairs:
            break

        nearby_pairs.sort(key=lambda x: x[2])

        current_adjusted = set()
        for i, j, current_dist in nearby_pairs:
            if i in adjusted_indices and j in adjusted_indices:
                continue

            direction = positions[j] - positions[i]
            direction /= np.linalg.norm(direction)
            move_dist = direction * (MARGIN + min_distance - current_dist) / 2
            axis_dist = MARGIN * math.copysign(1, direction[2]) * (1.5 - current_dist / min_distance) / 2

            positions[i] -= move_dist
            positions[i][2] -= axis_dist
            current_adjusted.add(i)
            positions[j] += move_dist
            positions[j][2] += axis_dist
            current_adjusted.add(j)

        if not current_adjusted:
            break

        adjusted_indices.update(current_adjusted)

    for idx in adjusted_indices:
        objects[idx].location = positions[idx]
        objects[idx].keyframe_insert(data_path="location", frame=bpy.context.scene.frame_current)

    return len(adjusted_indices)

def create_drone_animation(start_frame, end_frame, min_distance, frame_interval):
    if frame_interval < 1:
        raise ValueError("帧间隔必须大于或等于1")

    total_adjusted = 0
    frame_range = range(start_frame + frame_interval, end_frame, frame_interval)
    total_frames = len(frame_range)
    frames_processed = 0

    for frame in frame_range:
        bpy.context.scene.frame_set(frame)
        adjusted = adjust_object_positions(Collections.find_drones(create=False).objects, min_distance)
        total_adjusted += adjusted
        frames_processed += 1
        progress = (frames_processed / total_frames) * 100
        print(f"\r  处理进度: {frames_processed}/{total_frames} 帧 ({progress:.1f}%), 当前帧: {frame}, 调整物体数量: {total_adjusted}", end="")
    print()

    return total_adjusted

def create_dynamic_drone_animation(start_frame, end_frame, safety_dist, adjust_rate):
    if start_frame >= end_frame:
        raise ValueError("起始帧必须小于结束帧")

    print(f"参数设置: 起始帧={start_frame}, 结束帧={end_frame}, 安全距离={safety_dist:.02f}")

    iteration = total_adjusted = no_adjust_count = 0
    frame_interval = 1 if adjust_rate == 1 else math.ceil((end_frame - start_frame) / 4.0)

    while True:
        iteration += 1
        print(f"\n迭代 {iteration}: 帧间隔={frame_interval}")
        adjusted = create_drone_animation(start_frame, end_frame, safety_dist, frame_interval)
        no_adjust_count = 0 if adjusted else no_adjust_count + 1
        if (frame_interval == 1 and adjusted == 0) or no_adjust_count >= 3:
            break
        total_adjusted += adjusted
        if  frame_interval > 1:
            frame_interval = math.floor(frame_interval * adjust_rate)

    print(f"\n调整完成，累计调整物体数量: {total_adjusted}")
    return total_adjusted

class SkybrushCalculateSafePathOperator(Operator):
    bl_idname = "skybrush.calculate_safe_path"
    bl_label = "Calculate safe path"
    bl_description = (
        "Over-calculation safe path for range intervals"
    )
    bl_options = {"REGISTER", "UNDO"}

    start_frame = IntProperty(
        name="Start frame",
        description="The start frame of the range interval",
        min=1
    )

    end_frame = IntProperty(
        name="End frame",
        description="End frame of the range",
        min=1
    )

    safety_dist=FloatProperty(
        name="Safety distance",
        description="Safety distance",
        default=2.6,
        min=1,
        soft_min=2.5,
        soft_max=3.0,
    )

    adjust_rate=FloatProperty(
        name="Adjust rate",
        description="Adjust rate",
        default=0.9,
        min=0.1,
        max=1.0,
    )

    def invoke(self, context, event):
        self.start_frame = context.scene.frame_start
        self.end_frame = context.scene.frame_end
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        try:
            start = time.time()
            with ConsoleWindow():
                total_adjusted = create_dynamic_drone_animation(
                    self.start_frame, self.end_frame, self.safety_dist, self.adjust_rate)
            self.report({"INFO"}, f"总计耗时 {time.time() - start:.2f} 秒，添加 {total_adjusted} 个关键帧")
            return {"FINISHED"}
        except Exception as e:
            self.report({"ERROR"}, f"异常: {e}")
            return {"CANCELLED"}
