#!/usr/bin/python3
"""distributes archive to web servers"""

from fabric.api import *
from datetime import datetime
import os

env.host = ['100.25.133.127', '34.224.63.130']
env.user = 'ubuntu'
env.key_filename = '~/ssh/ssh_keypairs'


def do_deploy(archive_path):
    """deploy files to server"""

    if not os.path.exists(archive_path):
        print("Archive does not exist")
        return False
    
    try:
        # upload archive using the put command
        put(archive_path, '/tmp/')

        # create target directory to upload the archive to
        archive_name = archive_path.split('/')[-1]
        folder = ('/data/web_static/releases/{}' .format(
                archive_name.split('.')[0]
                ))

        run('sudo mkdir -p {}' .format(folder))

        # uncompress the archive to the folder and delete  .tgz
        run('sudo tar -xzf /tmp/{} -C {}'.format(archive_name, folder))

        # remove the archive
        run('sudo rm /tmp/{}' .format(archive_name))

        # move the contents to web_static
        run('sudo mv {}/web_static/* {}/' .format(folder, folder))

        # remove extraneous web_static directory
        run('sudo rmdir {}/web_static' .format(folder))

        # delete pre existing symbolic link
        run('sudo rm -rf /data/web_static/current')

        present_link = '/data/web_static/current'

        # create a new symbollic linked to the new code version
        run('sudo ln -sf {} {}' .format(folder, present_link))

        #print new version deployed and return true
        print("New version deployed")
        return True

    except Exception as e:
        print(f"Error during deployment: {e}")
        return False

if __name__ == "__main__":
    do_deploy("/versions/archive_path.tgz")
