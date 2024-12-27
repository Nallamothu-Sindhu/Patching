import os
import subprocess
from datetime import datetime
import json
from .csv_converting import csv_convert_function
 
def backup_server_status(backup_path, ip_address, stage):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        backup_dir = os.path.join(backup_path, f"{ip_address}_{stage}_{timestamp}")
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        backup_file = os.path.join(backup_dir, f'server_status_{stage}.txt')
        final_dic = {}
        res = subprocess.run(['systemd-detect-virt'], stdout=subprocess.PIPE)
        final_dic['server_status'] = res.stdout.decode('utf-8').strip()
        with open(backup_file, 'w') as f:
            json.dump(final_dic, f, indent=4)
        return {"changed": True, "msg": f"Backup server status saved to {backup_file}"}
    except Exception as e:
        return {"failed": True, "msg": f"Backup server status failed: {e}"}
 
def compare_server_status(backup_path, ip_address):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        pre_patch_dir = os.path.join(backup_path, f"{ip_address}_Prepatch_{timestamp}")
        post_patch_dir = os.path.join(backup_path, f"{ip_address}_Postpatch_{timestamp}")
        pre_patch_file = os.path.join(pre_patch_dir, 'server_status_Prepatch.txt')
        post_patch_file = os.path.join(post_patch_dir, 'server_status_Postpatch.txt')
 
        if not os.path.exists(pre_patch_file):
            return {"failed": True, "msg": "No pre-patch server status file found to compare"}
        if not os.path.exists(post_patch_file):
            return {"failed": True, "msg": "No post-patch server status file found to compare"}
 
        with open(pre_patch_file, 'r') as f:
            pre_patch_info = json.load(f)
        with open(post_patch_file, 'r') as f:
            post_patch_info = json.load(f)
 
        diff_info = {}
        for key in pre_patch_info:
            if key in post_patch_info and pre_patch_info[key] != post_patch_info[key]:
                diff_info[key] = (f"PRE_PATCH -> {pre_patch_info[key]}", f"POST_PATCH -> {post_patch_info[key]}")
                csv_res = csv_convert_function(ip_address,backup_path,"info_server_status",pre_patch_info[key],post_patch_info[key])
                
                diff_info["csvvvvvvvvvvvvv"] = csv_res
        if diff_info != {}:

          diff_backup_dir = os.path.join(backup_path, f"{ip_address}_Difference_{timestamp}")
          if not os.path.exists(diff_backup_dir):
              os.makedirs(diff_backup_dir)
          diff_info_file = os.path.join(diff_backup_dir, 'diff_server_status.txt')
          with open(diff_info_file, 'w') as f:
              json.dump(diff_info, f, indent=4)
          return {"changed": True, "msg": f"Server status differences saved to {diff_info}"}
        else:
          return {"changed": True, "msg": f"Server status are identical"}
    except Exception as e: 
        return {"failed": True, "msg": f"Comparison of server status failed: {e}"}
