#! /usr/bin/python3
"""Module for dealing with mirrorlist syncing"""

import os
from pathlib import Path

def getMrlUrl():
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

def setMrlUrl(newUrl):
    """Save config of mirrorlist url"""
    configFolder = Path(os.path.expanduser("~/.auc/"))
    configFolder.mkdir(parents=True, exist_ok=True) # Ensure folder exists
    file = open(os.path.expanduser("~/.auc/mirrorlist.conf"), 'w')
    file.write('1\n')
    file.write(newUrl)
    file.write('\n')
    file.close() # Write settings to file
