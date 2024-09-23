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

import math, time, sys
import numpy as np
import traceback

import miro2 as miro

################################################################

class client:

	def sensors_callback(self, sensors):

		# received sensor data
		#print(sensors)
		pass

	def loop(self):

		# constant control signal
		dr = 0.2
		dtheta = 0.5
		timeout = 1
		T = 0.1

		# loop
		while self.interf.is_active():

			# if you want, you can sync with the commands sent to
			# the robot, here (this yields until the commands are sent)
			self.interf.wait_for_control_boundary()

			# send command to interface
			self.interf.set_vel(dr, dtheta, timeout)

		# finalise report
		print ("\n\nexit...")
		print (" ")

	def __init__(self, args):

		# defaults
		flags = 0
		use_pose_control = True

		# handle args
		for arg in args:

			if arg == "--no-cliff-reflex":
				flags |= miro.constants.PLATFORM_D_FLAG_DISABLE_CLIFF_REFLEX

			elif arg == "--open-loop":
				use_pose_control = False

			else:
				raise Exception("unknown argument '" + arg + "'")

		# get interface to robot
		self.interf = miro.lib.RobotInterface(flags=flags, use_pose_control=use_pose_control)

		# register to receive sensors callback
		self.interf.register_callback("sensors", self.sensors_callback)

		# run loop
		try:
			self.loop()
		except Exception as e:
			print(traceback.format_exc())

		# disconnect interface
		self.interf.disconnect()

################################################################

if __name__ == "__main__":

	# normal singular invocation
	main = client(sys.argv[1:])
