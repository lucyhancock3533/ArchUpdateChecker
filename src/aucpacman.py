#! /usr/bin/python3
"""AUC pacman module, deals with interacting with the pacman command"""

import subprocess, os, sys

def syncDB(): # Invoke pacman and update package database
    syncProcess = subprocess.Popen(["/usr/bin/gksudo", "/usr/bin/pacman -Syy"])
    syncProcess.wait()

def getUpdateCount(): # Get number of packages needing updates
    updates = os.popen("pacman -Qnu | wc -l")
    return int(updates.read())

def runUpdates(): # Run pacman and update system
    updates = subprocess.Popen(["/usr/bin/gksudo", "/usr/bin/pacman -Su --noconfirm --noprogressbar"], stdout=subprocess.PIPE)
    return updates

def getUpdates(): # Get list of updates
    updates = subprocess.check_output(["/usr/bin/pacman", "-Qnu"]).splitlines()
    return updates
