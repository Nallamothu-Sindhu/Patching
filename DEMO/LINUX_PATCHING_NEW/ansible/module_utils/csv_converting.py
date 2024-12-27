import csv
import os
from datetime import datetime

def csv_convert_function(ip_address,backup_path,func_name,prepatch_data,postpatch_data):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d")

        csv_backup_dir = os.path.join(backup_path, f"{ip_address}_CSV_{timestamp}")
        if not os.path.exists(csv_backup_dir):
            os.makedirs(csv_backup_dir)
               
            data = [
                   ["IP_ADDRESS/HOSTNAME","FUNCTIONALITY","PREPATCH DATA","POST PATCH DATA"],
                   [ip_address,func_name,prepatch_data,postpatch_data]
            ] 

            csv_backup_dir = os.path.join(backup_path, f"{ip_address}_CSV_{timestamp}")
            if not os.path.exists(csv_backup_dir):
                os.makedirs(csv_backup_dir)
            csv_file = os.path.join(csv_backup_dir, "ticketNum_"+str(ip_address)+'_output.csv')

            with open(csv_file,mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)

            return {"Sucess":"SUCESSSSSSSSSSSS"}
        else:
            data = [
                  # ["functionality","prepatch_data","postpatch_data"],
                  # [func_name,prepatch_data,postpatch_data]
                   [ip_address,func_name,prepatch_data,postpatch_data]
                   ]

            csv_backup_dir = os.path.join(backup_path, f"{ip_address}_CSV_{timestamp}")
            if not os.path.exists(csv_backup_dir):
                os.makedirs(csv_backup_dir)
            csv_file = os.path.join(csv_backup_dir, "ticketNum_"+str(ip_address)+'_output.csv')

            with open(csv_file,mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)

            return {"Sucess":"SUCESSSSSSSSSSSS"}

    except Exception as e:

        return {"failed": True, "msg": f"CSVVVVVVVVVVV failed: {e}"}
