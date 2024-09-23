import tkinter as tk
import rospy
from std_msgs.msg import UInt16MultiArray, Int16MultiArray

import time
import sys
import os
import numpy as np
import wave, struct

import miro2 as miro
from scipy.io import wavfile
from scipy.signal import resample


BUFFER_STUFF_SAMPLES = 4000

# messages larger than this will be dropped by the receiver,
# however, so - whilst we can stuff the buffer more than this -
# we can only send this many samples in any single message.

# 这个用于限制传输时，每次传输的包的大小，48是预留给头文件的
# 具体在哪定义的目前没有找到
# 但是一旦超出这个数字，就会导致接受方丢弃多余的部分
MAX_STREAM_MSG_SIZE = (4096 - 48)

# using a margin avoids sending many small messages - instead
# we will send a smaller number of larger messages, at the cost
# of being less precise in respecting our buffer stuffing target.
BUFFER_MARGIN = 1000
BUFFER_MAX = BUFFER_STUFF_SAMPLES + BUFFER_MARGIN
BUFFER_MIN = BUFFER_STUFF_SAMPLES - BUFFER_MARGIN



# microphone sample rate
MIC_SAMPLE_RATE = 20000

# sample count
SAMPLE_COUNT = 171897

# RECORE Time
RECORD_TIME = SAMPLE_COUNT/MIC_SAMPLE_RATE

# 假设您已经有一个 MIRO 机器人名称和音频发布类
from temp4 import speechtest

# 定义音频文件和问题的对应关系
question_audio_files = {
    "问题1": "/home/yufeng/mdk/bin/client_audio.wav",
    "问题2": "/home/yufeng/mdk/bin/question2.wav",
    "问题3": "/home/yufeng/mdk/bin/question3.wav",
}

class QuestionAnswerGame:
    def __init__(self):
        self.topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")
        self.audio_publisher = speechtest(self.topic_base_name)

    def play_question_audio(self, question):
        audio_file = question_audio_files.get(question)
        if audio_file:
            self.audio_publisher.wait_for_buffer()
            self.audio_publisher.send_audio(audio_file)
        else:
            print(f"无法找到问题 {question} 的音频文件")

# 创建问答游戏界面
def create_gui(game):
    root = tk.Tk()
    root.title("MIROE 问答游戏")

    tk.Label(root, text="请选择一个问题:").pack(pady=10)

    # 创建问题选择按钮
    for question, audio_file in question_audio_files.items():
        tk.Button(root, text=question, command=lambda q=question: game.play_question_audio(q)).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    rospy.init_node('qa_game_node', anonymous=True)

    game = QuestionAnswerGame()
    create_gui(game)
