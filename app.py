from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key'  # Replace with your secret key

from config import config
from parce_csv import *

DATABASE = config.get('db_file')
OBJECTS = config.get('objects')
DIR = config.get('path_to_csv')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def update_db(object_name):
    csv_files = find_csv_files(DIR)
    for file in csv_files:
        print(file)
        to_sqlite(
            data=from_csv(file), 
            db_file=DATABASE, 
            table_name=object_name)  

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('logged_in', None)
        username = request.form['username']
        password = request.form['password']
        
        # Add your login validation logic here
        # For simplicity, let's assume the correct username is "admin" and password is "password"
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect('/data')
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/data')
def data():
    if not session.get('logged_in'):
        return redirect('/')
    
    update_db(directory)    
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM data_table')
#     rows = cursor.fetchall()
#     conn.close()
    
    return render_template('data.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
