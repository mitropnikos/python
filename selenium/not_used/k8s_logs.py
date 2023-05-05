import psycopg2
from termcolor import colored
import paramiko
import time
from paramiko import SSHClient
from datetime import date
today = date.today()
import csv


"""
    A script that that takes as input the desired Account, connects to **** schema (for testing reasons) and is searching the context
     the namespace and the datacenter 
    for the respective iccarus account. Onward it connects to **** or to **** 
    depending on Account's Datacenter and creates a txt file with msisdn logs ( only for "today" ).
    To extract the relevant icarus information icarus-projects repo has been downloaded from git with the following commands.

    path='/****'
    echo "account,context,namespace,datacenter"; for file in $(ls $path | grep -v secrets); do grep -E 'Account|SYSID|Project|ProjectIndex|DataCenter' 
    $path/"$file" | cut -d ':' -f2 | xargs | awk '{print $1",""k8s-plus-"tolower($5)","tolower($1)"-icarus-"tolower($2)$4","$5  }' ;done
    The results of the above command have been inserted to public.icarus_hosts 
    Tested with  Python 3.8.10

"""

def connect_command(host,msisdn):
    global icarus_results
    icarus_results = ''

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, port=port, username=username, password=password)
    print('Connected to' +  str(host))

    for command in commands:
        stdin, stdout, stderr = client.exec_command(command.format(msisdn,full_path))
        time.sleep(1)
        outlines = stdout.readlines()
        icarus_results = ''.join(outlines)
        print(icarus_results)

        client.close()
        print('Connection to' +  str(host) +  'has been closed')


def file_creation(msisdn):
   if icarus_results == '':
    for text in icarus_results:
        f = open('icarus_logs.txt','a')
        f.write(str(text))
        f.close()
    print('no results for the user ' + str(msisdn) )    

def syslogs_db(account,msisdn):

    project_query = (
        """
        select * from public.icarus_hosts where account = '{}'
        """)

    global context
    global namespace
    global datacenter
    global mn_hostname
    global lh_hostname
    global username
    global password
    global port
    global path
    global icarus
    global commands
    global full_path
    full_path = ''
    port = '22'
    username = "****"
    password = "****"
    mn_hostname = '****'
    lh_hostname = '****'
    context = []
    namespace = []
    datacenter = []
    path = '/applogs/logs/hosts/K8S/'
    icarus = 'ng-icarus'
    commands = [' zgrep {} {} ']

    con = psycopg2.connect(database="****", user="****", password="****",host="****", port="****")
    print(colored("Connected To DryadDB\n", 'green'))
    cur = con.cursor()
    cur.execute(project_query.format(account))
    rows = cur.fetchall()
    results = list(rows)

    for result in results:
        context.append(result[1])
        namespace.append(result[2])
        datacenter.append(result[3])

    #print(context, namespace, datacenter)
    full_path = path + namespace[0] + '/' + icarus + '/' + str(today) + '/' + 'syslog-*'
    #print('full_path')

    if datacenter[0] == 'MN':
        connect_command(mn_hostname, msisdn)

    elif datacenter[0] == 'LH' :
        connect_command(lh_hostname, msisdn)
  
    con.close()
  
    file_creation(msisdn)
    print("Operation in DB has finished And connection has been closed. \n")
    

#sample of execution
syslogs_db('****','****')
