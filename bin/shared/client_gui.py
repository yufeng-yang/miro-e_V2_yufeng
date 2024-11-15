# #!/usr/bin/python3
# #
# #	@section COPYRIGHT
# #	Copyright (C) 2023 Consequential Robotics Ltd
# #	
# #	@section AUTHOR
# #	Consequential Robotics http://consequentialrobotics.com
# #	
# #	@section LICENSE
# #	For a full copy of the license agreement, and a complete
# #	definition of "The Software", see LICENSE in the MDK root
# #	directory.
# #	
# #	Subject to the terms of this Agreement, Consequential
# #	Robotics grants to you a limited, non-exclusive, non-
# #	transferable license, without right to sub-license, to use
# #	"The Software" in accordance with this Agreement and any
# #	other written agreement with Consequential Robotics.
# #	Consequential Robotics does not transfer the title of "The
# #	Software" to you; the license granted to you is not a sale.
# #	This agreement is a binding legal agreement between
# #	Consequential Robotics and the purchasers or users of "The
# #	Software".
# #	
# #	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# #	KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# #	WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# #	PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# #	OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# #	OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# #	OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# #	SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# #	

# import time
# import gi
# import os

# gi.require_version('Gtk', '3.0')
# from gi.repository import Gtk, GObject, GdkPixbuf, Gdk, GLib

# import rospy
# from std_msgs.msg import Float32MultiArray, UInt32MultiArray, UInt16MultiArray, UInt8MultiArray, UInt16, Int16MultiArray, String
# from geometry_msgs.msg import TwistStamped
# from sensor_msgs.msg import JointState, CompressedImage

# import cv2
# from cv_bridge import CvBridge, CvBridgeError
# import numpy as np

# import math
# import miro2 as miro



# from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation


# def format_num(n, d=2):
# 	s = ("{:." + str(d) + "f}").format(n)
# 	if n >= 0:
# 		s = " " + s;
# 	return s

# def wiggle(v, n, m):
# 	v = v + float(n) / float(m)
# 	if v > 2.0:
# 		v -= 2.0
# 	elif v > 1.0:
# 		v = 2.0 - v
# 	return v

# def generate_illum(colour, bright):

# 	rgb_str = colour.to_string()
# 	useless, rgb_values = rgb_str.split("(")
# 	rgb_values, useless = rgb_values.split(")")
# 	r, g, b = rgb_values.split(",")
# 	r = int(r)
# 	g = int(g)
# 	b = int(b)
# 	return (int(bright) << 24) | (r << 16) | (g << 8) | b

# def update_range(objs, lo, hi):
# 	for obj in objs:
# 		obj.set_lower(np.degrees(lo))
# 		obj.set_upper(np.degrees(hi))


# #Generate a fake enum for joint arrays
# tilt, lift, yaw, pitch = range(4)
# droop, wag, left_eye, right_eye, left_ear, right_ear = range(6)
# freq, volume, duration = range(3)
# front_left, mid_left, rear_left, front_right, mid_right, rear_right = range(6)
# closing = True
# opening = False
# right = True
# left = False

# class miro_gui:

# 	def __init__(self):

# 		# state
# 		self.step = 0

# 		#Load GUI from glade file
# 		self.builder = Gtk.Builder()
# 		self.builder.add_from_file("client_gui.glade")

# 		# update constants in builder
# 		update_range([
# 			self.builder.get_object("lift_adjustment"),
# 			self.builder.get_object("lift_meas_adjustment")
# 		], miro.constants.LIFT_RAD_MIN, miro.constants.LIFT_RAD_MAX)
# 		update_range([
# 			self.builder.get_object("yaw_adjustment"),
# 			self.builder.get_object("yaw_meas_adjustment")
# 		], miro.constants.YAW_RAD_MIN, miro.constants.YAW_RAD_MAX)
# 		update_range([
# 			self.builder.get_object("pitch_adjustment"),
# 			self.builder.get_object("pitch_meas_adjustment")
# 		], miro.constants.PITCH_RAD_MIN, miro.constants.PITCH_RAD_MAX)

# 		#Connect signals to handle callbacks from event
# 		self.builder.connect_signals(self)

# 		#Get Windows from GUI
# 		self.MainWindow = self.builder.get_object("MainWindow")
# 		self.CamWindow = self.builder.get_object("CamWindow")
# 		self.MicWindow = self.builder.get_object("MicWindow")
# 		self.MicScrolledWindow = self.builder.get_object("MicScrolledWindow")

# 		#Get Cam and Mic Buttons from GUI
# 		self.DisplayCamButton = self.builder.get_object("DisplayCamButton")
# 		self.DisplayMicButton = self.builder.get_object("DisplayMicButton")

# 		#Get Battery objects from GUI
# 		self.BatteryText = self.builder.get_object("BatteryText")
# 		self.BatteryBar = self.builder.get_object("BatteryBar")
# 		self.BatteryBar.add_offset_value(Gtk.LEVEL_BAR_OFFSET_LOW, 4.6)
# 		self.BatteryBar.add_offset_value(Gtk.LEVEL_BAR_OFFSET_HIGH, 4.8)
# 		#self.BatteryBar.add_offset_value(Gtk.LEVEL_BAR_OFFSET_FULL, 5.0)

# 		#Get Sonar objects from GUI
# 		self.SonarText = self.builder.get_object("SonarText")
# 		self.SonarBar = self.builder.get_object("SonarBar")

# 		#Get Light objects from GUI
# 		self.gui_LightBarFL = self.builder.get_object("LightBarFL")
# 		self.gui_LightBarFR = self.builder.get_object("LightBarFR")
# 		self.gui_LightBarRL = self.builder.get_object("LightBarRL")
# 		self.gui_LightBarRR = self.builder.get_object("LightBarRR")

# 		#Get Touch objects from GUI
# 		self.BodyTouchText = self.builder.get_object("BodyTouchText")
# 		self.HeadTouchText = self.builder.get_object("HeadTouchText")
# 		self.BodyTouchBars = []
# 		self.HeadTouchBars = []
# 		for i in range(14):
# 			temp = self.builder.get_object("BT" + str(i))
# 			self.BodyTouchBars.append(temp)
# 			temp = self.builder.get_object("HT" + str(i))
# 			self.HeadTouchBars.append(temp)

# 		#Get Accelerometer objects from GUI
# 		self.gui_AccBarBX = self.builder.get_object("AccBarBX")
# 		self.gui_AccBarBY = self.builder.get_object("AccBarBY")
# 		self.gui_AccBarBZ = self.builder.get_object("AccBarBZ")
# 		self.gui_AccBarBL2 = self.builder.get_object("AccBarBL2")
# 		self.gui_AccBarHX = self.builder.get_object("AccBarHX")
# 		self.gui_AccBarHY = self.builder.get_object("AccBarHY")
# 		self.gui_AccBarHZ = self.builder.get_object("AccBarHZ")
# 		self.gui_AccBarHL2 = self.builder.get_object("AccBarHL2")

# 		#Get Cliff objects from GUI
# 		self.gui_CliffBarL = self.builder.get_object("CliffBarL")
# 		self.gui_CliffBarR = self.builder.get_object("CliffBarR")

# 		#Get Wheel Speed objects from GUI
# 		self.gui_WheelSpeedOptoL = self.builder.get_object("WheelSpeedOptoL")
# 		self.gui_WheelSpeedOptoR = self.builder.get_object("WheelSpeedOptoR")
# 		self.gui_WheelSpeedEMFL = self.builder.get_object("WheelSpeedEMFL")
# 		self.gui_WheelSpeedEMFR = self.builder.get_object("WheelSpeedEMFR")

# 		self.VelControl = self.builder.get_object("VelControl")
# 		self.AngVelControl = self.builder.get_object("AngVelControl")
# 		self.UserControlVel = self.builder.get_object("UserControlVelocity")

# 		self.YawControl = self.builder.get_object("YawControl")
# 		self.LiftControl = self.builder.get_object("LiftControl")
# 		self.PitchControl = self.builder.get_object("PitchControl")
# 		self.ResetKinButton = self.builder.get_object("ResetKinButton")
# 		self.UserControlKin = self.builder.get_object("UserControlKin")

# 		self.LeftEyeControl = self.builder.get_object("LeftEyeControl")
# 		self.RightEyeControl = self.builder.get_object("RightEyeControl")
# 		self.BlinkButton = self.builder.get_object("BlinkButton")
# 		self.WiggleButton = self.builder.get_object("WiggleButton")
# 		self.LeftEarControl = self.builder.get_object("LeftEarControl")
# 		self.RightEarControl = self.builder.get_object("RightEarControl")
# 		self.WagControl = self.builder.get_object("WagControl")
# 		self.DroopControl = self.builder.get_object("DroopControl")
# 		self.WagRateControl = self.builder.get_object("WagRateControl")
# 		self.CosResetButton = self.builder.get_object("CosResetButton")
# 		self.UserControlCos = self.builder.get_object("UserControlCos")

# 		self.VelMeasured = self.builder.get_object("VelMeasured")
# 		self.AngVelMeasured = self.builder.get_object("AngVelMeasured")

# 		self.LiftMeasured = self.builder.get_object("LiftMeasured")
# 		self.YawMeasured = self.builder.get_object("YawMeasured")
# 		self.PitchMeasured = self.builder.get_object("PitchMeasured")

# 		self.FreqControl = self.builder.get_object("FreqControl")
# 		self.VolControl = self.builder.get_object("VolControl")
# 		self.DurationControl = self.builder.get_object("DurationControl")
# 		self.Tone1Button = self.builder.get_object("Tone1Button")
# 		self.Tone2Button = self.builder.get_object("Tone2Button")
# 		self.Tone3Button = self.builder.get_object("Tone3Button")
# 		self.Tone4Button = self.builder.get_object("Tone4Button")
# 		self.SendToneButton = self.builder.get_object("SendToneButton")

# 		self.UserControlIllum = self.builder.get_object("UserControlIllum")
# 		self.gui_LEDBrightF = self.builder.get_object("LEDBrightF")
# 		self.gui_LEDBrightM = self.builder.get_object("LEDBrightM")
# 		self.gui_LEDBrightR = self.builder.get_object("LEDBrightR")
# 		self.gui_LEDColourF = self.builder.get_object("LEDColourF")
# 		self.gui_LEDColourM = self.builder.get_object("LEDColourM")
# 		self.gui_LEDColourR = self.builder.get_object("LEDColourR")

# 		self.gui_Camera = [
# 			self.builder.get_object("CameraLeft"),
# 			self.builder.get_object("CameraRight")
# 			]
# 		self.gui_ResolutionSelection = self.builder.get_object("ResolutionSelection")
# 		self.gui_CapResolutionSelection = self.builder.get_object("CapResolutionSelection")
# 		self.gui_CapFPSSelection = self.builder.get_object("CapFPSSelection")
# 		self.gui_MeasuredFPS = self.builder.get_object("MeasuredFPS")

