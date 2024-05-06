# app.py

from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from utils import connect_to_database
from threading import Thread
import time
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect to MySQL
db = connect_to_database()
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lostwave')
def lostwave():
    return render_template("lostwave.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[0], password):
            session['logged_in'] = True
            session['username'] = username
            return redirect('/profile')
        else:
            return 'Invalid username or password'

    return render_template('login.html')

@app.route('/userdata', methods=['GET'])
def userdata():
    if 'logged_in' in session and session['logged_in']:
        username = session['username']

        # Perform a database query to retrieve user data based on the username
        #cursor.execute("SELECT username, email, other_column FROM users WHERE username = %s", (username,))
        try:
            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        except:
            return jsonify({'error': 'Internal server error'}), 500
        user_data = cursor.fetchone()  # Assuming only one row per username

        if user_data:
            # Convert user data to a dictionary and return it as JSON
            user_json = {
                'username': user_data[0],
                #'password': user_data[1]
                # Add other user data fields here
            }
            return jsonify(user_json)
        else:
            return jsonify({'error': 'User not found'}), 404
    else:
        return jsonify({'error': 'User not logged in'}), 401


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'logged_in' in session and session['logged_in']:
        return redirect('/profile')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)  # Hash the password

        # Check if username already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return 'Username already exists. Please choose another username.'
        
        # Insert new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        db.commit()

        session['logged_in'] = True
        session['username'] = username
        return redirect('/profile')

    return render_template('register.html')

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect('/')

def keep_mysql_connection_alive(cursor):
    # Periodically execute a lightweight query to keep the connection alive
    while True:
        try:
            cursor.execute("SELECT 1")
            time.sleep(60)  # Execute the query every 60 seconds

        except mysql.connector.Error as e:
            print("MySQL Error:", e)
            # Reconnect to the database if there's an error
            db.reconnect()
            cursor = db.cursor()

        except Exception as e:
            print("Error occurred:", e)
            # Handle other exceptions if necessary
            time.sleep(60)  # Wait before retrying

# Start a separate thread to keep the MySQL connection alive
keep_alive_thread = Thread(target=keep_mysql_connection_alive, args=(cursor,))
keep_alive_thread.daemon = True
keep_alive_thread.start()

if __name__ == '__main__':
    app.run(debug=True, port=25573, host="0.0.0.0")
