"""
Pure-Python recorded approach run (no Gazebo / ROS / Docker).

Simulates a red marker drifting toward image center across frames, runs the
detector + ApproachController, and optionally writes a JSONL log.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .approach import ApproachController, ApproachState
from .detect import detect_color_blob, make_blank_frame, paint_disk
from .geometry import CameraIntrinsics
from .safety import SafetyLimits


def default_waypoints(width: int, height: int) -> list[tuple[int, int]]:
    """Marker path from right-of-center toward principal point (scales with frame)."""
    cx = width // 2
    cy = height // 2
    # Start ~25% of width right of center, step inward.
    offsets = [width // 4, width // 6, width // 10, width // 20, 4, 0, 0, 0]
    return [(cx + off, cy) for off in offsets]


# Back-compat alias for VGA demos / CLI docs
DEFAULT_WAYPOINTS: list[tuple[int, int]] = default_waypoints(640, 480)


def run_recorded_sequence(
    *,
    output_path: Path | str | None = None,
    waypoints: list[tuple[int, int]] | None = None,
    width: int = 640,
    height: int = 480,
    radius: int = 10,
    lost_tail: int = 0,
) -> list[dict[str, Any]]:
    """
    Run detector+controller over synthetic frames; return list of row dicts.

    Parameters
    ----------
    output_path
        If set, write one JSON object per line (UTF-8 JSONL). Parent dirs created.
    waypoints
        Marker centers ``(u, v)`` per frame. Defaults to ``default_waypoints(width, height)``.
    width, height
        Frame size (must match camera intrinsics used here).
    radius
        Disk radius for the painted red marker.
    lost_tail
        Extra blank frames after waypoints (exercises lost-target hold / e-stop).
    """
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")
    if radius < 0:
        raise ValueError("radius must be non-negative")

    K = CameraIntrinsics(
        width=width,
        height=height,
        fx=float(max(width, 1)) * 0.78,
        fy=float(max(height, 1)) * 1.04,
        cx=width / 2.0,
        cy=height / 2.0,
    )
    ctrl = ApproachController(K=K, limits=SafetyLimits())
    state = ApproachState()
    pts = list(waypoints if waypoints is not None else default_waypoints(width, height))

    # Keep painted disks mostly inside the frame for small test sizes.
    safe_radius = min(radius, max(1, min(width, height) // 8))

    rows: list[dict[str, Any]] = []
    for i, (u, v) in enumerate(pts):
        frame = make_blank_frame(width, height)
        paint_disk(frame, u, v, safe_radius, (220, 60, 60))
        det = detect_color_blob(frame)
        cmd = ctrl.step(det, state)
        rows.append(
            {
                "frame": i,
                "marker_u": u,
                "marker_v": v,
                "found": det.found,
                "det_u": round(det.u, 3),
                "det_v": round(det.v, 3),
                "area": det.area,
                "score": round(det.score, 4),
                "vx": round(cmd.vx, 5),
                "vy": round(cmd.vy, 5),
                "vz": round(cmd.vz, 5),
                "reason": cmd.reason,
                "estop": cmd.estop,
                "lost_streak": state.lost_streak,
            }
        )

    for j in range(lost_tail):
        frame = make_blank_frame(width, height)
        det = detect_color_blob(frame)
        cmd = ctrl.step(det, state)
        i = len(pts) + j
        rows.append(
            {
                "frame": i,
                "marker_u": None,
                "marker_v": None,
                "found": det.found,
                "det_u": round(det.u, 3),
                "det_v": round(det.v, 3),
                "area": det.area,
                "score": round(det.score, 4),
                "vx": round(cmd.vx, 5),
                "vy": round(cmd.vy, 5),
                "vz": round(cmd.vz, 5),
                "reason": cmd.reason,
                "estop": cmd.estop,
                "lost_streak": state.lost_streak,
            }
        )

    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row, separators=(",", ":")) + "\n")

    return rows
