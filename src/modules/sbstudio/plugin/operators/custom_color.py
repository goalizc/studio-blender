import bpy
from bpy.props import StringProperty
from sbstudio.plugin.materials import (
    get_material_for_led_light_color,
    create_keyframe_for_diffuse_color_of_material,
    get_led_light_color,
    set_led_light_color,
)
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
    "SkybrushYellowBlueCyanColorOperator",
    "SkybrushRedYellowPurpleColorOperator",
    "SkybrushPurpleBlueCyanColorOperator",
)

def create_keyframe_for_diffuse_color(color):
    objects = bpy.context.selected_objects
    active_frame = bpy.data.scenes['Scene'].frame_current
    for i in range(len(objects)):
        material = get_material_for_led_light_color(objects[i])
        if material:
            create_keyframe_for_diffuse_color_of_material(
                material, color, frame=active_frame
            )


class SkybrushRedColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.red_color'
    bl_label = '红 色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        color = (1, 0, 0, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushBlueColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.blue_color'
    bl_label = '蓝 色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        color = (0, 0, 1, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushYellowColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.yellow_color'
    bl_label = '黄 色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        color = (1, 1, 0, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}

class SkybrushGreenColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.green_color'
    bl_label = '绿 色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        color = (0, 1, 0, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushWhiteColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.white_color'
    bl_label = '白 色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        color = (1, 1, 1, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushBlackColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.black_color'
    bl_label = '黑 色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        color = (0, 0, 0, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushPinkColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.pink_color'
    bl_label = '粉 红'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        color = (1, 0.412, 0.706, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushSkyBlueColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.sky_blue_color'
    bl_label = '天 蓝'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        color = (0, 1, 1, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushPurpleColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.purple_color'
    bl_label = '紫 色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        color = (0.887923, 0, 1, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushOrangeColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.orange_color'
    bl_label = '橙 色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        color = (1, 0.549, 0.0, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushCyanColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.cyan_color'
    bl_label = '青 色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        color = (0.005181, 0.991102, 0.450786, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushVioletColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.violet_color'
    bl_label = '蓝紫色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        color = (0.181164, 0.002125, 0.964686, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushOrangeYellowColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.orange_yellow_color'
    bl_label = '橙黄色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        color = (1, 0.226966, 0.006512, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushPurplishRedColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.purplish_red_color'
    bl_label = '紫红色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        color = (1, 0.000303, 0.234551, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushBlueGreenColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.blue_green_color'
    bl_label = '蓝绿色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        color = (0.603827, 0.991102, 0.002732, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushBabyBlueColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.baby_blue_color'
    bl_label = '浅蓝色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        color = (0, 0.318547, 0.930111, 1)
        create_keyframe_for_diffuse_color(color)
        return {'FINISHED'}


class SkybrushRandomColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.random_color'
    bl_label = '随机色'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        a = [0, 1]
        objects = bpy.context.selected_objects
        active_frame = bpy.data.scenes['Scene'].frame_current
        for i in range(len(objects)):
            material = get_material_for_led_light_color(objects[i])
            if material:
                color = (random.choice(a), random.choice(a), random.choice(a), 1)
                while color == (0, 0, 0, 1):
                    color = (random.choice(a), random.choice(a), random.choice(a), 1)
                create_keyframe_for_diffuse_color_of_material(
                    material, color, frame=active_frame
                )
        return {'FINISHED'}


class SkybrushYellowBlueCyanColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.yellow_blue_cyan_color'
    bl_label = '黄兰青'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        a = [(0.991102, 0.938686, 0.000607, 1), (0.001518, 0.351533, 0.982251, 1), (0.003346, 0.991102, 0.502887, 1)]
        objects = bpy.context.selected_objects
        active_frame = bpy.data.scenes['Scene'].frame_current
        for i in range(len(objects)):
            material = get_material_for_led_light_color(objects[i])
            if material:
                color = random.choice(a)
                create_keyframe_for_diffuse_color_of_material(
                    material, color, frame=active_frame
                )
        return {'FINISHED'}


class SkybrushRedYellowPurpleColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.red_yellow_purple_color'
    bl_label = '红黄紫'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        a = [(1, 0.000607, 0.278894, 1), (0.991102, 0.938686, 0.000607, 1), (0.887923, 0, 1, 1)]
        objects = bpy.context.selected_objects
        active_frame = bpy.data.scenes['Scene'].frame_current
        for i in range(len(objects)):
            material = get_material_for_led_light_color(objects[i])
            if material:
                color = random.choice(a)
                create_keyframe_for_diffuse_color_of_material(
                    material, color, frame=active_frame
                )
        return {'FINISHED'}


class SkybrushPurpleBlueCyanColorOperator(bpy.types.Operator):
    bl_idname = 'skybrush.purple_blue_cyan_color'
    bl_label = '紫蓝青'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        a = [(0.887923, 0, 1, 1), (0.001821, 0, 1, 1), (0, 1, 0.938686, 1)]
        objects = bpy.context.selected_objects
        active_frame = bpy.data.scenes['Scene'].frame_current
        for i in range(len(objects)):
            material = get_material_for_led_light_color(objects[i])
            if material:
                color = random.choice(a)
                create_keyframe_for_diffuse_color_of_material(
                    material, color, frame=active_frame
                )
        return {'FINISHED'}


class SkybrushCloseMaterialChannelOperator(bpy.types.Operator):
    bl_idname = 'skybrush.close_material_channel'
    bl_label = '关闭材质通道'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for area in bpy.context.screen.areas:
            if area.type == 'DOPESHEET_EDITOR':
                space_data = area.spaces.active
                space_data.dopesheet.show_materials = False
                break
        else:
            space_data = None

        if space_data is not None:
            pass
        return {'FINISHED'}


class SkybrushCloseTransformChannelOperator(bpy.types.Operator):
    bl_idname = 'skybrush.close_transform_channel'
    bl_label = '关闭变换通道'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for area in bpy.context.screen.areas:
            if area.type == 'DOPESHEET_EDITOR':
                space_data = area.spaces.active
                space_data.dopesheet.show_transforms = False
                break
        else:
            space_data = None

        if space_data is not None:
            pass
        return {'FINISHED'}


class SkybrushOpenMaterialChannelOperator(bpy.types.Operator):
    bl_idname = 'skybrush.open_material_channel'
    bl_label = '开启材质通道'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for area in bpy.context.screen.areas:
            if area.type == 'DOPESHEET_EDITOR':
                space_data = area.spaces.active
                space_data.dopesheet.show_materials = True
                break
        else:
            space_data = None

        if space_data is not None:
            pass
        return {'FINISHED'}


class SkybrushOpenTransformChannelOperator(bpy.types.Operator):
    bl_idname = 'skybrush.open_transform_channel'
    bl_label = '开启变换通道'
    bl_description = 'pick the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for area in bpy.context.screen.areas:
            if area.type == 'DOPESHEET_EDITOR':
                space_data = area.spaces.active
                space_data.dopesheet.show_transforms = True
                break
        else:
            space_data = None

        if space_data is not None:
            pass
        return {'FINISHED'}
