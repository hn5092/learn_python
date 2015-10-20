#coding=utf-8
'''
Created on Aug 11, 2015

@author: imad
'''
import paramiko 
def upload(localPath,remotepath):
    username = "root"
    password = "xuyu5092"
    client = paramiko.Transport(("192.168.80.101",22))
    client.connect(username=username,password=password)
    sftp = paramiko.SFTPClient.from_transport(client)
    sftp.put(localPath,remotepath)
    