#!/bin/bash
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

# caller can skip slow parts if desired
if [[ "$MIRO_SETUP_QUICK" == "" ]];
then

	# report
	if [ "$MIRO_SETUP_SILENT" == "" ];
	then
		echo -e "________________________________________________________________\n"
		echo -e "Sourcing mdk/setup.bash...\n"
	fi

fi

# error function
miro_config_error()
{
	echo
	echo -e "**** CONFIGURATION ERROR:"
	echo -e "     $1"
	echo
}

# warn function
miro_warn()
{
	echo -e "\t**** WARNING **** $1"
}

# MDK info function
miro_info()
{
	echo
	echo -e "[ MIRO ]"
	env | grep MIRO_ | sed 's/\(MIRO_WIFI_PASS=\).*/\1********/' | sort | sed s!$HOME!~!g
	echo -e "\n[ ROS ]"
	env | grep ROS | grep -v UNKNOWN | sed s!$HOME!~!g
	env | grep GAZEBO | grep -v UNKNOWN | sed s!$HOME!~!g
	env | grep PYTHON | grep -v UNKNOWN | sed s!$HOME!~!g
	echo -e "\n[ ROBOT ]"
	mm -info 2> /dev/null
	echo
}

# auto network address recovery function
miro_get_dynamic_address()
{
	# temp file
	TMP=/tmp/ifconfig.mdk

	# automatic recovery uses output of ifconfig. on many systems,
	# no further information is required, but on systems with multiple
	# adapters, user may need to specify the one they want to use else
	# the first in the list will be hit. note that a partial name will
	# also work, so e.g. "wlx" is useful on some Linux systems.
	if [[ "$MIRO_ADAPTER_NAME" == "" ]];
	then
		/sbin/ifconfig > $TMP
	else
		/sbin/ifconfig | grep $MIRO_ADAPTER_NAME -A 2 > $TMP
	fi

	# recover address from output of ifconfig
	MIRO_DYNAMIC_IP=`cat $TMP | grep inet | grep -v inet6 | grep -v 127.0.0.1 | head -n 1 | sed 's/[^0-9]*//' | sed 's/\ .*//'`

	# clear temp file
	rm $TMP
}

# network address resolution function
miro_resolve_network_address()
{
	# explicit
	[[ "$MIRO_LOCAL_IP" != "" ]] && { MIRO_LOCAL_IP_SRC="set from MIRO_LOCAL_IP"; return; }

	# static
	[[ "$MIRO_NETWORK_MODE" == "static" ]] && { MIRO_LOCAL_IP_SRC="set from MIRO_STATIC_IP"; MIRO_LOCAL_IP=$MIRO_STATIC_IP; }

	# dynamic
	[[ "$MIRO_NETWORK_MODE" == "dynamic" ]] && { miro_get_dynamic_address; MIRO_LOCAL_IP_SRC="set from miro_get_dynamic_address()"; MIRO_LOCAL_IP=$MIRO_DYNAMIC_IP; }

	# loopback
	[[ "$MIRO_NETWORK_MODE" == "loopback" ]] && { MIRO_LOCAL_IP_SRC="set to loopback"; MIRO_LOCAL_IP=127.0.0.1; }

	# resolve to something in case no network was available
	if [[ "$1" == "resolve" ]];
	then
		[[ "$MIRO_LOCAL_IP" == "" ]] && { MIRO_LOCAL_IP_SRC="network address not available, using loopback"; MIRO_LOCAL_IP=127.0.0.1; miro_warn "$MIRO_LOCAL_IP_SRC"; }
	fi
}

# identify system
UNAME=$(uname -m)
if [ "$UNAME" = "x86_64" ]; then
	export MIRO_SYSTEM=deb64
elif [ "$UNAME" = "i386" ]; then
	export MIRO_SYSTEM=deb32
elif [ "$UNAME" = "i686" ]; then
	export MIRO_SYSTEM=deb32
elif [ "$UNAME" = "armv7l" ]; then
	export MIRO_SYSTEM=arm32
elif [ "$UNAME" = "aarch64" ]; then
	export MIRO_SYSTEM=arm64
fi

# check we got something
[[ "$MIRO_SYSTEM" == "" ]] && { miro_config_error "system unrecognised: $UNAME"; return; }

