cd ~/Documents/raspbot-autonomy/ros2_ws
colcon build
source install/setup.bash

ros2 run raspbot_control bottle_follower

ros2 run raspbot_control image_publisher --ros-args -p source:=/root/ros2_ws/bottle.mp4