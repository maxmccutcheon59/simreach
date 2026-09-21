import pytest

from simreach_vision.safety import SafetyLimits, clamp_twist, should_estop


def test_clamp_twist():
    lim = SafetyLimits(max_speed_mps=0.05, max_lateral_mps=0.03, max_vertical_mps=0.02)
    vx, vy, vz = clamp_twist(1.0, -1.0, 0.5, lim)
    assert vx == 0.05
    assert vy == -0.03
    assert vz == 0.02


def test_should_estop():
    lim = SafetyLimits(lost_target_frames_estop=5)
    assert should_estop(4, lim) is False
    assert should_estop(5, lim) is True


def test_limits_reject_nonpositive_speed():
    with pytest.raises(ValueError):
        SafetyLimits(max_speed_mps=0).validate()


def test_limits_reject_bad_estop_frames():
    with pytest.raises(ValueError):
        SafetyLimits(lost_target_frames_estop=0).validate()