# get mdk dirs
export MIRO_DIR_MDK="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd )"
export MIRO_DIR_SHARE=$MIRO_DIR_MDK/share
export MIRO_DIR_BIN=$MIRO_DIR_MDK/bin/$MIRO_SYSTEM
export MIRO_DIR_ONBOARD=$MIRO_DIR_MDK/bin/onboard

# localise
if [[ -f "/etc/miro" ]]; then
	# onboard >= miro3 has /etc/miro
	export MIRO_ON_ROBOT=1
	export MIRO_USER=$(cat /etc/miro | grep user | sed 's/.* //')
	export MIRO_EDITION=$(cat /etc/miro | grep edition | sed 's/.* //')
elif [[ "$(cat /etc/hostname)" == "miropi" && -d "/home/miro/channel" ]]; then
	# onboard == miro2 is detected using these heuristics which are
	# unlikely to be hit on a user's workstation; we use known defaults
	export MIRO_ON_ROBOT=1
	export MIRO_USER=miro
	export MIRO_EDITION=2
else
	# otherwise we are on a workstation
	export MIRO_ON_ROBOT=
	export MIRO_USER=$USER

	# and can ask the MDK which edition it is (the file "EDITION" is
	# added during the create_release process, depending on the target)
	if [[ -f "$MIRO_DIR_MDK/EDITION" ]]; then
		export MIRO_EDITION=$(cat $MIRO_DIR_MDK/EDITION)
	else
		# early editions of offboard == miro2 do not have EDITION
		export MIRO_EDITION=2
	fi
fi

# check
[[ "$MIRO_USER" == "" || "$MIRO_EDITION" == "" ]] && { miro_config_error "unable to determine MIRO edition"; return; }

# get miro token
export MIRO_TOKEN=miro$MIRO_EDITION

# get user dirs
export MIRO_DIR_USER=~/.$MIRO_TOKEN
export MIRO_DIR_CONFIG=$MIRO_DIR_USER/config
export MIRO_DIR_TRASH=$MIRO_DIR_USER/trash

# get tmp dirs
export MIRO_DIR_TMP=/tmp/$MIRO_TOKEN
export MIRO_DIR_LOG=$MIRO_DIR_TMP/log
export MIRO_DIR_PID=$MIRO_DIR_TMP/pid
export MIRO_DIR_DUMP=$MIRO_DIR_TMP/dump

# get multitool
export MIRO_MULTITOOL=$MIRO_DIR_ONBOARD/multitool.sh

# determine state directory and ensure it exists
if [[ "$MIRO_ON_ROBOT" == "1" ]]; then
	if [[ "$MIRO_EDITION" == "2" ]]; then
		export MIRO_DIR_STATE=$XDG_RUNTIME_DIR/$MIRO_TOKEN/state
	else
		export MIRO_DIR_STATE=/run/$MIRO_TOKEN
		# must create it here because it needs elevation
		[[ ! -d "$MIRO_DIR_STATE" ]] && mm create_dir_state
	fi
else
	# on workstation, use XDG if available, else use /tmp
	DIR_STATE_PARENT=$XDG_RUNTIME_DIR
	[[ ! -d "$DIR_STATE_PARENT" ]] && DIR_STATE_PARENT=/tmp
	export MIRO_DIR_STATE=$DIR_STATE_PARENT/$MIRO_TOKEN/state
fi

# check dirs exist
[ -d "$MIRO_DIR_BIN" ] || { miro_config_error "failed to find MDK bin directory for this system"; return; }

# ensure dirs exist
mkdir -p "$MIRO_DIR_CONFIG" "$MIRO_DIR_TRASH" "$MIRO_DIR_LOG" "$MIRO_DIR_PID" "$MIRO_DIR_DUMP" "$MIRO_DIR_STATE"

# configure node to use .local
export NODE_PATH=$NODE_PATH:~/.local/npm/lib/node_modules

