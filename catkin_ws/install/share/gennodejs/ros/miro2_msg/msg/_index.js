
"use strict";

let object_ball = require('./object_ball.js');
let BatteryState = require('./BatteryState.js');
let animal_state = require('./animal_state.js');
let adjust = require('./adjust.js');
let animal_adjust = require('./animal_adjust.js');
let sleep_adjust = require('./sleep_adjust.js');
let sensors_package = require('./sensors_package.js');
let objects = require('./objects.js');
let funnel_web = require('./funnel_web.js');
let sleep = require('./sleep.js');
let object_face = require('./object_face.js');
let img_annotation = require('./img_annotation.js');
let affect_adjust = require('./affect_adjust.js');
let object_tag = require('./object_tag.js');
let voice_state = require('./voice_state.js');
let push = require('./push.js');
let priority_peak = require('./priority_peak.js');
let affect = require('./affect.js');

module.exports = {
  object_ball: object_ball,
  BatteryState: BatteryState,
  animal_state: animal_state,
  adjust: adjust,
  animal_adjust: animal_adjust,
  sleep_adjust: sleep_adjust,
  sensors_package: sensors_package,
  objects: objects,
  funnel_web: funnel_web,
  sleep: sleep,
  object_face: object_face,
  img_annotation: img_annotation,
  affect_adjust: affect_adjust,
  object_tag: object_tag,
  voice_state: voice_state,
  push: push,
  priority_peak: priority_peak,
  affect: affect,
};
