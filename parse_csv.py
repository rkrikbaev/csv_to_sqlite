# importing csv module
import csv
# importing sqlite3 module
import sqlite3

import os
import fnmatch     

# create database
connection=sqlite3.connect(db_file)
curosr=connection.cursor()

def find_csv_files(directory):
    csv_files = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.csv'):
            csv_files.append(os.path.join(root, filename))
    return csv_files

def read_from_csv(csv_file):
    # read the csv file
    with open(csv_file , 'r') as csvfile:
        # create the object of csv.reader()
        csv_file_reader = csv.reader(csvfile, delimiter=',')
        # skip the header 
        next(csv_file_reader,None)
        # pase csv data
        values = [ (row[0], row[1]) for row in csv_file_reader ]
        return values

def add_columns_to_table(db_file, table_name, data_from_csv):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
           
    # Check if the column already exists in the table
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    column_names = [ col[1] for col in columns ]
    for value_name, value in data_from_csv:
        column_name = value_name
        if value_name in column_names:
            pass
        else:
            # Check type
            if type(value) == int:
                print('The value is an integer.')
                column_type = 'INT'
            elif type(value) == float:
                print('The value is a float.')
                column_type = 'REAL' 
            elif type(value) == str:
                print('The value is a string.')
                column_type = 'TEXT' 
            else:
                print('The type of the value is unknown.')
                return                    
            # Add the column to the table
            query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};"
            cursor.execute(query)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def add_table_in_db(csv_file_headers):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # db fileds
    columns = ', '.join(csv_file_headers)           
    Table_Query = f'''CREATE TABLE if not Exists {table_name} ( {columns} )'''
    
    # Execute table query to create table
    curosr.execute(Table_Query)
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()               
               
def put_to_sqlite(list:data, string:db_file='db_csv.db', string:table_name='csv_data'):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Check if the current value already exists in the table
    value_to_check = data[0]  # The value to check is in the first column
    check_query = f'SELECT COUNT(*) FROM {table_name} WHERE column_name = dt'
    cursor.execute(check_query, (value_to_check,))
    result = cursor.fetchone()
    if result[0] == 0:  # If the count is 0, the value doesn't exist in the table                    
        # assign each field its value
        # create insert query
        values = [ x[0] fro x in data]
        values_as_string = ','.join(values)
        InsertQuery=f"INSERT INTO {table_name} VALUES ({values_as_string})"
        # Execute query
        curosr.execute(InsertQuery)
        # commit changes
        connection.commit()
        # close connection
        connection.close()
