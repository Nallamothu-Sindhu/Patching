from ansible.module_utils.basic import AnsibleModule

import os
import sys
import json
import csv
import glob

# Add the current directory to the sys.path to find the module files

module_path = os.path.dirname(__file__)

sys.path.insert(0, module_path)

# Import custom functions from module_utils

from ansible.module_utils.file_system_fstab import compare_fstab_list,backup_fstab_list

from ansible.module_utils.file_system_mount import compare_mount_list,backup_mount_list

from ansible.module_utils.list_softwares import compare_services_list

from ansible.module_utils.update_packages import update_packages

from ansible.module_utils.backup_and_zip_module import backup_and_zip

#from ansible.module_utils.get_info_and_dateTime import backup_info_dateTime,compare_info_dateTime

from ansible.module_utils.monitor_process import backup_monitor_process,compare_monitor_process

from ansible.module_utils.network_status import backup_network_status,compare_network_status

from ansible.module_utils.pswd_groups_sudoers import backup_pswd_groups_sudoers,compare_pswd_groups_sudoers

from ansible.module_utils.routing_info import backup_routing_info,compare_routing_info

from ansible.module_utils.memory_info import backup_memory_info,compare_memory_info

from ansible.module_utils.server_status import backup_server_status,compare_server_status

from ansible.module_utils.system_build_date import backup_system_build_date,compare_system_build_date

from ansible.module_utils.network_interface_info import backup_network_info,compare_network_info

from ansible.module_utils.network_config import backup_network_config,compare_network_config

from ansible.module_utils.network_link_status import backup_network_link_status,compare_network_link_status

from ansible.module_utils.selinux_status import backup_selinux_status,compare_selinux_status

from ansible.module_utils.kernel_install import compare_kernel_info, backup_kernel_info

from ansible.module_utils.host_configuration import compare_hosts_info, backup_hosts_info

from ansible.module_utils.dns_resolvers import compare_dns_resolvers_info,backup_dns_resolvers_info
from ansible.module_utils.Satellite_subscription_status import compare_satellite_subscription_status,backup_satellite_subscription_status
from ansible.module_utils.Redhat_release import compare_redhat_release_info,backup_redhat_release_info
from ansible.module_utils.db_avail_and_running_status import backup_db_avail_and_running_status,compare_db_avail_and_running_status 
from ansible.module_utils.firewall_status_and_configuration import compare_firewall_status_and_config,backup_firewall_status_and_config

from ansible.module_utils.host_information import backup_info_host_information,compare_info_host_information
from ansible.module_utils.cpu_information import backup_info_cpu_information ,compare_info_cpu_information
from ansible.module_utils.blkid_information import backup_info_blkid , compare_info_blkid
from ansible.module_utils.uptime import backup_info_uptime , compare_info_uptime
from ansible.module_utils.kernel_version import backup_info_kernel_version , compare_info_kernel_version
from ansible.module_utils.last_reboot import backup_info_last_reboot , compare_info_last_reboot
from ansible.module_utils.current_FS_utilization import backup_info_current_FS_utilization ,compare_info_current_FS_utilization
from ansible.module_utils.disk_information import backup_info_disk_available , compare_info_disk_available

def convert_txt_to_csv(backup_path, ip_address):
    """
    Convert text files in the backup directory to CSV format.
 
    Args:
        backup_path (str): The base directory where backup files are stored.
        ip_address (str): The IP address of the machine to be included in the CSV.
 
    Returns:
        str: The path to the created CSV file or an error message.
    """
      # server_config_list:
    folder_path = os.path.join(backup_path, f"{ip_address}_Postpatch_*")
    output_csv_file = os.path.join(backup_path, f"{ip_address}_postpatch_output.csv")
 
    data_rows = []
    unique_fieldnames = ['ip_address', 'functionality_name', 'results']
    seen_entries = set()  # To track unique entries
 
    matching_folders = glob.glob(folder_path)
 
    if not matching_folders:
        return {"failed": True, "msg": f"No matching folders found for {folder_path}"}
 
    for folder in matching_folders:
        for filename in os.listdir(folder):
            if filename.endswith('.txt'):
                file_path = os.path.join(folder, filename)
                functionality_name = filename[:-4]  # Remove .txt for the functionality name
                with open(file_path, 'r') as file:
                    results = file.read().strip()
 
                    # Process results to only keep the values
                    if results.startswith('{') and results.endswith('}'):
                        try:
                            result_dict = json.loads(results)
                            results = '\n'.join(str(value) for value in result_dict.values())
                        except json.JSONDecodeError:
                            pass  # Keep the original results if JSON parsing fails
 
                    entry = (ip_address, functionality_name)
                    if entry not in seen_entries:
                        data_rows.append({
                            'ip_address': ip_address,
                            'functionality_name': functionality_name,
                            #'results':server
                            #'results': results
                        })
                        seen_entries.add(entry)
 
    if data_rows:
        with open(output_csv_file, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=unique_fieldnames)
            writer.writeheader()
            for row in data_rows:
                writer.writerow(row)
 
    return output_csv_file
    

