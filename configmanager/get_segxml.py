# -*- coding: utf-8 -*-
'''
Created on 2013年11月11日

@author: Echo
'''
import urllib2 
import sys, httplib 
import time

def callGetGatewayCfgByIDService(transactionID, gacode, appcode, auth): 
    msgModel = '''\
　　<?xml version=”1.0” encoding=”utf-8” ?>
　　<ServiceRequest>
　　<TransactionID>%s</TransactionID>
　　<TimeStamp>%s</TimeStamp>
　　<GACode>%s</GACode>
　　<AppCode>%s</AppCode>
　　<Authenticator>%s</Authenticator>
  </ServiceRequest>
    '''
    timestamp = time.strftime("%Y%m%d%H%m%S")
    message = msgModel %(transactionID,timestamp, gacode, appcode, auth) 
    
    webservice = httplib.HTTPConnection("219.141.189.154:8087") 
    webservice.putrequest("POST", "/efarm2/services/efarmService?method=GetGatewayCfgByID") 
    webservice.putheader("Host", "219.141.189.154:8087") 
    webservice.putheader("User-Agent", "Python") 
    webservice.putheader("Content-type", "text/xml") 
    webservice.putheader("Content-length", "%d" % len(message)) 
    webservice.endheaders() 
    webservice.send(message) 
    # get the response 
    res = webservice.getresponse()
     
    status = res.status
    reason = res.reason
    data = res.read() 
        
#     print status, reason, data   
     
    buildCfgFile(data)
    
    webservice.close()
    
def buildCfgFile(xmlstr):
    f = open("cfg.xml", 'w')
    f.write(xmlstr)
    f.close()

if __name__ == "__main__":
    callGetGatewayCfgByIDService("0987654321","9128321","pm","SADKFL12WDSSADFS121")

