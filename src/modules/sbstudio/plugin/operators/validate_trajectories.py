import sys
import math
import numpy as np
import bpy

from typing import cast
from bpy.props import BoolProperty, FloatProperty
from bpy.types import Context, Operator

from sbstudio.api.console import ConsoleWindow
from sbstudio.model.safety_check import SafetyCheckParams
from sbstudio.model.trajectory import Trajectory
from sbstudio.plugin.api import call_api_from_blender_operator
from sbstudio.plugin.props.frame_range import FrameRangeProperty, resolve_frame_range
from sbstudio.plugin.tasks.light_effects import suspended_light_effects
from sbstudio.plugin.tasks.safety_check import suspended_safety_checks
from sbstudio.plugin.utils.evaluator import get_position_of_object
from sbstudio.plugin.utils.sampling import sample_positions_of_objects_in_frame_range
from sbstudio.viewer_bridge import (
    SkybrushViewerBridge,
    SkybrushViewerError,
    SkybrushViewerNotFoundError,
)

from .utils import get_drones_to_export

__all__ = ("ValidateTrajectoriesOperator",)

skybrush_viewer = SkybrushViewerBridge()
"""Global object to access Skybrush Viewer and send it the trajectories to validate."""


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

    def execute(self, context: Context):
        drones = get_drones_to_export(selected_only=self.selected_only)
        frame_range = resolve_frame_range(self.frame_range)
        if frame_range is None:
            self.report({"ERROR"}, "Selected frame range is empty")
            return {"CANCELLED"}

        safety_check = context.scene.skybrush.safety_check
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
            max_acceleration=(
                safety_check.acceleration_warning_threshold if safety_check else 4
            ),
            max_yaw_rate=safety_check.yaw_rate_warning_threshold
            if safety_check
            else 30,
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
            trajectories = cast(
                dict[str, Trajectory],
                sample_positions_of_objects_in_frame_range(
                    drones,
                    frame_range,
                    fps=4,
                    context=context,
                    by_name=True,
                    simplify=True,
                ),
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

    def invoke(self, context: Context, event):
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
        default=2.5,
        soft_min=0.5,
        soft_max=10.0,
    )

    max_xy_velocity = FloatProperty(
        name="Max XY velocity",
        description="Maximum xy velocity of all drones in the current frame",
        unit="VELOCITY",
        default=10,
        soft_min=0.5,
        soft_max=50.0,
    )

    max_z_velocity = FloatProperty(
        name="Max Z velocity",
        description="Maximum z velocity of all drones in the current frame",
        unit="VELOCITY",
        default=3,
        soft_min=0.5,
        soft_max=50.0,
    )

    max_xy_acceleration = FloatProperty(
        name="Max XY acceleration",
        description="Maximum xy acceleration allowed when planning the duration of transitions between fixed points",
        unit="ACCELERATION",
        default=1.1,
        soft_min=0.1,
        soft_max=20,
    )

    max_z_acceleration = FloatProperty(
        name="Max Z acceleration",
        description="Maximum z acceleration allowed when planning the duration of transitions between fixed points",
        unit="ACCELERATION",
        default=2,
        soft_min=0.1,
        soft_max=20,
    )

    max_tilt_angle = FloatProperty(
        name="Max tilt angle",
        description="Maximum tilt angle of the drone",
        unit="ROTATION",
        default=25 * math.pi / 180,
        min=0,
        max=45 * math.pi / 180,
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

        max_tilt_acceleration = 9.8 * math.tan(self.max_tilt_angle)
        print(f"[Validate] Max tilt angle: {max_tilt_acceleration:.02f}m/s2")
        def calculate_angles(A, B):
            velocity = np.sqrt((A ** 2).sum(-1))
            norm_A = np.linalg.norm(A, axis=1)
            norm_B = np.linalg.norm(B, axis=1)
            indices = np.logical_and(norm_A > 0, norm_B > 0)
            cosines = np.sum(A[indices] * B[indices], axis=1) / (norm_A[indices] * norm_B[indices])
            result = {k: np.sqrt(max_tilt_acceleration * velocity[k] / v)
                for k, v in zip(np.where(indices)[0], np.arccos(np.clip(cosines, -1.0, 1.0)))}
            result = {k: (velocity[k] * context.scene.render.fps, v) for k, v in result.items()}
            return {k: n / m for k, (n, m) in result.items() if n > m}

        distance_history, distance_result = {}, []
        def check_distance(frame, points):
            dist = tril + np.triu(np.sqrt(((points[:, None, :] - points) ** 2).sum(-1)))
            x, y = np.where(dist < self.min_distance)
            zpxy = frozenset(zip([int(x) for x in x], [int(y) for y in y]))
            if context.scene.skybrush.safety_check.proximity_warning_target == "ABOVE_MIN_NAV_ALT":
                sc_mna = context.scene.skybrush.safety_check.min_navigation_altitude
                zpxy = [i for i in zpxy if np.all(np.array([points[j][2] for j in i]) > sc_mna)]
            for xy in distance_history.keys() - zpxy:
                distance_result.append((xy, distance_history[xy]))
                del distance_history[xy]
            for xy in zpxy:
                if xy not in distance_history or dist[xy] < distance_history[xy][1]:
                    distance_history[xy] = (frame, dist[xy])

        Vxy_history, Vxy_result = {}, []
        Axy_history, Axy_result = {}, []
        Vz_history, Vz_result = {}, []
        Az_history, Az_result = {}, []
        angle_history, angle_result, vector_previous = {}, [], np.array([(0.,0.,0.)] * len(drones))

        previous_Vxy = None
        previous_Vz = None

        def check_velocity(frame, previous, points):
            nonlocal previous_Vxy, previous_Vz
            vector = points - previous

            Vxy = np.sqrt((vector[:, :2] ** 2).sum(-1)) * context.scene.render.fps
            index = np.where(Vxy > self.max_xy_velocity)[0]
            for i in Vxy_history.keys() - index:
                Vxy_result.append((i, Vxy_history[i]))
                del(Vxy_history[i])
            for i in index:
                if i not in Vxy_history or Vxy[i] > Vxy_history[i][1]:
                    Vxy_history[i] = (frame, Vxy[i])

            if previous_Vxy is not None:
                Axy = np.abs(Vxy - previous_Vxy) * context.scene.render.fps
                index = np.where(Axy > self.max_xy_acceleration)[0]
                for i in Axy_history.keys() - index:
                    Axy_result.append((i, Axy_history[i]))
                    del(Axy_history[i])
                for i in index:
                    if i not in Axy_history or Axy[i] > Axy_history[i][1]:
                        Axy_history[i] = (frame, Axy[i])
            previous_Vxy = Vxy

            Vz = vector[:, 2] * context.scene.render.fps
            index = np.where(Vz > self.max_z_velocity)[0]
            for i in Vz_history.keys() - index:
                Vz_result.append((i, Vz_history[i]))
                del(Vz_history[i])
            for i in index:
                if i not in Vz_history or Vz[i] > Vz_history[i][1]:
                    Vz_history[i] = (frame, Vz[i])

            if previous_Vz is not None:
                Az = np.abs(Vz - previous_Vz) * context.scene.render.fps
                index = np.where(Az > self.max_z_acceleration)[0]
                for i in Az_history.keys() - index:
                    Az_result.append((i, Az_history[i]))
                    del(Az_history[i])
                for i in index:
                    if i not in Az_history or Az[i] > Az_history[i][1]:
                        Az_history[i] = (frame, Az[i])
            previous_Vz = Vz

            angle = calculate_angles(vector[:, :2], vector_previous[:, :2])
            index = angle.keys()
            for i in angle_history.keys() - index:
                if angle_history[i][2] > 5:
                    angle_result.append((i, angle_history[i][:2]))
                del(angle_history[i])
            for i in index:
                if i not in angle_history:
                    angle_history[i] = (frame, angle[i], 1)
                elif angle[i] > angle_history[i][1]:
                    angle_history[i] = (frame, angle[i], angle_history[i][2] + 1)
            np.copyto(vector_previous, vector)

        with suspended_safety_checks(), suspended_light_effects(), ConsoleWindow():
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
            Vxy_result.extend(Vxy_history.items())
            Axy_result.extend(Axy_history.items())
            Vz_result.extend(Vz_history.items())
            Az_result.extend(Az_history.items())
            bpy.types.Scene.validate_trajectories_result = {
                "drones": drones,
                "distance_result": distance_result,
                "Vxy_result": Vxy_result,
                "Axy_result": Axy_result,
                "Vz_result": Vz_result,
                "Az_result": Az_result,
                "angle_result": angle_result
            }
            context.scene.frame_set(frame_current)

        return {"FINISHED"}

    def get_positions(self, context, frame, drones):
        context.scene.frame_set(frame)
        return np.array([get_position_of_object(drone) for drone in drones])
