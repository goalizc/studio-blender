bl_info = {
    "name": "Skybrush Studio",
    "author": "CollMot Robotics Ltd.",
    "description": "Extends Blender with UI components for drone show design",
    "version": (4, 2, 0),
    "blender": (4, 4, 0),
    "category": "Interface",
    "doc_url": "https://doc.collmot.com/public/skybrush-studio-for-blender/latest/",
    "tracker_url": "https://github.com/skybrush-io/studio-blender/issues",
}

__license__ = "GPLv3"

# BLENDER ADD-ON INFO ENDS HERE ### DO NOT REMOVE THIS LINE #################

#############################################################################
# imports needed to set up the Python path properly

import os
import sys
import threading

from inspect import isfunction
from bpy.ops import preferences
from bpy.props import PointerProperty
from bpy.types import Object, Scene, Operator, VIEW3D_HT_header
from functools import partial
from pathlib import Path
from types import ModuleType


#############################################################################
# 引入三方库目录
packages_dir = os.path.join(os.path.expanduser("~"), "Documents", "blender_packages")
sys.path.insert(0, packages_dir)


#############################################################################
# 重新加载插件操作
def draw_reload_sbstudio_button(self, context):
    layout = self.layout
    layout.operator("skybrush.reload_sbstudio", text="", icon="FILE_SCRIPT")

def reload_sbstudio():
    base = "ui_skybrush_studio"
    preferences.addon_disable(module=base)
    for name, module in [item for item in sys.modules.items()]:
        if isinstance(module, ModuleType) and module.__name__.startswith("sbstudio."):
            del sys.modules[name]
        elif name == base:
            del sys.modules[name]
    preferences.addon_enable(module=base)

class VIEW3D_HT_reload_sbstudio(Operator):
    bl_idname = "skybrush.reload_sbstudio"
    bl_label = "重新加载Skybrush Studio"
    bl_description = '重装Skybrush Studio插件后，点击此按钮可重新加载插件'

    def execute(self, context):
        threading.Thread(target=reload_sbstudio).start()
        return {'FINISHED'}

from bpy.props import PointerProperty
from bpy.types import Object, Scene

#############################################################################
# Note: This code needs to be harmonized with the plugin installer to have
# the same target directory for all add-on specific dependencies.

this_file = sys.modules[__name__].__file__
candidates: list[Path] = []
if this_file is not None:
    candidates.extend(
        [
            Path(this_file).parent,
            Path(this_file).parent.parent,
        ]
    )
for candidate in candidates:
    path = (Path(candidate) / "vendor" / "skybrush").resolve()
    if path.exists():
        sys.path.insert(0, str(path))
        break


#############################################################################
# imports needed by the addon

