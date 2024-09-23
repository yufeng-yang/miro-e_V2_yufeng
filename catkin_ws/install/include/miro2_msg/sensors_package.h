// Generated by gencpp from file miro2_msg/sensors_package.msg
// DO NOT EDIT!


#ifndef MIRO2_MSG_MESSAGE_SENSORS_PACKAGE_H
#define MIRO2_MSG_MESSAGE_SENSORS_PACKAGE_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <std_msgs/Header.h>
#include <miro2_msg/BatteryState.h>
#include <std_msgs/Float32MultiArray.h>
#include <std_msgs/UInt16.h>
#include <std_msgs/UInt32.h>
#include <sensor_msgs/Imu.h>
#include <sensor_msgs/Imu.h>
#include <sensor_msgs/JointState.h>
#include <std_msgs/Float32MultiArray.h>
#include <nav_msgs/Odometry.h>
#include <sensor_msgs/Range.h>
#include <std_msgs/UInt16MultiArray.h>
#include <std_msgs/UInt16.h>
#include <std_msgs/UInt16.h>
#include <std_msgs/Float32MultiArray.h>
#include <std_msgs/Float32MultiArray.h>
#include <std_msgs/Float32MultiArray.h>
#include <std_msgs/Float32MultiArray.h>
#include <geometry_msgs/Pose2D.h>

namespace miro2_msg
{
template <class ContainerAllocator>
struct sensors_package_
{
  typedef sensors_package_<ContainerAllocator> Type;

  sensors_package_()
    : header()
    , battery()
    , cliff()
    , dip()
    , flags()
    , imu_head()
    , imu_body()
    , kinematic_joints()
    , light()
    , odom()
    , sonar()
    , stream()
    , touch_body()
    , touch_head()
    , wheel_speed_cmd()
    , wheel_speed_back_emf()
    , wheel_speed_opto()
    , wheel_effort_pwm()
    , body_pose()  {
    }
  sensors_package_(const ContainerAllocator& _alloc)
    : header(_alloc)
    , battery(_alloc)
    , cliff(_alloc)
    , dip(_alloc)
    , flags(_alloc)
    , imu_head(_alloc)
    , imu_body(_alloc)
    , kinematic_joints(_alloc)
    , light(_alloc)
    , odom(_alloc)
    , sonar(_alloc)
    , stream(_alloc)
    , touch_body(_alloc)
    , touch_head(_alloc)
    , wheel_speed_cmd(_alloc)
    , wheel_speed_back_emf(_alloc)
    , wheel_speed_opto(_alloc)
    , wheel_effort_pwm(_alloc)
    , body_pose(_alloc)  {
  (void)_alloc;
    }



   typedef  ::std_msgs::Header_<ContainerAllocator>  _header_type;
  _header_type header;

   typedef  ::miro2_msg::BatteryState_<ContainerAllocator>  _battery_type;
  _battery_type battery;

   typedef  ::std_msgs::Float32MultiArray_<ContainerAllocator>  _cliff_type;
  _cliff_type cliff;

   typedef  ::std_msgs::UInt16_<ContainerAllocator>  _dip_type;
  _dip_type dip;

   typedef  ::std_msgs::UInt32_<ContainerAllocator>  _flags_type;
  _flags_type flags;

   typedef  ::sensor_msgs::Imu_<ContainerAllocator>  _imu_head_type;
  _imu_head_type imu_head;

   typedef  ::sensor_msgs::Imu_<ContainerAllocator>  _imu_body_type;
  _imu_body_type imu_body;

   typedef  ::sensor_msgs::JointState_<ContainerAllocator>  _kinematic_joints_type;
  _kinematic_joints_type kinematic_joints;

   typedef  ::std_msgs::Float32MultiArray_<ContainerAllocator>  _light_type;
  _light_type light;

   typedef  ::nav_msgs::Odometry_<ContainerAllocator>  _odom_type;
  _odom_type odom;

   typedef  ::sensor_msgs::Range_<ContainerAllocator>  _sonar_type;
  _sonar_type sonar;

   typedef  ::std_msgs::UInt16MultiArray_<ContainerAllocator>  _stream_type;
  _stream_type stream;

   typedef  ::std_msgs::UInt16_<ContainerAllocator>  _touch_body_type;
  _touch_body_type touch_body;

