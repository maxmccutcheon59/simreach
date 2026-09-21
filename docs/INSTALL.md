# Install — SimReach

## Paths

| Goal | Path | Needs Gazebo? | Needs Docker? |
|------|------|---------------|---------------|
| Unit-test vision / approach | `pip install -e ".[dev]" && pytest -q` | No | **No** |
| Recorded approach demo | `python scripts/recorded_run.py` | No | **No** |
| ROS 2 node + launch | Docker image or local ROS 2 Humble | Optional | Optional |
| Full Gazebo world | Docker + host display / GPU as available | Yes | Recommended |

## Host (logic only — recommended first)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
pytest -q
ruff check src tests
python scripts/recorded_run.py -o examples/last_run.jsonl
```

Requires Python ≥ 3.10. No ROS, Gazebo, camera, or Docker.

## Docker (ROS 2 Humble + Gazebo packages) — optional

```bash
docker build -t simreach:v0.2.0 .
docker run --rm simreach:v0.2.0 pytest -q
docker run --rm -it simreach:v0.2.0 bash
```

Inside the container (if `colcon build` succeeded during image build):

```bash
source /opt/ros/humble/setup.bash
source /ws/install/setup.bash
ros2 launch simreach_bringup sim_approach.launch.py
```

Gazebo GUI typically needs:

```bash
xhost +local:docker   # host — understand the security implication first
docker run --rm -it --env DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix simreach:v0.2.0 bash
```

If Gazebo cannot run in your environment, the package layout, optional Dockerfile, recorded-run script, and unit-tested `simreach_vision` core are the supported deliverable for v0.2.0.

## Controller docs

See [`CONTROLLER.md`](CONTROLLER.md) for IBVS-lite conventions and tuning.

## Hardware

**Do not buy hardware for v0.2.0 ($0).** See `BOM.md` for a future cheap-arm research list only.
