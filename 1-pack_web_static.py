#!/usr/bin/python3
"""Fabric script that generates a
.tgz archive from the contents of the web_static
folder of your AirBnB Clone repo"""

from fabric.api import *
from datetime import datetime


def do_pack():
    """the method that pack the folder with date"""
    local("sudo mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    fileName = "versions/web_static_{}.tgz".format(date)
    path = local("sudo tar -cvzf {} web_static".format(fileName), capture=True)
    if path.succeeded:
        return path
    else:
        return None