   typedef  ::std_msgs::UInt16_<ContainerAllocator>  _touch_head_type;
  _touch_head_type touch_head;

   typedef  ::std_msgs::Float32MultiArray_<ContainerAllocator>  _wheel_speed_cmd_type;
  _wheel_speed_cmd_type wheel_speed_cmd;

   typedef  ::std_msgs::Float32MultiArray_<ContainerAllocator>  _wheel_speed_back_emf_type;
  _wheel_speed_back_emf_type wheel_speed_back_emf;

   typedef  ::std_msgs::Float32MultiArray_<ContainerAllocator>  _wheel_speed_opto_type;
  _wheel_speed_opto_type wheel_speed_opto;

   typedef  ::std_msgs::Float32MultiArray_<ContainerAllocator>  _wheel_effort_pwm_type;
  _wheel_effort_pwm_type wheel_effort_pwm;

   typedef  ::geometry_msgs::Pose2D_<ContainerAllocator>  _body_pose_type;
  _body_pose_type body_pose;





  typedef boost::shared_ptr< ::miro2_msg::sensors_package_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::miro2_msg::sensors_package_<ContainerAllocator> const> ConstPtr;

}; // struct sensors_package_

typedef ::miro2_msg::sensors_package_<std::allocator<void> > sensors_package;

typedef boost::shared_ptr< ::miro2_msg::sensors_package > sensors_packagePtr;
typedef boost::shared_ptr< ::miro2_msg::sensors_package const> sensors_packageConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::miro2_msg::sensors_package_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::miro2_msg::sensors_package_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::miro2_msg::sensors_package_<ContainerAllocator1> & lhs, const ::miro2_msg::sensors_package_<ContainerAllocator2> & rhs)
{
  return lhs.header == rhs.header &&
    lhs.battery == rhs.battery &&
    lhs.cliff == rhs.cliff &&
    lhs.dip == rhs.dip &&
    lhs.flags == rhs.flags &&
    lhs.imu_head == rhs.imu_head &&
    lhs.imu_body == rhs.imu_body &&
    lhs.kinematic_joints == rhs.kinematic_joints &&
    lhs.light == rhs.light &&
    lhs.odom == rhs.odom &&
    lhs.sonar == rhs.sonar &&
    lhs.stream == rhs.stream &&
    lhs.touch_body == rhs.touch_body &&
    lhs.touch_head == rhs.touch_head &&
    lhs.wheel_speed_cmd == rhs.wheel_speed_cmd &&
    lhs.wheel_speed_back_emf == rhs.wheel_speed_back_emf &&
    lhs.wheel_speed_opto == rhs.wheel_speed_opto &&
    lhs.wheel_effort_pwm == rhs.wheel_effort_pwm &&
    lhs.body_pose == rhs.body_pose;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::miro2_msg::sensors_package_<ContainerAllocator1> & lhs, const ::miro2_msg::sensors_package_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace miro2_msg

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::miro2_msg::sensors_package_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::miro2_msg::sensors_package_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::miro2_msg::sensors_package_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::miro2_msg::sensors_package_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::miro2_msg::sensors_package_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::miro2_msg::sensors_package_<ContainerAllocator> const>
  : TrueType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::miro2_msg::sensors_package_<ContainerAllocator> >
{
  static const char* value()
  {
    return "429d8257e8e981414c3f64c0a1074b4d";
  }

  static const char* value(const ::miro2_msg::sensors_package_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x429d8257e8e98141ULL;
  static const uint64_t static_value2 = 0x4c3f64c0a1074b4dULL;
};

template<class ContainerAllocator>
struct DataType< ::miro2_msg::sensors_package_<ContainerAllocator> >
{
  static const char* value()
  {
    return "miro2_msg/sensors_package";
  }

  static const char* value(const ::miro2_msg::sensors_package_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::miro2_msg::sensors_package_<ContainerAllocator> >
{
  static const char* value()
  {
    return "#	@section COPYRIGHT\n"
"#	Copyright (C) 2023 Consequential Robotics Ltd\n"
"#	\n"
"#	@section AUTHOR\n"
"#	Consequential Robotics http://consequentialrobotics.com\n"
"#	\n"
"#	@section LICENSE\n"
"#	For a full copy of the license agreement, and a complete\n"
"#	definition of \"The Software\", see LICENSE in the MDK root\n"
"#	directory.\n"
"#	\n"
"#	Subject to the terms of this Agreement, Consequential\n"
"#	Robotics grants to you a limited, non-exclusive, non-\n"
"#	transferable license, without right to sub-license, to use\n"
"#	\"The Software\" in accordance with this Agreement and any\n"
"#	other written agreement with Consequential Robotics.\n"
"#	Consequential Robotics does not transfer the title of \"The\n"
"#	Software\" to you; the license granted to you is not a sale.\n"
"#	This agreement is a binding legal agreement between\n"
"#	Consequential Robotics and the purchasers or users of \"The\n"
"#	Software\".\n"
"#	\n"
"#	THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY\n"
"#	KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE\n"
"#	WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR\n"
"#	PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS\n"
"#	OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR\n"
"#	OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR\n"
"#	OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE\n"
"#	SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n"
"#	\n"
"#\n"
"#	This message packages all the messages in /sensors into one\n"
"#	container so that a subscriber can receive them succinctly,\n"
"#	and in synchrony.\n"
"\n"
"\n"
"\n"
"#### HEADER\n"
"\n"
"# standard header\n"
"std_msgs/Header header\n"
"\n"
"\n"
"\n"
"#### CONTENT\n"
"\n"
"BatteryState battery\n"
"std_msgs/Float32MultiArray cliff\n"
"std_msgs/UInt16 dip\n"
"std_msgs/UInt32 flags\n"
"sensor_msgs/Imu imu_head\n"
"sensor_msgs/Imu imu_body\n"
"sensor_msgs/JointState kinematic_joints\n"
"std_msgs/Float32MultiArray light\n"
"nav_msgs/Odometry odom\n"
"sensor_msgs/Range sonar\n"
"std_msgs/UInt16MultiArray stream\n"
"std_msgs/UInt16 touch_body\n"
"std_msgs/UInt16 touch_head\n"
"std_msgs/Float32MultiArray wheel_speed_cmd\n"
"std_msgs/Float32MultiArray wheel_speed_back_emf\n"
"std_msgs/Float32MultiArray wheel_speed_opto\n"
"std_msgs/Float32MultiArray wheel_effort_pwm\n"
"\n"
"# available only in the simulator\n"
"geometry_msgs/Pose2D body_pose\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"================================================================================\n"
"MSG: std_msgs/Header\n"
"# Standard metadata for higher-level stamped data types.\n"
"# This is generally used to communicate timestamped data \n"
"# in a particular coordinate frame.\n"
"# \n"
"# sequence ID: consecutively increasing ID \n"
"uint32 seq\n"
"#Two-integer timestamp that is expressed as:\n"
"# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n"
"# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n"
"# time-handling sugar is provided by the client library\n"
"time stamp\n"
"#Frame this data is associated with\n"
"string frame_id\n"
"\n"
"================================================================================\n"
"MSG: miro2_msg/BatteryState\n"
"\n"
"# this is BatteryState.msg from the kinetic release; it is\n"
"# imported here so that we can use it as a legacy format\n"
"# on kinetic and later clients - at noetic, the format was\n"
"# changed to add temperature values.\n"
"#\n"
"# http://docs.ros.org/en/noetic/changelogs/sensor_msgs/changelog.html\n"
"# version 1.13.0 (2020-05-21)\n"
"\n"
"# Constants are chosen to match the enums in the linux kernel\n"
"# defined in include/linux/power_supply.h as of version 3.7\n"
"# The one difference is for style reasons the constants are\n"
"# all uppercase not mixed case.\n"
"\n"
"# Power supply status constants\n"
"uint8 POWER_SUPPLY_STATUS_UNKNOWN = 0\n"
"uint8 POWER_SUPPLY_STATUS_CHARGING = 1\n"
"uint8 POWER_SUPPLY_STATUS_DISCHARGING = 2\n"
"uint8 POWER_SUPPLY_STATUS_NOT_CHARGING = 3\n"
"uint8 POWER_SUPPLY_STATUS_FULL = 4\n"
"\n"
"# Power supply health constants\n"
"uint8 POWER_SUPPLY_HEALTH_UNKNOWN = 0\n"
"uint8 POWER_SUPPLY_HEALTH_GOOD = 1\n"
"uint8 POWER_SUPPLY_HEALTH_OVERHEAT = 2\n"
"uint8 POWER_SUPPLY_HEALTH_DEAD = 3\n"
"uint8 POWER_SUPPLY_HEALTH_OVERVOLTAGE = 4\n"
"uint8 POWER_SUPPLY_HEALTH_UNSPEC_FAILURE = 5\n"
"uint8 POWER_SUPPLY_HEALTH_COLD = 6\n"
"uint8 POWER_SUPPLY_HEALTH_WATCHDOG_TIMER_EXPIRE = 7\n"
"uint8 POWER_SUPPLY_HEALTH_SAFETY_TIMER_EXPIRE = 8\n"
"\n"
"# Power supply technology (chemistry) constants\n"
"uint8 POWER_SUPPLY_TECHNOLOGY_UNKNOWN = 0\n"
"uint8 POWER_SUPPLY_TECHNOLOGY_NIMH = 1\n"
"uint8 POWER_SUPPLY_TECHNOLOGY_LION = 2\n"
"uint8 POWER_SUPPLY_TECHNOLOGY_LIPO = 3\n"
"uint8 POWER_SUPPLY_TECHNOLOGY_LIFE = 4\n"
"uint8 POWER_SUPPLY_TECHNOLOGY_NICD = 5\n"
"uint8 POWER_SUPPLY_TECHNOLOGY_LIMN = 6\n"
"\n"
"Header  header\n"
"float32 voltage          # Voltage in Volts (Mandatory)\n"
"float32 current          # Negative when discharging (A)  (If unmeasured NaN)\n"
"float32 charge           # Current charge in Ah  (If unmeasured NaN)\n"
"float32 capacity         # Capacity in Ah (last full capacity)  (If unmeasured NaN)\n"
"float32 design_capacity  # Capacity in Ah (design capacity)  (If unmeasured NaN)\n"
"float32 percentage       # Charge percentage on 0 to 1 range  (If unmeasured NaN)\n"
"uint8   power_supply_status     # The charging status as reported. Values defined above\n"
"uint8   power_supply_health     # The battery health metric. Values defined above\n"
"uint8   power_supply_technology # The battery chemistry. Values defined above\n"
"bool    present          # True if the battery is present\n"
"\n"
"float32[] cell_voltage   # An array of individual cell voltages for each cell in the pack\n"
"                         # If individual voltages unknown but number of cells known set each to NaN\n"
"string location          # The location into which the battery is inserted. (slot number or plug)\n"
"string serial_number     # The best approximation of the battery serial number\n"
"\n"
"================================================================================\n"
"MSG: std_msgs/Float32MultiArray\n"
"# Please look at the MultiArrayLayout message definition for\n"
"# documentation on all multiarrays.\n"
"\n"
"MultiArrayLayout  layout        # specification of data layout\n"
"float32[]         data          # array of data\n"
"\n"
"\n"
"================================================================================\n"
"MSG: std_msgs/MultiArrayLayout\n"
"# The multiarray declares a generic multi-dimensional array of a\n"
"# particular data type.  Dimensions are ordered from outer most\n"
"# to inner most.\n"
"\n"
"MultiArrayDimension[] dim # Array of dimension properties\n"
"uint32 data_offset        # padding elements at front of data\n"
"\n"
"# Accessors should ALWAYS be written in terms of dimension stride\n"
"# and specified outer-most dimension first.\n"
"# \n"
"# multiarray(i,j,k) = data[data_offset + dim_stride[1]*i + dim_stride[2]*j + k]\n"
"#\n"
"# A standard, 3-channel 640x480 image with interleaved color channels\n"
"# would be specified as:\n"
"#\n"
"# dim[0].label  = \"height\"\n"
"# dim[0].size   = 480\n"
"# dim[0].stride = 3*640*480 = 921600  (note dim[0] stride is just size of image)\n"
"# dim[1].label  = \"width\"\n"
"# dim[1].size   = 640\n"
"# dim[1].stride = 3*640 = 1920\n"
"# dim[2].label  = \"channel\"\n"
"# dim[2].size   = 3\n"
"# dim[2].stride = 3\n"
"#\n"
"# multiarray(i,j,k) refers to the ith row, jth column, and kth channel.\n"
"\n"
"================================================================================\n"
"MSG: std_msgs/MultiArrayDimension\n"
"string label   # label of given dimension\n"
"uint32 size    # size of given dimension (in type units)\n"
"uint32 stride  # stride of given dimension\n"
"================================================================================\n"
"MSG: std_msgs/UInt16\n"
"uint16 data\n"
"\n"
"================================================================================\n"
"MSG: std_msgs/UInt32\n"
"uint32 data\n"
"================================================================================\n"
"MSG: sensor_msgs/Imu\n"
"# This is a message to hold data from an IMU (Inertial Measurement Unit)\n"
"#\n"
"# Accelerations should be in m/s^2 (not in g's), and rotational velocity should be in rad/sec\n"
"#\n"
"# If the covariance of the measurement is known, it should be filled in (if all you know is the \n"
"# variance of each measurement, e.g. from the datasheet, just put those along the diagonal)\n"
"# A covariance matrix of all zeros will be interpreted as \"covariance unknown\", and to use the\n"
"# data a covariance will have to be assumed or gotten from some other source\n"
"#\n"
"# If you have no estimate for one of the data elements (e.g. your IMU doesn't produce an orientation \n"
"# estimate), please set element 0 of the associated covariance matrix to -1\n"
"# If you are interpreting this message, please check for a value of -1 in the first element of each \n"
"# covariance matrix, and disregard the associated estimate.\n"
"\n"
"Header header\n"
"\n"
"geometry_msgs/Quaternion orientation\n"
"float64[9] orientation_covariance # Row major about x, y, z axes\n"
"\n"
"geometry_msgs/Vector3 angular_velocity\n"
"float64[9] angular_velocity_covariance # Row major about x, y, z axes\n"
"\n"
"geometry_msgs/Vector3 linear_acceleration\n"
"float64[9] linear_acceleration_covariance # Row major x, y z \n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Quaternion\n"
"# This represents an orientation in free space in quaternion form.\n"
"\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
"float64 w\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Vector3\n"
"# This represents a vector in free space. \n"
"# It is only meant to represent a direction. Therefore, it does not\n"
"# make sense to apply a translation to it (e.g., when applying a \n"
"# generic rigid transformation to a Vector3, tf2 will only apply the\n"
"# rotation). If you want your data to be translatable too, use the\n"
"# geometry_msgs/Point message instead.\n"
"\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
"================================================================================\n"
"MSG: sensor_msgs/JointState\n"
"# This is a message that holds data to describe the state of a set of torque controlled joints. \n"
"#\n"
"# The state of each joint (revolute or prismatic) is defined by:\n"
"#  * the position of the joint (rad or m),\n"
"#  * the velocity of the joint (rad/s or m/s) and \n"
"#  * the effort that is applied in the joint (Nm or N).\n"
"#\n"
"# Each joint is uniquely identified by its name\n"
"# The header specifies the time at which the joint states were recorded. All the joint states\n"
"# in one message have to be recorded at the same time.\n"
"#\n"
"# This message consists of a multiple arrays, one for each part of the joint state. \n"
"# The goal is to make each of the fields optional. When e.g. your joints have no\n"
"# effort associated with them, you can leave the effort array empty. \n"
"#\n"
"# All arrays in this message should have the same size, or be empty.\n"
"# This is the only way to uniquely associate the joint name with the correct\n"
"# states.\n"
"\n"
"\n"
"Header header\n"
"\n"
"string[] name\n"
"float64[] position\n"
"float64[] velocity\n"
"float64[] effort\n"
"\n"
"================================================================================\n"
"MSG: nav_msgs/Odometry\n"
"# This represents an estimate of a position and velocity in free space.  \n"
"# The pose in this message should be specified in the coordinate frame given by header.frame_id.\n"
"# The twist in this message should be specified in the coordinate frame given by the child_frame_id\n"
"Header header\n"
"string child_frame_id\n"
"geometry_msgs/PoseWithCovariance pose\n"
"geometry_msgs/TwistWithCovariance twist\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/PoseWithCovariance\n"
"# This represents a pose in free space with uncertainty.\n"
"\n"
"Pose pose\n"
"\n"
"# Row-major representation of the 6x6 covariance matrix\n"
"# The orientation parameters use a fixed-axis representation.\n"
"# In order, the parameters are:\n"
"# (x, y, z, rotation about X axis, rotation about Y axis, rotation about Z axis)\n"
"float64[36] covariance\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Pose\n"
"# A representation of pose in free space, composed of position and orientation. \n"
"Point position\n"
"Quaternion orientation\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Point\n"
"# This contains the position of a point in free space\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/TwistWithCovariance\n"
"# This expresses velocity in free space with uncertainty.\n"
"\n"
"Twist twist\n"
"\n"
"# Row-major representation of the 6x6 covariance matrix\n"
"# The orientation parameters use a fixed-axis representation.\n"
"# In order, the parameters are:\n"
"# (x, y, z, rotation about X axis, rotation about Y axis, rotation about Z axis)\n"
"float64[36] covariance\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Twist\n"
"# This expresses velocity in free space broken into its linear and angular parts.\n"
"Vector3  linear\n"
"Vector3  angular\n"
"\n"
"================================================================================\n"
"MSG: sensor_msgs/Range\n"
"# Single range reading from an active ranger that emits energy and reports\n"
"# one range reading that is valid along an arc at the distance measured. \n"
"# This message is  not appropriate for laser scanners. See the LaserScan\n"
"# message if you are working with a laser scanner.\n"
"\n"
"# This message also can represent a fixed-distance (binary) ranger.  This\n"
"# sensor will have min_range===max_range===distance of detection.\n"
"# These sensors follow REP 117 and will output -Inf if the object is detected\n"
"# and +Inf if the object is outside of the detection range.\n"
"\n"
"Header header           # timestamp in the header is the time the ranger\n"
"                        # returned the distance reading\n"
"\n"
"# Radiation type enums\n"
"# If you want a value added to this list, send an email to the ros-users list\n"
"uint8 ULTRASOUND=0\n"
"uint8 INFRARED=1\n"
"\n"
"uint8 radiation_type    # the type of radiation used by the sensor\n"
"                        # (sound, IR, etc) [enum]\n"
"\n"
"float32 field_of_view   # the size of the arc that the distance reading is\n"
"                        # valid for [rad]\n"
"                        # the object causing the range reading may have\n"
"                        # been anywhere within -field_of_view/2 and\n"
"                        # field_of_view/2 at the measured range. \n"
"                        # 0 angle corresponds to the x-axis of the sensor.\n"
"\n"
"float32 min_range       # minimum range value [m]\n"
"float32 max_range       # maximum range value [m]\n"
"                        # Fixed distance rangers require min_range==max_range\n"
"\n"
"float32 range           # range data [m]\n"
"                        # (Note: values < range_min or > range_max\n"
"                        # should be discarded)\n"
"                        # Fixed distance rangers only output -Inf or +Inf.\n"
"                        # -Inf represents a detection within fixed distance.\n"
"                        # (Detection too close to the sensor to quantify)\n"
"                        # +Inf represents no detection within the fixed distance.\n"
"                        # (Object out of range)\n"
"================================================================================\n"
"MSG: std_msgs/UInt16MultiArray\n"
"# Please look at the MultiArrayLayout message definition for\n"
"# documentation on all multiarrays.\n"
"\n"
"MultiArrayLayout  layout        # specification of data layout\n"
"uint16[]            data        # array of data\n"
"\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Pose2D\n"
"# Deprecated\n"
"# Please use the full 3D pose.\n"
"\n"
"# In general our recommendation is to use a full 3D representation of everything and for 2D specific applications make the appropriate projections into the plane for their calculations but optimally will preserve the 3D information during processing.\n"
"\n"
"# If we have parallel copies of 2D datatypes every UI and other pipeline will end up needing to have dual interfaces to plot everything. And you will end up with not being able to use 3D tools for 2D use cases even if they're completely valid, as you'd have to reimplement it with different inputs and outputs. It's not particularly hard to plot the 2D pose or compute the yaw error for the Pose message and there are already tools and libraries that can do this for you.\n"
"\n"
"\n"
"# This expresses a position and orientation on a 2D manifold.\n"
"\n"
"float64 x\n"
"float64 y\n"
"float64 theta\n"
;
  }

  static const char* value(const ::miro2_msg::sensors_package_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::miro2_msg::sensors_package_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.header);
      stream.next(m.battery);
      stream.next(m.cliff);
      stream.next(m.dip);
      stream.next(m.flags);
      stream.next(m.imu_head);
      stream.next(m.imu_body);
      stream.next(m.kinematic_joints);
      stream.next(m.light);
      stream.next(m.odom);
      stream.next(m.sonar);
      stream.next(m.stream);
      stream.next(m.touch_body);
      stream.next(m.touch_head);
      stream.next(m.wheel_speed_cmd);
      stream.next(m.wheel_speed_back_emf);
      stream.next(m.wheel_speed_opto);
      stream.next(m.wheel_effort_pwm);
      stream.next(m.body_pose);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct sensors_package_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::miro2_msg::sensors_package_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::miro2_msg::sensors_package_<ContainerAllocator>& v)
  {
    s << indent << "header: ";
    s << std::endl;
    Printer< ::std_msgs::Header_<ContainerAllocator> >::stream(s, indent + "  ", v.header);
    s << indent << "battery: ";
    s << std::endl;
    Printer< ::miro2_msg::BatteryState_<ContainerAllocator> >::stream(s, indent + "  ", v.battery);
    s << indent << "cliff: ";
    s << std::endl;
    Printer< ::std_msgs::Float32MultiArray_<ContainerAllocator> >::stream(s, indent + "  ", v.cliff);
    s << indent << "dip: ";
    s << std::endl;
    Printer< ::std_msgs::UInt16_<ContainerAllocator> >::stream(s, indent + "  ", v.dip);
    s << indent << "flags: ";
    s << std::endl;
    Printer< ::std_msgs::UInt32_<ContainerAllocator> >::stream(s, indent + "  ", v.flags);
    s << indent << "imu_head: ";
    s << std::endl;
    Printer< ::sensor_msgs::Imu_<ContainerAllocator> >::stream(s, indent + "  ", v.imu_head);
    s << indent << "imu_body: ";
    s << std::endl;
    Printer< ::sensor_msgs::Imu_<ContainerAllocator> >::stream(s, indent + "  ", v.imu_body);
    s << indent << "kinematic_joints: ";
    s << std::endl;
    Printer< ::sensor_msgs::JointState_<ContainerAllocator> >::stream(s, indent + "  ", v.kinematic_joints);
    s << indent << "light: ";
    s << std::endl;
    Printer< ::std_msgs::Float32MultiArray_<ContainerAllocator> >::stream(s, indent + "  ", v.light);
    s << indent << "odom: ";
    s << std::endl;
    Printer< ::nav_msgs::Odometry_<ContainerAllocator> >::stream(s, indent + "  ", v.odom);
    s << indent << "sonar: ";
    s << std::endl;
    Printer< ::sensor_msgs::Range_<ContainerAllocator> >::stream(s, indent + "  ", v.sonar);
    s << indent << "stream: ";
    s << std::endl;
    Printer< ::std_msgs::UInt16MultiArray_<ContainerAllocator> >::stream(s, indent + "  ", v.stream);
    s << indent << "touch_body: ";
    s << std::endl;
    Printer< ::std_msgs::UInt16_<ContainerAllocator> >::stream(s, indent + "  ", v.touch_body);
    s << indent << "touch_head: ";
    s << std::endl;
    Printer< ::std_msgs::UInt16_<ContainerAllocator> >::stream(s, indent + "  ", v.touch_head);
    s << indent << "wheel_speed_cmd: ";
    s << std::endl;
    Printer< ::std_msgs::Float32MultiArray_<ContainerAllocator> >::stream(s, indent + "  ", v.wheel_speed_cmd);
    s << indent << "wheel_speed_back_emf: ";
    s << std::endl;
    Printer< ::std_msgs::Float32MultiArray_<ContainerAllocator> >::stream(s, indent + "  ", v.wheel_speed_back_emf);
    s << indent << "wheel_speed_opto: ";
    s << std::endl;
    Printer< ::std_msgs::Float32MultiArray_<ContainerAllocator> >::stream(s, indent + "  ", v.wheel_speed_opto);
    s << indent << "wheel_effort_pwm: ";
    s << std::endl;
    Printer< ::std_msgs::Float32MultiArray_<ContainerAllocator> >::stream(s, indent + "  ", v.wheel_effort_pwm);
    s << indent << "body_pose: ";
    s << std::endl;
    Printer< ::geometry_msgs::Pose2D_<ContainerAllocator> >::stream(s, indent + "  ", v.body_pose);
  }
};

} // namespace message_operations
} // namespace ros

#endif // MIRO2_MSG_MESSAGE_SENSORS_PACKAGE_H