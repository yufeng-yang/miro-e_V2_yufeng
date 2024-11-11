import gi
import rospy
from temp_audio_play import AudioPlayback
from temp_5s_record import AudioRecorder
from temp_speech_preprocess import speech_recognition
from temp_good_weather_feed import good_weather_feedback
from temp7_light_test import GoodWeatherFeedback
import miro2 as miro

# 确保我们使用的是 GTK 3
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from gi.repository import GdkPixbuf

class QandAApp(Gtk.Window):
    # def __init__(self):
    #     # 初始化 GTK 窗口
    #     Gtk.Window.__init__(self, title="Q&A 游戏")
    #     self.set_border_width(20)
    #     self.set_default_size(400, 300)

    #     # 用于检测回答是否正确的变量
    #     self.mood = None

    #     # 初始化 RobotInterface
    #     self.interface = miro.lib.RobotInterface()

    #     # 创建一个垂直盒子来放置按钮和标签
    #     vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    #     self.add(vbox)

    #     # 创建两个按钮，每个按钮播放不同的音频
    #     self.button1 = Gtk.Button(label="问题1")
    #     self.button1.connect("clicked", self.play_question1)
    #     vbox.pack_start(self.button1, True, True, 0)

    #     self.button2 = Gtk.Button(label="问题2")
    #     self.button2.connect("clicked", self.play_question2)
    #     vbox.pack_start(self.button2, True, True, 0)

    #     # 显示反馈结果的标签
    #     self.result_label = Gtk.Label(label="")
    #     vbox.pack_start(self.result_label, True, True, 0)

    #     # 显示窗口
    #     self.show_all()

    def __init__(self):
        # 初始化 GTK 窗口
        Gtk.Window.__init__(self, title="Q&A 游戏")
        self.set_border_width(20)
        self.set_default_size(800, 600)  # 设置窗口的默认大小
        self.set_resizable(False)  # 禁止窗口自动调整大小

        # 用于检测回答是否正确的变量
        self.mood = None

        # 初始化 RobotInterface
        self.interface = miro.lib.RobotInterface()  # 你的 RobotInterface 实例

        # 创建一个网格布局
        grid = Gtk.Grid()
        self.add(grid)

        # 设置窗口四周的 margin 为 5%
        grid.set_margin_top(30)
        grid.set_margin_bottom(30)
        grid.set_margin_start(30)
        grid.set_margin_end(30)

        # 加载并调整图片1
        self.image1 = Gtk.Image.new_from_file("/home/yufeng/mdk/bin/Weather_question_picture.png")  # 替换为你自己的图片路径
        button1 = Gtk.Button()
        button1.set_image(self.image1)
        button1.connect("clicked", self.play_question1)

        # 加载并调整图片2
        self.image2 = Gtk.Image.new_from_file("/home/yufeng/mdk/bin/Q2.png")  # 替换为你自己的图片路径
        button2 = Gtk.Button()
        button2.set_image(self.image2)
        button2.connect("clicked", self.play_question2)

        # 加载图片3
        self.image3 = Gtk.Image.new_from_file("/home/yufeng/mdk/bin/happy_dog.png")  # 替换为你自己的图片路径
        button3 = Gtk.Button()
        button3.set_image(self.image3)
        button3.connect("clicked", self.play_question3)

        # 加载图片4
        self.image4 = Gtk.Image.new_from_file("/home/yufeng/mdk/bin/sad_dog.png")  # 替换为你自己的图片路径
        button4 = Gtk.Button()
        button4.set_image(self.image4)
        button4.connect("clicked", self.play_question4)

        # 添加左右之间的分割带（空白）
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)

        # 将按钮按左右布局放置，左边是图片1，右边上方是图片2，右边下方是图片3和图片4
        grid.attach(button1, 0, 0, 1, 2)  # 图片1占据左边整个垂直区域
        grid.attach(separator, 1, 0, 1, 2)  # 分隔左右两部分
        grid.attach(button2, 2, 0, 2, 1)  # 图片2占据右边上半部分，跨两列
        grid.attach(button3, 2, 1, 1, 1)  # 图片3占据右边下半部分左边
        grid.attach(button4, 3, 1, 1, 1)  # 图片4占据右边下半部分右边

        # 显示反馈结果的标签，放在右边的下半部分
        self.result_label = Gtk.Label(label="")
        grid.attach(self.result_label, 2, 2, 2, 1)

        # 显示窗口
        self.show_all()

        # 让图像自适应大小
        self.connect("size-allocate", self.on_resize)

    # 当窗口大小改变时调整图片的大小
    def on_resize(self, widget, allocation):
        width = allocation.width
        height = allocation.height

        # 限制图片的最小和最大宽度和高度
        min_width, max_width = 150, 400  # 最小和最大宽度
        min_height, max_height = 150, 400  # 最小和最大高度

        #计算目标宽度
        image1_width = max(min(int(width * 0.35), max_width), min_width)
        image2_width = max(min(int(width * 0.25), max_width), min_width)
        image3_width = max(min(int(width * 0.12), max_width), min_width)
        image4_width = max(min(int(width * 0.12), max_width), min_width)



        # 使用Pixbuf加载图片并按比例调整宽度和高度
        self.image1.set_from_pixbuf(self.get_resized_pixbuf("/home/yufeng/mdk/bin/Weather_question_picture.png", image1_width))
        self.image2.set_from_pixbuf(self.get_resized_pixbuf("/home/yufeng/mdk/bin/Q2.png", image2_width))
        self.image3.set_from_pixbuf(self.get_resized_pixbuf("/home/yufeng/mdk/bin/happy_dog.png", image3_width))
        self.image4.set_from_pixbuf(self.get_resized_pixbuf("/home/yufeng/mdk/bin/sad_dog.png", image4_width))

    def get_resized_pixbuf(self, image_path, target_width):
        # 从文件加载图片
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_path)
        # 获取图片的宽高比
        ratio = pixbuf.get_width() / pixbuf.get_height()
        # 根据目标宽度计算目标高度，保持宽高比
        target_height = int(target_width / ratio)
        # 返回调整后的Pixbuf对象
        return pixbuf.scale_simple(target_width, target_height, GdkPixbuf.InterpType.BILINEAR)

    def play_question1(self, widget):
        # 播放问题1
        self.playback("/home/yufeng/mdk/output.wav", ["sunny", "good", "warm"])

    def play_question2(self, widget):
        # 播放问题2
        self.playback("/home/yufeng/mdk/bin/Question2.wav", ["answer2"])

    def play_question3(self, widget):
        # 调用封装好的行为类
        feedback = GoodWeatherFeedback(self.interface, "happy")
        feedback.main()

    def play_question4(self, widget):
        # 播放问题2
        # self.playback("/home/yufeng/mdk/bin/Question2.wav", ["answer4"])
        feedback = GoodWeatherFeedback(self.interface, "sad")
        feedback.main()


    def playback(self, question_file, expected_answer):
        # 播放音频
        playback = AudioPlayback(self.interface, "/miro", question_file)
        # print("=======")
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
            # happy_dog = good_weather_feedback(self.interface,self.mood)
            happy_dog = GoodWeatherFeedback(self.interface,self.mood)
            happy_dog.main()
        else:
            print("执行'难过'的回应")
            # 机器人可以执行另一个行为，例如播放“鼓励”的音频
            # self.interface.play_sound("sad_sound.wav")  # 伪代码，实际执行根据接口实现
            sad_dog = GoodWeatherFeedback(self.interface,self.mood)
            sad_dog.main()

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


