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

import rospy
from std_msgs.msg import Int16MultiArray
import numpy as np
import wave
from scipy.signal import resample

class AudioPlayback:
    def __init__(self, interface, topic_base_name, wav_file, target_sample_rate=8000):
        self.interface = interface
        self.target_sample_rate = target_sample_rate

        # 读取音频文件
        with wave.open(wav_file, 'rb') as wav_file:
            sample_rate = wav_file.getframerate()  # 获取采样率
            n_channels = wav_file.getnchannels()  # 获取声道数
            audio_data = wav_file.readframes(wav_file.getnframes())
            audio_array = np.frombuffer(audio_data, dtype=np.int16)

            # 根据声道数 reshape 音频数组
            audio_array = audio_array.reshape(-1, n_channels)
            print(f"原始采样率: {sample_rate} Hz, 声道数: {n_channels}")

        # 如果采样率不同于目标采样率，则进行降采样
        if sample_rate != target_sample_rate:
            print(f"采样率不同，开始将采样率 {sample_rate} Hz 降采样到 {target_sample_rate} Hz")
            num_samples_downsampled = int(audio_array.shape[0] * target_sample_rate / sample_rate)
            for c in range(n_channels):
                audio_array[:, c] = resample(audio_array[:, c], num_samples_downsampled)
            print(f"降采样完成")

        self.outbuf = audio_array
        self.n_channels = n_channels
        self.buffer_stuff = 0
        self.playchan = 0
        self.playsamp = 0
        self.buffer_space = None
        self.buffer_total = None
        self.finish_question = False

        # 设置 ROS 话题发布者
        self.pub_stream = rospy.Publisher(topic_base_name + "/control/stream", Int16MultiArray, queue_size=0)
        self.sub_stream = rospy.Subscriber(topic_base_name + "/sensors/stream", UInt16MultiArray, self.space_detecter, queue_size=1, tcp_nodelay=True)

        # 控制缓存大小的相关参数
        self.BUFFER_MAX = 4000 + 1000  # 最大缓存大小
        self.BUFFER_MIN = 4000 - 1000  # 最小缓存大小
        self.MAX_STREAM_MSG_SIZE = 4096 - 48  # 单次最大传输的数据量

    def space_detecter(self, msg):
        self.buffer_space = msg.data[0]
        self.buffer_total = msg.data[1]
        self.buffer_stuff = self.buffer_total - self.buffer_space
        # print(msg)

    def wait_for_buffer(self):
        while self.buffer_space is None or self.buffer_total is None:
            rospy.sleep(0.02)
            # print("waiting for buffer space")

    def play(self):
        self.wait_for_buffer()
        num_samples = int(self.outbuf.shape[0])
        outbuf = np.zeros((num_samples, 0))

        # 计算播放时长
        duration = num_samples / self.target_sample_rate
        print(f"音频播放时长: {duration:.2f} 秒")
        print('################')
        print(self.finish_question)
        # 准备音频数据
        for c in range(self.n_channels):
            x = self.outbuf[:, c]
            x = np.clip(x, -32768, 32767).astype(np.int16)
            outbuf = np.concatenate((outbuf, x[:, np.newaxis]), axis=1)

        # 动态处理声道名称
        chan = ["LEFT", "RIGHT", "CENTRE", "TAIL"]

        while not rospy.core.is_shutdown():

            # 严格控制缓存空间，只有当 `buffer_stuff` 小于 BUFFER_MIN 时才发送数据
            if self.buffer_stuff < self.BUFFER_MIN:
                
                # 如果是第一次发送，输出声道的名字
                if self.playsamp == 0 and self.playchan < len(chan):
                    print(f"播放 {chan[self.playchan]} 声道的音频...")

                # 计算一次传输的数据量，确保不超过接收端的可用空间和消息大小限制
                n_samp = min(self.BUFFER_MAX - self.buffer_stuff, self.buffer_space, outbuf.shape[0] - self.playsamp, self.MAX_STREAM_MSG_SIZE)

                # 提取当前要发送的数据
                spkrdata = outbuf[self.playsamp:self.playsamp + n_samp, self.playchan]
                self.playsamp += n_samp

                # 创建消息并发布
                msg = Int16MultiArray()
                msg.data = [int(i) for i in spkrdata]
                self.pub_stream.publish(msg)

                # 更新 `buffer_stuff`，确保在下次检查缓存时不会立即发送
                self.buffer_stuff = self.BUFFER_MIN

                # 如果当前声道播放完毕，切换到下一个声道
                if self.playsamp == outbuf.shape[0]:
                    self.playsamp = 0
                    self.playchan += 1
                    rospy.sleep(0.7)

                    # 如果所有声道播放完毕，结束播放
                    if self.playchan == self.n_channels:
                        print("(播放完成)")
                        self.finish_question = True
                        print(self.finish_question)
                        break

            # 稍作延迟，防止过快地重新检查缓存空间
            rospy.sleep(0.02)
