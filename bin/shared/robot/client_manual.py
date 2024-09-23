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

import math
import numpy as np
import sys, os, time
import curses
import argparse

import miro2 as miro

################################################################

class client:

	def loop(self, stdscr):

		# turn off delay
		stdscr.nodelay(1)

		# output
		dtheta = 2.0
		dy = 0.2
		timeout = 0.5

		# use getch() once so that print works (why?)
		c = stdscr.getch()

		# instructions
		print ("Use arrow keys to control MIRO directly.\r")
		print ("Press ESCAPE to exit\r")

		# loop
		while self.interf.is_active():

			# this is a terrible way of getting the keydown
			# state, but it seems that it's a challenge to
			# do it well in Python for some reason.
			c = stdscr.getch()

			if c != -1:

				if c == 260:
					self.interf.set_vel(0, dtheta, timeout)
				elif c == 261:
					self.interf.set_vel(0, -dtheta, timeout)
				elif c == 259:
					self.interf.set_vel(dy, 0, timeout)
				elif c == 258:
					self.interf.set_vel(-dy, 0, timeout)
				elif c == 32:
					self.interf.set_vel(0, 0, timeout)
				elif c == 27:
					self.interf.term()
				else:
					print (c)
					pass

			# flush buffer
			while c != -1:
				c = stdscr.getch()

			# yield
			time.sleep(0.1)

		# finalise report
		print ("\n\nexit...")
		print (" ")

	def __init__(self):

		# args
		parser = argparse.ArgumentParser(description='manually control your robot')
		parser.add_argument('--name', dest='robot_name', default=None,
				help='specify the robot to connect to')
		args = parser.parse_args()

		# get interface to robot
		self.interf = miro.lib.RobotInterface(robot_name=args.robot_name)

		# run loop
		curses.wrapper(self.loop)

		# disconnect interface
		self.interf.disconnect()

################################################################

if __name__ == "__main__":

	# normal singular invocation
	main = client()
