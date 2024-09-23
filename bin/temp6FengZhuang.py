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



class speechtest:
    def __init__(self, topic_base_name):
        # 初始化机器人接口
        self.interface = miro.lib.RobotInterface()

        # 读取音频文件
        with wave.open('/home/yufeng/mdk/bin/client_audio.wav', 'rb') as wav_file:
            audio_data = wav_file.readframes(wav_file.getnframes())
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            audio_array = audio_array.reshape(-1, 4)

        self.outbuf = audio_array
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

        print(f"录制时长：{RECORD_TIME} 秒")

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
        # 降采样后的样本数量
        num_samples_downsampled = int(SAMPLE_COUNT / 2.5)

        # 初始化输出缓冲区
        outbuf = np.zeros((num_samples_downsampled, 0))

        for c in range(4):  # 处理4个通道的数据
            x = resample(self.outbuf[:, c], num_samples_downsampled)
            x = np.clip(x, -32768, 32767).astype(np.int16)  # 保证为 int16 类型
            outbuf = np.concatenate((outbuf, x[:, np.newaxis]), axis=1)

        # channel names
        chan = ["LEFT", "RIGHT", "CENTRE", "TAIL"]

        while not rospy.core.is_shutdown():
            if self.buffer_stuff < BUFFER_MIN:
                if self.playsamp == 0:
                    print(f"播放 {chan[self.playchan]} 声道的音频...")

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

                    # 如果4个通道都播放完毕，结束
                    if self.playchan == 4:
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
