'''
Created on 04-Jan-2016

@author: bromount
'''

import sys
import re
import string
import SOAPpy
import smtplib
import time
import datetime
from datetime import date
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
from operator import itemgetter
from docutils.nodes import line
from time import sleep

'''ifile  = open('/opt/cri/script/team.csv', "rb")
reader = csv.reader(ifile)'''

'''ifile1  = open('team.csv', "rb")
reader1 = csv.reader(ifile)'''

ctfWsdl = 'https://forge.collab.net/ce-soap60/services/CollabNet?wsdl'

ctf = SOAPpy.SOAPProxy(ctfWsdl)     

login = ctf.login('annamalai','Openthis22!@')
print "Logged in to Forge"

userid= ctf.getUserSessionBySoapId(login)

projects = ctf.getProjectList(login,False)

trackerWsdl = 'https://forge.collab.net/ce-soap60/services/TrackerApp?wsdl'
tracker = SOAPpy.SOAPProxy(trackerWsdl)

def get_field_values(tracker_id):

    f_values=tracker.getFields(login,tracker_id)
    print f_values

trk_id='tracker2160'

get_field_values(trk_id)