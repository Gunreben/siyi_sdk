# GimbalControlROS2Node.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, String, Bool
from GimbalCoreController import GimbalController

class GimbalControllerNode(Node):
    def __init__(self):
        super().__init__('gimbal_controller_node')
        self.controller = GimbalController()

        # Subscribers
        self.create_subscription(Float64, 'gimbal/yaw', self.set_yaw_callback, 10)
        self.create_subscription(Float64, 'gimbal/pitch', self.set_pitch_callback, 10)
        self.create_subscription(Bool, 'gimbal/connect', self.connect_callback, 10)
        self.create_subscription(Bool, 'gimbal/disconnect', self.disconnect_callback, 10)

        # Publisher
        self.attitude_publisher = self.create_publisher(String, 'gimbal/attitude', 10)
        self.get_logger().info('Gimbal Controller Node has been started.')

        # Timer to publish attitude
        #self.attitude_timer = self.create_timer(1.0, self.publish_attitude)

    def connect_callback(self, msg):
        if msg.data:
            success = self.controller.connect()
            if success:
                self.get_logger().info('Successfully connected to gimbal.')
            else:
                self.get_logger().error('Failed to connect to gimbal.')

    def disconnect_callback(self, msg):
        if msg.data:
            self.controller.disconnect()
            self.get_logger().info('Disconnected from gimbal.')

    def set_yaw_callback(self, msg):
        if self.controller.connected:
            yaw_deg = msg.data
            attitude = self.controller.get_attitude()
            if attitude:
                current_pitch = attitude[1]
            else:
                current_pitch = 0.0
            success = self.controller.set_angles(yaw_deg, current_pitch)
            if success:
                self.get_logger().info(f'Set yaw to {yaw_deg} degrees.')
            else:
                self.get_logger().error('Failed to set yaw angle.')
        else:
            self.get_logger().warn('Gimbal is not connected. Cannot set yaw.')

    def set_pitch_callback(self, msg):
        if self.controller.connected:
            pitch_deg = msg.data
            attitude = self.controller.get_attitude()
            if attitude:
                current_yaw = attitude[0]
            else:
                current_yaw = 0.0
            success = self.controller.set_angles(current_yaw, pitch_deg)
            if success:
                self.get_logger().info(f'Set pitch to {pitch_deg} degrees.')
            else:
                self.get_logger().error('Failed to set pitch angle.')
        else:
            self.get_logger().warn('Gimbal is not connected. Cannot set pitch.')

    def publish_attitude(self):
        if self.controller.connected:
            attitude = self.controller.get_attitude()
            if attitude:
                yaw, pitch, roll = attitude
                attitude_str = f'yaw={yaw:.2f}°, pitch={pitch:.2f}°, roll={roll:.2f}°'
                msg = String()
                msg.data = attitude_str
                self.attitude_publisher.publish(msg)
                self.get_logger().info(f'Published attitude: {attitude_str}')


def main(args=None):
    rclpy.init(args=args)
    node = GimbalControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down Gimbal Controller Node...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
