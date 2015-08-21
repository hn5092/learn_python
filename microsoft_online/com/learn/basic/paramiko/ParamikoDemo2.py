#coding=utf-8
'''
Created on Aug 5, 2015

@author: imad
'''
import threading
import paramiko
from time import sleep
#这个方法用来发送消息  转换成为二进制
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
#读取账号记录
class account():
    def __init__(self,info):
        info = info.split(" ")
        self.hostname = info[0]
        self.pwd = info[1]
        self.username = info[2]
def readacount ():
    f = open("e:\\hadoop.txt")
    l = [ x for x in f.read().split('\n') if not x == ""]
    accountlist = []
    for info in l:
        accountlist.append(account(info))
    return accountlist
#读取CPU信息       
class cpuinfo():
    def __init__(self,hostname,cpu):
        l = self.clearinfo(cpu)
        self.hostname = "xym%s" %(hostname[-1])
        for i in l :
            if i.endswith("us"):
                self.us = i.split("%")[0]
            elif i.endswith("id"):
                print "this is i :%s" %(i)
                self.id = i.split("%")[0]
            elif i.endswith("sy"):
                print "this is i :%s" %(i)
                self.sy = i.split("%")[0]
            elif i.endswith("wa"):
                print "this is i :%s" %(i)
                self.wa = i.split("%")[0]
                
    def clearinfo(self,cpu):
        #Cpu(s):  0.1%us,  0.4%sy,  0.0%ni, 96.8%id,  2.7%wa,  0.0%hi,  0.0%si,  0.0%st  
        #提取冒号后面的然后空格换成无,用逗号分隔
        l = cpu.split(':')[-1].strip().replace(" ","").split(",")
        return l

#读取MEMORY信息
class memory():
    def __init__(self,hostname,mem):
        l = self.clearinfo(mem)
        self.hostname = "xym%s" %(hostname[-1])
        print l 
        for i in l :
            if i.endswith("total"):
                self.total = i.split("k")[0]
                print self.total
            elif i.endswith("used"):
                print "this is i :%s" %(i)
                self.used = i.split("k")[0]
            elif i.endswith("free"):
                print "this is i :%s" %(i)
                self.free = i.split("k")[0]
            elif i.endswith("buffers"):
                print "this is i :%s" %(i)
                self.buffers = i.split("k")[0]
                
    def clearinfo(self,mem):
        #Mem:    873536k total,   769536k used,   104000k free,   135880k buffers  
        #提取冒号后面的然后空格换成无,用逗号分隔
        l= mem.split(":")[1].strip().replace(" ","")
        return l.split(",")
        
class sshObj(threading.Thread):
   
    def __init__(self,cmd,connlist):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.connlist = connlist
        
    #清洗数据
    def cleardata(self):
        l = self.info.split("\n")
        cpu = ""
        mem = ""
        for a in l:
            if a.startswith("Cpu"):
                print a
                cpu = cpuinfo(self.cmd.hostname,a)
            if a.startswith("Mem"):
                mem = memory(self.cmd.hostname,a)
        return cpu,mem
    #进行连接并得到值对象
    def run(self):
        print "this is %s" %(self.cmd.hostname)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.cmd.hostname, username=self.cmd.username, password=self.cmd.pwd )
        cannel = ssh.invoke_shell()  #获取一个命令调用
        cannel.send("top \n")#发送一个命令
        #防止有时候发送不成功  再次发送指令
        while "VIRT" not in cannel.recv(9999):
            cannel.send("top \n")
        else:    
            while True:
                #接受命令
                self.info = cannel.recv(9999).replace("[m", "").replace("[H", "").replace("[4;1H", "").replace("[K", "").replace("[7m", "")
                print self.info
                c,m = self.cleardata()
                #判断
                if not isinstance(c, str):
                    for conn in self.connlist:
                        self.connlist[conn].sendall(send_data("%s:%s:%s:%s:%s:%s"%('cpu',c.hostname,c.us,c.sy,c.id,c.wa)))
                if not isinstance(m, str):
                    for conn in self.connlist:
                        self.connlist[conn].sendall(send_data("%s:%s:%s:%s:%s:%s"%('mem',m.hostname,m.total,m.used,m.free,m.buffers)))
        
        ssh.close()    

# paramiko.util.log_to_file("paramiko.log")
#  #允许链接不在host里面的主机
# for cmd in readacount():
#     conn = sshObj(cmd)
#     conn.start()
#     print "%s已经启动"%(cmd.hostname)
