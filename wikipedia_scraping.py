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
        
        # Find the first table with caption "Highest-grossing films"
        tables = soup.find_all('table', {'class': 'wikitable'})
        table = None
        
        for t in tables:
            caption = t.find('caption')
            if caption and 'highest-grossing films' in caption.get_text().lower():
                table = t
                break
        
        if not table:
            print("Could not find highest-grossing films table")
            return []
        
        movies = []
        rows = table.find_all('tr')[1:]  # Skip header row
        
        print(f"Processing {len(rows)} rows from Wikipedia table...")
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 5:  # Rank, Peak, Title, Worldwide gross, Year, Ref
                try:
                    # Extract title (3rd column - index 2)
                    title_cell = cells[2]
                    title_link = title_cell.find('a')
                    if title_link:
                        title = title_link.get_text(strip=True)
                    else:
                        title = title_cell.get_text(strip=True)
                    
                    # Remove footnote markers
                    title = re.sub(r'\[[^\]]*\]', '', title).strip()
                    
                    # Extract worldwide gross (4th column - index 3)
                    gross_cell = cells[3]
                    gross_text = gross_cell.get_text(strip=True)
                    
                    # Clean and convert gross to integer (remove $, commas, etc.)
                    # Handle format like "$2,923,710,708"
                    gross_clean = re.sub(r'[^\d]', '', gross_text)
                    if gross_clean and len(gross_clean) >= 9:  # At least 9 digits for billion+
                        worldwide_gross = int(gross_clean)
                    else:
                        continue
                    
                    # Extract year (5th column - index 4)
                    year_cell = cells[4]
                    year_text = year_cell.get_text(strip=True)
                    year_match = re.search(r'\b(19|20)\d{2}\b', year_text)
                    year = year_match.group() if year_match else "2023"
                    
                    if title and worldwide_gross > 1_000_000_000:  # Only billion+ movies
                        movies.append({
                            'title': title,
                            'worldwide_gross': worldwide_gross,
                            'year': year
                        })
                        print(f"Added: {title} ({year}) - ${worldwide_gross:,}")
                        
                except (ValueError, AttributeError, IndexError) as e:
                    print(f"Error processing row: {e}")
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



