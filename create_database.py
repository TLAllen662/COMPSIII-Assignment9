import sqlite3

def create_movies_database():
    """Create a SQLite database file named movies.db with a movies table."""
    
    # Create/connect to the database file
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    
    # Create a movies table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER,
            genre TEXT,
            director TEXT,
            rating REAL,
            description TEXT
        )
    ''')
    
    # You can also create additional tables if needed
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS actors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            birth_year INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movie_actors (
            movie_id INTEGER,
            actor_id INTEGER,
            FOREIGN KEY (movie_id) REFERENCES movies (id),
            FOREIGN KEY (actor_id) REFERENCES actors (id),
            PRIMARY KEY (movie_id, actor_id)
        )
    ''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database 'movies.db' created successfully with tables!")
    print("Tables created:")
    print("- movies: for storing movie information")
    print("- actors: for storing actor information") 
    print("- movie_actors: for linking movies to actors")

if __name__ == "__main__":
    create_movies_database()