

import bpy
import os
import math
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from sbstudio.plugin.materials import (
    get_led_light_color,
)
from bpy.props import BoolProperty, StringProperty
import numpy as np
import bmesh
__all__ = ("SkybrushHHExportOperator", "SkybrushHHChoosePNGOperator", )


#线性颜色转gamma颜色
def linear_2_gamma(value: float) -> float:
    if value <= 0.0:
        return 0.0
    elif value <= 0.0031308:
        return 12.92 * value
    elif value < 1.0:
        return 1.055 * math.pow(value, 0.4166667) - 0.055
    else:
        return math.pow(value, 0.45454545)

#gamma颜色转线性颜色
def gamma_2_linear(value: float) -> float:
    if value <= 0.04045:
        return value / 12.92;
    elif value < 1.0:
        return math.pow((value + 0.055)/1.055, 2.4)
    else:
        return math.pow(value, 2.2)

def _to_int_255(value: float) -> int:
    value = linear_2_gamma(value)
    return max(0, min(255, int(value * 255 + 0.5)))

class Path_Save(object):
    def __init__(self,path,blend_obj, drone_name,frame_length,frame_rate,data_type):
        self.ob=blend_obj
        self.drone_name=drone_name
        self.file_path = path + "/H_" + drone_name+ '.fpath'
        self.file=None
        self.frame_length=frame_length
        self.frame_rate=frame_rate
        self.PathObject = {
            "name": "DroneShow",
            "author": "Mr Haixiang.Wu",
        }
        self.PathObject.setdefault('data', [])
        self.PathObject.setdefault('rgb', [])
        self.data_type = data_type

    def add_frame(self,frame, realframe):
        x = int(self.ob.matrix_world.to_translation().x * 100)
        y = int(self.ob.matrix_world.to_translation().y * 100)
        z = int(self.ob.matrix_world.to_translation().z * 100)

        # get color rgb
        r = 0
        g = 0
        b = 0

        if self.data_type == "bsdf_color":
            try:
                r = _to_int_255(self.ob.active_material.node_tree.nodes['Principled BSDF'].inputs[0].default_value[0])
                g = _to_int_255(self.ob.active_material.node_tree.nodes['Principled BSDF'].inputs[0].default_value[1])
                b = _to_int_255(self.ob.active_material.node_tree.nodes['Principled BSDF'].inputs[0].default_value[2])
            except Exception as e:
                try:
                    r = _to_int_255(self.ob.active_material.node_tree.nodes[1].inputs[0].default_value[0])
                    g = _to_int_255(self.ob.active_material.node_tree.nodes[1].inputs[0].default_value[1])
                    b = _to_int_255(self.ob.active_material.node_tree.nodes[1].inputs[0].default_value[2])
                except Exception as e1:
                    print(e1)
        elif self.data_type == "view_color":
            r = _to_int_255(self.ob.color[0])
            g = _to_int_255(self.ob.color[1])
            b = _to_int_255(self.ob.color[2])
        else:
            color = get_led_light_color(self.ob)
            r = _to_int_255(color[0])
            g = _to_int_255(color[1])
            b = _to_int_255(color[2])


        self.add_data([x, y, z,r,g,b,frame,realframe])

    def add_data(self, data):
        self.PathObject["data"].append(data)

    def write_file(self):
        print("start to save"+self.drone_name + " dance file")
        self.file = open(self.file_path, 'wb')
        self.file.write(self.frame_length.to_bytes(4, byteorder='little', signed=True))
        self.file.write(self.frame_rate.to_bytes(4, byteorder='little', signed=True))
        for [x,y,z,r,g,b,frame,realframe] in  self.PathObject["data"]:
            self.file.write((x).to_bytes(4, byteorder='little', signed=True))
            self.file.write((y).to_bytes(4, byteorder='little', signed=True))
            self.file.write((z).to_bytes(4, byteorder='little', signed=True))
            self.file.write((r).to_bytes(1, byteorder='little', signed=False))
            self.file.write((g).to_bytes(1, byteorder='little', signed=False))
            self.file.write((b).to_bytes(1, byteorder='little', signed=False))
            self.file.write((frame%255).to_bytes(1, byteorder='little', signed=False))
            print("name:" + self.drone_name + " realframe:" + str(realframe) + " frame:" + str(frame) + " frameindex:" + str(frame%255) + " x:" + str(x) + " y:" + str(y) + " z:" + str(z) + " r:" + str(r) + " g:" + str(g) + " b:" + str(b))
        print(self.drone_name+ " dacne file save complete!!")
        self.file.close()

    def write_file_test(self):
        print("start to save"+self.drone_name + " dance file")
        self.file = open(self.file_path, 'w')
        self.file.write("frame_length:" + str(self.frame_length) + "\n")
        self.file.write("frame_rate:" +  str(self.frame_rate) + "\n")
        for [x,y,z,r,g,b,frame,realframe] in  self.PathObject["data"]:
            self.file.write("name:" + self.drone_name + " realframe:" + str(realframe) + " frame:" + str(frame) + " frameindex:" + str(frame%255) + " x:" + str(x) + " y:" + str(y) + " z:" + str(z) + " r:" + str(r) + " g:" + str(g) + " b:" + str(b) + "\n")
        print(self.drone_name+ " dacne file save complete!!")
        self.file.close()