# 		#Generate variables to store user input
# 		self.preset = False
# 		self.user_blink = 0
# 		self.user_waggle = 0
# 		self.user_wiggle = 0
# 		self.user_wag_rate = 0
# 		self.wag_phase = 0

# 		#Microphone Parameters
# 		# Number of points to display
# 		self.x_len = 40000
# 		# number of microphones coming through on topic
# 		self.no_of_mics = 4

# 		#Generate figure for plotting mics
# 		self.fig1 = plt.figure()
# 		self.fig1.suptitle("Microphones") # Give figure title

# 		#LEFT EAR
# 		self.left_ear_plot = self.fig1.add_subplot(4,1,1)
# 		self.left_ear_plot.set_ylim([-33000, 33000])
# 		self.left_ear_plot.set_xlim([0, self.x_len])
# 		self.left_ear_xs = np.arange(0, self.x_len)
# 		self.left_ear_plot.set_xticklabels([])
# 		self.left_ear_plot.set_yticks([])
# 		self.left_ear_plot.grid(which="both", axis="x")
# 		self.left_ear_plot.set_ylabel("Left Ear", rotation=0, ha="right")
# 		self.left_ear_ys = np.zeros(self.x_len)
# 		self.left_ear_line, = self.left_ear_plot.plot(self.left_ear_xs, self.left_ear_ys, linewidth=0.5, color="b")

# 		#RIGHT EAR
# 		self.right_ear_plot = self.fig1.add_subplot(4,1,2)
# 		self.right_ear_plot.set_ylim([-33000, 33000])
# 		self.right_ear_plot.set_xlim([0, self.x_len])
# 		self.right_ear_xs = np.arange(0, self.x_len)
# 		self.right_ear_plot.set_xticklabels([])
# 		self.right_ear_plot.set_yticks([])
# 		self.right_ear_plot.grid(which="both", axis="x")
# 		self.right_ear_plot.set_ylabel("Right Ear", rotation=0, ha="right")
# 		self.right_ear_ys = np.zeros(self.x_len)
# 		self.right_ear_line, = self.right_ear_plot.plot(self.right_ear_xs, self.right_ear_ys, linewidth=0.5, color="r")

# 		#HEAD
# 		self.head_plot = self.fig1.add_subplot(4,1,3)
# 		self.head_plot.set_ylim([-33000, 33000])
# 		self.head_plot.set_xlim([0, self.x_len])
# 		self.head_xs = np.arange(0, self.x_len)
# 		self.head_plot.set_xticklabels([])
# 		self.head_plot.set_yticks([])
# 		self.head_plot.grid(which="both", axis="x")
# 		self.head_plot.set_ylabel("Head", rotation=0, ha="right")
# 		self.head_ys = np.zeros(self.x_len)
# 		self.head_line, = self.head_plot.plot(self.head_xs, self.head_ys, linewidth=0.5, color="g")

# 		#Tail
# 		self.tail_plot = self.fig1.add_subplot(4,1,4)
# 		self.tail_plot.set_ylim([-33000, 33000])
# 		self.tail_plot.set_xlim([0, self.x_len])
# 		self.tail_xs = np.arange(0, self.x_len)
# 		self.tail_plot.set_yticks([])
# 		self.tail_plot.set_xlabel("Samples")
# 		self.tail_plot.grid(which="both", axis="x")
# 		self.tail_plot.set_ylabel("Tail", rotation=0, ha="right")
# 		self.tail_ys = np.zeros(self.x_len)
# 		self.tail_line, = self.tail_plot.plot(self.tail_xs, self.tail_ys, linewidth=0.5, color="c")

# 		self.canvas = FigureCanvas(self.fig1)
# 		self.ani = animation.FuncAnimation(self.fig1, self.update_line, fargs=(self.left_ear_ys,self.right_ear_ys, self.head_ys, self.tail_ys,), init_func=self.animation_init, interval=10, blit=False)
# 		self.fig1.subplots_adjust(hspace=0, wspace=0)
# 		self.MicScrolledWindow.add(self.canvas)

# 		# variables to store input data
# 		self.input_package = None
# 		self.input_camera = [None, None]
# 		self.t_input_camera = [[], []]
# 		self.input_mics = np.zeros((self.x_len, self.no_of_mics))

# 		#Create object to convert ROS images to OpenCV format
# 		self.image_converter = CvBridge()

# 		#Start timer to call function which updates GUI
# 		GLib.timeout_add(20, self.update_gui)
# 		GLib.timeout_add(20, self.update_images)

# 		#Create objects to hold published data
# 		self.velocity = TwistStamped()

# 		self.kin_joints = JointState()
# 		self.kin_joints.name = ["tilt", "lift", "yaw", "pitch"]
# 		self.kin_joints.position = [0.0, math.radians(34.0), 0.0, 0.0]

# 		self.cos_joints = Float32MultiArray()
# 		self.cos_joints.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# 		self.tone = UInt16MultiArray()
# 		self.tone.data = [0, 0, 0]

# 		self.illum = UInt32MultiArray()
# 		self.illum.data = [0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF]

# 		self.camera_zoom = None
# 		self.auto_camera_zoom = [0, 0] # determine zoom from first received frame
# 		self.frame_params = [180, '180w', 15]
# 		self.meas_fps = ["", ""]

# 		# set initial values
# 		self.on_ResetCosButton_clicked()
# 		self.adjustEyeInitialValues()
# 		self.on_LEDReset_clicked()

# 		# display GUI
# 		self.MainWindow.show_all()

# 		# robot name
# 		topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")
# 		print("subscribing to topics under", topic_base_name)

# 		# publishers
# 		self.pub_cmd_vel = rospy.Publisher(topic_base_name + "/control/cmd_vel", TwistStamped, queue_size=0)
# 		self.pub_cos = rospy.Publisher(topic_base_name + "/control/cosmetic_joints", Float32MultiArray, queue_size=0)
# 		self.pub_illum = rospy.Publisher(topic_base_name + "/control/illum", UInt32MultiArray, queue_size=0)
# 		self.pub_kin = rospy.Publisher(topic_base_name + "/control/kinematic_joints", JointState, queue_size=0)
# 		self.pub_tone = rospy.Publisher(topic_base_name + "/control/tone", UInt16MultiArray, queue_size=0)
# 		self.pub_command = rospy.Publisher(topic_base_name + "/control/command", String, queue_size=0)

# 		# subscribers
# 		self.sub_package = rospy.Subscriber(topic_base_name + "/sensors/package",
# 					miro.msg.sensors_package, self.callback_package, queue_size=1, tcp_nodelay=True)
# 		self.sub_mics = rospy.Subscriber(topic_base_name + "/sensors/mics",
# 					Int16MultiArray, self.callback_mics, queue_size=1, tcp_nodelay=True)
# 		self.sub_caml = rospy.Subscriber(topic_base_name + "/sensors/caml/compressed",
# 					CompressedImage, self.callback_caml, queue_size=1, tcp_nodelay=True)
# 		self.sub_camr = rospy.Subscriber(topic_base_name + "/sensors/camr/compressed",
# 					CompressedImage, self.callback_camr, queue_size=1, tcp_nodelay=True)

# 	#Handle Closure of Main Window
# 	def on_MainWindow_destroy(self, *args):
# 		print("GUI closed due to user quit")
# 		Gtk.main_quit()

# 	def on_DisplayCamButton_toggled(self, *args):
# 		if self.DisplayCamButton.get_active():
# 			self.CamWindow.show_all()
# 			print("Displaying Cameras")
# 			self.on_ResolutionSelection_changed()
# 			self.on_CapResolutionSelection_changed()
# 		else:
# 			self.CamWindow.hide()
# 			print("Stop Displaying Cameras")

# 	#Handle Closure of Camera Window to prevent destruction
# 	def on_CamWindow_delete_event(self, *args):
# 		self.CamWindow.hide()
# 		self.DisplayCamButton.set_active(False)
# 		print("Camera window closed due to user quit")
# 		return True #This prevents call of destroy function

# 	def on_DisplayMicButton_toggled(self, *args):
# 		if self.DisplayMicButton.get_active():
# 			self.MicWindow.show_all()
# 			print("Displaying Microphones")
# 		else:
# 			self.MicWindow.hide()
# 			print("Stop Displaying Microphones")

# 	#Handle Closure of Mic Window to prevent destruction
# 	def on_MicWindow_delete_event(self, *args):
# 		self.MicWindow.hide()
# 		self.DisplayMicButton.set_active(False)
# 		print("Microphone window closed due to user quit")
# 		return True #This prevents call of destroy function

# ################################################# VELOCITY CONTROL ###########################################################

# 	def on_VelControl_change_value(self, *args):
# 		self.velocity.twist.linear.x = self.VelControl.get_value()

# 	def on_AngVelControl_change_value(self, *args):
# 		self.velocity.twist.angular.z = self.AngVelControl.get_value()

# 	def on_ResetBodyVel_clicked(self, *args):
# 		self.VelControl.set_value(0.0)
# 		self.velocity.twist.linear.x = self.VelControl.get_value()
# 		self.AngVelControl.set_value(0.0)
# 		self.velocity.twist.angular.z = self.AngVelControl.get_value()

# ############################################### KINEMATICS CONTROL ###########################################################

# 	def on_ResetKinButton_clicked(self, *args):
# 		self.LiftControl.set_value(34.0)
# 		self.YawControl.set_value(0.0)
# 		self.PitchControl.set_value(0.0)
# 		self.kin_joints.position[lift] = math.radians(self.LiftControl.get_value())
# 		self.kin_joints.position[pitch] = math.radians(self.PitchControl.get_value())
# 		self.kin_joints.position[yaw] = math.radians(self.YawControl.get_value())

# 	def on_LiftControl_change_value(self, *args):
# 		self.kin_joints.position[lift] = math.radians(self.LiftControl.get_value())

# 	def on_PitchControl_change_value(self, *args):
# 		self.kin_joints.position[pitch] = math.radians(self.PitchControl.get_value())

# 	def on_YawControl_change_value(self, *args):
# 		self.kin_joints.position[yaw] = math.radians(self.YawControl.get_value())

# ############################################### COSMETICS CONTROL ###########################################################

# 	def adjustEyeInitialValues(self):

# 		# the calibration values for the eyelids are half-closed
# 		# but it's annoying to have the GUI default to this because
# 		# then the cameras are half-obscured so for the eyes only
# 		# we don't start at the calibration point
# 		self.LeftEyeControl.set_value(0.0)
# 		self.RightEyeControl.set_value(0.0)

