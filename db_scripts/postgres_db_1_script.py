import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta
import hashlib

# Connect to PostgreSQL (adjust connection parameters as needed)
conn = psycopg2.connect(
    dbname="library_class_version",
    user="library_class_version_user",
    password="RGTIiUfgNLXVctih8AqymqQ3UF5CHY2E",
    host="dpg-cr2de8lsvqrc73fkju1g-a.frankfurt-postgres.render.com",  # or the hostname of your PostgreSQL server
    port="5432"        # default port for PostgreSQL
)
cursor = conn.cursor()

# Create the Books table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Books (
        BookID SERIAL PRIMARY KEY,
        Title TEXT NOT NULL,
        Author TEXT NOT NULL,
        ISBN TEXT UNIQUE,
        PublishedYear INTEGER,
        AvailableCopies INTEGER NOT NULL,
        image TEXT
    )
    """
)

# Create the Users table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Users (
        UserID SERIAL PRIMARY KEY,
        Name TEXT NOT NULL,
        Email TEXT UNIQUE,
        Phone TEXT,
        Password TEXT
    )
    """
)

# Create the Loans table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Loans (
        LoanID SERIAL PRIMARY KEY,
        BookID INTEGER REFERENCES Books(BookID),
        UserID INTEGER REFERENCES Users(UserID),
        LoanDate DATE NOT NULL,
        DueDate DATE NOT NULL,
        ReturnDate DATE
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
    VALUES (%s, %s, %s, %s, %s)
    """,
    books
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
    VALUES (%s, %s, %s)
    """,
    users
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
    VALUES (%s, %s, %s, %s, %s)
    """,
    loans
)

# Update Books table with image URLs
image_urls = {
    1: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/The_Great_Gatsby_Cover_1925_Retouched.jpg/220px-The_Great_Gatsby_Cover_1925_Retouched.jpg",
    2: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/To_Kill_a_Mockingbird_%28first_edition_cover%29.jpg/220px-To_Kill_a_Mockingbird_%28first_edition_cover%29.jpg",
    3: "https://upload.wikimedia.org/wikipedia/en/5/51/1984_first_edition_cover.jpg",
    4: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Moby-Dick_FE_title_page.jpg/220px-Moby-Dick_FE_title_page.jpg",
}

for book_id, url in image_urls.items():
    cursor.execute(
        """
        UPDATE Books
        SET image = %s
        WHERE BookID = %s
        """,
        (url, book_id)
    )

# Hash and insert a sample password (for testing)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Update existing users with a sample password
cursor.execute(
    """
    UPDATE Users
    SET Password = %s
    """,
    (hash_password('password123'),)
)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database created and sample data inserted successfully.")
