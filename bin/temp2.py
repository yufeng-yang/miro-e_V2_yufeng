import rospy
from std_msgs.msg import UInt16MultiArray, Int16MultiArray

import time
import sys
import os
import numpy as np
import wave, struct

import miro2 as miro
from scipy.io import wavfile
from scipy.signal import resample


BUFFER_STUFF_SAMPLES = 4000

# messages larger than this will be dropped by the receiver,
# however, so - whilst we can stuff the buffer more than this -
# we can only send this many samples in any single message.

# 这个用于限制传输时，每次传输的包的大小，48是预留给头文件的
# 具体在哪定义的目前没有找到
# 但是一旦超出这个数字，就会导致接受方丢弃多余的部分
MAX_STREAM_MSG_SIZE = (4096 - 48)

# using a margin avoids sending many small messages - instead
# we will send a smaller number of larger messages, at the cost
# of being less precise in respecting our buffer stuffing target.
BUFFER_MARGIN = 1000
BUFFER_MAX = BUFFER_STUFF_SAMPLES + BUFFER_MARGIN
BUFFER_MIN = BUFFER_STUFF_SAMPLES - BUFFER_MARGIN



# microphone sample rate
MIC_SAMPLE_RATE = 20000

# sample count
SAMPLE_COUNT = 171897

# RECORE Time
RECORD_TIME = SAMPLE_COUNT/MIC_SAMPLE_RATE



