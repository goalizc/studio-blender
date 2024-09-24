from mathutils import Vector

from bpy.props import FloatProperty, IntProperty
from bpy.types import Operator, Context
from sbstudio.plugin.constants import Collections

__all__ = ("RedistributionTakeoffGridOperator",)

class RedistributionTakeoffGridOperator(Operator):
    bl_idname = "skybrush.redistribution_takeoff_grid"
    bl_label = "Redistribution Takeoff Grid"
    bl_description = "Redistribution the takeoff grid and the corresponding set of drones"
    bl_options = {"REGISTER", "UNDO"}

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

    @classmethod
    def poll(cls, context: Context):
        drones = Collections.find_drones(create=False)
        return drones is not None and len(drones.objects) > 0

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        drones = Collections.find_drones().objects.items()
        drones.sort(key=lambda a: int(a[0][6:]))
        drones = [item[1] for item in drones]

        for i in range(self.columns):
            for j in range(self.rows):
                drone = drones[j * self.columns + i]
                drone.location = Vector((i * self.spacing, j * self.spacing, 0))
                drone.keyframe_insert(data_path="location", frame=1)

        context.scene.frame_set(1)

        return {"FINISHED"}
