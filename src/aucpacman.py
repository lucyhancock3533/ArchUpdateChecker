#! /usr/bin/python3
"""AUC pacman module, deals with interacting with the pacman command"""

import subprocess
import os

def sync_db(cmd): # Invoke pacman and update package database
    """Updates pacman database"""
    subprocess.check_output(cmd)

def get_update_count(): # Get number of packages needing updates
    """Retrives number of updates available"""
    updates = os.popen("pacman -Qnu")
    updates = updates.read().splitlines()
    count = 0
    for update in updates:
        if "[ignored]" not in update:
            count = count + 1
    return count

def get_ignore_count(): # Get number of packages needing updates
    """Retrives number of updates available"""
    updates = os.popen("pacman -Qnu")
    updates = updates.read().splitlines()
    count = 0
    for update in updates:
        if "[ignored]" in update:
            count = count + 1
    return count

def run_updates(cmd): # Run pacman and update system
    """Executes pacman command to update"""
    updates = subprocess.Popen( \
        cmd \
        , stdout=subprocess.PIPE)
    return updates

def get_updates(): # Get list of updates
    """Gets a list of updates available"""
    updates = subprocess.check_output(["/usr/bin/pacman", "-Qnu"]).splitlines()
    return updates
