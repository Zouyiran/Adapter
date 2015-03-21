# -*- coding: utf-8 -*-
'''
Created on 2013年11月13日

@author: CH
'''
import os
import time
import struct
import socket
import xml
from xml.dom.minidom import parse

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from edgemanager.csender import CSender    

#====================================================================================================
""" the following funtions are used by PostInsControlMsgByInsID"""
def handlePICMBIRequest(request):
    """处理接收到的服务请求，从中解析出需要的参数TransactionID, TimeStamp, ItemRequest列表，并返回这些参数"""
    f=open("tepXml.xml", 'w')
    f.write(request)
    f.close()
    
    dom = parse("tepXml.xml")#载入xml文件 
            
    transactionID = dom.getElementsByTagName("TransactionID")[0].firstChild.data
    timestamp = dom.getElementsByTagName("TimeStamp")[0].firstChild.data
    itemrequestlists = dom.getElementsByTagName("ItemRequest")
    print ".........."
    print transactionID,timestamp,itemrequestlists
    return transactionID,timestamp,itemrequestlists
        
def getDevinsList(itemRequestLists):
    devLists = []
    for itemRequest in itemRequestLists:
        print "itemRequests"
        dev = {}
        insID = itemRequest.getElementsByTagName("InsID")[0].firstChild.data
        controlMsg = itemRequest.getElementsByTagName("ControlMsg")[0].firstChild.data
        controlBrief = itemRequest.getElementsByTagName("ControlBrief")[0].firstChild.data

        print insID,controlMsg,controlBrief
            
        deviceInfo = findDeviceInfo(insID)
#            device_info=["","","0x00",""]
        segmac = deviceInfo[0]
        scmac = deviceInfo[1]
        register = int(deviceInfo[2], 16)
        status = deviceInfo[3]
            
        dev["InsID"] = insID
        dev["Status"] = status
        dev["Desc"] = ""
        dev["CurTime"] = time.strftime("%Y%m%d%H%m%S")
            
        devLists.append(dev)
            
        if controlMsg=="C":
            print "Cmsg---C,send control Msg"
            sender = CSender(segmac, scmac, register, int(controlBrief, 16))
            sender.run()
            #sendControlMsg(segmac, scmac, register, int(controlBrief, 16))#由CSender完成
        elif controlMsg=="H":
            pass
        else:
            pass 
    return devLists       
#     @soap(String, _return=Array(String))
def findDeviceInfo(insID):
    """根据设备ID，在本地缓存的的配置文件中查找请求的设备地址,包括:所在边缘网关地址segmac,
    所属控器地址scmac,及寄存器地址register,工作状态workstatus,并将结果生成字符列表返回 """
        
    print "find dev info"
    results = []
    segXml = ET.parse("D:\\Java\\workspace\\Ptest\\adapter\\configmanager\\SEG.xml")#载入xml文件 
    servResponseRoot = segXml.getroot()#获取根节点 'ServiceResponse' 

    flag = 0
    for eachMargin in servResponseRoot[6]:
        if not flag:
            if eachMargin.find('Mac') != None:
                segMac = eachMargin.find('Mac').text
                for eachSc in eachMargin.findall('SC'):
                    if eachSc.find('Mac') != None:
                        scMac = eachSc.find('Mac').text
                        for eachDevice in eachSc.findall('Device'):
                            if eachDevice.find('Address') != None and eachDevice.find('InsID').text == insID:
                                flag = 1
                                deviceAddr = eachDevice.find('Address').text #获得设备寄存器地址
                                deviceStatus = eachDevice.find('WorkStatus').text
                                break
                            else:
                                continue
    if flag == 1:
        results.append(segMac)
        results.append(scMac)
        results.append(deviceAddr)
        results.append(deviceStatus)#注意将设备地址转换成整型返回
    else:
        results = ["0.0.0.0","0.0.0.0.0.0.0.0","0x00",""]
    print results
    return results
#====================================================================================================
#=======================================由CSender完成=================================================            
#     @soap(String, String, Integer, Integer)
def sendControlMsg(segmac, scmac, register, data):
    """将设备信息和控制数据一起传给边缘网关的内部的控制数据接收服务器端口"""
    print "sending control Msg"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    client.connect(("127.0.0.1", 2222))
    client.send(makeCMSGpdu(segmac, scmac, register, data))
    #client.send("hello")
    client.close()
    print "over to send control Msg"
    
#     @soap(String, String, Integer, Integer, _return=String)
def makeCMSGpdu(segmac, scmac, register, data):
    segmac=struct.pack("!I",convertMac(segmac))
    scmac=struct.pack("!Q",convertMac(scmac))
    register=struct.pack("<H",register)
    cdata=struct.pack("<H",data)
        
    pdu = segmac+scmac+register+cdata
    print "making pdu successfully"
    return pdu
    
def convertMac(mac):
    #"""将ip地址转换成整数"""
    mac = mac.split(".")
    bytestr = ""
    for byte in mac:
        byte = int(byte)
        byte = "%02x" % byte
        bytestr += byte

    bytestr = "0x" + bytestr
    return int(bytestr, 16)
#=======================================由CSender完成================================================= 
#====================================================================================================