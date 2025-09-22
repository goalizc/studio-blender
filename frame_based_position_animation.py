import bpy
import math
import numpy as np
from sbstudio.plugin.utils.evaluator import get_position_of_object

# 获取Blender集合中的物体列表
def get_collection_objects(collection):
    if collection not in bpy.data.collections:
        raise ValueError(f"集合 '{collection}' 不存在")
    return bpy.data.collections[collection].objects

# 检测距离过近的物体对
def find_nearby_objects(positions, min_distance):
    num_objects = len(positions)
    distances = np.sqrt(((positions[:, np.newaxis] - positions)**2).sum(axis=2))
    # 创建上三角矩阵掩码，避免重复检查物体对
    upper_triangle_mask = np.triu(np.ones((num_objects, num_objects), dtype=bool), k=1)
    too_close = np.where((distances < min_distance - 1e-6) & upper_triangle_mask)
    return [(i, j, distances[i, j]) for i, j in zip(too_close[0], too_close[1])]

# 检查移动物体后是否会导致与其他物体距离过近
def check_object_movement_safety(positions, index_to_move, direction, move_dist, excluded_indices, min_distance):
    temp_positions = positions.copy()
    temp_positions[index_to_move] += direction * move_dist

    for k in range(len(temp_positions)):
        if k == index_to_move or k in excluded_indices:
            continue
        dist = np.linalg.norm(temp_positions[index_to_move] - temp_positions[k])
        if dist < min_distance - 1e-6:
            return False

    return True

# 调整物体位置以保持安全距离，返回调整的物体数量
def adjust_object_positions(objects, min_distance):
    positions = np.array([get_position_of_object(obj) for obj in objects], dtype=np.float64)
    adjusted_indices = set()
    max_iterations = 5

    # 迭代调整直到符合安全距离或达到最大迭代次数
    for _ in range(max_iterations):
        nearby_pairs = find_nearby_objects(positions, min_distance)
        if not nearby_pairs:
            break

        # 优先处理距离最近的物体对
        nearby_pairs.sort(key=lambda x: x[2])

        current_adjusted = set()
        for i, j, current_dist in nearby_pairs:
            # 计算分离方向并单位化
            direction = positions[j] - positions[i]
            direction /= np.linalg.norm(direction)

            # 计算移动距离，确保物体分离足够距离
            move_dist = (min_distance - current_dist) + 1e-4  # 现在需要移动整个距离，因为只移动一个物体

            if check_object_movement_safety(positions, i, -direction, move_dist, [j], min_distance):
                # 移动物体i
                positions[i] -= direction * move_dist
                current_adjusted.add(i)
            else:
                # 移动物体j
                positions[j] += direction * move_dist
                current_adjusted.add(j)

        adjusted_indices.update(current_adjusted)

    # 应用调整并设置关键帧
    for idx in adjusted_indices:
        objects[idx].location = positions[idx]
        objects[idx].keyframe_insert(data_path="location", frame=bpy.context.scene.frame_current)

    return len(adjusted_indices)

# 创建无人机动画并确保安全距离
def create_drone_animation(collection, start_frame, end_frame, min_distance, frame_interval=1):
    if start_frame >= end_frame:
        raise ValueError("起始帧必须小于结束帧")
    if frame_interval < 1:
        raise ValueError("帧间隔必须大于或等于1")

    # 获取物体并检查初始状态
    drones = get_collection_objects(collection)
    if not drones:
        raise ValueError(f"集合 '{collection}' 中没有可动画的物体")

    # 验证起始帧安全距离
    bpy.context.scene.frame_set(start_frame)
    initial_positions = np.array([get_position_of_object(drone) for drone in drones], dtype=np.float64)
    if find_nearby_objects(initial_positions, min_distance):
        raise ValueError(f"起始帧 {start_frame} 中存在距离小于安全距离 {min_distance} 的物体")

    # 处理每一帧，保持安全距离
    total_adjusted = 0
    total_frames = len(range(start_frame + 1, end_frame, frame_interval))
    frames_processed = 0

    for frame in range(start_frame + 1, end_frame, frame_interval):
        bpy.context.scene.frame_set(frame)
        adjusted = adjust_object_positions(drones, min_distance)
        total_adjusted += adjusted
        frames_processed += 1

        # 每处理10帧或最后一帧时打印进度
        if frames_processed % 10 == 0 or frames_processed == total_frames:
            progress = (frames_processed / total_frames) * 100
            print(f"  处理进度: {frames_processed}/{total_frames} 帧 ({progress:.1f}%), 当前帧: {frame}, 调整物体数量: {adjusted}")

    return total_adjusted

# 使用动态帧间隔创建无人机动画
def create_dynamic_drone_animation(collection, start_frame, end_frame, min_safety_dist, max_safety_dist, adjust_rate=0.9):
    if min_safety_dist > max_safety_dist:
        raise ValueError("最小安全距离不能大于最大安全距离")

    total_adjusted = 0
    safety_dist = max_safety_dist
    frame_interval = (end_frame - start_frame) / 4.0
    no_adjust_count = 0
    iteration = 1

    print(f"开始动态调整无人机动画...")
    print(f"参数设置: 集合='{collection}', 起始帧={start_frame}, 结束帧={end_frame}, 最小安全距离={min_safety_dist}, 最大安全距离={max_safety_dist}")

    # 动态调整帧间隔和安全距离
    while frame_interval >= 1:
        print(f"\n迭代 {iteration}: 安全距离={safety_dist:.3f}, 帧间隔={math.ceil(frame_interval)}")
        adjusted = create_drone_animation(collection, start_frame, end_frame, safety_dist, math.ceil(frame_interval))
        total_adjusted += adjusted
        print(f"  本次迭代调整物体数量: {adjusted}")

        # 更新参数
        safety_dist = min_safety_dist + (safety_dist - min_safety_dist) * adjust_rate
        frame_interval *= adjust_rate
        no_adjust_count = 0 if adjusted else no_adjust_count + 1

        # 检查是否需要提前结束
        if no_adjust_count >= 3:
            print(f"  连续3次迭代无调整，提前结束动态优化")
            break

        iteration += 1

    print(f"\n动态调整完成，累计调整物体数量: {total_adjusted}")
    return total_adjusted

# 执行动画生成
if __name__ == "__main__":
    print("========= 无人机动画生成开始 =========")
    total_adjusted = create_dynamic_drone_animation(
        collection="Collection",
        start_frame=3093,
        end_frame=3873,
        min_safety_dist=2.5,
        max_safety_dist=2.9,
        adjust_rate=0.9
    )
    print(f"\n========= 无人机动画生成完成 =========")
