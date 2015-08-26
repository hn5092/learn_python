#coding=utf-8
'''
Created on Aug 5, 2015

@author: imad
'''
import time

import paramiko


hostname = "192.168.80.101"
username = "root"
password = "xuyu5092"
print dir(paramiko)
# paramiko.util.log_to_file("paramiko.log")
# ssh = paramiko.SSHClient
# #
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #�������Ӳ���host���������
# ssh.connect(hostname=hostname, username=username, password=password )
# stdin,stdout,stderr = ssh.exec_command("top")
# print stdout.read()
# chancel = ssh.invoke_shell()
# chancel.send("top \n")
# # time.sleep(3)
# # resp = chancel.recv(9999)
# # print resp
# while 1:
#     resp = chancel.recv(9999).replace("[m", "").replace("[H", "").replace("[4;1H", "").replace("[K", "").replace("[7m", "").strip()
# #     print resp.replace("[m", "").replace("[H", "").replace("[4;1H", "").replace("[K", "").replace("[7m", "")
#     for x in resp.split("\n"):
#         if x.startswith("Cpu"):
#             print x
# ssh.close()
