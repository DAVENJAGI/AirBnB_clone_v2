#!/usr/bin/python3
"""generates  a tgz archive from web_static folder"""

from fabric.api import local
from time import strftime
from datetime import datetime
import os


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

        # get the size of file andprint it with the print function.
        file_size = os.path.getsize("versions/{}.tgz" .format(filename))

        print("web_static packed: versions/{}.tgz -> {}Bytes"
              .format(filename, file_size))

        return filename

    except Exception as e:
        print(f"Error: {e}")
        return None
