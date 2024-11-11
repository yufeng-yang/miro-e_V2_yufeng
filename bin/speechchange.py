import numpy as np
from scipy.io import wavfile
from scipy.signal import resample

def display_wav_features(file_path):
    # 读取 WAV 文件
    sample_rate, audio_array = wavfile.read(file_path)
    
    # 显示音频文件的特征
    print(f"Sample Rate: {sample_rate} Hz")
    print(f"Number of Channels: {audio_array.shape[1] if audio_array.ndim > 1 else 1}")
    print(f"Number of Samples: {audio_array.shape[0]}")
    duration = audio_array.shape[0] / sample_rate
    print(f"Duration: {duration:.2f} seconds")
    print(f"Data Type: {audio_array.dtype}")
    
    return sample_rate, audio_array

def resample_wav(file_path, output_path, target_sample_rate=8000):
    # 显示并读取音频文件的特征
    sample_rate, audio_array = display_wav_features(file_path)
    
    # 计算新的采样点数
    num_samples_downsampled = int(audio_array.shape[0] * target_sample_rate / sample_rate)
    
    # 对每个通道进行降采样
    if audio_array.ndim == 1:  # 单声道音频
        audio_array_resampled = resample(audio_array, num_samples_downsampled)
    else:  # 多声道音频
        audio_array_resampled = np.zeros((num_samples_downsampled, audio_array.shape[1]), dtype=audio_array.dtype)
        for c in range(audio_array.shape[1]):
            audio_array_resampled[:, c] = resample(audio_array[:, c], num_samples_downsampled)
    
    # 保存降采样后的音频数据到新文件
    wavfile.write(output_path, target_sample_rate, audio_array_resampled.astype(np.int16))
    print(f"Resampled audio saved to {output_path} with sample rate {target_sample_rate} Hz")

# 示例用法
input_wav = "/home/yufeng/mdk/bin/output2.wav"
output_wav = "/home/yufeng/mdk/bin/output2.wav"
# resample_wav(input_wav, output_wav)
# display_wav_features(output_wav)
