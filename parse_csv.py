# importing csv module
import csv
# importing sqlite3 module
import sqlite3

import os
import fnmatch

from config import config

db_file = config.get('db_csv.db')
table_name = config.get('csv_data')
directory = config.get('path_csv')

def send_data(directory):
    
    csv_files = find_csv_files(directory)
    for file in csv_files:
        print(file)
        csv_to_sqlite(csv_file=file, db_file=db_file, table_name=table_name)
        

def find_csv_files(directory):
    csv_files = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.csv'):
            csv_files.append(os.path.join(root, filename))
    return csv_files

# # Example usage
# directory = '/path/to/directory'
# csv_files = find_csv_files(directory)
# for file in csv_files:
#     print(file)

def csv_to_sqlite(csv_file, db_file='db_csv.db', table_name='csv_data'):
  
    # read the csv file
    with open(csv_file , 'r') as csvfile:
        # create the object of csv.reader()
        csv_file_reader = csv.reader(csvfile,delimiter=',')
        # skip the header 
        next(csv_file_reader,None)
        # create fileds 
        sr =''
        period=''
        data_value=''
        suppressed=''
        status = ''
        units= ''
        magnitude =''

        ##### create a database table using sqlite3###

        # 1. create query    
        Table_Query = f'''CREATE TABLE if not Exists {table_name} 
        (Series_reference TEXT,Period TEXT,Data_value TEXT,
        Suppressed TEXT,STATUS TEXT,UNITS TEXT,Magnitude REAL)'''

        # 2. create database
        connection=sqlite3.connect(db_file)
        curosr=connection.cursor()
        # 3. execute table query to create table
        curosr.execute(Table_Query)

        # 4. pase csv data
        for row in csv_file_reader:
            # skip the first row
            for i in range(len(row)):
                # assign each field its value
                sr=row[0]
                period=row[1]
                data_value=row[2]
                suppressed=row[3]
                status = row[4]
                units= row[5]
                magnitude = row[6]

            # 5. create insert query
            InsertQuery=f"INSERT INTO {table_name} VALUES ('{sr}','{period}','{data_value}','{suppressed}','{status}','{units}','{magnitude}')"
            # 6. Execute query
            curosr.execute(InsertQuery)
        # 7. commit changes
        connection.commit()
        # 8. close connection
        connection.close()
