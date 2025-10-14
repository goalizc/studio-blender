import bpy
import mathutils
import re
import json
import math
import numpy as np

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
from sbstudio.plugin.materials import (
    get_material_for_led_light_color,
    create_keyframe_for_diffuse_color_of_material,
    get_led_light_color,
    set_led_light_color,
)

__all__ = (
    "SkybrushAddCurrentFrameToExportFrameDataOperator",
    "SkybrushCreateRealFrameDataOperator",
    "SkybrushCalculatePathOperator",
    "SkybrushClearPathOperator",
    "SkybrushInsertKeyframePathOperator",
    "SkybrushClearKeyframePathOperator",
    "SkybrushCalculatePathAverageOperator",
    "SkybrushNewCalculateGroupTakeoffOperator",
    "SkybrushCalculateGroupTakeoffOperator",
    "SkybrushRecalculateGroupTakeoffOperator",
    "SkybrushStarfallOperator",
    "SkybrushSelectFileOperator",
)

PATTERN = r"Drone \d+$"

def get_all_drones():
    objects = []
    for obj in bpy.data.objects:
        if re.search(PATTERN, obj.name):
            objects.append(obj)
    return objects


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

    columns = IntProperty(
        name="Columns",
        description="Number of columns in the takeoff grid",
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
            self.layout.prop(self, "columns")
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
        if self.use_import:
            if not self.redistribution_takeoff_grid(drones, context.scene.skybrush.settings.filepath):
                return {"CANCELLED"}
        else:
            skybrush.redistribution_takeoff_grid(rows=self.rows, columns=self.columns, spacing=self.spacing)
        skybrush.new_calculate_group_takeoff(distance=self.distance, layer_height=self.layer_height,
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
        skybrush.new_calculate_group_takeoff(distance=self.distance, layer_height=self.layer_height,
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

    def redistribution_takeoff_grid(self, drones, filepath):
        try:
            points = json.loads(open(filepath).read())
        except Exception as e:
            print(e)
            self.report({"ERROR"}, f"文件错误: {filepath}")
            return False

        if len(points) != len(drones):
            self.report({"ERROR"}, "导入的位置数量不匹配无人机的数量")
            return False

        for point, drone in zip(points, drones):
            drone.location = mathutils.Vector((point[0], point[1], 0))
            drone.keyframe_insert(data_path="location", frame=1)

        return True

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


class SkybrushNewCalculateGroupTakeoffOperator(bpy.types.Operator):
    bl_idname = 'skybrush.new_calculate_group_takeoff'
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

class SkybrushNewCalculateGroupLandOperator(bpy.types.Operator):
    bl_idname = 'skybrush.new_calculate_group_land'
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
        bpy.data.scenes["Scene"].skybrush.hh_export.export_farme_data = str(storyboard.active_entry.frame_start)
        skybrush.create_real_frame_data()

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

class SkybrushStarfallOperator(bpy.types.Operator):
    bl_idname = 'skybrush.starfall'
    bl_label = 'Starfall'
    bl_description = 'Calculate starfall landing'
    bl_options = {'REGISTER', 'UNDO'}

    takeoff_frame = IntProperty(
        name="Takeoff frame",
        description="The frame where the drone starts taking off",
        default=1,
        min=1
    )

    shape_frame = IntProperty(
        name="Shape frame",
        description="The frame where the shape begin landing"
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

    landing_height = FloatProperty(
        name="Landing height",
        description="The altitude at which the drone starts to land",
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

    def invoke(self, context, event):
        self.shape_frame = context.scene.frame_current
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        bezier_knots = np.array([(0, 0), (1/3, 0), (2/3, 1), (1, 1)])
        fps = context.scene.render.fps
        drones = list(Collections.find_drones(create=False).objects)
        context.scene.frame_set(self.takeoff_frame)
        targets = [(p[0], p[1], self.height) for p in [get_position_of_object(d) for d in drones]]
        context.scene.frame_set(self.shape_frame)
        shape = [get_position_of_object(d) for d in drones]

        landing, height = [], self.height
        if height > self.landing_height:
            landing.append((self.landing_height, math.ceil((height - self.landing_height) * fps / 2)))
            height = self.landing_height
        landing.append((0, math.ceil(height * fps)))

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
            return frames, trajectory

        def check(arr1, arr2):
            n = min(len(arr1), len(arr2))
            arr1, arr2 = np.array(arr1[0:n]), np.array(arr2[0:n])
            return np.all(((arr1 - arr2) ** 2).sum(-1) > self.distance ** 2)

        def delay(frame_current, src, tgt, trajectory, runnings):
            while not np.all([check(trajectory, r[2]) for r in runnings if r[2]]):
                for r in runnings:
                    if r[2]: r[2].pop(0)
                frame_current = frame_current + 1
            return frame_current

        def set_interpolation(drone, frame, index, interpolation):
            kp = drone.animation_data.action.fcurves.find("location", index=index).keyframe_points
            for k in [k for k in kp if k.co[0] == frame]:
                k.interpolation = interpolation

        def keyframe_insert(drone, frame):
            drone.keyframe_insert(data_path="location", frame=frame)
            set_interpolation(drone, frame, 0, "BEZIER")
            set_interpolation(drone, frame, 1, "BEZIER")
            set_interpolation(drone, frame, 2, "LINEAR")

        def run(frame_current, drone, target, runnings):
            source = get_position_of_object(drone)
            frames, trajectory = gen_trajectory(source, target)
            frame_current = delay(frame_current, source, target, trajectory, runnings)
            keyframe_insert(drone, frame_current)
            drone.location, frame = target, frame_current + frames
            keyframe_insert(drone, frame)
            for height, frames in landing:
                drone.location[2] = height
                frame += frames
                keyframe_insert(drone, frame)
            return trajectory, frame_current

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

        runnings, frame_current = [], self.shape_frame
        for drone, target in [pair for group in groups for pair in group]:
            trajectory, frame_current = run(frame_current, drone, target, runnings)
            runnings.insert(0, (get_position_of_object(drone), target, trajectory))
            print(len(runnings), drone)

        return {"FINISHED"}

class SkybrushCalculateGroupTakeoffOperator(bpy.types.Operator):
    bl_idname = 'skybrush.calculate_group_takeoff'
    bl_label = 'Calculate group takeoff path'
    bl_description = 'Calculate group takeoff path with staggered takeoff for each group'
    bl_options = {'REGISTER', 'UNDO'}

    rows = IntProperty(
        name="Rows",
        description="Number of rows in the takeoff grid",
        default=10,
        soft_min=1,
        soft_max=100,
    )

    columns = IntProperty(
        name="Columns",
        description="Number of columns in the takeoff grid",
        default=10,
        soft_min=1,
        soft_max=100,
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

    spacing_drone = IntProperty(
        name="Spacing Between Drones",
        description="Spacing Between Aircraft Takeoff Count",
        default=2,
        soft_min=0,
        soft_max=100,
    )

    max_acceleration = FloatProperty(
        name="Max acceleration",
        description="Maximum acceleration allowed when planning the duration of transitions between fixed points",
        default=3,
        unit="ACCELERATION",
        min=0.1,
        soft_min=0.1,
        soft_max=20,
    )

    max_velocity = FloatProperty(
        name="Max velocity",
        description="Max velocity",
        unit="VELOCITY",
        default=3.0,
    )

    frames_per_second = IntProperty(
        name="fps",
        description="The frames per second (FPS) when calculating the path",
        default=12,
        options=set(),
    )

    dryrun = BoolProperty(
        default=False,
        options={"HIDDEN"}
    )

    spacing = FloatProperty(
        default=0,
        options={"HIDDEN"}
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
        # The code below is used to trigger the settings panel in the lower
        # left hand corner, see:
        #
        # https://blender.stackexchange.com/questions/191956/how-to-make-custom-create-options-panel-in-bottom-left
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        velocity = 0
        objects = {}
        locations = {}
        bpy.context.scene.frame_set(1)
        for obj in [item[1] for item in Collections.find_drones().objects.items()]:
            x = obj.matrix_world.to_translation().x
            y = obj.matrix_world.to_translation().y
            z = obj.matrix_world.to_translation().z
            if self.spacing:
                di = int(y / self.spacing + 0.5) + int(x / self.spacing + 0.5) * self.rows + 1
            else:
                di = int(re.search(r"\d+$", obj.name).group())
            objects[di] = obj
            locations[di] = [x, y, z]

        # 获取无人机分组
        groups = []
        for i in range(1, self.spacing_drone + 2):
            for j in range(1, self.spacing_drone + 2):
                didx = (i - 1) * self.rows + j
                group = []
                for index in range(didx, self.columns * self.rows, self.rows * (self.spacing_drone + 1)):
                    for row in range(0, self.rows - j + 1, self.spacing_drone + 1):
                        group.append(row + index)
                group = list(filter(lambda i: i in objects.keys(), group))
                groups.append(group)



        # self.layer_height = velocity * t1 + 0.5 * self.max_acceleration * t1 * t1 + self.max_velocity * t2
        # self.max_velocity = velocity +  self.max_acceleration * t1
        t1 = (self.max_velocity - velocity) / self.max_acceleration # 加速消耗的时间
        s1 = velocity * t1 + 0.5 * self.max_acceleration * t1 * t1
        s2 = self.layer_height - s1
        t2 = 0
        if s2 > 0:
            t2 = s2 / self.max_velocity # 匀速消耗的时间
        else:
            s1 = self.layer_height
            t1 = math.sqrt(s1 / self.max_acceleration)



        tframe1 = t1 * self.frames_per_second
        tframe2 = (t1 + t2) * self.frames_per_second

        points = []
        groups_len = len(groups)
        for i in range(groups_len):
            group = groups[i]
            frame1 = i * tframe2
            frame2 = i * tframe2 + tframe1
            frame3 = (i + 1) * tframe2
            z = self.min_height + (groups_len - i - 1) * self.layer_height
            t3 = (z - self.layer_height) / self.max_velocity
            tframe3 = t3 * self.frames_per_second
            frame4 = frame3 + tframe3
            for j in range(len(group)):
                di = group[j]
                locations[di][2] = 0
                if not self.dryrun:
                    objects[di].keyframe_insert(data_path="location", frame= 1)
                    objects[di].keyframe_insert(data_path="location", frame= frame1)

                locations[di][2] = s1
                objects[di].location = locations[di]
                if not self.dryrun:
                    objects[di].keyframe_insert(data_path="location", frame= frame2)

                locations[di][2] = self.layer_height
                objects[di].location = locations[di]
                if not self.dryrun:
                    objects[di].keyframe_insert(data_path="location", frame= frame3)

                locations[di][2] = z
                objects[di].location = locations[di]
                if not self.dryrun:
                    objects[di].keyframe_insert(data_path="location", frame= frame4)

                points.append(objects[di].location)
        if self.dryrun:
            create_formation("group takeoff", points)

        self.report({"INFO"}, "Create successful")
        return {"FINISHED"}

class SkybrushAddCurrentFrameToExportFrameDataOperator(bpy.types.Operator):
    bl_idname = 'skybrush.add_current_frame_to_export_frame_data'
    bl_label = 'Add current frame to export frame data'
    bl_description = 'Add current frame to export frame data'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hh_export = context.scene.skybrush.hh_export
        if len(hh_export.export_farme_data) and hh_export.export_farme_data[-1] != '-':
            hh_export.export_farme_data += ','
        hh_export.export_farme_data += str(context.scene.frame_current)
        return {"FINISHED"}

class SkybrushCreateRealFrameDataOperator(bpy.types.Operator):
    bl_idname = 'skybrush.create_real_frame_data'
    bl_label = 'Frame data'
    bl_description = 'Delete constraints and generate keyframe data for entities'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hh_export = context.scene.skybrush.hh_export
        export_farme_data = hh_export.export_farme_data
        export_farme_data_arr = []
        if len(export_farme_data) > 0:
            export_farme_data_arr = export_farme_data.split(",")

        objects = []
        frames = []
        saveframes = []
        obj_frame_data_dict = {}
        for obj in bpy.data.objects:
            if re.search(PATTERN, obj.name):
                obj_frame_data_dict[obj.name] = []
                objects.append(obj)

        # fcurves = find_all_f_curves_contains_data_path(objects[0], "constraints[")
        # for fcurve in fcurves:
        #     self.report({"INFO"}, "fcurve = " + str(fcurve))
        #     for point in fcurve.keyframe_points:
        #         frame = int(point.co[0])
        #         frames.append(frame)
        #         saveframes.append(frame)

        for frame_str in export_farme_data_arr:
            frame_arr = frame_str.split("-")
            if len(frame_arr) == 1:
                frame = int(frame_arr[0])
                if frame not in saveframes:
                    saveframes.append(frame)
            else:
                si = int(frame_arr[0])
                ei = int(frame_arr[1])
                for frame in range(si, ei):
                    if frame not in saveframes:
                        saveframes.append(frame)

        # self.report({"INFO"}, "saveframes = " + str(saveframes) + objects[0].name)
        sce = bpy.context.scene
        for frame in saveframes:
            sce.frame_set(frame)
            for obj in objects:
                pos = []
                x = obj.matrix_world.to_translation().x
                y = obj.matrix_world.to_translation().y
                z = obj.matrix_world.to_translation().z
                pos.append(frame)
                pos.append(x)
                pos.append(y)
                pos.append(z)
                obj_frame_data_dict[obj.name].append(pos)

        for obj in objects:
            for constraint in obj.constraints:
                keyframe_data_path = f"constraints[{constraint.name!r}].influence".replace("'", '"')
                self.report({"INFO"}, keyframe_data_path)
                for frame in frames:
                    obj.keyframe_delete(keyframe_data_path, frame = frame)
            obj.constraints.clear()
            obj_frame_data = obj_frame_data_dict[obj.name]
            for frame_data in obj_frame_data:
                obj.location = (frame_data[1], frame_data[2], frame_data[3])
                obj.keyframe_insert(data_path="location", frame=frame_data[0])

        self.report({"INFO"}, "Create successful")
        return {"FINISHED"}


def calculate_path(context, is_use_wait):
    hh_export = context.scene.skybrush.hh_export
    frame_start = hh_export.frame_start
    frame_end = hh_export.frame_end
    frame_distance = hh_export.frame_distance
    frames_per_second = hh_export.frames_per_second
    max_velocity = hh_export.frame_velocity
    objects = []
    save_frame_data_dict = {}
    obj_save_frame_data_dict = {}
    save_frame_data_dict[frame_start] = True
    save_frame_data_dict[frame_end] = True
    print("select objects")
    for obj in bpy.data.objects:
        if re.search(PATTERN, obj.name):
            obj_save_frame_data_dict[obj.name] = {}
            obj_save_frame_data_dict[obj.name][frame_start] = []
            obj_save_frame_data_dict[obj.name][frame_end] = []
            objects.append(obj)
            fcurve = find_f_curve_for_data_path(obj, "location")
            if fcurve is not None:
                for point in fcurve.keyframe_points:
                    frame = int(point.co[0])
                    if frame >= frame_start:
                        save_frame_data_dict[frame] = True
                        obj_save_frame_data_dict[obj.name][frame] = []

    print("cache keyframe")
    sce = bpy.context.scene
    for frame in save_frame_data_dict:
        if frame >= frame_start and frame <= frame_end:
            sce.frame_set(frame)
            if frame == frame_start:
                for obj in objects:
                    if frame in obj_save_frame_data_dict[obj.name]:
                        pos = obj_save_frame_data_dict[obj.name][frame]
                        x = obj.matrix_world.to_translation().x
                        y = obj.matrix_world.to_translation().y
                        z = obj.matrix_world.to_translation().z
                        pos.append(frame)
                        pos.append(mathutils.Vector((x,y,z)))
                        obj["current_location"] = (x,y,z)
            else:
                for obj in objects:
                    if frame in obj_save_frame_data_dict[obj.name]:
                        pos = obj_save_frame_data_dict[obj.name][frame]
                        x = obj.matrix_world.to_translation().x
                        y = obj.matrix_world.to_translation().y
                        z = obj.matrix_world.to_translation().z
                        pos.append(frame)
                        pos.append(mathutils.Vector((x, y, z)))

    # 一帧移动最大距离
    max_distance_per_frame = max_velocity / frames_per_second
    # 模拟运动
    for frame in range(frame_start, frame_end + 1):
        frame_position_key = "frame_positions" + str(frame)
        for obj in objects:
            location_arr = obj["current_location"]
            current_location = mathutils.Vector((location_arr[0],location_arr[1],location_arr[2]))
            target_position = current_location
            target_frame = frame
            for pos_frame in range(frame, frame_end + 1):
                if pos_frame in obj_save_frame_data_dict[obj.name]:
                    target_position = obj_save_frame_data_dict[obj.name][pos_frame][1]
                    target_frame = pos_frame
                    break


            # 计算方向
            offset_position = target_position - current_location
            direction = offset_position.normalized()
            distance = offset_position.length
            velocity = 0
            offset_frame = target_frame - frame

            if is_use_wait:
                # 计算最大速度移动
                if offset_frame > 1 and distance > max_distance_per_frame:
                    velocity = max_velocity
                else:
                    velocity = distance
            else:
                # 计算平均速度移动
                if offset_frame > 1:
                    velocity = distance / (offset_frame / frames_per_second)
                else:
                    velocity = distance

            if velocity > max_velocity:
                velocity = max_velocity

            check_fail = False
            # 检测碰撞
            for other_obj in objects:
                if obj != other_obj:
                    other_location_arr = other_obj["current_location"]
                    other_current_location = mathutils.Vector((other_location_arr[0],other_location_arr[1],other_location_arr[2]))

                    other_offset_position = current_location - other_current_location
                    other_distance = other_offset_position.length
                    if other_distance < frame_distance:
                        # 有碰撞，调整位置
                        avoid_direction = other_offset_position.normalized()
                        direction += avoid_direction
                        check_fail = True

            if check_fail:
                if is_use_wait:
                    # 不进行移动，相当于等待
                    direction -= offset_position.normalized()
                direction = direction.normalized()

            # 计算每帧移动的距离
            distance_per_frame = velocity / frames_per_second
            movement_vector = direction * distance_per_frame
            # print(str(frame) + "," + str(target_frame))
            # 移动物体
            current_location += movement_vector
            obj["current_location"] = current_location
            obj[frame_position_key] = current_location
        if frame % 10 == 0:
            print("frame " + str(frame))


class SkybrushCalculatePathAverageOperator(bpy.types.Operator):
    bl_idname = 'skybrush.calculate_average_path'
    bl_label = 'Calculate path (average velocity)'
    bl_description = 'Calculate path (average velocity)'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        calculate_path(context, False)
        self.report({"INFO"}, "Calculate successful")
        return {"FINISHED"}

class SkybrushCalculatePathOperator(bpy.types.Operator):
    bl_idname = 'skybrush.calculate_path'
    bl_label = 'Calculate path (waiting, maximum velocity)'
    bl_description = 'Calculate path (waiting, maximum velocity)'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        calculate_path(context, True)
        self.report({"INFO"}, "Calculate path successful")
        return {"FINISHED"}

class SkybrushClearPathOperator(bpy.types.Operator):
    bl_idname = 'skybrush.clear_path'
    bl_label = 'Clear path'
    bl_description = 'Clear path'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        frame_start = bpy.context.scene.frame_start
        frame_end = bpy.context.scene.frame_end
        for obj in bpy.data.objects:
            if re.search(PATTERN, obj.name):
                key = "frame_positions"
                if key in obj:
                    del obj[key]

                for f in range(frame_start, frame_end + 1):
                    key = "frame_positions" + str(f)
                    if key in obj:
                        del obj[key]
                key = "current_location"
                if key in obj:
                    del obj[key]


        self.report({"INFO"}, "Clear path successful")
        return {"FINISHED"}


class SkybrushInsertKeyframePathOperator(bpy.types.Operator):
    bl_idname = 'skybrush.insert_keyframe_path'
    bl_label = 'Insert path keyframe'
    bl_description = 'Insert path keyframe'
    bl_options = {'REGISTER', 'UNDO'}

    def insert(self, objects, frame):
        key = "frame_positions" + str(frame)
        for obj in objects:
            if key in obj:
                obj.location = obj[key]
                obj.keyframe_insert(data_path="location", frame=frame)

    def execute(self, context):
        hh_export = context.scene.skybrush.hh_export
        frame_start = hh_export.frame_start
        frame_end = hh_export.frame_end
        frame_interval = hh_export.frame_interval
        if frame_interval < 1:
            frame_interval = 1

        objects = []
        for obj in bpy.data.objects:
            if re.search(PATTERN, obj.name):
                objects.append(obj)

        for f in range(frame_start, frame_end, frame_interval):
            self.insert(objects, f)
            print("插入" + str(f))
        self.insert(objects, frame_end)



        self.report({"INFO"}, "Insert Keyframe successful")
        return {"FINISHED"}

class SkybrushClearKeyframePathOperator(bpy.types.Operator):
    bl_idname = 'skybrush.clear_keyframe_path'
    bl_label = 'Clear path keyframe'
    bl_description = 'Clear path keyframe'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hh_export = context.scene.skybrush.hh_export
        frame_start = hh_export.frame_start
        frame_end = hh_export.frame_end
        objects = get_all_drones()
        frames = []
        fcurve = find_f_curve_for_data_path(objects[0], "location")
        if fcurve is not None:
            for point in fcurve.keyframe_points:
                frame = int(point.co[0])
                if frame > frame_start and frame < frame_end:
                    frames.append(frame)

        for obj in objects:
            for frame in frames:
                obj.keyframe_delete("location", frame = frame)

        self.report({"INFO"}, "Clear Keyframe successful")
        return {"FINISHED"}