def main():

    module_args = dict(

        backup_path=dict(type='str', required=True),

       # action=dict(type='str', required=True),

        ip_address=dict(type='str', required=True)

    )

    module = AnsibleModule(

        argument_spec=module_args,

    )

    backup_path = module.params['backup_path']

    #action = module.params['action']

    ip_address = module.params['ip_address']

    # Compare backup lists
    backup_file_system_fstab= backup_fstab_list(backup_path,ip_address,"Postpatch")

    compare_file_system_fstab = compare_fstab_list(backup_path, ip_address)
    backup_file_system_mount= backup_mount_list(backup_path,ip_address,"Postpatch")

    compare_file_system_mount = compare_mount_list(backup_path, ip_address)

    compare_file_services = compare_services_list(backup_path, ip_address)


    #backup_information
#    backup_info = backup_info_dateTime(backup_path, ip_address, "Postpatch")
 #   compare_date_time = compare_info_dateTime(backup_path, ip_address)

    #monitor_process
    backup_monitor_pro = backup_monitor_process(backup_path, ip_address, "Postpatch")
    compare_monitor_pro = compare_monitor_process(backup_path, ip_address)

    #network status
    backup_network_stat = backup_network_status(backup_path, ip_address, "Postpatch")
    compare_network_stat = compare_network_status(backup_path, ip_address)

    #pswd_groups_sudoers
    backup_pswd_groups_sudo = backup_pswd_groups_sudoers(backup_path, ip_address, "Postpatch")
    compare_pswd_groups_sudo = compare_pswd_groups_sudoers(backup_path, ip_address)

    #routing
    backup_routing_status_post = backup_routing_info(backup_path, ip_address, "Postpatch")
    compare_routing_dg_status = compare_routing_info(backup_path, ip_address)
    
    #memory info
    backup_memory_info_post = backup_memory_info(backup_path, ip_address, "Postpatch")
    compare_memory_info_res = compare_memory_info(backup_path, ip_address)

    #server status
    backup_server_status_post = backup_server_status(backup_path, ip_address, "Postpatch")
    compare_server_info = compare_server_status(backup_path, ip_address)

    #system build date
    backup_system_build_date_res = backup_system_build_date(backup_path, ip_address, "Postpatch")
    compare_system_build_date_res = compare_system_build_date(backup_path, ip_address)

    #network interface info
    backup_network_info_res = backup_network_info(backup_path, ip_address,"Postpatch")
    compare_network_interface = compare_network_info(backup_path, ip_address)

    #network config
    backup_network_config_res = backup_network_config(backup_path, ip_address,"Postpatch")
    compare_network_config_res = compare_network_config(backup_path, ip_address)

    #network link status
    backup_network_link_status_res = backup_network_link_status(backup_path, ip_address,"Postpatch")
    compare_network_link_status_res = compare_network_link_status(backup_path, ip_address)

    #selinux status
    backup_selinux_status_res = backup_selinux_status(backup_path, ip_address,"Postpatch")
    compare_selinux_status_res = compare_selinux_status(backup_path, ip_address)

    #kernel 
    backup_kernel_info_file= backup_kernel_info(backup_path,ip_address,"Postpatch")
    compare_kernel_status = compare_kernel_info(backup_path, ip_address)

    #host config
    backup_hosts_info_file= backup_hosts_info(backup_path,ip_address,"Postpatch")
    compare_hosts_config = compare_hosts_info(backup_path,ip_address)

    #dns config
    backup_dns_resolvers_info_file=backup_dns_resolvers_info(backup_path,ip_address,"Postpatch")
    compare_dns_resolvers_file=compare_dns_resolvers_info(backup_path,ip_address)
   
    backup_satellite_subscription_status_file=backup_satellite_subscription_status(backup_path,ip_address,"Postpatch")
    compare_satellite_subscription_status_file=compare_satellite_subscription_status(backup_path,ip_address)
    
    backup_redhat_release_info_file=backup_redhat_release_info(backup_path,ip_address,"Postpatch")
    compare_redhat_release_file=compare_redhat_release_info(backup_path,ip_address)

    backup_db_avail_and_running_status_file = backup_db_avail_and_running_status(backup_path,ip_address,"Postpatch")
    compare_db_avail_and_running_status_file = compare_db_avail_and_running_status(backup_path,ip_address)

    backup_firewall_status_and_config_file = backup_firewall_status_and_config(backup_path,ip_address,"Postpatch")
    compare_firewall_status_and_config_file = compare_firewall_status_and_config(backup_path,ip_address)
   
    backup_info_host_information_file = backup_info_host_information(backup_path,ip_address,"Postpatch")
    compare_info_host_information_file = compare_info_host_information(backup_path, ip_address)

    backup_info_uptime_file = backup_info_uptime(backup_path, ip_address,"Postpatch")
    compare_info_uptime_file = compare_info_uptime(backup_path, ip_address)

    backup_info_cpu_information_file = backup_info_cpu_information(backup_path, ip_address,"Postpatch")
    compare_info_cpu_information_file = compare_info_cpu_information(backup_path, ip_address)

    backup_info_blkid_file = backup_info_blkid(backup_path, ip_address,"Postpatch")
    compare_info_blkid_file = compare_info_blkid(backup_path, ip_address)

    backup_info_current_FS_utilization_file = backup_info_current_FS_utilization(backup_path, ip_address,"Postpatch")
    compare_info_current_FS_utilization_file = compare_info_current_FS_utilization(backup_path, ip_address)

    backup_info_last_reboot_file = backup_info_last_reboot(backup_path, ip_address,"Postpatch")
    compare_info_last_reboot_file = compare_info_last_reboot(backup_path, ip_address)

    backup_info_kernel_version_file = backup_info_kernel_version(backup_path, ip_address,"Postpatch")
    compare_info_kernel_version_file = compare_info_kernel_version(backup_path, ip_address)

    backup_info_disk_available_file = backup_info_disk_available(backup_path, ip_address,"Postpatch")
    compare_info_disk_available_file = compare_info_disk_available(backup_path, ip_address)
    # Update packages

    stdout, stderr = update_packages(module)

    # Call the backup_and_zip function

    zip_path = backup_and_zip(ip_address)

    csv_file_path = convert_txt_to_csv(backup_path, ip_address)

    # Check for any errors during CSV conversion
    if isinstance(csv_file_path, dict) and csv_file_path.get("failed"):
        module.fail_json(**csv_file_path)

    result = dict(

        changed=True,

      #  original_message='',

       # message='Compare, update packages, and backup functions called',

        stdout=stdout,

        stderr=stderr,
        backup_file_system_fstab=backup_file_system_fstab,
        compare_file_system_fstab=compare_file_system_fstab,
        backup_file_system_mount=backup_file_system_mount,

        compare_file_system_mount=compare_file_system_mount,

        compare_file_services=compare_file_services,

        #backup_date_time_info=backup_info,

       # compare_date_time_info=compare_date_time,

        zip_path=zip_path,

        compare_network_stat = compare_network_stat,

        compare_pswd_groups_sudo = compare_pswd_groups_sudo,

        rounting_info_res = compare_routing_dg_status,

        compare_memory_info_res = compare_memory_info_res,

        compare_server_details = compare_server_info,

        compare_system_build_date_res = compare_system_build_date_res,

        compare_network_interface_details = compare_network_interface,
        compare_network_config_res = compare_network_config_res,
        compare_network_link_status_res = compare_network_link_status_res,
        compare_selinux_status_res = compare_selinux_status_res,
        backup_kernel_info_file=backup_kernel_info_file,
        compare_kernel_status=compare_kernel_status,

        backup_hosts_info_file=backup_hosts_info_file,
        compare_hosts_config=compare_hosts_config,

        backup_dns_resolvers_info_file=backup_dns_resolvers_info_file,
        compare_dns_resolvers_file=compare_dns_resolvers_file,
    
        backup_satellite_subscription_status_file=backup_satellite_subscription_status_file,
        compare_satellite_subscription_status_file=compare_satellite_subscription_status_file,
    
        backup_redhat_release_info_file=backup_redhat_release_info_file,
        compare_redhat_release_file=compare_redhat_release_file,
        
        backup_db_avail_and_running_status_file = backup_db_avail_and_running_status_file,
        compare_db_avail_and_running_status_file = compare_db_avail_and_running_status_file,

        compare_firewall_status_and_config_file = compare_firewall_status_and_config_file,

        backup_info_host_information_file = backup_info_host_information_file,
        compare_info_host_information_file = compare_info_host_information_file,

        backup_info_uptime_file = backup_info_uptime_file,
        compare_info_uptime_file = compare_info_uptime_file,

        backup_info_cpu_information_file = backup_info_cpu_information_file,
        compare_info_cpu_information_file = compare_info_cpu_information_file,

        backup_info_blkid_file = backup_info_blkid_file,
        compare_info_blkid_file = compare_info_blkid_file,

        backup_info_last_reboot_file = backup_info_last_reboot_file,
        compare_info_last_reboot_file = compare_info_last_reboot_file,

        backup_info_kernel_version_file = backup_info_kernel_version_file,
        compare_info_kernel_version_file = compare_info_kernel_version_file,

        backup_info_disk_available_file = backup_info_disk_available_file,
        compare_info_disk_available_file = compare_info_disk_available_file,

        backup_info_current_FS_utilization_file = backup_info_current_FS_utilization_file,
        compare_info_current_FS_utilization_file = compare_info_current_FS_utilization_file,
        csv_file_path=csv_file_path,

    )

    module.exit_json(**result)

if __name__ == '__main__':

    main()
