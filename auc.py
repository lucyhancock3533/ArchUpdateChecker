import subprocess, os, sys

def syncDB():
    syncProcess = subprocess.Popen(["/usr/bin/pacman", "-Syy"])
    syncProcess.wait()
    if syncProcess.returncode == 0:
        print("Database syncronised")
    else:
        print("Failed to syncronise DB")
        quit(1)

def getUpdates():
    updates = os.popen("pacman -Qnu | wc -l")
    updCount = int(updates.read())
    print(str(updCount) + " updates are available")
    return updCount

syncDB()
getUpdates()
