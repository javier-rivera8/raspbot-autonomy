ls#!/bin/bash
xhost +
docker run -it \
--privileged=true \
--net=host \
--env="DISPLAY" \
--env="QT_X11_NO_MITSHM=1" \
-v /tmp/.X11-unix:/tmp/.X11-unix \
--security-opt apparmor:unconfined \
-v /home/pi/temp:/root/temp \
-v /home/pi/raspbot-autonomy/ros2_ws:/root/ros2_ws \
-v /dev/i2c-1:/dev/i2c-1 \
-v /dev/i2c-0:/dev/i2c-0 \
--device=/dev/video0 \
--device=/dev/video1 \
--device=/dev/gpiomem \
-v /home/pi/raspbot-autonomy/docker/entrypoint.sh:/root/entrypoint.sh 
yahboomtechnology/ros-humble:0.1.0 /bin/bash -c "
    apt-get update -qq &&
    apt-get install -y python3-pip &&
    python3 -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu &&
    python3 -m pip install ultralytics opencv-python-headless &&
    chmod +x /root/entrypoint.sh &&
    exec /root/entrypoint.sh
  "
