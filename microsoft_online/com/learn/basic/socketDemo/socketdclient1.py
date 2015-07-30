#coding=utf-8
import hashlib, struct

import socket
import threading,random
from base64 import b64encode, b64decode
from xml import parsers
 
connectionlist = {}
 
def sendMessage(message):
    global connectionlist
    for connection in connectionlist.values():
        connection.send(str(send_data(message)))
        
def deleteconnection(item):
    global connectionlist
    del connectionlist['connection'+item]
     

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
    
def send_data(raw_str):
    back_str = []
 
    back_str.append('\x81')
    data_length = len(raw_str)
 
    if data_length < 125:
        back_str.append(chr(data_length))
    else:
        back_str.append(chr(126))
        back_str.append(chr(data_length >> 8))
        back_str.append(chr(data_length & 0xFF))
 
    back_str = "".join(back_str) + raw_str
    return back_str
        
class WebSocket(threading.Thread):
    
    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    
    def __init__(self,conn,index,name,remote, path="/"):
        threading.Thread.__init__(self)
        self.conn = conn
        self.index = index
        self.name = name
        self.remote = remote
        self.path = path
        self.buffer = ""     
    def run(self):
        print('Socket%s Start!' % self.index)
        headers = {}
        self.handshaken = False
 
        while True:
            if self.handshaken == False:
                print ('Socket%s Start Handshaken with %s!' % (self.index,self.remote))
                self.buffer += bytes.decode(self.conn.recv(1024))

                if self.buffer.find('\r\n\r\n') != -1:
                    header, data = self.buffer.split('\r\n\r\n', 1)
                    for line in header.split("\r\n")[1:]:
                        key, value = line.split(": ", 1)
                        headers[key] = value
 
                    headers["Location"] = ("ws://%s%s" %(headers["Host"], self.path))
                    key = headers['Sec-WebSocket-Key']
                    key = '%s'% (key)
                    print str(hashlib.sha1(key+ self.GUID).digest())
                    #处理
                    token = b64encode(str(hashlib.sha1(key+ self.GUID).digest()))

                    handshake="HTTP/1.1 101 Switching Protocols\r\n"\
                    "Upgrade: websocket\r\n"\
                    "Connection: Upgrade\r\n"\
                    "Sec-WebSocket-Accept: "+bytes.decode(token)+"\r\n\r\n"
                    
                    self.conn.send(str(handshake))
                    self.handshaken = True  
                    print ('Socket %s Handshaken with %s success!' %(self.index, self.remote))  
                    sendMessage('Welcome, ' + self.name + ' !')  
                   
            else:
                mm=parse_data(self.conn.recv(64))
                print(mm)
                self.buffer +=mm.decode('utf-8')
                self.buffer = str(self.buffer)
                print type(self.buffer)
                if self.buffer.find("\xFF")!=-1:
                    s = self.buffer.split("\xFF")[0][1:]
                    if s=='quit':
                        print ('Socket%s Logout!' % (self.index))
                        sendMessage(self.name+' Logout')
                        deleteconnection(str(self.index))
                        self.conn.close()
                        break
                    else:
                        print ('Socket%s Got msg:%s from %s!' % (self.index,s,self.remote))
                        sendMessage(self.name+':'+s)
            self.buffer = ""
  
     
class WebSocketServer(object):
    def __init__(self):
        self.socket = None
    def begin(self):
        print( 'WebSocketServer Start!')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("127.0.0.1",12345))
        self.socket.listen(50)
         
        global connectionlist
         
        i=0
        while True:
            connection, address = self.socket.accept()
            username=address[0]
                 
            newSocket = WebSocket(connection,i,username,address)
            newSocket.start()
            connectionlist['connection'+str(i)]=connection
            i = i + 1
 
if __name__ == "__main__":
    server = WebSocketServer()
    server.begin()