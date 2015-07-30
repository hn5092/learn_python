#coding=utf-8
'''
Created on 2015年7月20日

@author: Administrator
'''
from base64 import b64encode
import hashlib
import socket
import threading

from IPython.external import path
from IPython.parallel.client.remotefunction import remote

from com.learn.basic.socketDemo.socketdclient1 import sendMessage


GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

def jonnyS(client, address):
#设置超时时间
    client.settimeout(500)
    handshaken = False
    headers =''
    index = 0
    buffer = "" 
#接收数据的大小
    while True:
        if handshaken == False:
                print ('Socket%s Start Handshaken with %s!' % (client,address))
                buffer += bytes.decode(client.recv(1024))
                if buffer.find('\r\n\r\n') != -1:
                    header, data = buffer.split('\r\n\r\n', 1)
                    for line in header.split("\r\n")[1:]:
                        l=line.split(':')
                        headers[l[0]]=l[1]
                    
 
                    headers["Location"] = ("ws://%s%s" %(headers["Host"], path))
                    key = headers['Sec-WebSocket-Key']
                    key = '%s'% (key)
                    print str(hashlib.sha1(key+ GUID).digest())
                    #处理
                    token = b64encode(str(hashlib.sha1(key+ GUID).digest()))

                    handshake="HTTP/1.1 101 Switching Protocols\r\n"\
                    "Upgrade: websocket\r\n"\
                    "clientection: Upgrade\r\n"\
                    "Sec-WebSocket-Accept: "+bytes.decode(token)+"\r\n\r\n"
                    client.send(str(handshake))
                    handshaken = True  
                    print ('Socket %s Handshaken with %s success!' %(index, address))  
                    sendMessage('Welcome, ' + address[0] + ' !')  


HOST = 'localhost'
PORT = 99
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(10)
while True:
    client,addr=s.accept()
    print addr
    thread = threading.Thread(target=jonnyS, args=(client, addr))
    thread.start()

