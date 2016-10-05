#!/usr/bin/python
#The purpose of this script is to execute a basic querey against CUCM via AXL

from suds.client import Client
from suds.sax.element import Element
import base64
import ssl

if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

cmserver = 'IP-ADDRESS'
cmport = '8443'
wsdl = 'file:///var/www/html/AXLAPI.wsdl'
location = 'https://' + cmserver + ':' + cmport + '/axl/'
username = 'MyAXLUser'
password = 'MyPassword'

def getUser(userName):
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        authenticationHeader = {
        "SOAPAction" : "ActionName",
        "Authorization" : "Basic %s" % base64string
        }
        client = Client(wsdl, location=location, username=username, password=password, headers=authenticationHeader)
        userName = str(userName)[:-1].lower()
        agentName = Element('userid').setText(userName)
        try:
                getUser = client.service.getUser(agentName)
                DEVICEID = getUser[0][0][11][0][0]
                return DEVICEID
        except:
                return "no device associated"

print getUser('Rick.Breidenstein')
