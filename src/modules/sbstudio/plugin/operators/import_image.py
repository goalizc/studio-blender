import bpy
import math
import numpy as np
from scipy import ndimage
import os

from bpy.props import BoolProperty, EnumProperty, IntProperty, FloatProperty, StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

__all__ = ("SkybrushHHImportImageOperator",)

class SkybrushHHImportImageOperator(Operator, ImportHelper):
    bl_idname = "export_scene.import_image"
    bl_label = "Import Image"
    bl_options = {"REGISTER"}

    filter_glob = StringProperty(
        default=";".join([f"*{ext}" for ext in bpy.path.extensions_image]),
        options={"HIDDEN"}
    )

    filepath = StringProperty(
        name="Path",
        description="Path of the imported image",
        default="",
        subtype='FILE_PATH',
        options={"HIDDEN"}
    )

    min_distance = FloatProperty(
        name="Minimum Import Distance",
        description="The minimum distance for imported image",
        unit="LENGTH",
        default=3.0,
        min=0.1,
    )

    threshold = FloatProperty(
        name="Background color threshold",
        default=1,
        min=0.01,
    )

    structure = EnumProperty(
        items=[("DIR8", "8 directions", ""), ("DIR4", "4 directions", "")],
        name="Structure",
        default="DIR8"
    )

    iterations = IntProperty(
        name="Inflation iteration count",
        default=1,
        min=0
    )

    adaptive = BoolProperty(
        name="Adaptive Algorithm",
        default=False
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        image = bpy.data.images.load(self.filepath)
        width, height = image.size

        pixels = np.asarray(image.pixels, dtype=np.float32).reshape(width * height, 4)
        img_gray = pixels[:, :3].mean(axis=1, dtype=np.float32)
        base, threshold = np.median(img_gray), img_gray.std() * self.threshold
        lower, upper = base - threshold, base + threshold
        pixels = np.logical_and(img_gray > lower, img_gray < upper).reshape(height, width)

        if self.adaptive:
            points = self.detect_dots_adaptive(~pixels)
        else:
            for _ in range(self.iterations):
                padded = np.pad(pixels, 1, mode='edge')
                neighbors = np.zeros_like(pixels, dtype=np.bool_)
                neighbors |= padded[1:-1, 0:-2] | padded[1:-1, 2:]
                neighbors |= padded[0:-2, 1:-1] | padded[2:, 1:-1]
                if self.structure == "DIR8":
                    neighbors |= padded[0:-2, 0:-2] | padded[0:-2, 2:] | padded[2:, 0:-2] | padded[2:, 2:]
                pixels |= neighbors
            points = np.array([self.centroid(pixels, x, y)
                for y in range(height) for x in range(width) if not pixels[y, x]])

        if len(points) > 1:
            dist_matrix = np.linalg.norm(points[:, np.newaxis] - points, axis=2)
            np.fill_diagonal(dist_matrix, np.inf)
            scale = self.min_distance / np.min(dist_matrix)
        else:
            scale = 1.0

        filename, ext = os.path.splitext(os.path.basename(self.filepath))

        mesh = bpy.data.meshes.new("mesh_" + filename)
        mesh.vertices.add(len(points))
        mesh.vertices.foreach_set("co", np.insert(points * scale, 1, 0, axis=1).flatten())
        bpy.context.scene.collection.objects.link(bpy.data.objects.new(filename, mesh))

        empty = bpy.data.objects.new("image_" + filename, None)
        empty.empty_display_type = 'IMAGE'
        empty.data = image
        empty.empty_image_offset = (0, 0)
        empty.use_empty_image_alpha = True
        empty.color[3] = 0.25
        empty.rotation_euler[0] = math.pi / 2
        empty.scale = [max(width, height) * scale] * 3
        collection = bpy.data.collections.get("图片")
        if collection is None:
            collection = bpy.data.collections.new("图片")
            bpy.context.scene.collection.children.link(collection)
        collection.objects.link(empty)

        return {'FINISHED'}

    @staticmethod
    def centroid(pixels, x, y):
        height, width = pixels.shape
        points = []
        def scan(points, x, y):
            P, X = [], x + 1
            while x >= 0 and not pixels[y, x]:
                P.append(x); pixels[y, x], x = True, x - 1
            while X < width and not pixels[y, X]:
                P.append(X); pixels[y, X], X = True, X + 1
            if y > 0:
                [pixels[y - 1, x] or scan(points, x, y - 1) for x in P]
            if y + 1 < height:
                [pixels[y + 1, x] or scan(points, x, y + 1) for x in P]
            points += [(x, y) for x in P]
        scan(points, x, y)
        return np.mean(points, axis=0) + 0.5

    @staticmethod
    def detect_dots_adaptive(binary):
        # 1. 标记所有独立的块（包括重叠的块）
        label_im, nb_labels = ndimage.label(binary)
        if nb_labels == 0:
            print("未检测到任何圆点")
            return []

        # 2. 计算所有块的面积，取中位数（中位数能有效排除重叠块和噪点的干扰）
        sizes = ndimage.sum(binary, label_im, range(1, nb_labels + 1))
        avg_area = np.median(sizes)
        # 面积 = pi * r^2  =>  直径 d = 2 * sqrt(area / pi)
        estimated_d = 2 * np.sqrt(avg_area / np.pi)
        print(f"自动估算的圆点直径约为: {estimated_d:.2f} 像素")

        # 3. 距离变换与平滑
        distance = ndimage.distance_transform_edt(binary)
        # 动态 sigma：设为直径的 1/8 左右
        sigma_val = estimated_d / 8
        smoothed_dist = ndimage.gaussian_filter(distance, sigma=sigma_val)

        # 4. 提取局部极大值
        # 动态 size：设为直径的 1/3，确保一个圆范围内只有一个峰值
        filter_size = int(estimated_d / 3)
        local_max = ndimage.maximum_filter(smoothed_dist, size=filter_size) == smoothed_dist
        local_max = local_max & (smoothed_dist > estimated_d * 0.2) # 过滤背景

        y_coords, x_coords = np.where(local_max)
        raw_centers = np.column_stack((x_coords, y_coords))

        # 5. 【坐标后处理】去重
        # 即使极大值过滤了，如果波峰是平坦的，仍可能产生相邻点
        def filter_close_points(coords, min_sep):
            final_coords = []
            temp_coords = list(coords)
            while len(temp_coords) > 0:
                p = temp_coords.pop(0)
                final_coords.append(p)
                # 移除所有离当前点太近的点
                temp_coords = [c for c in temp_coords if np.linalg.norm(c - p) > min_sep]
            return np.array(final_coords)

        # 最小间距设为直径的 1/3
        return filter_close_points(raw_centers, min_sep=estimated_d / 3)
