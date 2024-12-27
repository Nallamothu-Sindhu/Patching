import os
import subprocess
from datetime import datetime
import json
from .csv_converting import csv_convert_function

 
def backup_routing_info(backup_path, ip_address, stage):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        backup_dir = os.path.join(backup_path, f"{ip_address}_{stage}_{timestamp}")
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        backup_file = os.path.join(backup_dir, f'routing_info_{stage}.txt')
        final_dic = {}
        #ip route
        res = subprocess.run(['ip', 'route'], stdout=subprocess.PIPE)
        final_dic['routing_details'] = res.stdout.decode('utf-8').strip()
        
        # default gateway
        res = subprocess.run(['ip', 'route', 'show', 'default'], stdout=subprocess.PIPE)
        final_dic['default_gateway'] = res.stdout.decode('utf-8').strip()
 
        with open(backup_file, 'w') as f:
            json.dump(final_dic, f, indent=4)
        return {"changed": True, "msg": f"Backup routing info saved to {backup_file}"}
    except Exception as e:
        return {"failed": True, "msg": f"Backup routing info failed: {e}"}
 
def compare_routing_info(backup_path, ip_address):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        pre_patch_dir = os.path.join(backup_path, f"{ip_address}_Prepatch_{timestamp}")
        post_patch_dir = os.path.join(backup_path, f"{ip_address}_Postpatch_{timestamp}")
        pre_patch_file = os.path.join(pre_patch_dir, 'routing_info_Prepatch.txt')
        post_patch_file = os.path.join(post_patch_dir, 'routing_info_Postpatch.txt')
 
        if not os.path.exists(pre_patch_file):
            return {"failed": True, "msg": "No pre-patch routing info file found to compare"}
        if not os.path.exists(post_patch_file):
            return {"failed": True, "msg": "No post-patch routing info file found to compare"}
 
        with open(pre_patch_file, 'r') as f:
            pre_patch_info = json.load(f)
        with open(post_patch_file, 'r') as f:
            post_patch_info = json.load(f)
 
        diff_info = {}
        for key in pre_patch_info:
            if key in post_patch_info and pre_patch_info[key] != post_patch_info[key]:
                diff_info[key] = (f"PRE_PATCH -> {pre_patch_info[key]}", f"POST_PATCH -> {post_patch_info[key]}")
                csv_res = csv_convert_function(ip_address,backup_path,"info_routing_info",pre_patch_info[key],post_patch_info[key])
                
                diff_info["csvvvvvvvvvvvvv"] = csv_res
        if diff_info != {}:
          diff_backup_dir = os.path.join(backup_path, f"{ip_address}_Difference_{timestamp}")
          if not os.path.exists(diff_backup_dir):
              os.makedirs(diff_backup_dir)
          diff_info_file = os.path.join(diff_backup_dir, 'diff_routing_info.txt')
          with open(diff_info_file, 'w') as f:
              json.dump(diff_info, f, indent=4)
          return {"changed": True, "msg": f"Routing info differences saved to {diff_info}"}
        else:
            return {"changed": True, "msg": f"Routing info are identical"}
    except Exception as e:
        return {"failed": True, "msg": f"Comparison of routing info failed: {e}"}
