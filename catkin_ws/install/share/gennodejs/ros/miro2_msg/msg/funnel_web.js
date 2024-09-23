// Auto-generated. Do not edit!

// (in-package miro2_msg.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let img_annotation = require('./img_annotation.js');

//-----------------------------------------------------------

class funnel_web {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.cliff = null;
      this.light = null;
      this.sonar = null;
      this.touch = null;
      this.illum = null;
      this.audio_level = null;
      this.tones = null;
      this.img_ann = null;
    }
    else {
      if (initObj.hasOwnProperty('cliff')) {
        this.cliff = initObj.cliff
      }
      else {
        this.cliff = new Array(2).fill(0);
      }
      if (initObj.hasOwnProperty('light')) {
        this.light = initObj.light
      }
      else {
        this.light = new Array(4).fill(0);
      }
      if (initObj.hasOwnProperty('sonar')) {
        this.sonar = initObj.sonar
      }
      else {
        this.sonar = 0.0;
      }
      if (initObj.hasOwnProperty('touch')) {
        this.touch = initObj.touch
      }
      else {
        this.touch = new Array(2).fill(0);
      }
      if (initObj.hasOwnProperty('illum')) {
        this.illum = initObj.illum
      }
      else {
        this.illum = new Array(6).fill(0);
      }
      if (initObj.hasOwnProperty('audio_level')) {
        this.audio_level = initObj.audio_level
      }
      else {
        this.audio_level = 0.0;
      }
      if (initObj.hasOwnProperty('tones')) {
        this.tones = initObj.tones
      }
      else {
        this.tones = [];
      }
      if (initObj.hasOwnProperty('img_ann')) {
        this.img_ann = initObj.img_ann
      }
      else {
        this.img_ann = new img_annotation();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type funnel_web
    // Check that the constant length array field [cliff] has the right length
    if (obj.cliff.length !== 2) {
      throw new Error('Unable to serialize array field cliff - length must be 2')
    }
    // Serialize message field [cliff]
    bufferOffset = _arraySerializer.float32(obj.cliff, buffer, bufferOffset, 2);
    // Check that the constant length array field [light] has the right length
    if (obj.light.length !== 4) {
      throw new Error('Unable to serialize array field light - length must be 4')
    }
    // Serialize message field [light]
    bufferOffset = _arraySerializer.float32(obj.light, buffer, bufferOffset, 4);
    // Serialize message field [sonar]
    bufferOffset = _serializer.float32(obj.sonar, buffer, bufferOffset);
    // Check that the constant length array field [touch] has the right length
    if (obj.touch.length !== 2) {
      throw new Error('Unable to serialize array field touch - length must be 2')
    }
    // Serialize message field [touch]
    bufferOffset = _arraySerializer.uint16(obj.touch, buffer, bufferOffset, 2);
    // Check that the constant length array field [illum] has the right length
    if (obj.illum.length !== 6) {
      throw new Error('Unable to serialize array field illum - length must be 6')
    }
    // Serialize message field [illum]
    bufferOffset = _arraySerializer.uint32(obj.illum, buffer, bufferOffset, 6);
    // Serialize message field [audio_level]
    bufferOffset = _serializer.float32(obj.audio_level, buffer, bufferOffset);
    // Serialize message field [tones]
    bufferOffset = _arraySerializer.uint16(obj.tones, buffer, bufferOffset, null);
    // Serialize message field [img_ann]
    bufferOffset = img_annotation.serialize(obj.img_ann, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type funnel_web
    let len;
    let data = new funnel_web(null);
    // Deserialize message field [cliff]
    data.cliff = _arrayDeserializer.float32(buffer, bufferOffset, 2)
    // Deserialize message field [light]
    data.light = _arrayDeserializer.float32(buffer, bufferOffset, 4)
    // Deserialize message field [sonar]
    data.sonar = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [touch]
    data.touch = _arrayDeserializer.uint16(buffer, bufferOffset, 2)
    // Deserialize message field [illum]
    data.illum = _arrayDeserializer.uint32(buffer, bufferOffset, 6)
    // Deserialize message field [audio_level]
    data.audio_level = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [tones]
    data.tones = _arrayDeserializer.uint16(buffer, bufferOffset, null)
    // Deserialize message field [img_ann]
    data.img_ann = img_annotation.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 2 * object.tones.length;
    length += img_annotation.getMessageSize(object.img_ann);
    return length + 64;
  }

  static datatype() {
    // Returns string type for a message object
    return 'miro2_msg/funnel_web';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '76a57687660541f43a46784ba4f65383';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
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
    # dim[0].label  = "height"
    # dim[0].size   = 480
    # dim[0].stride = 3*640*480 = 921600  (note dim[0] stride is just size of image)
    # dim[1].label  = "width"
    # dim[1].size   = 640
    # dim[1].stride = 3*640 = 1920
    # dim[2].label  = "channel"
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new funnel_web(null);
    if (msg.cliff !== undefined) {
      resolved.cliff = msg.cliff;
    }
    else {
      resolved.cliff = new Array(2).fill(0)
    }

    if (msg.light !== undefined) {
      resolved.light = msg.light;
    }
    else {
      resolved.light = new Array(4).fill(0)
    }

    if (msg.sonar !== undefined) {
      resolved.sonar = msg.sonar;
    }
    else {
      resolved.sonar = 0.0
    }

    if (msg.touch !== undefined) {
      resolved.touch = msg.touch;
    }
    else {
      resolved.touch = new Array(2).fill(0)
    }

    if (msg.illum !== undefined) {
      resolved.illum = msg.illum;
    }
    else {
      resolved.illum = new Array(6).fill(0)
    }

    if (msg.audio_level !== undefined) {
      resolved.audio_level = msg.audio_level;
    }
    else {
      resolved.audio_level = 0.0
    }

    if (msg.tones !== undefined) {
      resolved.tones = msg.tones;
    }
    else {
      resolved.tones = []
    }

    if (msg.img_ann !== undefined) {
      resolved.img_ann = img_annotation.Resolve(msg.img_ann)
    }
    else {
      resolved.img_ann = new img_annotation()
    }

    return resolved;
    }
};

module.exports = funnel_web;
