#!/usr/bin/python3
import fabric
from fabric.api import local
from time import strftime
from datetime import date


def do_pack():
    """Script that generetes a tgz archive from content of web_static"""

    filename = strftime("%y%m%d%H%M%S")

    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(filename))

        return "version/web_static_{}.tgz" .format(filename)

    except Exception as e:
        return None
