#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the
contents of the web_static folder
"""
from datetime import datetime
from fabric.api import local
from os import path


def do_pack():
    """ Generates a .tgz archive from web_static folder """
    try:
        if not path.exists("versions"):
            local('mkdir versions')
        time = datetime.now()
        format = "%Y%m%d%H%M%S"
        file = 'versions/web_static_{}.tgz'.format(time.strftime(format))
        local('tar -cvzf {} web_static'.format(file))
        return file
    except Exception:
        return None
