#coding=utf-8
'''
Created on Jul 29, 2015

@author: imad
'''
import SocketServer
class MyTCPHandler(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print "{} wrote:{}".format(self.client_address[0],22)
        print self.data
        self.request.sendall(self.data.upper())
        
HOST,PORT = "localhost",99

server = SocketServer.TCPServer((HOST,PORT),MyTCPHandler)

server.serve_forever()
    
    
    
    
    
    
    
# import SocketServer,threading,socket
# class MyTCPHandler(SocketServer.BaseRequestHandler):
#     
#     def handle(self):
#         self.data = self.request.recv(1024).strip()
#         print "{} wrote:".format(self.client_address[0])
#         print self.data
#         self.request.sendall(self.data.upper())
#         
# HOST,PORT = "",9999
# 
# server = SocketServer.ThreadingTCPServer((HOST,PORT),MyTCPHandler)
# 
# server.serve_forever()