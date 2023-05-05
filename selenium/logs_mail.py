import psycopg2
from termcolor import colored
import paramiko
import time
from paramiko import SSHClient
import csv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
import glob
from datetime import date
today = date.today()
import smtplib
global username
username = "****"
global password
password = "****"
global curry_connect
curry_connect = ''
global currynode1
global currynode2
curry_logs_node1 = []
curry_logs_node2 = []
global port
port ='****'
def connect_ssh(vm,connect):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=vm, port=port, username=username, password=password)
    curry_connect = connect  

def connect_command(node,msisdn,result,curry_logs,lista):
    global curry_result
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=node, port=port, username=username, password=password)
  
    for command in commands:
        stdin, stdout, stderr = client.exec_command(command.format(msisdn))
        time.sleep(1)
        outlines = stdout.readlines()
        result = ''.join(outlines)
        if len(result) == 0:
            lista.append('0')
         
        else:
            curry_logs = result
            lista.append(result)
        
        client.close()
     
def file_creation():
    full_logs = curry_logs_node1 + curry_logs_node2
    for text in sorted(full_logs):
        if curry_logs_node1 == '0' and curry_logs_node2 == '0':
          print("No Results for the inputed msisdn")
        else:
            f = open("full_logs.txt", 'a')
            f.write(text)
            f.close()
def logs_db(tlc,msisdn):
    print('logs_db function has starder')
    project_query = (
        """
        select * from public.hosts where project = '{}'
        """)
    project_query_insert = (
        """
        insert into public.hosts (project,curry_node1,curry_node2) VALUES ('{}','{}','{}')
        """)
    update_node1_query = (
        """
        update public.hosts    
        set curry_node1 = '{}'
        where project = '{}'
         """)
    update_node2_query = (
        """
        update public.hosts    
        set curry_node2 = '{}'
        where project = '{}'
         """)
    global commands
    commands = ['grep {} /applogs/curry/curry-standard-flows.log']
    saved_projects_list = []
    global node_1
    global node_2
    node_1 = []
    node_2 = []
    global hostname_node1
    hostname_node1 = []
    global hostname_node2
    hostname_node2 = []
    con = psycopg2.connect(database="****", user="****", password="****",host="****", port="****")

    cur = con.cursor()
    cur.execute(project_query.format(tlc))
    rows = cur.fetchall()
    results = list(rows)
    for project in results:
        saved_projects_list.append(project[0])
    while True:
        if tlc in saved_projects_list:
            query = (""" select * from public.hosts where project = '{}' """)
            cur.execute(query.format(tlc))
         
            curry_rows = cur.fetchall()
            curry_results = list(curry_rows)

            for curry_host in curry_results:
                node_1.append(curry_host[1])
                node_2.append(curry_host[2])
                hostname_node1 = node_1[0]
                hostname_node2 = node_2[0]
             
                if hostname_node1 == node_1[0]: 
                    try:
                        connect_ssh(hostname_node1,'1')
                        curry_connect = '1'
                    except:
                        curry_connect = '2' 
                    if curry_connect == '1': 
                        connect_command(hostname_node1,msisdn,'result_1','curry_logs_1',curry_logs_node1)
                      
                    elif curry_connect == '2':  
                     
                        hostname_node1 = input("Dwse node1 : ")
                        cur.execute(update_node1_query.format(hostname_node1.lower().strip(), tlc))
                        con.commit()  
                      
                        connect_command(hostname_node1, msisdn, 'result_1', 'curry_logs_1', curry_logs_node1)
                if hostname_node2 == node_2[0]: 
                    try:
                        connect_ssh(hostname_node2,'3')
                        curry_connect = '3'
                    except:
                        curry_connect = '4'  
                    if curry_connect == '3': 
                        connect_command(hostname_node2,msisdn,'result_2','curry_logs_2',curry_logs_node2)
                        break
                    elif curry_connect == '4':  
                      
                        hostname_node2 = input("Dwse node2 : ")
                        cur.execute(update_node2_query.format(hostname_node2.lower().strip(), tlc))
                        con.commit() 
                     
                     
                        connect_command(hostname_node2,msisdn,'result_2','curry_logs_2',curry_logs_node2)

            break
        else:
        
            type = input("Dwse value gia na sinexiseis : ")
            if type == '1':
                project = input("Dwse project : ")
                currynode1 = input("Dwse host gia curry node 1 : ")
                currynode2 = input("Dwse host gia curry node 2 : ")
                cur.execute(project_query_insert.format(project.upper().strip(), currynode1.strip().lower(),currynode2.strip().lower()))
                con.commit()
             
                connect_command(currynode1,msisdn,'result_1','curry_logs_1',curry_logs_node1)
                connect_command(currynode2,msisdn,'result_2','curry_logs_2',curry_logs_node2)
                break
            elif type == '2':           
                break
            else:
        
                print("Dwse dwsto value...")
                print(".......................")
    print("")
    con.close()
    file_creation()
