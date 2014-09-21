# -*- coding:utf-8 -*-
'''
Created on 2013年11月18日

@author: Ethan
'''

import struct
import time

from function.crc import getCRC 
from function.bytestr2mac import convertmac
from function.store_ip import storeip
from configmanager.config_manager import ConfigManager
from config.config import *
from datamanager.data_manager import DataManager

global logger

class CPacketHandler(object):
    def __init__(self,packet,ip,segIP):
        self.packet = packet
        self.ip = ip
        self.segIP = segIP
         
    def run(self):
        dataInfoList = []      
        mbapHeader = self.packet[0:10]
        data = self.packet[10:]
        ctmbID = mbapHeader[2:4]
        ctmbID = struct.unpack("!H", ctmbID)[0]
        if ctmbID == 0x00:
            print 'data reported by edge use <CTMB>'
            cmd = data[9:10]
            cmd = struct.unpack("!B", cmd)[0]
            
            #定时上报
            if cmd == 0x04:
                logger.info("From %s, received regular report data" %self.ip)
                forcrc = data[:-3]
                forcrc = forcrc[1:]
                format = "!" + "B" * len(forcrc)
                calculate_crc = getCRC(list(struct.unpack(format, forcrc)))
                recv_crc = struct.unpack("!H", data[-3:-1])[0]
                if calculate_crc == recv_crc:
                    print 'crc checking passed!'
                
                    #边缘网关标识符Mac
                    segmac = mbapHeader[6:10]
                    segmac = struct.unpack("!I", segmac)[0]
                    segmac = convertmac(hex(segmac), 4)
                               
                    #采控器地址 Mac   
                    scmac = data[1:9]
                    scmac = struct.unpack("!Q", scmac)[0]
                    scmac = convertmac(hex(scmac), 8)
                      
                    #起始寄存器地址Address
                    reg = data[10:12]
                    reg = struct.unpack("<H", reg)[0]
                    
                    #数据长度
                    datalength = data[12:14]#N*4
                    datalength = struct.unpack("<H", datalength)[0]
                    datalength = datalength / 4 #N
                    
                    #每个数据值以及其所包含的信息
                    for n in range(0,datalength):
                        reg = reg + n*4
                        getConfigInfo = ConfigManager(XMLFILEPATH)
                        eachDataInfoDict,configFile = getConfigInfo.get(segmac,scmac,reg)
                        
                        value = data[(14+n*4):(18+n*4)]
                        value = struct.unpack("<I", value)[0]
                        TH = float((value >> 16) >> 8)
                        TL = float((value >> 16) & 0x00FF)
                        realvalue = eval(eachDataInfoDict['Rule'])#算映射值           
                        del eachDataInfoDict['Rule']
                        eachDataInfoDict['Value'] = realvalue
                        eachDataInfoDict['GatherTime'] = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
                        
                        dataInfoList.append(eachDataInfoDict)
                        
                        try:
                            dm = DataManager(DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
                            logger.info("User %s connected to database" %DATABASE_USER)
                            dm.writeDevHtyData(eachDataInfoDict)
                            logger.info("User %s write data to database successfully" %DATABASE_USER)
                        except Exception:
                            logger.info("User %s failed to write data to database" %DATABASE_USER)
                                              
                    storeip(self.ip,segmac,configFile,self.segIP)                       
                else:
                    print 'crc checking error!'
                    
                              
            #历史数据上报    
            elif cmd == 0x64:
                logger.info("From %s, received historical reporting data"%self.ip)
                forcrc = data[:-3]
                forcrc = forcrc[1:]
                format = "!" + "B" * len(forcrc)
                calculate_crc = getCRC(list(struct.unpack(format, forcrc)))
                recv_crc = struct.unpack("!H", data[-3:-1])
                if calculate_crc == recv_crc[0]:
                    print 'crc checking passed!'
                    
                    #边缘网关标识符
                    segmac = mbapHeader[0:4]
                    segmac = struct.unpack("!I", segmac)[0]
                    segmac = convertmac(hex(segmac), 4)                  
                    
                    #采控器地址
                    scmac = data[1:9]
                    scmac = struct.unpack("!Q", scmac)[0]
                    scmac = convertmac(hex(scmac), 8)
                    
                    #起始寄存器地址
                    reg = data[10:12]
                    reg = struct.unpack("<H", reg)[0]
                    
                    #数据长度
                    datalength = data[12:14]# N*4
                    datalength = struct.unpack("!H", datalength)[0]
                    datalength = datalength / 4 #N
                    
                    #数据采集时间    
                    timestamp = data[12:16]
                    timestamp = struct.unpack("<I", timestamp)[0]
                    timestamp = time.gmtime(timestamp)
                    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", timestamp)                  
                    
                    for n in range(0,datalength):
                        reg = reg + n*4
                        getConfigInfo = ConfigManager(XMLFILEPATH)
                        eachDataInfoDict,configFile = getConfigInfo.get(segmac,scmac,reg)
                        
                        value = data[(14+n*4):(18+n*4)]
                        value = struct.unpack("<I", value)[0]
                        TH = float((value >> 16) >> 8)
                        TL = float((value >> 16) & 0x00FF)
                        realvalue = eval(eachDataInfoDict['Rule'])#算映射值           
                        del eachDataInfoDict['Rule']
                        eachDataInfoDict['Value'] = realvalue
                        eachDataInfoDict['GatherTime'] = timestamp
                        
                        dataInfoList.append(eachDataInfoDict)
                        
                    storeip(self.ip,segmac,configFile,self.segIP)                       
                else:
                    print 'crc checking wrong!'                  
            else:
                pass
        else:
            logger.info("From %s, received data is not CTMB and ignored"%self.ip)
            print 'not CTMB!'
            
        print "infoList: ",dataInfoList       
        #return dataInfoList
 

    
