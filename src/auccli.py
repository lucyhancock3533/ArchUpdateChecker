from aucpacman import sync_db, get_update_count, get_ignore_count, get_updates, run_updates
from aucpmml import get_mrl_url, set_mrl_url, update_mrl
"""Module dealing with cli for AUC"""

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
    sync_db(["/usr/bin/sudo", "pacman", "-Sy"])
    print(str(get_update_count()) + " updates are available, " + str(get_ignore_count())\
    + " updates are ignored")
    if (get_update_count() > 0):
        prompt_updates()

def prompt_updates():
    updates = [upd.decode("utf-8") for upd in get_updates()]
    print("Updates available: " + ', '.join(updates))
    check_upd = input("Update now?(y/n) ")
    if check_upd == 'y':
        do_updates()

def do_updates():
    update_pipe = run_updates(["/usr/bin/sudo", "pacman", "-Su", "--noconfirm", "--noprogressbar"])
    for line in update_pipe.stdout: # Update text view
        print(line.decode("utf-8"))
