# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-09-21

### Added

- `paint_disk` helper for more realistic synthetic markers.
- `tests/fixtures` — declarative blob-detector scene catalog + parameterized tests.
- `simreach_vision.recorded_run` + `scripts/recorded_run.py` — pure-Python logged approach (JSONL) **without Gazebo**.
- `docs/CONTROLLER.md` — coordinate conventions, state machine, tuning knobs.
- Broader unit coverage: vertical align, low-score-as-lost, streak recovery, geometry/safety validation, recorded-run e-stop tail.

### Changed

- Version bump to **0.2.0**; README / INSTALL / ARCHITECTURE / BOM / Dockerfile tags updated.
- README clarifies that **Docker is optional** and not required to pass tests.
- Controller module docs expanded (still ROS-stub compatible).

### Security

- Soft clamps + lost-target e-stop unchanged; recorded-run writes local JSONL only (no network, no PII).
- `$0` hardware posture retained; BOM remains research-only.

## [0.1.0] - 2026-09-21

### Added

- `simreach_vision` — stdlib-only color-blob detector, camera geometry, IBVS-lite approach controller, soft safety clamps.
- `simreach_bringup` — ROS 2 ament_python package stub (approach node, launch, params).
- `worlds/simple_table.sdf` — minimal Gazebo world with red target marker.
- `Dockerfile` — ROS 2 Humble base + Gazebo ROS packages; non-root user; pytest default.
- `BOM.md` — future cheap-arm research list (**do not buy** for v0.1.0).
- `SECURITY.md`, `COMPLIANCE_NOTES.md`, docs (`INSTALL`, `ARCHITECTURE`).
- Unit tests for geometry, detection, approach, and safety (no ROS/Gazebo required).
- CI reference workflows under `ci/` (merge to `.github/workflows/` needs `workflow` OAuth scope).

### Security

- `.gitignore` excludes `.env*` / keys; gitleaks config present.
- Lost-target software e-stop and velocity clamps in controller path.
- No secrets required for local unit tests.
