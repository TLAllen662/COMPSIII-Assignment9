import sqlite3
import os

def reset_database():
    """Reset the database with the correct table structure for tests."""
    
    # Delete existing database if it exists
    if os.path.exists('movies.db'):
        os.remove('movies.db')
        print("Deleted existing movies.db")
    
    # Create new database with correct structure
    connection = sqlite3.connect('movies.db')
    cursor = connection.cursor()
    
    # Create table to match test expectations exactly
    cursor.execute('''
        CREATE TABLE movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            worldwide_gross INTEGER,
            year INTEGER
        )
    ''')
    
    connection.commit()
    connection.close()
    print("Created new movies.db with correct structure")
    
    # Verify the structure
    connection = sqlite3.connect('movies.db')
    cursor = connection.cursor()
    cursor.execute("PRAGMA table_info(movies)")
    columns = cursor.fetchall()
    
    print("New table structure:")
    for col in columns:
        print(f"  {col}")
    
    connection.close()

if __name__ == "__main__":
    reset_database()