import sqlite3
from datetime import datetime, timedelta

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create the Books table
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Books (
    BookID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    Author TEXT NOT NULL,
    ISBN TEXT UNIQUE,
    PublishedYear INTEGER,
    AvailableCopies INTEGER NOT NULL
)
"""
)

# Create the Users table
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Email TEXT UNIQUE,
    Phone TEXT
)
"""
)

# Create the Loans table
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Loans (
    LoanID INTEGER PRIMARY KEY AUTOINCREMENT,
    BookID INTEGER,
    UserID INTEGER,
    LoanDate DATE NOT NULL,
    DueDate DATE NOT NULL,
    ReturnDate DATE,
    FOREIGN KEY (BookID) REFERENCES Books(BookID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
)
"""
)

# Insert sample data into Books table
books = [
    ("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", 1925, 5),
    ("To Kill a Mockingbird", "Harper Lee", "9780061120084", 1960, 3),
    ("1984", "George Orwell", "9780451524935", 1949, 4),
    ("Moby Dick", "Herman Melville", "9781503280786", 1851, 2),
]

cursor.executemany(
    """
INSERT INTO Books (Title, Author, ISBN, PublishedYear, AvailableCopies)
VALUES (?, ?, ?, ?, ?)
""",
    books,
)

# Insert sample data into Users table
users = [
    ("Alice Johnson", "alice.johnson@example.com", "555-1234"),
    ("Bob Smith", "bob.smith@example.com", "555-5678"),
    ("Carol White", "carol.white@example.com", "555-8765"),
]

cursor.executemany(
    """
INSERT INTO Users (Name, Email, Phone)
VALUES (?, ?, ?)
""",
    users,
)

# Insert sample data into Loans table
# Generate some loan dates
today = datetime.now().date()
due_date_10_days = today + timedelta(days=10)

loans = [
    (1, 1, today, due_date_10_days, None),  # BookID 1, UserID 1
    (2, 2, today, due_date_10_days, None),  # BookID 2, UserID 2
    (3, 3, today, due_date_10_days, today),  # BookID 3, UserID 3 (already returned)
]

cursor.executemany(
    """
INSERT INTO Loans (BookID, UserID, LoanDate, DueDate, ReturnDate)
VALUES (?, ?, ?, ?, ?)
""",
    loans,
)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database created and sample data inserted successfully.")
