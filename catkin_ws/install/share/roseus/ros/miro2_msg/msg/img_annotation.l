;; Auto-generated. Do not edit!


(when (boundp 'miro2_msg::img_annotation)
  (if (not (find-package "MIRO2_MSG"))
    (make-package "MIRO2_MSG"))
  (shadow 'img_annotation (find-package "MIRO2_MSG")))
(unless (find-package "MIRO2_MSG::IMG_ANNOTATION")
  (make-package "MIRO2_MSG::IMG_ANNOTATION"))

(in-package "ROS")
;;//! \htmlinclude img_annotation.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass miro2_msg::img_annotation
  :super ros::object
  :slots (_header _type _cam _centre _vertices _size _area _id _distance ))

(defmethod miro2_msg::img_annotation
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:type __type) (instance std_msgs::String :init))
    ((:cam __cam) (instance std_msgs::String :init))
    ((:centre __centre) (instance std_msgs::Float32MultiArray :init))
    ((:vertices __vertices) (instance std_msgs::Float32MultiArray :init))
    ((:size __size) (instance std_msgs::Float32 :init))
    ((:area __area) (instance std_msgs::Float32 :init))
    ((:id __id) (instance std_msgs::UInt8 :init))
    ((:distance __distance) (instance std_msgs::Float32 :init))
    )
   (send-super :init)
   (setq _header __header)
   (setq _type __type)
   (setq _cam __cam)
   (setq _centre __centre)
   (setq _vertices __vertices)
   (setq _size __size)
   (setq _area __area)
   (setq _id __id)
   (setq _distance __distance)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:type
   (&rest __type)
   (if (keywordp (car __type))
       (send* _type __type)
     (progn
       (if __type (setq _type (car __type)))
       _type)))
  (:cam
   (&rest __cam)
   (if (keywordp (car __cam))
       (send* _cam __cam)
     (progn
       (if __cam (setq _cam (car __cam)))
       _cam)))
  (:centre
   (&rest __centre)
   (if (keywordp (car __centre))
       (send* _centre __centre)
     (progn
       (if __centre (setq _centre (car __centre)))
       _centre)))
  (:vertices
   (&rest __vertices)
   (if (keywordp (car __vertices))
       (send* _vertices __vertices)
     (progn
       (if __vertices (setq _vertices (car __vertices)))
       _vertices)))
  (:size
   (&rest __size)
   (if (keywordp (car __size))
       (send* _size __size)
     (progn
       (if __size (setq _size (car __size)))
       _size)))
  (:area
   (&rest __area)
   (if (keywordp (car __area))
       (send* _area __area)
     (progn
       (if __area (setq _area (car __area)))
       _area)))
  (:id
   (&rest __id)
   (if (keywordp (car __id))
       (send* _id __id)
     (progn
       (if __id (setq _id (car __id)))
       _id)))
  (:distance
   (&rest __distance)
   (if (keywordp (car __distance))
       (send* _distance __distance)
     (progn
       (if __distance (setq _distance (car __distance)))
       _distance)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; std_msgs/String _type
    (send _type :serialization-length)
    ;; std_msgs/String _cam
    (send _cam :serialization-length)
    ;; std_msgs/Float32MultiArray _centre
    (send _centre :serialization-length)
    ;; std_msgs/Float32MultiArray _vertices
    (send _vertices :serialization-length)
    ;; std_msgs/Float32 _size
    (send _size :serialization-length)
    ;; std_msgs/Float32 _area
    (send _area :serialization-length)
    ;; std_msgs/UInt8 _id
    (send _id :serialization-length)
    ;; std_msgs/Float32 _distance
    (send _distance :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; std_msgs/String _type
       (send _type :serialize s)
     ;; std_msgs/String _cam
       (send _cam :serialize s)
     ;; std_msgs/Float32MultiArray _centre
       (send _centre :serialize s)
     ;; std_msgs/Float32MultiArray _vertices
       (send _vertices :serialize s)
     ;; std_msgs/Float32 _size
       (send _size :serialize s)
     ;; std_msgs/Float32 _area
       (send _area :serialize s)
     ;; std_msgs/UInt8 _id
       (send _id :serialize s)
     ;; std_msgs/Float32 _distance
       (send _distance :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; std_msgs/String _type
     (send _type :deserialize buf ptr-) (incf ptr- (send _type :serialization-length))
   ;; std_msgs/String _cam
     (send _cam :deserialize buf ptr-) (incf ptr- (send _cam :serialization-length))
   ;; std_msgs/Float32MultiArray _centre
     (send _centre :deserialize buf ptr-) (incf ptr- (send _centre :serialization-length))
   ;; std_msgs/Float32MultiArray _vertices
     (send _vertices :deserialize buf ptr-) (incf ptr- (send _vertices :serialization-length))
   ;; std_msgs/Float32 _size
     (send _size :deserialize buf ptr-) (incf ptr- (send _size :serialization-length))
   ;; std_msgs/Float32 _area
     (send _area :deserialize buf ptr-) (incf ptr- (send _area :serialization-length))
   ;; std_msgs/UInt8 _id
     (send _id :deserialize buf ptr-) (incf ptr- (send _id :serialization-length))
   ;; std_msgs/Float32 _distance
     (send _distance :deserialize buf ptr-) (incf ptr- (send _distance :serialization-length))
   ;;
   self)
  )

(setf (get miro2_msg::img_annotation :md5sum-) "7933292787df9dea2afeb186ff97727a")
(setf (get miro2_msg::img_annotation :datatype-) "miro2_msg/img_annotation")
(setf (get miro2_msg::img_annotation :definition-)
      "#	@section COPYRIGHT
#	Copyright (C) 2023 Consequential Robotics Ltd
#	
#	@section AUTHOR
#	Consequential Robotics http://consequentialrobotics.com
#	
#	@section LICENSE
#	For a full copy of the license agreement, and a complete
#	definition of \"The Software\", see LICENSE in the MDK root
#	directory.
#	
#	Subject to the terms of this Agreement, Consequential
#	Robotics grants to you a limited, non-exclusive, non-
#	transferable license, without right to sub-license, to use
#	\"The Software\" in accordance with this Agreement and any
#	other written agreement with Consequential Robotics.
#	Consequential Robotics does not transfer the title of \"The
#	Software\" to you; the license granted to you is not a sale.
#	This agreement is a binding legal agreement between
#	Consequential Robotics and the purchasers or users of \"The
#	Software\".
#	
#	THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY
#	KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#	WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
#	PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
#	OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
#	OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#	OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#	SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#	
#
#	This message defines all of the required parameters needed to annotate
# the camera images with output from the vision.py library. This is mainly
# used to provide output to mirocode.



#### HEADER

# standard header
std_msgs/Header header



#### CONTENT

std_msgs/String type
std_msgs/String cam
std_msgs/Float32MultiArray centre
std_msgs/Float32MultiArray vertices
std_msgs/Float32 size
std_msgs/Float32 area
std_msgs/UInt8 id
std_msgs/Float32 distance

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: std_msgs/String
string data

================================================================================
MSG: std_msgs/Float32MultiArray
# Please look at the MultiArrayLayout message definition for
# documentation on all multiarrays.

MultiArrayLayout  layout        # specification of data layout
float32[]         data          # array of data


================================================================================
MSG: std_msgs/MultiArrayLayout
# The multiarray declares a generic multi-dimensional array of a
# particular data type.  Dimensions are ordered from outer most
# to inner most.

MultiArrayDimension[] dim # Array of dimension properties
uint32 data_offset        # padding elements at front of data

# Accessors should ALWAYS be written in terms of dimension stride
# and specified outer-most dimension first.
# 
# multiarray(i,j,k) = data[data_offset + dim_stride[1]*i + dim_stride[2]*j + k]
#
# A standard, 3-channel 640x480 image with interleaved color channels
# would be specified as:
#
# dim[0].label  = \"height\"
# dim[0].size   = 480
# dim[0].stride = 3*640*480 = 921600  (note dim[0] stride is just size of image)
# dim[1].label  = \"width\"
# dim[1].size   = 640
# dim[1].stride = 3*640 = 1920
# dim[2].label  = \"channel\"
# dim[2].size   = 3
# dim[2].stride = 3
#
# multiarray(i,j,k) refers to the ith row, jth column, and kth channel.

================================================================================
MSG: std_msgs/MultiArrayDimension
string label   # label of given dimension
uint32 size    # size of given dimension (in type units)
uint32 stride  # stride of given dimension
================================================================================
MSG: std_msgs/Float32
float32 data
================================================================================
MSG: std_msgs/UInt8
uint8 data

")



(provide :miro2_msg/img_annotation "7933292787df9dea2afeb186ff97727a")


