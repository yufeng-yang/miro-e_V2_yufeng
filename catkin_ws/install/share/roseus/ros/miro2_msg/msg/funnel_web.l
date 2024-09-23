;; Auto-generated. Do not edit!


(when (boundp 'miro2_msg::funnel_web)
  (if (not (find-package "MIRO2_MSG"))
    (make-package "MIRO2_MSG"))
  (shadow 'funnel_web (find-package "MIRO2_MSG")))
(unless (find-package "MIRO2_MSG::FUNNEL_WEB")
  (make-package "MIRO2_MSG::FUNNEL_WEB"))

(in-package "ROS")
;;//! \htmlinclude funnel_web.msg.html


(defclass miro2_msg::funnel_web
  :super ros::object
  :slots (_cliff _light _sonar _touch _illum _audio_level _tones _img_ann ))

(defmethod miro2_msg::funnel_web
  (:init
   (&key
    ((:cliff __cliff) (make-array 2 :initial-element 0.0 :element-type :float))
    ((:light __light) (make-array 4 :initial-element 0.0 :element-type :float))
    ((:sonar __sonar) 0.0)
    ((:touch __touch) (make-array 2 :initial-element 0 :element-type :integer))
    ((:illum __illum) (make-array 6 :initial-element 0 :element-type :integer))
    ((:audio_level __audio_level) 0.0)
    ((:tones __tones) (make-array 0 :initial-element 0 :element-type :integer))
    ((:img_ann __img_ann) (instance miro2_msg::img_annotation :init))
    )
   (send-super :init)
   (setq _cliff __cliff)
   (setq _light __light)
   (setq _sonar (float __sonar))
   (setq _touch __touch)
   (setq _illum __illum)
   (setq _audio_level (float __audio_level))
   (setq _tones __tones)
   (setq _img_ann __img_ann)
   self)
  (:cliff
   (&optional __cliff)
   (if __cliff (setq _cliff __cliff)) _cliff)
  (:light
   (&optional __light)
   (if __light (setq _light __light)) _light)
  (:sonar
   (&optional __sonar)
   (if __sonar (setq _sonar __sonar)) _sonar)
  (:touch
   (&optional __touch)
   (if __touch (setq _touch __touch)) _touch)
  (:illum
   (&optional __illum)
   (if __illum (setq _illum __illum)) _illum)
  (:audio_level
   (&optional __audio_level)
   (if __audio_level (setq _audio_level __audio_level)) _audio_level)
  (:tones
   (&optional __tones)
   (if __tones (setq _tones __tones)) _tones)
  (:img_ann
   (&rest __img_ann)
   (if (keywordp (car __img_ann))
       (send* _img_ann __img_ann)
     (progn
       (if __img_ann (setq _img_ann (car __img_ann)))
       _img_ann)))
  (:serialization-length
   ()
   (+
    ;; float32[2] _cliff
    (* 4    2)
    ;; float32[4] _light
    (* 4    4)
    ;; float32 _sonar
    4
    ;; uint16[2] _touch
    (* 2    2)
    ;; uint32[6] _illum
    (* 4    6)
    ;; float32 _audio_level
    4
    ;; uint16[] _tones
    (* 2    (length _tones)) 4
    ;; miro2_msg/img_annotation _img_ann
    (send _img_ann :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32[2] _cliff
     (dotimes (i 2)
       (sys::poke (elt _cliff i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;; float32[4] _light
     (dotimes (i 4)
       (sys::poke (elt _light i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;; float32 _sonar
       (sys::poke _sonar (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; uint16[2] _touch
     (dotimes (i 2)
       (write-word (elt _touch i) s)
       )
     ;; uint32[6] _illum
     (dotimes (i 6)
       (write-long (elt _illum i) s)
       )
     ;; float32 _audio_level
       (sys::poke _audio_level (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; uint16[] _tones
     (write-long (length _tones) s)
     (dotimes (i (length _tones))
       (write-word (elt _tones i) s)
       )
     ;; miro2_msg/img_annotation _img_ann
       (send _img_ann :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32[2] _cliff
   (dotimes (i (length _cliff))
     (setf (elt _cliff i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     )
   ;; float32[4] _light
   (dotimes (i (length _light))
     (setf (elt _light i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     )
   ;; float32 _sonar
     (setq _sonar (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; uint16[2] _touch
   (dotimes (i (length _touch))
     (setf (elt _touch i) (sys::peek buf ptr- :short)) (incf ptr- 2)
     )
   ;; uint32[6] _illum
   (dotimes (i (length _illum))
     (setf (elt _illum i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     )
   ;; float32 _audio_level
     (setq _audio_level (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; uint16[] _tones
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _tones (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _tones i) (sys::peek buf ptr- :short)) (incf ptr- 2)
     ))
   ;; miro2_msg/img_annotation _img_ann
     (send _img_ann :deserialize buf ptr-) (incf ptr- (send _img_ann :serialization-length))
   ;;
   self)
  )

(setf (get miro2_msg::funnel_web :md5sum-) "76a57687660541f43a46784ba4f65383")
(setf (get miro2_msg::funnel_web :datatype-) "miro2_msg/funnel_web")
(setf (get miro2_msg::funnel_web :definition-)
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
#	This message packages several messages for simple
#	delivery to the web client.



float32[2] cliff
float32[4] light
float32 sonar
uint16[2] touch
uint32[6] illum
float32 audio_level
uint16[] tones
img_annotation img_ann

================================================================================
MSG: miro2_msg/img_annotation
#	@section COPYRIGHT
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



(provide :miro2_msg/funnel_web "76a57687660541f43a46784ba4f65383")