# 	def on_ResetCosButton_clicked(self, *args):
# 		self.LeftEyeControl.set_value(miro.constants.EYE_CALIB)
# 		self.RightEyeControl.set_value(miro.constants.EYE_CALIB)
# 		self.LeftEarControl.set_value(miro.constants.EAR_CALIB)
# 		self.RightEarControl.set_value(miro.constants.EAR_CALIB)
# 		self.WagControl.set_value(miro.constants.WAG_CALIB)
# 		self.DroopControl.set_value(miro.constants.DROOP_CALIB)
# 		self.WagRateControl.set_value(31.0)
# 		self.cos_joints.data[droop] = self.DroopControl.get_value()
# 		self.cos_joints.data[wag] = self.WagControl.get_value()
# 		self.cos_joints.data[left_eye] = self.LeftEyeControl.get_value()
# 		self.cos_joints.data[right_eye] = self.RightEyeControl.get_value()
# 		self.cos_joints.data[left_ear] = self.LeftEarControl.get_value()
# 		self.cos_joints.data[right_ear] = self.RightEarControl.get_value()
# 		self.user_wag_rate = 0

# ######## EYES ########

# 	def on_LeftEyeControl_change_value(self, *args):
# 		self.cos_joints.data[left_eye] = self.LeftEyeControl.get_value()

# 	def on_RightEyeControl_change_value(self, *args):
# 		self.cos_joints.data[right_eye] = self.RightEyeControl.get_value()

# 	def on_BlinkButton_clicked(self, *args):
# 		if self.UserControlCos.get_active():
# 			self.user_blink = 1

# 	def on_WaggleButton_clicked(self, *args):
# 		if self.UserControlCos.get_active():
# 			self.user_waggle = 1

# 	def on_WiggleButton_clicked(self, *args):
# 		if self.UserControlCos.get_active():
# 			self.user_wiggle = 1

# ######## Tail ########

# 	def on_WagControl_change_value(self, *args):
# 		self.cos_joints.data[wag] = self.WagControl.get_value()

# 	def on_DroopControl_change_value(self, *args):
# 		self.cos_joints.data[droop] = self.DroopControl.get_value()

# 	def on_WagRateControl_change_value(self, *args):
# 		wag_rate = self.WagRateControl.get_value()
# 		if wag_rate == 31:
# 			self.user_wag_rate = 0
# 		else:
# 			self.user_wag_rate = wag_rate


# ######## EARS #########

# 	def on_LeftEarControl_change_value(self, *args):
# 		self.cos_joints.data[left_ear] = self.LeftEarControl.get_value()

# 	def on_RightEarControl_change_value(self, *args):
# 		self.cos_joints.data[right_ear] = self.RightEarControl.get_value()

# ##################################### Measured Velocities + Angles ##########################################################

# 	#Returning true from change_value prevents user from altering slider value
# 	def on_VelMeasured_change_value(self, *args):
# 		return True

# 	def on_AngVelMeasured_change_value(self, *args):
# 		return True

# 	def on_LiftMeasured_change_value(self, *args):
# 		return True

# 	def on_YawMeasured_change_value(self, *args):
# 		return True

# 	def on_PitchMeasured_change_value(self, *args):
# 		return True

# 	def on_SonarBar_change_value(self, *args):
# 		return True

# ################################### TONE GENERATOR ##########################################################################

# 	def on_SendToneButton_clicked(self, *args):
# 		self.tone.data[freq] = int(self.FreqControl.get_value())
# 		self.tone.data[volume] = int(self.VolControl.get_value())
# 		self.tone.data[duration] = int(self.DurationControl.get_value())
# 		self.pub_tone.publish(self.tone)

# 	def on_Tone1Button_clicked(self, *args):
# 		self.tone.data[freq] = 1
# 		self.tone.data[volume] = int(self.VolControl.get_value())
# 		self.tone.data[duration] = 1
# 		self.pub_tone.publish(self.tone)

# 	def on_Tone2Button_clicked(self, *args):
# 		self.tone.data[freq] = 2
# 		self.tone.data[volume] = int(self.VolControl.get_value())
# 		self.tone.data[duration] = 1
# 		self.pub_tone.publish(self.tone)

# 	def on_Tone3Button_clicked(self, *args):
# 		self.tone.data[freq] = 3
# 		self.tone.data[volume] = int(self.VolControl.get_value())
# 		self.tone.data[duration] = 1
# 		self.pub_tone.publish(self.tone)


# ##################################### LED PATTERN GENERATOR #################################################################

# 	def on_LEDChange(self, *args):

# 		value = generate_illum(
# 					self.gui_LEDColourF.get_rgba(),
# 					self.gui_LEDBrightF.get_value()
# 					)
# 		self.illum.data[front_left] = value
# 		self.illum.data[front_right] = value
# 		value = generate_illum(
# 					self.gui_LEDColourM.get_rgba(),
# 					self.gui_LEDBrightM.get_value()
# 					)
# 		self.illum.data[mid_left] = value
# 		self.illum.data[mid_right] = value
# 		value = generate_illum(
# 					self.gui_LEDColourR.get_rgba(),
# 					self.gui_LEDBrightR.get_value()
# 					)
# 		self.illum.data[rear_left] = value
# 		self.illum.data[rear_right] = value

# 	def LEDSetAll(self, color, bright):

# 		self.gui_LEDColourF.set_rgba(color)
# 		self.gui_LEDBrightF.set_value(bright)
# 		self.gui_LEDColourM.set_rgba(color)
# 		self.gui_LEDBrightM.set_value(bright)
# 		self.gui_LEDColourR.set_rgba(color)
# 		self.gui_LEDBrightR.set_value(bright)
# 		self.on_LEDChange()

# 	def on_LEDReset_clicked(self, *args):

# 		color = Gdk.RGBA(1.0, 1.0, 1.0, 1.0)
# 		bright = 0
# 		self.LEDSetAll(color, 0)

# 	def on_LEDPreset1_clicked(self, *args):

# 		color = Gdk.RGBA(1.0, 1.0, 1.0, 1.0)
# 		bright = 63
# 		self.LEDSetAll(color, 63)

# 	def on_LEDPreset2_clicked(self, *args):

# 		bright = 63
# 		self.gui_LEDColourF.set_rgba(Gdk.RGBA(1.0, 0.0, 0.0, 1.0))
# 		self.gui_LEDBrightF.set_value(bright)
# 		self.gui_LEDColourM.set_rgba(Gdk.RGBA(0.0, 1.0, 0.0, 1.0))
# 		self.gui_LEDBrightM.set_value(bright)
# 		self.gui_LEDColourR.set_rgba(Gdk.RGBA(0.0, 0.0, 1.0, 1.0))
# 		self.gui_LEDBrightR.set_value(bright)
# 		self.on_LEDChange()

# 	def on_LEDPreset3_clicked(self, *args):
# 		print ("Preset 3")
#  #############################################################################################################################

# 	def on_ButtonJpegLo_clicked(self, *args):
# 		cmd = "jpeg=10"
# 		self.pub_command.publish(cmd)

# 	def on_ButtonJpegMed_clicked(self, *args):
# 		cmd = "jpeg=60"
# 		self.pub_command.publish(cmd)

# 	def on_ButtonJpegHi_clicked(self, *args):
# 		cmd = "jpeg=80"
# 		self.pub_command.publish(cmd)

# 	def on_ResolutionSelection_changed(self, *args):
# 		self.camera_zoom = self.gui_ResolutionSelection.get_active_text()

# 	def parse_resolution(self, res_string):
# 		width_string, height_string = res_string.split("x", 1)
# 		width = int(width_string)
# 		height = int(height_string)
# 		return width, height

# 	def on_SendCamParamsButton_clicked(self, *args):
# 		cmd = "frame=" + self.frame_params[1] + "@" + str(self.frame_params[2])
# 		self.pub_command.publish(cmd)

# 		# set camera zoom to auto so it sets automatically when next frame arrives
# 		self.auto_camera_zoom = [self.frame_params[0], time.time()]

# 	def on_CapResolutionSelection_changed(self, *args):

# 		res_text = self.gui_CapResolutionSelection.get_active_text()
# 		cap_resolution_w, cap_resolution_h = self.parse_resolution(res_text)
# 		self.frame_params[0] = cap_resolution_h

# 		# convert to bridge format
# 		if (cap_resolution_w * 3) / 4 == cap_resolution_h:
# 			cap_resolution = str(cap_resolution_h) + "s"
# 		else:
# 			cap_resolution = str(cap_resolution_h) + "w"
# 		self.frame_params[1] = cap_resolution

# 	def on_CapFPSSelection_change_value(self, *args):
# 		self.frame_params[2] = int(self.gui_CapFPSSelection.get_value())

# ################################################################
# ## ROS CALLBACKS

# 	def callback_package(self, msg):

# 		# store for processing in update_gui
# 		self.input_package = msg

# 	def callback_mics(self, data):

# 		# discard data if GUI not displayed
# 		if not self.DisplayMicButton.get_active():
# 			return

# 		# save microphone data to rolling buffer for later processing
# 		# reshape into 4 x 500 array
# 		data = np.asarray(data.data)
# 		data = np.transpose(data.reshape((self.no_of_mics, 500)))
# 		data = np.flipud(data)
# 		# array is [ L, R, H, B] mics
# 		# add to top of buffer
# 		self.input_mics = np.vstack((data, self.input_mics[:self.x_len-500,:]))

# 	def do_auto_camera_zoom(self, image_height):

# 		if image_height <= 240:
# 			self.gui_ResolutionSelection.set_active(2)
# 		elif image_height > 600:
# 			self.gui_ResolutionSelection.set_active(0)
# 		else:
# 			self.gui_ResolutionSelection.set_active(1)
# 		self.on_ResolutionSelection_changed()

# 	def do_auto_camera_res(self, shape):

# 		l = ['240x176', '320x176', '320x240', '480x360', '640x360', '960x720', '1280x720']
# 		s = str(shape[1]) + "x" + str(shape[0])
# 		for i in range(len(l)):
# 			if s == l[i]:
# 				print("detected camera resolution", s)
# 				self.gui_CapResolutionSelection.set_active(i)
# 				return

# 	def callback_cam(self, ros_image, index):

# 		# discard data if GUI not displayed
# 		if not self.CamWindow.get_property("visible"):
# 			self.t_input_camera = [[], []]
# 			return
			
# 		# ignore empty frames which occur sometimes during parameter changes
# 		if len(ros_image.data) == 0:
# 			print("dropped empty camera frame")
# 			return

# 		# silently (ish) handle corrupted JPEG frames
# 		try:

# 			# convert compressed ROS image to raw CV image
# 			image = self.image_converter.compressed_imgmsg_to_cv2(ros_image, "rgb8")

