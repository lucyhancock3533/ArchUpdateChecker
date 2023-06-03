#! /usr/bin/python3
"""AUC Main CLI module, syncs, checks for updates, and alerts user."""

from aucpacman import sync_db, get_update_count, get_ignore_count, get_updates, run_updates
from aucpmml import get_mrl_url, set_mrl_url, update_mrl

def run_auc_cli():
    print("ArchUpdateChecker v0-git")
    mirrorlist = get_mrl_url()
    if(mirrorlist == ""):
        pass
    elif(mirrorlist == "NOMRLUPD"):
        run_auc()
    else:
        update_mrl("sudo")
        run_auc()

def run_auc():
	log = Logger()
    sync_db(["/usr/bin/sudo", "pacman", "-Sy"])
	log.log_write("AUC running in CLI mode")
	note_str = str(get_update_count()) + " updates are available, " + str(get_ignore_count())\
    + " updates are ignored"
    print(note_str)
	log.log_write(note_str)
    if (get_update_count() > 0):
        prompt_updates(log)
	log.log_close()

def prompt_updates(log):
    updates = [upd.decode("utf-8") for upd in get_updates()]
	upd_str = "Updates available: " + ', '.join(updates)
    print(upd_str)
	log.log_write(upd_str)
    check_upd = input("Update now?(y/n) ")
    if check_upd == 'y':
        do_updates(log)

def do_updates(log):
    update_pipe = run_updates(["/usr/bin/sudo", "pacman", "-Su", "--noconfirm", "--noprogressbar"])
    for line in update_pipe.stdout: # Update text view
        print(line.decode("utf-8"))
		log.log_write(line.decode("utf-8"))
	log.log_write("AUC updates are complete")