import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client
import time
from urllib.parse import urljoin
from dotenv import load_dotenv
from schema_adapter import insert_legacy_deal  # Import our new adapter

# --- Configuration ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
PAGES_TO_SCRAPE = 5 # Scrape the first 5 pages of the Canary Media archive

# --- Initialize Supabase Client ---
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Successfully connected to Supabase.")
except Exception as e:
    print(f"Error connecting to Supabase: {e}")
    exit()

def scrape_canarymedia_page(page_number):
    """Scrapes a specific page of the Canary Media archive."""
    base_url = 'https://www.canarymedia.com'
    scrape_url = f'{base_url}/articles?page={page_number}'
    
    print(f"Fetching page {page_number}/{PAGES_TO_SCRAPE}: {scrape_url}")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(scrape_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch page {page_number}: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    
    # Look for article links - Canary Media uses various selectors
    article_links = soup.select('a[href*="/articles/"]')
    
    for link_tag in article_links:
        href = link_tag.get('href')
        if href and '/articles/' in href and href not in links:
            full_url = urljoin(base_url, href)
            links.append(full_url)
    
    return links[:20]  # Limit to avoid too many duplicates

def get_article_text(article_url):
    """Fetches and extracts the raw text from a single article."""
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(article_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch article: {e}")
        return None, None

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract company name from title
    title_tag = soup.find('h1') or soup.find('title')
    company_name = title_tag.text.strip() if title_tag else "Unknown Company"
    
    # Extract article text - Canary Media structure
    article_body = (soup.find('div', class_='article-body') or 
                   soup.find('div', class_='post-content') or
                   soup.find('article') or 
                   soup.find('main'))
    
    if article_body:
        # Remove ads, sidebars, etc.
        for unwanted in article_body.find_all(['aside', 'nav', 'header', 'footer']):
            unwanted.decompose()
            
        raw_text = article_body.get_text(strip=True)
        return company_name, raw_text
    
    return company_name, None

def main():
    """Main scraper function using the new schema."""
    print("Starting Canary Media scraper (NEW SCHEMA)...")
    
    all_article_urls = []
    for i in range(1, PAGES_TO_SCRAPE + 1):
        page_urls = scrape_canarymedia_page(i)
        if not page_urls:
            print(f"No more articles found on page {i}. Stopping scrape.")
            break
        all_article_urls.extend(page_urls)
        time.sleep(1)  # Rate limiting

    print(f"\nFound a total of {len(all_article_urls)} article URLs from Canary Media.")
    
    unique_urls = list(set(all_article_urls))
    print(f"Processing {len(unique_urls)} unique URLs...")
    new_articles_found = 0

    for url in unique_urls:
        # Check if we already have this article using new schema
        try:
            # Check new deals table
            existing_new = supabase.table('deals').select('id', count='exact').eq('source_url', url).execute()
            
            # Check old deals table (backup)
            try:
                existing_old = supabase.table('deals_backup').select('id', count='exact').eq('source_url', url).execute()
            except:
                existing_old = type('obj', (object,), {'count': 0})()  # Mock object with count=0
                
        except Exception as e:
            print(f"Error checking existing articles: {e}")
            continue
            
        if existing_new.count > 0 or existing_old.count > 0:
            print(f"  -> Skipping existing article: {url}")
            continue

        new_articles_found += 1
        company_name, raw_text = get_article_text(url)
        
        if raw_text and len(raw_text) > 100:  # Ensure we have substantial content
            print(f"    -> Processing '{company_name}' with new schema...")
            
            # Use our new schema-aware insertion
            success = insert_legacy_deal(
                supabase=supabase,
                company_name=company_name,
                source_url=url,
                raw_text_content=raw_text,
                status='NEW'
            )
            
            if success:
                print(f"    -> ✅ Successfully inserted deal for {company_name}")
            else:
                print(f"    -> ❌ Failed to insert deal for {company_name}")
        else:
            print(f"    -> Skipping article with insufficient content")
            
        time.sleep(0.5)  # Rate limiting
    
    print(f"\n🎉 Canary Media scrape complete! Added {new_articles_found} new articles using NEW SCHEMA.")
    print("These deals will be automatically scored by Alex's investment algorithm!")

if __name__ == "__main__":
    main()
