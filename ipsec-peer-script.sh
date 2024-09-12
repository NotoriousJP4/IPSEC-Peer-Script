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
        echo "IPSEC Peer Script started. PID # is (${pid})"
        
        
    



}