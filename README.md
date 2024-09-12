Overview

The IPSEC Peer Script is a custom bash shell script designed to manage and monitor IPsec peer connections. It provides essential functionalities such as starting, stopping, and checking the status of an IPsec peer-checking process (ipsec_peer_check.py). 

This script is useful for automating IPsec connection management in environments that rely on secure VPN tunnels, ensuring that peers are monitored and that status changes can be logged and acted upon.

Features
	
 	1. Start: Launches the IPsec peer-checking process and monitors its PID.
	2. Stop: Gracefully terminates the IPsec peer-checking process.
	3. Status: Checks if the IPsec peer-checking process is currently running.
	4. Restart: Restarts the process by stopping and starting it again.
	5. Logging: Logs the status of the process to the system daemon log.

Requirements

	1. Bash shell (tested on sh and bash)
	2. IPSec peer-checking script (ipsec_peer_check.py)
	3. Utilities: pgrep (for process management), kill (for process termination), and logger (for system logging)

Installation

1. Upload [files] into a folder on the pfSense firewall
2. Ensure the ipsec_peer_check.py script is placed in /usr/local/sbin/ or update the command path in the script to match the correct location of your Python script.
3. Ensure the ipsec_peer_check.py script is placed in /usr/local/sbin/ or update the command path in the script to match the correct location of your Python script.
