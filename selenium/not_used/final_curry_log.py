import psycopg2
from termcolor import colored
import paramiko
import time
from paramiko import SSHClient
import csv
import os

global curry_connect
curry_connect = ''
global currynode1
global currynode2
curry_logs_node1 = []
curry_logs_node2 = []




def connect_ssh(vm,connect):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=vm, port=port, username=username, password=password)
    curry_connect = connect 
    print("Connected to" +  str(vm))

def connect_command(node,msisdn,result,curry_logs,lista):
    
    global curry_result
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=node, port=port, username=username, password=password)
    print("Connected to" + str(node))

    for command in commands:
        stdin, stdout, stderr = client.exec_command(command.format(msisdn))
        time.sleep(1)
        outlines = stdout.readlines()
        result = ''.join(outlines)

        if len(result) == 0:
            lista.append(0)
            print("no result for" + str(msisdn) + "on" +  str(node))

        else:
            curry_logs = result
            lista.append(result)
            #print(curry_logs)

        client.close()
        print('Connection to' + str(node) +  'has been closed')

def file_creation():
    full_logs = curry_logs_node1 + curry_logs_node2

    for text in sorted(full_logs):

        if curry_logs_node1 == 0 and curry_logs_node2 == 0:
            print("No Results for" +  str(msisdn))

        else:

            f = open("full_logs.txt", 'a')
            f.write(str(text))
            f.close()
            #works only on linux
            #sort_files = 'cat full_logs.txt | sort -k1 > sorted__curry_logs.txt'
            #os.system(sort_files)

def logs_db(tlc,msisdn):

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
    global port
    port = ****
    global username
    username = "****"
    global password
    password = "****"
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
    print(colored("Connected To DB\n", 'green'))
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
                print("found" +  str(tlc)+ "in saved_projects_list with curry node 1 :" +  str(node_1[0]) + "and curry node 2 :" +  str(node_2[0]))

                if hostname_node1 == node_1[0]: 

                    try:
                        connect_ssh(hostname_node1,'1')
                        curry_connect = '1'
                    except:
                        curry_connect = '2' 

                    if curry_connect == '1': 
                        connect_command(hostname_node1,msisdn,'result_1','curry_logs_1',curry_logs_node1)
                      

                    elif curry_connect == '2':  
                        print(str(tlc) + "is configured in DB but" +  str(hostname_node1) +  "is not legit \nPlease provide the correct nodes")
                        hostname_node1 = input("Dwse node1 : ")
                        cur.execute(update_node1_query.format(hostname_node1.lower().strip(), tlc))
                        con.commit() 
                        print(str(tlc) + "Curry Node 1 has been updated with the following value :" + str(hostname_node1))

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
                        print(str(tlc) + " is configured in DB but" +  str(hostname_node2) +  "is not legit \nPlease provide the correct nodes")
                        hostname_node2 = input("Dwse node2 : ")
                        cur.execute(update_node2_query.format(hostname_node2.lower().strip(), tlc))
                        con.commit()  
                        print( + " Curry Node 2 has been updated with the following value :" +  str(hostname_node2))
                      
                        connect_command(hostname_node2,msisdn,'result_2','curry_logs_2',curry_logs_node2)
                  

            break

        else:
            print(colored(str(tlc) +  "is not configured"))
            print("Press 1 if you want to configure it now")
            print("Press 2 to exit")
            type = input("Dwse value gia na sinexiseis : ")

            if type == '1':
                project = input("Dwse project : ")
                currynode1 = input("Dwse host gia curry node 1 : ")
                currynode2 = input("Dwse host gia curry node 2 : ")

                cur.execute(project_query_insert.format(project.upper().strip(), currynode1.strip().lower(),currynode2.strip().lower()))
                con.commit()
                print("1 item inserted successfully")

                connect_command(currynode1,msisdn,'result_1','curry_logs_1',curry_logs_node1)
                connect_command(currynode2,msisdn,'result_2','curry_logs_2',curry_logs_node2)


                break

            elif type == '2':
                print(".......................")
                break

            else:
                print("Dwse dwsto value...")
                print(".......................")

    print("")
    con.close()
    print("Operation in DB has finished And connection has been closed. \n")
    file_creation()
    #os.remove("full_logs.txt")


# sample of execution
logs_db('****'.strip().upper(),'****'.strip())
