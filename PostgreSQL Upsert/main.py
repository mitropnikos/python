import etlfuncs as etl
from datetime import timedelta, datetime

#               job info
job_id = 'jobX'
job_name = '***'


#              Job config
job_dir = repo_dir + '\\jobs\\' + job_id
etl.os.chdir(job_dir)
run_id = etl.datetime.now().strftime("%Y%m%d%H%M%S")
etl_id = f'{job_id}-{run_id}'
import sqlqueries as sq


#            Parameters

run_mode = etl.sys.argv[1]
#run_mode = 'auto'

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
    
    
    
def job(min_date, max_date, etl_id ):
    # extracting data from hive
    etl.log_screen(f'HIVE: Creating hdfs_staging_table for time range >= {min_date} and <= {max_date}')
    etl.run_sql('bihivesys', 'drop table if exists hdfs_staging_table')
    etl.run_sql('bihivesys', sq.query1.format(min_date = min_date, max_date = max_date, etl_id = etl_id))
    etl.run_sql('bihivesys', 'refresh table hdfs_staging_table')

    # Creating citus staging table that will host the data from the above step
    etl.log_screen('Citus : Creating citus_staging_tbl')
    etl.run_sql('citus', 'drop table if exists citus_staging_tbl')
    etl.run_sql('citus', sq.query2)

    # We trasfer the Data from Hive to Citus by using a "bridge connection" -- ddl_hive.sql
    etl.log_screen('Loading Data from Hive to Citus - Bridge Connection - ')
    etl.run_sql('bihivesys', sq.query3)

    #We tranfer the stagging data on Citus to our main table that hosts all historical data
    etl.log_screen('Citus : Loading data from Stagging table to Production one')
    etl.run_sql('citus', sq.query4)
    
    
