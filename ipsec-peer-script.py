#!/usr/local/bin/python3.11

import os
import configparser
import re
from time import sleep

config_file = "/root/ipsec-peer-script/ipsec-peer-script.cfg"

config = configparser.ConfigParser()
config.read(config_file)

time_wait = config['TIMER']['time_wait']

def get_frr_config():
    # Get the full FRR configuration output
    frr_config = os.popen(f"vtysh -e \"show run\"").read()
    return(frr_config)

def get_local_as():
    # Get the local autonomous system number for this firewall
    frr_config_bgp_as = re.search('router bgp (.+)\n', get_frr_config())
    localAS = frr_config_bgp_as.group(1)
    return(localAS)

def get_frr_bgp_state(peer_ip):
    # Get the top level BGP config section, we use this to check if the primary neighbor is already shutdown
    frr_bgp_config = re.search('router bgp (.*?)!', get_frr_config(), flags=re.S)
    frr_bgp_string = frr_bgp_config.group(1)
    # This is the shutdown string we are looking for
    shutdown_string = f"neighbor {peer_ip} shutdown"

    if shutdown_string in frr_bgp_string:
        # The neighbor is already shutdown, so set the state to 1
        shutdown_state = 1
        return(shutdown_state)
    else:
        # The neighbor is not shutdown, so set the state to 0
        shutdown_state = 0
        return(shutdown_state)

def checkTunnels(config_data):
    tunnelName = config_data[0][1]
    primaryPeer = config_data[1][1]
    secondaryPeer = config_data[2][1]
    primaryPeerState = os.system(f"ping -o -c 3 -W 3000 {primaryPeer}")
    secondaryPeerState = os.system(f"ping -o -c 3 -W 3000 {secondaryPeer}")
    if primaryPeerState == 0:
        
        if get_frr_bgp_state(primaryPeer) == 1:
            # Bring the primary neighbor/peer up
            vtysh_cmd = os.popen(f"vtysh -e \"configure terminal\" -e \"router bgp {get_local_as()}\" -e \"no neighbor {primaryPeer} shutdown\"").read()
        if get_frr_bgp_state(secondaryPeer) == 0:
                # Shutdown the secondary neighbor/peer
                vtysh_cmd = os.popen(f"vtysh -e \"configure terminal\" -e \"router bgp {get_local_as()}\" -e \"neighbor {secondaryPeer} shutdown\"").read()
    elif primaryPeerState != 0 and secondaryPeerState == 0:
        if get_frr_bgp_state(primaryPeer) == 0:
            # Shutdown the primary neighbor/peer
            vtysh_cmd = os.popen(f"vtysh -e \"configure terminal\" -e \"router bgp {get_local_as()}\" -e \"neighbor {primaryPeer} shutdown\"").read()
        if get_frr_bgp_state(secondaryPeer) == 1:
            # Bring the secondary neighbor/peer up
            vtysh_cmd = os.popen(f"vtysh -e \"configure terminal\" -e \"router bgp {get_local_as()}\" -e \"no neighbor {secondaryPeer} shutdown\"").read()
    
while True:
    section_names: list[str] = config.sections()
    for section_name in section_names:
        if re.search(r'^TUNNEL+', section_name):
            config_data = config.items(section_name)
            checkTunnels(config_data)
    sleep(int(time_wait))
