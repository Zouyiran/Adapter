# -*- coding: utf-8 -*- 
'''
Created on 2013年11月5日

@author: Zouyiran
'''

import re
import string
from configmanager.read_segxml import *
from config.config import *


class ConfigManager(object):
    def __init__(self, xml):
        self.xml = xml

    def get(self, segmac, scmac, reg):  # 得到该设备的所需信息
        configFile_all = readSegXml(self.xml)

        flag = segmac in configFile_all.keys()
        if flag:
            configFile_seg = configFile_all[segmac]

            flag = scmac in configFile_seg.keys()
            if flag:
                configFile_sc = configFile_seg[scmac]
                count = 0
                for eachDev in configFile_sc.keys():
                    if reg == string.atoi(eachDev, 16):
                        everyDataInfo = {}
                        everyDataInfo['InsID'] = configFile_sc[eachDev]['InsID']  #找设备编号

                        everyDataInfo['DeviceType'] = configFile_sc[eachDev]['DevTypeID']  #找设备型号
                        everyDataInfo['MonitorName'] = configFile_sc[eachDev]['MonitorName']  #找设备场所名
                        everyDataInfo['Name'] = configFile_sc[eachDev]['Name']  #找设备名

                        if configFile_sc[eachDev]['MonitorCode'] != None:
                            everyDataInfo['EntityID'] = configFile_sc[eachDev]['MonitorCode']  #找场所ID
                            #everyDataInfo['MonitorName'] = configFile_sc[eachDev]['MonitorName']#找场所ID

                        everyDataInfo['WorkStatus'] = configFile_sc[eachDev]['WorkStatus']  #找采集数据时的工作模式

                        rule = configFile_sc[eachDev]['Rules'].values()
                        for eachRule in rule:
                            # 含有TH及TL的为原始数据转换规则
                            searchRule = re.search('TH', eachRule) or re.search('TL', eachRule)
                            if searchRule is not None:
                                everyDataInfo['Rule'] = eachRule  #找到映射规则
                                #{'EntityID': '6879921629', 'DeviceType': '3043', 'Rule': '(TH+TL/100-4)/16*100', 'InsID': '4974093649', 'WorkStatus': '1'}                                   
                            else:
                                pass
                            # 含有S:的为显示转换规则
                            SRule = re.search('S:', eachRule)
                            if SRule is not None:
                                everyDataInfo['SRule'] = eachRule  #找到映射规则
                                #{'EntityID': '6879921629', 'DeviceType': '3043', 'Rule': '(TH+TL/100-4)/16*100', 'InsID': '4974093649', 'WorkStatus': '1'}                                   
                            else:
                                pass
                        return everyDataInfo, configFile_all
                    else:
                        count += 1
                if count == len(configFile_sc):
                    logger.info("设备描述文件中无此设备%s" % str(reg))
            else:
                logger.info("设备描述文件中无此采控器%s" % str(scmac))
        else:
            logger.info("设备描述文件中无此边缘网关%s" % str(segmac))     