import rospy
import numpy as np
import wave
import struct
import miro2 as miro

# 设置常量
MIC_SAMPLE_RATE = 20000  # 录音采样率
RECORD_TIME = 5  # 录制时长
SAMPLE_COUNT = RECORD_TIME * MIC_SAMPLE_RATE  # 样本数量

class AudioRecorder:
    def __init__(self, interface):
        self.interface = interface
        self.micbuf = np.zeros((0, 4), 'uint16')  # 初始化4声道的缓存
        self.outbuf = None
        self.buffer_stuff = 0

        # 订阅麦克风数据
        self.interface.register_callback("microphones", self.callback_mics)
        print(f"录制从4个麦克风 {RECORD_TIME} 秒的音频...")

    def callback_mics(self, msg):
        if self.micbuf is not None:
            # 将接收到的麦克风数据追加到缓存区
            self.micbuf = np.concatenate((self.micbuf, msg.data))
            print(".", end="", flush=True)

            # 如果达到录制的样本数量，则停止录音
            if self.micbuf.shape[0] >= SAMPLE_COUNT:
                self.outbuf = self.micbuf
                self.micbuf = None  # 停止接收麦克风数据
                print("录音完成！")

    def record(self):
        # 等待录音完成
        while self.outbuf is None:
            rospy.sleep(0.1)
        print(f"录制数据的形状: {self.outbuf.shape}")

    def save_wav(self, filename):
        if self.outbuf is None:
            raise ValueError("没有录制的数据可以保存，请先录音。")

        print(f"保存音频文件到 {filename}")

        # 保存 WAV 文件
        with wave.open(filename, 'wb') as file:
            file.setsampwidth(2)
            file.setframerate(MIC_SAMPLE_RATE)
            file.setnchannels(4)  # 四声道
            x = np.reshape(self.outbuf, (-1))
            for s in x:
                file.writeframes(struct.pack('<h', s))

        print(f"音频文件保存成功：{filename}")
