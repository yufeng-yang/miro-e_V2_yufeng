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

# create node
import rospy
rospy.init_node("client_minimal", anonymous=True)

################################################################

# to use in MIROcode, copy everything below this line into the
# MIROcode Python editor.
#
# vvvvvv vvvvvv vvvvvv vvvvvv

################################################################

import os
import sys
import time
import numpy as np

import miro2 as miro
import geometry_msgs

################################################################

class controller:

	def callback_package(self, msg):

		# report
		vbat = np.round(np.array(msg.battery.voltage) * 100.0) / 100.0
		if not vbat == self.vbat:
			self.vbat = vbat
			print ("battery", vbat)

	def loop(self):

		# state
		t_now = 0.0
		msg_wheels = geometry_msgs.msg.TwistStamped()

		# loop
		while t_now < 1.0 and not rospy.core.is_shutdown():

			# send wheels
			msg_wheels.twist.linear.x = 0.2
			msg_wheels.twist.angular.z = 0.5
			self.pub_wheels.publish(msg_wheels)

			# state
			time.sleep(0.02)
			t_now = t_now + 0.02

	def __init__(self, args):
	
		# state
		self.vbat = 0

		# robot name
		topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")

		# publish
		topic = topic_base_name + "/control/cmd_vel"
		print ("publish", topic)
		self.pub_wheels = rospy.Publisher(topic, geometry_msgs.msg.TwistStamped, queue_size=0)

		# subscribe
		topic = topic_base_name + "/sensors/package"
		print ("subscribe", topic)
		self.sub_package = rospy.Subscriber(topic, miro.msg.sensors_package,
					self.callback_package, queue_size=1, tcp_nodelay=True)

		# wait for connect
		print ("wait for connect...")
		time.sleep(1)

if __name__ == "__main__":

	# normal singular invocation
	main = controller(sys.argv[1:])
	main.loop()

