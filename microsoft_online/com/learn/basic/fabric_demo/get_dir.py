#coding=utf-8
'''
Created on Aug 26, 2015

@author: imad
'''
import fabric.api
from fabric.api import *
env.user = 'root'
env.hosts = ['192.168.80.101','192.168.80.102']
env.password = 'xuyu5092'
@runs_once
def input_raw():
    return prompt("pleast inout directory ",default="/home")
def worktask(dirname):
    run("ls -l "+dirname)
@task
def go():
    getdirname = input_raw()
    worktask(getdirname)