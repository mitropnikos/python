import pyodbc
import hdfs
import pandas as pd

def run_sql(dsn, query):
    conn = pyodbc.connect(f'DSN={dsn}', autocommit=True)
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.close()

def get_sql_data(dsn, query):
    conn = pyodbc.connect(f'DSN={dsn}', autocommit=True)
    return pd.read_sql(query, conn)
    conn.close()
