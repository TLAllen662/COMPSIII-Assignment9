#!/usr/bin/env python3
"""
Python script to create a movies table using sqlite3 module.
This script creates a comprehensive movies table with various column types.
"""

import sqlite3
import os

def create_movies_table():
    """
    Create a movies table in the movies.db database with comprehensive columns.
    """
    
    # Database file path
    db_file = 'movies.db'
    
    try:
        # Connect to the SQLite database
        print(f"Connecting to database: {db_file}")
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        
        # Create the movies table with various data types
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            release_year INTEGER,
            duration_minutes INTEGER,
            genre TEXT,
            director TEXT,
            lead_actor TEXT,
            lead_actress TEXT,
            production_company TEXT,
            budget REAL,
            box_office REAL,
            imdb_rating REAL CHECK(imdb_rating >= 0 AND imdb_rating <= 10),
            metacritic_score INTEGER CHECK(metacritic_score >= 0 AND metacritic_score <= 100),
            is_sequel BOOLEAN DEFAULT 0,
            release_date TEXT,
            country TEXT DEFAULT 'USA',
            language TEXT DEFAULT 'English',
            plot_summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
        
        print("Creating movies table...")
        cursor.execute(create_table_sql)
        
        # Create an index on commonly searched columns for better performance
        print("Creating indexes...")
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_movies_title ON movies(title)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_movies_year ON movies(release_year)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_movies_genre ON movies(genre)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_movies_director ON movies(director)')
        
        # Insert some sample data to demonstrate the table structure
        sample_movies = [
            (
                'The Matrix', 1999, 136, 'Science Fiction', 'The Wachowskis',
                'Keanu Reeves', 'Carrie-Anne Moss', 'Warner Bros.',
                63000000, 467200000, 8.7, 73, 0, '1999-03-31',
                'USA', 'English', 'A computer hacker learns about the true nature of reality.',
                '2024-01-01 10:00:00', '2024-01-01 10:00:00'
            ),
            (
                'Inception', 2010, 148, 'Science Fiction', 'Christopher Nolan',
                'Leonardo DiCaprio', 'Marion Cotillard', 'Warner Bros.',
                160000000, 836800000, 8.8, 74, 0, '2010-07-16',
                'USA', 'English', 'A thief who steals corporate secrets through dream-sharing technology.',
                '2024-01-01 10:00:00', '2024-01-01 10:00:00'
            ),
            (
                'Parasite', 2019, 132, 'Thriller', 'Bong Joon-ho',
                'Song Kang-ho', 'Cho Yeo-jeong', 'CJ Entertainment',
                11400000, 263500000, 8.5, 96, 0, '2019-05-30',
                'South Korea', 'Korean', 'A poor family schemes to become employed by a wealthy family.',
                '2024-01-01 10:00:00', '2024-01-01 10:00:00'
            )
        ]
        
        insert_sql = '''
        INSERT OR IGNORE INTO movies (
            title, release_year, duration_minutes, genre, director,
            lead_actor, lead_actress, production_company, budget, box_office,
            imdb_rating, metacritic_score, is_sequel, release_date,
            country, language, plot_summary, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        print("Inserting sample data...")
        cursor.executemany(insert_sql, sample_movies)
        
        # Commit the changes
        connection.commit()
        
        # Display table information
        print("\n" + "="*60)
        print("MOVIES TABLE CREATED SUCCESSFULLY!")
        print("="*60)
        
        # Show table schema
        cursor.execute("PRAGMA table_info(movies)")
        columns = cursor.fetchall()
        
        print("\nTable Schema:")
        print("-" * 60)
        print(f"{'Column':<20} {'Type':<15} {'Nullable':<10} {'Default':<15}")
        print("-" * 60)
        
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            not_null = "NOT NULL" if col[3] == 1 else "NULL"
            default_val = col[4] if col[4] is not None else ""
            print(f"{col_name:<20} {col_type:<15} {not_null:<10} {str(default_val):<15}")
        
        # Show sample data
        cursor.execute("SELECT COUNT(*) FROM movies")
        count = cursor.fetchone()[0]
        print(f"\nTotal movies in database: {count}")
        
        if count > 0:
            print("\nSample movies:")
            print("-" * 60)
            cursor.execute("SELECT title, release_year, director, imdb_rating FROM movies LIMIT 5")
            movies = cursor.fetchall()
            
            print(f"{'Title':<20} {'Year':<6} {'Director':<20} {'Rating':<6}")
            print("-" * 60)
            for movie in movies:
                print(f"{movie[0]:<20} {movie[1]:<6} {movie[2]:<20} {movie[3]:<6}")
        
        print("\n" + "="*60)
        
    except sqlite3.Error as e:
        print(f"SQLite error occurred: {e}")
        return False
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
        
    finally:
        # Close the database connection
        if connection:
            connection.close()
            print(f"Database connection closed.")
    
    return True

def main():
    """
    Main function to run the script.
    """
    print("SQLite3 Movies Table Creation Script")
    print("=" * 40)
    
    success = create_movies_table()
    
    if success:
        print("\n✅ Script completed successfully!")
        print("\nYou can now use the movies table in your applications.")
        print("\nExample usage:")
        print("```python")
        print("import sqlite3")
        print("connection = sqlite3.connect('movies.db')")
        print("cursor = connection.cursor()")
        print("cursor.execute('SELECT * FROM movies')")
        print("movies = cursor.fetchall()")
        print("connection.close()")
        print("```")
    else:
        print("\n❌ Script failed. Please check the error messages above.")

if __name__ == "__main__":
    main()