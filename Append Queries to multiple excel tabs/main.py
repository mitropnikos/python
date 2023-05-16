from openpyxl import Workbook
import time
import os 
import pandas as pd 
import pyodbc


# Declare your time period and Schema
min_date = '2023-04-01'
max_date = '2023-04-30'
schema = '****'
output_file = f'{schema}_{min_date}_{max_date}.xlsx'

mydir = r'C:\Users\user\...'
os.chdir(mydir)
import sqlqueries as sq

queries_list = [
    sq.query1,
    sq.query2,
    sq.query3,
    sq.query4,
    sq.query5,
    sq.query6,
    sq.query7,
    sq.query8,
    sq.query9  
    ]

# Excel 
tab_names = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9"
    ]

def get_sql_data(dsn, query):
    conn = pyodbc.connect(f'DSN={dsn}', autocommit=True)
    return pd.read_sql(query, conn)
    conn.close()
    

def main():
    try:
        start_time = time.time()
        # Create a new workbook
        workbook = Workbook()
        
        # Iterate over the queries and tab names
        for query, tab_name in zip(queries_list, tab_names):
            print(f"Running query: {tab_name}")
            data = get_sql_data('conn', query.format(schema = schema, min_date = min_date, max_date = max_date))
            # Create a new worksheet for the query results
            worksheet = workbook.create_sheet(title=tab_name)
            # column headers to the worksheet
            headers = data.columns.tolist()
            worksheet.append(headers)
            
            # Write the data to the worksheet
            for _, row in data.iterrows():
                worksheet.append(row.tolist())    
            print(f"{tab_name} query finished.")
                
        # Remove the default sheet created by openpyxl
        workbook.remove(workbook["Sheet"])
        
        # Save the workbook to the output file
        workbook.save(output_file)
        end_time = time.time()
        total_time = (end_time - start_time) / 60
        print(f"File generated in the following path : {mydir}")
        print(f"Total execution time: {total_time:.2f} Minutes")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()  
