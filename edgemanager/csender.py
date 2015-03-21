# -*- coding:utf-8 -*-
'''
Created on 2013年11月18日

@author: Zouyiran
'''

import struct
import socket
import pickle

from function.crc import getCRC  
from function.mac2bytestr import convertmac

global logger

class CSender(object):
    def __init__(self, segmac, scmac, register, controldata):
        self.segmac = segmac
        self.scmac = scmac
        self.register = register
        self.controldata = controldata
        self.session_id = 0
        
    def run(self,filename = 'seg_ip.txt'):       
        ipfile = open(filename,'rb')
        ipdict = pickle.load(ipfile)#ipdict {'segmac':'','segmac_port':''}
        ipfile.close()
        flag = self.segmac in ipdict.keys()
        if flag:
            ip = ipdict[self.segmac]
            port = ipdict[self.segmac+'_port']
        else:
            print 'can not find segmac(',self.segmac,')in configure file!' 
                      
        TH = self.controldata >> 8 
        TL = self.controldata & 0x00FF
        
        pdu = self.makePDU(self.segmac, self.scmac, self.register, TH, TL)
        try:
            sent = self.send(pdu, ip, port)
            if sent != None:
                print 'successfully sent control message'  
        except:
            print "failed to send control message"
            pass              

    def makePDU(self, segMac, scMac, registerAddr, TH, TL):
        header = struct.pack("!B", 0xCC)#帧头
        scmac = struct.pack("!Q", convertmac(scMac))#采控器地址
        cmd = struct.pack("!B", 0x06)#下发控制命令
        register = struct.pack("<H", registerAddr)#寄存器地址
        
        try:
            data = TH << 8 | TL
            print data
            data = struct.pack("<H", data)#数据
        except:
            data = struct.pack("<H", 0x00)

        tail = struct.pack("!B", 0xDD)#帧尾
        pdu = scmac + cmd + register +  data# 要送去做CRC的字段
        format = "!" + "B" * len(pdu)
        crc = struct.pack("!H", getCRC(list(struct.unpack(format, pdu))))#unpack之后是元组，转成列表

        pdu = header + pdu + crc + tail
        pdu = self.makeMBAPHeader(segMac, pdu) + pdu
        return pdu

    def makeMBAPHeader(self, segMac, pdu):
        session = struct.pack("!H", self.session_id)
        proto = struct.pack("!H", 0)
        length = struct.pack("<H", len(pdu) + 4)
        segmac = struct.pack("!I", convertmac(segMac))
        mbap_header = session + proto + length + segmac
        return mbap_header
    
    def send(self, pdu, addr, port):
        iplist = addr.split(".")
        if len(iplist) == 4:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        try:
            sock.connect((addr, port))
            logger.info("connected to %s %s" %addr %port)
        except:
            print "csender connect failed"
            logger.info("failed to connect to %s %s" %addr %port)
            sock.close()
            return None

        try:            
            ret = sock.send(pdu) 
            logger.info("sent pdu to %s %s " %addr %port)          
        except:
            logger.info("failed to send pdu to %s %s " %addr %port)
            sock.close()
            return None
        
        sock.close()
        return ret
