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
import threading

def jonnyS(client, address):
    try:
    #设置超时时间
        client.settimeout(500)
    #接收数据的大小
        while True:
            buf = client.recv(2048)
    #将接收到的信息原样的返回到客户端中
            client.sendall('1')
            print buf
    #超时后显示退出
    except socket.timeout:
        print 'time out'
    client.close()
    #将接收到的信息原样的返回到客户端中
    #超时后显示退出
    #关闭与客户端的连接


HOST = 'localhost'
PORT = 8888
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(10)
while True:
    conn,addr=s.accept()
    print addr
    thread = threading.Thread(target=jonnyS, args=(conn, addr))
    thread.start()
    s.close()
