import os
import subprocess
from datetime import datetime
import json
from .csv_converting import csv_convert_function

 
def backup_network_info(backup_path, ip_address,stage):
    """
    Backs up network information before a patch.
    """
    try:
        # Check if 'ip' command is available
        if subprocess.call(['which', 'ip'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) != 0:
            return {"failed": True, "msg": "ip command not found. Please ensure network management tools are installed."}
 
        timestamp = datetime.now().strftime("%Y-%m-%d")
        pre_patch_dir = os.path.join(backup_path, f"{ip_address}_{stage}_{timestamp}")
 
        if not os.path.exists(pre_patch_dir):
            os.makedirs(pre_patch_dir)
 
        backup_file = os.path.join(pre_patch_dir, 'network_info_{stage}.txt')
 
        final_dic = {}
        res = subprocess.run(['ip', '-br', 'addr'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 
        if res.returncode != 0:
            return {"failed": True, "msg": f"ip command failed: {res.stderr.decode('utf-8').strip()}"}
 
        final_dic['network_interfaces'] = res.stdout.decode('utf-8').strip()
 
        with open(backup_file, 'w') as f:
            json.dump(final_dic, f, indent=4)
 
        return {"changed": True, "msg": f"Backup network info saved to {backup_file}"}
 
    except Exception as e:
        return {"failed": True, "msg": f"Backup network info failed: {e}"}
 
def compare_network_info(backup_path, ip_address):
    """
    Compares pre-patch and post-patch network information and saves differences.
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        post_patch_dir = os.path.join(backup_path, f"{ip_address}_Postpatch_{timestamp}")
 
        if not os.path.exists(post_patch_dir):
            os.makedirs(post_patch_dir)
 
        post_backup_file = os.path.join(post_patch_dir, 'network_info_Postpatch.txt')
 
        final_dic = {}
        res = subprocess.run(['ip', '-br', 'addr'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 
        if res.returncode != 0:
            return {"failed": True, "msg": f"ip command failed: {res.stderr.decode('utf-8').strip()}"}
 
        final_dic['network_interfaces'] = res.stdout.decode('utf-8').strip()
 
        with open(post_backup_file, 'w') as f:
            json.dump(final_dic, f, indent=4)
 
        # Find the most recent pre-patch directory
        pre_patch_dirs = [d for d in os.listdir(backup_path) if d.startswith(f"{ip_address}_Prepatch_")]
        if not pre_patch_dirs:
            return {"failed": True, "msg": "No pre-patch network info file found to compare"}
 
        pre_patch_dir = os.path.join(backup_path, max(pre_patch_dirs))
        pre_patch_file = os.path.join(pre_patch_dir, 'network_info_Prepatch.txt')
 
        if not os.path.exists(pre_patch_file):
            return {"failed": True, "msg": "Pre-patch network info file not found in the most recent pre-patch directory"}
 
        with open(pre_patch_file, 'r') as f:
            pre_patch_info = json.load(f)
        with open(post_backup_file, 'r') as f:
            post_patch_info = json.load(f)
 
        diff_info = {}
        for key in pre_patch_info:
            if key in post_patch_info and pre_patch_info[key] != post_patch_info[key]:
                diff_info[key] = (f"PRE_PATCH -> {pre_patch_info[key]}", f"POST_PATCH -> {post_patch_info[key]}")
                csv_res = csv_convert_function(ip_address,backup_path,"info_network_info",pre_patch_info[key],post_patch_info[key])
                
                diff_info["csvvvvvvvvvvvvv"] = csv_res       
               
        if diff_info != {}:
            diff_backup_dir = os.path.join(backup_path, f"{ip_address}_Difference_{timestamp}")
            if not os.path.exists(diff_backup_dir):
               os.makedirs(diff_backup_dir)
            diff_info_file = os.path.join(diff_backup_dir, 'diff_network_info.txt')
            with open(diff_info_file, 'w') as f:
                 json.dump(diff_info, f, indent=4)
 
            return {"changed": True, "msg": f"Network info differences saved to {diff_info_file}"}
        else:
            return {"changed": False, "msg": "Network info is identical between pre-patch and post-patch"}
 
    except Exception as e:
        return {"failed": True, "msg": f"Comparison of network info failed: {e}"}
