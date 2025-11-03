import sqlite3
import requests
from bs4 import BeautifulSoup

# Connect to database
connection = sqlite3.connect('movies.db')
# request wikipedia page
response = requests.get('https://en.wikipedia.org/wiki/List_of_American_films_of_2023')
soup = BeautifulSoup(response.content, 'html.parser')
title = soup.find('title').text
print(f"Page Title: {title}")
cursor = connection.cursor()

# Create table
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
connection.commit()
connection.close()

print("Database 'movies.db' created successfully!")





