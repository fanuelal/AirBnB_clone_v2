#!/usr/bin/python3
"""script (based on the file 1-pack_web_static.py) 
that distributes an archive to your web servers,"""
from fabric.api import *
from datetime import datetime
from os.path import exists

env.hosts = ['3.235.242.152', '3.81.29.69']

def do_deploy(archive_path):
    """ deploy on the server"""

    if exists(archive_path) is False:
        return False
    fileName = archive_path.split('/')[-1]
    tmp = "/tmp/" + fileName
    un_tgz = '/data/web_static/releases/' + "{}".format(fileName.split('.')[0])
    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True
