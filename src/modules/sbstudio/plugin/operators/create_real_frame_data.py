import bpy
import mathutils
import re
import math

from bpy.ops import skybrush
from bpy.props import BoolProperty, StringProperty, FloatProperty, IntProperty
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
    "SkybrushCreateRealFrameDataOperator",
    "SkybrushCalculatePathOperator",
    "SkybrushClearPathOperator",
    "SkybrushInsertKeyframePathOperator",
    "SkybrushClearKeyframePathOperator",
    "SkybrushCalculatePathAverageOperator",
    "SkybrushCalculateGroupTakeoffOperator",
    "SkybrushRecalculateGroupTakeoffOperator",
)

PATTERN = "Drone \d+$"

def get_all_drones():
    objects = []
    for obj in bpy.data.objects:
        if re.search(PATTERN, obj.name):
            objects.append(obj)
    return objects


class SkybrushRecalculateGroupTakeoffOperator(bpy.types.Operator):
    bl_idname = 'skybrush.recalculate_group_takeoff'
    bl_label = 'Recalculate group takeoff path'
    bl_description = 'Recalculate group takeoff path with staggered takeoff for each group'
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

    def invoke(self, context, event):
        self.frame = context.scene.frame_current
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        skybrush.redistribution_takeoff_grid(rows=self.rows, columns=self.columns, spacing=self.spacing)
        skybrush.calculate_group_takeoff(rows=self.rows, columns=self.columns, dryrun=True)

        points, target_frame = [], context.scene.frame_end + 100
        context.scene.frame_set(self.frame)
        for drone in Collections.find_drones(create=False).objects:
            points.append(drone.location)
            drone.keyframe_insert(data_path="location", frame=target_frame)
        create_formation("group target", points)

        storyboard = bpy.data.scenes["Scene"].skybrush.storyboard
        bpy.data.scenes["Scene"].skybrush.formations.selected = bpy.data.collections["group target"]
        skybrush.append_formation_to_storyboard()
        storyboard.active_entry.frame_start = target_frame
        bpy.data.scenes["Scene"].skybrush.formations.selected = bpy.data.collections["group takeoff"]
        skybrush.append_formation_to_storyboard()
        storyboard.active_entry.frame_start = target_frame + 500
        skybrush.recalculate_transitions(scope='TO_SELECTED')

        context.scene.frame_set(target_frame + 500)
        for drone in Collections.find_drones(create=False).objects:
            drone.location = mathutils.Vector(get_position_of_object(drone))
            drone.location.z = 0
            drone.keyframe_insert(data_path="location", frame=1)
        skybrush.calculate_group_takeoff(rows=self.rows, columns=self.columns, spacing=self.spacing)

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
        soft_min=0,
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
        for obj in bpy.data.objects:
            if re.search(PATTERN, obj.name):
                x = obj.matrix_world.to_translation().x
                y = obj.matrix_world.to_translation().y
                z = obj.matrix_world.to_translation().z
                if self.spacing:
                    di = int(y / self.spacing + 0.5) * self.columns + int(x / self.spacing + 0.5) + 1
                else:
                    di = int(re.search("\d+$", obj.name).group())
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
