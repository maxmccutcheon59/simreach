# Architecture — SimReach v0.2.0

```
sensor_msgs/Image (rgb8) ──► detect_color_blob ──► Detection
                                                    │
                                                    ▼
                                         ApproachController.step
                                                    │
                                                    ▼
                              ApproachCommand (vx,vy,vz) ──clamp──► Twist /cmd_vel

Pure-Python path (no Gazebo):
  paint_disk / fixtures ──► detect ──► controller ──► JSONL (scripts/recorded_run.py)
```

## Layers

1. **`simreach_vision`** (pure Python, stdlib-only runtime) — detector (`paint_rect` / `paint_disk`), geometry, IBVS-lite controller, safety clamps, recorded-run helper. Fully unit-tested without ROS/Gazebo/Docker.
2. **`simreach_bringup`** (ROS 2 ament_python) — thin `approach_node`, params YAML, launch stub (kept for sim bring-up).
3. **`worlds/simple_table.sdf`** — minimal table + red marker for Gazebo when available.
4. **Dockerfile** — `ros:humble-ros-base` + gazebo_ros pkgs; non-root user; pytest default CMD. **Optional** — not required to pass tests.
5. **`tests/fixtures`** — declarative synthetic scenes for blob-detector coverage.
6. **`scripts/recorded_run.py`** — example logged approach without Gazebo.

## Safety (software)

- Soft speed clamps (`SafetyLimits`)
- Lost-target e-stop after N consecutive misses
- No shell/`eval` on image bytes; size-checked buffer parse only
- Container runs as non-root when Docker is used

## Out of scope (v0.2.0)

- Real robot drivers, motor torque limits, or purchased hardware (**$0**)
- Learned/ML perception / face or biometric models
- Multi-arm coordination / force control
