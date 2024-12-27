import os
import sys
import json
import csv
import glob
from ansible.module_utils.basic import AnsibleModule
 
# Import your custom module functions here
from ansible.module_utils.file_system_fstab import backup_fstab_list
from ansible.module_utils.file_system_mount import backup_mount_list
from ansible.module_utils.list_softwares import backup_services_list
from ansible.module_utils.monitor_process import backup_monitor_process
from ansible.module_utils.network_status import backup_network_status
from ansible.module_utils.pswd_groups_sudoers import backup_pswd_groups_sudoers
from ansible.module_utils.routing_info import backup_routing_info
from ansible.module_utils.memory_info import backup_memory_info
from ansible.module_utils.server_status import backup_server_status
from ansible.module_utils.system_build_date import backup_system_build_date
from ansible.module_utils.selinux_status import backup_selinux_status
from ansible.module_utils.network_interface_info import backup_network_info
from ansible.module_utils.network_config import backup_network_config
from ansible.module_utils.network_link_status import backup_network_link_status
from ansible.module_utils.kernel_install import backup_kernel_info
from ansible.module_utils.host_configuration import backup_hosts_info
from ansible.module_utils.dns_resolvers import backup_dns_resolvers_info
from ansible.module_utils.db_avail_and_running_status import backup_db_avail_and_running_status
from ansible.module_utils.Satellite_subscription_status import backup_satellite_subscription_status
from ansible.module_utils.Redhat_release import backup_redhat_release_info
from ansible.module_utils.firewall_status_and_configuration import backup_firewall_status_and_config
from ansible.module_utils.host_information import backup_info_host_information
from ansible.module_utils.uptime import backup_info_uptime
from ansible.module_utils.kernel_version import backup_info_kernel_version
from ansible.module_utils.last_reboot import backup_info_last_reboot
from ansible.module_utils.current_FS_utilization import backup_info_current_FS_utilization
from ansible.module_utils.disk_information import backup_info_disk_available
from ansible.module_utils.blkid_information import backup_info_blkid
from ansible.module_utils.cpu_information import backup_info_cpu_information
 
 
def main():
    module_args = dict(
        backup_path=dict(type='str', required=True),
        ip_address=dict(type='str', required=True),
        #server=dict(type='str', required=True)
       
    )
    module = AnsibleModule(
        argument_spec=module_args,
    )
   
    backup_path = module.params['backup_path']
    ip_address = module.params['ip_address']
    #server = module.params['server']
    

    '''  module.debug(f"Received backup_path: {backup_path}")
    module.debug(f"Received ip_address: {ip_address}")
    module.debug(f"Received server_config_list: {server_config_list}")

    try:

        print(f"Debug: Raw input for server_config_list: {server_config_list}")
        print(f"Debug: Type of server_config_list: {type(server_config_list)}")
        sys.stdout.flush()
    
            # Check if server_config_list is a valid list
        if isinstance(server_config_list, list):
            print("Debug: server_config_list is a valid list.")
            sys.stdout.flush()
        else:
            module.fail_json(msg="Error: server_config_list is not a valid list.")

    except Exception as e:
    # Log any errors encountered while processing the input
        print(f"Error while processing server_config_list: {e}")
        sys.stdout.flush()
        module.fail_json(msg=f"Exception while processing server_config_list: {str(e)}") '''

    
    #for server_config in server_config_list:
    
    backup_file_system_fstab = backup_fstab_list(backup_path, ip_address, "Prepatch")
    
    backup_file_system_mount = backup_mount_list(backup_path, ip_address, "Prepatch")
    
    backup_services = backup_services_list(backup_path, ip_address)

    network_status_results = backup_network_status(backup_path, ip_address, "Prepatch")
   
    pswd_groups_sudoers_results = backup_pswd_groups_sudoers(backup_path, ip_address, "Prepatch")
   
    backup_routing_dg_info_results = backup_routing_info(backup_path, ip_address, "Prepatch")
    
    backup_memory_swap_info_results = backup_memory_info(backup_path, ip_address, "Prepatch")
    
    backup_server_info_results = backup_server_status(backup_path, ip_address, "Prepatch")
    
    backup_system_build_date_results = backup_system_build_date(backup_path, ip_address, "Prepatch")
   
    backup_selinux_info_results = backup_selinux_status(backup_path, ip_address,"Prepatch")
    
    backup_network_interface_pre_results = backup_network_info(backup_path, ip_address,"Prepatch")
    
    backup_network_config_results = backup_network_config(backup_path, ip_address,"Prepatch")
   
    backup_network_link_status_results = backup_network_link_status(backup_path, ip_address,"Prepatch")
   
    backup_kernel_status_results = backup_kernel_info(backup_path, ip_address, "Prepatch")
   
    backup_host_config_results = backup_hosts_info(backup_path, ip_address, "Prepatch")
  
    backup_dns_resolvers_file_results = backup_dns_resolvers_info(backup_path, ip_address, "Prepatch")
    
    backup_db_avail_and_running_status_results = backup_db_avail_and_running_status(backup_path, ip_address, "Prepatch")
   
    backup_satellite_subscription_status_file = backup_satellite_subscription_status(backup_path, ip_address, "Prepatch")
   

    backup_redhat_release_file_results = backup_redhat_release_info(backup_path, ip_address, "Prepatch")
   
    backup_firewall_status_and_config_file_results = backup_firewall_status_and_config(backup_path, ip_address, "Prepatch")
  
    backup_info_host_information_file_results = backup_info_host_information(backup_path, ip_address, "Prepatch")
    
    backup_info_uptime_results = backup_info_uptime(backup_path, ip_address, "Prepatch")
   
    backup_info_cpu_information_results = backup_info_cpu_information(backup_path, ip_address, "Prepatch")
 
    backup_info_blkid_results = backup_info_blkid(backup_path, ip_address, "Prepatch")
    
    backup_info_last_reboot_results = backup_info_last_reboot(backup_path, ip_address, "Prepatch")
   
    backup_info_kernel_version_results = backup_info_kernel_version(backup_path, ip_address, "Prepatch")
   
    backup_info_disk_available_results = backup_info_disk_available(backup_path, ip_address, "Prepatch")
  
    backup_info_current_FS_utilization_results = backup_info_current_FS_utilization(backup_path, ip_address, "Prepatch")
   


    

    


    # Convert existing txt files to CSV
  #  csv_file_path = convert_txt_to_csv(backup_path, ip_address, server)
 
    # Check for any errors during CSV conversion
   # if isinstance(csv_file_path, dict) and csv_file_path.get("failed"):
    #    module.fail_json(**csv_file_path)
 
    result = dict(
        changed=True,  # Assuming changes have occurred
        backup_file_system_fstab=backup_file_system_fstab,
        backup_file_system_mount=backup_file_system_mount,
        network_status=network_status_results,
        pswd_groups_sudoers_res=pswd_groups_sudoers_results,
        backup_routing_dg_info=backup_routing_dg_info_results,
        backup_memory_swap_info=backup_memory_swap_info_results,
        backup_server_details=backup_server_info_results,
        backup_system_build_date_res=backup_system_build_date_results,
        backup_selinux_details=backup_selinux_info_results,
        backup_network_interface_details=backup_network_interface_pre_results,
        backup_network_config_res=backup_network_config_results,
        backup_network_link_status_res=backup_network_link_status_results,
        backup_kernel_status=backup_kernel_status_results,
        backup_host_config=backup_host_config_results,
        backup_dns_resolvers_file=backup_dns_resolvers_file_results,
        backup_db_avail_and_running_status_res=backup_db_avail_and_running_status_results,
        backup_satellite_subscription_status_file=backup_satellite_subscription_status_file,
        backup_redhat_release_file=backup_redhat_release_file_results,
        backup_firewall_status_and_config_file=backup_firewall_status_and_config_file_results,
        backup_info_host_information_file=backup_info_host_information_file_results,
        backup_info_uptime_file=backup_info_uptime_results,
        backup_info_cpu_information_file=backup_info_cpu_information_results,
        backup_info_blkid_file=backup_info_blkid_results,
        backup_info_last_reboot_file=backup_info_last_reboot_results,
        backup_info_kernel_version_file=backup_info_kernel_version_results,
        backup_info_disk_available_file=backup_info_disk_available_results,
        backup_info_current_FS_utilization_file=backup_info_current_FS_utilization_results,
      #  csv_file_path=csv_file_path,
    )
 
    module.exit_json(**result)
 
if __name__ == '__main__':
    main()
