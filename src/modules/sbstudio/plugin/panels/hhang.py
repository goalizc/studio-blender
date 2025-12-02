import bpy

from bpy.types import Panel
from sbstudio.plugin.constants import Collections

from sbstudio.plugin.operators import (
    SkybrushCreateRealFrameDataOperator,
    SkybrushCalculateGroupTakeoffOperator,
    SkybrushCalculateGroupLandOperator,
    SkybrushRecalculateGroupTakeoffOperator,
    SkybrushNebulaOperator,
    SkybrushRedColorOperator,
    SkybrushBlueColorOperator,
    SkybrushYellowColorOperator,
    SkybrushGreenColorOperator,
    SkybrushWhiteColorOperator,
    SkybrushBlackColorOperator,
    SkybrushPinkColorOperator,
    SkybrushSkyBlueColorOperator,
    SkybrushPurpleColorOperator,
    SkybrushOrangeColorOperator,
    SkybrushCyanColorOperator,
    SkybrushVioletColorOperator,
    SkybrushOrangeYellowColorOperator,
    SkybrushPurplishRedColorOperator,
    SkybrushBlueGreenColorOperator,
    SkybrushBabyBlueColorOperator,
    SkybrushRandomColorOperator,
    SkybrushRandomBlueColorOperator,
    SkybrushYellowBlueCyanColorOperator,
    SkybrushRandomColorNoBlackOperator,
    SkybrushRandomBlueColorNoBlackOperator,
    SkybrushHHExportOperator,
    SkybrushHHChooseImageOperator,
    SkybrushFrameDelayOperator,
    SkybrushCalculateSafePathOperator,
    SkybrushExportTakeoffPositionOperator,
)

__all__ = ("HHangPanel",)

def filter_channels(self, context):
    for area in bpy.context.screen.areas:
        if area.type == 'DOPESHEET_EDITOR':
            space_data = area.spaces.active
            xor = context.scene.filter_color_channels ^ context.scene.filter_noncolor_channels
            space_data.dopesheet.filter_text = ("楠楠", "颜色")[xor]
            space_data.dopesheet.use_filter_invert = xor ^ context.scene.filter_color_channels

bpy.types.Scene.filter_color_channels = bpy.props.BoolProperty(
    name="颜色通道",
    default=True,
    update=filter_channels
)

bpy.types.Scene.filter_noncolor_channels = bpy.props.BoolProperty(
    name="非颜色通道",
    default=True,
    update=filter_channels
)

class HHangPanel(Panel):
    bl_idname = "OBJECT_PT_skybrush_hhang_panel"
    bl_label = "HH Plugins"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Han Hang"

    def draw(self, context):
        layout = self.layout
        layout.label(text = "Function:")
        layout.operator(SkybrushRecalculateGroupTakeoffOperator.bl_idname, text="Recalculate group takeoff")
        layout.operator(SkybrushCalculateSafePathOperator.bl_idname, text="Calculate safe path")
        layout.operator(SkybrushFrameDelayOperator.bl_idname)
        layout.operator(SkybrushHHChooseImageOperator.bl_idname)
        layout.operator(SkybrushExportTakeoffPositionOperator.bl_idname)
        layout.operator(SkybrushHHExportOperator.bl_idname, text="Export HH Frame Data")

        layout.label(text = "Single color:")
        row = layout.row(align=True)
        row.operator(SkybrushRedColorOperator.bl_idname, text="Red", icon="NODE_MATERIAL")
        row.operator(SkybrushBlueColorOperator.bl_idname, text="Blue", icon="NODE_MATERIAL")
        row.operator(SkybrushYellowColorOperator.bl_idname, text="Yellow", icon="NODE_MATERIAL")
        row = layout.row(align=True)
        row.operator(SkybrushGreenColorOperator.bl_idname, text="Green", icon="NODE_MATERIAL")
        row.operator(SkybrushWhiteColorOperator.bl_idname, text="White", icon="NODE_MATERIAL")
        row.operator(SkybrushBlackColorOperator.bl_idname, text="Black", icon="NODE_MATERIAL")
        row = layout.row(align=True)
        row.operator(SkybrushPinkColorOperator.bl_idname, text="Pink", icon="NODE_MATERIAL")
        row.operator(SkybrushSkyBlueColorOperator.bl_idname, text="Sky Blue", icon="NODE_MATERIAL")
        row.operator(SkybrushPurpleColorOperator.bl_idname, text="Purple", icon="NODE_MATERIAL")
        row = layout.row(align=True)
        row.operator(SkybrushOrangeColorOperator.bl_idname, text="Orange", icon="NODE_MATERIAL")
        row.operator(SkybrushCyanColorOperator.bl_idname, text="Cyan", icon="NODE_MATERIAL")
        row.operator(SkybrushVioletColorOperator.bl_idname, text="Blue-Purple", icon="NODE_MATERIAL")
        row = layout.row(align=True)
        row.operator(SkybrushOrangeYellowColorOperator.bl_idname, text="Orange-Yellow", icon="NODE_MATERIAL")
        row.operator(SkybrushPurplishRedColorOperator.bl_idname, text="Magenta", icon="NODE_MATERIAL")
        row = layout.row(align=True)
        row.operator(SkybrushBlueGreenColorOperator.bl_idname, text="Blue-Green", icon="NODE_MATERIAL")
        row.operator(SkybrushBabyBlueColorOperator.bl_idname, text="Light Blue", icon="NODE_MATERIAL")
        layout.label(text = "Random Color:")
        row = layout.row(align=True)
        row.operator(SkybrushRandomColorOperator.bl_idname, text="Random Color", icon="MATERIAL")
        row.operator(SkybrushRandomBlueColorOperator.bl_idname, text="Random Blue Color", icon="MATERIAL")
        # row.operator(SkybrushYellowBlueCyanColorOperator.bl_idname, text="Yellow-Lime-Cyan", icon="MATERIAL")
        row = layout.row(align=True)
        row.operator(SkybrushRandomColorNoBlackOperator.bl_idname, icon="MATERIAL")
        row.operator(SkybrushRandomBlueColorNoBlackOperator.bl_idname, icon="MATERIAL")

        layout.label(text = "通道:")
        row = layout.row(align=True)
        row.prop(context.scene, "filter_color_channels", toggle=True)
        row.prop(context.scene, "filter_noncolor_channels", toggle=True)
