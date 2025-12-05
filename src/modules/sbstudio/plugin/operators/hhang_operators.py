import bpy
import itertools
import math
import mathutils
import numpy as np
import re, time

from bpy.ops import skybrush
from bpy.props import BoolProperty, StringProperty, FloatProperty, IntProperty
from bpy_extras.io_utils import ImportHelper
from sbstudio.plugin.objects import remove_objects
from sbstudio.plugin.actions import (
    find_all_f_curves_for_data_path,
    find_f_curve_for_data_path,
)
from sbstudio.plugin.constants import Collections
from sbstudio.plugin.utils.evaluator import get_position_of_object
from sbstudio.plugin.model.formation import create_formation
from sbstudio.api.console import ConsoleWindow
from sbstudio.plugin.utils.transition import is_transition_constraint
from .utils import check_distance, check_trajectory
__all__ = (
    "SkybrushAddCurrentFrameToExportFrameDataOperator",
    "SkybrushCalculateGroupLandOperator",
    "SkybrushCalculateGroupTakeoffOperator",
    "SkybrushNebulaOperator",
    "SkybrushRecalculateGroupTakeoffOperator",
    "SkybrushReplaceCopyLocationConstraintOperator",
    "SkybrushSelectFileOperator",
)

class SkybrushSelectFileOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "skybrush.select_file"
    bl_label = 'Select file'
    name: StringProperty(options={"HIDDEN"})
    filter_glob: StringProperty(options={"HIDDEN"})
    def execute(self, context):
        if not self.name:
            context.scene.skybrush.settings.filepath = self.filepath
        elif hasattr(context.scene.skybrush.settings, self.name):
            setattr(context.scene.skybrush.settings, self.name, self.filepath)
        return {"FINISHED"}

