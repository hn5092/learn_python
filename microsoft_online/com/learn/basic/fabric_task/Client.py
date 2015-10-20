#coding=utf-8
'''
Created on Oct 13, 2015

@author: imad
'''



import paramiko
class Client():
    def __init__(self,ip="127.0.0.1",port=22,username="root",pwd="xuyu5092"):
        self.port = port
        self.username = username
        self.pwd = pwd
        self.ip = ip
        self.client = paramiko.Transport((self.ip,self.port))
        self.client.connect(username=self.username,password=self.pwd)
        self.sftp = paramiko.SFTPClient.from_transport( self.client)
    def upload(self,localPath,remotePath):
        self.sftp.put(localPath,remotePath)
    def download(self,remotePath,localPath):
        self.sftp.get(remotePath,localPath)
client = Client(ip = "192.168.80.101")
# print "this is path : "+webAppPath+env.version+"/web-%s.tar" % (env.version)
# client.download(env.webAppPath+env.version+"/web-%s.tar" % (env.version),env.webAppPath+"web-%s.tar" % (env.version))
       