from sbstudio.i18n.translations import translations_dict
from sbstudio.plugin.lists import (
    SKYBRUSH_UL_lightfxlist,
    SKYBRUSH_UL_scheduleoverridelist,
)
from sbstudio.plugin.menus import GenerateMarkersMenu
from sbstudio.plugin.model import (
    ColorFunctionProperties,
    DroneShowAddonFileSpecificSettings,
    DroneShowAddonGlobalSettings,
    DroneShowAddonObjectProperties,
    DroneShowAddonProperties,
    FormationsPanelProperties,
    LEDControlPanelProperties,
    HHangLEDControlPanelProperties,
    LightEffect,
    LightEffectCollection,
    EnumPropertyItem,
    ArgumentProperty,
    ColorFunctionProperties,
    ColorRampFunctionProperties,
    PyroControlPanelProperties,
    SafetyCheckProperties,
    ScheduleOverride,
    Storyboard,
    StoryboardEntry,
    StoryboardEntryOrTransition,
    get_formation_order_overlay,
    get_pyro_effects_overlay,
    get_safety_check_overlay,
    HHangPanelProperties,
)
from sbstudio.plugin.operators import (
    AddMarkersFromQRCodeOperator,
    AddMarkersFromStaticCSVOperator,
    AddMarkersFromSVGOperator,
    AddMarkersFromZippedCSVOperator,
    AddMarkersFromZippedDSSOperator,
    AppendFormationToStoryboardOperator,
    ApplyColorsToSelectedDronesOperator,
    CreateFormationOperator,
    CreateLightEffectOperator,
    CreateNewScheduleOverrideEntryOperator,
    CreateNewStoryboardEntryOperator,
    CreateTakeoffGridOperator,
    RedistributionTakeoffGridOperator,
    RenameOperator,
    DACExportOperator,
    DDSFExportOperator,
    DeselectFormationOperator,
    DetachMaterialsFromDroneTemplateOperator,
    DrotekExportOperator,
    DSSPath3ExportOperator,
    DSSPathExportOperator,
    DuplicateLightEffectOperator,
    EVSKYExportOperator,
    ExportLightEffectsOperator,
    FinaleCSVExportOperator,
    FixConstraintOrderingOperator,
    GetFormationStatisticsOperator,
    ImportLightEffectsOperator,
    KMZExportOperator,
    LandOperator,
    LitebeeExportOperator,
    MoveLightEffectDownOperator,
    MoveLightEffectUpOperator,
    MoveStoryboardEntryDownOperator,
    MoveStoryboardEntryUpOperator,
    PrepareSceneOperator,
    RecalculateTransitionsOperator,
    RefreshFileFormatsOperator,
    RemoveFormationOperator,
    RemoveLightEffectOperator,
    RemoveScheduleOverrideEntryOperator,
    RemoveStoryboardEntryOperator,
    ReorderFormationMarkersOperator,
    ReturnToHomeOperator,
    RunAllMigrationOperators,
    RunFullProximityCheckOperator,
    SelectFormationOperator,
    SelectStoryboardEntryForCurrentFrameOperator,
    SetLightEffectEndFrameOperator,
    SetLightEffectStartFrameOperator,
    SetServerURLOperator,
    SetStoryboardEntryEndFrameOperator,
    SetStoryboardEntryStartFrameOperator,
    SetupSceneOperator,
    SkybrushCSVExportOperator,
    SkybrushExportOperator,
    SkybrushPDFExportOperator,
    SkybrushHHExportOperator,
    SkybrushHHImportImageOperator,
    SkybrushAddCurrentFrameToExportFrameDataOperator,
    SkybrushReplaceCopyLocationConstraintOperator,
    SkybrushCalculateGroupTakeoffOperator,
    SkybrushCalculateGroupLandOperator,
    SkybrushRecalculateGroupTakeoffOperator,
    SkybrushNebulaOperator,
    SkybrushSelectFileOperator,
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
    SkybrushSKYCAndPDFExportOperator,
    SwapColorsInLEDControlPanelOperator,
    TakeoffOperator,
    TriggerPyroOnSelectedDronesOperator,
    UpdateFormationOperator,
    UpdateFrameRangeFromStoryboardOperator,
    UpdateTimeMarkersFromStoryboardOperator,
    UseSelectedVertexGroupForFormationOperator,
    ValidateLightsOperator,
    ValidateTrajectoriesOperator,
    UseHHangLEDControlOperator,
    HHangLEDControlGenerateOperator,
    HHangLEDControlApplyOperator,
    HHangLEDControlGradientOperator,
    VVIZExportOperator,
    SkybrushAdsorbOperator,
    SkybrushFrameDelayOperator,
    SkybrushCalculateSafePathOperator,
    SkybrushOffsetLightEffectOperator,
    SkybrushShowMessageOperator,
    SkybrushExportTakeoffPositionOperator,
)
from sbstudio.plugin.panels import (
    DroneShowAddonObjectPropertiesPanel,
    ExportPanel,
    HHangPanel,
    FormationsPanel,
    LEDControlPanel,
    LightEffectsPanel,
    PyroControlPanel,
    SafetyCheckPanel,
    SetupPanel,
    ShowPanel,
    StoryboardEditor,
    SwarmPanel,
    TransitionEditorFromCurrentFormation,
    TransitionEditorIntoCurrentFormation,
)
from sbstudio.plugin.plugin_helpers import (
    register_header,
    register_list,
    register_menu,
    register_operator,
    register_panel,
    register_translations,
    register_type,
    unregister_header,
    unregister_list,
    unregister_menu,
    unregister_operator,
    unregister_panel,
    unregister_translations,
    unregister_type,
)
from sbstudio.plugin.state import (
    register as register_state,
)
from sbstudio.plugin.state import (
    unregister as unregister_state,
)
from sbstudio.plugin.tasks import (
    InitializationTask,
    InvalidatePixelCacheTask,
    PyroEffectsTask,
    SafetyCheckTask,
    UpdateLightEffectsTask,
)

