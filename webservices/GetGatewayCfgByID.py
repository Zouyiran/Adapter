#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import datetime

from config import *
from requestfunc import *

class GetGatewayCfgByID:
    def __init__(self, mid = "", endDate = ""):
        self.mid = mid
        self.endDate = endDate 
        self.url = "/efarm2/services/efarmService?method=GetGatewayCfgByID"

    def run(self):
        transactionID = uuid.uuid4()
        timeStamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S');
        auth = ""
        request = render.GetGatewayCfgByID(transactionID, timeStamp, gaCode, appCode, self.mid, self.endDate, auth)
        auth = authenticator(timeStamp, request)
        request = render.GetGatewayCfgByID(transactionID, timeStamp, gaCode, appCode, self.mid, self.endDate, auth)
        response = sendRequest(str(request), MANAGE_ADDR, MANAGE_PORT, self.url, "POST")
        xml = open(PROGRAM_ROOT + "/xmls" +  os.sep + "SEG.xml", "w")
        xml.write(response)
        xml.close()