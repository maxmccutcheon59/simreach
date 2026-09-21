from simreach_vision.approach import ApproachController, ApproachState
from simreach_vision.detect import Detection
from simreach_vision.geometry import CameraIntrinsics
from simreach_vision.safety import SafetyLimits


def _ctrl() -> ApproachController:
    return ApproachController(
        K=CameraIntrinsics.default_vga(),
        limits=SafetyLimits(
            max_speed_mps=0.05,
            max_lateral_mps=0.03,
            max_vertical_mps=0.03,
            lost_target_frames_estop=3,
        ),
        pixel_tol=8.0,
        approach_speed=0.02,
    )


def test_align_moves_left_when_target_on_right():
    c = _ctrl()
    st = ApproachState()
    # Target to the right of center -> expect negative vy
    det = Detection(found=True, u=c.K.cx + 40, v=c.K.cy, area=100, score=0.5)
    cmd = c.step(det, st)
    assert cmd.estop is False
    assert cmd.reason == "align"
    assert cmd.vx == 0.0
    assert cmd.vy < 0.0


def test_centered_advances():
    c = _ctrl()
    st = ApproachState()
    det = Detection(found=True, u=c.K.cx, v=c.K.cy, area=100, score=0.5)
    cmd = c.step(det, st)
    assert cmd.reason == "approach"
    assert cmd.vx == 0.02
    assert cmd.vy == 0.0
    assert cmd.vz == 0.0


def test_lost_target_estop_after_streak():
    c = _ctrl()
    st = ApproachState()
    miss = Detection(found=False, u=0, v=0, area=0, score=0.0)
    r1 = c.step(miss, st)
    r2 = c.step(miss, st)
    r3 = c.step(miss, st)
    assert r1.estop is False and r1.reason == "target_lost_hold"
    assert r2.estop is False
    assert r3.estop is True and r3.reason == "lost_target_estop"
    assert r3.vx == 0.0 and r3.vy == 0.0 and r3.vz == 0.0


def test_lateral_clamped_to_limits():
    c = ApproachController(
        K=CameraIntrinsics.default_vga(),
        limits=SafetyLimits(max_speed_mps=0.05, max_lateral_mps=0.01, max_vertical_mps=0.01),
        ky=10.0,  # huge gain -> would exceed clamp without safety
        kz=10.0,
    )
    st = ApproachState()
    det = Detection(found=True, u=c.K.cx + 200, v=c.K.cy, area=50, score=1.0)
    cmd = c.step(det, st)
    assert abs(cmd.vy) <= 0.01 + 1e-12
