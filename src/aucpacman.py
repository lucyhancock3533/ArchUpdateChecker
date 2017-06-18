#! /usr/bin/python3

import subprocess, os, sys

def syncDB(): # Invoke pacman and update package database
    syncProcess = subprocess.Popen(["/usr/bin/pacman", "-Syy"])
    syncProcess.wait()

def getUpdateCount(): # Get number of packages needing updates
    updates = os.popen("pacman -Qnu | wc -l")
    return int(updates.read())

def runUpdates(): # Run pacman and update system
    updateProcess = subprocess.Popen(["/usr/bin/pacman", "-Su"])
    updateProcess.wait()
