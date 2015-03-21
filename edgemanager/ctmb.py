#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct
import time

from function.crc import getCRC 
from function.bytestr2mac import convertmac
from function.store_ip import *
from configmanager.config_manager import ConfigManager
from config.config import *
from config.globals import *
from webservices.GetDevInsRangeList import *
from webservices.InsertDevInsData import *
from webservices.AlertToApp import *

class CCTMBHandler():
    def __init__(self, mbapHeader, data, ip, segIP):
        self.mbapHeader = mbapHeader
        self.data = data
        self.ip = ip
        self.segIP = segIP

    def run(self):
        cmd = self.data[9:10]
        cmd = struct.unpack("!B", cmd)[0]

        if cmd == 0x04:
            #定时上报
            logger.info("数据包为：CTMB协议定时上报数据")
            self.regularReport(self.mbapHeader, self.data)

    def regularReport(self, mbapHeader, data):
        gathertime = datetime.datetime.now()
        dataInfoList = []
        forcrc = data[:-3]
        forcrc = forcrc[1:]
        format = "!" + "B" * len(forcrc)
        calculate_crc = getCRC(list(struct.unpack(format, forcrc)))
        recv_crc = struct.unpack("!H", data[-3:-1])[0]
        if calculate_crc == recv_crc:
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
            datalength = data[12:14] #N * 4
            datalength = struct.unpack("<H", datalength)[0]
            datalength = datalength / 4 # N
            
            #每个数据值以及其所包含的信息
            for n in range(0, datalength):
                reg = reg + n * 4
                getConfigInfo = ConfigManager(XMLFILEPATH)
                try:
                    eachDataInfoDict, configFile = getConfigInfo.get(segmac,scmac,reg)
                except:
                    continue
                value = data[(14 + n * 4) : (18 + n * 4)]
                value = struct.unpack("<I", value)[0]
                TH = float((value >> 16) >> 8)
                TL = float((value >> 16) & 0x00FF)
                try:
                    realvalue = eval(eachDataInfoDict['Rule']) #算映射值  
                    del eachDataInfoDict['Rule'] 
                except Exception, e:
                    #如果原始数据转换规则出错则默认原始数据为0
                    realvalue = 0
                    logger.info("未找到原始数据转换规则或者规则错误，原因%s" % str(e))

                try:
                    SValue = self.getSValue(realvalue, eachDataInfoDict['SRule'])
                    del eachDataInfoDict['SRule']
                except Exception, e:
                    #如果查询显示转换规则出错则默认显示数据与原始数据一致
                    SValue = realvalue
                    logger.info("未找到显示转换规则或者规则错误，原因%s" % str(e))

                eachDataInfoDict['Value'] = realvalue
                eachDataInfoDict['SValue'] = SValue
                #以收到上报数据的时间作为采集时间
                eachDataInfoDict['GatherTime'] = gathertime
                #处理是否告警
                rangeRequester = GetDevInsRangeList(eachDataInfoDict['InsID'])
                high, low = rangeRequester.run()
                entityName = eachDataInfoDict['MonitorName'].encode("UTF-8")
                deviceName = eachDataInfoDict['Name'].encode("UTF-8")
                
                insid = eachDataInfoDict["InsID"]
                #本地内存中没有该设备的记录，则新建一个，默认告警状态为正常
                if insid not in globals.deviceMap.keys():
                    eachDataInfoDict['AlertType'] = 0
                    eachDataInfoDict['AlertDesc'] = "正常"
                    globals.deviceMap[insid] = eachDataInfoDict
                #有记录则当前应沿用之前的告警状态
                else:
                    eachDataInfoDict['AlertType'] = globals.deviceMap[insid]['AlertType']
                    eachDataInfoDict['AlertDesc'] = globals.deviceMap[insid]['AlertDesc']

                if high != -1 and float(SValue) > float(high):  
                    #若已经处于告警状态，不再重复告警
                    if globals.deviceMap[insid]['AlertType'] != 2:               
                        msg = "%s%s(%s)在%s超过阈值(%d,%d)" % (entityName, deviceName, SValue, datetime.datetime.now(), low, high)
                        eachDataInfoDict['AlertType'] = 2
                        eachDataInfoDict['AlertDesc'] = msg
                        alertRequester = AlertToApp()
                        alertRequester.insid = eachDataInfoDict['InsID']
                        alertRequester.workstatus = eachDataInfoDict['WorkStatus']
                        alertRequester.alertType = 1
                        alertRequester.contents = msg
                        alertRequester.run()

                elif low != -1 and float(SValue) < float(low):
                    #若已经处于告警状态，不再重复告警
                    if globals.deviceMap[insid]['AlertType'] != 1:               
                        msg = "%s%s(%s)在%s超过阈值(%d,%d)" % (entityName, deviceName, SValue, datetime.datetime.now(), low, high)
                        eachDataInfoDict['AlertType'] = 1
                        eachDataInfoDict['AlertDesc'] = msg
                        alertRequester = AlertToApp()
                        alertRequester.insid = eachDataInfoDict['InsID']
                        alertRequester.workstatus = eachDataInfoDict['WorkStatus']
                        alertRequester.alertType = 1
                        alertRequester.contents = msg
                        alertRequester.run()
                else:
                    #若处于告警状态，发出恢复正常告警指令，若已为正常状态，不再发出告警
                    eachDataInfoDict['AlertType'] = 0
                    eachDataInfoDict['AlertDesc'] = "正常"
                    if globals.deviceMap[insid]['AlertType'] != 0:  
                        msg = "%s%s(%s)在%s恢复正常(%d,%d)" % (entityName, deviceName, SValue, datetime.datetime.now(), low, high)
                        alertRequester = AlertToApp()
                        alertRequester.insid = eachDataInfoDict['InsID']
                        alertRequester.workstatus = eachDataInfoDict['WorkStatus']
                        alertRequester.alertType = 0
                        alertRequester.contents = msg
                        alertRequester.run()

                #更新内存中设备状态表信息
                globals.deviceMap[eachDataInfoDict["InsID"]] = eachDataInfoDict
                dataInfoList.append(eachDataInfoDict)
                
                storeip(self.ip, segmac, configFile, self.segIP)    

            requester = InsertDevInsData(dataInfoList)
            requester.run()

        else:
            logger.info("数据CRC校验不通过，上报数据CRC校验和为%s，正确应为%s" % (recv_crc, calculate_crc))

    def getSValue(self, value, rule):
        if rule[:3] == "S:1":
            format = rule[4:]
            format = "%" + format
            svalue = format % value
            return svalue
        
        elif rule[:3] == "S:0":
            rule = rule[5:-1]
            rule = rule.split("@")
            rulemap = {}
            for index in range(0, len(rule), 2):
                rulemap[int(rule[index])] = rule[index + 1]

            return rulemap[int(value)]