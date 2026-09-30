import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PublisherNode(Node):

    def __init__(self):
        super().__init__('publisher_node')

        self.publisher = self.create_publisher(
            String,
            'my_topic',
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_message
        )

    def publish_message(self):
        msg = String()
        msg.data = 'Hello ROS 2!'

        self.publisher.publish(msg)

        self.get_logger().info(
            f'Публікація: {msg.data}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = PublisherNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
