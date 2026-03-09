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
  osrf/ros:humble-desktop /bin/bash