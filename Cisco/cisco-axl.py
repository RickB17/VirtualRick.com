#!/usr/bin/python
#The purpose of this script is to execute a basic query against CUCM via AXL

from suds.client import Client
from suds.sax.element import Element
import base64
import ssl

def createClient():
        cmserver = 'IP-ADDRESS'
        cmport = '8443'
        username = 'MyAXLuser'
        password = 'MyPassword'
        wsdl = 'file:///var/www/html/AXLAPI.wsdl'
        location = 'https://' + cmserver + ':' + cmport + '/axl/'

        if hasattr(ssl, '_create_unverified_context'):
                ssl._create_default_https_context = ssl._create_unverified_context
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        authenticationHeader = {
        "SOAPAction" : "ActionName",
        "Authorization" : "Basic %s" % base64string
        }

        client = Client(wsdl, location=location, username=username, password=password, headers=authenticationHeader)
        return client

def doDeviceLogout(client, phoneUUID):
        #phoneUUID in the form returned from getPhone
        FKDEVICE = client.factory.create('ns0:XFkType')
        FKDEVICE._uuid = phoneUUID
        try:
                doDeviceLogout = client.service.doDeviceLogout(FKDEVICE)
                return doDeviceLogout
        except:
                return "ERROR doDeviceLgout"
        
def getPhone(client, deviceid):
        #deviceid in the form of SEPMACADDRESS, the form returned from getUser
        eDEVICEID = Element('name').setText(deviceid)
        eRETURN = Element('returnedTags')
        try:
                getPhone = client.service.getPhone(eDEVICEID)
                return getPhone[0][0]['_uuid'][1:-1]
        except:
                return "ERROR executing getPhone"
        
def getUser(client, userName):
        userName = str(userName).lower()
        agentName = Element('userid').setText(userName)
        try:
                getUser = client.service.getUser(agentName)
                DEVICEID = getUser[0][0][11][0][0]
                return DEVICEID
        except:
                return "no device associated"
        
def listUser(client, userName):
        eSearch = Element('searchCriteria')
        eUserid = Element('userid').setText('{0}'.format(userName))
        eSearch.append(eUserid)
        eReturn = Element('returnedTags')
        elastName = Element('lastName')
        eReturn.append(elastName)
        result = client.service.listUser(eSearch, eReturn)
        return result

def getFields(client, ns):
        outputfile = open('{0}.txt'.format(ns),'w')
        OUTPUT = client.factory.create(ns)
        outputfile.write(str(OUTPUT))
        return '{0}.txt created'.format(ns)

def main(argv):
        CLIENT = createClient()
        try:
                opts, args = getopt.getopt(argv, ["gu","gp"],["getUser=","getPhone="])
        except getopt.GetoptError as err:
                print (err)
                sys.exit(2)
        for opt, arg in opts:
                if opt == '--getUser':
                        print 'expecting a user.name'
                        USERNAME = arg
                        print str(getUser(CLIENT, USERNAME))
                elif opt == '--getPhone':
                        print 'expecting a SEPMAC'
                        DEVICEID = arg
                        print str(getPhone(CLIENT,DEVICEID))


if __name__=='__main__':
        main(sys.argv[1:])
