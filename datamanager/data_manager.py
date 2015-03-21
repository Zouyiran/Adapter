# -*- coding:utf-8 -*-

from pymongo import MongoClient
from pymongo.errors import *
import pymongo, datetime, config, random
from config.config import *

global logger

'''
Created on 2013年10月12日

@author: Echo
'''

class DataManager():
    def __init__(self, host = DATABASE_ADDR, port = DATABASE_PORT, dbname = DATABASE_NAME, username = DATABASE_USER, password = DATABASE_PASSWORD):
        try:
            self.connection = MongoClient(host, port)#与MongoDB服务建立连接
            self.user = username #数据库用户名及密码，用于认证
            self.userpwd = password
            self.db = self.connection[dbname]#要操作的数据库

        except Exception, e:
            logger.info("MongoDB连接失败, 错误原因%s" % str(e))

        if username != "" and password != "" :
            try:
                self.db.authenticate(self.user, self.userpwd)
            except:
                logger.info("MongoDB认证失败, 错误原因%s" % str(e))
          
    def __insert(self, data):
        #"私有方法，向数据库的集合中插入数据"
        if data:   
            try:         
                self.collection.insert(data)
                logger.info("成功写入数据: " +",".join(["%s: %s" %(k, v) for k, v in data.items()]))
            except Exception, e:
                logger.error("数据插入失败，错误原因%s", str(e))
            

    def __update(self, data):
        #"私有方法，向数据库的集合中更新数据"
        if data:
            if self.collection.find({"InsID" : data["InsID"]}).count() == 0:  
                try:              
                    self.collection.insert(data)
                    logger.info("成功更新数据: " +",".join(["%s: %s" %(k, v) for k, v in data.items()]))
                except Exception, e:
                    logger.error("数据更新失败，错误原因%s", str(e))
            else:
                try:     
                    self.collection.update({"InsID" : data["InsID"]}, data)
                    logger.info("成功更新数据: " +",".join(["%s: %s" %(k, v) for k, v in data.items()]))
                except Exception, e:
                    logger.error("数据更新失败，错误原因%s", str(e))
        
    def getData(self, collection, query = {}):
        #"get data from collection in database"
        self.collection = self.db[collection]  
        if type(query) is not dict:
            print "查询条件需为字典类型"
        else:
            return self.collection.find(query).sort("InsID", pymongo.ASCENDING)
            
    def removeData(self, query = {}):
        if self.getData(query):
            self.collection.remove(query)
            print "成功删除数据"  
    
    def writeDevHtyData(self, data): #设备历史状态信息
        self.collection = self.db["DeviceInsHty"]
        devData = {}
        devData["InsID"] = int(data["InsID"])
        devData["DeviceType"] = int(data["DeviceType"])
        devData["GatherTime"] = datetime.datetime.strptime(data["GatherTime"], "%Y-%m-%d-%H-%M-%S")
        devData["CreateTime"] = datetime.datetime.now()
        devData["Value"] = data["Value"]
        devData["SValue"] = data["SValue"]
        devData["EntityID"] = int(data["EntityID"])
        devData["WorkStatus"] = int(data["WorkStatus"])

        devData["AlertType"] = data["AlertType"]
        devData["AlertDesc"] = data["AlertDesc"]
              
        self.__insert(devData)

        self.db.logout()         
        self.connection.close()
    
     
    def writeDevStatusData(self, data): #设备状态表
        self.collection = self.db["DeviceInsStatus"]
        devData = {}
        devData["InsID"] = int(data["InsID"])
        devData["DeviceType"] = int(data["DeviceType"])
        devData["GatherTime"] = datetime.datetime.strptime(data["GatherTime"], "%Y-%m-%d-%H-%M-%S")
        devData["CreateTime"] = datetime.datetime.now()
        devData["Value"] = data["Value"]
        devData["SValue"] = data["SValue"]
        devData["EntityID"] = int(data["EntityID"])
        devData["WorkStatus"] = int(data["WorkStatus"])
              
        devData["AlertType"] = data["AlertType"]
        devData["AlertDesc"] = data["AlertDesc"]
        
        self.__update(devData)

        self.db.logout()         
        self.connection.close()