create table citus_prd_tbl -- prd table
(
local_date	text,
.....
unique (local_date.....)
);
create index col1_aggr_local_date_idx on citus_prd_tbl (local_date);
