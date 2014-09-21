# -*- coding: utf-8 -*-
'''
Created on 2013年11月13日

@author: Echo
'''


# -*- coding: utf-8 -*-
import os
import web
from server_functions import *

temPath = os.path.abspath(os.getcwd())+"/webservices/templates"
render = web.template.render(temPath, cache = False)

urls = (
    '/(.*)', 'xmlServer'   #这里可以根据请求的url的不同将请求定位到下面不同的类里处理，就可实现多个接口
)

app = web.application(urls, globals())

class xmlServer:
    #先假设是通过GET方法进行请求，如果他们用的是POST修改就可以了
    def POST(self, method):
        method = web.input().method  #获取url中的method参数
        if method == "PostInsControlMsgByInsID":
            print method
            return self.PostInsControlMsgByInsID()

    def PostInsControlMsgByInsID(self):
        request = web.data() #这里读取请求中的xml数据
        print request          
        
        transactionID, timeStamp, itemRequestLists = handlePICMBIRequest(request) 
        devList = getDevinsList(itemRequestLists)

        web.header('Content-Type', 'text/xml: chartset=\"UTF-8\"') 
        reponseData = self.handlePICMBIResponse(transactionID, timeStamp, devList) #调用函数处理发来的xml请求，生成返回的xml回应
        #response_data = "Well done!"
        return reponseData #发送出去

    
    def handlePICMBIResponse(self, transactionID, timeStamp, devList):
        #这里应对收到的xml请求进行处理，返回xml数据，我这里没有处理，直接使用了一个没有任何参数的模板返回
        return render.response(transactionID, timeStamp, devList)
        
web.webapi.internalerror = web.debugerror
if __name__ == '__main__': 
    app.run()
