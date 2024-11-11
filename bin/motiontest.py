#!/usr/bin/env python3

import rospy
import time
from geometry_msgs.msg import TwistStamped
import miro2 as miro

class MovementTester:
    def __init__(self):
        # 初始化 ROS 节点
        # rospy.init_node("movement_tester", anonymous=True)
        
        # 机器人接口，用于控制运动
        self.interface = miro.lib.RobotInterface()  # 使用适当的接口初始化
        
        # 设置运动参数
        self.linear_speed = 0.2  # 线速度
        self.angular_speed = 0.5  # 角速度
        self.move_duration = 3    # 每次运动的持续时间

    def move_forward(self):
        """让机器人向前移动一段距离"""
        print("Moving forward with linear speed:", self.linear_speed)
        for _ in range(3):
            self.interface.set_vel(self.linear_speed, 0.1)
        time.sleep(self.move_duration)
        self.interface.set_vel(0.0, 0.0)  # 停止运动

    def turn_right(self):
        """让机器人向右旋转"""
        print("Turning right with angular speed:", -self.angular_speed)
        self.interface.set_vel(0.0, -self.angular_speed)
        time.sleep(self.move_duration)
        self.interface.set_vel(0.0, 0.0)  # 停止运动

    def turn_left(self):
        """让机器人向左旋转"""
        print("Turning left with angular speed:", self.angular_speed)
        self.interface.set_vel(0.0, self.angular_speed)
        time.sleep(self.move_duration)
        self.interface.set_vel(0.0, 0.0)  # 停止运动

    def loop(self):
        """测试循环"""
        while not rospy.is_shutdown():
            # 测试向前移动
            self.move_forward()
            time.sleep(1)  # 停止1秒

            # 测试右转
            self.turn_right()
            time.sleep(1)  # 停止1秒

            # 测试左转
            self.turn_left()
            time.sleep(1)  # 停止1秒

if __name__ == "__main__":
    try:
        tester = MovementTester()
        tester.loop()
    except rospy.ROSInterruptException:
        pass
