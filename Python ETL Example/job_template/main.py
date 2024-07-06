# we import the etlfunctions or any other build-in python module
import etlfuncs as etl
from datetime import timedelta

#### Job Info and Metadata ####################################################
# We are getting the master repo (or prod) directory from an env var, so we can chdir in the job folder later
# The job id, name, and other metadata (the latter in dict format allowing multiple values per field) must be given.
repo_dir = etl.os.getenv("BI_REPO1")
job_id = 'BI20_job_template' 
job_name = 'My_Umobile_trafficSources_activations' 
job_metadata = {
    "run_on":etl.os.environ['COMPUTERNAME'],
    "pid":etl.os.getpid(),
    "source_tables":["my_umobile_sd.securedapiresponses"],
    "stage_tables":["bi.bi20_myumobile_sources_stg", "bi20.myumobile_sources_stg"],
    "target_tables":['bi20.myumobile_sources_hist'],
    "authors":["emloyee's ldap user. For example  jon.doe"],
    "accounts":['Account name. For example  BR TIM'],
    "project_codes":["TTS"],
    "tickets":["BI-0001"],
    "products":["SecureD", "VAS"]}

                                                    # Job Parameters #
# Job Parameters. Make sure to include "run.bat" and "manual_run.bat" files in your directory. Copy paste them from other jobs.
# The below code lines, are used in the production server , where your job is running from windows task scheduler with the help of the bat files. min_date and max_date vars are the vars that are going to be used on your sqlqueries.py folder
# When run via IDE, the script always falls back to auto mode (catches the exception of not defined sys.argv[1] which is the variable coming rom the bat file)
try:
  run_mode = etl.sys.argv[1]
except:
  run_mode = 'auto'

if run_mode == 'auto':
    min_date = etl.datetime.now().date() + timedelta(days=-3)
    min_date = min_date.strftime('%Y-%m-%d')    
    
    max_date = etl.datetime.now().date() + timedelta(days=-1)
    max_date = max_date.strftime('%Y-%m-%d')
    
    run_dates_list = etl.pd.date_range(start=min_date, end=max_date, freq='1D')
    run_dates_list = run_dates_list.format(formatter=lambda x: x.strftime('%Y-%m-%d'))
    
elif run_mode == 'manual':
    min_date = etl.sys.argv[2]
    max_date = etl.sys.argv[3]
    run_dates_list = etl.pd.date_range(start=min_date, end=max_date, freq='1D')
    run_dates_list = run_dates_list.format(formatter=lambda x: x.strftime('%Y-%m-%d'))
else:
    etl.sys.exit('Wrong run_mode parameter')

                    # Working Directory Change and SQL import #
# Based on the metadata above, we change the dir and go in the job folder
# Also, run_id and etl_id are set (those are used for moniroting/ troubleshooting and are unique per run)
# FIanlly, after chdir import the SQL queries file
job_dir = repo_dir + '\\jobs\\' + job_id
etl.os.chdir(job_dir)
run_id = etl.datetime.now().strftime("%Y%m%d%H%M%S")
etl_id = f'{job_id}-{run_id}'
import sqlqueries as sq 


                        # Functions #
# Break down the data processing into separate functions that perform certain steps.

def perform_actions(min_date, max_date, etl_id):
    etl.log_screen(f"Hive -> Creating bi.bi20_myumobile_sources_stg for the period {min_date} - {max_date}")
    # Every time that the script is being executed, we drop and recreate the staging table for the corresponding time period.
    etl.run_sql('bihivesys', 'drop table if exists bi.bi20_myumobile_sources_stg')
    # We execute our first query, and we pass into it min_date, max_date and etl_id 
    etl.run_sql('bihivesys', sq.query1.format(min_date = min_date, max_date = max_date, etl_id = etl_id))
    
    # Citus staging table will be dropped and recreated for every execution
    etl.log_screen("Citus -> Creating bi20.myumobile_sources_stg that will host data from Hive")
    etl.run_sql('citus', 'drop table if exists bi20.myumobile_sources_stg')
    etl.run_sql('citus', sq.create1)
    
    # In order to transfer our data from Hive to Citus, we will use one "bridge" Connection A.K.A dblink
    # To create the dblink, please check the ddl.hive.sql file
    etl.log_screen("Hive -> Loading Data from Hive to Citus by using via the dblink connection")
    etl.run_sql('bihivesys', sq.insert1)
    
    # Now we need to transfer the staging data from citus to the final table on citus that will hold all the historical data.
    # In order to create this table, please check the "ddl_citus.sql" file. 
    # For the data insertion to our `production table` we can use the upsert feature of postgresql. More information can be found on the sqlqueries.py folder
    etl.log_screen('Citus : Loading data from Stagging table to Production one')
    etl.run_sql('citus', sq.insert2)
 
# main() is just the wrapper, along with logging some basic info at the beginning of the run
def main():
    etl.log_screen(f'run_id={run_id} pid={job_metadata["pid"]}')
    etl.log_screen(f'run_mode={run_mode} min_date={min_date} max_date={max_date}')
    perform_actions(min_date, max_date, etl_id)


# there's the option to disable DB logging and avoid sending emails upon failures, please refer to etlfuncs file
# This is useful for testing. Don't forget to have both functionalities enabled in prod though
etl.exec_main(main, job_id, job_name, run_id, job_metadata)
