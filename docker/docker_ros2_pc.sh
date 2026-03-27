#!/bin/bash
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
WORKSPACE_DIR="$SCRIPT_DIR/../ros2_ws"
IMAGE_NAME="raspbot-ros2-pc"

# Build the image once (skipped automatically if already up to date)
docker build -t "$IMAGE_NAME" -f "$SCRIPT_DIR/Dockerfile.pc" "$SCRIPT_DIR"

xhost +
docker run -it \
  --net=host \
  --env="DISPLAY" \
  --env="QT_X11_NO_MITSHM=1" \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v "$WORKSPACE_DIR":/root/ros2_ws \
  -v "$HOME/Downloads":/root/Downloads \
  -v "$SCRIPT_DIR/entrypoint.sh":/root/entrypoint.sh \
  "$IMAGE_NAME"