"""SimReach vision-guided approach logic (ROS-independent, unit-testable)."""

from .approach import ApproachCommand, ApproachController, ApproachState
from .detect import Detection, detect_color_blob, make_blank_frame, paint_rect
from .geometry import CameraIntrinsics, normalized_error, pixel_to_normalized
from .safety import SafetyLimits, clamp_twist, should_estop

__all__ = [
    "ApproachCommand",
    "ApproachController",
    "ApproachState",
    "Detection",
    "detect_color_blob",
    "make_blank_frame",
    "paint_rect",
    "CameraIntrinsics",
    "pixel_to_normalized",
    "normalized_error",
    "SafetyLimits",
    "clamp_twist",
    "should_estop",
]

__version__ = "0.1.0"
