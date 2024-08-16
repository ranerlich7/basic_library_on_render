from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
