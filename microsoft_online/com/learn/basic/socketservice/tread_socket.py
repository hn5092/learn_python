#coding=utf-8
'''
Created on 2015年7月20日

@author: Administrator
'''
import socket
import threading
import time
import os

def jonnyS(client, address):
    try:
    #设置超时时间
        client.settimeout(500)
    #接收数据的大小
        while True:
            buf = client.recv(2048)
            cmd = os.popen(buf)
            print cmd.read()
            time.sleep(5)
    #将接收到的信息原样的返回到客户端中
            client.sendall('1232133123')
            print buf
    #超时后显示退出
    except socket.timeout:
        print 'time out'
    client.close()
    #将接收到的信息原样的返回到客户端中
    #超时后显示退出
    #关闭与客户端的连接


HOST = 'localhost'
PORT = 99
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(10)
while True:
    conn,addr=s.accept()
    print addr
    print type(conn)
    #设置多线程
    thread = threading.Thread(target=jonnyS, args=(conn, addr))
    #启动线程开始run
    thread.start()

