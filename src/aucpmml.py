#! /usr/bin/python3
"""Module for dealing with mirrorlist syncing"""

import os, requests
from pathlib import Path

def get_mrl_url():
    """Opens config and get mirrorlist url"""
    try: # Catch if file does not yet exist
        with open(os.path.expanduser("~/.auc/mirrorlist.conf")) as file:
            lines = file.readlines() # Read in file
            file.close()
        if(len(lines) > 1):
            version = int(lines[0]) # Version check for future changes
            if(version == 1):
                url = lines[1].strip() # Strip newline
                return url
        return "" # Return blank on error
    except FileNotFoundError:
        return "" # Return blank on error

def set_mrl_url(new_url):
    """Save config of mirrorlist url"""
    config_folder = Path(os.path.expanduser("~/.auc/"))
    config_folder.mkdir(parents=True, exist_ok=True) # Ensure folder exists
    file = open(os.path.expanduser("~/.auc/mirrorlist.conf"), 'w')
    file.write('1\n')
    file.write(new_url)
    file.write('\n')
    file.close() # Write settings to file

def update_mrl():
    url = get_mrl_url()
    mrl_req =  requests.get(url)
    config_folder = Path(os.path.expanduser("~/.auc/"))
    config_folder.mkdir(parents=True, exist_ok=True) # Ensure folder exists
    if mrl_req.status_code != requests.codes.ok:
        print("Failed to update mirrorlist")
        return
    file = open(os.path.expanduser("~/.auc/mirrorlist.tmp"), 'w')
    file.write(mrl_req.text.replace('#S', 'S')) # Remove commenting from generated mirrorlist
    file.close()
    os.popen("gksudo mv ~/.auc/mirrorlist.tmp /etc/pacman.d/mirrorlist")
