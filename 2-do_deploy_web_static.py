#!/usr/bin/python3
"""script (based on the file 1-pack_web_static.py) that distributes an archive to your web servers,"""
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


    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}/".format(un_tgz))

        run("tar -xzf {} -C {}/".format(tmp, un_tgz))
        run("rm {}".format(tmp))
        run("mv {}/web_static/* {}/".format(un_tgz, un_tgz))
        run("rm -rf {}/web_static".format(un_tgz))
        run("rm -rf /data/web_static/currrent")
        run("ln -s {}/ /data/web_static/current".format(un_tgz))

        return True
    except:
        return False
