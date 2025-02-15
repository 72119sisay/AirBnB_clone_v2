#!/usr/bin/python3
""" Fabric script that creates and distributes the archive"""

import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once

env.hosts = ['34.201.61.173', '100.25.34.184']


@runs_once
def do_pack():
    """ Create a tar archive of the web_static folder"""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    date = datetime.now()
    filename = "web_static_{}{}{}{}{}{}.tgz".format(
        date.year, date.month, date.day, date.hour, date.minute, date.second
    )
    local("tar -cvzf versions/{} web_static".format(filename))
    path = "versions/{}".format(filename)
    if os.path.exists(path):
        return path
    else:
        return None


def do_deploy(archive_path):
    """ Deploy the web_static to the web server """
    if not os.path.exists(archive_path):
        return False
    put(archive_path, "/tmp/")
    filename = archive_path.split("/")[-1]
    foldername = filename.split(".")[0]
    run("mkdir -p /data/web_static/releases/{}/".format(foldername))
    run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
        .format(filename, foldername))
    run("rm /tmp/{}".format(filename))
    run("mv /data/web_static/releases/{}/web_static/*\
         /data/web_static/releases/{}/".format(foldername, foldername))
    run("rm -rf /data/web_static/releases/{}/web_static".format(foldername))
    run("rm -rf /data/web_static/current")
    run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
        .format(foldername))
    return True


def deploy():
    """ Call the do_pack and do_deploy functions"""
    path = do_pack()
    if not path:
        return False
    return do_deploy(path)
