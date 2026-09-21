from setuptools import setup

package_name = "simreach_bringup"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", ["launch/sim_approach.launch.py"]),
        ("share/" + package_name + "/config", ["config/approach_params.yaml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Max McCutcheon",
    maintainer_email="MaxMcCutcheon1@outlook.com",
    description="SimReach ROS 2 bringup for vision-guided approach (sim-first)",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "approach_node = simreach_bringup.approach_node:main",
        ],
    },
)
