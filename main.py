# -*- coding:utf-8 -*-
'''
# Created on 2013年10月17日
# 
# @author: Echo
# '''

from edgemanager.edge_manager import *
from webservices.gateway_services import * 

def main():
    edgemanager=EdgeManager(502)
    edgemanager.run()
    app.run()
    
    
#     try:
#         from wsgiref.simple_server import make_server
#         soap_application = soaplib.core.Application([PostInsControlMsgByInsIDService], 'tns')
#         wsgi_application = wsgi.Application(soap_application)
#         server = make_server('localhost', 7789, wsgi_application)
#         server.serve_forever()
#     except ImportError:
#         print "Error: example server code requires Python >= 2.5"
        
if __name__ == "__main__":
    main()
