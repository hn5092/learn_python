#coding=utf-8
'''
Created on Aug 26, 2015

@author: imad
'''
from fabric.colors import *
from fabric.api import *
env.user = 'root'
env.roledefs = {'master':{'192.168.80.101'},
                'yarn':{'192.168.80.103'},
                'zookeeper':{'192.168.80.102','192.168.80.104','192.168.80.105'}
                }
env.passswords = {'root@192.168.80.101:22':'xuyu5092',
                  'root@192.168.80.102:22':'xuyu5092',
                  'root@192.168.80.103:22':'xuyu5092',
                  'root@192.168.80.104:22':'xuyu5092',
                  'root@192.168.80.105:22':'xuyu5092'
                  }

@roles('zookeeper')
def zookeepertask():
    run('/itcast/zookeeper-3.4.5/bin/zkServer.sh stop')
    print green("zookeeper启动完毕")

@roles("master")
def mastertask():
    run('/itcast/hadoop-2.2.0/sbin/stop-dfs.sh')
    print green("hdfs启动完毕")

@roles('yarn')
def yarntask():
    run('/itcast/hadoop-2.2.0/sbin/stop-yarn.sh')
    print green("yarn启动完毕")
def boot():
    execute(yarntask)
    execute(mastertask)
    execute(zookeepertask)