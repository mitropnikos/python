-- Hive internal table
CREATE TABLE bi.test_fact_table
col1 string,
col2 string
)


-- Example of link to Citus table from Hive
CREATE TABLE bi.citus_bi20_myumobile_sources_stg
USING org.apache.spark.sql.jdbc
OPTIONS (
	url "jdbc:postgresql://citus01.**.*****5432/citus?user=citus&password={}",
	dbtable="bi20.myumobile_sources_stg"
)

/*

This statement is being executed on Hive's side.
Before you execute your python script, create the table on Citus side and then execute the below statement on hive.
You need to declare the below statements :
    1. password : ...&password=123456..
    2. dbtable. This is the name of the table that you created on Citus Side.
    
*/
