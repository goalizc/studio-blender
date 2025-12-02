import bpy
from bpy.props import StringProperty
from sbstudio.plugin.colors import create_keyframe_for_color_of_drone
import random
__all__ = (
    "SkybrushRedColorOperator",
    "SkybrushBlueColorOperator",
    "SkybrushYellowColorOperator",
    "SkybrushGreenColorOperator",
    "SkybrushWhiteColorOperator",
    "SkybrushBlackColorOperator",
    "SkybrushPinkColorOperator",
    "SkybrushSkyBlueColorOperator",
    "SkybrushPurpleColorOperator",
    "SkybrushOrangeColorOperator",
    "SkybrushCyanColorOperator",
    "SkybrushVioletColorOperator",
    "SkybrushOrangeYellowColorOperator",
    "SkybrushPurplishRedColorOperator",
    "SkybrushBlueGreenColorOperator",
    "SkybrushBabyBlueColorOperator",
    "SkybrushRandomColorOperator",
    "SkybrushRandomBlueColorOperator",
    "SkybrushYellowBlueCyanColorOperator",
    "SkybrushRandomColorNoBlackOperator",
    "SkybrushRandomBlueColorNoBlackOperator",
)

def create_keyframe_for_diffuse_color(color):
    objects = bpy.context.selected_objects
    active_frame = bpy.data.scenes['Scene'].frame_current
    for i in range(len(objects)):
        create_keyframe_for_color_of_drone(objects[i], color, frame=active_frame)


class ShowCreateKeyframeFailedMessage(bpy.types.Operator):
    def execute(self, context):
        try:
            return self.noexcept_execute(context)
        except RuntimeError:
            bpy.ops.skybrush.show_message(
                "INVOKE_DEFAULT",
                message="颜色函数曲线不可设置关键帧，它们可能已被锁定",
                title="错误",
                icon='ERROR'
            )
            return {"CANCELLED"}


class SkybrushRedColorOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.red_color'
    bl_label = '红 色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        color = (1, 0, 0, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushBlueColorOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.blue_color'
    bl_label = '蓝 色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        color = (0, 0, 1, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushYellowColorOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.yellow_color'
    bl_label = '黄 色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        color = (1, 1, 0, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}

class SkybrushGreenColorOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.green_color'
    bl_label = '绿 色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        color = (0, 1, 0, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushWhiteColorOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.white_color'
    bl_label = '白 色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        color = (0.666, 0.666, 0.666, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushBlackColorOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.black_color'
    bl_label = '黑 色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        color = (0, 0, 0, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushPinkColorOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.pink_color'
    bl_label = '粉 红'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        color = (1, 0.412, 0.706, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushSkyBlueColorOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.sky_blue_color'
    bl_label = '天 蓝'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        color = (0, 1, 1, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushPurpleColorOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.purple_color'
    bl_label = '紫 色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        color = (0.887923, 0, 1, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushOrangeColorOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.orange_color'
    bl_label = '橙 色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        color = (1, 0.549, 0.0, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushCyanColorOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.cyan_color'
    bl_label = '青 色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        color = (0.005181, 0.991102, 0.450786, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushVioletColorOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.violet_color'
    bl_label = '蓝紫色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        color = (0.181164, 0.002125, 0.964686, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushOrangeYellowColorOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.orange_yellow_color'
    bl_label = '橙黄色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        color = (1, 0.226966, 0.006512, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushPurplishRedColorOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.purplish_red_color'
    bl_label = '紫红色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        color = (1, 0.000303, 0.234551, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushBlueGreenColorOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.blue_green_color'
    bl_label = '蓝绿色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        color = (0.603827, 0.991102, 0.002732, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushBabyBlueColorOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.baby_blue_color'
    bl_label = '浅蓝色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        color = (0, 0.318547, 0.930111, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushRandomColorOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.random_color'
    bl_label = '随机色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        a = [0, 1]
        objects = bpy.context.selected_objects
        random.shuffle(objects)
        split = int(len(objects) * 0.6)
        active_frame = bpy.data.scenes['Scene'].frame_current
        for obj in objects[:split]:
            create_keyframe_for_color_of_drone(obj, (0, 0, 0, 1), frame=active_frame)
        for obj in objects[split:]:
            color = (random.choice(a), random.choice(a), random.choice(a), 1)
            while color == (0, 0, 0, 1):
                color = (random.choice(a), random.choice(a), random.choice(a), 1)
            create_keyframe_for_color_of_drone(obj, color, frame=active_frame)
        return {'FINISHED'}


class SkybrushRandomBlueColorOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.random_blue_color'
    bl_label = '随机蓝色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        a = [(0, 0, 1, 1), (0, 1, 1, 1), (0.005181, 0.991102, 0.450786, 1), (0, 0.318547, 0.930111, 1)]
        objects = bpy.context.selected_objects
        random.shuffle(objects)
        split = int(len(objects) * 0.6)
        active_frame = bpy.data.scenes['Scene'].frame_current
        for obj in objects[:split]:
            create_keyframe_for_color_of_drone(obj, (0, 0, 0, 1), frame=active_frame)
        for obj in objects[split:]:
            create_keyframe_for_color_of_drone(obj, random.choice(a), frame=active_frame)
        return {'FINISHED'}


class SkybrushYellowBlueCyanColorOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.yellow_blue_cyan_color'
    bl_label = '黄兰青'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        a = [(0.991102, 0.938686, 0.000607, 1), (0.001518, 0.351533, 0.982251, 1), (0.003346, 0.991102, 0.502887, 1)]
        objects = bpy.context.selected_objects
        active_frame = bpy.data.scenes['Scene'].frame_current
        for i in range(len(objects)):
            create_keyframe_for_color_of_drone(objects[i], random.choice(a), frame=active_frame)
        return {'FINISHED'}


class SkybrushRandomColorNoBlackOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.random_color_no_black'
    bl_label = '随机色（无黑）'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        a = [0, 1]
        active_frame = bpy.data.scenes['Scene'].frame_current
        for obj in bpy.context.selected_objects:
            color = (random.choice(a), random.choice(a), random.choice(a), 1)
            while color == (0, 0, 0, 1):
                color = (random.choice(a), random.choice(a), random.choice(a), 1)
            create_keyframe_for_color_of_drone(obj, color, frame=active_frame)
        return {'FINISHED'}


class SkybrushRandomBlueColorNoBlackOperator(ShowCreateKeyframeFailedMessage):
    bl_idname = 'skybrush.random_blue_color_no_black'
    bl_label = '随机蓝色（无黑）'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def noexcept_execute(self, context):
        a = [(0, 0, 1, 1), (0, 1, 1, 1), (0.005181, 0.991102, 0.450786, 1), (0, 0.318547, 0.930111, 1)]
        active_frame = bpy.data.scenes['Scene'].frame_current
        for obj in bpy.context.selected_objects:
            create_keyframe_for_color_of_drone(obj, random.choice(a), frame=active_frame)
        return {'FINISHED'}