# 			# set camera zoom automatically if has not been set already
# 			if not self.auto_camera_zoom is None:
# 				h = self.auto_camera_zoom[0]
# 				dt = time.time() - self.auto_camera_zoom[1]
# 				if h == 0:
# 					# initial state, set from first received frame regardless
# 					self.do_auto_camera_zoom(image.shape[0])
# 					self.auto_camera_zoom = None
# 					# for initial frame, also set resolution selector
# 					self.do_auto_camera_res(image.shape)
# 				elif dt > 4.0:
# 					self.auto_camera_zoom = None
# 				elif abs(image.shape[0] - h) < 32:
# 					self.do_auto_camera_zoom(h)
# 					self.auto_camera_zoom = None

# 			# do zoom
# 			if self.camera_zoom == "0.5x":
# 				image = cv2.resize(image, (int(image.shape[1] * 0.5), int(image.shape[0] * 0.5)))
# 			elif self.camera_zoom == "2x":
# 				image = cv2.resize(image, (int(image.shape[1] * 2.0), int(image.shape[0] * 2.0)))

# 			# store image for display
# 			self.input_camera[index] = image

# 		except CvBridgeError as e:

# 			# swallow error, silently
# 			#print(e)
# 			pass

# 	def callback_caml(self, ros_image):

# 		self.callback_cam(ros_image, 0)

# 	def callback_camr(self, ros_image):

# 		self.callback_cam(ros_image, 1)

# ################################################################
# ## GUI UPDATES

# 	def update_line(self, i, left_ear_ys, right_ear_ys, head_ys, tail_ys):
# 		if self.DisplayMicButton.get_active():
# 			#Flip buffer so that incoming data moves in from the right
# 			left_ear_data = np.flipud(self.input_mics[:, 0])
# 			right_ear_data = np.flipud(self.input_mics[:, 1])
# 			head_data = np.flipud(self.input_mics[:, 2])
# 			tail_data = np.flipud(self.input_mics[:, 3])

# 			#Append new buffer data to plotting data
# 			left_ear_ys = np.append(left_ear_ys, left_ear_data)
# 			right_ear_ys = np.append(right_ear_ys, right_ear_data)
# 			head_ys = np.append(head_ys, head_data)
# 			tail_ys = np.append(tail_ys, tail_data)

# 			#Remove old sample outside of plot
# 			left_ear_ys = left_ear_ys[-self.x_len:]
# 			right_ear_ys = right_ear_ys[-self.x_len:]
# 			head_ys = head_ys[-self.x_len:]
# 			tail_ys = tail_ys[-self.x_len:]

# 			#Set data to line
# 			self.left_ear_line.set_ydata(left_ear_ys)
# 			self.right_ear_line.set_ydata(right_ear_ys)
# 			self.head_line.set_ydata(head_ys)
# 			self.tail_line.set_ydata(tail_ys)

# 		#Return the line to be animated
# 		return self.left_ear_line, self.right_ear_line, self.head_line, self.tail_line,

# 	def animation_init(self):
# 		self.left_ear_line.set_ydata(np.zeros(self.x_len))
# 		self.right_ear_line.set_ydata(np.zeros(self.x_len))
# 		self.head_line.set_ydata(np.zeros(self.x_len))
# 		self.tail_line.set_ydata(np.zeros(self.x_len))
# 		return self.left_ear_line, self.right_ear_line, self.head_line, self.tail_line,

# 	def update_images(self):

# 		# skip if GUI not open
# 		if not self.CamWindow.get_property("visible"):
# 			return True

# 		# for each camera
# 		for i in range(2):

# 			# get image
# 			image = self.input_camera[i]
# 			self.input_camera[i] = None
# 			if image is None:
# 				continue

# 			# do fps
# 			t = time.time()
# 			tt = self.t_input_camera[i]
# 			tt.append(t)
# 			n_meas = 15
# 			tt = tt[-(n_meas+1):]
# 			if len(tt) == (n_meas+1):
# 				dt = (tt[n_meas] - tt[0]) / float(n_meas)
# 				fps = format_num(1.0 / dt, 1)
# 			else:
# 				fps = "???"
# 			self.meas_fps[i] = fps

# 			# write in cross-hairs
# 			h = image.shape[0]
# 			w = image.shape[1]
# 			# https://www.python.org/dev/peps/pep-0238/
# 			h2 = h // 2
# 			w2 = w // 2
# 			cv2.line(image, (0, h2), (w, h2), (255, 0, 255), 1)
# 			cv2.line(image, (0, h2), (w, h2), (255, 0, 255), 1)
# 			cv2.line(image, (w2, 0), (w2, h), (255, 0, 255), 1)
# 			cv2.line(image, (w2-1, 0), (w2-1, h), (255, 0, 255), 1)

# 			# write in nominal "dead ahead" point (see dev/camera_model/190724/horiz_map)
# 			x = w * 0.75
# 			if i == 1:
# 				x = w * 0.25
# 			x = int(x)
# 			cv2.line(image, (x, int(h*0.45)), (x, int(h*0.55)), (255, 0, 255), 1)

# 			# update displayed image
# 			pb = GdkPixbuf.Pixbuf.new_from_data(image.tostring(),
# 						GdkPixbuf.Colorspace.RGB, False, 8,
# 						image.shape[1], image.shape[0],
# 						image.shape[2]*image.shape[1]
# 						)
# 			self.gui_Camera[i].set_from_pixbuf(pb.copy())

# 		fpss = self.meas_fps[0] + " / " + self.meas_fps[1]
# 		if self.gui_MeasuredFPS.get_text() != fpss:
# 			self.gui_MeasuredFPS.set_text(fpss)

# 		return True

# 	def update_gui(self):

# 		self.step += 1
# 		step_ = self.step % 100

# 		if not self.input_package is None:

# 			# acquire
# 			p = self.input_package
# 			self.input_package = None

# 			# update battery
# 			x = p.battery.voltage
# 			self.BatteryBar.set_value(x)
# 			self.BatteryText.set_text(format_num(x) + "V")

# 			# update sonar
# 			x = p.sonar.range
# 			self.SonarBar.set_value(x)
# 			if x == 0:
# 				self.SonarText.set_text("short")
# 			elif x > 1.0:
# 				self.SonarText.set_text("inf")
# 			else:
# 				self.SonarText.set_text(format_num(x) + "m")

# 			# update light
# 			x = p.light.data
# 			self.gui_LightBarFL.set_value(x[0] * 100)
# 			self.gui_LightBarFR.set_value(x[1] * 100)
# 			self.gui_LightBarRL.set_value(x[2] * 100)
# 			self.gui_LightBarRR.set_value(x[3] * 100)

# 			# update body touch
# 			x = p.touch_body.data
# 			self.BodyTouchText.set_text("{0:014b}".format(x))
# 			for i in range(14):
# 				self.BodyTouchBars[i].set_value(x & (1 << i))

# 			# update head touch
# 			x = p.touch_head.data
# 			self.HeadTouchText.set_text("{0:014b}".format(x))
# 			hts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# 			# raw order if not re-ordered in firmware...
# 			#order = [8, 7, 0, 1, 4, 3, 6, 5, 2, 9, 12, 13, 10, 11]
# 			# but, now re-ordered in firmware...
# 			order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
# 			# hint: body touch are ordered correctly just by wiring
# 			for i in range(14):
# 				hts[order[i]] = x & (1 << i)
# 			for i in range(14):
# 				self.HeadTouchBars[i].set_value(hts[i])

# 			# update body imu
# 			x = p.imu_body.linear_acceleration
# 			#self.BodyIMUTextX.set_text(format_num(x.x))
# 			#self.BodyIMUTextY.set_text(format_num(x.y))
# 			#self.BodyIMUTextZ.set_text(format_num(x.z))
# 			self.gui_AccBarBX.set_value(x.x / 9.81 * 50.0)
# 			self.gui_AccBarBY.set_value(x.y / 9.81 * 50.0)
# 			self.gui_AccBarBZ.set_value(x.z / 9.81 * 50.0)
# 			l = np.sqrt(x.x*x.x + x.y*x.y + x.z*x.z)
# 			self.gui_AccBarBL2.set_value(l / 9.81 * 50.0)

# 			# update head imu
# 			x = p.imu_head.linear_acceleration
# 			#self.HeadIMUTextX.set_text(format_num(x.x))
# 			#self.HeadIMUTextY.set_text(format_num(x.y))
# 			#self.HeadIMUTextZ.set_text(format_num(x.z))
# 			self.gui_AccBarHX.set_value(x.x / 9.81 * 50.0)
# 			self.gui_AccBarHY.set_value(x.y / 9.81 * 50.0)
# 			self.gui_AccBarHZ.set_value(x.z / 9.81 * 50.0)
# 			l = np.sqrt(x.x*x.x + x.y*x.y + x.z*x.z)
# 			self.gui_AccBarHL2.set_value(l / 9.81 * 50.0)

# 			# update cliff
# 			x = (np.array([p.cliff.data[0], p.cliff.data[1]]) * 15).astype('int')
# 			#self.CliffLeftText.set_text(str(x[0]))
# 			#self.CliffRightText.set_text(str(x[1]))
# 			self.gui_CliffBarL.set_value(x[0])
# 			self.gui_CliffBarR.set_value(x[1])

# 			# update odom
# 			x = p.odom.twist.twist
# 			self.VelMeasured.set_value(x.linear.x)
# 			self.AngVelMeasured.set_value(x.angular.z)

# 			# update wheel speed (gui elements read in mm/s)
# 			x = p.wheel_speed_opto.data
# 			self.gui_WheelSpeedOptoL.set_value(x[0] * 1000)
# 			self.gui_WheelSpeedOptoR.set_value(x[1] * 1000)
# 			x = p.wheel_speed_back_emf.data
# 			self.gui_WheelSpeedEMFL.set_value(x[0] * 1000)
# 			self.gui_WheelSpeedEMFR.set_value(x[1] * 1000)

# 			# update kinematic joints
# 			x = p.kinematic_joints.position
# 			self.LiftMeasured.set_value(math.degrees(x[1]))
# 			self.YawMeasured.set_value(math.degrees(x[2]))
# 			self.PitchMeasured.set_value(math.degrees(x[3]))

# 		# if user is controlling illumination
# 		if self.UserControlIllum.get_active():
# 			self.pub_illum.publish(self.illum)

# 		# if user is controlling velocity
# 		if self.UserControlVel.get_active():
# 			self.pub_cmd_vel.publish(self.velocity)

# 		# if user is controlling kinematics
# 		if self.UserControlKin.get_active():
# 			self.pub_kin.publish(self.kin_joints)

# 		# if user is controlling cosmetics
# 		if self.UserControlCos.get_active():

# 			wiggle_n = 20

# 			if self.user_blink > 0:

# 				self.cos_joints.data[left_eye] = wiggle(0.0, self.user_blink, wiggle_n)
# 				self.cos_joints.data[right_eye] = wiggle(0.0, self.user_blink, wiggle_n)

