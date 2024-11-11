# import rospy
# from sensor_msgs.msg import CompressedImage
# import cv2
# from cv_bridge import CvBridge, CvBridgeError
# import numpy as np
# from ultralytics import YOLO
# import os

# class ObjectDetectionClient:
#     def __init__(self, target_label="bottle"):
#         # 初始化 YOLO 模型
#         self.model = YOLO("yolo11n.pt")  # 请确保模型权重路径正确
#         self.target_label = target_label  # 目标物体标签

#         # ROS -> OpenCV 图像转换器
#         self.bridge = CvBridge()

#         # 初始化相机数据存储
#         self.left_camera_image = None

#         # 订阅左眼摄像头的压缩图像
#         topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")
#         self.sub_caml = rospy.Subscriber(topic_base_name + "/sensors/caml/compressed",
#                                          CompressedImage, self.callback_caml, queue_size=1, tcp_nodelay=True)

#     def callback_caml(self, ros_image):
#         # 获取左眼图像并进行目标检测
#         try:
#             # 转换为 OpenCV 格式的图像
#             image = self.bridge.compressed_imgmsg_to_cv2(ros_image, "bgr8")
#             self.left_camera_image = image

#             # 使用 YOLO 模型检测目标物体
#             # results = self.model(image, device="cpu")  # 使用 CPU 进行推理
#             results = self.model(image)

#             # 在图像中标记检测到的目标
#             for result in results:
#                 boxes = result.boxes.data
#                 for box in boxes:
#                     label = result.names[int(box[-1].item())]
#                     confidence = box[4].item()

#                     # 检测到的物体是目标标签时，进行标记
#                     if label == self.target_label and confidence > 0.5:
#                         x1, y1, x2, y2 = map(int, box[:4])
#                         cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                         cv2.putText(image, f"{label} {confidence:.2f}", (x1, y1 - 10),
#                                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#             # 显示检测结果
#             cv2.imshow("Left Camera - Object Detection", image)
#             cv2.waitKey(1)

#         except CvBridgeError as e:
#             print(f"CvBridge Error: {e}")

#     def loop(self):
#         # 保持 ROS 节点运行
#         rospy.spin()


# if __name__ == "__main__":
#     # 初始化 ROS 节点
#     rospy.init_node("object_detection_client", anonymous=True)

#     # 创建检测对象，并启动循环
#     client = ObjectDetectionClient(target_label="bottle")
#     client.loop()

# ===============================
# import rospy
# from sensor_msgs.msg import CompressedImage
# import cv2
# from cv_bridge import CvBridge, CvBridgeError
# import numpy as np
# from ultralytics import YOLO
# import os

# class ObjectDetectionClient:
#     def __init__(self, target_label="bottle", confidence_threshold=0.5, detection_interval=10):
#         # 初始化 YOLO 模型
#         self.model = YOLO("yolo11n.pt")  # 请确保模型权重路径正确
#         self.target_label = target_label  # 目标物体标签
#         self.confidence_threshold = confidence_threshold  # 置信度阈值
#         self.detection_interval = detection_interval  # 检测间隔
#         self.frame_count = 0  # 帧计数器

#         # ROS -> OpenCV 图像转换器
#         self.bridge = CvBridge()

#         # 初始化相机数据存储
#         self.left_camera_image = None

#         # 订阅左眼摄像头的压缩图像
#         topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")
#         self.sub_caml = rospy.Subscriber(topic_base_name + "/sensors/caml/compressed",
#                                          CompressedImage, self.callback_caml, queue_size=1, tcp_nodelay=True)

#     def callback_caml(self, ros_image):
#         # 获取左眼图像并进行目标检测
#         try:
#             # 转换为 OpenCV 格式的图像
#             image = self.bridge.compressed_imgmsg_to_cv2(ros_image, "bgr8")
#             self.left_camera_image = image

#             # 每隔 detection_interval 帧检测一次
#             if self.frame_count % self.detection_interval == 0:
#                 results = self.model(image)

#                 # 在图像中标记检测到的目标
#                 for result in results:
#                     boxes = result.boxes.data
#                     for box in boxes:
#                         label = result.names[int(box[-1].item())]
#                         confidence = box[4].item()

#                         # 检测到的物体是目标标签或是"person"
#                         if confidence > self.confidence_threshold:
#                             x1, y1, x2, y2 = map(int, box[:4])
#                             if label == self.target_label:
#                                 # 用绿色框标记目标标签物体
#                                 cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                                 cv2.putText(image, f"{label} {confidence:.2f}", (x1, y1 - 10),
#                                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#                             elif label == "person":
#                                 # 用红色框标记“person”
#                                 cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
#                                 cv2.putText(image, f"{label} {confidence:.2f}", (x1, y1 - 10),
#                                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

