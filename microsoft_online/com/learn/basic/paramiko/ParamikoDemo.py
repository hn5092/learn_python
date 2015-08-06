#coding=utf-8
'''
Created on Aug 5, 2015

@author: imad
'''
import paramiko
hostname = "192.168.80.101"
username = "root"
password = "xuyu5092"

paramiko.util.log_to_file("paramiko.log")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #允许链接不在host里面的主机
ssh.connect(hostname=hostname, username=username, password=password )
stdin,stdout,stderr = ssh.exec_command("ps")
print stdout.read()
ssh.close()
