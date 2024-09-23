#!/bin/bash

# _setup_util.py will have a hard-coded local path ($HOME/mdk/catkin_ws/install)
# if we didn't clean up properly before the build; this isn't needed.
#
# it will also have opt/ros/noetic hard-coded, which won't work if we run the
# built package on a non-noetic system.
#
# so, we just replace the whole line with one that uses the local ROS.
TGT=install/_setup_util.py
TMP=/tmp/_setup_util.py
cat $TGT | sed "s|CMAKE_PREFIX_PATH = r'.*|CMAKE_PREFIX_PATH = ('/opt/ros/' + os.getenv('MIRO_ROS_RELEASE')).split(';')|" > $TMP
cp $TMP $TGT
rm $TMP

# at genpy #127, a line was added that is not compatible with kinetic:
# https://github.com/ros/genpy/issues/132
#
# at least, not unless kinetic is updated. we can't update kinetic on the robot
# easily, and the discussion at that issue says that the line is not needed if
# running kinetic, the default will do the right thing, so we just add a check
# and only run the offending lines on Python3. that isn't exactly the right
# check, but it will probably do.
#
# NB: The 'python3' directory is used by python2, because it's on the path, and
# apart from this issue, that's fine. so we don't need to provide a separate
# python2 tree.
#
# NB: If there /is no/ python3 directory, then we are building on python2.7 and
# don't have to do anything
if [[ -d "install/lib/python3" ]]
then
    cd install/lib/python3/dist-packages/miro2_msg/msg
    for TGT in *.py; do
	    TMP=/tmp/$TGT
	    cat $TGT | sed "s|^\( *\)codecs.lookup_error(|\1if sys.version_info >= (3,0): codecs.lookup_error(|g" > $TMP
	    cp $TMP $TGT
	    rm $TMP
    done
fi

