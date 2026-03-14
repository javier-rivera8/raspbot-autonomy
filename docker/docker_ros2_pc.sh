#!/bin/bash
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
WORKSPACE_DIR="$SCRIPT_DIR/../ros2_ws"

xhost +
docker run -it \
  --net=host \
  --env="DISPLAY" \
  --env="QT_X11_NO_MITSHM=1" \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v "$WORKSPACE_DIR":/root/ros2_ws \
  -v "$SCRIPT_DIR/entrypoint.sh":/root/entrypoint.sh \
  osrf/ros:humble-desktop /bin/bash -c "
    apt-get update -qq &&
    apt-get install -y python3-pip &&
    python3 -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu &&
    python3 -m pip install ultralytics opencv-python-headless &&
    chmod +x /root/entrypoint.sh &&
    exec /root/entrypoint.sh
  "