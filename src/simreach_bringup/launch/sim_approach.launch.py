"""Launch stub for SimReach vision-guided approach (Gazebo + node).

Full Gazebo bringup requires the Docker image (see Dockerfile / docs/INSTALL.md).
This launch file starts the approach node with default params; world spawn is
documented separately because Gazebo Classic vs Harmonic differs by distro.
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    pkg = get_package_share_directory("simreach_bringup")
    params = os.path.join(pkg, "config", "approach_params.yaml")
    return LaunchDescription(
        [
            Node(
                package="simreach_bringup",
                executable="approach_node",
                name="simreach_approach",
                output="screen",
                parameters=[params],
            ),
        ]
    )