class SkybrushRecalculateGroupTakeoffOperator(bpy.types.Operator):
    bl_idname = 'skybrush.recalculate_group_takeoff'
    bl_label = 'Recalculate group takeoff path'
    bl_description = 'Recalculate group takeoff path with staggered takeoff for each group'
    bl_options = {'REGISTER', 'UNDO'}

    use_import = BoolProperty(
        name="Import from file",
        default=False,
        description="Import takeoff position data from file",
    )

    rows = IntProperty(
        name="Rows",
        description="Number of rows in the takeoff grid",
        default=10,
        soft_min=1,
        soft_max=100,
    )

    spacing = FloatProperty(
        name="Spacing",
        description="Spacing between the slots in the grid",
        default=3,
        soft_min=0,
        soft_max=50,
        unit="LENGTH",
    )

    frame = IntProperty(
        name="Frame",
        description="Keyframes that need to be transformed after takeoff",
    )

    distance = FloatProperty(
        name="Separation distance",
        description="The distance between drones on each layer",
        default=3,
        soft_min=1,
        soft_max=50,
        unit="LENGTH",
    )

    layer_height = FloatProperty(
        name="Layer height",
        description="Layer height between the layer in the grid",
        default=6,
        soft_min=5,
        soft_max=50,
        unit="LENGTH",
    )

    min_height = FloatProperty(
        name="Minimum Altitude",
        description="Minimum Altitude of the Bottom Layer",
        default=50,
        soft_min=0,
        soft_max=1000,
        unit="LENGTH",
    )

    offset_x = FloatProperty(
        name="Offset X",
        description="The offset distance on the x-axis",
        default=0,
        soft_min=-100,
        soft_max= 100,
        unit="LENGTH",
    )

    offset_y = FloatProperty(
        name="Offset Y",
        description="The offset distance on the y-axis",
        default=0,
        soft_min=-100,
        soft_max= 100,
        unit="LENGTH",
    )

    zoom_height = FloatProperty(
        name="Zoom Height",
        description="The altitude at which drones began to zoom",
        default=30,
        soft_min=10,
        soft_max=1000,
        unit="LENGTH",
    )

    zoom_ratio = FloatProperty(
        name="Zoom Ratio",
        description="The maximum ratio to which the drone can eventually zoom",
        default=1,
        soft_min=0,
        soft_max=1000,
    )

    velocity = FloatProperty(
        name="Velocity",
        description="Velocity",
        unit="VELOCITY",
        default=3.0,
    )

    def draw(self, context):
        self.layout.use_property_split= True
        self.layout.prop(self, "use_import")
        if self.use_import:
            row = self.layout.row()
            row.prop(context.scene.skybrush.settings, "filepath")
            sf = row.operator("skybrush.select_file", text="", icon="FILEBROWSER")
            sf.name = "filepath"
            sf.filter_glob = "*.json;*.txt"
        else:
            self.layout.prop(self, "rows")
            self.layout.prop(self, "spacing")
        self.layout.prop(self, "frame")
        self.layout.prop(self, "distance")
        self.layout.prop(self, "layer_height")
        self.layout.prop(self, "min_height")
        self.layout.prop(self, "offset_x")
        self.layout.prop(self, "offset_y")
        self.layout.prop(self, "zoom_height")
        self.layout.prop(self, "zoom_ratio")
        self.layout.prop(self, "velocity")

    def invoke(self, context, event):
        self.frame = context.scene.frame_current
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        drones = list(Collections.find_drones(create=False).objects)
        skybrush.redistribution_takeoff_grid(use_import=self.use_import,
                                             rows=self.rows, spacing=self.spacing)
        skybrush.calculate_group_takeoff(distance=self.distance, layer_height=self.layer_height,
                                         offset_x=self.offset_x, offset_y=self.offset_y,
                                         min_height=self.min_height, zoom_height=self.zoom_height,
                                         zoom_ratio=self.zoom_ratio, velocity=self.velocity, dryrun=True)

        points, target_frame = [], context.scene.frame_end + 100
        context.scene.frame_set(self.frame)
        for drone in drones:
            points.append(drone.location)
            drone.keyframe_insert(data_path="location", frame=target_frame)
        create_formation("group target", points)

        storyboard = bpy.data.scenes["Scene"].skybrush.storyboard
        bpy.data.scenes["Scene"].skybrush.formations.selected = bpy.data.collections["group target"]
        skybrush.append_formation_to_storyboard(dryrun=True)
        target_entry = storyboard.active_entry
        storyboard.active_entry.frame_start = target_frame
        bpy.data.scenes["Scene"].skybrush.formations.selected = bpy.data.collections["group takeoff"]
        skybrush.append_formation_to_storyboard(dryrun=True)
        storyboard.active_entry.frame_start = target_frame + 500
        skybrush.recalculate_transitions(scope='TO_SELECTED')

        context.scene.frame_set(target_frame + 500)
        points = np.array([get_position_of_object(drone) for drone in drones])
        center = np.mean(points, axis=0)
        points = (points - center) / self.zoom_ratio + center - np.array((self.offset_x, self.offset_y, 0))
        for drone, point in zip(drones, points):
            drone.location = mathutils.Vector((point[0], point[1], 0))
            drone.keyframe_insert(data_path="location", frame=1)
        skybrush.calculate_group_takeoff(distance=self.distance, layer_height=self.layer_height,
                                         offset_x=self.offset_x, offset_y=self.offset_y,
                                         min_height=self.min_height, zoom_height=self.zoom_height,
                                         zoom_ratio=self.zoom_ratio, velocity=self.velocity)

        self.remove_keyframe(drones, target_entry.frame_start)
        self.remove_keyframe(drones, target_entry.frame_end)
        self.remove_keyframe(drones, storyboard.active_entry.frame_start)
        self.remove_storyboard_entry("group target")
        self.remove_storyboard_entry("group takeoff")
        remove_objects(bpy.data.collections["group target"])
        remove_objects(bpy.data.collections["group takeoff"])

        return {"FINISHED"}

    def remove_storyboard_entry(self, name):
        try:
            storyboard = bpy.data.scenes["Scene"].skybrush.storyboard
            storyboard.active_entry = storyboard.entries[name]
            skybrush.remove_storyboard_entry()
        except Exception as e:
            print(e)
            self.report({"WARNING"}, f"未成功删除故事版条目: {name}")

    def remove_keyframe(self, drones, frame):
        for drone in drones:
            drone.keyframe_delete(data_path="location", frame=frame)
            for constraint in drone.constraints:
                constraint = f"constraints[{constraint.name!r}].influence".replace("'", '"')
                drone.keyframe_delete(data_path=constraint, frame=frame)


