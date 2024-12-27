import os

import subprocess

from datetime import datetime

import json
from .csv_converting import csv_convert_function
 
def backup_info_host_information(backup_path, ip_address, stage):

    """

    Backs up host information before or after the patch.

    Args:

    - backup_path (str): The base directory where backup files will be stored.

    - ip_address (str): The IP address of the machine to be included in the backup directory name.

    - stage (str): The stage of the process ('PRE_PATCH' or 'POST_PATCH').
 
    Returns:

    - dict: A dictionary with 'changed' and 'msg' keys to indicate the status of the backup operation.

    """

    try:

        timestamp = datetime.now().strftime("%Y-%m-%d")

        backup_dir = os.path.join(backup_path, f"{ip_address}_{stage}_{timestamp}")
        if not os.path.exists(backup_dir):

            os.makedirs(backup_dir)

        backup_file = os.path.join(backup_dir, f'backup_info_host_information_{stage}.txt')

        final_dic = {}

        res_host_f = subprocess.run(['hostname','-f'], stdout=subprocess.PIPE)

        res_host_f = res_host_f.stdout.decode('utf-8').strip()

        final_dic['Hostname_f'] = res_host_f

        res_hostctl_status = subprocess.run(['hostnamectl','status'], stdout=subprocess.PIPE)

        res_hostctl_status = res_hostctl_status.stdout.decode('utf-8').strip()

        final_dic['Hostname_ctl_status'] = res_hostctl_status

        with open(backup_file, 'w') as f:

            json.dump(final_dic, f)

        return {"changed": True, "msg": f"Backup of host_information saved to {backup_file}"}

    except Exception as e:

        return {"failed": True, "msg": f"Backup failed: {e}"}
 
def compare_info_host_information(backup_path, ip_address):

    """

    Compares the pre-patch and post-patch host information and saves the differences to a file.

    Args:

    - backup_path (str): The base directory where backup files are stored.

    - ip_address (str): The IP address of the machine to be included in the backup directory name.
 
    Returns:

    - dict: A dictionary with 'changed' and 'msg' keys to indicate the status of the comparison operation.

    """

    try:

        timestamp = datetime.now().strftime("%Y-%m-%d")

        pre_patch_dir = os.path.join(backup_path, f"{ip_address}_Prepatch_{timestamp}")

        post_patch_dir = os.path.join(backup_path, f"{ip_address}_Postpatch_{timestamp}")
 
        pre_patch_file = os.path.join(pre_patch_dir, 'host_information_Prepatch.txt')

        post_patch_file = os.path.join(post_patch_dir, 'host_information_Postpatch.txt')
 
        if not os.path.exists(pre_patch_file):

            return {"failed": True, "msg": "No pre-patch backup file found to compare"}
 
        if not os.path.exists(post_patch_file):

            return {"failed": True, "msg": "No post-patch backup file found to compare"}
 
        with open(pre_patch_file, 'r') as f:

            pre_patch_info = json.load(f)

        with open(post_patch_file, 'r') as f:

            post_patch_info = json.load(f)
 
        diff_info = {}
        print("diffffffffffff11111111111111122222222222222222",diff_info)
        for key in pre_patch_info:
            if key in post_patch_info and pre_patch_info[key] != post_patch_info[key]:
               diff_info[key] = ("PREPATCH ->"+str(pre_patch_info[key]), "POSTPATCH ->"+str(post_patch_info[key]))
               csv_res = csv_convert_function(ip_address,backup_path,"info_host_information",pre_patch_info[key],post_patch_info[key])
                
               diff_info["csvvvvvvvvvvvvv"] = csv_res
        if diff_info != {}:
            diff_backup_dir = os.path.join(backup_path, f"{ip_address}_Difference_{timestamp}")
            if not os.path.exists(diff_backup_dir):
               os.makedirs(diff_backup_dir)
            diff_info_dateTime_file = os.path.join(diff_backup_dir, 'diff_info_host_information.txt')
            with open(diff_info_dateTime_file, 'w') as f:
                 json.dump(diff_info, f, indent=4)
            return {"changed": True, "msg": f"host information differ:\n{diff_info}"}

        else:

            return {"changed": False, "msg": "Info files are identical"}

    except Exception as e:

        return {"failed": True, "msg": f"Comparison failed: {e}"}