# 				# follow
# 				self.LeftEyeControl.set_value(self.cos_joints.data[left_eye])
# 				self.RightEyeControl.set_value(self.cos_joints.data[right_eye])

# 				self.user_blink += 1
# 				if self.user_blink > (2 * wiggle_n):
# 					self.user_blink = 0

# 			if self.user_wag_rate > 0 or self.wag_phase > 0:

# 				if self.user_wag_rate > 0:
# 					self.wag_phase += np.pi / self.user_wag_rate
# 				else:
# 					self.wag_phase = 0

# 				if self.wag_phase >= 2 * np.pi:
# 					self.wag_phase -= 2 * np.pi

# 				self.cos_joints.data[droop] = 0.0
# 				self.cos_joints.data[wag] = np.sin(self.wag_phase) * 0.5 + 0.5

# 				# follow
# 				self.WagControl.set_value(self.cos_joints.data[wag])
# 				self.DroopControl.set_value(self.cos_joints.data[droop])

# 				# clear any pending waggle so it doesn't execute when wag stops
# 				self.user_waggle = 0

# 			elif self.user_waggle > 0:

# 				if self.user_waggle <= (2 * wiggle_n):
# 					self.cos_joints.data[wag] = wiggle(0.5, self.user_waggle, wiggle_n)
# 					self.cos_joints.data[droop] = 0.0
# 				else:
# 					self.cos_joints.data[wag] = 0.5
# 					self.cos_joints.data[droop] = wiggle(0.0, self.user_waggle - (2*wiggle_n), wiggle_n)

# 				# follow
# 				self.WagControl.set_value(self.cos_joints.data[wag])
# 				self.DroopControl.set_value(self.cos_joints.data[droop])

# 				self.user_waggle += 1
# 				if self.user_waggle > (4 * wiggle_n):
# 					self.user_waggle = 0

# 			if self.user_wiggle > 0:

# 				self.cos_joints.data[left_ear] = wiggle(0.3333, self.user_wiggle, wiggle_n)
# 				self.cos_joints.data[right_ear] = wiggle(0.3333, self.user_wiggle, wiggle_n)

# 				# follow
# 				self.LeftEarControl.set_value(self.cos_joints.data[left_ear])
# 				self.RightEarControl.set_value(self.cos_joints.data[right_ear])

# 				self.user_wiggle += 1
# 				if self.user_wiggle > (2 * wiggle_n):
# 					self.user_wiggle = 0

# 			self.pub_cos.publish(self.cos_joints)

# 		return True

# ################################################################
# ## MAIN

# if __name__ == "__main__":
# 	main = miro_gui()
# 	rospy.init_node("client_gui")
# 	Gtk.main()


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

import time
import gi
import os

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GdkPixbuf, Gdk, GLib

import rospy
from std_msgs.msg import Float32MultiArray, UInt32MultiArray, UInt16MultiArray, UInt8MultiArray, UInt16, Int16MultiArray, String
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import JointState, CompressedImage

import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

import math
import miro2 as miro



from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def format_num(n, d=2):
	s = ("{:." + str(d) + "f}").format(n)
	if n >= 0:
		s = " " + s;
	return s

def wiggle(v, n, m):
	v = v + float(n) / float(m)
	if v > 2.0:
		v -= 2.0
	elif v > 1.0:
		v = 2.0 - v
	return v

def generate_illum(colour, bright):

	rgb_str = colour.to_string()
	useless, rgb_values = rgb_str.split("(")
	rgb_values, useless = rgb_values.split(")")
	r, g, b = rgb_values.split(",")
	r = int(r)
	g = int(g)
	b = int(b)
	return (int(bright) << 24) | (r << 16) | (g << 8) | b

def update_range(objs, lo, hi):
	for obj in objs:
		obj.set_lower(np.degrees(lo))
		obj.set_upper(np.degrees(hi))


#Generate a fake enum for joint arrays
tilt, lift, yaw, pitch = range(4)
droop, wag, left_eye, right_eye, left_ear, right_ear = range(6)
freq, volume, duration = range(3)
front_left, mid_left, rear_left, front_right, mid_right, rear_right = range(6)
closing = True
opening = False
right = True
left = False

