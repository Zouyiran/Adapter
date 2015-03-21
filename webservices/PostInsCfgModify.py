#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
from xml.dom.minidom import parse
from config import *
from GetGatewayCfgByID import *

class Handler:
    def __init__(self, data):
        self.data = data

    def handle(self):
        f = open(PROGRAM_ROOT + "/xmls/temp.xml", 'w')
        f.write(self.data)
        f.close()
        try:
            dom = parse(PROGRAM_ROOT + "/xmls/temp.xml")
            cfgID = dom.getElementsByTagName("CfgID")[0].firstChild.data
            updateTime = dom.getElementsByTagName("UpdateTime")[0].firstChild.data
            mid = dom.getElementsByTagName("Mid")[0].firstChild.data
            type = dom.getElementsByTagName("Type")[0].firstChild.data
        except:
            msg = "管理平台返回数据无法解析"
            logger.info(msg)
            return

        web.header('Content-Type', 'text/xml') 

        requester = GetGatewayCfgByID(mid)
        requester.run()
        return render.PostInsCfgModify(1, "")