query1 = """
create table bi.bi20_myumobile_sources_stg as 
with v1 as 
(
     select	
            local_date,
            service,
    		trafficsource,
    		count(case when fraudulent = 1 then 1 end) as sbb_subs,
    		count(case when fraudulent = 0 then 1 end) as no_sbb_subs,
    		count(*) as subs,
            '{etl_id}' as etl_id
    from tbl 
    where 
    	local_date >= '{min_date}' and local_date <= '{max_date}'
    and result = 'SUCCESS'
    group by 1,2,3
) 
select * 
from v1 
"""


create1 = """
create table bi20.myumobile_sources_stg 
(
	local_date text,
    service text,
	trafficsource text,
	sbb_subs bigint,
	no_sbb_subs bigint,
	subs bigint,
	etl_id text
)
"""

insert1 = """
insert into bi.citus_bi20_myumobile_sources_stg
select * from bi.bi20_myumobile_sources_stg
"""

insert2 = """
insert into bi20.myumobile_sources_hist
select * 
from bi20.myumobile_sources_stg
on conflict(local_date, service, trafficsource)
do 
	update set 
				sbb_subs = EXCLUDED.sbb_subs,
				no_sbb_subs = EXCLUDED.no_sbb_subs,
				subs = EXCLUDED.subs
"""

# Explanation below : 
"""
1. The ON CONFLICT clause specifies that if a row being inserted would violate the unique constraint defined on the (local_date, service, trafficsource) 
columns, then instead of inserting a new row, an update will be performed on the existing row.

2. The DO UPDATE SET clause specifies how to update the existing row. In this case, the sbb_subs, no_sbb_subs, and subs columns 
of the existing row will be set to the corresponding values from the row being inserted. 
3. The EXCLUDED keyword is used to refer to the values being inserted into the table.

Conluding : 
We are inserting rows into myumobile_sources_hist, and if there is a conflict with the unique constraint, 
it will update the existing row with the new values being inserted.
"""
