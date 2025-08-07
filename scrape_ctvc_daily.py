import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client
import time
from urllib.parse import urljoin
from dotenv import load_dotenv

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

def scrape_ctvc_page():
    """Scrapes the first page of the CTVC tag archive."""
    base_url = 'https://www.ctvc.co'
    scrape_url = f'{base_url}/tag/insights/page/1/'
    
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
    main_content = soup.find('div', class_='loop')
    if main_content:
        article_containers = main_content.find_all('article')
        for container in article_containers:
            link_tag = container.find('a')
            if link_tag and 'href' in link_tag.attrs:
                full_url = urljoin(base_url, link_tag['href'])
                links.append(full_url)
    return links

def get_article_text(article_url):
    """Fetches and extracts the raw text from a single article."""
    print(f"  -> Fetching content for: {article_url}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(article_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        return None, None
    article_soup = BeautifulSoup(response.content, 'html.parser')
    title = article_soup.find('h1')
    title_text = title.get_text(strip=True) if title else "No Title Found"
    article_body = article_soup.find('div', class_='article-content') or article_soup.find('div', class_='entry-content')
    if article_body:
        return title_text, article_body.get_text(strip=True, separator='\n')
    return title_text, None

# --- Main Execution ---
if __name__ == "__main__":
    print("Starting daily CTVC scrape...")
    article_urls = scrape_ctvc_page()
    
    if not article_urls:
        print("No articles found.")
    else:
        new_articles_found = 0
        for url in article_urls:
            res = supabase.table('deals').select('id', count='exact').eq('source_url', url).execute()
            if res.count > 0:
                continue

            new_articles_found += 1
            company_name, raw_text = get_article_text(url)
            if raw_text:
                print(f"    -> Inserting '{company_name}' into database...")
                try:
                    supabase.table('deals').insert({
                        'company_name': company_name, 'source_url': url,
                        'raw_text_content': raw_text, 'status': 'NEW'
                    }).execute()
                except Exception as e:
                    print(f"    -> Database insert failed: {e}")
            time.sleep(0.5)
        
        print(f"\nDaily CTVC scrape complete. Added {new_articles_found} new articles.")
