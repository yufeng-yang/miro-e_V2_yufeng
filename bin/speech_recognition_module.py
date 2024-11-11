import speech_recognition as sr

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("请说话...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("recognizing and judging your mood...")
        text = recognizer.recognize_google(audio, language="en-US")
        print(f"(your mood is happy) you said: {text}")
        return text
    except sr.UnknownValueError:
        print("抱歉，无法理解你的话。")
        return None
    except sr.RequestError:
        print("无法连接到语音识别服务。")
        return None