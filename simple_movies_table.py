#!/usr/bin/env python3
"""
Simple Python script to create a movies table using sqlite3 module.
"""

import sqlite3

def create_movies_table():
    """
    Create a movies table with comprehensive columns and data types.
    """
    
    try:
        # Connect to the SQLite database
        print("Connecting to movies.db...")
        connection = sqlite3.connect('movies.db')
        cursor = connection.cursor()
        
        # First, let's check if the table already exists and its structure
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='movies'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("Movies table already exists. Current structure:")
            cursor.execute("PRAGMA table_info(movies)")
            columns = cursor.fetchall()
            print(f"{'Column':<20} {'Type':<15} {'Not Null':<10} {'Default':<15}")
            print("-" * 60)
            for col in columns:
                not_null = "YES" if col[3] == 1 else "NO"
                default_val = col[4] if col[4] is not None else ""
                print(f"{col[1]:<20} {col[2]:<15} {not_null:<10} {str(default_val):<15}")
        else:
            # Create the movies table with various data types
            print("Creating new movies table...")
            create_table_sql = '''
            CREATE TABLE movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                year INTEGER,
                genre TEXT,
                director TEXT,
                lead_actor TEXT,
                production_company TEXT,
                budget REAL,
                box_office REAL,
                imdb_rating REAL CHECK(imdb_rating >= 0 AND imdb_rating <= 10),
                is_sequel BOOLEAN DEFAULT 0,
                release_date TEXT,
                country TEXT DEFAULT 'USA',
                language TEXT DEFAULT 'English',
                plot_summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            '''
            
            cursor.execute(create_table_sql)
            print("Movies table created successfully!")
            
            # Show the new table structure
            cursor.execute("PRAGMA table_info(movies)")
            columns = cursor.fetchall()
            print("\nNew table structure:")
            print(f"{'Column':<20} {'Type':<15} {'Not Null':<10} {'Default':<15}")
            print("-" * 60)
            for col in columns:
                not_null = "YES" if col[3] == 1 else "NO"
                default_val = col[4] if col[4] is not None else ""
                print(f"{col[1]:<20} {col[2]:<15} {not_null:<10} {str(default_val):<15}")
        
        # Insert some sample data if the table is empty
        cursor.execute("SELECT COUNT(*) FROM movies")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print(f"\nTable is empty. Inserting sample data...")
            sample_movies = [
                ('The Matrix', 1999, 'Science Fiction', 'The Wachowskis', 'Keanu Reeves', 'Warner Bros.', 63000000, 467200000, 8.7, 0, '1999-03-31', 'USA', 'English', 'A computer hacker learns about the true nature of reality.'),
                ('Inception', 2010, 'Science Fiction', 'Christopher Nolan', 'Leonardo DiCaprio', 'Warner Bros.', 160000000, 836800000, 8.8, 0, '2010-07-16', 'USA', 'English', 'A thief who steals corporate secrets through dream-sharing technology.'),
                ('The Godfather', 1972, 'Crime', 'Francis Ford Coppola', 'Marlon Brando', 'Paramount Pictures', 6000000, 246120974, 9.2, 0, '1972-03-24', 'USA', 'English', 'The aging patriarch of an organized crime dynasty transfers control to his reluctant son.')
            ]
            
            insert_sql = '''
            INSERT INTO movies (
                title, year, genre, director, lead_actor, production_company, 
                budget, box_office, imdb_rating, is_sequel, release_date, 
                country, language, plot_summary
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            cursor.executemany(insert_sql, sample_movies)
            print(f"Inserted {len(sample_movies)} sample movies.")
        else:
            print(f"\nTable already contains {count} movies.")
        
        # Show current data
        cursor.execute("SELECT title, year, director, imdb_rating FROM movies LIMIT 5")
        movies = cursor.fetchall()
        
        if movies:
            print(f"\nCurrent movies in database:")
            print(f"{'Title':<25} {'Year':<6} {'Director':<25} {'Rating':<6}")
            print("-" * 70)
            for movie in movies:
                title = movie[0][:24] if movie[0] else ""
                year = movie[1] if movie[1] else ""
                director = movie[2][:24] if movie[2] else ""
                rating = movie[3] if movie[3] else ""
                print(f"{title:<25} {year:<6} {director:<25} {rating:<6}")
        
        # Commit changes
        connection.commit()
        print(f"\n✅ Database operations completed successfully!")
        
    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        if connection:
            connection.close()
            print("Database connection closed.")
    
    return True

def demonstrate_table_operations():
    """
    Demonstrate various SQL operations on the movies table.
    """
    print("\n" + "="*50)
    print("DEMONSTRATION OF TABLE OPERATIONS")
    print("="*50)
    
    connection = sqlite3.connect('movies.db')
    cursor = connection.cursor()
    
    # Example queries
    examples = [
        ("All movies:", "SELECT title, year FROM movies"),
        ("Movies after 2000:", "SELECT title, year FROM movies WHERE year > 2000"),
        ("Movies by rating (descending):", "SELECT title, imdb_rating FROM movies ORDER BY imdb_rating DESC"),
        ("Count by genre:", "SELECT genre, COUNT(*) FROM movies GROUP BY genre")
    ]
    
    for description, query in examples:
        print(f"\n{description}")
        print("-" * 30)
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                print(f"  {row}")
        except sqlite3.Error as e:
            print(f"  Error: {e}")
    
    connection.close()

if __name__ == "__main__":
    print("SQLite3 Movies Table Script")
    print("=" * 30)
    
    if create_movies_table():
        demonstrate_table_operations()
        
        print(f"\n" + "="*50)
        print("EXAMPLE USAGE IN YOUR CODE:")
        print("="*50)
        print("""
import sqlite3

# Connect to database
connection = sqlite3.connect('movies.db')
cursor = connection.cursor()

# Insert a new movie
cursor.execute('''
    INSERT INTO movies (title, year, genre, director) 
    VALUES (?, ?, ?, ?)
''', ('New Movie', 2024, 'Action', 'New Director'))

# Query movies
cursor.execute('SELECT * FROM movies WHERE year > 2020')
recent_movies = cursor.fetchall()

# Commit and close
connection.commit()
connection.close()
        """)
    else:
        print("Failed to create/access movies table.")