def get_drone_num(list_drone_objs, path, frame_length, data_type, is_export_name):
    num=0
    blender_frame_rate = bpy.context.scene.render.fps # blender framerate
    pre_drone_name = "Drone "
    if is_export_name:
        pre_drone_name = "drone_"

    if data_type == "view_color":
        pre_drone_name = ""

    for i in range(1, len(bpy.data.objects) + 1):
        drone_name=pre_drone_name + str(i)
        drone_fill_name=str(i).zfill(3)
        
        if drone_name in bpy.data.objects:
            blend_obj = bpy.data.objects[drone_name]
            path_obj=Path_Save(path,blend_obj,drone_fill_name,frame_length,blender_frame_rate,data_type)
            list_drone_objs.append(path_obj)
            num = num + 1
    print("get drone num:"+str(num))
    return  num



class SkybrushHHExportOperator(Operator, ExportHelper):
    
    bl_idname = "export_scene.skybrush_hh"
    bl_label = "Export"
    bl_options = {"REGISTER"}

    filename_ext = ""

    bsdf_color_data = BoolProperty(
        name="原理化BSDF颜色",
        default=False,
        description=(
            "选择后导出汉航基础色数据"
        ),
    )

    object_color_data = BoolProperty(
        name="视图颜色",
        default=False,
        description=(
            "选择后导出汉航视图色数据"
        ),
    )

    export_test = BoolProperty(
        name="测试导出",
        default=False,
        description=(
            "选择后导出汉航测试数据"
        ),
    )

    export_name = BoolProperty(
        name="使用drone_1格式",
        default=False,
        description=(
            "选择后导出drone_1,drone_2，否则使用Drone 1,Drone 2"
        ),
    )

    def execute(self, context):
        path, _ = os.path.splitext(self.filepath)
        try:
            os.mkdir(path)
        except OSError:
            print("Path folder found\n")
        else:
            print("Successfully created paths folder\n")
        frame_start = bpy.context.scene.frame_start
        frame_end = bpy.context.scene.frame_end
        list_drone_objs=[]
        data_type = "default_color"
        if self.bsdf_color_data:
            data_type = "bsdf_color"
        elif self.object_color_data:
            data_type = "view_color"

        number_of_uavs = get_drone_num(list_drone_objs, path, frame_end - frame_start + 1, data_type, self.export_name)  # 自动获取无人机的个数

        # iterate through frames
        for f in range(frame_start, frame_end + 1):
            bpy.context.scene.frame_set(f)
            print("scan frame :" + str(f))
            for drone in list_drone_objs:
                drone.add_frame(f - frame_start + 1, f)
        if self.export_test:
            for drone in list_drone_objs:
                drone.write_file_test()
        else:
            for drone in list_drone_objs:
                drone.write_file()
        print("Export successful")
        self.report({"INFO"}, "Export successful")
        return {"FINISHED"}

    def invoke(self, context, event):
        if not self.filepath:
            filepath = bpy.data.filepath or "Untitled"
            filepath, _ = os.path.splitext(filepath)
            self.filepath = filepath

        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


