#coding=utf-8
'''
Created on Jul 30, 2015

@author: imad
'''
#coding=utf-8
'''
Created on 2015年7月20日

@author: Administrator
'''
import socket
HOST = 'localhost'
PORT = 8888
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print type(s)
s.bind((HOST,PORT))
s.listen(10)
conn,addr=s.accept()
while True:
    print type(conn)
    print addr
    #接收数据的大小
    buf = conn.recv(1024)
    #将接收到的信息原样的返回到客户端中
    conn.sendall('1')
conn.close()