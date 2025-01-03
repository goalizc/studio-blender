from bpy.types import Texture, PropertyGroup
from bpy.props import PointerProperty, FloatProperty
from sbstudio.plugin.props import ColorProperty

__all__ = ("HHangLEDControlPanelProperties",)

class HHangLEDControlPanelProperties(PropertyGroup):
    def update(self, context):
        self.color = self.texture.color_ramp.evaluate(self.position)[:3]

    texture = PointerProperty(type=Texture, name="HHangLEDControlTexture", options={"HIDDEN"})
    position = FloatProperty(name="Color ramp postion", default=0, min=0, max=1, update=update)
    color = ColorProperty(name="Selected color")
