import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Optional: Update the new column with image URLs
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
    SET image = ?
    WHERE BookID = ?
    """,
        (url, book_id),
    )


# Commit the changes and close the connection
conn.commit()
conn.close()