class miro_gui:

	def __init__(self):

		# state
		self.step = 0

		#Load GUI from glade file
		self.builder = Gtk.Builder()
		self.builder.add_from_file("client_gui.glade")

		# update constants in builder
		update_range([
			self.builder.get_object("lift_adjustment"),
			self.builder.get_object("lift_meas_adjustment")
		], miro.constants.LIFT_RAD_MIN, miro.constants.LIFT_RAD_MAX)
		update_range([
			self.builder.get_object("yaw_adjustment"),
			self.builder.get_object("yaw_meas_adjustment")
		], miro.constants.YAW_RAD_MIN, miro.constants.YAW_RAD_MAX)
		update_range([
			self.builder.get_object("pitch_adjustment"),
			self.builder.get_object("pitch_meas_adjustment")
		], miro.constants.PITCH_RAD_MIN, miro.constants.PITCH_RAD_MAX)

		#Connect signals to handle callbacks from event
		self.builder.connect_signals(self)

		#Get Windows from GUI
		self.MainWindow = self.builder.get_object("MainWindow")
		self.CamWindow = self.builder.get_object("CamWindow")
		self.MicWindow = self.builder.get_object("MicWindow")
		self.MicScrolledWindow = self.builder.get_object("MicScrolledWindow")

		#Get Cam and Mic Buttons from GUI
		self.DisplayCamButton = self.builder.get_object("DisplayCamButton")
		self.DisplayMicButton = self.builder.get_object("DisplayMicButton")

		#Get Battery objects from GUI
		self.BatteryText = self.builder.get_object("BatteryText")
		self.BatteryBar = self.builder.get_object("BatteryBar")
		self.BatteryBar.add_offset_value(Gtk.LEVEL_BAR_OFFSET_LOW, 4.6)
		self.BatteryBar.add_offset_value(Gtk.LEVEL_BAR_OFFSET_HIGH, 4.8)
		#self.BatteryBar.add_offset_value(Gtk.LEVEL_BAR_OFFSET_FULL, 5.0)

		#Get Sonar objects from GUI
		self.SonarText = self.builder.get_object("SonarText")
		self.SonarBar = self.builder.get_object("SonarBar")

		#Get Light objects from GUI
		self.gui_LightBarFL = self.builder.get_object("LightBarFL")
		self.gui_LightBarFR = self.builder.get_object("LightBarFR")
		self.gui_LightBarRL = self.builder.get_object("LightBarRL")
		self.gui_LightBarRR = self.builder.get_object("LightBarRR")

		#Get Touch objects from GUI
		self.BodyTouchText = self.builder.get_object("BodyTouchText")
		self.HeadTouchText = self.builder.get_object("HeadTouchText")
		self.BodyTouchBars = []
		self.HeadTouchBars = []
		for i in range(14):
			temp = self.builder.get_object("BT" + str(i))
			self.BodyTouchBars.append(temp)
			temp = self.builder.get_object("HT" + str(i))
			self.HeadTouchBars.append(temp)

		#Get Accelerometer objects from GUI
		self.gui_AccBarBX = self.builder.get_object("AccBarBX")
		self.gui_AccBarBY = self.builder.get_object("AccBarBY")
		self.gui_AccBarBZ = self.builder.get_object("AccBarBZ")
		self.gui_AccBarBL2 = self.builder.get_object("AccBarBL2")
		self.gui_AccBarHX = self.builder.get_object("AccBarHX")
		self.gui_AccBarHY = self.builder.get_object("AccBarHY")
		self.gui_AccBarHZ = self.builder.get_object("AccBarHZ")
		self.gui_AccBarHL2 = self.builder.get_object("AccBarHL2")

		#Get Cliff objects from GUI
		self.gui_CliffBarL = self.builder.get_object("CliffBarL")
		self.gui_CliffBarR = self.builder.get_object("CliffBarR")

		#Get Wheel Speed objects from GUI
		self.gui_WheelSpeedOptoL = self.builder.get_object("WheelSpeedOptoL")
		self.gui_WheelSpeedOptoR = self.builder.get_object("WheelSpeedOptoR")
		self.gui_WheelSpeedEMFL = self.builder.get_object("WheelSpeedEMFL")
		self.gui_WheelSpeedEMFR = self.builder.get_object("WheelSpeedEMFR")

		self.VelControl = self.builder.get_object("VelControl")
		self.AngVelControl = self.builder.get_object("AngVelControl")
		self.UserControlVel = self.builder.get_object("UserControlVelocity")

		self.YawControl = self.builder.get_object("YawControl")
		self.LiftControl = self.builder.get_object("LiftControl")
		self.PitchControl = self.builder.get_object("PitchControl")
		self.ResetKinButton = self.builder.get_object("ResetKinButton")
		self.UserControlKin = self.builder.get_object("UserControlKin")

		self.LeftEyeControl = self.builder.get_object("LeftEyeControl")
		self.RightEyeControl = self.builder.get_object("RightEyeControl")
		self.BlinkButton = self.builder.get_object("BlinkButton")
		self.WiggleButton = self.builder.get_object("WiggleButton")
		self.LeftEarControl = self.builder.get_object("LeftEarControl")
		self.RightEarControl = self.builder.get_object("RightEarControl")
		self.WagControl = self.builder.get_object("WagControl")
		self.DroopControl = self.builder.get_object("DroopControl")
		self.WagRateControl = self.builder.get_object("WagRateControl")
		self.CosResetButton = self.builder.get_object("CosResetButton")
		self.UserControlCos = self.builder.get_object("UserControlCos")

		self.VelMeasured = self.builder.get_object("VelMeasured")
		self.AngVelMeasured = self.builder.get_object("AngVelMeasured")

		self.LiftMeasured = self.builder.get_object("LiftMeasured")
		self.YawMeasured = self.builder.get_object("YawMeasured")
		self.PitchMeasured = self.builder.get_object("PitchMeasured")

		self.FreqControl = self.builder.get_object("FreqControl")
		self.VolControl = self.builder.get_object("VolControl")
		self.DurationControl = self.builder.get_object("DurationControl")
		self.Tone1Button = self.builder.get_object("Tone1Button")
		self.Tone2Button = self.builder.get_object("Tone2Button")
		self.Tone3Button = self.builder.get_object("Tone3Button")
		self.Tone4Button = self.builder.get_object("Tone4Button")
		self.SendToneButton = self.builder.get_object("SendToneButton")

		self.UserControlIllum = self.builder.get_object("UserControlIllum")
		self.gui_LEDBrightF = self.builder.get_object("LEDBrightF")
		self.gui_LEDBrightM = self.builder.get_object("LEDBrightM")
		self.gui_LEDBrightR = self.builder.get_object("LEDBrightR")
		self.gui_LEDColourF = self.builder.get_object("LEDColourF")
		self.gui_LEDColourM = self.builder.get_object("LEDColourM")
		self.gui_LEDColourR = self.builder.get_object("LEDColourR")

		self.gui_Camera = [
			self.builder.get_object("CameraLeft"),
			self.builder.get_object("CameraRight")
			]
		self.gui_ResolutionSelection = self.builder.get_object("ResolutionSelection")
		self.gui_CapResolutionSelection = self.builder.get_object("CapResolutionSelection")
		self.gui_CapFPSSelection = self.builder.get_object("CapFPSSelection")
		self.gui_MeasuredFPS = self.builder.get_object("MeasuredFPS")

		#Generate variables to store user input
		self.preset = False
		self.user_blink = 0
		self.user_waggle = 0
		self.user_wiggle = 0
		self.user_wag_rate = 0
		self.wag_phase = 0

		#Microphone Parameters
		# Number of points to display
		self.x_len = 40000
		# number of microphones coming through on topic
		self.no_of_mics = 4

		#Generate figure for plotting mics
		self.fig1 = plt.figure()
		self.fig1.suptitle("Microphones") # Give figure title

		#LEFT EAR
		self.left_ear_plot = self.fig1.add_subplot(4,1,1)
		self.left_ear_plot.set_ylim([-33000, 33000])
		self.left_ear_plot.set_xlim([0, self.x_len])
		self.left_ear_xs = np.arange(0, self.x_len)
		self.left_ear_plot.set_xticklabels([])
		self.left_ear_plot.set_yticks([])
		self.left_ear_plot.grid(which="both", axis="x")
		self.left_ear_plot.set_ylabel("Left Ear", rotation=0, ha="right")
		self.left_ear_ys = np.zeros(self.x_len)
		self.left_ear_line, = self.left_ear_plot.plot(self.left_ear_xs, self.left_ear_ys, linewidth=0.5, color="b")

		#RIGHT EAR
		self.right_ear_plot = self.fig1.add_subplot(4,1,2)
		self.right_ear_plot.set_ylim([-33000, 33000])
		self.right_ear_plot.set_xlim([0, self.x_len])
		self.right_ear_xs = np.arange(0, self.x_len)
		self.right_ear_plot.set_xticklabels([])
		self.right_ear_plot.set_yticks([])
		self.right_ear_plot.grid(which="both", axis="x")
		self.right_ear_plot.set_ylabel("Right Ear", rotation=0, ha="right")
		self.right_ear_ys = np.zeros(self.x_len)
		self.right_ear_line, = self.right_ear_plot.plot(self.right_ear_xs, self.right_ear_ys, linewidth=0.5, color="r")

		#HEAD
		self.head_plot = self.fig1.add_subplot(4,1,3)
		self.head_plot.set_ylim([-33000, 33000])
		self.head_plot.set_xlim([0, self.x_len])
		self.head_xs = np.arange(0, self.x_len)
		self.head_plot.set_xticklabels([])
		self.head_plot.set_yticks([])
		self.head_plot.grid(which="both", axis="x")
		self.head_plot.set_ylabel("Head", rotation=0, ha="right")
		self.head_ys = np.zeros(self.x_len)
		self.head_line, = self.head_plot.plot(self.head_xs, self.head_ys, linewidth=0.5, color="g")

		#Tail
		self.tail_plot = self.fig1.add_subplot(4,1,4)
		self.tail_plot.set_ylim([-33000, 33000])
		self.tail_plot.set_xlim([0, self.x_len])
		self.tail_xs = np.arange(0, self.x_len)
		self.tail_plot.set_yticks([])
		self.tail_plot.set_xlabel("Samples")
		self.tail_plot.grid(which="both", axis="x")
		self.tail_plot.set_ylabel("Tail", rotation=0, ha="right")
		self.tail_ys = np.zeros(self.x_len)
		self.tail_line, = self.tail_plot.plot(self.tail_xs, self.tail_ys, linewidth=0.5, color="c")

		self.canvas = FigureCanvas(self.fig1)
		self.ani = animation.FuncAnimation(self.fig1, self.update_line, fargs=(self.left_ear_ys,self.right_ear_ys, self.head_ys, self.tail_ys,), init_func=self.animation_init, interval=10, blit=False)
		self.fig1.subplots_adjust(hspace=0, wspace=0)
		self.MicScrolledWindow.add(self.canvas)

		# variables to store input data
		self.input_package = None
		self.input_camera = [None, None]
		self.t_input_camera = [[], []]
		self.input_mics = np.zeros((self.x_len, self.no_of_mics))

		#Create object to convert ROS images to OpenCV format
		self.image_converter = CvBridge()

		#Start timer to call function which updates GUI
		GLib.timeout_add(20, self.update_gui)
		GLib.timeout_add(20, self.update_images)

		#Create objects to hold published data
		self.velocity = TwistStamped()

		self.kin_joints = JointState()
		self.kin_joints.name = ["tilt", "lift", "yaw", "pitch"]
		self.kin_joints.position = [0.0, math.radians(34.0), 0.0, 0.0]

		self.cos_joints = Float32MultiArray()
		self.cos_joints.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

		self.tone = UInt16MultiArray()
		self.tone.data = [0, 0, 0]

		self.illum = UInt32MultiArray()
		self.illum.data = [0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF]

		self.camera_zoom = None
		self.auto_camera_zoom = [0, 0] # determine zoom from first received frame
		self.frame_params = [180, '180w', 15]
		self.meas_fps = ["", ""]

		# set initial values
		self.on_ResetCosButton_clicked()
		self.adjustEyeInitialValues()
		self.on_LEDReset_clicked()

		# display GUI
		self.MainWindow.show_all()

		# robot name
		topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME")
		print("subscribing to topics under", topic_base_name)

		# publishers
		self.pub_cmd_vel = rospy.Publisher(topic_base_name + "/control/cmd_vel", TwistStamped, queue_size=0)
		self.pub_cos = rospy.Publisher(topic_base_name + "/control/cosmetic_joints", Float32MultiArray, queue_size=0)
		self.pub_illum = rospy.Publisher(topic_base_name + "/control/illum", UInt32MultiArray, queue_size=0)
		self.pub_kin = rospy.Publisher(topic_base_name + "/control/kinematic_joints", JointState, queue_size=0)
		self.pub_tone = rospy.Publisher(topic_base_name + "/control/tone", UInt16MultiArray, queue_size=0)
		self.pub_command = rospy.Publisher(topic_base_name + "/control/command", String, queue_size=0)

		# subscribers
		self.sub_package = rospy.Subscriber(topic_base_name + "/sensors/package",
					miro.msg.sensors_package, self.callback_package, queue_size=1, tcp_nodelay=True)
		self.sub_mics = rospy.Subscriber(topic_base_name + "/sensors/mics",
					Int16MultiArray, self.callback_mics, queue_size=1, tcp_nodelay=True)
		self.sub_caml = rospy.Subscriber(topic_base_name + "/sensors/caml/compressed",
					CompressedImage, self.callback_caml, queue_size=1, tcp_nodelay=True)
		self.sub_camr = rospy.Subscriber(topic_base_name + "/sensors/camr/compressed",
					CompressedImage, self.callback_camr, queue_size=1, tcp_nodelay=True)

	#Handle Closure of Main Window
	def on_MainWindow_destroy(self, *args):
		print("GUI closed due to user quit")
		Gtk.main_quit()

	def on_DisplayCamButton_toggled(self, *args):
		if self.DisplayCamButton.get_active():
			self.CamWindow.show_all()
			print("Displaying Cameras")
			self.on_ResolutionSelection_changed()
			self.on_CapResolutionSelection_changed()
		else:
			self.CamWindow.hide()
			print("Stop Displaying Cameras")

	#Handle Closure of Camera Window to prevent destruction
	def on_CamWindow_delete_event(self, *args):
		self.CamWindow.hide()
		self.DisplayCamButton.set_active(False)
		print("Camera window closed due to user quit")
		return True #This prevents call of destroy function

	def on_DisplayMicButton_toggled(self, *args):
		if self.DisplayMicButton.get_active():
			self.MicWindow.show_all()
			print("Displaying Microphones")
		else:
			self.MicWindow.hide()
			print("Stop Displaying Microphones")

	#Handle Closure of Mic Window to prevent destruction
	def on_MicWindow_delete_event(self, *args):
		self.MicWindow.hide()
		self.DisplayMicButton.set_active(False)
		print("Microphone window closed due to user quit")
		return True #This prevents call of destroy function

################################################# VELOCITY CONTROL ###########################################################

	def on_VelControl_change_value(self, *args):
		self.velocity.twist.linear.x = self.VelControl.get_value()

	def on_AngVelControl_change_value(self, *args):
		self.velocity.twist.angular.z = self.AngVelControl.get_value()

	def on_ResetBodyVel_clicked(self, *args):
		self.VelControl.set_value(0.0)
		self.velocity.twist.linear.x = self.VelControl.get_value()
		self.AngVelControl.set_value(0.0)
		self.velocity.twist.angular.z = self.AngVelControl.get_value()

############################################### KINEMATICS CONTROL ###########################################################

	def on_ResetKinButton_clicked(self, *args):
		self.LiftControl.set_value(34.0)
		self.YawControl.set_value(0.0)
		self.PitchControl.set_value(0.0)
		self.kin_joints.position[lift] = math.radians(self.LiftControl.get_value())
		self.kin_joints.position[pitch] = math.radians(self.PitchControl.get_value())
		self.kin_joints.position[yaw] = math.radians(self.YawControl.get_value())

	def on_LiftControl_change_value(self, *args):
		self.kin_joints.position[lift] = math.radians(self.LiftControl.get_value())

	def on_PitchControl_change_value(self, *args):
		self.kin_joints.position[pitch] = math.radians(self.PitchControl.get_value())

	def on_YawControl_change_value(self, *args):
		self.kin_joints.position[yaw] = math.radians(self.YawControl.get_value())

############################################### COSMETICS CONTROL ###########################################################

	def adjustEyeInitialValues(self):

		# the calibration values for the eyelids are half-closed
		# but it's annoying to have the GUI default to this because
		# then the cameras are half-obscured so for the eyes only
		# we don't start at the calibration point
		self.LeftEyeControl.set_value(0.0)
		self.RightEyeControl.set_value(0.0)

	def on_ResetCosButton_clicked(self, *args):
		self.LeftEyeControl.set_value(miro.constants.EYE_CALIB)
		self.RightEyeControl.set_value(miro.constants.EYE_CALIB)
		self.LeftEarControl.set_value(miro.constants.EAR_CALIB)
		self.RightEarControl.set_value(miro.constants.EAR_CALIB)
		self.WagControl.set_value(miro.constants.WAG_CALIB)
		self.DroopControl.set_value(miro.constants.DROOP_CALIB)
		self.WagRateControl.set_value(31.0)
		self.cos_joints.data[droop] = self.DroopControl.get_value()
		self.cos_joints.data[wag] = self.WagControl.get_value()
		self.cos_joints.data[left_eye] = self.LeftEyeControl.get_value()
		self.cos_joints.data[right_eye] = self.RightEyeControl.get_value()
		self.cos_joints.data[left_ear] = self.LeftEarControl.get_value()
		self.cos_joints.data[right_ear] = self.RightEarControl.get_value()
		self.user_wag_rate = 0

