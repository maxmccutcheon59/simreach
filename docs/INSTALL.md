# Install — SimReach

## Paths

| Goal | Path | Needs Gazebo? |
|------|------|---------------|
| Unit-test vision / approach logic | `pip install -e ".[dev]" && pytest -q` | No |
| ROS 2 node + launch | Docker image or local ROS 2 Humble | Optional |
| Full Gazebo world | Docker + host display / GPU as available | Yes |

## Host (logic only — recommended first)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
pytest -q
ruff check src tests
```

Requires Python ≥ 3.10. No ROS, Gazebo, or camera hardware.

## Docker (ROS 2 Humble + Gazebo packages)

```bash
docker build -t simreach:v0.1.0 .
docker run --rm simreach:v0.1.0 pytest -q
docker run --rm -it simreach:v0.1.0 bash
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
docker run --rm -it --env DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix simreach:v0.1.0 bash
```

If Gazebo cannot run in your environment, the package layout, Dockerfile, and unit-tested `simreach_vision` core are still the supported deliverable for v0.1.0.

## Lighter alternative (documented)

If Gazebo Classic is too heavy, keep using **`simreach_vision`** with synthetic frames (`make_blank_frame` / `paint_rect`) or swap the world for a lighter simulator later (e.g. Ignition/Harmonic, Webots) while reusing the same controller API. No code rewrite of the IBVS-lite core should be required.

## Hardware

**Do not buy hardware for v0.1.0.** See `BOM.md` for a future cheap-arm research list only.
