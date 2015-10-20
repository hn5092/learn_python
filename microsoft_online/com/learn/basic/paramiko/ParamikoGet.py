#coding=utf-8
'''
Created on Aug 11, 2015

@author: imad
'''
import paramiko 
username = "root"
password = "xuyu5092"
client = paramiko.Transport(("192.168.80.104",22))
client.connect(username=username,password=password)
sftp = paramiko.SFTPClient.from_transport(client)
localhost = "/root/webapp/web-1.0.1.tar"
remotepath = "/root/webapp/1.0.1/web-1.0.1.tar"
sftp.get(remotepath,localhost)
print "下载成功"
