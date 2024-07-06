create table bi20.myumobile_sources_hist
(
	local_date text,
    service text,
	trafficsource text,
	sbb_subs bigint,
	no_sbb_subs bigint,
	subs bigint,
	etl_id text,
unique(local_date, service, trafficsource)
);
create index myumobile_sources_hist_local_date_idx on bi20.myumobile_sources_hist (local_date);

/*

1. The "unique" constraint and the end of the `create table` ensures that no two rows in the table can have the same 
combination of values for local_date, service, and trafficsource.

2. The "create index" statement, creates an index on the local_date column that will make queries faster 
by allowing the database to quickly locate the relevant rows.

*/
