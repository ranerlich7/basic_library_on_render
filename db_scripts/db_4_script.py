import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Add Password column to Users table
cursor.execute("ALTER TABLE Users ADD COLUMN Password TEXT")

# Hash and insert a sample password (for testing)
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Update existing users with a sample password
cursor.execute("UPDATE Users SET Password = ?", (hash_password('password123'),))

# Commit changes and close connection
conn.commit()
conn.close()

print("Database schema updated and sample password set.")
