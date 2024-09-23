
# this target makes the catkin workspace, and does
# it silently so it can be used in the makefile
# without making too much mess
default :
	@echo making catkin workspace...
	@catkin_make install > /dev/null
	@./apply_local_fixes.sh

clean :
	rm -rf build devel install