class SkybrushCalculateGroupTakeoffOperator(bpy.types.Operator):
    bl_idname = 'skybrush.calculate_group_takeoff'
    bl_label = 'Calculate group takeoff path'
    bl_description = 'Calculate group takeoff path with staggered takeoff for each group'
    bl_options = {'REGISTER', 'UNDO'}

    distance = FloatProperty(
        name="Separation distance",
        description="The distance between drones on each layer",
        default=3,
        soft_min=1,
        soft_max=50,
        unit="LENGTH",
    )

    layer_height = FloatProperty(
        name="Layer height",
        description="Layer height between the layer in the grid",
        default=6,
        soft_min=5,
        soft_max=50,
        unit="LENGTH",
    )

    min_height = FloatProperty(
        name="Minimum Altitude",
        description="Minimum Altitude of the Bottom Layer",
        default=50,
        soft_min=20,
        soft_max=1000,
        unit="LENGTH",
    )

    offset_x = FloatProperty(
        name="Offset X",
        description="The offset distance on the x-axis",
        default=0,
        soft_min=-100,
        soft_max= 100,
        unit="LENGTH",
    )

    offset_y = FloatProperty(
        name="Offset Y",
        description="The offset distance on the y-axis",
        default=0,
        soft_min=-100,
        soft_max= 100,
        unit="LENGTH",
    )

    zoom_height = FloatProperty(
        name="Zoom Height",
        description="The altitude at which drones began to zoom",
        default=30,
        soft_min=10,
        soft_max=1000,
        unit="LENGTH",
    )

    zoom_ratio = FloatProperty(
        name="Zoom Ratio",
        description="The maximum ratio to which the drone can eventually zoom",
        default=1,
        soft_min=0,
        soft_max=1000,
    )

    velocity = FloatProperty(
        name="Velocity",
        description="Velocity",
        unit="VELOCITY",
        default=3.0,
    )

    stay_altitude = FloatProperty(
        name="Stay altitude",
        description="The altitude at which the drone hovers upon connecting to the RTK system",
        default=5,
        soft_min=1,
        soft_max=20,
        unit='LENGTH',
        options={"HIDDEN"}
    )

    stay_time = FloatProperty(
        name="Stay time",
        description="The altitude at which the drone starts to land",
        default=5,
        soft_min=1,
        soft_max=20,
        unit='TIME_ABSOLUTE',
    )

    dryrun = BoolProperty(
        default=False,
        options={"HIDDEN"}
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        def cacl(a, b):
            a = np.array([get_position_of_object(obj) for obj in a]).round(decimals=3)
            b = np.array([get_position_of_object(obj) for obj in b]).round(decimals=3)
            c = b[:,None,:] - a
            d = np.min(np.sqrt(np.sum(c * c, axis=-1)), axis = 1)
            for i in np.argsort(d):
                if d[i] >= self.distance: return i
            return None

        self.zoom_height = max(self.stay_altitude, min(self.zoom_height, self.min_height))
        if  self.layer_height < self.stay_altitude:
            self.layer_height = self.stay_altitude
        if  self.velocity < 1:
            self.velocity = 1

        context.scene.frame_set(1)
        drones = list(Collections.find_drones(create=False).objects)
        center = np.mean([get_position_of_object(drone) for drone in drones], axis=0)
        drones.sort(key=lambda a: a.location.x * 10000 + a.location.y)
        groups = []
        while len(drones):
            group = [drones[0]]; del(drones[0])
            while len(drones):
                i = cacl(group, drones)
                if i is None:
                    break
                group.append(drones[i]); del(drones[i])
            groups.append(group)

        height = self.min_height + self.layer_height * len(groups)
        f, inc = 1, ((self.layer_height - self.stay_altitude) / self.velocity
                     + self.stay_altitude + self.stay_time) * context.scene.render.fps
        f1 = self.stay_altitude * context.scene.render.fps
        f2 = f1 + self.stay_time * context.scene.render.fps
        f3 = f2 + math.ceil((self.zoom_height - self.stay_altitude) * context.scene.render.fps / self.velocity)

        for group in groups:
            height -= self.layer_height
            fr = f; f += inc
            f4 = f2 + (height - self.stay_altitude) / self.velocity * context.scene.render.fps
            for drone in group:
                self.keyframe_insert(drone, "LINEAR", fr)
                drone.location[2] = self.stay_altitude
                self.keyframe_insert(drone, "LINEAR", math.ceil(fr + f1))
                self.keyframe_insert(drone, "LINEAR", math.ceil(fr + f2))
                if abs(1 - self.zoom_ratio) > 1e-2:
                    drone.location[2] = self.zoom_height
                    self.keyframe_insert(drone, ("BEZIER", "BEZIER", "LINEAR"), math.ceil(fr + f3))
                    drone.location[0] = (drone.location[0] - center[0]) * self.zoom_ratio + center[0]
                    drone.location[1] = (drone.location[1] - center[1]) * self.zoom_ratio + center[1]
                drone.location[0] += self.offset_x
                drone.location[1] += self.offset_y
                drone.location[2]  = height
                self.keyframe_insert(drone, "LINEAR", math.ceil(fr + f4))

        points, fstop = [], fr + f4 + context.scene.render.fps
        for drone in Collections.find_drones(create=False).objects:
            self.keyframe_insert(drone, "BEZIER", fstop)
            points.append(drone.location);

        if self.dryrun:
            create_formation("group takeoff", points)

        return {"FINISHED"}

    def keyframe_insert(self, drone, interpolation, frame):
        if not self.dryrun:
            drone.keyframe_insert(data_path="location", frame=frame)
            if type(interpolation) not in (list, tuple):
                interpolation = [interpolation] * 3
            self.set_interpolation(drone, frame, 0, interpolation[0])
            self.set_interpolation(drone, frame, 1, interpolation[1])
            self.set_interpolation(drone, frame, 2, interpolation[2])

    def set_interpolation(self, drone, frame, index, interpolation):
        kp = drone.animation_data.action.fcurves.find("location", index=index).keyframe_points
        for k in [k for k in kp if k.co[0] == frame]:
            k.interpolation = interpolation

class SkybrushCalculateGroupLandOperator(bpy.types.Operator):
    bl_idname = 'skybrush.calculate_group_land'
    bl_label = 'Calculate group land path'
    bl_description = 'Calculate group land path with staggered land for each group'
    bl_options = {'REGISTER', 'UNDO'}

    distance = FloatProperty(
        name="Separation distance",
        description="The distance between drones on each layer",
        default=3,
        soft_min=1,
        soft_max=50,
        unit="LENGTH",
    )

    layer_height = FloatProperty(
        name="Layer height",
        description="Layer height between the layer in the grid",
        default=6,
        soft_min=5,
        soft_max=50,
        unit="LENGTH",
    )

    min_height = FloatProperty(
        name="Minimum Altitude",
        description="Minimum Altitude of the Bottom Layer",
        default=50,
        soft_min=0,
        soft_max=1000,
        unit="LENGTH",
    )

    zoom_height = FloatProperty(
        name="Zoom Height",
        description="The altitude at which drones began to zoom",
        default=30,
        soft_min=10,
        soft_max=1000,
        unit="LENGTH",
    )

    zoom_ratio = FloatProperty(
        name="Zoom Ratio",
        description="The maximum ratio to which the drone can eventually zoom",
        default=1,
        soft_min=0,
        soft_max=1000,
    )

    landing_height = FloatProperty(
        name="Landing height",
        description="The altitude at which the drone starts to land",
        default=10,
        soft_min=1,
        soft_max=20,
        unit='LENGTH',
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        def set_interpolation(drone, frame, index, interpolation):
            kp = drone.animation_data.action.fcurves.find("location", index=index).keyframe_points
            for k in [k for k in kp if k.co[0] == frame]:
                k.interpolation = interpolation

        def keyframe_insert(drone, frame, interpolation="LINEAR"):
            drone.keyframe_insert(data_path="location", frame=frame)
            if type(interpolation) not in (list, tuple):
                interpolation = [interpolation] * 3
            set_interpolation(drone, frame, 0, interpolation[0])
            set_interpolation(drone, frame, 1, interpolation[1])
            set_interpolation(drone, frame, 2, interpolation[2])

        def cacl(a, b):
            a = np.array([get_position_of_object(obj) for obj in a])
            b = np.array([get_position_of_object(obj) for obj in b])
            c = b[:,None,:] - a
            d = np.min(np.sqrt(np.sum(c * c, axis=-1)), axis = 1)
            for i in np.argsort(d):
                if d[i] >= self.distance: return i
            return None

        if  self.layer_height > self.landing_height:
            self.layer_height = self.landing_height
        self.zoom_height = max(self.landing_height, min(self.zoom_height, self.min_height))

        context.scene.frame_set(1)
        drones, points = list(Collections.find_drones(create=False).objects), []
        center = np.mean([get_position_of_object(drone) for drone in drones], axis=0)
        height = self.min_height
        while len(drones):
            group = [drones[0]]; del(drones[0])
            while len(drones):
                i = cacl(group, drones)
                if i is None:
                    break
                group.append(drones[i]); del(drones[i])
            points += [(drone.location[0], drone.location[1], height) for drone in group]
            height += self.layer_height

        points = (np.array(points) - center) * (self.zoom_ratio, self.zoom_ratio, 1) + center
        storyboard = bpy.data.scenes["Scene"].skybrush.storyboard
        create_formation("group land", points.tolist())
        bpy.data.scenes["Scene"].skybrush.formations.selected = bpy.data.collections["group land"]
        skybrush.append_formation_to_storyboard()
        skybrush.recalculate_transitions(scope='TO_SELECTED')
        context.scene.frame_set(storyboard.active_entry.frame_start)
        bpy.data.scenes["Scene"].skybrush.hhang.frame_range = str(storyboard.active_entry.frame_start)
        skybrush.replace_copy_location_constraint()

        context.scene.frame_set(context.scene.frame_current + context.scene.render.fps)
        drones = list(Collections.find_drones(create=False).objects)
        for drone in drones:
            keyframe_insert(drone, context.scene.frame_current)

        fps, frame = context.scene.render.fps, context.scene.frame_current
        landframes, step = self.landing_height * fps, self.layer_height / 2 * fps
        height = self.min_height
        while len(drones):
            group = [drone for drone in drones if abs(get_position_of_object(drone)[2] - height) < 0.1]
            if not group:
                self.report({"ERROR"}, "无法获取正确高度，分组时出现错误")
                return {"CANCELLED"}
            zoom = (height - self.zoom_height) / 2 * fps
            landing = (height - self.landing_height) / 2 * fps
            for drone in group:
                keyframe_insert(drone, frame, ("BEZIER", "BEZIER", "LINEAR"))
                point = (np.array(drone.location) - center) / self.zoom_ratio + center
                drone.location = mathutils.Vector((point[0], point[1], self.zoom_height))
                keyframe_insert(drone, frame + zoom)
                drone.location[2] = self.landing_height
                keyframe_insert(drone, frame + landing)
                drone.location[2] = 0
                keyframe_insert(drone, frame + landing + landframes)
            height += self.layer_height
            frame  += step
            drones  = [drone for drone in drones if drone not in group]

        return {"FINISHED"}

class SkybrushNebulaOperator(bpy.types.Operator):
    bl_idname = 'skybrush.nebula'
    bl_label = 'Nebula'
    bl_description = 'Calculating nebula takeoff and landing'
    bl_options = {'REGISTER', 'UNDO'}

    takeoff_frame = IntProperty(
        name="Takeoff frame",
        description="The frame where the drone starts taking off",
        default=1,
        soft_min=1
    )

    shape_frame = IntProperty(
        name="Shape frame",
        description="The initial frame of the nebula taking flight"
    )

    distance = FloatProperty(
        name="Separation distance",
        description="The distance between drones on each layer",
        default=3,
        soft_min=1,
        soft_max=50,
        unit="LENGTH",
    )

    height = FloatProperty(
        name="Height",
        description="The height of the virtual landing position in the sky",
        default=50,
        soft_min=10,
        unit="LENGTH"
    )

    speed_change_height = FloatProperty(
        name="Speed change height",
        description="The drone will change speed when it reaches this altitude.",
        default=10,
        soft_min=1,
        soft_max=20,
        unit='LENGTH',
    )

    xy_velocity = FloatProperty(
        name="XY Velocity",
        description="Maximum speed of the plane to reach the virtual position in the air",
        default=10,
        unit="VELOCITY"
    )

    z_velocity = FloatProperty(
        name="Z Velocity",
        description="Maximum vertical speed to a virtual location in the air",
        default=2,
        unit="VELOCITY"
    )

    complexity = IntProperty(
        name="Complexity",
        default=20181213,
        min=1
    )

    takeoff = BoolProperty(
        name="Takeoff",
        default=False,
    )

    insitu = BoolProperty(
        name="In situ",
        default=False,
    )

    def draw(self, context):
        self.layout.use_property_split= True
        self.layout.prop(self, "takeoff_frame")
        self.layout.prop(self, "shape_frame")
        self.layout.prop(self, "distance")
        self.layout.prop(self, "height")
        self.layout.prop(self, "speed_change_height")
        self.layout.prop(self, "xy_velocity")
        self.layout.prop(self, "z_velocity")
        self.layout.prop(self, "complexity")
        row = self.layout.row()
        row.prop(self, "takeoff")
        row.prop(self, "insitu")

    def invoke(self, context, event):
        self.shape_frame = context.scene.frame_current
        if self.complexity == 20181213:
            self.complexity = int(len(Collections.find_drones(create=False).objects) * 0.1)
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        bezier_knots = np.array([(0, 0), (1/3, 0), (2/3, 1), (1, 1)])
        fps = context.scene.render.fps
        drones = list(Collections.find_drones(create=False).objects)
        context.scene.frame_set(self.takeoff_frame)
        targets = [(p[0], p[1], self.height) for p in [get_position_of_object(d) for d in drones]]
        context.scene.frame_set(self.shape_frame)
        shape = [get_position_of_object(d) for d in drones]
        distance_sq = self.distance ** 2

        landing, height = [], self.height
        if height > self.speed_change_height:
            landing.append((self.speed_change_height, math.ceil((height - self.speed_change_height) * fps / 2)))
            height = self.speed_change_height
        landing.append((0, math.ceil(height * fps)))

        def set_interpolation(drone, frame, index, interpolation):
            kp = drone.animation_data.action.fcurves.find("location", index=index).keyframe_points
            for k in [k for k in kp if k.co[0] == frame]:
                k.interpolation = interpolation

        def keyframe_insert(drone, frame, interpolation=("BEZIER", "BEZIER", "LINEAR")):
            drone.keyframe_insert(data_path="location", frame=frame)
            for i in range(3):
                set_interpolation(drone, frame, i, interpolation[i])

        def find_farthest_pair(drones_positions, targets):
            a = np.array(drones_positions)
            b = np.array(targets)
            i = np.min(np.sum((a - b[:,None,:]) ** 2, axis=-1), axis=1).argmax()
            return (np.argmin(((a - b[i]) ** 2).sum(-1)), i)

        def find_nearest(group, targets):
            a = np.array([t for _, t in group])
            b = np.array(targets)
            c = np.min(np.sqrt(np.sum((a - b[:,None,:]) ** 2, axis=-1)), axis=1)
            for i in np.argsort(c):
                if c[i] >= self.distance: return i
            return None

        def comb(n, k):
            return math.factorial(n) // (math.factorial(k) * math.factorial(n-k))

        def gen_point(p1, p2, t):
            b = sum(comb(3, i) * t**i * (1-t)**(3-i) * bezier_knots[i] for i in range(4))[1]
            return np.multiply(np.array(p2) - p1, (b, b, t)) + p1

        def gen_trajectory(p1, p2):
            trajectory = [p1]
            distance = np.sqrt((np.subtract(p1, p2) ** 2).sum())
            frames = math.ceil(max(distance * 1.5 / self.xy_velocity,
                                   abs(p1[2] - p2[2]) / self.z_velocity) * fps)
            trajectory.extend([gen_point(p1, p2, i) for i in np.linspace(0, 1, frames + 1)[1:]])
            for h, f in landing:
                diff = h - p2[2]
                trajectory.extend([(p2[0], p2[1], p2[2] + diff * i / f) for i in range(1, f + 1)])
                p2 = (p2[0], p2[1], h)
            return frames, np.array(trajectory, dtype=np.float64)

        def delay(frame_current, trajectory, runnings):
            for i in itertools.count(0):
                for traj in runnings:
                    if not check_trajectory(trajectory, traj, i, distance_sq):
                        break
                else:
                    return i

        if self.insitu:
            order = np.argsort((np.subtract(shape, np.mean(targets, axis=0)) ** 2).sum(-1))
            trajectories = [(drones[i], targets[i],
                             *gen_trajectory(get_position_of_object(drones[i]), targets[i]))
                                for i in order]
        else:
            groups = []
            while len(drones):
                si, ti = find_farthest_pair(shape, targets)
                group = [(drones[si], targets[ti])]
                del(drones[si]); del(shape[si]); del(targets[ti])
                while len(drones):
                    ti = find_nearest(group, targets)
                    if ti is None:
                        break
                    si = np.argmin(((np.array(shape) - targets[ti]) ** 2).sum(-1))
                    group.append((drones[si], targets[ti]))
                    del(drones[si]); del(shape[si]); del(targets[ti])
                groups.append(group)
            trajectories = [(drone, target, *gen_trajectory(get_position_of_object(drone), target))
                                for group in groups for drone, target in group]

        with ConsoleWindow():
            start, runnings, frame_current, total = time.time(), [], self.shape_frame, len(trajectories)
            move = (lambda f, n: f - n) if self.takeoff else (lambda f, n: f + n)
            while trajectories:
                N = np.inf
                for i in range(min(len(trajectories), self.complexity)):
                    traj = trajectories[i][3]
                    for j in range(len(trajectories)):
                        if i != j and not check_distance(traj, trajectories[j][3][0], distance_sq):
                            break
                    else:
                        if (n := delay(frame_current, traj, runnings)) < N and (N := n, I := i)[0] == 0:
                            break
                if N == np.inf:
                    N, I = delay(frame_current, trajectories[0][3], runnings), 0
                drone, target, frames, trajectory = trajectories[I]
                trajectories.pop(I)
                frame_current = move(frame_current, N)
                runnings = [t[N:] for t in runnings]
                runnings = [t for t in runnings if t.shape[0]] + [trajectory]
                keyframe_insert(drone, frame_current)
                drone.location, frame = target, move(frame_current, frames)
                keyframe_insert(drone, frame)
                for height, frames in landing:
                    drone.location[2], frame = height, move(frame, frames)
                    keyframe_insert(drone, frame)
                if self.takeoff:
                    keyframe_insert(drone, self.takeoff_frame)
                percent = (total-len(trajectories))*100/total
                print(f"\r星云[{self.complexity}]: 已用时{time.time() - start:.1f}s 进度{percent:.2f}%", end="")
            print()

        return {"FINISHED"}

class SkybrushAddCurrentFrameToExportFrameDataOperator(bpy.types.Operator):
    bl_idname = 'skybrush.add_current_frame_to_frame_range'
    bl_label = 'Add current frame to frame range'
    bl_description = 'Add current frame to frame range'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hhang = context.scene.skybrush.hhang
        if len(hhang.frame_range) and hhang.frame_range[-1] != '-':
            hhang.frame_range += ','
        hhang.frame_range += str(context.scene.frame_current)
        return {"FINISHED"}

class SkybrushReplaceCopyLocationConstraintOperator(bpy.types.Operator):
    bl_idname = 'skybrush.replace_copy_location_constraint'
    bl_label = 'Replace Copy Location Constraint'
    bl_description = 'Replace copy location constraint with visible location'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        frame_range = context.scene.skybrush.hhang.frame_range
        if not frame_range:
            self.report({"INFO"}, "帧范围为空")

        frame_current = context.scene.frame_current
        drones = Collections.find_drones(create=False).objects
        keyframes = {obj: [] for obj in drones}

        def prepare(frame):
            context.scene.frame_set(frame)
            for obj in drones:
                keyframes[obj].append((frame, get_position_of_object(obj)))

        try:
            for sub in frame_range.split(','):
                ret = self.parse(sub)
                if ret is None:
                    self.report({"ERROR"}, f"无效的帧范围格式：{sub}")
                    return {"CANCELLED"}
                mode, result = ret
                if mode == 1:
                    prepare(result)
                else:
                    start, end = result[:2]
                    if start > end:
                        start, end = end, start
                    for i in range(start, end + 1, 1 if mode == 2 else result[2]):
                        prepare(i)
                    if i != end:
                        prepare(end)
        finally:
            context.scene.frame_current = frame_current

        for obj, obj_keyframes in keyframes.items():
            for frame, location in obj_keyframes:
                obj.location = location
                obj.keyframe_insert(data_path="location", frame=frame)
        for obj in drones:
            for c in [c for c in obj.constraints if is_transition_constraint(c)]:
                obj.constraints.remove(c)

        return {"FINISHED"}

    def parse(self, text):
        pattern = r'^(?:(\d+)|(\d+)-(\d+)|(\d+)-(\d+):(\d+))$'
        match = re.match(pattern, text.strip())
        if not match:
            return None

        groups = match.groups()
        if groups[0] is not None:
            return 1, int(groups[0])
        if groups[1] is not None and groups[2] is not None:
            return 2, [int(groups[1]), int(groups[2])]
        if groups[3] is not None and groups[4] is not None and groups[5] is not None:
            return 3, [int(groups[3]), int(groups[4]), int(groups[5])]

        return None
