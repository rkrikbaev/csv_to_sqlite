from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key'  # Replace with your secret key

DATABASE = 'data.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

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
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM data_table')
    rows = cursor.fetchall()
    conn.close()
    
    return render_template('data.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