def icarus_connect_command(host,msisdn):
    global icarus_results
    icarus_results = ''
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, port=port, username=username, password=password)
  
    for command in commands:
        stdin, stdout, stderr = client.exec_command(command.format(msisdn,full_path))
        time.sleep(1)
        outlines = stdout.readlines()
        icarus_results = ''.join(outlines)
        client.close()
      
def icarus_file_creation():
    for text in icarus_results:
        f = open('icarus_logs.txt','a')
        f.write(text)
        f.close()
def syslogs_db(account,msisdn):
    print ('syslog_db has stared')
    project_query = (
        """
        select * from public.icarus_hosts where account = '{}'
        """)
    global context
    global namespace
    global datacenter
    global mn_hostname
    global lh_hostname
    global path
    global icarus
    global commands
    global full_path
    full_path = ''
    mn_hostname = '****'
    lh_hostname = '****'
    context = []
    namespace = []
    datacenter = []
    path = '/applogs/logs/hosts/K8S/'
    icarus = 'ng-icarus'
    commands = [' grep {} {} ']
    con = psycopg2.connect(database="****", user="****", password="****",host="****", port="****")
    cur = con.cursor()
    cur.execute(project_query.format(account))
    rows = cur.fetchall()
    results = list(rows)
    for result in results:
        context.append(result[1])
        namespace.append(result[2])
        datacenter.append(result[3])
  
    full_path = path + namespace[0] + '/' + icarus + '/' + str(today) + '/' + '*.log'

    if datacenter[0] == 'MN':
        icarus_connect_command(mn_hostname, msisdn)
    elif datacenter[0] == 'LH' :
        icarus_connect_command(lh_hostname, msisdn)
    con.close()
    icarus_file_creation()
def recipient_mail(name):
    emailto = name
    emailfrom = "****"
    all_txt_files = []
    all_jpg_files = []
    
    main_dir_path = os.getcwd() 
    for file in glob.glob(main_dir_path + "\*.txt"):
        all_txt_files.append(file)
    for image in glob.glob(main_dir_path + "\*.png"):
        all_jpg_files.append(image)
    msg = MIMEMultipart()
    msg['To'] = emailto
    msg['From'] = emailfrom
    msg['Subject'] = "Logs"
    body = MIMEText("Please find attached logs")
    msg.attach(body)
    for file in all_txt_files :
        file_path = os.path.join(main_dir_path, file)
        attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition', 'attachment', filename=file)
        msg.attach(attachment)
    for image in all_jpg_files:
        file_path = os.path.join(main_dir_path, image)
        attachment.add_header('Content-Disposition', 'attachment', filename=image)
        attachment.add_header('Content-Disposition', 'attachment', filename=image)
        part = MIMEImage(open(file_path, "rb").read(), _subtype="jpg")
        msg.attach(part)
    try :
        server = smtplib.SMTP('****')
        server.set_debuglevel(0)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
        print("Successfully sent email to " + str(emailto))
    except :
        print("Error : Unable to sent email")



#def main():
    #logs_db('****'.strip().upper(), '****'.strip())
    #syslogs_db('****', '****')
    #recipient_mail('****')
#main()