class SkybrushHHChoosePNGOperator(Operator, ExportHelper):
    """选择PNG图片"""
    bl_idname = "export_scene.choose_png"
    bl_label = "Choose PNG"
    bl_options = {"REGISTER"}
    filename_ext = ".png"
    filter_glob = StringProperty(
        default="*.png",
        options={'HIDDEN'}
    )

    def get_sqrt_distance(self, x1, y1, x2, y2):
        return (x2 - x1)**2 + (y2 - y1)**2

    def execute(self, context):
        # 在此处添加您想要执行的代码
        hh_export = context.scene.skybrush.hh_export
        hh_export.png_image_path = self.filepath
        image = bpy.data.images.load(self.filepath)

        # Get the width and height of the image
        point_min_dis = hh_export.png_min_distance
        sqrt_point_min_dis = point_min_dis * point_min_dis
        point_scale = 10;
        sqrt_point_scale = point_scale * point_scale
        width = image.size[0]
        height = image.size[1]
        dict_pos = {}

        pixels = np.array(image.pixels)
        pixels = pixels.reshape(image.size[1], image.size[0], 4)

        # Get the pixel colors
        for y in range(height):
            for x in range(width):
                # Get the RGBA color value at this pixel
                r, g, b, a = pixels[y, x]
                if a >= 1:
                    str_key = "%d_%d" % (x, y)
                    src_pos = [x, 0, y]
                    for key in dict_pos.keys():
                        key_arr = key.split("_")
                        if self.get_sqrt_distance(src_pos[0], src_pos[2], int(key_arr[0]), int(key_arr[1])) <= sqrt_point_scale:
                            str_key = key
                            break

                    if str_key not in dict_pos:
                        dict_pos[str_key] = []

                    dict_pos[str_key].append(src_pos)

        points = []
        for list_pos in dict_pos.values():
            list_pos_len = len(list_pos)
            src_pos = np.array(list_pos)
            src_pos = np.sum(src_pos, axis=0)
            src_pos = [x / list_pos_len for x in src_pos]
            points.append(src_pos)

        sqrt_min_dis = -1
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                sqrt_dis = self.get_sqrt_distance(points[i][0], points[i][2], points[j][0], points[j][2])
                if sqrt_dis < sqrt_min_dis or sqrt_min_dis < 0:
                    sqrt_min_dis = sqrt_dis


        pos_scale = math.sqrt(sqrt_point_min_dis / sqrt_min_dis)
        self.report({"INFO"}, "使用最小距离，缩放比例：" + str(pos_scale))

        filename, ext = os.path.splitext(os.path.basename(self.filepath))

        # 创建 bmesh 对象
        bm = bmesh.new()

        # 添加顶点到 bmesh 中
        for coord in points:
            bm.verts.new([x * pos_scale for x in coord])

        # 创建 mesh 对象，并将 bmesh 数据赋给它
        mesh = bpy.data.meshes.new("mesh_" + filename)
        bm.to_mesh(mesh)

        # 创建新的 mesh 数据块，并将 mesh 对象赋给它
        obj = bpy.data.objects.new(filename, mesh)
        bpy.context.scene.collection.objects.link(obj)

        self.report({"INFO"}, self.filepath + str(len(points)))
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
