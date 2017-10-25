#! /usr/bin/python3
"""Module for dealing with mirrorlist syncing"""

import os

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
