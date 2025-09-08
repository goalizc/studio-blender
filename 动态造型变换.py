import itertools, math, hashlib
import numpy as np
import bpy

from typing import cast
from bpy.types import CopyLocationConstraint
from scipy.spatial import distance_matrix
from scipy.optimize import linear_sum_assignment
from sbstudio.plugin.api import get_api
from sbstudio.plugin.constants import Collections
from sbstudio.plugin.utils.evaluator import get_position_of_object

### 这里是配置参数 ###############################################
shape = bpy.data.objects["柱体.003"]
delay = 5

safety_kwds = {
    "max_velocity_xy": 8.0,
    "max_velocity_z": 2.0,
    "max_velocity_z_up": 3.0,
    "max_acceleration": 0.0
}
##################################################################

def vertex_group(i):
    name = f"__Shape[{i}]"
    try:
        vertex_group = shape.vertex_groups[name]
    except KeyError:
        vertex_group = shape.vertex_groups.new(name=name)
    vertex_group.add([i], 1, "REPLACE")
    return vertex_group

def constraint_name(drone):
    return hashlib.md5(drone.name.encode()).hexdigest()

def remove_constraint_keyframes(drone, name=None):
    if drone.animation_data is None:
        return
    full_path = f'constraints["{name or constraint_name(drone)}"].influence'
    for fcurve in drone.animation_data.action.fcurves:
        if fcurve.data_path == full_path:
            drone.animation_data.action.fcurves.remove(fcurve)

def get_constraint(drone):
    expected_id = constraint_name(drone)
    for constraint in drone.constraints:
        if constraint.type == "COPY_LOCATION" and constraint.name == expected_id:
            return cast(CopyLocationConstraint, constraint)
    constraint = drone.constraints.new(type="COPY_LOCATION")
    constraint.name = expected_id
    return cast(CopyLocationConstraint, constraint)

def update_constraint(drone, vertex_group, fstart, fend):
    constraint = get_constraint(drone)
    constraint.target = shape
    constraint.subtarget = vertex_group.name
    constraint.influence = 0
    constraint.keyframe_insert(data_path="influence", frame=fstart)
    constraint.influence = 1
    constraint.keyframe_insert(data_path="influence", frame=fend)

context = bpy.context
context.scene.frame_set(context.scene.frame_start)
depsgraph = context.evaluated_depsgraph_get()
drones = [(d, get_position_of_object(d)) for d in Collections.find_drones(create=False).objects]
drones.sort(key=lambda p: p[1][2], reverse=True)
shape_indexes = set(range(len(shape.data.vertices)))
start = context.scene.frame_start

for drone, _ in drones:
    remove_constraint_keyframes(drone)
    get_constraint(drone).influence = 0

for i in itertools.count(context.scene.frame_start, 5):
    context.scene.frame_set(i)
    depsgraph.update()
    evaluated_shape = shape.evaluated_get(depsgraph)
    deformed_mesh = evaluated_shape.to_mesh()
    actived = []

    for index in shape_indexes:
        pos = evaluated_shape.matrix_world @ deformed_mesh.vertices[index].co
        if pos.z > drones[0][1][2]:
            actived.append((index, pos))

    if actived:
        print(i, len(actived), drones[0][1][2])
        source = [pos for drone, pos in drones]
        target = [pos for index, pos in actived]
        plan = get_api().plan_transition(source, target, **safety_kwds)
        duration = math.ceil(plan.total_duration * (10 or context.scene.render.fps))
        next_start = i - duration
        start = start + delay if next_start < start + delay else next_start
        for target_index, drone_index in enumerate(plan.mapping):
            update_constraint(drones[drone_index][0], vertex_group(actived[target_index][0]), next_start, i)
        for index, _ in actived:
            shape_indexes.remove(index)
        for i in sorted(plan.mapping, reverse=True):
            del drones[i]
        if not shape_indexes:
            break

context.scene.frame_set(context.scene.frame_start)
