# ArchUpdateChecker
A small wrapper around pacman for Arch Linux that prompts the user when updates are available.

Requirements:
* Python 3
* GTK 3
* PyGObject
* GNU wc
* pacman package manager
* A bash like default shell

To run, execute auc.py as root, or using sudo/gksudo. If not ran as root, the pacman database will not be updated.
