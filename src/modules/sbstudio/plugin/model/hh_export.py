from bpy.props import StringProperty, FloatProperty, IntProperty
from bpy.types import PropertyGroup

__all__ = ("HHExportPanelProperties",)


class HHExportPanelProperties(PropertyGroup):
    export_farme_data = StringProperty(
        name="Frame data",
        description="For example: 1-2, 3, 5, 50-100",
        default="",
    )

    image_path = StringProperty(
        name="Path",
        description="Path of the imported image",
        default="",
    )

    min_distance = FloatProperty(
        name="Minimum Import Distance",
        description="The minimum distance for imported image",
        unit="LENGTH",
        default=3.0,
        min=0.1,
    )

    frame_start = IntProperty(
        name="Start Frame",
        description="Calculate Path Start Frame",
        default=0,
        options=set(),
    )

    frame_end = IntProperty(
        name="End Frame",
        description="Calculate Path End Frame",
        default=1,
        options=set(),
    )

    frame_distance = FloatProperty(
        name="Distance",
        description="The minimum distance between the aircraft when calculating the path",
        unit="LENGTH",
        default=3.0,
        min=0.1,
    )

    frames_per_second = IntProperty(
        name="fps",
        description="The frames per second (FPS) when calculating the path",
        default=12,
        options=set(),
    )

    frame_interval = IntProperty(
        name="Inserting keyframes at intervals",
        description="Insert a keyframe every X frames",
        default=1,
        options=set(),
    )

    frame_velocity = FloatProperty(
        name="Max velocity",
        description="The maximum velocity when calculating the path",
        unit="VELOCITY",
        default=4.0,
    )
