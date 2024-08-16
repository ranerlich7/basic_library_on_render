import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Add a new column "image" to the Books table
cursor.execute('''
ALTER TABLE Books
ADD COLUMN image TEXT
''')


# Commit the changes and close the connection
conn.commit()
conn.close()
