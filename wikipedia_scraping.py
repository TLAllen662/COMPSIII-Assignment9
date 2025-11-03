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
    """
    Scrape Wikipedia for highest-grossing movies data.
    
    Uses requests and BeautifulSoup to:
    1. Visit the Highest Grossing Films page
    2. Grab the table element with class 'wikitable'
    3. Find all tr elements from the table
    4. Iterate through rows and extract data from td/th elements
    5. Clean worldwide gross values (remove $, commas, T, F, F8)
    6. Return list of dictionaries with movie data
    """
    try:
        # Use requests to visit the Highest Grossing Films page
        url = 'https://en.wikipedia.org/wiki/List_of_highest-grossing_films'
        
        # Add headers to avoid 403 Forbidden error
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Grab the table element that has a class of 'wikitable'
        table = soup.find('table', {'class': 'wikitable'})
        
        if not table:
            print("Could not find table with class 'wikitable'")
            return []
        
        # From the table element find all instances of the tr element
        tr_elements = table.find_all('tr')
        print(f"Found {len(tr_elements)} tr elements in the table")
        
        movies = []
        
        # From the elements that were returned, iterate through the list
        for i, row in enumerate(tr_elements[1:], 1):  # Skip header row
            # Get the data for each row - find td and th elements
            cells = row.find_all(['td', 'th'])
            
            if len(cells) >= 5:  # Ensure we have enough columns
                try:
                    # Extract data from each cell
                    # Expected format: Rank, Peak, Title, Worldwide gross, Year, Ref
                    
                    # Rank (1st column - index 0)
                    rank_cell = cells[0]
                    rank = rank_cell.get_text(strip=True)
                    
                    # Peak (2nd column - index 1) 
                    peak_cell = cells[1]
                    peak = peak_cell.get_text(strip=True)
                    
                    # Title (3rd column - index 2)
                    title_cell = cells[2]
                    # Get text from link if available, otherwise get cell text
                    title_link = title_cell.find('a')
                    if title_link:
                        title = title_link.get_text(strip=True)
                    else:
                        title = title_cell.get_text(strip=True)
                    
                    # Remove footnote markers like [1], [2], etc.
                    title = re.sub(r'\[[^\]]*\]', '', title).strip()
                    
                    # Worldwide gross (4th column - index 3)
                    gross_cell = cells[3]
                    gross_text = gross_cell.get_text(strip=True)
                    
                    # Clean worldwide gross: remove "$", ",", "T", "F", "F8", and other characters
                    # Keep only digits
                    gross_cleaned = re.sub(r'[^\d]', '', gross_text)
                    
                    # Convert to integer if we have valid digits
                    if gross_cleaned and len(gross_cleaned) >= 9:  # At least 9 digits for billion+
                        worldwide_gross = int(gross_cleaned)
                    else:
                        continue  # Skip if gross is too small or invalid
                    
                    # Year (5th column - index 4)
                    year_cell = cells[4]
                    year_text = year_cell.get_text(strip=True)
                    # Extract 4-digit year
                    year_match = re.search(r'\b(19|20)\d{2}\b', year_text)
                    year = year_match.group() if year_match else "2023"
                    
                    # Only include movies with significant box office (1 billion+)
                    if title and worldwide_gross > 1_000_000_000:
                        # Create dictionary in the required format
                        movie_dict = {
                            'title': title,
                            'worldwide_gross': worldwide_gross,
                            'year': year
                        }
                        
                        movies.append(movie_dict)
                        print(f"Row {i}: Added {title} ({year}) - ${worldwide_gross:,}")
                        
                except (ValueError, AttributeError, IndexError) as e:
                    print(f"Error processing row {i}: {e}")
                    continue
            else:
                print(f"Row {i}: Insufficient columns ({len(cells)} found, need at least 5)")
        
        print(f"Successfully scraped {len(movies)} movies")
        return movies
        
    except requests.RequestException as e:
        print(f"Error fetching data from Wikipedia: {e}")
        return []
    except Exception as e:
        print(f"Error parsing Wikipedia data: {e}")
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



