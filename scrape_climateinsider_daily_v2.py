import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client
import time
from urllib.parse import urljoin
from dotenv import load_dotenv
from schema_adapter import insert_legacy_deal  # Import our new adapter

# --- Configuration ---
load_dotenv()  # Load variables from .env file
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# --- Initialize Supabase Client ---
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Successfully connected to Supabase.")
except Exception as e:
    print(f"Error connecting to Supabase: {e}")
    exit()

def scrape_climateinsider_page():
    """Scrapes the first page of the Climate Insider exclusives category."""
    base_url = 'https://climateinsider.com'
    scrape_url = f'{base_url}/category/exclusives/page/1/'
    
    print(f"Fetching page: {scrape_url}")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(scrape_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch page: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    article_containers = soup.find_all('article', class_='elementor-post')
    for container in article_containers:
        header = container.find('h3')
        if header and (link_tag := header.find('a')) and 'href' in link_tag.attrs:
            links.append(link_tag['href'])
    return links

def get_article_text(article_url):
    """Fetches and extracts the raw text from a single article."""
    print(f"  -> Fetching content for: {article_url}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(article_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"    -> Failed to fetch article: {e}")
        return None, None

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract title for company name
    title_tag = soup.find('h1') or soup.find('title')
    company_name = title_tag.get_text(strip=True) if title_tag else "Unknown Company"
    
    # Extract article content
    content_selectors = [
        'div.entry-content',
        'div.article-content', 
        'article',
        'div.post-content',
        'div.content',
        'div.elementor-widget-theme-post-content'
    ]
    
    raw_text = ""
    for selector in content_selectors:
        content_div = soup.select_one(selector)
        if content_div:
            # Remove script and style elements
            for script in content_div(['script', 'style']):
                script.decompose()
            raw_text = content_div.get_text(separator=' ', strip=True)
            break
    
    if not raw_text:
        # Fallback: get all text from body
        body = soup.find('body')
        if body:
            for script in body(['script', 'style']):
                script.decompose()
            raw_text = body.get_text(separator=' ', strip=True)
    
    return company_name, raw_text

def main():
    """Main scraper function using the new schema."""
    print("Starting Climate Insider daily scraper (NEW SCHEMA)...")
    
    article_urls = scrape_climateinsider_page()
    if not article_urls:
        print("No articles found. Exiting.")
        return

    print(f"Found {len(article_urls)} articles to process...")
    new_articles_found = 0

    for url in article_urls:
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
    
    print(f"\n🎉 Climate Insider scrape complete! Added {new_articles_found} new articles using NEW SCHEMA.")
    print("These deals will be automatically scored by Alex's investment algorithm!")

if __name__ == "__main__":
    main()
