# ArchUpdateChecker
A small wrapper around pacman for Arch Linux that prompts the user if updates are available when ran.

Requirements:
* Python 3.6+
* GTK 3 (Not required for CLI)
* GKSU (Not required for CLI)
* PyGObject (Not required for CLI)
* sudo
* pacman package manager
* Python requests package

To run with GTK, execute auc.py. AUC should be ran as a normal user, not as root.

To run from CLI, execute `auc.py --cli`, as normal user.
