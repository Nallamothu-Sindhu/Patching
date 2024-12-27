import os
import shutil
import zipfile
from datetime import datetime
def backup_and_zip(ip_address):
    # Generate the zip filename with ip_address and current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    zip_filename = f"backup_{ip_address}_{current_date}.zip"
    dest_dir = "/final"
    backup_path = "/backup"
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    # Move the contents of backup_path to the destination directory
    for item in os.listdir(backup_path):
        item_path = os.path.join(backup_path, item)
        dest_path = os.path.join(dest_dir, item)
        # Check if destination path already exists
        if os.path.exists(dest_path):
            # If it's a directory, remove it
            if os.path.isdir(dest_path):
                shutil.rmtree(dest_path)
            # If it's a file, remove it
            else:
                os.remove(dest_path)
        # Move the item to the destination directory
        shutil.move(item_path, dest_path)
    # Create the zip file
    zip_path = os.path.join(dest_dir, zip_filename)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dest_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dest_dir)
                zipf.write(file_path, arcname)
    return zip_path
