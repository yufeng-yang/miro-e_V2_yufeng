import rospy
from std_msgs.msg import Int16MultiArray
import numpy as np
import wave
from scipy.signal import resample
import os
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
MAX_STREAM_MSG_SIZE = (4096 - 48)
BUFFER_MARGIN = 1000
BUFFER_MAX = BUFFER_STUFF_SAMPLES + BUFFER_MARGIN
BUFFER_MIN = BUFFER_STUFF_SAMPLES - BUFFER_MARGIN
TARGET_SAMPLE_RATE = 8000  # 目标采样率

class speechtest:
    def __init__(self, topic_base_name):
        # 初始化机器人接口
        self.interface = miro.lib.RobotInterface()

        # 读取音频文件
        with wave.open('/home/yufeng/mdk/bin/Question1.wav', 'rb') as wav_file:
            sample_rate = wav_file.getframerate()  # 获取采样率
            n_channels = wav_file.getnchannels()  # 获取声道数
            audio_data = wav_file.readframes(wav_file.getnframes())
            audio_array = np.frombuffer(audio_data, dtype=np.int16)

            # 根据声道数 reshape 音频数组
            audio_array = audio_array.reshape(-1, n_channels)  # 自动根据声道数设置
            print(f"原始采样率: {sample_rate} Hz, 声道数: {n_channels}")

        # 如果采样率不是8000 Hz，则降采样
        if sample_rate != TARGET_SAMPLE_RATE:
            print(f"采样率不同，开始将采样率 {sample_rate} Hz 降采样到 {TARGET_SAMPLE_RATE} Hz")
            num_samples_downsampled = int(audio_array.shape[0] * TARGET_SAMPLE_RATE / sample_rate)
            for c in range(n_channels):  # 对每个通道进行降采样
                audio_array[:, c] = resample(audio_array[:, c], num_samples_downsampled)
            print(f"降采样完成")

        self.outbuf = audio_array
        self.n_channels = n_channels  # 保存声道数
        self.buffer_stuff = 0
        self.playchan = 0
        self.playsamp = 0
        self.buffer_space = None
        self.buffer_total = None

        # 设置话题名称和发布者
        self.topic_base_name = topic_base_name
        self.pub_stream = rospy.Publisher(self.topic_base_name + "/control/stream", Int16MultiArray, queue_size=0)

        # 订阅传感器数据
        self.sub_stream = rospy.Subscriber(self.topic_base_name + "/sensors/stream", UInt16MultiArray, self.space_detecter, queue_size=1, tcp_nodelay=True)

        print(f"录制时长：{audio_array.shape[0] / TARGET_SAMPLE_RATE} 秒")

    def space_detecter(self, msg):
        # 根据总空间和剩余空间，计算缓冲区使用的容量
        self.buffer_space = msg.data[0]
        self.buffer_total = msg.data[1]
        self.buffer_stuff = self.buffer_total - self.buffer_space

    def wait(self):
        # 等待接收到 buffer_space 和 buffer_total 数据
        while self.buffer_space is None or self.buffer_total is None:
            print("等待接收到 buffer_space 和 buffer_total 数据...")
            rospy.sleep(0.02)

    def loop(self):
        num_samples_downsampled = int(self.outbuf.shape[0])

        # 初始化输出缓冲区
        outbuf = np.zeros((num_samples_downsampled, 0))

        for c in range(self.n_channels):  # 根据声道数处理数据
            x = self.outbuf[:, c]  # 使用现有的采样数据
            x = np.clip(x, -32768, 32767).astype(np.int16)  # 保证为 int16 类型
            outbuf = np.concatenate((outbuf, x[:, np.newaxis]), axis=1)

        # channel names
        chan = ["LEFT", "RIGHT", "CENTRE", "TAIL"]

        while not rospy.core.is_shutdown():
            if self.buffer_stuff < BUFFER_MIN:
                if self.playsamp == 0:
                    # 动态选择声道名称
                    if self.playchan < len(chan):
                        print(f"播放 {chan[self.playchan]} 声道的音频...")
                    else:
                        print(f"播放通道 {self.playchan} 的音频...")

                # 计算要发送的样本数量
                n_samp = min(BUFFER_MAX - self.buffer_stuff, self.buffer_space, outbuf.shape[0] - self.playsamp, MAX_STREAM_MSG_SIZE)

                # 提取要发送的数据
                spkrdata = outbuf[self.playsamp:self.playsamp+n_samp, self.playchan]
                self.playsamp += n_samp

                # 发布音频数据
                msg = Int16MultiArray()
                msg.data = [int(i) for i in spkrdata]
                self.pub_stream.publish(msg)

                # 更新缓冲区使用量
                self.buffer_stuff = BUFFER_MIN

                # 如果已完成当前通道的播放，切换到下一个通道
                if self.playsamp == outbuf.shape[0]:
                    self.playsamp = 0
                    self.playchan += 1

                    # 如果所有声道都播放完毕，结束
                    if self.playchan == self.n_channels:
                        print("(播放完成)")
                        break

            rospy.sleep(0.02)

# 问答游戏的类
class QuestionAnswerGame:
    def __init__(self):
        self.topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")
        self.audio_publisher = speechtest(self.topic_base_name)

    def play_question_audio(self, question):
        # 假设已经有问题对应的音频文件，您可以调用 speechtest 中的逻辑来播放音频
        self.audio_publisher.wait()
        self.audio_publisher.loop()

# 创建问答游戏界面
def create_gui(game):
    import tkinter as tk
    root = tk.Tk()
    root.title("MIROE 问答游戏")

    tk.Label(root, text="请选择一个问题:").pack(pady=10)

    # 创建问题选择按钮（假设问题和音频已经有对应关系）
    tk.Button(root, text="问题1", command=lambda: game.play_question_audio("问题1")).pack(pady=5)
    tk.Button(root, text="问题2", command=lambda: game.play_question_audio("问题2")).pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    # rospy.init_node('qa_game_node', anonymous=True)

    game = QuestionAnswerGame()
    create_gui(game)
