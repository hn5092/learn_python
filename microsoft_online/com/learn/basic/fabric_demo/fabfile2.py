#coding=utf-8
'''
Created on Aug 26, 2015

@author: imad
'''
import fabric.api
from fabric.api import *
from fabric.contrib.console import confirm
# local("cmd") 运行本地命令
# lcd("cmd")切换本地目录
# run("cmd")执行远程命令
# sudu("cmd") sudo模式执行远程明亮
# put(localpath,remotepath) 上传文件到远程主机
# get(remotepath,localpat) 下载文件
# prompt("msg") 获得用户输入信息
# comfirm("task failed continue [Y/N]?") 提示信息确认
# reboot() 重启远程主机
# @task 标记一个任务  没有标记的在fab中是不可见的 
# @runs_onece  此任务只会执行一次 不受多台主机影响
env.user = 'root'
env.hosts = ['192.168.80.101','192.168.80.102']
env.password = 'xuyu5092'
@task
def remote_task():
    with cd('~'):
        run("hostname")
#         run("rm -r hbase2")
#         confirm("are you sure")
#         run("passwd")
#         prompt("新的 密码");    
#         prompt("新的 密码");
        print "user fabfile2"
