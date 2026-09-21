"""ROS-free tests for bringup helpers (import path without rclpy)."""

import sys
from pathlib import Path

import pytest

# Allow importing the bringup package from src layout without installing ament.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "simreach_bringup"))

from simreach_bringup.approach_node import (  # noqa: E402
    build_controller_from_params,
    rgb_bytes_to_frame,
)


def test_rgb_bytes_to_frame():
    data = bytes(
        [
            255, 0, 0,
            0, 255, 0,
            0, 0, 255,
            10, 20, 30,
        ]
    )
    frame = rgb_bytes_to_frame(data, height=2, width=2)
    assert frame[0][0] == [255, 0, 0]
    assert frame[1][1] == [10, 20, 30]


def test_rgb_bytes_rejects_short_buffer():
    with pytest.raises(ValueError):
        rgb_bytes_to_frame(b"\x00\x01", height=2, width=2)


def test_rgb_bytes_rejects_nonpositive_dims():
    with pytest.raises(ValueError):
        rgb_bytes_to_frame(b"\x00" * 12, height=0, width=2)


def test_build_controller_from_params():
    c = build_controller_from_params({"approach_speed": 0.01, "pixel_tol": 5.0})
    assert c.approach_speed == 0.01
    assert c.pixel_tol == 5.0