from sbstudio.plugin.utils.lang import (
    register as register_lang,
    unregister as unregister_lang,
)

types = (
    HHangPanelProperties,
    FormationsPanelProperties,
    EnumPropertyItem,
    ArgumentProperty,
    ColorFunctionProperties,
    ColorRampFunctionProperties,
    ScheduleOverride,
    StoryboardEntry,
    StoryboardEntryOrTransition,
    Storyboard,
    LightEffect,
    LightEffectCollection,
    LEDControlPanelProperties,
    HHangLEDControlPanelProperties,
    PyroControlPanelProperties,
    SafetyCheckProperties,
    DroneShowAddonFileSpecificSettings,
    DroneShowAddonGlobalSettings,
    DroneShowAddonProperties,
    DroneShowAddonObjectProperties,
)
"""Custom types in this addon."""

operators = (
    VIEW3D_HT_reload_sbstudio,
    PrepareSceneOperator,
    CreateFormationOperator,
    SelectFormationOperator,
    DeselectFormationOperator,
    UpdateFormationOperator,
    ReorderFormationMarkersOperator,
    RemoveFormationOperator,
    CreateNewStoryboardEntryOperator,
    AppendFormationToStoryboardOperator,
    MoveStoryboardEntryDownOperator,
    MoveStoryboardEntryUpOperator,
    SelectStoryboardEntryForCurrentFrameOperator,
    RemoveStoryboardEntryOperator,
    SetStoryboardEntryEndFrameOperator,
    SetStoryboardEntryStartFrameOperator,
    CreateNewScheduleOverrideEntryOperator,
    RemoveScheduleOverrideEntryOperator,
    UpdateFrameRangeFromStoryboardOperator,
    UpdateTimeMarkersFromStoryboardOperator,
    CreateLightEffectOperator,
    DuplicateLightEffectOperator,
    ExportLightEffectsOperator,
    ImportLightEffectsOperator,
    MoveLightEffectDownOperator,
    MoveLightEffectUpOperator,
    RemoveLightEffectOperator,
    SetLightEffectEndFrameOperator,
    SetLightEffectStartFrameOperator,
    CreateTakeoffGridOperator,
    RedistributionTakeoffGridOperator,
    RenameOperator,
    DetachMaterialsFromDroneTemplateOperator,
    FixConstraintOrderingOperator,
    RecalculateTransitionsOperator,
    ApplyColorsToSelectedDronesOperator,
    SwapColorsInLEDControlPanelOperator,
    TriggerPyroOnSelectedDronesOperator,
    ValidateLightsOperator,
    ValidateTrajectoriesOperator,
    SetServerURLOperator,
    SkybrushExportOperator,
    SkybrushCSVExportOperator,
    SkybrushPDFExportOperator,
    SkybrushSKYCAndPDFExportOperator,
    DACExportOperator,
    DDSFExportOperator,
    DrotekExportOperator,
    DSSPathExportOperator,
    DSSPath3ExportOperator,
    EVSKYExportOperator,
    FinaleCSVExportOperator,
    KMZExportOperator,
    LitebeeExportOperator,
    SkybrushHHExportOperator,
    SkybrushHHImportImageOperator,
    SkybrushAddCurrentFrameToExportFrameDataOperator,
    SkybrushReplaceCopyLocationConstraintOperator,
    SkybrushCalculateGroupTakeoffOperator,
    SkybrushCalculateGroupLandOperator,
    SkybrushRecalculateGroupTakeoffOperator,
    SkybrushNebulaOperator,
    SkybrushSelectFileOperator,
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
    VVIZExportOperator,
    SkybrushAdsorbOperator,
    SkybrushFrameDelayOperator,
    SkybrushCalculateSafePathOperator,
    SkybrushOffsetLightEffectOperator,
    SkybrushShowMessageOperator,
    SkybrushExportTakeoffPositionOperator,
    UseSelectedVertexGroupForFormationOperator,
    GetFormationStatisticsOperator,
    TakeoffOperator,
    LandOperator,
    ReturnToHomeOperator,
    AddMarkersFromStaticCSVOperator,
    AddMarkersFromSVGOperator,
    AddMarkersFromZippedCSVOperator,
    AddMarkersFromZippedDSSOperator,
    AddMarkersFromQRCodeOperator,
    RefreshFileFormatsOperator,
    RunFullProximityCheckOperator,
    RunAllMigrationOperators,
    SetupSceneOperator,
    UseHHangLEDControlOperator,
    HHangLEDControlGenerateOperator,
    HHangLEDControlApplyOperator,
    HHangLEDControlGradientOperator,
)
"""Operators in this addon; operators that require other operators must come
later in the list than their dependencies."""


