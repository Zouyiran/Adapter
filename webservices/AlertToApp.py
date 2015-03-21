#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import datetime
from xml.dom.minidom import parse
from config import *
from requestfunc import *

class AlertToApp:
    def __init__(self):
        self.insid = ""
        self.workstatus = ""
        self.alertType = ""
        self.contents = ""
        self.url = "/api/Api/AlertToApp.api.php"

    def run(self):
        transactionID = uuid.uuid4()
        timeStamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S');
        createtime = datetime.datetime.now()
        auth = ""
        request = render.AlertToApp(transactionID, timeStamp, appCode, auth, self.insid, createtime, self.workstatus, self.alertType, self.contents)
        auth = authenticator(timeStamp, request)
        request = render.AlertToApp(transactionID, timeStamp, appCode, auth, self.insid, createtime, self.workstatus, self.alertType, self.contents)
        response = sendRequest(str(request), BUSINESS_ADDR, BUSINESS_PORT, self.url, "POST")