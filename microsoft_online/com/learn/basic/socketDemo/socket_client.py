#coding=utf-8
'''
Created on 2015年7月20日

@author: Administrator
'''
import socket
HOST = '127.0.0.1'
PORT = 99
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))
while True:
    s.sendall(raw_input("shuru"))
    data = s.recv(1024)
    print data
s.close()
