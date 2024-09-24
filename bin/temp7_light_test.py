import rospy
from std_msgs.msg import UInt16MultiArray, Int16MultiArray

import time
import sys
import os
import numpy as np
import wave, struct

import miro2 as miro

interface = miro.lib.RobotInterface()
# interface.post_tone(freq=1000, dur=500, vol=128)  # 播放 1000Hz 的音调，持续 0.5 秒
# 定义红色到黄色之间的渐变颜色
colors = [
    (255, 0, 0),   # 红色
    (255, 64, 0),  # 橙红色
    (255, 128, 0), # 橙色
    (255, 192, 0), # 橙黄色
    (255, 255, 0)  # 黄色
]

# 让灯光以前中后组交替闪烁 5 秒钟
for i in range(25):
    color_index = i % len(colors)
    current_color = colors[color_index]

    # 每次逐渐减少亮度
    for brightness in range(200, 0, -40):  # 从 200 逐渐减到 0，步长为 40
        if i % 3 == 0:
            # 前部 LED 闪烁
            interface.set_illum(miro.constants.ILLUM_FRONT, current_color, brightness)
        elif i % 3 == 1:
            # 中部 LED 闪烁
            interface.set_illum(miro.constants.ILLUM_MID, current_color, brightness)
        else:
            # 后部 LED 闪烁
            interface.set_illum(miro.constants.ILLUM_REAR, current_color, brightness)

        # 每 0.05 秒逐渐降低亮度
        time.sleep(0.05)

    # 每 0.2 秒切换一次 LED 组
    time.sleep(0.15)

# 最后将所有灯光设置为稳定的黄色，亮度恢复到100
interface.set_illum(miro.constants.ILLUM_ALL, (255, 255, 0), 100)


