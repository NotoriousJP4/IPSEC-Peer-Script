#!/bin/sh

# Define locations and names of the python and shell scripts needed
py_script="ipsec_peer_script.py"
shell_script="/etc/rc.d/ipsec-peer-script.sh"

# Check if the python script is running. If not, attempt to start the service and creates
# an error log in /usr/bin/logger under the daemon facility and info is the priority level 
# (informational message)
if [ ! pgrep -f $py_script >/dev/null ]; then
    /usr/bin/logger -p daemon.info -t ipsec-peer-check "${py_script} is not running, starting now."
    "$shell_script" start

    if [ $? -ne 0]; then
        /usr/bin/logger -p daemon.info -t ipsec-peer-check "${py_script} failed to start, exiting."
        exit 1
    fi 
fi



