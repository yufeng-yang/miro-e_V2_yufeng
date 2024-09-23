from pydub import AudioSegment

# 加载音频文件
audio = AudioSegment.from_wav('/home/yufeng/mdk/bin/RecordedAudio.wav')

# 将音频转换为单声道
mono_audio = audio.set_channels(1)

# 保存为新的音频文件
mono_audio.export("/home/yufeng/mdk/bin/mono.wav", format="wav")
