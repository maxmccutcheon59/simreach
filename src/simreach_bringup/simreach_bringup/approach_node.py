"""
ROS 2 approach node — thin wrapper around simreach_vision.

Runs without a real camera by accepting sensor_msgs/Image when rclpy is available.
When imported outside a ROS environment, helper functions remain usable for tests.

This module deliberately avoids importing rclpy at module top-level so
`python -c "import simreach_bringup.approach_node"` works in CI without ROS.
"""

from __future__ import annotations

from typing import Any

# Shared logic (always available)
from simreach_vision import (  # noqa: F401 — re-exported for node users
    ApproachController,
    ApproachState,
    CameraIntrinsics,
    Detection,
    SafetyLimits,
    detect_color_blob,
)


def rgb_bytes_to_frame(
    data: bytes, height: int, width: int, step: int | None = None
) -> list[list[list[int]]]:
    """
    Convert tightly packed RGB8 image bytes to HxWx3 nested lists.

    Raises ValueError on size mismatch. Does not execute or eval anything.
    """
    if height <= 0 or width <= 0:
        raise ValueError("height and width must be positive")
    row_stride = step if step is not None else width * 3
    expected = row_stride * height
    if len(data) < expected:
        raise ValueError(f"image buffer too small: got {len(data)}, need {expected}")
    frame: list[list[list[int]]] = []
    for r in range(height):
        row: list[list[int]] = []
        base = r * row_stride
        for c in range(width):
            i = base + c * 3
            row.append([data[i], data[i + 1], data[i + 2]])
        frame.append(row)
    return frame


def build_controller_from_params(params: dict[str, Any]) -> ApproachController:
    """Construct controller from a plain dict (YAML / ROS params)."""
    K = CameraIntrinsics(
        width=int(params.get("image_width", 640)),
        height=int(params.get("image_height", 480)),
        fx=float(params.get("fx", 500.0)),
        fy=float(params.get("fy", 500.0)),
        cx=float(params.get("cx", 320.0)),
        cy=float(params.get("cy", 240.0)),
    )
    limits = SafetyLimits(
        max_speed_mps=float(params.get("max_speed_mps", 0.05)),
        max_lateral_mps=float(params.get("max_lateral_mps", 0.03)),
        max_vertical_mps=float(params.get("max_vertical_mps", 0.03)),
        lost_target_frames_estop=int(params.get("lost_target_frames_estop", 5)),
    )
    return ApproachController(
        K=K,
        limits=limits,
        ky=float(params.get("ky", 0.08)),
        kz=float(params.get("kz", 0.08)),
        approach_speed=float(params.get("approach_speed", 0.02)),
        pixel_tol=float(params.get("pixel_tol", 8.0)),
        min_score=float(params.get("min_score", 0.05)),
    )


def main(args: list[str] | None = None) -> None:
    """Entry point when ROS 2 + rclpy are installed (see Dockerfile)."""
    try:
        import rclpy
        from geometry_msgs.msg import Twist
        from rclpy.node import Node
        from sensor_msgs.msg import Image
    except ImportError as exc:  # pragma: no cover - exercised in sim image only
        raise SystemExit(
            "rclpy/ROS 2 not available. Run unit tests with pytest, or use the Dockerfile "
            "ROS image. Core logic: `pip install -e .` then `pytest`."
        ) from exc

    class ApproachNode(Node):
        def __init__(self) -> None:
            super().__init__("simreach_approach")
            self.declare_parameter("image_topic", "/camera/image_raw")
            self.declare_parameter("cmd_topic", "/cmd_vel")
            self.declare_parameter("max_speed_mps", 0.05)
            self.declare_parameter("max_lateral_mps", 0.03)
            self.declare_parameter("max_vertical_mps", 0.03)
            self.declare_parameter("lost_target_frames_estop", 5)
            self.declare_parameter("ky", 0.08)
            self.declare_parameter("kz", 0.08)
            self.declare_parameter("approach_speed", 0.02)
            self.declare_parameter("pixel_tol", 8.0)
            self.declare_parameter("image_width", 640)
            self.declare_parameter("image_height", 480)
            self.declare_parameter("fx", 500.0)
            self.declare_parameter("fy", 500.0)
            self.declare_parameter("cx", 320.0)
            self.declare_parameter("cy", 240.0)

            params = {n: self.get_parameter(n).value for n in (
                "max_speed_mps", "max_lateral_mps", "max_vertical_mps",
                "lost_target_frames_estop", "ky", "kz", "approach_speed", "pixel_tol",
                "image_width", "image_height", "fx", "fy", "cx", "cy",
            )}
            self._controller = build_controller_from_params(params)
            self._state = ApproachState()
            img_topic = self.get_parameter("image_topic").value
            cmd_topic = self.get_parameter("cmd_topic").value
            self._pub = self.create_publisher(Twist, cmd_topic, 10)
            self._sub = self.create_subscription(Image, img_topic, self._on_image, 10)
            self.get_logger().info(
                f"SimReach approach node ready (image={img_topic}, cmd={cmd_topic})"
            )

        def _on_image(self, msg: Image) -> None:
            if msg.encoding not in ("rgb8", "bgr8"):
                self.get_logger().warn(f"unsupported encoding {msg.encoding}; skipping")
                return
            # Only accept rgb8 for the pure detector; bgr8 would need channel swap.
            if msg.encoding != "rgb8":
                self.get_logger().warn("use rgb8 for simreach detector; skipping frame")
                return
            try:
                frame = rgb_bytes_to_frame(bytes(msg.data), msg.height, msg.width, msg.step)
            except ValueError as err:
                self.get_logger().error(f"bad image: {err}")
                return
            det = detect_color_blob(frame)
            cmd = self._controller.step(det, self._state)
            twist = Twist()
            if not cmd.estop:
                twist.linear.x = float(cmd.vx)
                twist.linear.y = float(cmd.vy)
                twist.linear.z = float(cmd.vz)
            self._pub.publish(twist)
            if cmd.estop:
                self.get_logger().warn(f"ESTOP: {cmd.reason}")

    rclpy.init(args=args)
    node = ApproachNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
