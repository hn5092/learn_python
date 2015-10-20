# coding=utf-8
'''
Created on Aug 26, 2015

@author: imad
'''
from _bsddb import version
import sys

from fabric.api import *
from fabric.colors import *
from fabric.contrib.console import confirm


# env.gateway = "xxx"
env.user = 'root'
env.password = 'xuyu5092'
env.roledefs = {'master':{'192.168.80.101'},
                'web':{'192.168.80.102', '192.168.80.104', '192.168.80.105'},
                'database':{'192.168.80.103'}
                }
env.passswords = {'root@192.168.80.101:22':'xuyu5092',
                  'root@192.168.80.102:22':'xuyu5092',
                  'root@192.168.80.103:22':'xuyu5092',
                  'root@192.168.80.104:22':'xuyu5092',
                  'root@192.168.80.105:22':'xuyu5092'
                  }
env.host_string = "root@xym01"
# env.gateway = ''
env.webAppPath = '/root/webapp/'
global localpath
@roles("master")
def put_task():
    run("rm -rf %s" % (env.webAppPath + env.filename))
    with settings(warn_only=True):
        result = put(env.localPath, env.webAppPath)
    if result.failed and not confirm("put file failed, Continue [Y/N]?"):
        abort("aorting file put task!")
    else:
        print "upload file success"
    with cd(env.webAppPath):
        uncompressWebApp()
    for key in env.roledefs :
        if not key == "master":
            for ip in env.roledefs[key]:
                run("scp /root/webapp/%s/%s-%s.tar root@%s:%s" % (env.version, key, env.version, ip, env.webAppPath))
                
                
def uncompressWebApp():
    run("tar -zxf %s" % (env.webAppPath + env.filename))
    result = run("ls %s" % (env.version))
    print "this is result : %s" % (result) 
    if "database-%s.tar" % (env.version) in result and "web-%s.tar" % (env.version) in result:
        print "uncompressWabApp file success"
    run("rm -rf %s" % (env.webAppPath + env.filename))
    # todo
   
        
@roles("web")
def deployWeb():
    with cd(env.webAppPath):
        uncompress("web")
        
        
@roles("database")
def deployDataBase():
    with cd(env.webAppPath):
        uncompress("database")
        
    
def uncompress(type):
    run("tar -zxf %s-%s.tar" % (type, env.version))
    result = run("ls")
    print "this is result : %s" % (result) 
    if "%s-%s" % (type, env.version) in result:
        print "uncompress file success"
    run("rm -rf %s-%s.tar" % (type, env.version))
        
def boot():
    env.version = raw_input("enter version : ")
    env.filename = "%s.tar" % (env.version)
    env.localPath = "E:\DeployWebApp\%s" % (env.filename)
    execute(put_task)
    execute(deployWeb)
    execute(deployDataBase)
    
#     client =  Client(ip = "192.168.80.101")
#     client.upload(localPath, webAppPath)
#     execute(zookeepertask)
#     execute(mastertask)
#     execute(yarntask)
