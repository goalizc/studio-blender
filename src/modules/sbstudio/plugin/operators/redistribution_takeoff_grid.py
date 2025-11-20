import json
import mathutils

from mathutils import Vector

from bpy.props import BoolProperty, FloatProperty, IntProperty
from bpy.types import Operator, Context
from sbstudio.plugin.constants import Collections

__all__ = ("RedistributionTakeoffGridOperator",)

class RedistributionTakeoffGridOperator(Operator):
    bl_idname = "skybrush.redistribution_takeoff_grid"
    bl_label = "Redistribution Takeoff Grid"
    bl_description = "Redistribution the takeoff grid and the corresponding set of drones"
    bl_options = {"REGISTER", "UNDO"}

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

    @classmethod
    def poll(cls, context: Context):
        drones = Collections.find_drones(create=False)
        return drones is not None and len(drones.objects) > 0

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

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        drones = sorted(Collections.find_drones().objects.values(), key=lambda a: int(a.name[6:]))

        if self.use_import:
            try:
                filepath = context.scene.skybrush.settings.filepath
                points = json.loads(open(filepath).read())
            except Exception as e:
                print(e)
                self.report({"ERROR"}, f"文件错误: {filepath}")
                return {"CANCELLED"}

            if len(points) != len(drones):
                self.report({"ERROR"}, "导入的位置数量不匹配无人机的数量")
                return {"CANCELLED"}

            for point, drone in zip(points, drones):
                drone.location = mathutils.Vector((point[0], point[1], 0))
                drone.keyframe_insert(data_path="location", frame=1)
        else:
            for i in range(len(drones)):
                drone = drones[i]
                x, y = i // self.rows, i % self.rows
                drone.location = Vector((x * self.spacing, y * self.spacing, 0))
                drone.keyframe_insert(data_path="location", frame=1)

        context.scene.frame_set(1)

        return {"FINISHED"}
