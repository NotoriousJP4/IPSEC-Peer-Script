#!/bin/sh

# Define the python script name and location
py_script = "ipsec-peer-script.py"
command = "/root/ipsec-peer-script/${py_script}"

rc_start() {
    # Start IPSEC Peer Script in the background (&)
    "${command}" &

    # Define the PID number (-f tells it to match against the entire command line)
    # **The PID = the output of the command "pgrep -f ipsec-peer-script.py"**
    # The executable "pgrep" is found in the bin (binaries) folder
    pid = "$(/bin/pgrep -f $py_script)"
    if [ -n "${pid}" ]; then
        echo "IPSEC Peer Script started. PID: (${pid})"
        /usr/bin/logger -p daemon.info -t ipsec-peer-script "IPSEC Peer Script started"

    else
        echo "IPSEC Peer Script failed to start"
        /usr/bin/logger -p daemon.info -t ipsec-peer-script "IPSEC Peer Script failed to start"
    fi

}

rc_stop() {

    pid = "$(/bin/pgrep -f $py_script)"
    if [ -n "${pid}" ]; then
        /bin/kill $pid
        echo "IPSEC Peer Scipt stopped. PID: (${pid})"
        /usr/bin/logger -p daemon.info -t ipsec-peer-script "IPSEC Peer Script stopped"
    fi

}


rc_status() {	
	# Check status and print pid if running
	pid="$(/bin/pgrep -f $py_script)"
	if [ -n "${pid}" ]; then
		echo "IPSEC Peer Script is running (${pid})"
	else
		echo "IPSEC Peer Script is not running"
	fi
}

if [ $# -eq 0 ]; then
	echo "No parameter specified - starting IPSEC Peer Script"
	rc_start
	exit
fi

case $1 in
	start)
		rc_start
		;;
	stop)
		rc_stop
		;;
	restart)
		rc_stop
		rc_start
		;;
	status)
		rc_status
		;;
esac
