#!/usr/bin/python
'''
Created on 08-Jul-2015

@author: aarunachalam
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
import shutil


ifile  = open('/opt/cri/script/team.csv', "rb")
reader = csv.reader(ifile)

ifile1  = open('/opt/cri/script/team.csv', "rb")
reader1 = csv.reader(ifile)

ctfWsdl = 'https://forge.collab.net/ce-soap60/services/CollabNet?wsdl'

ctf = SOAPpy.SOAPProxy(ctfWsdl)     

login = ctf.login('supportl2','C0llab1234$')
print "Logged in to Forge"

userid= ctf.getUserSessionBySoapId(login)

projects = ctf.getProjectList(login,False)

trackerWsdl = 'https://forge.collab.net/ce-soap60/services/TrackerApp?wsdl'
tracker = SOAPpy.SOAPProxy(trackerWsdl)

data =     []

def timeStamp():
    timestr = time.strftime("%Y%m%d")
    #print timestr
    return timestr
      
#This function will send mail to the managers

def sendmail_managers():
    sleep(5)
    with open("/opt/cri/html/"+timeStamp()+"_crus_report.html","r") as file_open:
        lines=file_open.read()
        print lines

    subjectline = "CRUS Tracker Report"
    receiever = ['support-managers@collab.net','anandm@collab.net']
    sender = "annamalai@collab.net"
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subjectline
    msg['From'] = sender
    msg['To'] = ", ".join(receiever)
    html = lines
    content = MIMEText(html, 'html')
    msg.attach(content)
    try:
        smtpObj = smtplib.SMTP('mail-qa1.sp.collab.net')
        smtpObj.sendmail(sender,receiever,msg.as_string())
        print "Email sent successfully to Managers"
    except:
        print "Error in sending mail to Managers"
        
def get_user_artifact(user):
    trackerWsdl = 'https://forge.collab.net/ce-soap60/services/TrackerApp?wsdl'
    tracker = SOAPpy.SOAPProxy(trackerWsdl)
    filter = SOAPpy.Types.structType()
    filter._addItem('SoapFilter', { 'name' : 'submittedBy', 'value' : user})
    filter._addItem('SoapFilters',{'name':'status' ,'value': 'Open'})
    filter._addItem('SoapFilters1',{'name': 'assignedTo','value': 'anandm'})
    filter._addItem('SoapFilters2',{'name': 'assignedTo','value': 'srose'})
    filter._addItem('SoapFilters3',{'name': 'assignedTo','value': 'prodmgmt'})
      
    #tracker2175 is the CRUS tracker
    tracker_id = "tracker2175" 
    artifacts = tracker.getArtifactList2(login,tracker_id,filter)
    print artifacts
    return artifacts

for row in reader:
    if row[0]:
        username = row[0]
        email = row[1]
        artifacts=get_user_artifact(username)
        counter = 0
            
        table = """
        <table border="1">
        <tr>
        <th>S.No </th>
        <th> Artifact </th>
        <th> Title </th>
        <th> Submitted Time</th>
        </tr>
        """
        table_end = """
        </table>
        <br>
        """
        for item in artifacts:
            for value in item:
                print value['submittedDate']
                submitted_time_list = list(value['submittedDate'])
                submitted_time_list=map(int, submitted_time_list)
                print submitted_time_list
                submitted_time_list.append(0)
                submitted_time_list.append(0)
                submitted_time_list.append(0)
                submitted_time_tuple=tuple(submitted_time_list)
                print submitted_time_tuple
                submitted_time = time.strftime("%Y/%m/%d ", submitted_time_tuple)
                print submitted_time
                #Target Date as of July 10th 2015
                target_date = (2015,7,10,0,0,0.0)
                target_date_list = list(target_date)
                print target_date_list
                target_date_list = map(int,target_date_list)
                print target_date_list
                target_date_list.append(0)
                target_date_list.append(0)
                target_date_list.append(0)
                target_date_tuple=tuple(target_date_list)
                print target_date_tuple
                target_date = time.strftime("%Y/%m/%d ", target_date_tuple)
                print target_date
                if submitted_time<target_date:
                    print "target date greater"
                else:
                    print "submitted time greater"
                    planning_folder = value['planningFolderId']
                    print planning_folder
                    if str(value['planningFolderId'])=='None':
                        print "checked the condition" 
                        time_tuple = value['submittedDate']
                        print time_tuple
                
                        dt_obj=datetime(*time_tuple[0:3])
                        print dt_obj
                
                        date_difference =  dt_obj.toordinal() - datetime.today().toordinal()
                
                        print date_difference
                                      
                        if date_difference <= -6:
                            counter=counter+1
                            table = table + "<tr><td><b><font color='black'>" + str(counter) + "</font></b></td><td><b><font color='black'><a href=https://forge.collab.net/sf/go/" + value['id'] + ">" + value['id'] +"</a></b></font> </td> <td> <b><font color='black'> " + value['title'].encode("utf-8") + "</font></b></td><td> <b><font color='black'>"  + submitted_time + "</font></b></td></tr>"
                        #print table
        #table = table + "</table> <br> Note: Artifacts which is not updated more than 'three' days will be in <font color='red'><b>RED</b></font>."
        print table
              
        if counter > 0:
            html_file=open('/opt/cri/html/'+timeStamp()+'_crus_report.html','a')    
            print >>html_file, username,table, table_end
            html_file.close()
        print "..."
        
        

sendmail_managers()
