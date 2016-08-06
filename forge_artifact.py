'''
Created on 07-Sep-2015

@author: bromount
'''
#!/usr/bin/python

import SOAPpy
import sys


ctfWsdl = 'https://forge.collab.net/ce-soap60/services/CollabNet?wsdl'

ctf = SOAPpy.SOAPProxy(ctfWsdl)     

login = ctf.login('username','password@@')
print "Logged in to Forge"

userid= ctf.getUserSessionBySoapId(login)

projects = ctf.getProjectList(login,False)

trackerWsdl = 'https://forge.collab.net/ce-soap60/services/TrackerApp?wsdl'
tracker = SOAPpy.SOAPProxy(trackerWsdl)

tracker_id = "tracker22558"

artifacts = tracker.getArtifactList2(login,tracker_id)

print artifacts

artf_title = "Testing"

artf_desc = " Desc Testing"

artf_group = "None"

artf_category = ""

artf_status = ""

artf_customer = ""

artf_priority = ""





create_artifact = tracker.createArtifact3(login,tracker_id,'Test_title','Test_desc','','None','Open','','2 - High', , ,0, , ,'','')

print "artifact created"
