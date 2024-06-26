#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers
"""
from fabric.api import run, put, env, local
from os.path import exists
from os import path
from datetime import datetime

env.hosts = ['100.26.232.74', '100.25.158.41']


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


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    Returns False if the file at the path archive_path doesn't exist
    """
    if exists(archive_path) is False:
        return False
    try:
        filename = archive_path.split("/")[-1]
        unfile = filename.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("mkdir -p {}{}".format(path, unfile))
        run("tar -xzf /tmp/{} -C {}{}".format(filename, path, unfile))
        run("rm -rf /tmp/{}".format(filename))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, unfile))
        run('rm -rf {}{}/web_static'.format(path, unfile))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, unfile))
        return True
    except Exception:
        return False
