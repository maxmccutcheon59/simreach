# Approach controller — SimReach

Pure-Python IBVS-lite controller in `simreach_vision.approach`.  
**No Gazebo, ROS, or OpenCV required** to understand or unit-test this path.

## Goal

Given a color-blob `Detection` each frame, emit a soft-clamped Cartesian twist
`(vx, vy, vz)` so a simulated camera / end-effector can:

1. **Align** — center the marker on the optical axis (image principal point).
2. **Approach** — once centered, creep forward at `approach_speed`.
3. **Hold / e-stop** — if the target is lost, zero motion, then soft e-stop.

## Coordinate conventions

Camera looks along **+X** into the workspace (sim convention used here):

| Symbol | Meaning |
|--------|---------|
| `u`, `v` | Image column / row (pixels) |
| `cx`, `cy` | Principal point (usually image center) |
| `eu`, `ev` | Normalized image-plane error (see `geometry.normalized_error`) |
| `vx` | Forward approach speed (m/s, sim scale) |
| `vy` | Lateral (positive = right in camera frame) |
| `vz` | Vertical (positive = down in image → up in this mapping) |

Control mapping:

- Target **right** of center (`eu > 0`) → command **negative** `vy` (slide left), gain `ky`.
- Target **below** center (`ev > 0`) → command **positive** `vz`, gain `kz`.
- Within `pixel_tol` of `(cx, cy)` → `vx = approach_speed`, `vy = vz = 0`.

## State machine (`ApproachCommand.reason`)

```
          found & score OK
     ┌────────────────────────┐
     │                        ▼
┌────┴────┐   not centered   ┌────────┐
│  start  │ ───────────────► │ align  │  (vx=0, vy/vz from error)
└────┬────┘                  └───┬────┘
     │                           │ centered
     │                           ▼
     │                      ┌──────────┐
     │                      │ approach │  (vx=approach_speed)
     │                      └──────────┘
     │
     │ lost / low score
     ▼
┌─────────────────┐  streak < N   ┌──────────────────┐
│ target_lost_hold│ ────────────► │ (keep holding)   │
└────────┬────────┘               └──────────────────┘
         │ streak ≥ lost_target_frames_estop
         ▼
┌──────────────────┐
│ lost_target_estop│  (all zeros, estop=True)
└──────────────────┘
```

Recovering a valid detection resets `lost_streak` to 0.

## Tuning knobs

| Param | Default | Role |
|-------|---------|------|
| `ky`, `kz` | `0.08` | Proportional gains on normalized error |
| `approach_speed` | `0.02` | Forward creep when centered (m/s) |
| `pixel_tol` | `8.0` | Pixel half-width for “centered” |
| `min_score` | `0.05` | Treat weaker blobs as lost |
| `SafetyLimits.max_*` | see `safety.py` | Soft clamps (always applied) |
| `lost_target_frames_estop` | `5` | Misses before soft e-stop |

Start with defaults; raise gains slowly. Soft clamps are **research aids**, not
certified functional safety (see `SECURITY.md` / `BOM.md`).

## Try it (no Docker)

```bash
pip install -e ".[dev]"
python scripts/recorded_run.py --output examples/last_run.jsonl --lost-tail 6
pytest -q
```

ROS stubs remain in `simreach_bringup` for when you have Humble + Gazebo.
