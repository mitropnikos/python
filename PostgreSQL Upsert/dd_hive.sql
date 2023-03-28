-- Bridge Connecton Hive - SQL
CREATE TABLE hdfs_citus_pridge_connection
USING org.apache.spark.sql.jdbc
OPTIONS (
	url "jdbc:postgresql://citus01....:{}port/citus?user=citus&password={pass}",
	dbtable="citus_staging_tbl "
)
