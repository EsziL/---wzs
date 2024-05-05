# app.py

from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from utils import connect_to_database

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect to MySQL
db = connect_to_database()
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/register', methods=['GET', 'POST'])
def register():
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
    if 'logged_in' in session:
        return f'Hello, {session["username"]}! This is your profile page.'
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=25573, host="0.0.0.0")
