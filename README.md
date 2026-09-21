# simreach

[![CI](https://github.com/maxmccutcheon59/simreach/actions/workflows/ci.yml/badge.svg)](https://github.com/maxmccutcheon59/simreach/actions/workflows/ci.yml)

**SimReach** — ROS 2 + Gazebo (sim-first) **vision-guided approach** scaffold for portfolio / education.  
Author: Max McCutcheon (`@maxmccutcheon59`) · `MaxMcCutcheon1@outlook.com` · MIT

> **v0.1.0 posture:** No hardware buys. Pure-Python `simreach_vision` is unit-tested without Gazebo. Full sim uses the provided Dockerfile when your host can run it.

## What it does

1. Detect a red marker in an RGB frame (stdlib color blob — no OpenCV required for tests).
2. Compute image-plane error vs camera center.
3. Emit a clamped Cartesian twist (align, then approach) with lost-target software e-stop.

## Quick start (unit tests — no ROS/Gazebo)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
ruff check src tests
```

## Docker (ROS 2 Humble + Gazebo packages)

```bash
docker build -t simreach:v0.1.0 .
docker run --rm simreach:v0.1.0 pytest -q
```

Gazebo GUI may be unavailable in headless CI; see [`docs/INSTALL.md`](docs/INSTALL.md).

## Layout

| Path | Role |
|------|------|
| `src/simreach_vision/` | Unit-testable detector + IBVS-lite controller + safety |
| `src/simreach_bringup/` | ROS 2 ament_python node, launch, params |
| `worlds/simple_table.sdf` | Minimal table + red target |
| `Dockerfile` | Humble + gazebo_ros; non-root user |
| `BOM.md` | Future cheap-arm **research only — do not buy** |
| `SECURITY.md` / `COMPLIANCE_NOTES.md` | Disclosure + legal flags |

## Docs

- [Install](docs/INSTALL.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Changelog](CHANGELOG.md)

## License

MIT — see [LICENSE](LICENSE).
