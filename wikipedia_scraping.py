import sqlite3

#connect to database
conn = sqlite3.connect('movies.db')

cursor = conn.cursor()

#create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        year INTEGER,
        genre TEXT,
        director TEXT
    )
''')

# Commit changes and close connection
conn.commit()
conn.close()

print("Database 'movies.db' created successfully!")





