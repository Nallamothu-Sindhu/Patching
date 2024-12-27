---
- name: Test my custom module
  hosts: target
  remote_user: ec2-user
  become: yes
  gather_facts: no
  vars:
     ansible_python_interpreter: /usr/bin/python3
     ansible_action: "pre"
     server_config_list: 
       - config1
       - config2

  tasks:
    # Ensure the /backup directory exists
    - name: Ensure /backup directory exists
      file:
        path: /backup
        state: directory
        mode: '0755'

    # Ensure the /final directory exists
    - name: Ensure /final directory exists
      file:
        path: /final
        state: directory
        mode: '0755'

    # Ensure the prepatch directory exists
    - name: Ensure the prepatch directory exists
      file:
        path: "/final/{{ ansible_ssh_host }}_Prepatch"
        state: directory
        mode: '0755'
      when: ansible_action == "pre"

    # Run the custom pre-patch module
    - name: Run the my custom module pre reboot
      pre_patch_module:
        backup_path: /final  # Specify the backup path
        ip_address: "{{ ansible_ssh_host }}"
        server_config_list: "{{ server_config_list }}"
      register: mount_backup_result
      when: ansible_action == "pre"

  

    # Ensure the postpatch directory exists
    - name: Ensure the postpatch directory exists
      file:
        path: "/final/{{ ansible_ssh_host }}_Postpatch"
        state: directory
        mode: '0755'
      when: ansible_action == "post"

    # Run the custom post-patch module
    - name: Run the my custom module post reboot
      post_patch_module:
        backup_path: /final # Specify the backup path
        ip_address: "{{ ansible_ssh_host }}"
      register: mount_backup_result_post
      when: ansible_action == "post"

   
