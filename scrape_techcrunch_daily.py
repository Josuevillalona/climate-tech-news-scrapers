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

def scrape_techcrunch_page():
    """Scrapes the first page of the TechCrunch startups category."""
    url = 'https://techcrunch.com/category/startups/page/1/'
    print(f"Fetching page: {url}")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch page: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    article_containers = soup.find_all('li', class_='wp-block-post')
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
    print("Starting daily TechCrunch scrape...")
    article_urls = scrape_techcrunch_page()
    
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
        
        print(f"\nDaily scrape complete. Added {new_articles_found} new articles.")
