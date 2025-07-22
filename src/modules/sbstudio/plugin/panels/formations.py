from bpy.types import Panel

from sbstudio.plugin.menus import GenerateMarkersMenu
from sbstudio.plugin.model.formation import count_markers_in_formation
from sbstudio.plugin.operators import (
    CreateFormationOperator,
    CreateTakeoffGridOperator,
    DeselectFormationOperator,
    GetFormationStatisticsOperator,
    LandOperator,
    RemoveFormationOperator,
    ReorderFormationMarkersOperator,
    ReturnToHomeOperator,
    SelectFormationOperator,
    TakeoffOperator,
    UpdateFormationOperator,
    AppendFormationToStoryboardOperator,
    RedistributionTakeoffGridOperator,
    RenameOperator,
    SkybrushNewCalculateGroupTakeoffOperator,
    SkybrushNewCalculateGroupLandOperator,
    SkybrushStarfallOperator,
    SkybrushAdsorbOperator,
    RunFullProximityCheckOperator,
)
from sbstudio.plugin.stats import get_drone_count

__all__ = ("FormationsPanel",)


class FormationsPanel(Panel):
    """Custom Blender panel that allows the user to create new formations or
    update existing ones.
    """

    bl_idname = "OBJECT_PT_skybrush_formations_panel"
    bl_label = "Formations"

    # The following three settings determine that the Formations panel gets
    # added to the sidebar of the 3D view
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Formations"

    @classmethod
    def poll(cls, context):
        return context.scene.skybrush.formations

    def draw(self, context):
        scene = context.scene
        formations = scene.skybrush.formations
        if not formations:
            return

        selected_formation = formations.selected
        layout = self.layout

        row = layout.row(align=True)
        row.operator(CreateTakeoffGridOperator.bl_idname, icon="ADD")
        row.operator(RenameOperator.bl_idname, text="", icon="EVENT_F2")
        layout.operator(RedistributionTakeoffGridOperator.bl_idname, icon="THREE_DOTS")

        row = layout.row(align=True)
        row.operator(SkybrushNewCalculateGroupTakeoffOperator.bl_idname, text="Takeoff", icon="TRIA_UP_BAR")
        row.operator(SkybrushNewCalculateGroupLandOperator.bl_idname, text="Land", icon="TRIA_DOWN_BAR")
        row.operator(SkybrushStarfallOperator.bl_idname, text="Starfall", icon="GEOMETRY_NODES")

        layout.separator()

        row = layout.row(align=True)
        row.prop(formations, "selected", text="")
        row.operator(CreateFormationOperator.bl_idname, icon="ADD", text="")
        row.operator(RemoveFormationOperator.bl_idname, icon="X", text="")

        row = layout.row(align=True)
        row.operator(SelectFormationOperator.bl_idname, text="Select")
        row.operator(DeselectFormationOperator.bl_idname, text="Deselect")
        row.operator(GetFormationStatisticsOperator.bl_idname, text="Stats")

        if selected_formation:
            num_drones = get_drone_count()
            num_markers = count_markers_in_formation(formations.selected)

            # 因为分组变换，所以不需要提示编队大小不匹配无人机数量
            # # If the number of markers in the formation is different from the
            # # number of drones, show a warning as we won't know what to do with
            # # the extra or missing drones
            # if num_markers != num_drones:
            #     row = layout.box()
            #     row.alert = False
            #     row.label(
            #         text=f"Formation size: {num_markers} "
            #         f"{'<' if num_markers < num_drones else '>'} "
            #         f"{num_drones}",
            #         icon="ERROR",
            #     )

        row = layout.row(align=True)
        row.menu(
            GenerateMarkersMenu.bl_idname, text="Generate Markers", icon="SHADERFX"
        )

        row = layout.row(align=True)
        row.operator(
            AppendFormationToStoryboardOperator.bl_idname,
            text="Append",
            icon="FORWARD",
        )

        row = layout.row(align=True)
        row.operator(
            SkybrushAdsorbOperator.bl_idname,
            text="Adsorb",
            icon="SNAP_ON",
        )
        row.operator(
            RunFullProximityCheckOperator.bl_idname,
            text="Verify",
            icon="DRIVER_DISTANCE",
        )

        row = layout.row(align=True)
        row.operator(
            UpdateFormationOperator.bl_idname, text="Update", icon="FILE_REFRESH"
        )
        row.operator_menu_enum(
            ReorderFormationMarkersOperator.bl_idname,
            "type",
            icon="SORTSIZE",
            text="Reorder",
        )

        row = layout.row()
        row.prop(formations, "order_overlay_enabled")
