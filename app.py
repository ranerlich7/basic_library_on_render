import hashlib
from flask import Flask, flash, redirect, render_template, request, session, url_for
import sqlite3
import psycopg2.extras
from dotenv import load_dotenv
import os

import psycopg2

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Set secret key from environment variable
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default-secret-key")


def get_connection():
    # Connect to PostgreSQL (adjust connection parameters as needed)
    conn = psycopg2.connect(
        dbname="library_class_version",
        user="library_class_version_user",
        password="RGTIiUfgNLXVctih8AqymqQ3UF5CHY2E",
        host="dpg-cr2de8lsvqrc73fkju1g-a.frankfurt-postgres.render.com",  # or the hostname of your PostgreSQL server
        port="5432",  # default port for PostgreSQL
    )
    return conn


# Function to get the list of books from the database
def get_books():
    conn = get_connection()
    # conn.row_factory = sqlite3.Row
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    print(books[0])
    return books


@app.route("/")
def book_list():
    books = get_books()
    return render_template("books.html", books=books)


# Function to get user by username
def get_user_by_username(username):
    conn = get_connection()
    # conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE Name = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


# Function to authenticate user
def authenticate(username, password):
    user = get_user_by_username(username)
    if user:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return user["Password"] == hashed_password
    return False


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if authenticate(username, password):
            session["username"] = username
            return redirect(url_for("book_list"))
        else:
            flash("Invalid credentials. Please try again.")
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
