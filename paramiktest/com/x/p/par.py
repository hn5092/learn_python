#coding=utf-8
'''
Created on 2015年7月6日
@author: Administrator
'''
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #允许链接不在host里面的主机
ssh.connect(hostname='192.168.80.101',port=22,username='root', password='xuyu5092')
stdin, stdout, stderr = ssh.exec_command('cat /etc/hosts')
for x in stdout:
    print x