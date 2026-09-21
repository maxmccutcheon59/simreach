"""
Image-based visual approach controller (IBVS-lite).

Maps image-plane error of a detected marker to a small Cartesian twist so a
simulated end-effector / camera can center and advance toward the target.
Pure Python — no ROS, Gazebo, or OpenCV required.
"""

from __future__ import annotations

from dataclasses import dataclass

from .detect import Detection
from .geometry import CameraIntrinsics, normalized_error
from .safety import SafetyLimits, clamp_twist, should_estop


@dataclass(frozen=True)
class ApproachCommand:
    """Camera/base-frame twist suggestion (m/s) plus status flags."""

    vx: float  # forward / approach (toward scene)
    vy: float  # lateral
    vz: float  # vertical
    done: bool
    estop: bool
    reason: str


@dataclass
class ApproachState:
    """Mutable controller bookkeeping across frames."""

    lost_streak: int = 0
    frames: int = 0


@dataclass
class ApproachController:
    """
    Proportional IBVS-style controller.

    Convention (camera looking along +X toward the workspace):
    - Image error eu (right of center) -> negative vy (slide left), gain ky
    - Image error ev (below center) -> positive vz, gain kz
    - When centered within pixel_tol, advance with +vx = approach_speed
    """

    K: CameraIntrinsics
    limits: SafetyLimits
    ky: float = 0.08
    kz: float = 0.08
    approach_speed: float = 0.02
    pixel_tol: float = 8.0
    min_score: float = 0.05

    def __post_init__(self) -> None:
        self.K.validate()
        self.limits.validate()
        if self.approach_speed <= 0:
            raise ValueError("approach_speed must be positive")
        if self.pixel_tol <= 0:
            raise ValueError("pixel_tol must be positive")

    def step(self, det: Detection, state: ApproachState) -> ApproachCommand:
        state.frames += 1

        if not det.found or det.score < self.min_score:
            state.lost_streak += 1
            if should_estop(state.lost_streak, self.limits):
                return ApproachCommand(
                    0.0, 0.0, 0.0, done=False, estop=True, reason="lost_target_estop"
                )
            return ApproachCommand(
                0.0, 0.0, 0.0, done=False, estop=False, reason="target_lost_hold"
            )

        state.lost_streak = 0
        eu, ev = normalized_error(det.u, det.v, self.K)
        # Pixel residual for "centered" check
        du = det.u - self.K.cx
        dv = det.v - self.K.cy
        centered = abs(du) <= self.pixel_tol and abs(dv) <= self.pixel_tol

        if centered:
            vx, vy, vz = clamp_twist(self.approach_speed, 0.0, 0.0, self.limits)
            # "Done" is reserved for higher-level stop (depth/contact); here we keep approaching.
            return ApproachCommand(vx, vy, vz, done=False, estop=False, reason="approach")

        # Lateral/vertical correction; pause forward motion until centered.
        raw_vy = -self.ky * eu
        raw_vz = self.kz * ev
        vx, vy, vz = clamp_twist(0.0, raw_vy, raw_vz, self.limits)
        return ApproachCommand(vx, vy, vz, done=False, estop=False, reason="align")
