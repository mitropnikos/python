import psycopg2
from datetime import datetime

if __name__ == '__main__':
        print "{", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "} Starting killing"
        conn = psycopg2.connect(
                "dbname=**** user=**** host=localhost port=****")
        cursor = conn.cursor()
        cursor.execute( "select pid from"
                        "(select *,((EXTRACT(epoch FROM (SELECT (NOW() - query_start))))::int) as sec "
                        "from pg_Stat_activity where state='active' and  waiting=true "
                        "and query like '%ADD_PARTITION%')where sec>10; "
                      )
        pids = cursor.fetchall()
        num_of_processes_killed=0
        for pid_info in pids:
                pid = pid_info[0]
                #user = pid_info[1].strip()
                print "[", datetime.now().strftime('%Y-%m-%d %H:%M:%S') , "] Killing process with pid:", pid
                cursor.execute('select pg_terminate_backend ({0});'.format(pid))
                num_of_processes_killed+=1
        print "{", datetime.now().strftime('%Y-%m-%d %H:%M:%S') ,"} Killed #", num_of_processes_killed, "processes"
        print "{", datetime.now().strftime('%Y-%m-%d %H:%M:%S') ,"} Stop killing"
