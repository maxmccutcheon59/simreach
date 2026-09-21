"""Synthetic blob-detector scene fixtures (no binary image assets required)."""

from .scenes import (
    RED_HI,
    RED_LO,
    SceneSpec,
    build_scene,
    expected_centroid,
    iter_catalog,
)

__all__ = [
    "RED_LO",
    "RED_HI",
    "SceneSpec",
    "build_scene",
    "expected_centroid",
    "iter_catalog",
]
