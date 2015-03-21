# -*- coding: utf-8 -*-
'''
Created on 2013年10月23日

@author: Zouyiran
'''

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def readSegXml(xml):
    allEdges = {}
    segXml = ET.parse(xml)  # 载入xml文件
    servResponseRoot = segXml.getroot()  # 获取根节点 'ServiceResponse'

    for eachMargin in servResponseRoot[6]:
        if eachMargin.find('Mac') != None:
            eachMarginMac = eachMargin.find('Mac').text
            allEdges[eachMarginMac] = {}
            for eachport in eachMargin.findall('Port'):
                if eachport.text != '0':
                    allEdges[eachMarginMac + '_port'] = eachport.text

        for eachSc in eachMargin.findall('SC'):  # .iter
            if eachSc.find('Mac') != None:
                eachScMac = eachSc.find('Mac').text
                allEdges[eachMarginMac][eachScMac] = {}
            for eachDevice in eachSc.findall('Device'):
                if eachDevice.find('Address') != None:
                    eachDeviceAddr = eachDevice.find('Address').text
                    allEdges[eachMarginMac][eachScMac][eachDeviceAddr] = {}
                for eachDevAttrib in list(eachDevice):
                    if eachDevAttrib.tag == 'InsID':
                        allEdges[eachMarginMac][eachScMac][eachDeviceAddr]['InsID'] = eachDevAttrib.text
                    elif eachDevAttrib.tag == 'WorkStatus':
                        allEdges[eachMarginMac][eachScMac][eachDeviceAddr]['WorkStatus'] = eachDevAttrib.text
                        #elif eachDevAttrib.tag == 'Address':#
                        #allEdges[eachMarginMac][eachScMac][eachDeviceAddr]['Address'] = eachDevAttrib.text
                    elif eachDevAttrib.tag == 'DevTypeID':
                        allEdges[eachMarginMac][eachScMac][eachDeviceAddr]['DevTypeID'] = eachDevAttrib.text
                    elif eachDevAttrib.tag == 'MonitorCode':
                        if eachDevAttrib.text != None:
                            allEdges[eachMarginMac][eachScMac][eachDeviceAddr]['MonitorCode'] = eachDevAttrib.text
                    elif eachDevAttrib.tag == 'MonitorName':
                        if eachDevAttrib.text != None:
                            allEdges[eachMarginMac][eachScMac][eachDeviceAddr]['MonitorName'] = eachDevAttrib.text
                    elif eachDevAttrib.tag == 'Name':
                        if eachDevAttrib.text != None:
                            allEdges[eachMarginMac][eachScMac][eachDeviceAddr]['Name'] = eachDevAttrib.text
                    elif eachDevAttrib.tag == 'Rules':
                        allEdges[eachMarginMac][eachScMac][eachDeviceAddr]['Rules'] = {}
                        for eachDevRule in eachDevAttrib.findall('Rule'):
                            eachDevRuleID = eachDevRule.attrib['ID']
                            allEdges[eachMarginMac][eachScMac][eachDeviceAddr]['Rules'][
                                eachDevRuleID] = eachDevRule.text
    return allEdges


# if __name__ == "__main__":
#     ret = readSegXml('..' + os.sep + 'xmls' + os.sep + 'SEG.xml')
#     print
#     ret
