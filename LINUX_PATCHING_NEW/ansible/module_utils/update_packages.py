import os

import subprocess
 
def run_command(module, cmd):

    """

    Run a shell command and return its stdout and stderr.

    If the command fails, the module will fail with an error message.

    """

    try:

        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')

    except subprocess.CalledProcessError as e:

        module.fail_json(msg=f"command failed: {cmd}", stderr=e.stderr.decode('utf-8'))
 
def get_linux_distribution():

    """

    Determine the Linux distribution.

    Returns a string identifier for the distribution.

    """

    if os.path.exists('/etc/os-release'):

        with open('/etc/os-release') as f:

            lines = f.readlines()

        distro_info = {}

        for line in lines:

            if '=' in line:

                key, value = line.strip().split('=', 1)

                distro_info[key] = value.strip('"')

        return distro_info.get('ID', '').lower()

    elif os.path.exists('/etc/lsb-release'):

        with open('/etc/lsb-release') as f:

            lines = f.readlines()

        distro_info = {}

        for line in lines:

            if '=' in line:

                key, value = line.strip().split('=', 1)

                distro_info[key] = value.strip('"')

        return distro_info.get('DISTRIB_ID', '').lower()

    else:

        return ''
 
def update_packages(module):

    """

    Update packages based on the Linux distribution.

    """

    distro_name = get_linux_distribution()

    if distro_name in ['centos', 'rhel', 'fedora', 'amzn', 'amazon']:

        cmd = 'yum update -y'

    elif distro_name in ['ubuntu', 'debian']:

        cmd = 'apt-get update && apt-get upgrade -y'

    else:

        module.fail_json(msg="unsupported distribution")
 
    stdout, stderr = run_command(module, cmd)

    return stdout, stderr
