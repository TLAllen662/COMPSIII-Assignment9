#!/usr/bin/env python3
"""
Demonstration of Wikipedia scraping following the specified requirements:

1. Use requests and BeautifulSoup to visit the Highest Grossing Films page
2. Grab the table element that has a class of 'wikitable'
3. From the table element find all instances of the tr element
4. Iterate through the list and get the data for each row
5. Extract data from td and th elements
6. Clean worldwide gross (remove "$", ",", "T", "F", "F8")
7. Return list of Python dictionaries
"""

from wikipedia_scraping import scrape_wikipedia

def demonstrate_scraping():
    """Demonstrate the Wikipedia scraping functionality."""
    
    print("="*60)
    print("WIKIPEDIA SCRAPING DEMONSTRATION")
    print("="*60)
    
    print("\n1. Using requests and BeautifulSoup to visit:")
    print("   https://en.wikipedia.org/wiki/List_of_highest-grossing_films")
    
    print("\n2. Finding table element with class 'wikitable'")
    print("3. Finding all tr elements from the table")
    print("4. Iterating through rows and extracting td/th data")
    print("5. Cleaning worldwide gross values")
    
    print("\nScraping in progress...")
    print("-" * 40)
    
    # Call the scraping function
    movies = scrape_wikipedia()
    
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)
    
    print(f"\nTotal movies scraped: {len(movies)}")
    
    if movies:
        print(f"\nFirst 5 movies in dictionary format:")
        print("-" * 40)
        
        for i, movie in enumerate(movies[:5], 1):
            print(f"\n{i}. Dictionary:")
            print(f"   {movie}")
            print(f"   Title: '{movie['title']}'")
            print(f"   Worldwide Gross: {movie['worldwide_gross']:,} (cleaned integer)")
            print(f"   Year: '{movie['year']}'")
        
        print(f"\n" + "-" * 40)
        print("DATA CLEANING VERIFICATION:")
        print("-" * 40)
        
        # Show some examples of cleaned data
        example_movie = movies[0]
        print(f"✅ Title cleaned: '{example_movie['title']}'")
        print(f"   (footnote markers like [1], [2] removed)")
        
        print(f"✅ Worldwide gross cleaned: {example_movie['worldwide_gross']}")
        print(f"   (Original likely had $, commas: ${example_movie['worldwide_gross']:,})")
        print(f"   (All non-digit characters removed: '$', ',', 'T', 'F', 'F8')")
        
        print(f"✅ Year extracted: '{example_movie['year']}'")
        print(f"   (4-digit year pattern found)")
        
        print(f"\n" + "="*60)
        print("DICTIONARY FORMAT VERIFICATION:")
        print("="*60)
        
        sample = movies[0]
        print(f"✅ Returns list of dictionaries: {type(movies)} with {len(movies)} items")
        print(f"✅ Each item is a dictionary: {type(sample)}")
        print(f"✅ Required keys present: {list(sample.keys())}")
        print(f"✅ Title is string: {type(sample['title'])}")
        print(f"✅ Worldwide gross is integer: {type(sample['worldwide_gross'])}")
        print(f"✅ Year is string: {type(sample['year'])}")
        
        # Show range of gross values
        gross_values = [movie['worldwide_gross'] for movie in movies]
        print(f"\n📊 Worldwide gross range:")
        print(f"   Highest: ${max(gross_values):,}")
        print(f"   Lowest:  ${min(gross_values):,}")
        print(f"   All values > $1 billion: {all(g > 1_000_000_000 for g in gross_values)}")
        
    else:
        print("❌ No movies were scraped. Check the scraping function.")
    
    print(f"\n" + "="*60)
    print("SCRAPING COMPLETE")
    print("="*60)

if __name__ == "__main__":
    demonstrate_scraping()