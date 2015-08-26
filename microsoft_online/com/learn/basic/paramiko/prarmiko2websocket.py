#coding=utf-8
'''
Created on 2015年7月20日

@author: Administrator
'''
from base64 import b64encode
import hashlib
import socket
import threading

import paramiko

from com.learn.basic.paramiko.ParamikoDemo2 import readacount, sshObj


#这个方法用来解析收到的二进制字符串
def parse_data(msg):
    if(len(msg)<1):
        return ''
    code_length = ord(msg[1]) & 127
 
    if code_length == 126:
        masks = msg[4:8]
        data = msg[8:]
    elif code_length == 127:
        masks = msg[10:14]
        data = msg[14:]
    else:
        masks = msg[2:6]
        data = msg[6:]
 
    i = 0
    raw_str = ''
 
    for d in data:
        raw_str += chr(ord(d) ^ ord(masks[i%4]))
        i += 1     
    return raw_str

class WebSocket(threading.Thread):
    GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    def __init__(self,conn,address,path="/"):
        threading.Thread.__init__(self)
        self.conn = conn
        self.address = address
        self.path = path
        self.handshaken = False
        self.buffer = "" 
    def run(self):
    #设置超时时间
        client.settimeout(500)
        headers = {}
    #接收数据的大小
        while True:
            #判断是否已经握手
            if self.handshaken == False:
                self.buffer += bytes.decode(self.conn.recv(1024))
                print self.buffer
                if self.buffer.find('\r\n\r\n') != -1:
                    header, data = self.buffer.split('\r\n\r\n', 1) 
                    for line in header.split("\r\n")[1:]:
                        key, value = line.split(": ", 1)
                        headers[key] = value
                        print key,value
                    headers["Location"] = ("ws://%s%s" %(headers["Host"], self.path))
                    key = headers['Sec-WebSocket-Key']
                    key = '%s'% (key)
                    #根据客户端的key计算密钥
                    token = b64encode(str(hashlib.sha1(key+ self.GUID).digest()))
                    handshake="HTTP/1.1 101 Switching Protocols\r\n"\
                    "Upgrade: websocket\r\n"\
                    "Connection: Upgrade\r\n"\
                    "Sec-WebSocket-Accept: "+bytes.decode(token)+"\r\n\r\n"
                    print str(handshake)
                    ##发送给客户端 握手信息
                    self.conn.send(str(handshake))
                    self.handshaken = True  
            else:
                while 1:
                    message = self.conn.recv(1024)
                    message = str(parse_data(message))
                    paramiko.util.log_to_file("paramiko.log")
                    global connlist
                    for x in connlist:
                        print connlist[x]
                    #允许链接不在host里面的主机
                    print "开始启动"
                    for cmd in readacount():
                        conn = sshObj(cmd,connlist)
                        conn.start()
                        print "%s已经启动"%(cmd.hostname)


HOST = 'localhost'
PORT = 99
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(10)
i=0
connlist={}
while True:
    client,addr=s.accept()
    websocket = WebSocket(client,addr)
    websocket.start()
    connlist[addr]=client #收集客户端
    i = i + 1
