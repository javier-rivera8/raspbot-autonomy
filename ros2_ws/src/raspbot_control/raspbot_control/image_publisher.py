"""
Fake camera publisher for testing without a Raspberry Pi.

Usage (inside the ROS 2 container):
  # From a webcam (default, device 0):
  ros2 run raspbot_control image_publisher

  # From a video file:
  ros2 run raspbot_control image_publisher --ros-args -p source:=/path/to/video.mp4

  # From a static image:
  ros2 run raspbot_control image_publisher --ros-args -p source:=/path/to/image.jpg
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
import numpy as np


class ImagePublisher(Node):
    def __init__(self):
        super().__init__('image_publisher')

        self.declare_parameter('source', '0')   # '0' = webcam, or a file path
        self.declare_parameter('fps', 30.0)

        source_param = self.get_parameter('source').get_parameter_value().string_value
        fps = self.get_parameter('fps').get_parameter_value().double_value

        # source can be an int (camera index) or a file path
        try:
            source = int(source_param)
        except ValueError:
            source = source_param

        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            self.get_logger().error(f'Cannot open source: {source}')
            raise RuntimeError(f'Cannot open source: {source}')

        self.publisher_ = self.create_publisher(Image, '/image_raw', 10)
        self.timer = self.create_timer(1.0 / fps, self.timer_callback)
        self.get_logger().info(f'Publishing /image_raw from: {source} at {fps} fps')

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            # Loop video back to start
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
            if not ret:
                return

        msg = Image()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera'
        msg.height, msg.width = frame.shape[:2]
        msg.encoding = 'bgr8'
        msg.step = msg.width * 3
        msg.data = frame.tobytes()
        self.publisher_.publish(msg)

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ImagePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
