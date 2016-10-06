#!/usr/bin/python
#The purpose of this script is to execute a basic query against CUCM via AXL

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
        userName = str(userName).lower()
        agentName = Element('userid').setText(userName)
        try:
                getUser = client.service.getUser(agentName)
                DEVICEID = getUser[0][0][11][0][0]
                return DEVICEID
        except:
                return "no device associated"
        
def listUser(userName):
        eSearch = Element('searchCriteria')
        eUserid = Element('userid').setText('{0}'.format(userName))
        eSearch.append(eUserid)
        eReturn = Element('returnedTags')
        elastName = Element('lastName')
        eReturn.append(elastName)
        client = Client(wsdl, location=location, username=username, password=password, headers=authenticationHeader)
        result = client.service.listUser(eSearch,eReturn)
        return result

def getFields(ns):
        #outputs the item to a text file so you can easily see what fields are available
        client = Client(wsdl, location=location, username=username, password=password, headers=authenticationHeader)
        outputfile = open('{0}.txt'.format(ns),'w')
        OUTPUT = client.factory.create(ns)
        outputfile.write(str(OUTPUT))
        return '{0}.txt created'.format(ns)

print getUser('Rick.Breidenstein')
