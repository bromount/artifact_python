#!/usr/bin/python
'''
Created on 21-Jul-2015

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

#cert.csv file should be inside the folder where you running the script

ifile  = open('/opt/cri/script/cert.csv', "rb")
reader = csv.reader(ifile)

ctfWsdl = 'https://forge.collab.net/ce-soap60/services/CollabNet?wsdl'

ctf = SOAPpy.SOAPProxy(ctfWsdl)     

login = ctf.login('username','XXXXXXXXX')
print "Logged in to Forge"

userid= ctf.getUserSessionBySoapId(login)

projects = ctf.getProjectList(login,False)

trackerWsdl = 'https://forge.collab.net/ce-soap60/services/TrackerApp?wsdl'
tracker = SOAPpy.SOAPProxy(trackerWsdl)

def timeStamp():
    #This will return the date for the HTML file for the manager's report
    timestr = time.strftime("%Y%m%d")
    return timestr

def get_association_artifact(artf_id):
    
    association_details=ctf.getAssociationList(login,artf_id)
    #print association_details
    for item in association_details:
        for value in item:
            print "Associated ID " + value['targetId']
            asso_artifact = value['targetId']
            return asso_artifact
    #print "Shadow Artifact ID " + artf_id
    #return asso_artifact
    #print team_name
    #return team_name

def send_mail(receiver_email,asso_id,username,body):
    
    subjectline = "Shadow Artifact Modification Alert"
    copied = ['karishma@collab.net']
    
    sender = "annamalai@collab.net"
        
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subjectline
    msg['From'] = sender
    msg['To'] = receiver_email
    msg['Cc'] = ",".join(copied)
    emails=receiver_email.split()+copied
    
    html =  body
    content = MIMEText(html, 'html')
        
    msg.attach(content)
    try:
        smtpObj = smtplib.SMTP('mail-qa1.sp.collab.net')
        smtpObj.sendmail(sender, emails, msg.as_string())         
        print "Successfully sent email to " + username
    except:
        print "Error: unable to send email to " + username
    
def get_user_artifact(user):
    filter = SOAPpy.Types.structType()
    filter._addItem('SoapFilter', { 'name' : 'submittedBy', 'value' : user})
    filter._addItem('SoapFilters',{'name':'status' ,'value': 'Open'})
    filter._addItem('SoapFilter1',{'name':'status' ,'value': 'In Progress'})
    filter._addItem('SoapFilters2',{'name':'status' ,'value': 'Impeded'})
    filter._addItem('SoapFilters3',{'name':'status' ,'value': 'Reopened'})
    
    #tracker222420 is the DEFECT tracker for CoreBugs
    tracker_id = "tracker22420"
    artifacts = tracker.getArtifactList2(login,tracker_id,filter)
    print artifacts
    return artifacts
    #print artifacts  
    
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
        <th> CRI - Artifact </th>
        <th> Shadow - Artifact </th>
        </tr>
        """
        table_end = """
        </table>
        <br>
        """
                
        for item in artifacts:
            for value in item:
                print value['lastModifiedDate']
                artifact_id = value['id']
                #if get_submitted_team(artifact_id)=='Support':
                get_association_artifact(artifact_id) 
                #sys.exit()
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
                
                modified_time = time.strftime("%m/%d/%y", modified_time_tuple)
                
                time_tuple = value['lastModifiedDate']
                
                dt_obj=datetime(*time_tuple[0:3])
                
                date_difference =  dt_obj.toordinal() - datetime.today().toordinal()
                print date_difference
                
                if date_difference == -1:
                    print "Your artifact Modified"
                    association=get_association_artifact(artifact_id)
                    print "Associated artifact id is : " + association
                    #print association
                    if "artf" in association:
                        print "Checking the CRI"
                        cri_detail = tracker.getArtifactData2(login,association)
                        print cri_detail
                        team_name = tracker.getArtifactData2(login,association)['flexFields']['values'][14]
                        print team_name
                        if team_name == 'Support':
                            cri_submit = tracker.getArtifactData2(login,association)['createdBy']
                            print cri_submit
                            user_email = ctf.getUserData2(login,cri_submit)['email']
                            print user_email
                            counter = counter + 1
                            table = table + "<tr><td><b><font color='black'>" + str(counter) + "</font></b></td><td><b><font color='black'><a href=https://forge.collab.net/sf/go/" + association + ">" + association +"</a></b></font> </td> <td> <b><font color='black'> <a href=https://forge.collab.net/sf/go/"  + artifact_id + ">" + artifact_id + "</a></font></b></td></tr>" + table_end
                            table = " Hi " + cri_submit +",<br> There is a modification in the below Shadow artifact for your CRI <br>" + table
                            print table
                            send_mail(user_email, artifact_id,cri_submit,table)
                            
                    else:
                        print "Your Associtation is not an artifact"

                else:
                    print "Your artifact still the same"
                
