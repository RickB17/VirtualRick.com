#!/usr/bin/python
#The purpose of this script is to execute a basic query against CUCM via AXL

from suds.client import Client
from suds.sax.element import Element
from xml.etree import ElementTree
import sys, getopt, re, requests
import base64
import ssl
import logging
import getpass
import requests

logging.basicConfig(filename='logfile.txt', level=logging.INFO)

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

def emGetSEP(userName):
        cucm_server = "YOURSERVERIP"
        emuser = "UserWithExtensionMobilityProxyAutenticationRole"
        appEmProxyUser = "may be the same as above"
        appPw = "your super secret and strong password"
        uri = 'http://{0}:8080/emservice/EMServiceServlet'.format(cucm_server)
        logging.info(uri)
        headers = {"Content-Type":"application/x-www-form-urlencoded"}
        parameters = "<query><appInfo><appID>{0}</appID><appCertificate>{1}</appCertificate></appInfo><userDevicesQuery><userID>{2}</userID></userDevicesQuery></query>".format(appEmProxyUser, appPw, userName)
        r = requests.post(uri, data={"xml": parameters}, headers=headers)
        logging.info(r.content)
        tree = ElementTree.fromstring(r.content)
        SEP = ElementTree.tostring(tree[0][0][0])[12:-14]
        return SEP
        
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
        try:
                opts, args = getopt.getopt(argv, ["gu","gp","ddl","emSEP"],["getUser=","getPhone=","doDeviceLogout=", "emGetSEP="])
        except getopt.GetoptError as err:
                print (err)
                sys.exit(2)
        for opt, arg in opts:
                print arg
                if opt == '--getUser':
                        print 'expecting a user.name'
                        USERNAME = arg
                        CLIENT = createClient()
                        print str(getUser(CLIENT, USERNAME))
                elif opt == '--getPhone':
                        print 'expecting a SEPMAC'
                        CLIENT = createClient()
                        DEVICEID = arg
                        print str(getPhone(CLIENT,DEVICEID))
                elif opt == '--doDeviceLogout':
                        print 'expecting a fkdevice uuid'
                        CLIENT = createClient()
                        UUID = arg
                        print str(doDeviceLogout(CLIENT,UUID))
                elif opt == '--emGetSEP':
                        print 'expecting user.name'
                        USERNAME = arg
                        print str(emGetSEP(USERNAME))

if __name__=='__main__':
        main(sys.argv[1:])
