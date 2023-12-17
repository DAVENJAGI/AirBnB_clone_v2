#!/usr/bin/python3
"""generates  a tgz archive from web_static folder"""

from fabric.api import *
from time import strftime
from datetime import datetime
import os


env.hosts = ['100.25.133.127', '34.224.63.130']
env.user = 'ubuntu'
env.key_filename = '~/ssh/ssh_keypairs'


@runs_once
def do_pack():
    """Script that generetes a tgz archive from content of web_static"""

    try:

        # create an archive file name
        date = datetime.utcnow()
        filename = ("web_static_{}{:02}{:02}{:02}{:02}{:02}" .format(
            date.year, date.month, date.day, date.hour, date.minute,
            date.second))

        # create an archive version folder
        local("mkdir -p versions")
        local("tar -czvf versions/{}.tgz web_static"
              .format(filename))

        # join the new pack to the versions folder
        file_path = os.path.join("versions", (filename))
#        print(file_path)

        # get the size of file and print it with the print function.
        file_size = os.path.getsize("versions/{}.tgz" .format(filename))

        print("web_static packed: versions/{}.tgz -> {}Bytes"
              .format(filename, file_size))

        return filename

    except Exception as e:
        print(f"Error: {e}")
        return None


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
        run('tar -xzf /tmp/{} -C {}'.format(archive_name, folder))

        # remove the archive
        run('rm /tmp/{}' .format(archive_name))

        # move the contents to web_static
        run('mv {}/web_static/* {}/' .format(folder, folder))

        # remove extraneous web_static directory
        run('rmdir {}/web_static' .format(folder))

        # delete pre existing symbolic link
        run('rm -rf /data/web_static/current')

        present_link = '/data/web_static/current'

        # create a new symbollic linked to the new code version
        run('ln -sf {} {}' .format(folder, present_link))

        # print new version deployed and return true
        print("New version deployed")
        return True

    except Exception as e:
        print(f"Error during deployment: {e}")
        return False


def deploy():
    """creates and distributes an archiveto your web servers
    using functiondeploy"""
    archive_path = do_pack()
    if not archive_path:
        print("No archive path found")
        return False

    return do_deploy(archive_path)
