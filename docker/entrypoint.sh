#!/bin/bash
# ──────────────────────────────────────────────
# Entrypoint: launches bringup + camera, then
# gives you a ready-to-go interactive shell.
# ──────────────────────────────────────────────
set -e

# Source ROS 2 underlay
source /opt/ros/humble/setup.bash

# Build & source your workspace (if needed)
if [ -d /root/ros2_ws/src ]; then
  cd /root/ros2_ws
  colcon build --packages-select raspbot_control --symlink-install 2>/dev/null || true
  source /root/ros2_ws/install/setup.bash
fi

# Make ROS available in every future `docker exec` shell
grep -qxF 'source /opt/ros/humble/setup.bash' /root/.bashrc || \
  echo 'source /opt/ros/humble/setup.bash' >> /root/.bashrc
grep -qxF 'source /root/ros2_ws/install/setup.bash' /root/.bashrc || \
  echo '[ -f /root/ros2_ws/install/setup.bash ] && source /root/ros2_ws/install/setup.bash' >> /root/.bashrc

echo "============================================"
echo "  Launching bringup + camera in background"
echo "============================================"

# ── 1. Bringup (adjust the package/launch file name if different) ──
# Common names: yahboomcar_bringup, raspbot_bringup
# If yours is a launch file:   ros2 launch <pkg> <file>.launch.py
# If yours is a node:          ros2 run <pkg> <node>
ros2 launch yahboomcar_bringup bringup.launch &
BRINGUP_PID=$!
echo "[entrypoint] Bringup started (PID $BRINGUP_PID)"

# ── 2. USB Camera ──
ros2 run usb_cam usb_cam_node_exe &
CAM_PID=$!
echo "[entrypoint] usb_cam started  (PID $CAM_PID)"

# Give nodes a moment to initialise
sleep 3

echo "============================================"
echo "  All background nodes running."
echo "  Run:  ros2 run raspbot_control bottle_follower"
echo "============================================"

# Drop into interactive bash (keeps container alive)
exec bash
