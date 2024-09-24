import wave
import os
from pydub import AudioSegment
import speech_recognition as sr
import rospy

class speech_recognition:
    def __init__(self,interface):
        self.interface = interface
        
    # 先确认格式
    def check_format(self):
        # 检查文件是否存在
        file_path = '/home/yufeng/mdk/bin/RecordedAudio.wav'
        if not os.path.exists(file_path):
            print(f"文件 {file_path} 不存在")
            return
        # 打开wav文件
        with wave.open('/home/yufeng/mdk/bin/RecordedAudio.wav', 'rb') as wav_file:
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
    
    # 预处理到能够进行语音识别的格式
    def preprocessing(self):
        # 加载音频文件
        audio = AudioSegment.from_wav('/home/yufeng/mdk/bin/RecordedAudio.wav')

        # 将音频转换为单声道
        mono_audio = audio.set_channels(1)

        # 保存为新的音频文件
        mono_audio.export("/home/yufeng/mdk/bin/mono.wav", format="wav")

    # 识别
    def recognition(self):
        # 初始化语音识别器
        recognizer = sr.Recognizer()

        # 加载音频文件
        while True:
            # 检查文件是否存在
            file_path = '/home/yufeng/mdk/bin/mono.wav'
            if not os.path.exists(file_path):
                print(f"文件 {file_path} 不存在, waiting")
                rospy.sleep(0.2)
            
            else:
                break
                
        with sr.AudioFile(file_path) as source:
            # 读取音频数据
            audio_data = recognizer.record(source)
            
            # 使用谷歌语音识别进行识别
            try:
                text = recognizer.recognize_google(audio_data, language='en')  # 设置识别语言
                print(f"识别结果: {text}")
                return text
            except sr.UnknownValueError:
                print("Sorry, I cant realise")
            except sr.RequestError as e:
                print(f"无法请求谷歌语音识别服务; {e}")

        
    def full_service(self):
        self.check_format()
        self.preprocessing()
        answer = self.recognition()
        return answer



