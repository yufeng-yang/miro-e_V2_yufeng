import wave

# 打开wav文件
with wave.open('/home/yufeng/mdk/bin/happy_dog_sound.WAV', 'rb') as wav_file:
    # 获取通道数
    n_channels = wav_file.getnchannels()
    # 获取采样宽度（字节数）
    sampwidth = wav_file.getsampwidth()
    # 获取采样率
    framerate = wav_file.getframerate()
    # 获取帧数
    n_frames = wav_file.getnframes()
    # 计算音频时长
    duration = n_frames / framerate

    print(f"通道数: {n_channels}")
    print(f"采样宽度（字节数）: {sampwidth}")
    print(f"采样率: {framerate} Hz")
    print(f"音频时长: {duration} 秒")
