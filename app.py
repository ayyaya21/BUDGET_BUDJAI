from flask import Flask, render_template, request, redirect, session
import hashlib
import mysql.connector
from flask import redirect
import os

app = Flask(__name__)
db_config = {
    'user': 'root',
    'password': '6939',
    'host': 'localhost',
    'database': 'db',
}
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
app.secret_key = 'pormungtai'

# Generate a secure random salt
salt = os.urandom(16)

def table_exists(table_name):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    return cursor.fetchone() is not None

if not table_exists('users'):
    cursor.execute('''
        CREATE TABLE users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        )
    ''')
    conn.commit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE name = %s", (name,))  # Update to 'name'
        user = cursor.fetchone()

        if user and verify_password(password, user[2]):
            session['email'] = user[1]
            return redirect('/login_success')

        return render_template('login_failed.html', error='Invalid user')

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        hashed_password = hash_password(password)

        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        conn.commit()

        return render_template("registration_confirmation.html")

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if 'email' in session:
        return render_template("dashboard.html", email=session['email'])
    else:
        return redirect('/login')

@app.route("/home")
def home():
    return render_template("home.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

def hash_password(password):
    password = password.encode('utf-8') + salt
    hashed_password = hashlib.sha256(password).hexdigest()
    return hashed_password

def verify_password(input_password, stored_password):
    input_password = input_password.encode('utf-8') + salt
    hashed_input_password = hashlib.sha256(input_password).hexdigest()
    return hashed_input_password == stored_password

if __name__ == "__main__":
    app.run(debug=True, port=3000)