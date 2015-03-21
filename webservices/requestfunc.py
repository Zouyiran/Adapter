#!/usr/bin/env python
# -*- coding: utf-8 -*-

import md5
import httplib
from config.config import *

appCode = "GASE"
appKey = "111111"
gaCode = "GASE"

def authenticator(timestamp, xml):
    key = md5.new(appKey).hexdigest()
    result = key + "$" + appCode + "$" + timestamp + "$" + str(xml)
    result = md5.new(result).hexdigest()
    return result

def sendRequest(msg, host, port, url, method):
    headers = {
        'Host': str(host) + ":" + str(port),
        'Content-Length': "%d" % len(msg),
        'User-Agent': "CTMB Adapter Gateway",
        'Content-type': 'text/xml'
    }
    httpClient = httplib.HTTPConnection(host, port)
    httpClient.request(method, url, msg, headers)
    response = httpClient.getresponse()

    data = response.read()  

    return data