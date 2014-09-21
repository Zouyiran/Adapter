# -*- coding: utf-8 -*- 
'''
Created on 2013年11月5日

@author: Ethan
'''

#import struct
import re
import string
from read_segxml import *

class ConfigManager(object):
    def __init__(self,xml):
        self.xml = xml
        
    def get(self,segmac,scmac,reg):#得到该设备的所需信息
        configFile_all = readSegXml(self.xml)
        
        flag = segmac in configFile_all.keys()#str#
        if flag:
            configFile_seg = configFile_all[segmac]
            
            flag = scmac in configFile_seg.keys()#str#
            if flag:
                configFile_sc = configFile_seg[scmac]
                count = 0
                for eachDev in configFile_sc.keys():
                    if reg == string.atoi(eachDev,16):#int#
                        everyDataInfo = {}#为这个设备建立信息字典
                            
                        everyDataInfo['InsID'] = configFile_sc[eachDev]['InsID']#找设备编号
                            
                        everyDataInfo['DeviceType'] = configFile_sc[eachDev]['DevTypeID']#找设备型号
                            
                        if configFile_sc[eachDev]['MonitorCode'] != None:
                            everyDataInfo['EntityID'] = configFile_sc[eachDev]['MonitorCode']#找场所ID
                                
                        everyDataInfo['WorkStatus'] = configFile_sc[eachDev]['WorkStatus']#找采集数据时的工作模式
                                            
                        rule = configFile_sc[eachDev]['Rules'].values()                 
                        for eachRule in rule:
                            searchRule = re.search('TH',eachRule) or re.search('TL',eachRule)
                            if searchRule is not None:                                 
                                everyDataInfo['Rule'] = eachRule#找到映射规则 
                                #{'EntityID': '6879921629', 'DeviceType': '3043', 'Rule': '(TH+TL/100-4)/16*100', 'InsID': '4974093649', 'WorkStatus': '1'}                                   
                            else:
                                pass         
                    else:
                        count += 1
                if count == len(configFile_sc):
                    print 'can not find reg(',reg,')in configure file!'            
            else:
                print 'can not find scmac(',scmac,')in configure file!'              
        else:
            print 'can not find segmac(',segmac,')in configure file!' 

        #print "dataInfo: ",everyDataInfo
        return everyDataInfo,configFile_all 