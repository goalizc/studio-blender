from bpy.props import StringProperty, FloatProperty, IntProperty
from bpy.types import PropertyGroup

__all__ = ("HHangPanelProperties",)


class HHangPanelProperties(PropertyGroup):
    frame_range = StringProperty(
        name="Frame range",
        description="For example:1,2-3,4-10:2",
        default="",
    )
