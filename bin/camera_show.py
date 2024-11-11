# import cv2
# import rospy
# import miro2 as miro
# import numpy as np
# class CameraDisplay:
#     def __init__(self):
#         # Initialize the robot interface
#         self.interface = miro.lib.RobotInterface() 

#         # Register camera callbacks
#         self.interface.register_callback("camera_left", self.display_left_camera)
#         self.interface.register_callback("camera_right", self.display_right_camera)


#     def display_left_camera(self, frame):
#         if isinstance(frame.data, np.ndarray):
#             cv2.imshow("Left Camera", frame.data)
#             cv2.waitKey(1)
#             cv2.destroyWindow("Left Camera")  # 尝试每帧关闭再打开窗口
#             cv2.imshow("Left Camera", frame.data)
#             cv2.waitKey(1)
#         else:
#             print("Left Camera data is not an ndarray.")

#     def display_right_camera(self, frame):
#         # Confirm data type and shape before displaying
#         if isinstance(frame.data, np.ndarray):
#             print("Right Camera Data Type:", frame.data.dtype)  # Check data type
#             print("Right Camera Data Shape:", frame.data.shape)  # Check data shape
#             cv2.imshow("Right Camera", frame.data)
#             cv2.waitKey(1)
#         else:
#             print("Right Camera data is not an ndarray.")

#     def loop(self):
#         # Keep the display running
#         rospy.spin()

# if __name__ == "__main__":

#     # Create display object and start loop
#     display = CameraDisplay()
#     display.loop()


# import rospy
# from sensor_msgs.msg import CompressedImage
# import cv2
# from cv_bridge import CvBridge
# import os

# class CameraTest:
#     def __init__(self):
#         # Initialize ROS node
#         rospy.init_node("camera_test", anonymous=True)

#         # Setup image converter and camera subscriber
#         self.image_converter = CvBridge()
#         topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")
#         self.sub_caml = rospy.Subscriber(topic_base_name + "/sensors/caml/compressed",
#                                          CompressedImage, self.callback_caml, queue_size=1, tcp_nodelay=True)

#     def callback_caml(self, ros_image):
#         # Convert ROS image to OpenCV format
#         image = self.image_converter.compressed_imgmsg_to_cv2(ros_image, "bgr8")
#         print(image)
#         # Show image
#         cv2.imshow("Left Camera", image)
#         cv2.waitKey(1)

#     def loop(self):
#         rospy.spin()

# if __name__ == "__main__":
#     cam_test = CameraTest()
#     cam_test.loop()


import cv2
import rospy
import miro2 as miro
import numpy as np
import time

class CameraDisplay:
    def __init__(self):
        # Initialize the robot interface
        self.interface = miro.lib.RobotInterface() 

    def loop(self):
        # Main loop to continuously fetch and display camera images
        while not rospy.core.is_shutdown():
            # 获取左右摄像头的图像数据
            left_image_frame = self.interface.get_cameras()[0]  # 左相机图像
            right_image_frame = self.interface.get_cameras()[1]  # 右相机图像

            # 显示左相机图像
            if left_image_frame is not None:
                left_image = left_image_frame.data  # 提取图像数据
                if isinstance(left_image, np.ndarray):
                    cv2.imshow("Left Camera", left_image)
                    cv2.waitKey(1)

            # 显示右相机图像
            if right_image_frame is not None:
                right_image = right_image_frame.data  # 提取图像数据
                if isinstance(right_image, np.ndarray):
                    cv2.imshow("Right Camera", right_image)
                    cv2.waitKey(1)

            # 控制帧率(别控制了，会卡的)
            # time.sleep(0.05)

if __name__ == "__main__":

    
    # Create display object and start loop
    display = CameraDisplay()
    display.loop()

