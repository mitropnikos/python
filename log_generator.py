#!/usr/bin/env python

from pyhive import hive
import csv
from datetime import datetime, timedelta, date
import uuid
import random
from itertools import izip_longest as zip_longest
import os
import glob
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

"""
    A script that takes as input the user username, a csv file with msisdns from the user, logs to HDFS and executes a query
    and creates system logs ( Request - Response ) and sylogs (validation). 

    The results (users.csv, hdfs_results.csv and logs.csv) are senting via email to the respective username's input

    Tested with Python 2.7.14

"""


#####################    OTP REQUEST ##########################################################################
aa = 'INFO'
ab = 'add.generate.pin.ng.outbound.GENERATE_PIN'
ac = 'ddresses=**************&threadPoolSize=10'
ad = '---> REQ: ADD GENERATE PIN REQUEST TO ***'
ae = 'MSISDN='
af = 'SHORT_CODE=*****'
ag = 'PIN='
ah = 'TEXT='
#################################################################################################################

#####################    OTP RESPONSE     #######################################################################
ba = '<--- RES: ADD GENERATE PIN REQUEST FROM ****'
bb = 'SMPP_COMMAND_STATUS_HEX=0x00000000'
bc = 'SMPP_COMMAND_STATUS_ERROR_CODE=ESME_ROK'
bd = 'SMPP_COMMAND_STATUS_DESCRIPTION=No Error'
be = 'SMPP_SENT_MESSAGE_COUNT='
#################################################################################################################

#################### SYSLOG VALIDATION ####################################
ca = '[http-nio-8080-exec-2] INFO  c.u.s.s.w.v1.NotificationController - Received external event notification: ExternalEventNotification('
event_id = 'eventId='
cb = 'uid='
cc = 'uidType=MSISDN'
cd = 'campaign=WEB, requestHeaders=null, userAgent=null, device=null, browser=null, os=null, ip=null, trafficSource=null, publisher=null, subPublisher=null, wifiFlow=false, additionalData=null, sessionId=null, category=OTP, subCategory=Input, location=OTP, text='
ce = 'channel=null)'
event_type = 'eventType='
result = 'result='
service = 'service='
##########################################################################


query =( '''
.....
''')


request = []
response = []
syslogs_b = []
today = date.today()
msisdn = []
contentprovider = []
sent_service = []

n = 3 # seconds. OTP RESPONSE TIMESTAMP SHOULD BE 3 SECONDS + FROM OTP REQUEST'S TIMESTAMP


def msisdn_serviceprovider():
    with open('hdfs_results.csv') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                msisdn.append(row[1])
                contentprovider.append(row[11])
                sent_service.append(row[2])



ldap = str(raw_input("Please provide your username : ")).strip()
ldap2 = str(raw_input("Please confirm your username : ")).strip()

while ldap2 != ldap:
    ldap = str(raw_input("Your credentials do not match. Please provide your username again : ")).strip()
    ldap2 = str(raw_input("Please confirm your username : ")).strip()


msisdn_file = raw_input("Name your msisdn file : ").strip()
msisdn_file_2 = raw_input("Enter the name of the file again  : ").strip()


while msisdn_file != msisdn_file_2 :
    msisdn_file = raw_input("The file names does not match. \nPlease provide again the msisdn file name : ").strip()
    msisdn_file_2 = raw_input("Please confirm file's name  : ").strip()


file = open(msisdn_file, "r")
csv_reader = csv.reader(file)

lists_from_csv = []

for row in csv_reader:
    if len(row) > 0:
        lists_from_csv.append(row)


format_strings = ','.join(['%s'] * len(lists_from_csv))


con = hive.Connection(host='********', port='10200', auth='LDAP',username='*******', password='********')
print ("Connected To HDFS \n")
print ("Query is running. This might take a while.... \n")
cursor = con.cursor()
cursor.execute(query % format_strings, tuple(lists_from_csv))
results = cursor.fetchall()
with open('hdfs_results.csv', 'w') as file:
                writer = csv.DictWriter(file, fieldnames = ["date","uid","service","eventType","result","text","date","eventType","result","service","text","serviceprovider"])
                writer.writeheader()
                writer = csv.writer(file, delimiter=",")
                writer.writerows(results)


if con :
        con.close()
print("Operation To HDFS Finished\n")



print("========== PROCCESSING OTP REQUEST ===========\n")

with open('hdfs_results.csv') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            ag2 = row[5][16:20]
            otp_request = row[0] + ' | ' + aa + ' | ' + ab + ' | ' + ac + ' || ' + ad + ' | ' + ae + row[1] + ' | ' + af + ' | ' + ag + ag2 + ' | ' + ah + row[5]
            line_count += 1
            print(otp_request)
            request.append(otp_request)

print("\n======= PROCCESSING  OTP RESPONSE ============\n")

with open('hdfs_results.csv') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            retry_count = random.randint(1, 3)
            ag2 = row[5][16:20]
            initial_date = row[0].split("T")
            hh_mm_ss = initial_date[1]
            time_str = hh_mm_ss
            date_format_str = '%H:%M:%S'
            given_time = datetime.strptime(time_str, date_format_str)
            final_time = given_time + timedelta(seconds=n)
            otp_response_time = str(initial_date[0]) + 'T' + str(final_time)[-8:]
            otp_response = otp_response_time + ' | ' + aa + ' | ' + ab + ' | ' + ac + ' || ' + ba + ' | ' + ae + row[1] + ' | ' + bb + ' | ' + bc + ' | ' + \
                           bd + ' | ' + be + str(retry_count) + ' | ' + af + ' | ' + ag + ag2 + ' | ' + ah + row[5]
            line_count += 1
            print(otp_response)
            response.append(otp_response)


print("\n======= PROCCESSING SYSLOGS VALIDATION =======\n")

with open('hdfs_results.csv') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        random_id = uuid.uuid4()
        if csvreader.line_num == 1:
            continue

        elif row[7] in (None, ""):
            row[7] = 'null'
            syslogs_b.append(row[7])

        else:

            syslogs = row[6] + ' ' + ca + event_id + str(random_id) + ', ' + cb + row[1] + ', ' + ' ' + cc + ', ' + event_type + row[7] + ', ' + result + row[8] + ', ' \
                    + service + row[2] + ', ' + cd + row[10] + ', ' + ce
            print(syslogs)
            syslogs_b.append(syslogs)

msisdn_serviceprovider()
print("\n")

d = [request,response,syslogs_b,msisdn,contentprovider,sent_service]
export_data = zip_longest(*d, fillvalue='')

with open(str(today) + '_' + 'ADD_logs.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(("request", "response", "validation", "msisdn", "contentprovider", "service"))
    writer.writerows(export_data)


os.chdir("/home/support/ADD")
all_csv_files = []

for file in glob.glob("*.csv"):
    all_csv_files.append(file)


emailfrom = "*******"
emailto = [ldap+"@upstreamsystems.com"]

msg = MIMEMultipart()
body_part = MIMEText('Please find attached System logs', 'plain')
msg["From"] = emailfrom
msg["To"] = ",".join(emailto)
msg["Subject"] = "ADD Logs"
msg.attach(body_part)

with open(str(today) + '_' + 'ADD_logs.csv', 'rb') as file:
    msg.attach(MIMEApplication(file.read(), Name=str(today) + '_' + 'ADD_logs.csv'))


try :
    server = smtplib.SMTP('********')
    server.set_debuglevel(0)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()
    print("Successfully sent email to " + str(ldap))
except :
    print("Error : Unable to sent email")



for file in all_csv_files:
    if file.endswith('.csv'):
        os.remove(file)
