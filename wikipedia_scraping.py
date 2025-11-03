import sqlite3
import requests
from bs4 import BeautifulSoup
import re

def create_movies_table():
    """Create the movies table in the database."""
    connection = sqlite3.connect('movies.db')
    cursor = connection.cursor()
    
    # Create table to match test expectations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            worldwide_gross INTEGER,
            year INTEGER
        )
    ''')
    
    connection.commit()
    connection.close()
    print("Movies table created successfully!")

def scrape_wikipedia():
    """Scrape Wikipedia for highest-grossing movies data."""
    try:
        # Request wikipedia page for highest-grossing films
        url = 'https://en.wikipedia.org/wiki/List_of_highest-grossing_films'
        
        # Add headers to avoid 403 Forbidden error
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table with highest-grossing movies
        # Look for the first table that contains movie data
        tables = soup.find_all('table', {'class': 'wikitable'})
        table = None
        
        for t in tables:
            # Check if this table has the right headers
            headers_row = t.find('tr')
            if headers_row and ('worldwide' in headers_row.get_text().lower() or 'gross' in headers_row.get_text().lower()):
                table = t
                break
        
        if not table:
            print("Could not find movies table")
            return []
        
        movies = []
        rows = table.find_all('tr')[1:]  # Skip header row
        
        for row in rows[:50]:  # Get top 50 movies
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 3:
                try:
                    # Extract title (usually in 2nd column, sometimes 1st)
                    title_cell = cells[1] if len(cells) > 2 else cells[0]
                    
                    # Clean title text
                    title_link = title_cell.find('a')
                    if title_link:
                        title = title_link.get_text(strip=True)
                    else:
                        title = title_cell.get_text(strip=True)
                    
                    # Remove footnote markers and extra text
                    title = re.sub(r'\[[^\]]*\]', '', title)
                    title = title.strip()
                    
                    # Extract worldwide gross (usually in 3rd column, sometimes 2nd)
                    gross_cell = cells[2] if len(cells) > 2 else cells[1]
                    gross_text = gross_cell.get_text(strip=True)
                    
                    # Clean and convert gross to integer (remove $, commas, etc.)
                    gross_clean = re.sub(r'[^\d]', '', gross_text)
                    if gross_clean and len(gross_clean) >= 9:  # At least 9 digits for billion+
                        worldwide_gross = int(gross_clean)
                    else:
                        continue
                    
                    # Extract year (usually in 4th column, sometimes 3rd)
                    year_cell = cells[3] if len(cells) > 3 else cells[2] if len(cells) > 2 else cells[1]
                    year_text = year_cell.get_text(strip=True)
                    year_match = re.search(r'\b(19|20)\d{2}\b', year_text)
                    year = year_match.group() if year_match else "2023"
                    
                    if title and worldwide_gross > 1_000_000_000:  # Only billion+ movies
                        movies.append({
                            'title': title,
                            'worldwide_gross': worldwide_gross,
                            'year': year
                        })
                        
                except (ValueError, AttributeError) as e:
                    continue
        
        print(f"Successfully scraped {len(movies)} movies")
        return movies
        
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
    except Exception as e:
        print(f"Error parsing data: {e}")
        return []

def save_to_database(movies):
    """Save movies data to the database."""
    connection = sqlite3.connect('movies.db')
    cursor = connection.cursor()
    
    for movie in movies:
        cursor.execute('''
            INSERT OR REPLACE INTO movies (title, worldwide_gross, year)
            VALUES (?, ?, ?)
        ''', (movie['title'], movie['worldwide_gross'], int(movie['year'])))
    
    connection.commit()
    connection.close()
    print(f"Saved {len(movies)} movies to database")

def main():
    """Main function to run the scraping and database operations."""
    print("Starting Wikipedia movie scraping...")
    
    # Create table
    create_movies_table()
    
    # Scrape data
    movies = scrape_wikipedia()
    print(f"Scraped {len(movies)} movies")
    
    # Save to database
    if movies:
        save_to_database(movies)
    else:
        print("No movies data to save")

if __name__ == "__main__":
    main()



