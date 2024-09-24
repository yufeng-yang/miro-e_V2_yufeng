import gi
import rospy
from temp_audio_play import AudioPlayback
from temp_5s_record import AudioRecorder
from temp_speech_preprocess import speech_recognition
from temp_good_weather_feed import good_weather_feedback
import miro2 as miro

# 确保我们使用的是 GTK 3
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class QandAApp(Gtk.Window):
    def __init__(self):
        # 初始化 GTK 窗口
        Gtk.Window.__init__(self, title="Q&A 游戏")
        self.set_border_width(20)
        self.set_default_size(400, 300)

        # 用于检测回答是否正确的变量
        self.mood = None

        # 初始化 RobotInterface
        self.interface = miro.lib.RobotInterface()

        # 创建一个垂直盒子来放置按钮和标签
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        # 创建两个按钮，每个按钮播放不同的音频
        self.button1 = Gtk.Button(label="问题1")
        self.button1.connect("clicked", self.play_question1)
        vbox.pack_start(self.button1, True, True, 0)

        self.button2 = Gtk.Button(label="问题2")
        self.button2.connect("clicked", self.play_question2)
        vbox.pack_start(self.button2, True, True, 0)

        # 显示反馈结果的标签
        self.result_label = Gtk.Label(label="")
        vbox.pack_start(self.result_label, True, True, 0)

        # 显示窗口
        self.show_all()

    def play_question1(self, widget):
        # 播放问题1
        self.playback("/home/yufeng/mdk/bin/Weather_Q.wav", ["sunny", "good", "warm"])

    def play_question2(self, widget):
        # 播放问题2
        self.playback("/home/yufeng/mdk/bin/Question2.wav", ["answer2"])

    def playback(self, question_file, expected_answer):
        # 播放音频
        playback = AudioPlayback(self.interface, "/miro", question_file)

        # 播放音频并暂停 1 秒
        rospy.sleep(1)
        playback.play()

        # 等待音频播放完成
        while True:
            if playback.finish_question is True:
                rospy.sleep(1)
                print("播放完成，开始5秒录音...")
                # 开始录音并保存为文件
                recorder = AudioRecorder(self.interface)
                recorder.record()  # 录音 5 秒
                recorder.save_wav("/home/yufeng/mdk/bin/RecordedAudio.wav")
                break
            else:
                print("等待提问完成...")
                rospy.sleep(0.2)

        # 录音完成后进行语音识别
        rospy.sleep(1)
        sr = speech_recognition(self.interface)
        answer = sr.full_service()
        print(answer)
        # 检查答案是否正确
        self.check_answer(answer, expected_answer)

    def check_answer(self, answer, expected_keywords):
        # 如果识别到的答案中包含任意一个正确的关键词
        if any(keyword in answer for keyword in expected_keywords):
            self.result_label.set_text(answer)
            print("开心")
            self.mood = "happy"
        else:
            self.result_label.set_text(answer)
            self.result_label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 0, 0, 1))  # 红色字体
            print("难过")
            self.mood = "sad"
        
        self.respond_to_answer()
    
    def respond_to_answer(self):
        # 如果机器人检测到的情绪为 "happy"，执行相应的动作
        if self.mood == "happy":
            print("执行'开心'的回应")
            # 在此添加 ROS 机器人的响应行为，例如播放奖励音频
            # 机器人可以执行特定的行为
            # self.interface.play_sound("happy_sound.wav")  # 伪代码，实际执行根据接口实现
            happy_dog = good_weather_feedback(self.interface,self.mood)
            happy_dog.main()
        else:
            print("执行'难过'的回应")
            # 机器人可以执行另一个行为，例如播放“鼓励”的音频
            # self.interface.play_sound("sad_sound.wav")  # 伪代码，实际执行根据接口实现

def main():
    # 初始化 GTK 应用程序
    app = QandAApp()
    app.connect("destroy", Gtk.main_quit)  # 关闭窗口时退出程序

    # 开始 GTK 主事件循环
    Gtk.main()

