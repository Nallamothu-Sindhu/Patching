import os
import subprocess
from datetime import datetime
 
def backup_services_list(backup_path, ip_address):
    """
    Backs up the list of running and stopped services before a patch.
    Arguments:
    - backup_path: The path where backups should be stored.
    - ip_address: The IP address of the system, used to differentiate backups.
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        backup_dir = os.path.join(backup_path, f"{ip_address}_Prepatch_{timestamp}")
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        # Backup running services
        running_services_file = os.path.join(backup_dir, 'pre_patch_running_services.txt')
        with open(running_services_file, 'w') as f:
            subprocess.run(['systemctl', 'list-units', '--type=service', '--state=running'], stdout=f, check=True)
        # Backup stopped services
        stopped_services_file = os.path.join(backup_dir, 'pre_patch_stopped_services.txt')
        with open(stopped_services_file, 'w') as f:
            subprocess.run(['systemctl', 'list-units', '--type=service', '--state=exited,failed'], stdout=f, check=True)
        return {"changed": True, "msg": f"Pre-patch backup of services list to {backup_dir}"}
    except Exception as e:
        return {"failed": True, "msg": f"Backup failed: {e}"}
 
def compare_services_list(backup_path, ip_address):
    """
    Creates a post-patch backup of services and compares it with the pre-patch backup.
    Arguments:
    - backup_path: The path where backups are stored.
    - ip_address: The IP address of the system, used to differentiate backups.
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        post_backup_dir = os.path.join(backup_path, f"{ip_address}_Postpatch_{timestamp}")
        if not os.path.exists(post_backup_dir):
            os.makedirs(post_backup_dir)
        # Backup post-patch running services
        post_running_services_file = os.path.join(post_backup_dir, 'post_patch_running_services.txt')
        with open(post_running_services_file, 'w') as f:
            subprocess.run(['systemctl', 'list-units', '--type=service', '--state=running'], stdout=f, check=True)
        # Backup post-patch stopped services
        post_stopped_services_file = os.path.join(post_backup_dir, 'post_patch_stopped_services.txt')
        with open(post_stopped_services_file, 'w') as f:
            subprocess.run(['systemctl', 'list-units', '--type=service', '--state=exited,failed'], stdout=f, check=True)
        # Assuming pre-patch backup exists and finding it
        pre_backup_dir = os.path.join(backup_path, f"{ip_address}_Prepatch_{timestamp}")  # This should be adjusted to find the actual pre-patch backup directory
        pre_running_services_file = os.path.join(pre_backup_dir, 'pre_patch_running_services.txt')  # Adjust path as needed
        pre_stopped_services_file = os.path.join(pre_backup_dir, 'pre_patch_stopped_services.txt')  # Adjust path as needed
        # Compare running services
        running_diff = subprocess.run(['diff', pre_running_services_file, post_running_services_file], capture_output=True, text=True)
        # Compare stopped services
        stopped_diff = subprocess.run(['diff', pre_stopped_services_file, post_stopped_services_file], capture_output=True, text=True)
        if running_diff.returncode == 0 and stopped_diff.returncode == 0:
            return {"changed": False, "msg": "No differences found in services lists."}
        else:
            differences = f"Running Services Differences:\n{running_diff.stdout}\nStopped Services Differences:\n{stopped_diff.stdout}"
            diff_backup_dir = os.path.join(backup_path, f"{ip_address}_Difference_{timestamp}")
            if not os.path.exists(diff_backup_dir):
               os.makedirs(diff_backup_dir)
            # Backup post-patch running services
            diff_running_services_file = os.path.join(diff_backup_dir, 'diff_patch_running_services.txt')
            with open(diff_running_services_file, 'w') as f:
                 f.write(differences)
            return {"changed": True, "msg": f"Services lists differ:\n{differences}"}
    except Exception as e:
        return {"failed": True, "msg": f"Comparison failed: {e}"}
