import os
import sys
import shutil
from datetime import date
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.blocking import BlockingScheduler

# When there is need, just change the directory
os.chdir(sys.path[0])

# /home/mrmetacom/Documents/MC-Server-Backups/
selected_dst_dir = str(input("Enter the full directory path where you would like to have the backup files saved "
                             "(example: /home/mrmetacom/Minecraft-Server/MC-Server-Backups/): "))
for x in range(5):
    # /home/mrmetacom/Documents/Current-MC-Server/
    selected_src_dir = str(input("Enter the full path of the directory you would like to backup "
                                 "(example: /home/mrmetacom/Minecraft-Server/Current-MC-Server/): "))
    if os.path.exists(selected_src_dir) is False:
        print("That directory path is invalid. Try again.")
        continue
    break
else:
    print("Failed to input a correct directory to backup. Goodbye.")
    exit()

for x in range(5):
    save_backups_amount = input("Enter how many backups you would like to have at any given time. For example, 10 means the last 10 backups will be saved: ")
    try:
        save_backups_amount = int(save_backups_amount)
    except ValueError:
        print("Please enter a number.")
    break
else:
    print("Failed to input a number. Goodbye.")
    exit()

backup_name = str(input("Enter the name that will be attached to each backup (example: 06_Nov_2022_NAME): "))


def take_backup(src_dir, dst_dir):
    # Extract the today's date
    today = date.today()
    date_format = today.strftime("%d_%b_%Y_")

    try:
        if os.path.exists(selected_dst_dir):
            # Delete the oldest backup if the last 10 have already been saved.
            backed_up_directories = os.listdir(selected_dst_dir)
            if len(backed_up_directories) >= save_backups_amount:
                backed_up_directories.sort(key=lambda directory: os.path.getctime(f"{selected_dst_dir}/{directory}"))
                oldest_directory = f"{selected_dst_dir}/{backed_up_directories[0]}"
                os.rmdir(oldest_directory)
                print(
                    f"{save_backups_amount} backups currently saved. Deleted the oldest before backing up again: {oldest_directory}")

        # When user enters a name for the backup copy
        new_dst_dir = f"{dst_dir}{date_format}{backup_name}"

        if os.path.exists(new_dst_dir) is False:
            # Now, just copy the files from source to destination
            shutil.copytree(src_dir, new_dst_dir)

            print("Backup Successful!")
        else:
            print(f"Error: Backup with name {new_dst_dir} already exists.")
    except FileNotFoundError:
        print("File does not exists!,\
        please give the complete path")


def backup_files():
    # Call the function
    take_backup(selected_src_dir, selected_dst_dir)


scheduler = BlockingScheduler()
scheduler.add_job(backup_files, CronTrigger(hour=4, minute=0, second=0))
print("Auto backup is running.")
scheduler.start()
