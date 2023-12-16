#!/usr/bin/python3
"""distributes archive to web servers"""

from fabric.api import *
from datetime import datetime
from os import path

env.host = ['100.25.133.127', '34.224.63.130']
env.user = 'ubuntu'
enf.key_filename = '~/ssh/ssh_keypairs'


def do_deploy(archive_path):
    """deploy files to server"""

    try:
        if not (path.exists(archive_path)):
            return False

        put(archive_path, '/tmp/')

        timestamp = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'
            .format(timestamp))

        run('sudo tar -xzf /tmp/web_static_{}.tgz -C \
                /data/web_static/releases/web_static_{}/'
            .formart(timestamp, timestamp))

        run('sudo rm /tmp/web_static_{].tgz' .format(timestamp))

        run('sudo mv /data/web_staticc/releases/web_static_{}/web_static/* \
                /data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        run('sudo rm -rf /data/web_static/releases/ \
                web_static_{}/web_static' .format(timestamp))

        run('sudo rm -rf /data/web_static/current')

        run('sudo ln -s /data/web_static/releases/ \
                web_static_{}/ /data/web_static/current' .format(timestamp))

    except Exception as e:
        return False

    return True
