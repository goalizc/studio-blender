from bpy.types import Operator
from sbstudio.plugin.constants import Collections
from sbstudio.plugin.model.formation import get_world_coordinates_of_markers_from_formation

__all__ = ("SkybrushAdsorbOperator",)

class SkybrushAdsorbOperator(Operator):
    bl_idname = 'skybrush.adsorb'
    bl_label = 'Attach drone to formation'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.skybrush.formations.selected

    def execute(self, context):
        formation = get_world_coordinates_of_markers_from_formation(context.scene.skybrush.formations.selected)
        drones = Collections.find_drones(create=False).objects
        length = min(len(formation), len(drones))
        for point, drone in zip(formation[:length], drones[:length]):
            drone.location = point
        return {"FINISHED"}
