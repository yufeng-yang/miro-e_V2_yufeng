#!/usr/bin/python3
#
#	@section COPYRIGHT
#	Copyright (C) 2023 Consequential Robotics Ltd
#	
#	@section AUTHOR
#	Consequential Robotics http://consequentialrobotics.com
#	
#	@section LICENSE
#	For a full copy of the license agreement, and a complete
#	definition of "The Software", see LICENSE in the MDK root
#	directory.
#	
#	Subject to the terms of this Agreement, Consequential
#	Robotics grants to you a limited, non-exclusive, non-
#	transferable license, without right to sub-license, to use
#	"The Software" in accordance with this Agreement and any
#	other written agreement with Consequential Robotics.
#	Consequential Robotics does not transfer the title of "The
#	Software" to you; the license granted to you is not a sale.
#	This agreement is a binding legal agreement between
#	Consequential Robotics and the purchasers or users of "The
#	Software".
#	
#	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
#	KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#	WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
#	PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
#	OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
#	OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#	OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#	SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#	

import rospy
from std_msgs.msg import UInt16MultiArray, Int16MultiArray

import time
import sys
import os
import numpy as np
import wave, struct

import miro2 as miro

# amount to keep the buffer stuffed - larger numbers mean
# less prone to dropout, but higher latency when we stop
# streaming. with a read-out rate of 8k, 4000 samples will
# buffer for half of a second, for instance.

# 这里的这个参数表示的是，缓冲区的大小。比如这里设置为4000,那么假设read-out rate
# 也就是音频的读取率为8k时，传输会等待缓冲区被填满，再开始播放
# 这就是延迟0.5s开始播放的原因。
# 因此越大的缓冲区造成越大的延迟，越小的缓冲区虽然减少播放延迟，但是很容易
# 收到网络波动的影响。
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

# how long to record before playing back in seconds?
RECORD_TIME = 10

# microphone sample rate (also available at miro2.constants)
MIC_SAMPLE_RATE = 20000

# sample count
SAMPLE_COUNT = RECORD_TIME * MIC_SAMPLE_RATE



################################################################

def error(msg):
	print(msg)
	sys.exit(0)

################################################################

# if no argument provided
if len(sys.argv) != 2:

	# show usage
	print ("pass one of the following arguments:")
	print ("\trecord: record stereo audio (ear mics) and store to /tmp/client_audio.wav")
	print ("\trecord4: record all four mics (centre and tail mics as well as ear mics)")
	print ("\techo: record audio then stream back to platform immediately")

	# done
	exit()


################################################################

