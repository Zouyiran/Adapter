# -*- coding:utf-8 -*-

from pymongo import MongoClient
from pymongo.errors import *
import pymongo, datetime, config, random
from config.config import logger

global logger

'''
Created on 2013年10月12日

@author: Echo
'''
"""设配网关中数据库操作接口，可向数据库中写入或者读取数据"""
#  DEV_KEY = {1:"InsID", 2:"DeviceType", 3:"GatherTime", 4:"CreateTime", 5: "Value", 6:"SValue",7:"EntityTD", 8:"WorkStatus", 9:"AlertType",9: "AlertDesc"}
#  CON_KEY = ["InsID", "ControlMsg", "ControlBrief", "ControlType", "RuleID", "TransactionID"]
#  ALERT_KEY = ["InsID", "AlertType", "WorkStatus", "Contents"]
COLLECTIONS_NAME = ["BLog","CallBAPILog","DeviceInsAlert","DeviceInsHty","DeviceInsStatus","DevInsControl",
                   "OperateLog","StatisticsDay","StatisticsHour","StatisticsMinute","StatisticsMonth"]#数据库中集合名称

class DataManager():
    def __init__(self, username, password, dbname, host = "localhost" , port = 27017):
        try:
            self.connection = MongoClient(host, port)#与MongoDB服务建立连接
            self.user = username #数据库用户名及密码，用于认证
            self.userpwd = password
            self.db = self.connection[dbname]#要操作的数据库
#             self.collection = self.db[colname]#数据库下面的集合
        except TypeError:
            print "连接失败 %s: %s ，端口号应为整数 " %(host, port)
            exit(0)
        except ConnectionFailure:
            print "连接 失败 %s: %s " %(host, port)
            exit(0)                          
         
        try:
            self.db.authenticate(self.user, self.userpwd)
        except:
            print "访问数据库失败，用户名或者密码错误"
            exit(0)
         
    def __setCollection(self, collection):
        self.collection = self.db[collection]  
        
    def __writeData(self, data):
        #"私有方法，向数据库的集合中插入文档"
        if data:
            if self.collection.find({"InsID" : data["InsID"]}).count() == 0:                
                self.collection.insert(data)
                print "成功写入数据: " +",".join(["%s: %s" %(k, v) for k, v in data.items()])
            else:
                self.collection.update({"InsID" : data["InsID"]}, data)
                print "成功更新数据"
        else:
            print "写入的数据类型需为字典且不能为空" 
    
    def __calSValue(self, value):
        return str(value).format() 
            
    def __del__(self):
        #"close the connection in the end"
        try:
            self.db.logout()         
            self.connection.close()
            logger.info("Disconnection to the database")
        except:
            pass       
        
    def getData(self, collection, query = {}):
        #"get data from collection in database"
        self.__setCollection(collection)
        if type(query) is not dict:
            print "查询条件需为字典类型"
        else:
            return self.collection.find(query).sort("InsID", pymongo.ASCENDING)
            
    def removeData(self, query = {}):
        if self.getData(query):
            self.collection.remove(query)
            print "成功删除数据"  
    
    def writeCallBAPLogData(self, data):
        self.__setCollection(COLLECTIONS_NAME[1])
        lData = {}
        lData["TransactionID"] = data["TransactionID"]
        lData["CallID"] = int(data["CallID"])
        lData["CallAPI"] = data["CallAPI"]
        lData["CallDataTime"] = datetime.datetime.now()
        lData["CallVar"] = data["CallVar"]
        lData["FeedBackStatus"] = data["FeedBackStatus"]
        lData["ErrorDescription"] = data["ErrorDescription"]
        
        self.__writeData(lData) 
                
    def writeAlertData(self, data):#设备报警信息
        self.__setCollection(COLLECTIONS_NAME[2])
        alertData = {}
        alertData["InsID"] = int(data["InsID"])
        alertData["AlertType"] = int(data["AlertType"])
        alertData["CreateTime"] = datetime.datetime.now()
        alertData["WorkStatus"] = int(data["WorkStatus"])
        alertData["Contents"] = data["Contents"]
                
        self.__writeData(alertData)
    
    def writeDevHtyData(self, data): #设备历史状态信息
        self.__setCollection(COLLECTIONS_NAME[3])
        devData = {}
        devData["InsID"] = int(data["InsID"])
        devData["DeviceType"] = int(data["DeviceType"])
        devData["GatherTime"] = datetime.datetime.strptime(data["GatherTime"], "%Y-%m-%d-%H-%M-%S")
        devData["CreateTime"] = datetime.datetime.now()
        devData["Value"] = data["Value"]
        devData["SValue"] = self.__calSValue(data["Value"])
        devData["EntityID"] = int(data["EntityID"])
        devData["WorkStatus"] = int(data["WorkStatus"])
#         devData["AlertType"] = int(data["AlertType"])        
#         devData["AlertDesc"] =  data[" AlertDesc"]
              
        self.__writeData(devData)
    
     
    def writeDevStatusData(self, data): #设备状态表
        self.__setCollection(COLLECTIONS_NAME[4])
        devData = {}
        devData["InsID"] = int(data["InsID"])
        devData["DeviceType"] = int(data["DeviceType"])
        devData["GatherTime"] = datetime.datetime.strptime(data["GatherTime"], "%Y-%m-%d-%H-%M-%S")
        devData["CreateTime"] = datetime.datetime.now()
        devData["Value"] = data["Value"]
        devData["SValue"] = self.__calSValue(data["Value"])
        devData["EntityID"] = int(data["EntityID"])
        devData["WorkStatus"] = int(data["WorkStatus"])
