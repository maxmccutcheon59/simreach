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


def test_intrinsics_reject_nonpositive():
    try:
        CameraIntrinsics(0, 480, 1, 1, 0, 0).validate()
        assert False, "expected ValueError"
    except ValueError:
        pass
