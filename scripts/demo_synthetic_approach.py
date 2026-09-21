#!/usr/bin/env python3
"""Run a few synthetic frames through the approach controller (no ROS)."""

from __future__ import annotations

from simreach_vision import (
    ApproachController,
    ApproachState,
    CameraIntrinsics,
    SafetyLimits,
    detect_color_blob,
    make_blank_frame,
    paint_rect,
)


def main() -> None:
    K = CameraIntrinsics.default_vga()
    ctrl = ApproachController(K=K, limits=SafetyLimits())
    state = ApproachState()
    # Target starts right of center, then we "teleport" it toward center across frames
    positions = [(420, 240), (380, 240), (340, 240), (320, 240), (320, 240)]
    for i, (u, v) in enumerate(positions):
        frame = make_blank_frame(K.width, K.height)
        paint_rect(frame, u - 8, v - 8, u + 8, v + 8, (220, 60, 60))
        det = detect_color_blob(frame)
        cmd = ctrl.step(det, state)
        print(
            f"frame={i} found={det.found} u={det.u:.1f} v={det.v:.1f} "
            f"-> vx={cmd.vx:.3f} vy={cmd.vy:.3f} vz={cmd.vz:.3f} reason={cmd.reason}"
        )


if __name__ == "__main__":
    main()
