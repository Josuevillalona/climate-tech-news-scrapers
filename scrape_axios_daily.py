import os
from bs4 import BeautifulSoup
from supabase import create_client, Client
import time
import json
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
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

def scrape_axios_page_with_playwright():
    """Scrapes the first page of Axios Climate Deals using Playwright to bypass blocking."""
    base_url = 'https://www.axios.com'
    scrape_url = f'{base_url}/pro/climate-deals?offset=0'
    
    print(f"Fetching page: {scrape_url}")

    html_content = ""
    with sync_playwright() as p:
        try:
            # Launch browser with more realistic settings to avoid detection
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage'
                ]
            )
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = context.new_page()
            
            # Add stealth settings
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
            """)
            
            page.goto(scrape_url, timeout=60000)
            
            print("Waiting for Cloudflare challenge to complete...")
            # Wait longer for Cloudflare challenge to complete
            page.wait_for_timeout(15000)  # Wait 15 seconds
            
            # Check if we're still on a challenge page
            title = page.title()
            if "Just a moment" in title or "challenge" in title.lower():
                print("Still on challenge page, waiting longer...")
                page.wait_for_timeout(10000)  # Wait another 10 seconds
            
            html_content = page.content()
            
            # Save HTML for debugging
            with open('axios_live_debug.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            print("Live HTML saved to axios_live_debug.html")
            
            browser.close()
        except Exception as e:
            print(f"Playwright failed to fetch page: {e}")
            return []

    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    
    # Check if we successfully got past the challenge
    title = soup.find('title')
    if title and ("Just a moment" in title.text or "challenge" in title.text.lower()):
        print("❌ Still blocked by Cloudflare challenge")
        return []
    
    # Look for JSON-LD structured data
    json_scripts = soup.find_all('script', type='application/ld+json')
    print(f"Found {len(json_scripts)} JSON-LD script tags")
    
    for script in json_scripts:
        try:
            data = json.loads(script.string)
            print(f"JSON data type: {type(data)}")
            if isinstance(data, list):
                print(f"List with {len(data)} items")
                for item in data:
                    if item.get('@type') == 'ItemList' and 'itemListElement' in item:
                        print(f"Found ItemList with {len(item['itemListElement'])} articles")
                        for element in item['itemListElement']:
                            if element.get('@type') == 'NewsArticle' and 'url' in element:
                                links.append(element['url'])
                        break  # Found what we need
            elif data.get('@type') == 'ItemList' and 'itemListElement' in data:
                print(f"Found ItemList with {len(data['itemListElement'])} articles")
                for element in data['itemListElement']:
                    if element.get('@type') == 'NewsArticle' and 'url' in element:
                        links.append(element['url'])
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            continue
    
    # If JSON-LD didn't work, try traditional scraping
    if not links:
        print("JSON-LD method failed, trying traditional scraping...")
        # Try multiple selector strategies
        article_containers = soup.find_all('div', {'data-cy': 'story-card-wrapper'})
        if not article_containers:
            # Try alternative selectors
            article_containers = soup.find_all('article')
            if not article_containers:
                # Try finding any links that look like articles
                all_links = soup.find_all('a', href=True)
                for link in all_links:
                    href = link['href']
                    if '/pro/climate-deals/' in href or 'climate' in href.lower():
                        full_url = urljoin(base_url, href)
                        links.append(full_url)
                return links
        
        for container in article_containers:
            link_tag = container.find('a')
            if link_tag and 'href' in link_tag.attrs:
                full_url = urljoin(base_url, link_tag['href'])
                links.append(full_url)
    
    return links

def get_article_text(article_url):
    """Fetches and extracts the raw text from a single article using Playwright."""
    print(f"  -> Fetching content for: {article_url}")
    with sync_playwright() as p:
        try:
            # Launch browser with stealth settings
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage'
                ]
            )
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = context.new_page()
            
            # Add stealth settings
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
            """)
            
            page.goto(article_url, wait_until='domcontentloaded', timeout=60000)
            
            # Wait for Cloudflare challenge if needed
            page.wait_for_timeout(10000)  # Wait 10 seconds
            
            # Check if we're on a challenge page
            title = page.title()
            if "Just a moment" in title or "challenge" in title.lower():
                print("    -> Waiting for Cloudflare challenge...")
                page.wait_for_timeout(15000)  # Wait another 15 seconds
            
            html_content = page.content()
            browser.close()
        except Exception as e:
            print(f"    -> Playwright failed to fetch article: {e}")
            return None, None
            
    article_soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check if we successfully got past the challenge
    title_tag = article_soup.find('title')
    if title_tag and ("Just a moment" in title_tag.text or "challenge" in title_tag.text.lower()):
        print("    -> Still blocked by Cloudflare, skipping article")
        return None, None
    
    # Extract title
    title_tag = article_soup.find('h1')
    title_text = title_tag.get_text(strip=True) if title_tag else "No Title Found"
    
    # Try multiple content selectors for Axios
    article_body = None
    selectors_to_try = [
        'div[data-cy="story-meta-space"]',
        'div[class*="article-content"]',
        'div[class*="entry-content"]',
        'div[class*="story-body"]',
        'div[class*="content"]',
        'main',
        'article'
    ]
    
    for selector in selectors_to_try:
        article_body = article_soup.select_one(selector)
        if article_body and len(article_body.get_text(strip=True)) > 100:
            break
    
    # Last resort - find any div with substantial content
    if not article_body:
        all_divs = article_soup.find_all('div')
        for div in all_divs:
            text = div.get_text(strip=True)
            if len(text) > 200 and 'climate' in text.lower():  # Look for climate-related content
                article_body = div
                break
    
    if article_body:
        return title_text, article_body.get_text(strip=True, separator='\n')
    else:
        print(f"    -> Could not extract content from {article_url}")
        return title_text, None

# --- Main Execution ---
if __name__ == "__main__":
    print("Starting daily Axios scrape...")
    article_urls = scrape_axios_page_with_playwright()
    
    if not article_urls:
        print("No articles found.")
    else:
        print(f"Found {len(article_urls)} article URLs from Axios.")
        
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
        
        print(f"\nDaily Axios scrape complete. Added {new_articles_found} new articles.")
