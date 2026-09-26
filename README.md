# simreach

[![CI](https://github.com/maxmccutcheon59/simreach/actions/workflows/ci.yml/badge.svg)](https://github.com/maxmccutcheon59/simreach/actions/workflows/ci.yml)

**SimReach** — ROS 2 + Gazebo (sim-first) **vision-guided approach** for a robot, with a unit-tested core.  
Author: Max McCutcheon (`@maxmccutcheon59`) · `MaxMcCutcheon1@outlook.com` · MIT

> **v0.2.0:** no hardware needed. Pure-Python `simreach_vision` is unit-tested **without Gazebo or Docker**. ROS stubs + optional Dockerfile remain for full sim. See the recorded-run example below.

## What it does

1. Detect a red marker in an RGB frame (stdlib color blob — no OpenCV required for tests).
2. Compute image-plane error vs camera center.
3. Emit a clamped Cartesian twist (align, then approach) with lost-target software e-stop.

## Quick start (unit tests — no ROS / Gazebo / Docker)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
ruff check src tests
```

## Recorded run (pure Python demo)

Replay a synthetic marker path through the detector + controller and write a JSONL log:

```bash
python scripts/recorded_run.py --output examples/last_run.jsonl --lost-tail 6
```

No Gazebo. Details: [`docs/CONTROLLER.md`](docs/CONTROLLER.md).

## Docker (optional — ROS 2 Humble + Gazebo packages)

```bash
docker build -t simreach:v0.2.0 .
docker run --rm simreach:v0.2.0 pytest -q
```

Gazebo GUI may be unavailable in headless CI; see [`docs/INSTALL.md`](docs/INSTALL.md).

## Layout

| Path | Role |
|------|------|
| `src/simreach_vision/` | Unit-testable detector + IBVS-lite controller + safety + recorded-run |
| `src/simreach_bringup/` | ROS 2 ament_python node, launch, params (**stubs kept**) |
| `tests/fixtures/` | Declarative blob-detector scenes (in-memory, no binary assets) |
| `scripts/recorded_run.py` | Example logged approach without Gazebo |
| `worlds/simple_table.sdf` | Minimal table + red target |
| `Dockerfile` | Humble + gazebo_ros; non-root user (**optional**) |
| `BOM.md` | Future cheap-arm **research only — do not buy** |
| `SECURITY.md` / `COMPLIANCE_NOTES.md` | Disclosure + legal flags |

## Docs

- [Install](docs/INSTALL.md)
- [Controller](docs/CONTROLLER.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Changelog](CHANGELOG.md)

## License

MIT — see [LICENSE](LICENSE).