class speechtest:
    def space_detecter(self, msg):
    # 用于根据总空间和使用空间，计算差额得到传输数据的大小
        # buffer_space: 剩余空间
        self.buffer_space = msg.data[0]
        # 总空间
        self.buffer_total = msg.data[1]
        # buffer_stuff: 缓冲区使用的容量，是目前被使用的缓冲区容量
        # 更准确的来说，是被订阅的这个topic的缓冲区当前被使用的容量
        self.buffer_stuff = self.buffer_total - self.buffer_space
        # print(msg)

    def wait(self):
        # 检查是否收到了buffer_space的数据
        while self.buffer_space is None or self.buffer_total is None:
            print("等待接收到 buffer_space 和 buffer_total 数据...")
            time.sleep(0.02)

    def loop(self):
        # 这是循环函数，也是主函数
        # outbuf是作为最终输出的缓冲区，不过被定义为16000行，0列的数据
        outbuf = np.zeros((int(SAMPLE_COUNT / 2.5), 0))
        # 这里的c是指通道，即四个通道，分别对应四个麦克风
        for c in range(4):
            # i是从0-40000,按照每2.5一个隔开，这里的i是用作序列，方便后续插值的
            i = np.arange(0, int(SAMPLE_COUNT), 2.5)
            # j又是从0-40000,不过此时是原本的序列，代表原本采集率（16k）下的序列号码
            j = np.arange(0, SAMPLE_COUNT)
            # x就是插值产生的新数据了。
            # 工作原理如下，i中的第一个为序列0,刚好j中就有序列0,因此就是元数据
            # i中第二个为2.5,j中没有2.5这个序列对应的数据，此时就是interp发挥作用，开始从序列2到序列3中进行插值了
            x = np.interp(i, j, self.outbuf[:, c])
            # 还记得之前0列的outbuf吗，此时就按照c=0 -- c=3,分别安装上4列数据，每列都对应一个通道
            outbuf = np.concatenate((outbuf, x[:, np.newaxis]), axis=1)
        
        # 不进行降采样
        # outbuf = self.outbuf
        ########################

        # channel names
        chan = ["LEFT", "RIGHT", "CENTRE", "TAIL"]

        # loop
        while not rospy.core.is_shutdown():

            # stuff output buffer
            # 之前定义的BUFFER_MIN就开始发挥作用了。
            if self.buffer_stuff < BUFFER_MIN:

                # report
                # playsamp 是已经发送出去的数据大小
                # 如果是0就说明，某一个playchan刚刚开始发送
                if self.playsamp == 0:

                    # report
                    print ("echo recording from " + chan[self.playchan] + " microphone...")

                # desired amount to send
                n_samp = BUFFER_MAX - self.buffer_stuff

                # limit by receiver buffer space
                # 避免发送的信息大小大于接受方的空闲空间
                n_samp = np.minimum(n_samp, self.buffer_space)

                # limit by amount available to send
                # 用于避免发送的大小，大于某个playchan剩余的数据
                n_samp = np.minimum(n_samp, outbuf.shape[0] - self.playsamp)

                # limit by maximum individual message size
                n_samp = np.minimum(n_samp, MAX_STREAM_MSG_SIZE)

                # prepare data
                # 这里的spkrdata指的是，本次将要传输的数据。
                # ！！这里终于是数据的，之前的n_samp是索引，而playsamp也是索引，是目前发到哪一个数据的索引
                # 因此这里就是从outbuf中取出数据。根据目前发送到那一个至目前+本次发送多少个，这一段数据。
                # 最后的playchan表明发送的是哪一个声道的数据
                spkrdata = outbuf[self.playsamp:(self.playsamp+n_samp), self.playchan]
                # 发送完成后，更新索引
                self.playsamp += n_samp

                # send data
                # 这里可以看出，传输的数据是int16格式的数据
                # 这个消息格式本身不对传输数量做任何限制，限制传输数量的是我之前那些代码
                # 该消息格式只是将每一个sample的大小范围，控制在int16,也就是-32768 到 32767
                msg = Int16MultiArray()
                # 将spkrdata中的数据转化为int
                msg.data = [int(i) for i in spkrdata]
                # 将msg发布出去
                self.pub_stream.publish(msg)

                # update buffer_stuff so that we don't send
                # again until we get some genuine feedback

                # !! 这一步也很重要，防止数据溢出的
                # 每次发送完，将大小设置为BUFFER_MIN，此时就不会再次发送，直到等到buffer_stuff被
                # 机器人手动更新
                self.buffer_stuff = BUFFER_MIN

                # finished?
                if self.playsamp == outbuf.shape[0]:

                    # move to next channel
                    self.playsamp = 0
                    self.playchan += 1

                    # finished?
                    if self.playchan == 4:

                        # clear output
                        print ("(playback complete)")
                        break

            # state
            time.sleep(0.02)

        # Disconnect the interface
        self.interface.disconnect()

    def __init__(self):
        # Create robot interface
        self.interface = miro.lib.RobotInterface()

		# state
        with wave.open('/home/yufeng/mdk/bin/client_audio.wav', 'rb') as wav_file:
        # 读取所有帧数据
            audio_data = wav_file.readframes(wav_file.getnframes())
        
            # 将音频数据转换为 numpy 数组，格式为 16 位小端序
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
        
            # 因为是双声道（2 channels），需要 reshape 成 (n_frames, 2)
            audio_array = audio_array.reshape(-1, 4)

        # print('#########')
        # print(audio_array)
        self.outbuf = audio_array
        self.buffer_stuff = 0
        # self.mode = mode
        self.playchan = 0
        self.playsamp = 0
        self.buffer_space =None
        self.buffer_total = None

        # # check mode
        # if not (mode == "echo" or mode == "record" or mode == "record4"):
        # 	error("argument not recognised")

        # robot name
        topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")

        # publish
        topic = topic_base_name + "/control/stream"
        print ("publish", topic)
        self.pub_stream = rospy.Publisher(topic, Int16MultiArray, queue_size=0)

        # subscribe
        topic = topic_base_name + "/sensors/stream"
        print ("subscribe", topic)
        self.sub_stream = rospy.Subscriber(topic, UInt16MultiArray, self.space_detecter, queue_size=1, tcp_nodelay=True)

        #subscribe to mics using robot Interface
        # self.interface.register_callback("microphones", self.callback_mics)

        # report
        print ("recording from 4 microphones for", RECORD_TIME, "seconds...")

if __name__ == "__main__":

    main = speechtest()
    # main.loop()
    main.wait()
    main.loop()