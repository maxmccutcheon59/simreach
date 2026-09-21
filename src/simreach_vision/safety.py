"""Soft safety clamps for approach velocity commands (sim / future hardware)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyLimits:
    """Symmetric Cartesian speed limits in m/s (sim scale; not a hardware warranty)."""

    max_speed_mps: float = 0.05
    max_lateral_mps: float = 0.03
    max_vertical_mps: float = 0.03
    lost_target_frames_estop: int = 5

    def validate(self) -> None:
        if self.max_speed_mps <= 0 or self.max_lateral_mps <= 0 or self.max_vertical_mps <= 0:
            raise ValueError("speed limits must be positive")
        if self.lost_target_frames_estop < 1:
            raise ValueError("lost_target_frames_estop must be >= 1")


def clamp(x: float, lim: float) -> float:
    if x > lim:
        return lim
    if x < -lim:
        return -lim
    return x


def clamp_twist(
    vx: float,
    vy: float,
    vz: float,
    limits: SafetyLimits,
) -> tuple[float, float, float]:
    """Clamp camera-frame (or base) twist components to configured soft limits."""
    limits.validate()
    return (
        clamp(vx, limits.max_speed_mps),
        clamp(vy, limits.max_lateral_mps),
        clamp(vz, limits.max_vertical_mps),
    )


def should_estop(lost_streak: int, limits: SafetyLimits) -> bool:
    """True when target has been missing for too many consecutive frames."""
    limits.validate()
    return lost_streak >= limits.lost_target_frames_estop
