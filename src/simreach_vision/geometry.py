"""Camera geometry helpers for image-based approach (no OpenCV required)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CameraIntrinsics:
    """Pinhole intrinsics in pixels. fx/fy focal lengths; cx/cy principal point."""

    width: int
    height: int
    fx: float
    fy: float
    cx: float
    cy: float

    @classmethod
    def default_vga(cls) -> CameraIntrinsics:
        """Reasonable defaults for a 640x480 sim camera."""
        w, h = 640, 480
        fx = fy = 500.0
        return cls(width=w, height=h, fx=fx, fy=fy, cx=w / 2.0, cy=h / 2.0)

    def validate(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("width and height must be positive")
        if self.fx <= 0 or self.fy <= 0:
            raise ValueError("fx and fy must be positive")


def pixel_to_normalized(u: float, v: float, K: CameraIntrinsics) -> tuple[float, float]:
    """Map pixel (u,v) to camera-normalized image plane coords (x,y)."""
    K.validate()
    return (u - K.cx) / K.fx, (v - K.cy) / K.fy


def normalized_error(
    u: float,
    v: float,
    K: CameraIntrinsics,
    target_u: float | None = None,
    target_v: float | None = None,
) -> tuple[float, float]:
    """
    Image-plane error from current blob center to desired image point.

    Default desired point is the principal point (optical axis / image center).
    Positive eu means target is to the right of desired; positive ev below.
    """
    tu = K.cx if target_u is None else target_u
    tv = K.cy if target_v is None else target_v
    xu, yu = pixel_to_normalized(u, v, K)
    xt, yt = pixel_to_normalized(tu, tv, K)
    return xu - xt, yu - yt
