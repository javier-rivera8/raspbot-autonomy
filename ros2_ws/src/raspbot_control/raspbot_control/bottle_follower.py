import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
import numpy as np
import cv2
from ultralytics import YOLO

# COCO class index for "bottle" (includes water bottles)
BOTTLE_CLASS_ID = 39

FORWARD_SPEED = 0.3          # m/s linear.x when bottle detected
CONFIDENCE_THRESHOLD = 0.5   # minimum YOLO confidence to act on


class BottleFollower(Node):
    """Move the robot forward while a water bottle is visible in /image_raw."""

    def __init__(self):
        super().__init__('bottle_follower')

        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(
            Image,
            '/image_raw',
            self.image_callback,
            10,
        )

        self.model = YOLO('yolov8n.pt')   # downloads automatically on first run

        self._bottle_detected = False
        self.get_logger().info('BottleFollower started — waiting for /image_raw ')

    def image_callback(self, msg: Image):
        # Convert ROS Image to OpenCV BGR (without cv_bridge to avoid NumPy ABI issues)
        try:
            frame = np.frombuffer(msg.data, dtype=np.uint8).reshape(
                msg.height, msg.width, -1
            )
            # If encoding is RGB, convert to BGR for OpenCV
            if 'rgb' in msg.encoding.lower():
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        except Exception as e:
            self.get_logger().error(f'Image conversion failed: {e}')
            return

        results = self.model(frame, verbose=False)

        bottle_found = False
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                if cls_id == BOTTLE_CLASS_ID and conf >= CONFIDENCE_THRESHOLD:
                    bottle_found = True
                    # Draw bounding box for debug (optional — comment out to save CPU)
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(
                        frame,
                        f'bottle {conf:.2f}',
                        (x1, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2,
                    )
                    break  # one detection is enough to trigger movement
            if bottle_found:
                break

        # Publish velocity command
        cmd = Twist()
        if bottle_found:
            cmd.linear.x = FORWARD_SPEED
            if not self._bottle_detected:
                self.get_logger().info('Bottle detected — moving forward')
        else:
            cmd.linear.x = 0.0
            if self._bottle_detected:
                self.get_logger().info('No bottle — stopping')

        self._bottle_detected = bottle_found
        self.publisher_.publish(cmd)

        # Show debug window (comment out if running headless)
        cv2.imshow('BottleFollower', frame)
        cv2.waitKey(1)

    def stop(self):
        cmd = Twist()
        cmd.linear.x = 0.0
        self.publisher_.publish(cmd)
        self.get_logger().info('Stopped')


def main(args=None):
    rclpy.init(args=args)
    node = BottleFollower()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.stop()
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
