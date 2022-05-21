import os
import sys
import shutil
from datetime import date
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.blocking import BlockingScheduler

# When there is need, just change the directory
os.chdir(sys.path[0])


# Function for performing the
# backup of the files and folders
def take_backup(src_dir='',
                dst_dir=''):

    # Extract the today's date
    today = date.today()
    date_format = today.strftime("%d_%b_%Y_")

    try:
        # When user enters a name for the backup copy
        dst_dir = f"{date_format}Current-MC-Server"

        # Now, just copy the files from source to destination
        shutil.copytree(src_dir, dst_dir)

        print("Backup Successful!")
    except FileNotFoundError:
        print("File does not exists!,\
        please give the complete path")


def backup_files():
    # Call the function
    take_backup(dst_dir="../MC-Server-Backups/", src_dir="/home/mrmetacom/Documents/Current-MC-Server/")


scheduler = BlockingScheduler()
scheduler.add_job(backup_files, CronTrigger(hour=21, minute=3, second=0))
print("Auto backup is running.")
scheduler.start()