lists = (SKYBRUSH_UL_lightfxlist, SKYBRUSH_UL_scheduleoverridelist)
"""List widgets in this addon."""

menus = (GenerateMarkersMenu,)
"""Menus in this addon."""

panels = (
    SetupPanel,
    ShowPanel,
    SwarmPanel,
    FormationsPanel,
    StoryboardEditor,
    TransitionEditorFromCurrentFormation,
    TransitionEditorIntoCurrentFormation,
    LEDControlPanel,
    LightEffectsPanel,
    # PyroControlPanel,
    SafetyCheckPanel,
    ExportPanel,
    HHangPanel,
    DroneShowAddonObjectPropertiesPanel,
)
"""Panels in this addon. The order also implicitly defines the order in which
our tabs appear in the sidebar of the 3D view."""

headers = ()
"""Headers in this addon."""

tasks = (
    InitializationTask(),
    InvalidatePixelCacheTask(),
    PyroEffectsTask(),
    SafetyCheckTask(),
    UpdateLightEffectsTask(),
)
"""Background tasks in this addon."""

overlay_getters = (
    partial(get_safety_check_overlay, create=False),
    partial(get_pyro_effects_overlay, create=False),
    get_formation_order_overlay,
)
"""Getters for the overlays in this addon, used to disable them before unloading."""

cython_compiled = False
for o in operators:
    if hasattr(o, 'draw') and not isfunction(o.draw):
        cython_compiled, o.DRAW, o.draw = True, o.draw, lambda s, o: s.DRAW(o)
    if hasattr(o, 'execute') and not isfunction(o.execute):
        cython_compiled, o.EXECUTE, o.execute = True, o.execute, lambda s, o: s.EXECUTE(o)
    if hasattr(o, 'invoke') and not isfunction(o.invoke):
        cython_compiled, o.INVOKE, o.invoke = True, o.invoke, lambda s, o, e: s.INVOKE(o, e)

def register():
    register_lang()
    register_translations(translations_dict)
    register_state()
    for custom_type in types:
        register_type(custom_type)
    for operator in operators:
        register_operator(operator)
    for list_ in lists:
        register_list(list_)
    for menu in menus:
        register_menu(menu)
    for panel in panels:
        register_panel(panel)
    for header in headers:
        register_header(header)
    for task in tasks:
        task.register()

    Scene.skybrush = PointerProperty(type=DroneShowAddonProperties)
    Object.skybrush = PointerProperty(type=DroneShowAddonObjectProperties)
    if not cython_compiled:
        VIEW3D_HT_header.append(draw_reload_sbstudio_button)


def unregister():
    for getter in overlay_getters:
        overlay = getter()
        if overlay:
            overlay.enabled = False
    for task in tasks:
        task.unregister()
    for header in reversed(headers):
        unregister_header(header)
    for panel in reversed(panels):
        unregister_panel(panel)
    for menu in menus:
        unregister_menu(menu)
    for list_ in lists:
        unregister_list(list_)
    for operator in reversed(operators):
        unregister_operator(operator)
    for custom_type in reversed(types):
        unregister_type(custom_type)
    unregister_state()
    unregister_translations()
    unregister_lang()
    if not cython_compiled:
        VIEW3D_HT_header.remove(draw_reload_sbstudio_button)
