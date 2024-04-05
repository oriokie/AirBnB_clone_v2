#!/usr/bin/python3
"""
Fabric Module for deployment
"""
from datetime import datetime
from fabric.api import env, local, put, run
from os.path import exists


def do_pack():
    """ Generates a .tgz archive from web_static folder """
    try:
        if not exists("versions"):
            local('mkdir versions')
        time = datetime.now()
        format = "%Y%m%d%H%M%S"
        file = 'versions/web_static_{}.tgz'.format(time.strftime(format))
        local('tar -cvzf {} web_static'.format(file))
        return file
    except Exception:
        return None


env.hosts = ['100.26.232.74', '100.25.158.41']


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


def deploy():
    """
    Call do_pack and do_deploy
    """
    try:
        archive_path = do_pack()
    except Exception:
        return False

    return do_deploy(archive_path)
