"""Blob detector tests — uses in-memory fixtures (no Gazebo / OpenCV / Docker)."""

from __future__ import annotations

import pytest

from simreach_vision.detect import detect_color_blob, make_blank_frame, paint_disk, paint_rect
from tests.fixtures.scenes import RED_HI, RED_LO, build_scene, expected_centroid, iter_catalog


def test_detect_missing_on_blank():
    frame = make_blank_frame(64, 48)
    det = detect_color_blob(frame, min_area=5)
    assert det.found is False


def test_detect_red_blob_centroid():
    frame = make_blank_frame(100, 80, fill=(20, 20, 20))
    paint_rect(frame, 45, 35, 54, 44, (220, 60, 60))
    det = detect_color_blob(frame, lo=RED_LO, hi=RED_HI, min_area=10)
    assert det.found is True
    assert abs(det.u - 49.5) < 0.6
    assert abs(det.v - 39.5) < 0.6
    assert det.area == 100
    assert det.score > 0


def test_make_blank_rejects_zero():
    with pytest.raises(ValueError):
        make_blank_frame(0, 10)


def test_paint_disk_rejects_negative_radius():
    frame = make_blank_frame(10, 10)
    with pytest.raises(ValueError):
        paint_disk(frame, 5, 5, -1, (220, 60, 60))


def test_ragged_frame_raises():
    frame = [[[0, 0, 0], [0, 0, 0]], [[0, 0, 0]]]  # ragged
    with pytest.raises(ValueError, match="ragged"):
        detect_color_blob(frame, min_area=1)


def test_empty_frame():
    det = detect_color_blob([], min_area=1)
    assert det.found is False
    assert det.area == 0


@pytest.mark.parametrize("spec", list(iter_catalog()), ids=lambda s: s.name)
def test_catalog_scenes(spec):
    frame = build_scene(spec)
    det = detect_color_blob(frame, lo=RED_LO, hi=RED_HI, min_area=spec.min_area)
    assert det.found is spec.expect_found
    if spec.expect_found:
        expected = expected_centroid(spec)
        assert expected is not None
        eu, ev = expected
        assert abs(det.u - eu) <= spec.centroid_tol
        assert abs(det.v - ev) <= spec.centroid_tol
        assert det.area >= spec.min_area
        assert 0.0 < det.score <= 1.0
    else:
        assert det.score == 0.0


def test_disk_centroid_near_center():
    frame = make_blank_frame(80, 80, fill=(10, 10, 10))
    paint_disk(frame, 40, 40, 8, (230, 50, 50))
    det = detect_color_blob(frame, lo=RED_LO, hi=RED_HI, min_area=20)
    assert det.found is True
    assert abs(det.u - 40.0) < 0.75
    assert abs(det.v - 40.0) < 0.75