######## EYES ########

	def on_LeftEyeControl_change_value(self, *args):
		self.cos_joints.data[left_eye] = self.LeftEyeControl.get_value()

	def on_RightEyeControl_change_value(self, *args):
		self.cos_joints.data[right_eye] = self.RightEyeControl.get_value()

	def on_BlinkButton_clicked(self, *args):
		if self.UserControlCos.get_active():
			self.user_blink = 1

	def on_WaggleButton_clicked(self, *args):
		if self.UserControlCos.get_active():
			self.user_waggle = 1

	def on_WiggleButton_clicked(self, *args):
		if self.UserControlCos.get_active():
			self.user_wiggle = 1

######## Tail ########

	def on_WagControl_change_value(self, *args):
		self.cos_joints.data[wag] = self.WagControl.get_value()

	def on_DroopControl_change_value(self, *args):
		self.cos_joints.data[droop] = self.DroopControl.get_value()

	def on_WagRateControl_change_value(self, *args):
		wag_rate = self.WagRateControl.get_value()
		if wag_rate == 31:
			self.user_wag_rate = 0
		else:
			self.user_wag_rate = wag_rate


######## EARS #########

	def on_LeftEarControl_change_value(self, *args):
		self.cos_joints.data[left_ear] = self.LeftEarControl.get_value()

	def on_RightEarControl_change_value(self, *args):
		self.cos_joints.data[right_ear] = self.RightEarControl.get_value()

##################################### Measured Velocities + Angles ##########################################################

	#Returning true from change_value prevents user from altering slider value
	def on_VelMeasured_change_value(self, *args):
		return True

	def on_AngVelMeasured_change_value(self, *args):
		return True

	def on_LiftMeasured_change_value(self, *args):
		return True

	def on_YawMeasured_change_value(self, *args):
		return True

	def on_PitchMeasured_change_value(self, *args):
		return True

	def on_SonarBar_change_value(self, *args):
		return True

################################### TONE GENERATOR ##########################################################################

	def on_SendToneButton_clicked(self, *args):
		self.tone.data[freq] = int(self.FreqControl.get_value())
		self.tone.data[volume] = int(self.VolControl.get_value())
		self.tone.data[duration] = int(self.DurationControl.get_value())
		self.pub_tone.publish(self.tone)

	def on_Tone1Button_clicked(self, *args):
		self.tone.data[freq] = 1
		self.tone.data[volume] = int(self.VolControl.get_value())
		self.tone.data[duration] = 1
		self.pub_tone.publish(self.tone)

	def on_Tone2Button_clicked(self, *args):
		self.tone.data[freq] = 2
		self.tone.data[volume] = int(self.VolControl.get_value())
		self.tone.data[duration] = 1
		self.pub_tone.publish(self.tone)

	def on_Tone3Button_clicked(self, *args):
		self.tone.data[freq] = 3
		self.tone.data[volume] = int(self.VolControl.get_value())
		self.tone.data[duration] = 1
		self.pub_tone.publish(self.tone)


##################################### LED PATTERN GENERATOR #################################################################

	def on_LEDChange(self, *args):

		value = generate_illum(
					self.gui_LEDColourF.get_rgba(),
					self.gui_LEDBrightF.get_value()
					)
		self.illum.data[front_left] = value
		self.illum.data[front_right] = value
		value = generate_illum(
					self.gui_LEDColourM.get_rgba(),
					self.gui_LEDBrightM.get_value()
					)
		self.illum.data[mid_left] = value
		self.illum.data[mid_right] = value
		value = generate_illum(
					self.gui_LEDColourR.get_rgba(),
					self.gui_LEDBrightR.get_value()
					)
		self.illum.data[rear_left] = value
		self.illum.data[rear_right] = value

	def LEDSetAll(self, color, bright):

		self.gui_LEDColourF.set_rgba(color)
		self.gui_LEDBrightF.set_value(bright)
		self.gui_LEDColourM.set_rgba(color)
		self.gui_LEDBrightM.set_value(bright)
		self.gui_LEDColourR.set_rgba(color)
		self.gui_LEDBrightR.set_value(bright)
		self.on_LEDChange()

	def on_LEDReset_clicked(self, *args):

		color = Gdk.RGBA(1.0, 1.0, 1.0, 1.0)
		bright = 0
		self.LEDSetAll(color, 0)

	def on_LEDPreset1_clicked(self, *args):

		color = Gdk.RGBA(1.0, 1.0, 1.0, 1.0)
		bright = 63
		self.LEDSetAll(color, 63)

	def on_LEDPreset2_clicked(self, *args):

		bright = 63
		self.gui_LEDColourF.set_rgba(Gdk.RGBA(1.0, 0.0, 0.0, 1.0))
		self.gui_LEDBrightF.set_value(bright)
		self.gui_LEDColourM.set_rgba(Gdk.RGBA(0.0, 1.0, 0.0, 1.0))
		self.gui_LEDBrightM.set_value(bright)
		self.gui_LEDColourR.set_rgba(Gdk.RGBA(0.0, 0.0, 1.0, 1.0))
		self.gui_LEDBrightR.set_value(bright)
		self.on_LEDChange()

	def on_LEDPreset3_clicked(self, *args):
		print ("Preset 3")
 #############################################################################################################################

	def on_ButtonJpegLo_clicked(self, *args):
		cmd = "jpeg=10"
		self.pub_command.publish(cmd)

	def on_ButtonJpegMed_clicked(self, *args):
		cmd = "jpeg=60"
		self.pub_command.publish(cmd)

	def on_ButtonJpegHi_clicked(self, *args):
		cmd = "jpeg=80"
		self.pub_command.publish(cmd)

	def on_ResolutionSelection_changed(self, *args):
		self.camera_zoom = self.gui_ResolutionSelection.get_active_text()

	def parse_resolution(self, res_string):
		width_string, height_string = res_string.split("x", 1)
		width = int(width_string)
		height = int(height_string)
		return width, height

	def on_SendCamParamsButton_clicked(self, *args):
		cmd = "frame=" + self.frame_params[1] + "@" + str(self.frame_params[2])
		self.pub_command.publish(cmd)

		# set camera zoom to auto so it sets automatically when next frame arrives
		self.auto_camera_zoom = [self.frame_params[0], time.time()]

	def on_CapResolutionSelection_changed(self, *args):

		res_text = self.gui_CapResolutionSelection.get_active_text()
		cap_resolution_w, cap_resolution_h = self.parse_resolution(res_text)
		self.frame_params[0] = cap_resolution_h

		# convert to bridge format
		if (cap_resolution_w * 3) / 4 == cap_resolution_h:
			cap_resolution = str(cap_resolution_h) + "s"
		else:
			cap_resolution = str(cap_resolution_h) + "w"
		self.frame_params[1] = cap_resolution

	def on_CapFPSSelection_change_value(self, *args):
		self.frame_params[2] = int(self.gui_CapFPSSelection.get_value())

################################################################
## ROS CALLBACKS

	def callback_package(self, msg):

		# store for processing in update_gui
		self.input_package = msg

	def callback_mics(self, data):

		# discard data if GUI not displayed
		if not self.DisplayMicButton.get_active():
			return

		# save microphone data to rolling buffer for later processing
		# reshape into 4 x 500 array
		data = np.asarray(data.data)
		data = np.transpose(data.reshape((self.no_of_mics, 500)))
		data = np.flipud(data)
		# array is [ L, R, H, B] mics
		# add to top of buffer
		self.input_mics = np.vstack((data, self.input_mics[:self.x_len-500,:]))

	def do_auto_camera_zoom(self, image_height):

		if image_height <= 240:
			self.gui_ResolutionSelection.set_active(2)
		elif image_height > 600:
			self.gui_ResolutionSelection.set_active(0)
		else:
			self.gui_ResolutionSelection.set_active(1)
		self.on_ResolutionSelection_changed()

	def do_auto_camera_res(self, shape):

		l = ['240x176', '320x176', '320x240', '480x360', '640x360', '960x720', '1280x720']
		s = str(shape[1]) + "x" + str(shape[0])
		for i in range(len(l)):
			if s == l[i]:
				print("detected camera resolution", s)
				self.gui_CapResolutionSelection.set_active(i)
				return

	def callback_cam(self, ros_image, index):

		# discard data if GUI not displayed
		if not self.CamWindow.get_property("visible"):
			self.t_input_camera = [[], []]
			return
			
		# ignore empty frames which occur sometimes during parameter changes
		if len(ros_image.data) == 0:
			print("dropped empty camera frame")
			return

		# silently (ish) handle corrupted JPEG frames
		try:

			# convert compressed ROS image to raw CV image
			image = self.image_converter.compressed_imgmsg_to_cv2(ros_image, "rgb8")

			# set camera zoom automatically if has not been set already
			if not self.auto_camera_zoom is None:
				h = self.auto_camera_zoom[0]
				dt = time.time() - self.auto_camera_zoom[1]
				if h == 0:
					# initial state, set from first received frame regardless
					self.do_auto_camera_zoom(image.shape[0])
					self.auto_camera_zoom = None
					# for initial frame, also set resolution selector
					self.do_auto_camera_res(image.shape)
				elif dt > 4.0:
					self.auto_camera_zoom = None
				elif abs(image.shape[0] - h) < 32:
					self.do_auto_camera_zoom(h)
					self.auto_camera_zoom = None

			# do zoom
			if self.camera_zoom == "0.5x":
				image = cv2.resize(image, (int(image.shape[1] * 0.5), int(image.shape[0] * 0.5)))
			elif self.camera_zoom == "2x":
				image = cv2.resize(image, (int(image.shape[1] * 2.0), int(image.shape[0] * 2.0)))

			# store image for display
			self.input_camera[index] = image

		except CvBridgeError as e:

			# swallow error, silently
			#print(e)
			pass

	def callback_caml(self, ros_image):

		self.callback_cam(ros_image, 0)

	def callback_camr(self, ros_image):

		self.callback_cam(ros_image, 1)

