from bpy.props import PointerProperty
from bpy.types import PropertyGroup

from .formations_panel import FormationsPanelProperties
from .led_control import LEDControlPanelProperties
from .hhang_led_control import HHangLEDControlPanelProperties
from .light_effects import LightEffectCollection
from .pyro_control import PyroControlPanelProperties
from .safety_check import SafetyCheckProperties
from .settings import DroneShowAddonFileSpecificSettings
from .storyboard import Storyboard
from .hh_export import HHExportPanelProperties

__all__ = ("DroneShowAddonProperties",)


class DroneShowAddonProperties(PropertyGroup):
    """Custom Blender property representing the properties of the entire drone
    show addon.

    Each Blender scene that is set up for Skybrush will contain one instance
    of this property.
    """

    formations: FormationsPanelProperties = PointerProperty(
        type=FormationsPanelProperties
    )
    led_control: LEDControlPanelProperties = PointerProperty(
        type=LEDControlPanelProperties
    )
    hhang_led_control: HHangLEDControlPanelProperties = PointerProperty(
        type=HHangLEDControlPanelProperties
    )
    light_effects: LightEffectCollection = PointerProperty(type=LightEffectCollection)
    pyro_control: PyroControlPanelProperties = PointerProperty(
        type=PyroControlPanelProperties
    )
    safety_check: SafetyCheckProperties = PointerProperty(type=SafetyCheckProperties)
    settings: DroneShowAddonFileSpecificSettings = PointerProperty(
        type=DroneShowAddonFileSpecificSettings
    )
    storyboard: Storyboard = PointerProperty(type=Storyboard)
    hh_export = PointerProperty(type=HHExportPanelProperties)
