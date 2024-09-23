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

import sys
import os
import time
import math
import numpy as np

import rospy
import std_msgs
import geometry_msgs

import miro2 as miro

################################################################

def error(msg):

	print(msg)
	sys.exit(0)

################################################################

class Client:

	def callback_package(self, msg):

		# ignore until active
		if not self.active:
			return

		# extract opto data
		wheel_speed = np.array(msg.wheel_speed_opto.data)

		# update controller
		self.controller.update_sensors(wheel_speed)

		# write line to log file
		if self.write_log:
			w = wheel_speed
			w = np.append(w, self.controller.pose_tgt.x)
			w = np.append(w, self.controller.pose_tgt.y)
			w = np.append(w, self.controller.pose_tgt.theta)
			w = np.append(w, self.controller.pose_est.x)
			w = np.append(w, self.controller.pose_est.y)
			w = np.append(w, self.controller.pose_est.theta)
			w = np.append(w, self.cmd_vel.dr)
			w = np.append(w, self.cmd_vel.dtheta)
			sw = np.array2string(w, max_line_width=np.nan, precision=3)
			self.fid.write(sw[1:-1] + "\n")

	def loop(self):

		# output
		msg_cmd_vel = geometry_msgs.msg.TwistStamped()

		# parameters
		T = 0.05
		T_pause = 1.0
		T_move = 2.0
		T_acc = 0.5
		v_max = 0.3

		# pattern
		if self.pattern == 'square':
			theta_turn = np.pi * 0.5
		if self.pattern == 'recip':
			theta_turn = np.pi

		# compute timings
		t = 0.0
		t1 = T_pause / 2
		t2 = t1 + T_move
		t3 = t2 + T_pause
		t4 = t3 + T_move
		tf = t4 + T_pause / 2

		# loop
		while self.active and not rospy.core.is_shutdown():

			# default is no drive
			gain = 0.0
			self.cmd_vel.zero()

			# in first period, drive forward
			i = np.minimum(t - t1, t2 - t)
			if i >= 0:

				# drive forward
				gain = np.minimum(i / T_acc, 1.0)
				self.cmd_vel.dr = v_max * gain

			# in second period, turn 180 degrees
			i = np.minimum(t - t3, t4 - t)
			if i >= 0:

				# compute new position
				gain = np.minimum(i / T_acc, 1.0)
				self.cmd_vel.dtheta = theta_turn / (t4 - t3)

			# do closed-loop control
			if self.closed_loop:

				# drive controller
				self.cmd_vel = self.controller.command_velocity(self.cmd_vel, T, gain)

			# send velocity
			msg_cmd_vel.twist.linear.x = self.cmd_vel.dr
			msg_cmd_vel.twist.angular.z = self.cmd_vel.dtheta
			self.pub_cmd_vel.publish(msg_cmd_vel)

			# yield
			time.sleep(T)
			t += T
			if t >= tf:
				t = 0.0

		# finalise report
		print ("\n\nexit...")
		print (" ")

	def __init__(self, args):

		# state
		self.active = False
		self.controller = miro.lib.PoseController()
		self.cmd_vel = miro.lib.DeltaPose()

		# params
		self.closed_loop = True
		self.write_log = False
		self.pattern = 'square'

		# handle args
		for arg in args:

			if arg == "--open-loop":
				self.closed_loop = False
				continue

			if arg == "--write-log":
				self.write_log = True
				continue

			if arg == "--recip":
				self.pattern = 'recip'
				continue

			error("argument not recognised \"" + arg + "\"")

		# open log file
		if self.write_log:
			self.fid = open("/tmp/log", "w")

		# robot name
		topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")

		# subscribe
		topic = topic_base_name + "/sensors/package"
		print ("subscribe", topic)
		self.sub_package = rospy.Subscriber(topic, miro.msg.sensors_package, self.callback_package, queue_size=1, tcp_nodelay=True)

		# publish
		topic = topic_base_name + "/control/cmd_vel"
		print ("publish", topic)
		self.pub_cmd_vel = rospy.Publisher(topic, geometry_msgs.msg.TwistStamped, queue_size=0)

		# publish
		topic = topic_base_name + "/control/flags"
		print ("publish", topic)
		self.pub_flags = rospy.Publisher(topic, std_msgs.msg.UInt32, queue_size=0)

		# wait for connect
		print ("\nwait for connect... ",)
		sys.stdout.flush()
		time.sleep(1)
		print ("OK")

		# send control flags
		default_flags = miro.constants.PLATFORM_D_FLAG_DISABLE_STATUS_LEDS
		msg = std_msgs.msg.UInt32()
		msg.data = default_flags
		msg.data |= miro.constants.PLATFORM_D_FLAG_PERSISTENT
		msg.data |= miro.constants.PLATFORM_D_FLAG_DISABLE_CLIFF_REFLEX
		print ("send control flags... ",)
		print (hex(msg.data),)
		self.pub_flags.publish(msg)
		print ("OK")

		# set to active
		self.active = True

if __name__ == "__main__":

	# normal singular invocation
	rospy.init_node("client_follower", anonymous=True)
	main = Client(sys.argv[1:])
	main.loop()