################################################################
## GUI UPDATES

	def update_line(self, i, left_ear_ys, right_ear_ys, head_ys, tail_ys):
		if self.DisplayMicButton.get_active():
			#Flip buffer so that incoming data moves in from the right
			left_ear_data = np.flipud(self.input_mics[:, 0])
			right_ear_data = np.flipud(self.input_mics[:, 1])
			head_data = np.flipud(self.input_mics[:, 2])
			tail_data = np.flipud(self.input_mics[:, 3])

			#Append new buffer data to plotting data
			left_ear_ys = np.append(left_ear_ys, left_ear_data)
			right_ear_ys = np.append(right_ear_ys, right_ear_data)
			head_ys = np.append(head_ys, head_data)
			tail_ys = np.append(tail_ys, tail_data)

			#Remove old sample outside of plot
			left_ear_ys = left_ear_ys[-self.x_len:]
			right_ear_ys = right_ear_ys[-self.x_len:]
			head_ys = head_ys[-self.x_len:]
			tail_ys = tail_ys[-self.x_len:]

			#Set data to line
			self.left_ear_line.set_ydata(left_ear_ys)
			self.right_ear_line.set_ydata(right_ear_ys)
			self.head_line.set_ydata(head_ys)
			self.tail_line.set_ydata(tail_ys)

		#Return the line to be animated
		return self.left_ear_line, self.right_ear_line, self.head_line, self.tail_line,

	def animation_init(self):
		self.left_ear_line.set_ydata(np.zeros(self.x_len))
		self.right_ear_line.set_ydata(np.zeros(self.x_len))
		self.head_line.set_ydata(np.zeros(self.x_len))
		self.tail_line.set_ydata(np.zeros(self.x_len))
		return self.left_ear_line, self.right_ear_line, self.head_line, self.tail_line,

	def update_images(self):

		# skip if GUI not open
		if not self.CamWindow.get_property("visible"):
			return True

		# for each camera
		for i in range(2):

			# get image
			image = self.input_camera[i]
			self.input_camera[i] = None
			if image is None:
				continue

			# do fps
			t = time.time()
			tt = self.t_input_camera[i]
			tt.append(t)
			n_meas = 15
			tt = tt[-(n_meas+1):]
			if len(tt) == (n_meas+1):
				dt = (tt[n_meas] - tt[0]) / float(n_meas)
				fps = format_num(1.0 / dt, 1)
			else:
				fps = "???"
			self.meas_fps[i] = fps

			# write in cross-hairs
			h = image.shape[0]
			w = image.shape[1]
			# https://www.python.org/dev/peps/pep-0238/
			h2 = h // 2
			w2 = w // 2
			cv2.line(image, (0, h2), (w, h2), (255, 0, 255), 1)
			cv2.line(image, (0, h2), (w, h2), (255, 0, 255), 1)
			cv2.line(image, (w2, 0), (w2, h), (255, 0, 255), 1)
			cv2.line(image, (w2-1, 0), (w2-1, h), (255, 0, 255), 1)

			# write in nominal "dead ahead" point (see dev/camera_model/190724/horiz_map)
			x = w * 0.75
			if i == 1:
				x = w * 0.25
			x = int(x)
			cv2.line(image, (x, int(h*0.45)), (x, int(h*0.55)), (255, 0, 255), 1)

			# update displayed image
			pb = GdkPixbuf.Pixbuf.new_from_data(image.tostring(),
						GdkPixbuf.Colorspace.RGB, False, 8,
						image.shape[1], image.shape[0],
						image.shape[2]*image.shape[1]
						)
			self.gui_Camera[i].set_from_pixbuf(pb.copy())

		fpss = self.meas_fps[0] + " / " + self.meas_fps[1]
		if self.gui_MeasuredFPS.get_text() != fpss:
			self.gui_MeasuredFPS.set_text(fpss)

		return True

	def update_gui(self):

		self.step += 1
		step_ = self.step % 100

		if not self.input_package is None:

			# acquire
			p = self.input_package
			self.input_package = None

			# update battery
			x = p.battery.voltage
			self.BatteryBar.set_value(x)
			self.BatteryText.set_text(format_num(x) + "V")

			# update sonar
			x = p.sonar.range
			self.SonarBar.set_value(x)
			if x == 0:
				self.SonarText.set_text("short")
			elif x > 1.0:
				self.SonarText.set_text("inf")
			else:
				self.SonarText.set_text(format_num(x) + "m")

			# update light
			x = p.light.data
			self.gui_LightBarFL.set_value(x[0] * 100)
			self.gui_LightBarFR.set_value(x[1] * 100)
			self.gui_LightBarRL.set_value(x[2] * 100)
			self.gui_LightBarRR.set_value(x[3] * 100)

			# update body touch
			x = p.touch_body.data
			self.BodyTouchText.set_text("{0:014b}".format(x))
			for i in range(14):
				self.BodyTouchBars[i].set_value(x & (1 << i))

			# update head touch
			x = p.touch_head.data
			self.HeadTouchText.set_text("{0:014b}".format(x))
			hts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			# raw order if not re-ordered in firmware...
			#order = [8, 7, 0, 1, 4, 3, 6, 5, 2, 9, 12, 13, 10, 11]
			# but, now re-ordered in firmware...
			order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
			# hint: body touch are ordered correctly just by wiring
			for i in range(14):
				hts[order[i]] = x & (1 << i)
			for i in range(14):
				self.HeadTouchBars[i].set_value(hts[i])

			# update body imu
			x = p.imu_body.linear_acceleration
			#self.BodyIMUTextX.set_text(format_num(x.x))
			#self.BodyIMUTextY.set_text(format_num(x.y))
			#self.BodyIMUTextZ.set_text(format_num(x.z))
			self.gui_AccBarBX.set_value(x.x / 9.81 * 50.0)
			self.gui_AccBarBY.set_value(x.y / 9.81 * 50.0)
			self.gui_AccBarBZ.set_value(x.z / 9.81 * 50.0)
			l = np.sqrt(x.x*x.x + x.y*x.y + x.z*x.z)
			self.gui_AccBarBL2.set_value(l / 9.81 * 50.0)

			# update head imu
			x = p.imu_head.linear_acceleration
			#self.HeadIMUTextX.set_text(format_num(x.x))
			#self.HeadIMUTextY.set_text(format_num(x.y))
			#self.HeadIMUTextZ.set_text(format_num(x.z))
			self.gui_AccBarHX.set_value(x.x / 9.81 * 50.0)
			self.gui_AccBarHY.set_value(x.y / 9.81 * 50.0)
			self.gui_AccBarHZ.set_value(x.z / 9.81 * 50.0)
			l = np.sqrt(x.x*x.x + x.y*x.y + x.z*x.z)
			self.gui_AccBarHL2.set_value(l / 9.81 * 50.0)

			# update cliff
			x = (np.array([p.cliff.data[0], p.cliff.data[1]]) * 15).astype('int')
			#self.CliffLeftText.set_text(str(x[0]))
			#self.CliffRightText.set_text(str(x[1]))
			self.gui_CliffBarL.set_value(x[0])
			self.gui_CliffBarR.set_value(x[1])

			# update odom
			x = p.odom.twist.twist
			self.VelMeasured.set_value(x.linear.x)
			self.AngVelMeasured.set_value(x.angular.z)

			# update wheel speed (gui elements read in mm/s)
			x = p.wheel_speed_opto.data
			self.gui_WheelSpeedOptoL.set_value(x[0] * 1000)
			self.gui_WheelSpeedOptoR.set_value(x[1] * 1000)
			x = p.wheel_speed_back_emf.data
			self.gui_WheelSpeedEMFL.set_value(x[0] * 1000)
			self.gui_WheelSpeedEMFR.set_value(x[1] * 1000)

			# update kinematic joints
			x = p.kinematic_joints.position
			self.LiftMeasured.set_value(math.degrees(x[1]))
			self.YawMeasured.set_value(math.degrees(x[2]))
			self.PitchMeasured.set_value(math.degrees(x[3]))

		# if user is controlling illumination
		if self.UserControlIllum.get_active():
			self.pub_illum.publish(self.illum)

		# if user is controlling velocity
		if self.UserControlVel.get_active():
			self.pub_cmd_vel.publish(self.velocity)

		# if user is controlling kinematics
		if self.UserControlKin.get_active():
			self.pub_kin.publish(self.kin_joints)

		# if user is controlling cosmetics
		if self.UserControlCos.get_active():

			wiggle_n = 20

			if self.user_blink > 0:

				self.cos_joints.data[left_eye] = wiggle(0.0, self.user_blink, wiggle_n)
				self.cos_joints.data[right_eye] = wiggle(0.0, self.user_blink, wiggle_n)

				# follow
				self.LeftEyeControl.set_value(self.cos_joints.data[left_eye])
				self.RightEyeControl.set_value(self.cos_joints.data[right_eye])

				self.user_blink += 1
				if self.user_blink > (2 * wiggle_n):
					self.user_blink = 0

			if self.user_wag_rate > 0 or self.wag_phase > 0:

				if self.user_wag_rate > 0:
					self.wag_phase += np.pi / self.user_wag_rate
				else:
					self.wag_phase = 0

				if self.wag_phase >= 2 * np.pi:
					self.wag_phase -= 2 * np.pi

				self.cos_joints.data[droop] = 0.0
				self.cos_joints.data[wag] = np.sin(self.wag_phase) * 0.5 + 0.5

				# follow
				self.WagControl.set_value(self.cos_joints.data[wag])
				self.DroopControl.set_value(self.cos_joints.data[droop])

				# clear any pending waggle so it doesn't execute when wag stops
				self.user_waggle = 0

			elif self.user_waggle > 0:

				if self.user_waggle <= (2 * wiggle_n):
					self.cos_joints.data[wag] = wiggle(0.5, self.user_waggle, wiggle_n)
					self.cos_joints.data[droop] = 0.0
				else:
					self.cos_joints.data[wag] = 0.5
					self.cos_joints.data[droop] = wiggle(0.0, self.user_waggle - (2*wiggle_n), wiggle_n)

				# follow
				self.WagControl.set_value(self.cos_joints.data[wag])
				self.DroopControl.set_value(self.cos_joints.data[droop])

				self.user_waggle += 1
				if self.user_waggle > (4 * wiggle_n):
					self.user_waggle = 0

			if self.user_wiggle > 0:

				self.cos_joints.data[left_ear] = wiggle(0.3333, self.user_wiggle, wiggle_n)
				self.cos_joints.data[right_ear] = wiggle(0.3333, self.user_wiggle, wiggle_n)

				# follow
				self.LeftEarControl.set_value(self.cos_joints.data[left_ear])
				self.RightEarControl.set_value(self.cos_joints.data[right_ear])

				self.user_wiggle += 1
				if self.user_wiggle > (2 * wiggle_n):
					self.user_wiggle = 0

			self.pub_cos.publish(self.cos_joints)

		return True

################################################################
## MAIN

if __name__ == "__main__":
	main = miro_gui()
	rospy.init_node("client_gui")
	Gtk.main()

