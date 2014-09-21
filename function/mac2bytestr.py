# -*- coding:utf-8 -*-
'''
Created on 2013年11月19日

@author: Ethan
'''
def convertmac(mac):
    """将ip地址转换成整数"""
    mac = mac.split(".")
    bytestr = ""
    for byte in mac:
        byte = int(byte)
        byte = "%02x" % byte
        bytestr += byte

    bytestr = "0x" + bytestr
    return int(bytestr, 16)