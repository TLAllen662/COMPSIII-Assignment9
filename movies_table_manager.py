#!/usr/bin/env python3
"""
Python script to work with the existing movies table structure using sqlite3 module.
"""

import sqlite3

def show_table_info():
    """
    Display information about the existing movies table.
    """
    print("Movies Table Information")
    print("=" * 40)
    
    try:
        connection = sqlite3.connect('movies.db')
        cursor = connection.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='movies'")
        if not cursor.fetchone():
            print("❌ Movies table does not exist!")
            return False
        
        # Show table structure
        cursor.execute("PRAGMA table_info(movies)")
        columns = cursor.fetchall()
        
        print("\nCurrent Table Structure:")
        print("-" * 50)
        print(f"{'Column':<15} {'Type':<12} {'Not Null':<10} {'Default':<10}")
        print("-" * 50)
        
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            not_null = "YES" if col[3] == 1 else "NO"
            default_val = str(col[4]) if col[4] is not None else ""
            print(f"{col_name:<15} {col_type:<12} {not_null:<10} {default_val:<10}")
        
        # Show current data count
        cursor.execute("SELECT COUNT(*) FROM movies")
        count = cursor.fetchone()[0]
        print(f"\nTotal movies in database: {count}")
        
        # Show sample data if any exists
        if count > 0:
            cursor.execute("SELECT * FROM movies LIMIT 3")
            movies = cursor.fetchall()
            print(f"\nSample data:")
            print("-" * 50)
            for movie in movies:
                print(f"ID: {movie[0]}, Title: {movie[1]}, Year: {movie[2]}")
                print(f"Genre: {movie[3]}, Director: {movie[4]}")
                if len(movie) > 5:
                    print(f"Rating: {movie[5]}")
                if len(movie) > 6:
                    print(f"Description: {movie[6][:50]}...")
                print("-" * 30)
        
        connection.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")
        return False

def insert_sample_movies():
    """
    Insert sample movies using the existing table structure.
    """
    print("\nInserting Sample Movies")
    print("=" * 30)
    
    try:
        connection = sqlite3.connect('movies.db')
        cursor = connection.cursor()
        
        # Sample movies data matching the existing structure (id, title, year, genre, director, rating, description)
        sample_movies = [
            ('The Matrix', 1999, 'Science Fiction', 'The Wachowskis', 8.7, 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.'),
            ('Inception', 2010, 'Science Fiction', 'Christopher Nolan', 8.8, 'A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.'),
            ('The Godfather', 1972, 'Crime', 'Francis Ford Coppola', 9.2, 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.'),
            ('Pulp Fiction', 1994, 'Crime', 'Quentin Tarantino', 8.9, 'The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.'),
            ('The Dark Knight', 2008, 'Action', 'Christopher Nolan', 9.0, 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.')
        ]
        
        # Insert movies (without ID as it's auto-increment)
        insert_sql = '''
        INSERT OR IGNORE INTO movies (title, year, genre, director, rating, description) 
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        
        for movie in sample_movies:
            cursor.execute(insert_sql, movie)
            print(f"✅ Inserted: {movie[0]} ({movie[1]})")
        
        connection.commit()
        
        # Show updated count
        cursor.execute("SELECT COUNT(*) FROM movies")
        count = cursor.fetchone()[0]
        print(f"\nTotal movies now in database: {count}")
        
        connection.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")
        return False

def demonstrate_queries():
    """
    Demonstrate various SQL queries on the movies table.
    """
    print("\nSQL Query Demonstrations")
    print("=" * 30)
    
    try:
        connection = sqlite3.connect('movies.db')
        cursor = connection.cursor()
        
        # Query 1: All movies
        print("\n1. All movies:")
        cursor.execute("SELECT title, year, director FROM movies ORDER BY year")
        movies = cursor.fetchall()
        for movie in movies:
            print(f"   {movie[0]} ({movie[1]}) - {movie[2]}")
        
        # Query 2: Movies with high ratings
        print("\n2. Movies with rating > 8.5:")
        cursor.execute("SELECT title, rating FROM movies WHERE rating > 8.5 ORDER BY rating DESC")
        high_rated = cursor.fetchall()
        for movie in high_rated:
            print(f"   {movie[0]} - {movie[1]}")
        
        # Query 3: Movies by genre
        print("\n3. Movies by genre:")
        cursor.execute("SELECT genre, COUNT(*) as count FROM movies GROUP BY genre ORDER BY count DESC")
        genres = cursor.fetchall()
        for genre in genres:
            print(f"   {genre[0]}: {genre[1]} movies")
        
        # Query 4: Recent movies (after 2000)
        print("\n4. Movies after 2000:")
        cursor.execute("SELECT title, year FROM movies WHERE year > 2000 ORDER BY year DESC")
        recent = cursor.fetchall()
        for movie in recent:
            print(f"   {movie[0]} ({movie[1]})")
        
        connection.close()
        
    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")

def create_movies_table_template():
    """
    Show the template for creating a movies table.
    """
    print("\nMovies Table Creation Template")
    print("=" * 40)
    
    template = '''
import sqlite3

def create_movies_table():
    # Connect to database
    connection = sqlite3.connect('movies.db')
    cursor = connection.cursor()
    
    # Create table with various data types
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        year INTEGER,
        genre TEXT,
        director TEXT,
        rating REAL CHECK(rating >= 0 AND rating <= 10),
        description TEXT,
        budget REAL,
        box_office REAL,
        duration_minutes INTEGER,
        release_date TEXT,
        country TEXT DEFAULT 'USA',
        language TEXT DEFAULT 'English',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Commit and close
    connection.commit()
    connection.close()
    print("Movies table created successfully!")

# Usage
create_movies_table()
    '''
    
    print(template)

if __name__ == "__main__":
    print("SQLite3 Movies Table Management Script")
    print("=" * 50)
    
    # Show current table info
    if show_table_info():
        # Insert sample data
        insert_sample_movies()
        
        # Demonstrate queries
        demonstrate_queries()
        
        # Show template for future reference
        create_movies_table_template()
        
        print("\n" + "="*50)
        print("✅ Script completed successfully!")
        print("Your movies.db database is ready to use.")
    else:
        print("❌ Could not access movies table.")