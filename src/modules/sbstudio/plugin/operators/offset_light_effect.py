import bpy

from bpy.props import IntProperty
from bpy.types import Operator

class SkybrushOffsetLightEffectOperator(Operator):
    bl_idname = "skybrush.offset_light_effect"
    bl_label = "Offset light effect"
    bl_description = (
        "Offset the lighting effect start frame"
    )
    bl_options = {"REGISTER", "UNDO"}

    frames = IntProperty(
        name="Frames",
        description="Offset frames",
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        for entry in context.scene.skybrush.light_effects.entries:
            entry.frame_start += self.frames
        return {"FINISHED"}
