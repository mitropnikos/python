query1 = """
create table hdfs_staging_table as 
....
"""

query2 = """
create table citus_staging_tbl 
(
....
)
"""

query3 = """
insert into hdfs_citus_staging_tbl
select * from hdfs_staging_table 
"""

query4 = """
insert into citus_prd_tbl
select *
from hdfs_citus_staging_tbl
on conflict (local_date.....)
do 
	update set 	
				subscribed = EXCLUDED.subscribed,
        ......
"""
