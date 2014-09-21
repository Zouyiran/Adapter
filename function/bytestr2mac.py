# -*- coding:utf-8 -*-
'''
Created on 2013年11月19日

@author: Ethan
'''

def convertmac(mac, length):
    if mac[-1] == "L":
        mac = str(mac)[2:-1]
    else:
        mac = str(mac[2:])
    if len(mac) < length * 2:
        mac = "0" * (length * 2 - len(mac)) + mac
    newmac = []
    i = 0
    while i < len(mac):
        now = mac[i:i+2]
        num = int(now, 16)
        newmac.append(str(num))
        i += 2
    return ".".join(newmac)