# caller can skip slow parts if desired
if [[ "$MIRO_SETUP_QUICK" == "" ]];
then

	# locate user setup file if there is one, else select default
	export MIRO_USER_SETUP=$MIRO_DIR_CONFIG/user_setup.bash
	if [ -e "$MIRO_USER_SETUP" ];
	then
		# if present, source default one first to ensure all settings
		# are loaded, even ones that are new and not in the user file
		source $MIRO_DIR_SHARE/config/user_setup.bash
	else
		MIRO_USER_SETUP=$MIRO_DIR_SHARE/config/user_setup.bash
	fi

	# load that file
	source $MIRO_USER_SETUP || { miro_config_error "failed to source user_setup.bash"; }

	# determine robot address
	if [[ "$MIRO_ROBOT_IP" == "" ]];
	then
		MIRO_ROBOT_IP_SRC="not set"
	else
		MIRO_ROBOT_IP_SRC="set explicitly"
	fi

	# determine local address
	miro_resolve_network_address resolve
	export ROS_IP=$MIRO_LOCAL_IP

	# determine master address
	if [[ "$ROS_MASTER_IP" == "" ]];
	then
		if [[ "$MIRO_ROBOT_IP" != "" ]];
		then
			export ROS_MASTER_IP=$MIRO_ROBOT_IP
			ROS_MASTER_IP_SRC="set from MIRO_ROBOT_IP"
		else
			export ROS_MASTER_IP=localhost
			ROS_MASTER_IP_SRC="not set, assumed running locally"
		fi
	else
		ROS_MASTER_IP_SRC="set explicitly"
	fi
	export ROS_MASTER_URI=http://$ROS_MASTER_IP:11311

	# source ROS setup
	source /opt/ros/$MIRO_ROS_RELEASE/setup.bash || { miro_config_error "failed to source ROS setup.bash"; }

	# python version to use with ROS
	export MIRO_ROS_PYTHON='python' && [[ "$ROS_PYTHON_VERSION" == "3" ]] && MIRO_ROS_PYTHON='python3'

	# source Gazebo setup, if installed
	if [[ -f "/usr/share/gazebo/setup.sh" ]];
	then
		source /usr/share/gazebo/setup.sh
	fi

	# source catkin workspace setup
	CATKIN_INSTALL=install
	CATKIN_SETUP=$MIRO_DIR_MDK/catkin_ws/$CATKIN_INSTALL/setup.bash
	if [ -f "$CATKIN_SETUP" ];
	then
		source $CATKIN_SETUP || { miro_config_error "failed to source catkin setup.bash"; }
	else
		miro_config_error "catkin_ws has not yet been built on this machine - did you install_mdk.sh?"
	fi

	# add path to python share
	TMP=$MIRO_DIR_SHARE/python
	[[ ":$PYTHONPATH:" != *":$TMP:"* ]] && PYTHONPATH=$TMP:$PYTHONPATH

	# make packages available to third-party software
	TMP=$MIRO_DIR_MDK/sim
	[[ ":$GAZEBO_RESOURCE_PATH:" != *":$TMP:"* ]] && GAZEBO_RESOURCE_PATH=$TMP:$GAZEBO_RESOURCE_PATH
	TMP=$MIRO_DIR_MDK/sim/models
	[[ ":$GAZEBO_MODEL_PATH:" != *":$TMP:"* ]] && GAZEBO_MODEL_PATH=$TMP:$GAZEBO_MODEL_PATH
	TMP=$MIRO_DIR_BIN
	[[ ":$GAZEBO_PLUGIN_PATH:" != *":$TMP:"* ]] && GAZEBO_PLUGIN_PATH=$TMP:$GAZEBO_PLUGIN_PATH

	# read MDK release
	export MIRO_MDK_RELEASE=$(cat $MIRO_DIR_MDK/RELEASE)
	[ "$MIRO_MDK_RELEASE" != "" ] || { miro_config_error "failed to read MDK release file"; return; }

	# report
	if [ "$MIRO_SETUP_SILENT" == "" ];
	then
		echo MIRO user: $MIRO_USER
		echo MIRO edition: $MIRO_EDITION
		echo MDK path: $MIRO_DIR_MDK
		echo MDK release: $MIRO_MDK_RELEASE
		echo User setup: $MIRO_USER_SETUP
		echo State directory: $MIRO_DIR_STATE
		echo ROS version: $MIRO_ROS_RELEASE \($MIRO_ROS_PYTHON\)
		echo
		echo -e "Local network address: $MIRO_LOCAL_IP ($MIRO_LOCAL_IP_SRC)"
		echo -e "Robot network address: $MIRO_ROBOT_IP ($MIRO_ROBOT_IP_SRC)"
		echo -e "ROS master address: $ROS_MASTER_URI ($ROS_MASTER_IP_SRC)"
		echo
		echo -e "Type \"miro_info\" to see your environment"
		echo -e "________________________________________________________________\n"
	fi

fi