if __name__ == "__main__":
    main()




# import tkinter as tk
# import rospy
# from temp_audio_play import AudioPlayback
# from temp_5s_record import AudioRecorder
# from temp_speech_preprocess import speech_recognition
# import miro2 as miro

# class QandAApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Q&A Game")

#         # 这是一个用于检测回答是否正确的变量
#         self.mood = None

#         # 初始化 RobotInterface
#         self.interface = miro.lib.RobotInterface()

#         # 创建两个按钮，每个按钮播放不同的音频
#         self.button1 = tk.Button(root, text="问题1", command=self.play_question1)
#         self.button1.pack(pady=20)

#         self.button2 = tk.Button(root, text="问题2", command=self.play_question2)
#         self.button2.pack(pady=20)

#         # 显示反馈结果
#         self.result_label = tk.Label(root, text="")
#         self.result_label.pack(pady=20)

#     def play_question1(self):
#         # 播放问题1
#         self.playback("/home/yufeng/mdk/bin/Weather_Q.wav", ["sunny", "good", "warm"])

#     def play_question2(self):
#         # 播放问题2
#         self.playback("/home/yufeng/mdk/bin/Question2.wav", "answer2")

#     def playback(self, question_file, expected_answer):
#         # 播放音频
#         playback = AudioPlayback(self.interface, "/miro", question_file)

#         rospy.sleep(1)
#         playback.play()

#         while True:
#             if playback.finish_question is True:
#                 rospy.sleep(1)
#                 print("播放完成，开始5秒录音...")
#                 recorder = AudioRecorder(self.interface)
#                 recorder.record()  # 录音 5 秒
#                 recorder.save_wav("/home/yufeng/mdk/bin/RecordedAudio.wav")
#                 break
#             else:
#                 print("waiting asking")
#                 rospy.sleep(0.2)

#         rospy.sleep(1)
#         sr = speech_recognition(self.interface)
#         answer = sr.full_service()
#         print(answer)
#         self.check_answer(answer, expected_answer)

#     def check_answer(self, answer, expected_keywords):
#         if any(keyword in answer for keyword in expected_keywords):
#             self.result_label.config(text=answer, fg="green")
#             print("happy")
#             self.mood = "happy"
            
#         else:
#             self.result_label.config(text=answer, fg="red")
#             print("sad")
#             self.mood = "sad"

# def main():

#     # 创建主窗口
#     root = tk.Tk()

#     # 创建应用程序实例
#     app = QandAApp(root)

#     # 进入 Tkinter 事件循环
#     root.mainloop()

#     while not rospy.core.is_shutdown():
#         if app.mood is "None":
#             rospy.sleep(0.5)
#         else:
#             break
    
#     if app.mood is "happy":
#         print(666)
#     else:
#         print(111)


# if __name__ == "__main__":
#     main()






# def QandA():
#     # 初始化def main():
#     # 初始化 RobotInterface
#     interface = miro.lib.RobotInterface()

#     # 初始化播放和录制
#     playback = AudioPlayback(interface, "/miro", "/home/yufeng/mdk/bin/Question1.wav")
    
#     rospy.sleep(1)
#     # 播放音频
#     playback.play()

#     # 目前是一个预设的状态，后期看看能不能修改
#     # rospy.sleep(4)
#     while True:
#         if playback.finish_question is True:
#             # 播放完成后进行录音
#             rospy.sleep(1)
#             print("播放完成，开始5秒录音...")
#             recorder = AudioRecorder(interface)
#             recorder.record()  # 录音 5 秒
#             recorder.save_wav("/home/yufeng/mdk/bin/RecordedAudio.wav")
#             break

        
#         else:
#             print("waiting asking")
#             rospy.sleep(0.2)

#     rospy.sleep(1)
#     sr = speech_recognition(interface)
#     answer = sr.full_service()
#     print(answer)
#     if "answer" in answer:
#         print("happy")