#         devData["AlertType"] = int(data["AlertType"])        
#         devData["AlertDesc"] =  data[" AlertDesc"]
              
        self.__writeData(devData)
        
    def writeControlData(self, data):#设备控制信息
        self.__setCollection(COLLECTIONS_NAME[5])
        conData = {}
        conData["InsID"] = int(data["InsID"])
        conData["ControlMsg"] = data["ControlMsg"]
        conData["CreateTime"] = datetime.datetime.now()
        conData["ControlBrief"] = data["ControlBrief"]
        conData["ControlType"] = int(data["ControlType"])
        conData["RuleID"] = int(data["RuleID"])
        conData["TransactionID"] = int(data["TransactionID"])        
        
        self.__writeData(conData)
        
    def writeOpLogData(self, data):#设备操作日志
        self.__setCollection(COLLECTIONS_NAME[6])
        data = {}
#         data["App"] = App
#         data["Act"] = Act
#         data["OperateTime"] = datetime.datetime.now()
#         data["OperNo"] = int(OperNo)
#         data["UserTime"] = UserName
#         data["ImplementCallResult"] = int(ICallResult)        
        
        self.__writeData(data)
        
    
            
#     def writeDeviceData(self, InsID, DeviceType, GatherTime, Value, SValue,EntityTD, WorkStatus, AlertType, AlertDesc): 
#         data = {}
#         data["InsID"] = int(InsID)
#         data["DeviceType"] = int(DeviceType)
#         data["GatherTime"] = datetime.datetime.strptime(GatherTime, "%Y-%m-%d-%H")
#         data["CreateTime"] = datetime.datetime.now()
#         data["SValue"] = SValue
#         data["EntityTD"] = int(EntityTD)
#         data["WorkStatus"] = int(WorkStatus)
#         data["AlertType"] = int(AlertType)        
#         data[" AlertDesc"] =  AlertDesc
#               
#         self.__writeData(data)
#         
#     def writeControlData(self, InsID, ControlMsg, ControlBrief, ControlType, RuleID, TransactionID):
#         data = {}
#         data["InsID"] = int(InsID)
#         data["ControlMsg"] = ControlMsg
#         data["CreateTime"] = datetime.datetime.now()
#         data["ControlBrief"] = ControlBrief
#         data["ControlType"] = int(ControlType)
#         data["RuleID"] = int(RuleID)
#         data["TransactionID"] = int(TransactionID)        
#         
#         self.__writeData(data)
#         
#     def writeOpLogData(self, App, Act, OperNo, OperateTime, UserName, ICallResult):
#         data = {}
#         data["App"] = App
#         data["Act"] = Act
#         data["OperateTime"] = datetime.datetime.now()
#         data["OperNo"] = int(OperNo)
#         data["UserTime"] = UserName
#         data["ImplementCallResult"] = int(ICallResult)        
#         
#         self.__writeData(data)
#         
#     def writeAlertData(self, InsID, AlertType, WorkStatus, Contents):
#         data = {}
#         data["InsID"] = int(InsID)
#         data["AlertType"] = int(AlertType)
#         data["CreateTime"] = datetime.datetime.now()
#         data["WorkStatus"] = int(WorkStatus)
#         data["Contents"] = Contents
#                 
#         self.__writeData(data)
#     
#     def writeCallBAPLogData(self, TranctionID, CallID, CallAPI, CallVar, FBackStatus, ErrorDsc):
#         data = {}
#         data["TransactionID"] = TranctionID
#         data["CallID"] = int(CallID)
#         data["CallAPI"] = CallAPI
#         data["CallDataTime"] = datetime.datetime.now()
#         data["CallVar"] = CallVar
#         data["FeedBackStatus"] = FBackStatus
#         data["ErrorDescription"] = ErrorDsc
#         
#         self.__writeData(data)
        
    
#     def writeSDayData(self, InsID, EntityID, MinValue, AvgValue, MaxValue):
#         sday_data = {}
        
        
if __name__ == "__main__":
    dm = DataManager(config.DATABASE_USER, config.DATABASE_PASSWORD, config.DATABASE_NAME)
#     for i in range(1000):
#         dm.writeData({config.KEY1: i, config.KEY2: random.randint(1,35)})
#     if dm.getData():
#         for item in dm.getData(): 
#             print item
#         print "record(s): %d **************************************" %dm.getData().count()
#     query = {config.KEY2: 21}
#     var = dm.getData(query)
#     if var:
#         for item in var: 
#             print item,item[config.KEY1],type(item)
#         print "find %d record(s)" %var.count()
#         print "var type:",type(var)
#     
#     dm.removeData(query)
#     dm.setCollection("test")

#     dm.setCollection("DeviceInsAlert")
#     data1 = AlertData(0, 0, 1, " important ").dev_data
#     data2 = AlertData(1, 0, 1, " urge ").dev_data 
#     
#     alertData = [2, 0, 1, """well"""] 
#     
#     data3 = DataPacker(config.ALERTKEY, alertData).packer()
#     dm.writeData(data1)
#     dm.writeData(data2)
#     dm.writeData(data3)
    dataSet = dm.getData()
    for e in dataSet:
        print e
    

    
        

        
