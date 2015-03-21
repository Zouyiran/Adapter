#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import datetime
from xml.dom.minidom import parse
from config import *
from requestfunc import *

class InsertDevInsData:
    def __init__(self, datas):
        self.datas = datas
        self.url = "/api/Api/InsertDevInsData.api.php"

    def run(self):
        transactionID = uuid.uuid4()
        timeStamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S');
        #以生成接口请求xml报文的时间作为创建时间
        createtime = datetime.datetime.now()
        auth = ""
        request = render.InsertDevInsData(transactionID, timeStamp, appCode, auth, self.datas, createtime)
        auth = authenticator(timeStamp, request)
        request = render.InsertDevInsData(transactionID, timeStamp, appCode, auth, self.datas, createtime)
        response = sendRequest(str(request), BUSINESS_ADDR, BUSINESS_PORT, self.url, "POST")

        f = open(PROGRAM_ROOT + "/xmls/temp.xml", 'w')
        f.write(response)
        f.close()
        try:
            dom = parse(PROGRAM_ROOT + "/xmls/temp.xml")
            result = dom.getElementsByTagName("Result")[0].firstChild.data
            ErrorDescription = dom.getElementsByTagName("ErrorDescription")[0].firstChild.data
        except:
            msg = "业务平台返回数据无法解析"
            logger.info(msg)
            return  

        if result == "1":
            success = "向业务平台上报数据成功，事务序列号: " + str(transactionID)
            logger.info(success)
        else:
            fail = "向业务平台上报数据失败，事务序列号: " + str(transactionID) + " 失败原因: " + str(ErrorDescription)
            logger.info(fail)