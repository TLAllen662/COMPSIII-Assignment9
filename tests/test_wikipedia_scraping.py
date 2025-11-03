import sqlite3
import os
from wikipedia_scraping import *
import pytest

@pytest.fixture
def db_connection():
    """Fixture to provide a database connection for tests"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'movies.db')
    connection = sqlite3.connect(db_path)
    yield connection
    connection.close()

# Test that the users table has been created
def test_movies_table_exists(db_connection):
    """Verify that the users table exists in the database."""
    cursor = db_connection.cursor()
    
    # Check if users table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='movies';")
    result = cursor.fetchone()
    assert result is not None, "Movies table does not exist"
    
# Test that the movies table has the correct columns
def test_movies_table_columns(db_connection):
    """Verify the schema of the movies table."""
    cursor = db_connection.cursor()

    # Get table info
    cursor.execute("PRAGMA table_info(movies);")
    columns = cursor.fetchall()
    
    # Expected columns and their types
    # Format: (name, type, notnull, default, primary_key)
    expected_columns = [
        ('id', 'INTEGER', 0, None, 1),      # Primary key
        ('title', 'TEXT', 1, None, 0),      # Not null
        ('worldwide_gross', 'INTEGER', 0, None, 0),
        ('year', 'INTEGER', 0, None, 0)
    ]
    
    # Check number of columns
    assert len(columns) == 4, f"Expected 4 columns, found {len(columns)}"
    
    # Check each column's details
    for expected, actual in zip(expected_columns, columns):
        assert actual[1] == expected[0], f"Column name mismatch: expected {expected[0]}, got {actual[1]}"
        assert actual[2] == expected[1], f"Column type mismatch for {actual[1]}"
        assert actual[5] == expected[4], f"Primary key configuration mismatch for {actual[1]}"

def test_scrape_wikipedia_returns_list():
    """Test that the function returns a list of dictionaries"""
    result = scrape_wikipedia()
    assert isinstance(result, list), "Function should return a list"
    assert len(result) > 0, "Function should return non-empty list"

def test_movie_data_structure():
    """Test that each movie dictionary has the correct keys and value types"""
    result = scrape_wikipedia()
    required_keys = {'title', 'worldwide_gross', 'year'}
    
    for movie in result:
        # Check keys
        assert set(movie.keys()) == required_keys, f"Movie should have exactly these keys: {required_keys}"
        
        # Check value types
        assert isinstance(movie['title'], str), "Title should be a string"
        assert isinstance(movie['worldwide_gross'], int), "Worldwide gross should be an integer"
        assert isinstance(movie['year'], str), "Year should be a string"
        
        # Check non-empty values
        assert len(movie['title']) > 0, "Title should not be empty"
        assert movie['worldwide_gross'] > 0, "Worldwide gross should be positive"
        assert len(movie['year']) == 4, "Year should be 4 characters long"

def test_specific_movies_present():
    """Test that some well-known highest-grossing movies are present"""
    result = scrape_wikipedia()
    titles = [movie['title'] for movie in result]
    
    # Check for some movies that should definitely be in the list since they are near the top
    must_have_movies = [
        'Avatar',
        'Avengers: Endgame',
        'Titanic',
        'The Lion King',
        'Jurassic Park'
    ]
    
    for movie in must_have_movies:
        assert any(movie in title for title in titles), f"{movie} should be in the list"

def test_worldwide_gross_formatting():
    """Test that worldwide gross values are properly cleaned and converted"""
    result = scrape_wikipedia()
    
    for movie in result:
        gross = movie['worldwide_gross']
        assert isinstance(gross, int), "Gross should be converted to integer"
        assert gross > 1_000_000_000, "All movies should have gross > $1 billion"

def test_database_size(db_connection):
    """Verify that the database contains at least 10 of the highest-grossing movies"""
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM movies")
    count = cursor.fetchone()[0]
    assert count > 10, f"Database should contain more than 10 movies, found {count}"