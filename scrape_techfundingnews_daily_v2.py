import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client
import time
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from schema_adapter import insert_legacy_deal  # Import our new adapter

# --- Configuration ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# --- How many times to click the "Load More" button ---
LOAD_MORE_CLICKS = 3 

# --- Initialize Supabase Client ---
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Successfully connected to Supabase.")
except Exception as e:
    print(f"Error connecting to Supabase: {e}")
    exit()

def scrape_techfundingnews_with_playwright():
    """Scrapes Tech Funding News by clicking the 'Load More' button."""
    base_url = 'https://techfundingnews.com'
    scrape_url = f'{base_url}/category/climate-tech/'
    
    print(f"Fetching page: {scrape_url}")

    html_content = ""
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(scrape_url, wait_until='domcontentloaded', timeout=60000)
            
            # Handle the cookie consent banner before doing anything else.
            print("Page loaded. Checking for cookie consent banner...")
            try:
                cookie_button = page.locator('button:has-text("ACCEPT")')
                if cookie_button.is_visible(timeout=5000):
                    print("  -> Cookie banner found. Clicking 'ACCEPT'.")
                    cookie_button.click()
                    page.wait_for_timeout(2000)
                else:
                    print("  -> No cookie banner found.")
            except Exception as e:
                print(f"  -> Could not click cookie button (it may not exist): {e}")

            print("Clicking 'Load More' button...")
            for i in range(LOAD_MORE_CLICKS):
                print(f"  -> Click {i + 1}/{LOAD_MORE_CLICKS}")
                load_more_button = page.locator('#primary > div.cs-posts-area.cs-posts-area-posts > div.cs-posts-area__pagination > button')
                if load_more_button.is_visible():
                    load_more_button.click()
                    page.wait_for_timeout(3000) 
                else:
                    print("  -> 'Load More' button not found. Stopping.")
                    break
            
            print("Finished clicking. Extracting HTML.")
            html_content = page.content()
            browser.close()
        except Exception as e:
            print(f"Playwright failed to fetch page: {e}")
            return []

    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    
    # Based on your selector, find all article headlines
    article_headers = soup.select('h2.cs-entry__title a')
    for link_tag in article_headers:
        if 'href' in link_tag.attrs:
            links.append(link_tag['href'])
    
    return links

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
    title_tag = soup.find('h1')
    company_name = title_tag.text.strip() if title_tag else "Unknown Company"
    
    # Extract article text
    article_body = soup.find('div', class_='entry-content') or soup.find('article')
    if article_body:
        raw_text = article_body.get_text(strip=True)
        return company_name, raw_text
    
    return company_name, None

def main():
    """Main scraper function using the new schema."""
    print("Starting Tech Funding News scraper (NEW SCHEMA)...")
    
    all_article_urls = scrape_techfundingnews_with_playwright()

    print(f"\nFound a total of {len(all_article_urls)} article URLs from Tech Funding News.")
    
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
    
    print(f"\n🎉 Tech Funding News scrape complete! Added {new_articles_found} new articles using NEW SCHEMA.")
    print("These deals will be automatically scored by Alex's investment algorithm!")

if __name__ == "__main__":
    main()
