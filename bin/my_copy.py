import numpy as np
import soundfile as sf

def copy_wav_file(input_path, output_path):
    # 读取 WAV 文件
    audio_array, sample_rate = sf.read(input_path)
    # 确保数组是可写的
    audio_array_copy = np.array(audio_array, copy=True)
    # 将复制后的音频数据写入新文件
    sf.write(output_path, audio_array_copy, sample_rate)

# 使用这个函数来复制文件
copy_wav_file("/home/yufeng/mdk/bin/output.wav", "output1.wav")
