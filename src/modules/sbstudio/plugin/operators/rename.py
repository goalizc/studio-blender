from bpy.types import Operator
from sbstudio.plugin.constants import Collections
from sbstudio.plugin.selection import get_selected_drones

__all__ = ("RenameOperator",)

class RenameOperator(Operator):
    bl_idname = "skybrush.rename"
    bl_label = "Rename"
    bl_description = "Rename the selected drone"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        drones = Collections.find_drones(create=False)
        return drones is not None and len(drones.objects) > 0

    def execute(self, context):
        alldrones = Collections.find_drones(create=False).objects
        index = self.start_index(alldrones)
        for drone in sorted(
            get_selected_drones() or alldrones,
            key=lambda obj: (obj.location.y, obj.location.x, obj.location.z)
        ):
            drone.name = f"Drone {index}"
            index += 1
        return {"FINISHED"}

    def start_index(self, alldrones):
        i, names = 1, set([d.name for d in alldrones])
        while f"Drone {i}" in names:
            i += 1
        return i