#             # 显示检测结果
#             cv2.imshow("Left Camera - Object Detection", image)
#             cv2.waitKey(1)

#             # 增加帧计数器
#             self.frame_count += 1

#         except CvBridgeError as e:
#             print(f"CvBridge Error: {e}")

#     def loop(self):
#         # 保持 ROS 节点运行
#         rospy.spin()


# if __name__ == "__main__":
#     # 初始化 ROS 节点
#     rospy.init_node("object_detection_client", anonymous=True)

#     # 创建检测对象，并设置目标标签、置信度阈值和检测间隔
#     client = ObjectDetectionClient(target_label="bottle", confidence_threshold=0.5, detection_interval=1)
#     client.loop()
# # ==================

import rospy
from sensor_msgs.msg import CompressedImage
import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from ultralytics import YOLO
import os
import time
import miro2 as miro

class ObjectDetectionClient:
    def __init__(self, target_label="bottle", confidence_threshold=0.3, detection_interval=1):
        # 初始化 YOLO 模型
        self.model = YOLO("yolo11s.pt")
        self.target_label = target_label
        self.confidence_threshold = confidence_threshold
        self.detection_interval = detection_interval
        self.frame_count = 0
        
        # ROS -> OpenCV 图像转换器
        self.bridge = CvBridge()

        # 初始化相机数据存储
        self.left_camera_image = None

        # 机器人接口，用于控制运动
        self.interface = miro.lib.RobotInterface()   # 使用适当的接口初始化

        # 订阅左眼摄像头的压缩图像
        topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")
        self.sub_caml = rospy.Subscriber(topic_base_name + "/sensors/caml/compressed",
                                         CompressedImage, self.callback_caml, queue_size=1, tcp_nodelay=True)

    def callback_caml(self, ros_image):
        try:
            # 转换为 OpenCV 格式的图像
            image = self.bridge.compressed_imgmsg_to_cv2(ros_image, "bgr8")
            self.left_camera_image = image

            # 每隔 detection_interval 帧检测一次
            if self.frame_count % self.detection_interval == 0:
                results = self.model(image)
                bottle_found = False

                for result in results:
                    boxes = result.boxes.data
                    for box in boxes:
                        label = result.names[int(box[-1].item())]
                        confidence = box[4].item()

                        # 如果检测到的物体是瓶子
                        if label == self.target_label and confidence > self.confidence_threshold:
                            x1, y1, x2, y2 = map(int, box[:4])
                            bottle_center_x = (x1 + x2) // 2
                            bottle_found = True

                            # 标记检测到的瓶子
                            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.putText(image, f"{label} {confidence:.2f}", (x1, y1 - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                            # 移动机器人朝向瓶子
                            self.move_towards_bottle(bottle_center_x, image.shape[1])

                if not bottle_found:
                    # 没找到瓶子时，可以让机器人执行搜索动作，比如缓慢旋转
                    print("Bottle not found, rotating to search.")
                    self.interface.set_vel(0.0, -0.1)  # 旋转以寻找目标

            # 增加帧计数器
            self.frame_count += 1

            # 显示图像窗口
            cv2.imshow("Left Camera - Object Detection", image)
            cv2.waitKey(1)

        except CvBridgeError as e:
            print(f"CvBridge Error: {e}")

    def move_towards_bottle(self, bottle_center_x, image_width):
        # 根据瓶子位置调整机器人运动方向
        center_threshold = 20  # 中心区域阈值
        lin_vel = 0.1  # 线速度
        ang_vel = 0.0  # 角速度

        # 计算瓶子相对于图像中心的偏移
        image_center_x = image_width // 2
        offset_x = bottle_center_x - image_center_x

        if abs(offset_x) < center_threshold:
            # 瓶子在中心区域，向前移动
            print("Bottle centered, moving forward.")
            self.interface.set_vel(lin_vel, 0.0)
        elif offset_x > 0:
            # 瓶子在右侧，向右转动
            ang_vel = 0.0
            print("Bottle on the right, turning right.")
            # self.interface.set_vel(0.0, ang_vel)
            # print("Bottle centered, moving forward.")
            self.interface.set_vel(0.1, -0.1)
        else:
            # 瓶子在左侧，向左转动
            ang_vel = 0.0
            print("Bottle on the left, turning left.")
            # self.interface.set_vel(0.0, ang_vel)
            self.interface.set_vel(0.1, 0.1)

    def loop(self):
        # 保持 ROS 节点运行
        rospy.spin()


if __name__ == "__main__":

    # 创建检测对象，并启动循环
    client = ObjectDetectionClient(target_label="bottle", confidence_threshold=0.3, detection_interval=1)
    client.loop()
