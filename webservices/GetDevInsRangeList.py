#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import datetime
from xml.dom.minidom import parse
from config import *
from requestfunc import *

class GetDevInsRangeList:
    def __init__(self, insid):
        self.insid = insid
        self.url = "/api/Api/GetDevInsRangeList.api.php"

    def run(self):
        transactionID = uuid.uuid4()
        timeStamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S');
        auth = ""
        request = render.GetDevInsRangeList(transactionID, timeStamp, appCode, auth, self.insid)
        auth = authenticator(timeStamp, request)
        request = render.GetDevInsRangeList(transactionID, timeStamp, appCode, auth, self.insid)   
        response = sendRequest(str(request), BUSINESS_ADDR, BUSINESS_PORT, self.url, "POST")

        f = open(PROGRAM_ROOT + "/xmls/temp.xml", 'w')
        f.write(response)
        f.close()
        high = -1
        low = -1
        try:
            dom = parse(PROGRAM_ROOT + "/xmls/temp.xml")
            high = int(dom.getElementsByTagName("HighValue")[0].firstChild.data)
            low = int(dom.getElementsByTagName("LowValue")[0].firstChild.data)
            return high, low
        except:
            msg = "业务平台返回阈值无法解析"
            logger.info(msg)
            return high, low