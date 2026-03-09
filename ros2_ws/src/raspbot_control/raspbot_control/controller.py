import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


FORWARD_SPEED = 0.3   # m/s
DURATION_SECS = 2.0   # seconds moving in each direction
TIMER_PERIOD  = 0.1   # seconds between publishes


class RaspbotController(Node):
    """Moves the robot forward and backward alternately to test cmd_vel."""

    def __init__(self):
        super().__init__('raspbot_controller')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(TIMER_PERIOD, self.timer_callback)

        self.elapsed = 0.0
        self.going_forward = True
        self.get_logger().info('Raspbot controller started — forward/backward test')

    def timer_callback(self):
        self.elapsed += TIMER_PERIOD

        msg = Twist()

        if self.going_forward:
            msg.linear.x = FORWARD_SPEED
            self.get_logger().info('Moving FORWARD', throttle_duration_sec=1.0)
        else:
            msg.linear.x = -FORWARD_SPEED
            self.get_logger().info('Moving BACKWARD', throttle_duration_sec=1.0)

        self.publisher_.publish(msg)

        if self.elapsed >= DURATION_SECS:
            self.elapsed = 0.0
            self.going_forward = not self.going_forward

    def stop(self):
        msg = Twist()
        msg.linear.x = 0.0
        self.publisher_.publish(msg)
        self.get_logger().info('Stopped')


def main(args=None):
    rclpy.init(args=args)
    node = RaspbotController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.stop()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
