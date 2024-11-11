#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError
import cv2

class MiroCameraViewer:
    def __init__(self):
        # 初始化ROS节点
        rospy.init_node('miro_camera_viewer', anonymous=True)

        # 创建图像转换器
        self.bridge = CvBridge()

        # 订阅左眼摄像头话题
        rospy.Subscriber("/miro/sensors/caml/compressed", CompressedImage, self.callback_caml)
        
        # 订阅右眼摄像头话题
        rospy.Subscriber("/miro/sensors/camr/compressed", CompressedImage, self.callback_camr)

    def callback_caml(self, msg):
        # 解压缩并显示左眼图像
        try:
            cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
            cv2.imshow("Left Camera", cv_image)
            cv2.waitKey(1)
        except CvBridgeError as e:
            rospy.logerr(f"CvBridge Error for caml: {e}")

    def callback_camr(self, msg):
        # 解压缩并显示右眼图像
        try:
            cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
            cv2.imshow("Right Camera", cv_image)
            cv2.waitKey(1)
        except CvBridgeError as e:
            rospy.logerr(f"CvBridge Error for camr: {e}")

    def start(self):
        # 开始循环
        rospy.spin()
        # 关闭窗口
        cv2.destroyAllWindows()

if __name__ == "__main__":
    viewer = MiroCameraViewer()
    viewer.start()
