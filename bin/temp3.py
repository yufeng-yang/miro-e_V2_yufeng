from scipy.io import wavfile
import numpy as np

# 读取 WAV 文件
file_path = '/home/yufeng/mdk/bin/client_audio.wav'
samplerate, data = wavfile.read(file_path)

# 打印采样率和音频数据的信息
print(f"采样率: {samplerate} Hz")
print(f"音频数据形状: {data.shape}")

# 如果是多声道音频 (例如立体声)，每一列是一个声道的数据
if len(data.shape) > 1:
    num_channels = data.shape[1]
    print(f"通道数: {num_channels}")
else:
    num_channels = 1
    print(f"通道数: {num_channels}")

# 打印前 10 个采样点的数据
print("前10个采样点的数据:")
print(data[:10])
