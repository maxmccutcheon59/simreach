# Architecture — SimReach v0.1.0

```
sensor_msgs/Image (rgb8) ──► detect_color_blob ──► Detection
                                                    │
                                                    ▼
                                         ApproachController.step
                                                    │
                                                    ▼
                              ApproachCommand (vx,vy,vz) ──clamp──► Twist /cmd_vel
```

## Layers

1. **`simreach_vision`** (pure Python, stdlib-only runtime) — detector, geometry, IBVS-lite controller, safety clamps. Fully unit-tested without ROS/Gazebo.
2. **`simreach_bringup`** (ROS 2 ament_python) — thin `approach_node`, params YAML, launch stub.
3. **`worlds/simple_table.sdf`** — minimal table + red marker for Gazebo when available.
4. **Dockerfile** — `ros:humble-ros-base` + gazebo_ros pkgs; non-root user; pytest default CMD.

## Safety (software)

- Soft speed clamps (`SafetyLimits`)
- Lost-target e-stop after N consecutive misses
- No shell/`eval` on image bytes; size-checked buffer parse only
- Container runs as non-root

## Out of scope (v0.1.0)

- Real robot drivers, motor torque limits, or purchased hardware
- Learned/ML perception
- Multi-arm coordination / force control
