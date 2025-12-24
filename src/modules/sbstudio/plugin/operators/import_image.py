import bmesh
import bpy
import math
import numpy as np
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

    binary = BoolProperty(
        name="Display binary image",
        default=False
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        image = bpy.data.images.load(self.filepath)
        width, height = image.size

        pixels = np.array(image.pixels).reshape(width * height, 4)
        if image.alpha_mode == 'STRAIGHT':
            pixels[:, :3] *= pixels[:, 3, np.newaxis]
        pixels = np.apply_along_axis(lambda c: (c[0] + c[1] + c[2]) / 3, 1, pixels)
        mean, threshold = np.mean(pixels), np.std(pixels) * self.threshold
        lower, upper = mean - threshold, mean + threshold
        pixels = np.array([lower < n < upper for n in pixels], dtype=np.bool_).reshape(height, width)

        try:
            if self.iterations:
                from scipy.ndimage import generate_binary_structure, binary_dilation
                structure = generate_binary_structure(2, 2 if self.structure == "DIR8" else 1)
                pixels = binary_dilation(pixels, structure=structure, iterations=self.iterations)
        except:
            padded = np.pad(pixels, 1, mode='edge')
            h_mask = (padded[1:-1, 0:-2] & padded[1:-1, 2:  ])
            v_mask = (padded[0:-2, 1:-1] & padded[2:  , 1:-1])
            d1mask = (padded[0:-2, 0:-2] & padded[2:  , 2:  ])
            d2mask = (padded[0:-2, 2:  ] & padded[2:  , 0:-2])
            pixels = pixels | h_mask | v_mask | d1mask | d2mask

        if self.binary:
            gray = pixels.reshape(height, width)
            image.pixels = np.dstack((gray, gray, gray, np.ones_like(gray))).flatten()

        points = np.array([self.centroid(pixels, x, y) for y in range(height) for x in range(width) if not pixels[y, x]])
        dist_matrix = np.linalg.norm(points[:, np.newaxis] - points, axis=2)
        np.fill_diagonal(dist_matrix, np.inf)
        scale = self.min_distance / np.min(dist_matrix)
        filename, ext = os.path.splitext(os.path.basename(self.filepath))

        bm = bmesh.new()
        for coord in points:
            bm.verts.new((coord[0] * scale, 0, coord[1] * scale))
        mesh = bpy.data.meshes.new("mesh_" + filename)
        bm.to_mesh(mesh)
        bm.free()

        mesh = bpy.data.objects.new(filename, mesh)
        empty = bpy.data.objects.new("image_" + filename, None)
        empty.empty_display_type = 'IMAGE'
        empty.data = image
        empty.empty_image_offset = (0, 0)
        empty.use_empty_image_alpha = True
        empty.color[3] = 0.25
        empty.rotation_euler[0] = math.pi / 2
        empty.scale = [width * scale] * 3

        bpy.context.scene.collection.objects.link(mesh)
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
        return np.average(points, 0) + (0.5, 0.5)
