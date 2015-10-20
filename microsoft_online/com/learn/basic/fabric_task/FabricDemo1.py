#coding=utf-8
'''
Created on Aug 11, 2015

@author: imad
'''
from fabric.api import *
env.user = "root"
env.hosts = ['192.168.80.101','192.168.80.102']
env.password = "xuyu5092"

@runs_once
def local_task():
    local("uname -a")
def remote_task():
    with cd("/data/logs"):
        run("ls -l")
