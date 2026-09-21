"""
Lightweight color-blob detector on RGB frames (list/nested tuples or numpy-like).

No OpenCV dependency so unit tests run on a plain Python interpreter.
Frames are HxWx3 with channels in 0..255 (int or float).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

RGB = tuple[int, int, int]


@dataclass(frozen=True)
class Detection:
    """Detected blob in image coordinates."""

    found: bool
    u: float  # column (x)
    v: float  # row (y)
    area: int
    score: float  # 0..1 rough confidence from area fraction


def _get_pixel(frame: Sequence[Sequence[Sequence[float]]], r: int, c: int) -> RGB:
    pix = frame[r][c]
    return int(pix[0]), int(pix[1]), int(pix[2])


def _in_range(rgb: RGB, lo: RGB, hi: RGB) -> bool:
    return all(lo[i] <= rgb[i] <= hi[i] for i in range(3))


def detect_color_blob(
    frame: Sequence[Sequence[Sequence[float]]],
    lo: RGB = (180, 40, 40),
    hi: RGB = (255, 120, 120),
    min_area: int = 20,
) -> Detection:
    """
    Find centroid of pixels inside [lo, hi] inclusive RGB bounds.

    Default band targets a bright-red marker in Gazebo/sim screenshots.
    Returns found=False if area < min_area.

    Notes
    -----
    - Frames must be rectangular (equal row lengths); ragged rows raise ValueError.
    - Empty / zero-size frames return found=False.
    - Score grows with area relative to ``max(min_area * 5, 100)``, capped at 1.0.
    """
    if not frame or not frame[0]:
        return Detection(found=False, u=0.0, v=0.0, area=0, score=0.0)

    h = len(frame)
    w = len(frame[0])
    sum_u = 0.0
    sum_v = 0.0
    area = 0

    for r in range(h):
        row = frame[r]
        if len(row) != w:
            raise ValueError("ragged frame rows are not supported")
        for c in range(w):
            if _in_range(_get_pixel(frame, r, c), lo, hi):
                sum_u += c
                sum_v += r
                area += 1

    if area < min_area:
        return Detection(found=False, u=0.0, v=0.0, area=area, score=0.0)

    u = sum_u / area
    v = sum_v / area
    # Confidence from area vs a modest reference (not full-frame fraction).
    score = min(1.0, area / float(max(min_area * 5, 100)))
    return Detection(found=True, u=u, v=v, area=area, score=score)


def make_blank_frame(width: int, height: int, fill: RGB = (30, 30, 30)) -> list[list[list[int]]]:
    """Allocate a solid-color HxWx3 frame for tests / synthetic scenes."""
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")
    return [[[fill[0], fill[1], fill[2]] for _ in range(width)] for _ in range(height)]


def paint_rect(
    frame: list[list[list[int]]],
    u0: int,
    v0: int,
    u1: int,
    v1: int,
    color: RGB,
) -> None:
    """Fill inclusive rectangle [u0,u1] x [v0,v1] (clipped to frame)."""
    h = len(frame)
    w = len(frame[0])
    for v in range(max(0, v0), min(h, v1 + 1)):
        for u in range(max(0, u0), min(w, u1 + 1)):
            frame[v][u][0] = color[0]
            frame[v][u][1] = color[1]
            frame[v][u][2] = color[2]


def paint_disk(
    frame: list[list[list[int]]],
    cu: int,
    cv: int,
    radius: int,
    color: RGB,
) -> None:
    """
    Fill a filled disk of integer radius centered at (cu, cv), clipped to frame.

    Useful for more realistic marker fixtures than axis-aligned rectangles.
    """
    if radius < 0:
        raise ValueError("radius must be non-negative")
    h = len(frame)
    w = len(frame[0])
    r2 = radius * radius
    for v in range(max(0, cv - radius), min(h, cv + radius + 1)):
        for u in range(max(0, cu - radius), min(w, cu + radius + 1)):
            if (u - cu) * (u - cu) + (v - cv) * (v - cv) <= r2:
                frame[v][u][0] = color[0]
                frame[v][u][1] = color[1]
                frame[v][u][2] = color[2]
