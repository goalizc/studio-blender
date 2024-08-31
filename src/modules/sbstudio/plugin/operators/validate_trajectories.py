import sys
import numpy as np
import bpy

from bpy.props import BoolProperty, FloatProperty
from bpy.types import Operator

from sbstudio.model.safety_check import SafetyCheckParams
from sbstudio.plugin.api import call_api_from_blender_operator
from sbstudio.plugin.tasks.light_effects import suspended_light_effects
from sbstudio.plugin.tasks.safety_check import suspended_safety_checks
from sbstudio.plugin.props.frame_range import FrameRangeProperty, resolve_frame_range
from sbstudio.plugin.utils.evaluator import get_position_of_object
from sbstudio.plugin.utils.sampling import sample_positions_of_objects_in_frame_range
from sbstudio.viewer_bridge import (
    SkybrushViewerBridge,
    SkybrushViewerError,
    SkybrushViewerNotFoundError,
)

from .utils import get_drones_to_export

__all__ = ("ValidateTrajectoriesOperator",)

#: Global object to access Skybrush Viewer and send it the trajectories to validate
skybrush_viewer = SkybrushViewerBridge()


class ValidateTrajectoriesSkybrushViewerOperator(Operator):
    """Validates the trajectories of the drones in a given frame range."""

    bl_idname = "skybrush.validate_trajectories"
    bl_label = "Validate Trajectories"
    bl_description = "Validates the trajectories of the drones in a given frame range."

    # validate all drones or only selected ones
    selected_only = BoolProperty(
        name="Selection only",
        default=False,
        description=(
            "Validate only the selected drones. "
            "Uncheck to export all drones, irrespectively of the selection."
        ),
    )

    # frame range source
    frame_range = FrameRangeProperty()

    def execute(self, context):
        drones = get_drones_to_export(selected_only=self.selected_only)
        frame_range = resolve_frame_range(self.frame_range)
        if frame_range is None:
            self.report({"ERROR"}, "Selected frame range is empty")
            return {"CANCELLED"}

        safety_check = getattr(context.scene.skybrush, "safety_check", None)
        validation = SafetyCheckParams(
            max_velocity_xy=(
                safety_check.velocity_xy_warning_threshold if safety_check else 8
            ),
            max_velocity_z=(
                safety_check.velocity_z_warning_threshold if safety_check else 2
            ),
            max_velocity_z_up=(
                safety_check.velocity_z_warning_threshold_up_or_none
                if safety_check
                else None
            ),
            max_altitude=(
                safety_check.altitude_warning_threshold if safety_check else 150
            ),
            min_distance=(
                safety_check.proximity_warning_threshold if safety_check else 3
            ),
        )

        try:
            running = skybrush_viewer.check_running()
        except SkybrushViewerNotFoundError:
            running = False
        except SkybrushViewerError as ex:
            self.report({"ERROR"}, str(ex))
            return {"CANCELLED"}
        except Exception:
            self.report(
                {"ERROR"}, "Error while checking whether Skybrush Viewer is running"
            )
            return {"CANCELLED"}

        if not running:
            self.report(
                {"ERROR"},
                "Skybrush Viewer is not running; please start it and try again",
            )
            return {"CANCELLED"}

        with suspended_safety_checks(), suspended_light_effects():
            trajectories = sample_positions_of_objects_in_frame_range(
                drones,
                frame_range,
                fps=4,
                context=context,
                by_name=True,
                simplify=True,
            )

        # Calculate the start time of the validated range, in seconds
        fps = context.scene.render.fps
        start_of_scene = context.scene.frame_start
        timestamp_offset = (frame_range[0] - start_of_scene) / fps

        if timestamp_offset:
            for trajectory in trajectories.values():
                trajectory.shift_time_in_place(-timestamp_offset)

        filename = bpy.data.filepath or None
        try:
            with call_api_from_blender_operator(self) as api:
                show_data = api.export(
                    trajectories=trajectories,
                    validation=validation,
                    timestamp_offset=(
                        timestamp_offset if timestamp_offset != 0 else None
                    ),
                    renderer="skyc",
                )
        except Exception:
            return {"CANCELLED"}

        assert show_data is not None

        try:
            skybrush_viewer.load_show_for_validation(show_data, filename=filename)
            self.report(
                {"INFO"},
                "Now switch to the Skybrush Viewer window to view the results",
            )
            return {"FINISHED"}
        except SkybrushViewerNotFoundError:
            self.report(
                {"ERROR"},
                "Skybrush Viewer is not running; please start it and try again",
            )
        except SkybrushViewerError as ex:
            self.report({"ERROR"}, str(ex))
        except Exception:
            self.report({"ERROR"}, "Error while sending show data to Skybrush Viewer")

        return {"CANCELLED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class ValidateTrajectoriesOperator(Operator):
    """Validates the trajectories of the drones in a given frame range."""

    bl_idname = "skybrush.validate_trajectories"
    bl_label = "Validate Trajectories"
    bl_description = "Validates the trajectories of the drones in a given frame range."

    min_distance = FloatProperty(
        name="Min distance",
        description="Minimum distance along all possible pairs of drones in the current frame, calculated between their centers of mass",
        unit="LENGTH",
        default=1.2,
        soft_min=0.5,
        soft_max=10.0,
    )

    max_velocity = FloatProperty(
        name="Max velocity",
        description="Maximum velocity of all drones in the current frame",
        unit="VELOCITY",
        default=5,
        soft_min=0.5,
        soft_max=50.0,
    )

    max_acceleration = FloatProperty(
        name="Max acceleration",
        description="Maximum acceleration allowed when planning the duration of transitions between fixed points",
        unit="ACCELERATION",
        default=3,
        soft_min=0.1,
        soft_max=20,
    )

    # validate all drones or only selected ones
    selected_only = BoolProperty(
        name="Selection only",
        default=False,
        description=(
            "Validate only the selected drones. "
            "Uncheck to export all drones, irrespectively of the selection."
        ),
    )

    # frame range source
    frame_range = FrameRangeProperty()

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        frame_current = context.scene.frame_current
        drones = get_drones_to_export(selected_only=self.selected_only)
        tril = np.tril(np.full((len(drones), len(drones)), 999))
        frame_range = resolve_frame_range(self.frame_range)
        if frame_range is None:
            self.report({"ERROR"}, "Selected frame range is empty")
            return {"CANCELLED"}

        distance_history, distance_result = {}, []
        def check_distance(frame, points):
            dist = tril + np.triu(np.sqrt(((points[:, None, :] - points) ** 2).sum(-1)))
            x, y = np.where(dist < self.min_distance)
            zpxy = frozenset(zip([int(x) for x in x], [int(y) for y in y]))
            for xy in distance_history.keys() - zpxy:
                distance_result.append((xy, distance_history[xy]))
                del distance_history[xy]
            for xy in zpxy:
                if xy not in distance_history or dist[xy] < distance_history[xy][1]:
                    distance_history[xy] = (frame, dist[xy])

        velocity_history, velocity_result, velocity_previous = {}, [], np.zeros(len(drones))
        acceleration_history, acceleration_result = {}, []
        def check_velocity(frame, previous, points):
            velocity = np.sqrt(((points - previous) ** 2).sum(-1)) * context.scene.render.fps
            index = np.where(velocity > self.max_velocity)[0]
            for i in velocity_history.keys() - index:
                velocity_result.append((i, velocity_history[i]))
                del(velocity_history[i])
            for i in index:
                if i not in velocity_history or velocity[i] > velocity_history[i][1]:
                    velocity_history[i] = (frame, velocity[i])

            acceleration = np.abs(velocity - velocity_previous)
            index = np.where(acceleration > self.max_acceleration)[0]
            for i in acceleration_history.keys() - index:
                acceleration_result.append((i, acceleration_history[i]))
                del(acceleration_history[i])
            for i in  index:
                if i not in acceleration_history or acceleration[i] > acceleration_history[i][1]:
                    acceleration_history[i] = (frame, acceleration[i])

            np.copyto(velocity_previous, velocity)

        with suspended_safety_checks(), suspended_light_effects():
            self.console_toggle()
            current_frame, last_frame = frame_range
            previous = self.get_positions(context, current_frame, drones)
            check_distance(current_frame, previous)
            while current_frame < last_frame:
                current_frame += 1
                print(f"[Validate] Current Frame: {current_frame}/{last_frame}\r", end="")
                current = self.get_positions(context, current_frame, drones)
                check_distance(current_frame, current)
                check_velocity(current_frame, previous, current)
                previous = current
            print()
            distance_result.extend(distance_history.items())
            velocity_result.extend(velocity_history.items())
            acceleration_result.extend(acceleration_history.items())
            bpy.types.Scene.drones = drones
            bpy.types.Scene.distance_result = distance_result
            bpy.types.Scene.velocity_result = velocity_result
            bpy.types.Scene.acceleration_result = acceleration_result
            context.scene.frame_set(frame_current)
            self.console_toggle()

        return {"FINISHED"}

    def get_positions(self, context, frame, drones):
        context.scene.frame_set(frame)
        return np.array([get_position_of_object(drone) for drone in drones])

    def console_toggle(self):
        if sys.platform[:3] == "win":
            bpy.ops.wm.console_toggle()
