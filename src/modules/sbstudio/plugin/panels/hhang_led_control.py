from bpy.types import Panel

class HHangLEDControlPanel(Panel):
    bl_idname = "OBJECT_PT_skybrush_hhang_led_control_panel"
    bl_label = "HanHang LED Control"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LEDs"

    def draw(self, context):
        hhang_led_control = context.scene.skybrush.hhang_led_control
        if hhang_led_control.texture:
            row = self.layout.row()
            row.box().template_color_ramp(hhang_led_control.texture, "color_ramp", expand=True)
        row = self.layout.row()
        row.column().prop(hhang_led_control, "position", text="", slider=True)
        row.column().prop(hhang_led_control, "color", text="")
        row.column().operator("skybrush.hhang_led_control_apply", text="", icon="SEQUENCE_COLOR_01")
        row.column().operator("skybrush.hhang_led_control_gradient", text="", icon="GP_MULTIFRAME_EDITING")
