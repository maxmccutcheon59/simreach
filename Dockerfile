# SimReach — ROS 2 Humble + Gazebo Classic (sim-first). No hardware required.
# Build:  docker build -t simreach:v0.1.0 .
# Test:   docker run --rm simreach:v0.1.0 pytest -q
# Shell:  docker run --rm -it simreach:v0.1.0 bash
#
# GUI Gazebo needs display forwarding on the host (not available in all CI boxes).
# Unit-testable vision/control logic runs without Gazebo.

FROM ros:humble-ros-base-jammy

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1

# Gazebo Classic + camera / ros bridge packages (best-effort; image stays usable if some are missing)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-pytest \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-gazebo-ros \
    ros-humble-vision-msgs \
    ros-humble-cv-bridge \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ws/src/simreach
COPY . /ws/src/simreach

# Install pure-Python package for unit tests (no ROS needed for this layer's pytest)
RUN pip3 install --no-cache-dir -e ".[dev]"

# Optional: colcon build of ROS package when sourcing /opt/ros/humble
WORKDIR /ws
RUN bash -lc "source /opt/ros/humble/setup.bash && \
    rosdep update || true && \
    apt-get update && rosdep install --from-paths src --ignore-src -r -y || true && \
    colcon build --packages-select simreach_bringup --symlink-install || \
    echo 'colcon build skipped/failed — pure Python tests still work'" \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ws/src/simreach
# Non-root user for container runtime (least privilege)
RUN useradd -ms /bin/bash simreach && chown -R simreach:simreach /ws
USER simreach

CMD ["pytest", "-q"]
