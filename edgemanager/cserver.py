# -*- coding:utf-8 -*-
'''
Created on 2013年11月18日

@author: Zouyiran
'''

import socket
import struct
import threading
from csender import CSender
from cpacket_handler import CPacketHandler
from config.config import logger,segIP

global logger
global segIP

class CIPv4ServerTCP(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        
    def run(self):
        addr = ("", self.port)

        try:        
            self.adapter_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.adapter_sock.bind(addr)
            self.adapter_sock.listen(10)
            logger.info("IPv4 TCP服务器已经启动，服务器绑定地址%s" % str(addr))

        except Exception, e:
            logger.error("启动IPv4 TCP服务器失败，错误原因%s" % str(e))
            exit(0)

        while True:
            (edge_sock, address) = self.adapter_sock.accept()
            try:
                edge_sock.settimeout(10)
                buf = edge_sock.recv(1024)
                if not buf:
                    break
                handler = CPacketHandler(buf, address[0], segIP)#对接收数据进行处理
                handler.run()  
            except socket.timeout:
                pass
            edge_sock.close()

class CIPv4ServerUDP(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port

    def run(self):
        addr = ("", self.port)
        try:                    
            adapter_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)          
            adapter_sock.bind(addr) 
            logger.info("IPv4 UDP服务器已经启动，服务器绑定地址%s" % str(addr))
        except Exception, e:
            logger.error("启动IPv4 UDP服务器失败，错误原因%s" % str(e))
            exit(0)

        while True:
                buf,address = adapter_sock.recvfrom(1024)
                if not buf:
                    break
                handler = CPacketHandler(buf, address[0],segIP)#对接收数据进行处理
                handler.run()  
        self.adapter_sock.close()
        
class CIPv6ServerTCP(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port     

    def run(self):      
        addr = ("", self.port)
        try:            
            self.adapter_sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)           
            self.adapter_sock.bind(addr)
            self.adapter_sock.listen(10)
            logger.info("IPv6 TCP服务器已经启动，服务器绑定地址%s" % str(addr))  
        except Exception, e:
            logger.error("启动IPv6 TCP服务器失败，错误原因%s" % str(e))
            exit(0)
        
        while True:
            (edge_sock, address) = self.adapter_sock.accept()
            try:
                edge_sock.settimeout(10)
                buf = edge_sock.recv(1024)
                if not buf:
                    break
                handler = CPacketHandler(buf, address[0],segIP)
                handler.run()  
            except socket.timeout:
                pass
            edge_sock.close()

class CIPv6ServerUDP(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port       

    def run(self):
        addr = ("", self.port)
        try:      
            self.adapter_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            self.adapter_sock.bind(addr)
            logger.info("IPv6 UDP服务器已经启动，服务器绑定地址%s" % str(addr))  
        except Exception, e:
            logger.error("启动IPv6 UDP服务器失败，错误原因%s" % str(e))
            exit(0)
        while True:
                buf,address = self.adapter_sock.recvfrom(1024)
                if not buf:
                    break
                handler = CPacketHandler(buf, address[0], segIP)
                handler.run()  
        self.adapter_sock.close()

#-----------------------------------------------------
class CControlMSGServer(threading.Thread):
    """接收ConfigManager传来数据包并解析出边缘网关mac地址，采控器地址，寄存器地址及控制数据并下发"""
    def __init__(self, port):#controlmsg_packet格式（segmac, scmac, register, controldata）
        threading.Thread.__init__(self)
        self.port = port

    def run(self):
        addr = ("", self.port)#addr监听地址 和端口号，本端
        try:    
            self.controlMsg_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socket.SOCK_STREAM：TCP
            
            self.controlMsg_sock.bind(addr)
            self.controlMsg_sock.listen(10)#最多允许10个连接同时连进来，而后来的连接会被拒绝掉
#             logger.info("%s %di Ipv6 UDP server is starting..."%addr)
        except:
            pass
            exit(0)
#             logger.error("%s %d failed to start Ipv6 UDP server."%addr)
        while True:
            (cmsg_sock, address) = self.controlMsg_sock.accept()#address，对端
            cmsg_sock.settimeout(10)
            cmsg_pdu = cmsg_sock.recv(1024)#1024：buffer_size  
            print "received a cmsg_pdu"
            if not cmsg_pdu:
                break
            self.cmsgPacketHandler(cmsg_pdu)               
        self.controlMsg_sock.close()
          
    def cmsgPacketHandler(self,packet):
        """解析收到的控制信息数据包，并下发至采控器端"""
        segmac = packet[0:4]#边缘网关地址
        print "segmac"
        segmac=struct.unpack("!I", segmac)[0]
        print segmac
        self.segmac=self.convertmac(segmac,4)
        
        scmac = packet[4:12]#采控器地址
        print "scmac",scmac
        scmac=struct.unpack("!Q", scmac)[0]
        print scmac
        self.scmac=self.convertmac(scmac,8)
        
        register = packet[12:14]#寄存器地址
        self.register=struct.unpack("<H",register)[0]
#         self.register=hex(register)
        print self.register 
        controldata = packet[14:16]#控制数据
        self.controldata=struct.unpack("<H",controldata)[0]
        print self.controldata
        print "cmsgPacketHandler"
        sender=CSender(self.segmac,self.scmac,self.register,self.controldata)
        sender.run()
        print "CSender ending..."
        
    def convertmac(self, macNum, length):
        """将整数转换成给定长度的ip地址"""
        macip = []
        for i in range(length):
            bytestr=macNum %256
            macip.append(str(bytestr))
            macNum/=256
# 
        print '.'.join(macip[::-1])
        return '.'.join(macip[::-1]) 

        
