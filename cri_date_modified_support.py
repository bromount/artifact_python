'''
Created on Jun 21, 2015

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

ifile  = open('/opt/cri/script/team.csv', "rb")
reader = csv.reader(ifile)

'''ifile1  = open('team.csv', "rb")
reader1 = csv.reader(ifile)'''

ctfWsdl = 'https://forge.collab.net/ce-soap60/services/CollabNet?wsdl'

ctf = SOAPpy.SOAPProxy(ctfWsdl)     

login = ctf.login('supportl2','C0llab1234$')
print "Logged in to Forge"

userid= ctf.getUserSessionBySoapId(login)

projects = ctf.getProjectList(login,False)

trackerWsdl = 'https://forge.collab.net/ce-soap60/services/TrackerApp?wsdl'
tracker = SOAPpy.SOAPProxy(trackerWsdl)

data =     []

#this function will return the current date

def timeStamp():
    timestr = time.strftime("%Y%m%d")
    #print timestr
    return timestr

#this function will send mail to individual in team.csv

def sendmail_individual(table,total_artifacts,receiver_email,username):
    subjectline = username + ", you have " +  str(total_artifacts) + "  issue(s) in CRI Tracker"
                
    table =  "<h2>" + subjectline + "</h2>" + table
              
    copied = ['annamalai@collab.net']
    
    sender = "annamalai@collab.net"
        
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subjectline
    msg['From'] = sender
    msg['To'] = receiver_email
    msg['Cc'] = ",".join(copied)
    emails=receiver_email.split()+copied
    html = table
        
    content = MIMEText(html, 'html')
        
    msg.attach(content)
    try:
        smtpObj = smtplib.SMTP('mail-qa1.sp.collab.net')
        if total_artifacts > 0:
            smtpObj.sendmail(sender, emails, msg.as_string())         
            print "Successfully sent email to " + username
    except:
        print "Error: unable to send email to " + username
        
#This function will send mail to the managers

def sendmail_managers():
    sleep(5)
    with open("/opt/cri/html/"+timeStamp()+"_cri_details_support.html","r") as file_open:
        lines=file_open.read()
        print lines

    subjectline = "CRI Tracker Report - Support"
    receiever = ['support-managers@collab.net']
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
    filter._addItem('SoapFilter', { 'name' : 'assignedTo', 'value' : user})
    filter._addItem('SoapFilters',{'name':'status' ,'value': 'Open'})
    filter._addItem('SoapFilter1',{'name':'status' ,'value': 'In Progress'})
    filter._addItem('SoapFilters2',{'name':'status' ,'value': 'Re-opened'})
    filter._addItem('SoapFilters4',{'name':'status' ,'value': 'Fixed - Verify & Close'})
            
    #proj1362 is the customer issues project
    #tracker2160 is the CRI tracker
    tracker_id = "tracker2160" 
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
        <th> Last Modified </th>
        </tr>
        """
        table_end = """
        </table>
        <br>
        """
        
        for item in artifacts:
            for value in item:
                print value['lastModifiedDate']
                #print type(item)
                #counter = counter + 1
                modified_time_list = list(value['lastModifiedDate'])
                modified_time_list=map(int, modified_time_list)
                print modified_time_list
                modified_time_list.append(0)
                modified_time_list.append(0)    
                modified_time_list.append(0)
                modified_time_tuple=tuple(modified_time_list)
                print modified_time_tuple
                #modified_time_tuple=map(int, modified_time_tuple)
                
                modified_time = time.strftime("%m/%d/%y ", modified_time_tuple)
                
                #To find the different between two dates
                time_tuple = value['lastModifiedDate']
                dt_obj=datetime(*time_tuple[0:3])
                
                date_difference =  dt_obj.toordinal() - datetime.today().toordinal()
                
                if date_difference >= -3:
                    pass
                    #table = table + "<tr><td><b><font color='black'>" + str(counter) + "</font></b></td><td><b><font color='red'><a href=https://forge.collab.net/sf/go/" + value['id'] + ">" + value['id'] +"</a></b></font> </td> <td> <b><font color='black'> " + value['title'].encode("utf-8") + "</font></b></td><td> <b><font color='black'>" + modified_time + "</font></b></td></tr>"
                else:
                    counter=counter+1
                    table = table + "<tr><td><b><font color='black'>" + str(counter) + "</font></b></td><td><b><font color='black'><a href=https://forge.collab.net/sf/go/" + value['id'] + ">" + value['id'] +"</a></b></font> </td> <td> <b><font color='black'> " + value['title'].encode("utf-8") + "</font></b></td><td> <b><font color='black'>"  + modified_time + "</font></b></td></tr>"

        #table = table + "</table> <br> Note: Artifacts which is not updated more than 'three' days will be in <font color='red'><b>RED</b></font>."
        print table
        sendmail_individual(table, counter,email,username)      
                
        #print data
        if counter > 0:
            html_file=open('/opt/cri/html/'+timeStamp()+'_cri_details_support.html','a')
            print >>html_file, username, table, table_end
            html_file.close()            
        print "..."
        

sendmail_managers()
        


        


    
