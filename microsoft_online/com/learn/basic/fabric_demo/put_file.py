#coding=utf-8
'''
Created on Aug 26, 2015

@author: imad
'''
import fabric.api
from fabric.api import *
from fabric.contrib.console import confirm
env.user = 'root'
env.hosts = ['192.168.80.101','192.168.80.102']
env.password = 'xuyu5092'
# env.gateway = ''
localpath = '__init__.py'
remotepath = '/root/tmp/python'

@task
def put_task():
    run('mkdir -p /root/tmp/python')
    with settings(warn_only=True):
        result = put(localpath,remotepath)
    if result.failed and not confirm("put file failed, Continue [Y/N]?"):
        abort("aorting file put task!")

    
    