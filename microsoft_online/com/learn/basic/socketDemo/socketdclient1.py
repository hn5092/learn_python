#coding=utf-8
'''
Created on 2015年7月21日

@author: Administrator
'''
from __future__ import with_statement
from contextlib import closing
import multitask
import socket
def client_handler(sock):
    with closing(sock):
        while True:
            data = (yield multitask.recv(sock, 1024))
            if not data:
                break
            yield multitask.send(sock, data)

def echo_server(hostname, port):
    addrinfo = socket.getaddrinfo(hostname, port,
                                  socket.AF_INET,
                                  socket.SOCK_STREAM)
    
    (family, socketype, porot, canonname, sockaddr) = addrinfo[0]
    with closing(socket.socket(family,
                               socketype,
                               porot)) as sock:
        sock.setsockopt(socket.SOL_SOCKET,
                        socket.SO_REUSEADDR, 1)
        sock.bind(sockaddr)
        sock.listen(5)
        while True:
            multitask.add(client_handler((
                        yield multitask.accept(sock))[0]))
                        
if __name__ == '__main__':
    import sys
    hostname = '192.168.2.102'
    port = 1111
    
    if len(sys.argv) > 1:
        hostname = sys.argv[1]
    
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    
    multitask.add(echo_server(hostname, port))
    
    try:
        multitask.run()
    except KeyboardInterrupt:
        pass
