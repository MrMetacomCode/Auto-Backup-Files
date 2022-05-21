import os
import sys
import shutil
from datetime import date
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.blocking import BlockingScheduler

# When there is need, just change the directory
os.chdir(sys.path[0])


selected_dst_dir = "/home/mrmetacom/Documents/MC-Server-Backups/"
selected_src_dir = "/home/mrmetacom/Documents/Current-MC-Server/"


def take_backup(src_dir, dst_dir):

    # Extract the today's date
    today = date.today()
    date_format = today.strftime("%d_%b_%Y_")

    try:
        # When user enters a name for the backup copy
        new_dst_dir = f"{dst_dir}{date_format}Current-MC-Server"

        # Now, just copy the files from source to destination
        shutil.copytree(src_dir, new_dst_dir)

        print("Backup Successful!")
    except FileNotFoundError:
        print("File does not exists!,\
        please give the complete path")


def backup_files():
    # Call the function
    take_backup(selected_src_dir, selected_dst_dir)


scheduler = BlockingScheduler()
scheduler.add_job(backup_files, CronTrigger(hour=21, minute=20, second=0))
print("Auto backup is running.")
scheduler.start()
