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
def take_backup(src_file_name,
                dst_file_name=None,
                src_dir='',
                dst_dir=''):
    try:

        # Extract the today's date
        today = date.today()
        date_format = today.strftime("%d_%b_%Y_")

        # Make the source directory,
        # where we wanna backup our files
        src_dir = src_dir + src_file_name

        # If user not enter any source file,
        # then just give the error message...
        if not src_file_name:
            print("Please give at least the source file name")
            exit()

        try:

            # If user provides all the inputs
            if src_file_name and dst_file_name and src_dir and dst_dir:
                src_dir = src_dir + src_file_name
                dst_dir = dst_dir + dst_file_name

            # When User Enter Either
            # 'None' or empty String ('')
            elif dst_file_name is None or not dst_file_name:
                dst_file_name = src_file_name
                dst_dir = dst_dir + date_format + dst_file_name

            # When user enters an empty string with one or more spaces (' ')
            elif dst_file_name.isspace():
                dst_file_name = src_file_name
                dst_dir = dst_dir + date_format + dst_file_name

            # When user enters a name for the backup copy
            else:
                dst_dir = dst_dir + date_format + dst_file_name

            # Now, just copy the files from source to destination
            shutil.copy2(src_dir, dst_dir)

            print("Backup Successful!")
        except FileNotFoundError:
            print("File does not exists!,\
            please give the complete path")

    # When we need to back up the folders only...
    except PermissionError:
        shutil.copytree(src_file_name, dst_dir)
        print(f"Copied {src_file_name} to {dst_dir}.")


def backup_files():
    # Call the function
    take_backup("Current-MC-Server", dst_dir="../MC-Server-Backups/", src_dir="cd ../Current-MC-Server")


scheduler = BlockingScheduler()
scheduler.add_job(backup_files, CronTrigger(hour=23, minute=59, second=0))
print("Auto backup is running.")
scheduler.start()