class client:

	def callback_stream(self, msg):
		# 这里的msg似乎是用于传输的信息

		self.buffer_space = msg.data[0]
		self.buffer_total = msg.data[1]
		self.buffer_stuff = self.buffer_total - self.buffer_space
		# print('###########')
		# print(msg)
		# print('-=============')
	def callback_mics(self, msg):

		# if recording
		if not self.micbuf is None:
			# 这里的micbuf似乎是麦克风接收到数据的缓存区域
			# 因此有这个区域存在的话，就说明有录音任务

			# append mic data to store
			# 这里似乎可以确定，msg.data确实是用于传输数据的。
			# 他把传输的数据附加到了，micbuf上面
			self.micbuf = np.concatenate((self.micbuf, msg.data))

			# report
			sys.stdout.write(".")
			sys.stdout.flush()

			# finished recording?
			# 第一个参数在这里首次被使用了。超过sample rate×second，一旦放满就说明传输完成
			if self.micbuf.shape[0] >= SAMPLE_COUNT:

				# end recording
				# 录音完成，把录好的存为outbuf
				self.outbuf = self.micbuf
				# 并把micbuf设置为None
				self.micbuf = None
				print(self.outbuf)
				print('###############')
				print (" OK!")

	# cilent类下的loop方法
	def loop(self):

		# loop
		# 当节点没有被关闭时候,几乎可以说是一直在运行了
		while not rospy.core.is_shutdown():

			# if recording finished
			#除非录制已经完成，才会进入下一步判断，否则会不停的休0.2秒
			if not self.outbuf is None:
				break

			# state
			time.sleep(0.02)

		# 跑出来到这里了，说明录制已经完成了，那么就要根据输入的参数，来决定实现哪一个功能。
		# if echo
		if self.mode == "echo":

			# 还记得嘛，这里的outbuf就是从micbuf链接而来的，就是录制好的2s采样率20k的音频。
			# SAMPLE_COUNT就是当年设定好的outbuf的大小，也就是2×20k
			# downsample for playback

			# outbuf是作为最终输出的缓冲区，不过被定义为16000行，0列的数据
			outbuf = np.zeros((int(SAMPLE_COUNT / 2.5), 0))
			# 这里的c是指通道，即四个通道，分别对应四个麦克风
			for c in range(4):
				# i是从0-40000,按照每2.5一个隔开，这里的i是用作序列，方便后续插值的
				i = np.arange(0, SAMPLE_COUNT, 2.5)
				# j又是从0-40000,不过此时是原本的序列，代表原本采集率（16k）下的序列号码
				j = np.arange(0, SAMPLE_COUNT)
				# x就是插值产生的新数据了。
				# 工作原理如下，i中的第一个为序列0,刚好j中就有序列0,因此就是元数据
				# i中第二个为2.5,j中没有2.5这个序列对应的数据，此时就是interp发挥作用，开始从序列2到序列3中进行插值了
				x = np.interp(i, j, self.outbuf[:, c])
				# 还记得之前0列的outbuf吗，此时就按照c=0 -- c=3,分别安装上4列数据，每列都对应一个通道
				outbuf = np.concatenate((outbuf, x[:, np.newaxis]), axis=1)

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

		# if record
		if self.mode == "record" or self.mode == "record4":

			# write output file
			outfilename = '/tmp/client_audio.wav'
			file = wave.open(outfilename, 'wb')
			file.setsampwidth(2)
			file.setframerate(MIC_SAMPLE_RATE)

			# write data
			if self.mode == "record4":
				print ("writing all four channels to file...")
				file.setnchannels(4)
				x = np.reshape(self.outbuf[:, :], (-1))
				for s in x:
					file.writeframes(struct.pack('<h', s))
			else:
				print ("writing two channels to file (LEFT and RIGHT)...")
				file.setnchannels(2)
				x = np.reshape(self.outbuf[:, [0, 1]], (-1))
				for s in x:
					file.writeframes(struct.pack('<h', s))

			# close file
			file.close()
			print ("wrote output file at", outfilename)
	# mode就是用在这里的，设定为什么模式，比如echo模式还是recore或者record4
	def __init__(self, mode):

		# Create robot interface
		self.interface = miro.lib.RobotInterface()

		# state
		self.micbuf = np.zeros((0, 4), 'uint16')
		self.outbuf = None
		self.buffer_stuff = 0
		self.mode = mode
		self.playchan = 0
		self.playsamp = 0

		# check mode
		if not (mode == "echo" or mode == "record" or mode == "record4"):
			error("argument not recognised")

		# robot name
		topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")

		# publish
		topic = topic_base_name + "/control/stream"
		print ("publish", topic)
		self.pub_stream = rospy.Publisher(topic, Int16MultiArray, queue_size=0)

		# subscribe
		topic = topic_base_name + "/sensors/stream"
		print ("subscribe", topic)
		self.sub_stream = rospy.Subscriber(topic, UInt16MultiArray, self.callback_stream, queue_size=1, tcp_nodelay=True)

		#subscribe to mics using robot Interface
		self.interface.register_callback("microphones", self.callback_mics)

		# report
		print ("recording from 4 microphones for", RECORD_TIME, "seconds...")

if __name__ == "__main__":

	main = client(sys.argv[1])
	main.loop()
