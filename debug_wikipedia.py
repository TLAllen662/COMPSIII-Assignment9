import requests
from bs4 import BeautifulSoup

def debug_wikipedia_page():
    """Debug the Wikipedia page structure to understand the layout."""
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_highest-grossing_films'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print("Fetching Wikipedia page...")
        response = requests.get(url, headers=headers)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all tables
            tables = soup.find_all('table', {'class': 'wikitable'})
            print(f"Found {len(tables)} wikitable(s)")
            
            # Analyze first few tables
            for i, table in enumerate(tables[:3]):
                print(f"\n--- Table {i+1} ---")
                
                # Get table caption if any
                caption = table.find('caption')
                if caption:
                    print(f"Caption: {caption.get_text(strip=True)}")
                
                # Get headers
                header_row = table.find('tr')
                if header_row:
                    headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
                    print(f"Headers: {headers}")
                
                # Get first data row
                data_rows = table.find_all('tr')[1:3]  # First 2 data rows
                for j, row in enumerate(data_rows):
                    cells = row.find_all(['td', 'th'])
                    cell_texts = [cell.get_text(strip=True)[:50] for cell in cells]
                    print(f"Row {j+1}: {cell_texts}")
        else:
            print(f"Failed to fetch page: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_wikipedia_page()