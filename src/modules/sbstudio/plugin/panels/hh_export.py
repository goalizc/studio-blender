import bpy

from bpy.types import Panel

from sbstudio.plugin.operators import (
    SkybrushCreateRealFrameDataOperator,
    SkybrushCalculatePathOperator,
    SkybrushClearPathOperator,
    SkybrushInsertKeyframePathOperator,
    SkybrushClearKeyframePathOperator,
    SkybrushCalculatePathAverageOperator,
    SkybrushCalculateGroupTakeoffOperator,
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
    SkybrushYellowBlueCyanColorOperator,
    SkybrushRedYellowPurpleColorOperator,
    SkybrushPurpleBlueCyanColorOperator,
    SkybrushCloseMaterialChannelOperator,
    SkybrushCloseTransformChannelOperator,
    SkybrushOpenMaterialChannelOperator,
    SkybrushOpenTransformChannelOperator,
    SkybrushHHExportOperator,
    SkybrushHHChoosePNGOperator,
)

__all__ = ("HHExportPanel",)


class HHExportPanel(Panel):
    

    bl_idname = "OBJECT_PT_skybrush_hh_export_panel"
    bl_label = "HH Plugins"

    
    
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "HH & Export"


    @classmethod
    def poll(cls, context):
        return context.scene.skybrush.hh_export


    def draw(self, context):
        scene = context.scene
        hh_export = scene.skybrush.hh_export
        settings = scene.skybrush.settings
        if not hh_export or not settings:
            return

        layout = self.layout
        layout.prop(hh_export, "export_farme_data")
        layout.operator(SkybrushCreateRealFrameDataOperator.bl_idname, text="Create Frame Data")
        layout.operator(SkybrushHHExportOperator.bl_idname, text="Export HH Frame Data")

        layout.prop(hh_export, "png_image_path")
        layout.prop(hh_export, "png_min_distance")
        layout.operator(SkybrushHHChoosePNGOperator.bl_idname, text="Select PNG image")

        layout.label(text = "Calculate path:")
        layout.prop(hh_export, "frame_start")
        layout.prop(hh_export, "frame_end")
        layout.prop(hh_export, "frame_distance")
        layout.prop(hh_export, "frames_per_second")
        layout.prop(hh_export, "frame_velocity")
        layout.operator(SkybrushCalculatePathOperator.bl_idname, text="Calculate path (waiting, maximum velocity)")
        layout.operator(SkybrushCalculatePathAverageOperator.bl_idname, text="Calculate path (average velocity)")
        layout.operator(SkybrushClearPathOperator.bl_idname, text="Clear path")

        layout.prop(hh_export, "frame_interval")
        layout.operator(SkybrushInsertKeyframePathOperator.bl_idname, text="Insert path keyframe")
        layout.operator(SkybrushClearKeyframePathOperator.bl_idname, text="Clear path keyframe")

        layout.label(text = "Calculate takeoff and landing path:")
        layout.operator(SkybrushCalculateGroupTakeoffOperator.bl_idname, text="Calculate group takeoff")

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
        row.operator(SkybrushYellowBlueCyanColorOperator.bl_idname, text="Yellow-Lime-Cyan", icon="MATERIAL")
        row = layout.row(align=True)
        row.operator(SkybrushRedYellowPurpleColorOperator.bl_idname, text="Red-Yellow-Purple", icon="MATERIAL")
        row.operator(SkybrushPurpleBlueCyanColorOperator.bl_idname, text="Purple-Blue-Cyan", icon="MATERIAL")
        layout.label(text = "Channel Filtering:")
        row = layout.row(align=True)
        row.operator(SkybrushCloseMaterialChannelOperator.bl_idname, text="Disable Material Channel", icon="MATERIAL")
        row.operator(SkybrushOpenMaterialChannelOperator.bl_idname, text="Enable Material Channel", icon="HIDE_OFF")
        row = layout.row(align=True)
        row.operator(SkybrushCloseTransformChannelOperator.bl_idname, text="Disable Transform Channel", icon="ORIENTATION_GLOBAL")
        row.operator(SkybrushOpenTransformChannelOperator.bl_idname, text="Enable Transform Channel", icon="HIDE_OFF")
        layout.label(text = "")
