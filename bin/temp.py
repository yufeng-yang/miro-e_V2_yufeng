import numpy as np
# i = np.arange(0, 40, 2.5)
# print(i)
# x = np.interp(i, j, self.outbuf[:, c])
# '=================================================================='
# outbuf = np.array([
#     [0, 10, 20, 30],  # 样本 0: [LEFT, RIGHT, CENTRE, TAIL]
#     [1, 11, 21, 31],  # 样本 1: [LEFT, RIGHT, CENTRE, TAIL]
#     [2, 12, 22, 32],  # 样本 2: [LEFT, RIGHT, CENTRE, TAIL]
#     [3, 13, 23, 33],  # 样本 3: [LEFT, RIGHT, CENTRE, TAIL]
#     [4, 14, 24, 34],  # 样本 4: [LEFT, RIGHT, CENTRE, TAIL]
#     [5, 15, 25, 35],  # 样本 5: [LEFT, RIGHT, CENTRE, TAIL]
#     [6, 16, 26, 36],  # 样本 6: [LEFT, RIGHT, CENTRE, TAIL]
#     [7, 17, 27, 37],  # 样本 7: [LEFT, RIGHT, CENTRE, TAIL]
#     [8, 18, 28, 38],  # 样本 8: [LEFT, RIGHT, CENTRE, TAIL]
#     [9, 19, 29, 39],  # 样本 9: [LEFT, RIGHT, CENTRE, TAIL]
# ])

# playsamp = 3
# n_samp = 2
# spkrdata = outbuf[playsamp:(playsamp+n_samp),1]
# print(spkrdata)
# '=================================================================='
# import wave

# # 打开wav文件
# with wave.open('/home/yufeng/mdk/bin/client_audio.wav', 'rb') as wav_file:
#     # 获取通道数
#     n_channels = wav_file.getnchannels()
#     # 获取采样宽度（字节数）
#     sampwidth = wav_file.getsampwidth()
#     # 获取采样率
#     framerate = wav_file.getframerate()
#     # 获取帧数
#     n_frames = wav_file.getnframes()
#     # 计算音频时长
#     duration = n_frames / framerate

#     print(f"通道数: {n_channels}")
#     print(f"采样宽度（字节数）: {sampwidth}")
#     print(f"采样率: {framerate} Hz")
#     print(f"音频时长: {duration} 秒")

import wave
import numpy as np

# 打开 WAV 文件
with wave.open('/home/yufeng/mdk/bin/client_audio.wav', 'rb') as wav_file:
    # 读取所有帧数据
    audio_data = wav_file.readframes(wav_file.getnframes())
    
    # 将音频数据转换为 numpy 数组，格式为 16 位小端序
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    
    # 因为是双声道（2 channels），需要 reshape 成 (n_frames, 2)
    audio_array = audio_array.reshape(-1, 4)

    print('#########')
    print(audio_array)



