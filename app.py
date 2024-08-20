import hashlib
from flask import Flask, flash, redirect, render_template, request, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'assgasdghw4362347ustf'  # Change this to a real secret key for production

# Function to get the list of books from the database
def get_books():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Books')
    books = cursor.fetchall()
    conn.close()
    return books

@app.route('/')
def book_list():
    books = get_books()
    return render_template('books.html', books=books)


# Function to get user by username
def get_user_by_username(username):
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE Name = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Function to authenticate user
def authenticate(username, password):
    user = get_user_by_username(username)
    if user:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return user['Password'] == hashed_password
    return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate(username, password):
            session['username'] = username
            return redirect(url_for('book_list'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
