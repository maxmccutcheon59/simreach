import pytest

from simreach_vision.geometry import CameraIntrinsics, normalized_error, pixel_to_normalized


def test_pixel_to_normalized_center():
    K = CameraIntrinsics.default_vga()
    x, y = pixel_to_normalized(K.cx, K.cy, K)
    assert abs(x) < 1e-9
    assert abs(y) < 1e-9


def test_normalized_error_right_of_center():
    K = CameraIntrinsics.default_vga()
    eu, ev = normalized_error(K.cx + K.fx, K.cy, K)
    assert abs(eu - 1.0) < 1e-9
    assert abs(ev) < 1e-9


def test_normalized_error_custom_target():
    K = CameraIntrinsics.default_vga()
    eu, ev = normalized_error(K.cx, K.cy, K, target_u=K.cx + K.fx, target_v=K.cy)
    assert abs(eu - (-1.0)) < 1e-9
    assert abs(ev) < 1e-9


def test_intrinsics_reject_nonpositive():
    with pytest.raises(ValueError):
        CameraIntrinsics(0, 480, 1, 1, 0, 0).validate()


def test_intrinsics_reject_nonpositive_focal():
    with pytest.raises(ValueError):
        CameraIntrinsics(640, 480, 0, 1, 320, 240).validate()
