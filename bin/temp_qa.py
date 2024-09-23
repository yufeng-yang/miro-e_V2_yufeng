import rospy
from temp_audio_play import AudioPlayback
from temp_5s_record import AudioRecorder
import miro2 as miro

def QandA():
    # 初始化def main():
    # 初始化 RobotInterface
    interface = miro.lib.RobotInterface()

    # 初始化播放和录制
    playback = AudioPlayback(interface, "/miro", "/home/yufeng/mdk/bin/Question1.wav")
    
    rospy.sleep(1)
    # 播放音频
    playback.play()

    rospy.sleep(4)

    # 播放完成后进行录音
    print("播放完成，开始5秒录音...")
    recorder = AudioRecorder(interface)
    recorder.record()  # 录音 5 秒
    recorder.save_wav("/home/yufeng/mdk/bin/RecordedAudio.wav")

if __name__ == "__main__":
    QandA()

