import bpy
from sbstudio.plugin.constants import Collections

drones = Collections.find_drones(create=False).objects

# --------------------------
# 请根据你的需求修改以下参数
# --------------------------
frame     = 12868     # 要设置关键帧的帧号（例如第50帧）
influence = 1.0       # 该帧的影响权重值（1.0=完全生效，0.0=完全失效）
parent    = "空物体"  # 仅处理指向该父对象的父子约束（留空则处理所有父子约束）
# --------------------------

for obj in drones:
    for constraint in obj.constraints:
        if constraint.type == 'CHILD_OF':
            if parent and (constraint.target is None or constraint.target.name != parent):
                continue

            bpy.context.scene.frame_set(frame)
            constraint.influence = influence
            constraint.keyframe_insert(data_path="influence", frame=frame)
