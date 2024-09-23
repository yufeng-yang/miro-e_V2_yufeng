import speech_recognition as sr

# 初始化语音识别器
recognizer = sr.Recognizer()

# 加载音频文件
audio_file = '/home/yufeng/mdk/bin/mono.wav'
with sr.AudioFile(audio_file) as source:
    # 读取音频数据
    audio_data = recognizer.record(source)
    
    # 使用谷歌语音识别进行识别
    try:
        text = recognizer.recognize_google(audio_data, language='en-US')  # 设置识别语言
        print(f"识别结果: {text}")
    except sr.UnknownValueError:
        print("谷歌语音识别无法理解音频")
    except sr.RequestError as e:
        print(f"无法请求谷歌语音识别服务; {e}")
