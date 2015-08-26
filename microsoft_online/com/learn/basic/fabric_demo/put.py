#coding=utf-8
'''
Created on Aug 26, 2015

@author: imad
'''
from fabric.colors import *
from fabric.api import *
env.user = 'root'
env.roledefs = {'webserver':{'192.168.80.101'},'dbserver':{'192.168.80.102'}}
env.passswords = {'root@192.168.80.101:22':'xuyu5092','root@192.168.80.102:22':'xuyu5092'}
@roles('webserver')
def webtask():
    print yellow("install webserver")

@roles("dbserver")
def dbtask():
    print red("install dbserver")

@roles('webserver','dbserver')
def publictask():
    print green("install success")
def go():
    execute(webtask)
    execute(dbtask)
    execute(publictask)