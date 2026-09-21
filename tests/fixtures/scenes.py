"""
Catalog of synthetic RGB scenes for blob-detector tests.

Scenes are built in memory (no PNG/JPEG fixtures) so CI stays dependency-light
and Docker is never required for pytest.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Literal

from simreach_vision.detect import RGB, make_blank_frame, paint_disk, paint_rect

Shape = Literal["rect", "disk"]

RED_LO: RGB = (180, 40, 40)
RED_HI: RGB = (255, 120, 120)
RED: RGB = (220, 60, 60)
BG: RGB = (20, 20, 20)


@dataclass(frozen=True)
class SceneSpec:
    """Declarative fixture describing one synthetic frame."""

    name: str
    width: int
    height: int
    shape: Shape
    # For rect: (u0, v0, u1, v1). For disk: (cu, cv, radius, unused).
    geom: tuple[int, int, int, int]
    color: RGB = RED
    fill: RGB = BG
    expect_found: bool = True
    min_area: int = 10
    # Optional absolute tolerance on centroid when expect_found.
    centroid_tol: float = 1.0


def expected_centroid(spec: SceneSpec) -> tuple[float, float] | None:
    """Analytic centroid for the painted geometry (None if not expected found)."""
    if not spec.expect_found:
        return None
    if spec.shape == "rect":
        u0, v0, u1, v1 = spec.geom
        # Inclusive integer bounds → midpoint of discrete pixel centers.
        return (u0 + u1) / 2.0, (v0 + v1) / 2.0
    cu, cv, _radius, _ = spec.geom
    return float(cu), float(cv)


def build_scene(spec: SceneSpec) -> list[list[list[int]]]:
    """Materialize a SceneSpec into an HxWx3 frame."""
    frame = make_blank_frame(spec.width, spec.height, fill=spec.fill)
    if spec.shape == "rect":
        u0, v0, u1, v1 = spec.geom
        paint_rect(frame, u0, v0, u1, v1, spec.color)
    else:
        cu, cv, radius, _ = spec.geom
        paint_disk(frame, cu, cv, radius, spec.color)
    return frame


def catalog() -> list[SceneSpec]:
    """Named scenes used by parameterized detector tests."""
    return [
        SceneSpec(
            name="blank_no_blob",
            width=64,
            height=48,
            shape="rect",
            geom=(0, 0, -1, -1),  # paint nothing meaningful; empty rect clipped
            expect_found=False,
            min_area=5,
        ),
        SceneSpec(
            name="red_rect_center",
            width=100,
            height=80,
            shape="rect",
            geom=(45, 35, 54, 44),
            expect_found=True,
            min_area=10,
        ),
        SceneSpec(
            name="red_rect_top_left",
            width=80,
            height=60,
            shape="rect",
            geom=(2, 2, 11, 11),
            expect_found=True,
            min_area=10,
        ),
        SceneSpec(
            name="red_disk_offset",
            width=120,
            height=90,
            shape="disk",
            geom=(80, 30, 6, 0),
            expect_found=True,
            min_area=20,
            centroid_tol=1.5,
        ),
        SceneSpec(
            name="tiny_blob_below_min_area",
            width=40,
            height=40,
            shape="rect",
            geom=(18, 18, 19, 19),  # 4 pixels
            expect_found=False,
            min_area=20,
        ),
        SceneSpec(
            name="out_of_band_green",
            width=60,
            height=60,
            shape="rect",
            geom=(20, 20, 35, 35),
            color=(40, 220, 40),
            expect_found=False,
            min_area=10,
        ),
        SceneSpec(
            name="clipped_disk_edge",
            width=50,
            height=50,
            shape="disk",
            geom=(2, 25, 5, 0),
            expect_found=True,
            min_area=10,
            centroid_tol=2.5,
        ),
    ]


def iter_catalog() -> Iterator[SceneSpec]:
    yield from catalog()
