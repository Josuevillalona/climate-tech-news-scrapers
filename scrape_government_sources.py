#!/usr/bin/env python3
"""
Government Sources Scraper for Climate Tech Intelligence
========================================================

Scrapes high-value government sources for early-stage climate tech signals:
- ARPA-E funding announcements (2-year commercialization timeline)
- DOE breakthrough technology announcements
- National lab licensing deals and technology transfers

This provides 24-48 hours advantage over mainstream news and 2+ years
early warning for technologies approaching commercial viability.

Author: Climate Tech Intelligence System
Date: August 9, 2025
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime, timedelta
import time
import logging
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GovernmentSourcesTracker:
    """Base class for government source scrapers with common functionality."""
    
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def _make_request(self, url: str, max_retries: int = 3) -> Optional[BeautifulSoup]:
        """Make HTTP request with retry logic and error handling."""
        for attempt in range(max_retries):
            try:
                logger.info(f"Fetching {url} (attempt {attempt + 1})")
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                logger.info(f"Successfully fetched {url}")
                return soup
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    
        logger.error(f"Failed to fetch {url} after {max_retries} attempts")
        return None
    
    def _extract_funding_amount(self, text: str) -> Optional[str]:
        """Extract funding amounts from text using multiple patterns."""
        patterns = [
            r'\$\s*(\d+(?:\.\d+)?)\s*([BMK]?)(?:illion)?',
            r'(\d+(?:\.\d+)?)\s*([BMK]?)(?:illion)?\s*dollars?',
            r'awarded\s+\$\s*(\d+(?:\.\d+)?)\s*([BMK]?)',
            r'funding\s+of\s+\$\s*(\d+(?:\.\d+)?)\s*([BMK]?)',
            r'receives?\s+\$\s*(\d+(?:\.\d+)?)\s*([BMK]?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount = float(match.group(1))
                multiplier = match.group(2).upper() if len(match.groups()) > 1 else ''
                
                if multiplier == 'B':
                    amount *= 1000000000
                elif multiplier == 'M':
                    amount *= 1000000
                elif multiplier == 'K':
                    amount *= 1000
                    
                return f"${amount:,.0f}"
        
        return None
    
    def _extract_companies(self, text: str) -> List[str]:
        """Extract company names from text using common patterns."""
        patterns = [
            r'([A-Z][a-zA-Z\s&,.-]+(?:Inc|LLC|Corp|Corporation|Ltd|Limited|Technologies|Systems|Energy|Solutions)\.?)',
            r'startup\s+([A-Z][a-zA-Z\s&,.-]+)',
            r'company\s+([A-Z][a-zA-Z\s&,.-]+)',
            r'([A-Z][a-zA-Z\s&,.-]+)\s+(?:received|awarded|developed|announced)'
        ]
        
        companies = set()
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                company = match.strip()
                if len(company) > 2 and len(company) < 100:  # Reasonable company name length
                    companies.add(company)
        
        return list(companies)

class ARPAEFundingScraper(GovernmentSourcesTracker):
    """Scraper for ARPA-E funding announcements and awards."""
    
    def __init__(self):
        super().__init__("ARPA-E")
        self.base_url = "https://arpa-e.energy.gov"
        
    def scrape_funding_announcements(self) -> List[Dict]:
        """Scrape ARPA-E funding announcements and awards."""
        discoveries = []
        
        # Try multiple ARPA-E pages for funding information
        urls_to_check = [
            "https://arpa-e.energy.gov/news-and-events/news-and-insights",
            "https://arpa-e.energy.gov/news-and-events/press-releases",
            "https://arpa-e.energy.gov/technologies"  # Technology portfolio
        ]
        
        for url in urls_to_check:
            soup = self._make_request(url)
            if soup:
                page_discoveries = self._process_arpae_page(soup, url)
                discoveries.extend(page_discoveries)
                time.sleep(2)  # Rate limiting
                
        logger.info(f"Found {len(discoveries)} ARPA-E funding discoveries")
        return discoveries
    
    def _process_arpae_page(self, soup: BeautifulSoup, page_url: str) -> List[Dict]:
        """Process ARPA-E page for funding information."""
        discoveries = []
        
        try:
            # Look for article links using various selectors
            article_selectors = [
                'h3 a',  # Based on your finding
                'a[href*="/news/"]',
                'a[href*="/press-releases/"]',
                'a[href*="/technologies/"]',
                '.insights-data a',  # Based on your CSS path
                '.news-item a',
                '.article-link'
            ]
            
            article_links = set()  # Use set to avoid duplicates
            
            for selector in article_selectors:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href:
                        if not href.startswith('http'):
                            href = self.base_url + href
                        article_links.add(href)
            
            logger.info(f"Found {len(article_links)} article links on {page_url}")
            
            # Process each article
            for article_url in list(article_links)[:15]:  # Limit to first 15 articles
                if self._is_funding_related_url(article_url):
                    article_soup = self._make_request(article_url)
                    if article_soup:
                        discovery = self._process_arpae_article(article_soup, article_url)
                        if discovery:
                            discoveries.append(discovery)
                            
                    time.sleep(1)  # Rate limiting
                    
        except Exception as e:
            logger.error(f"Error processing ARPA-E page {page_url}: {str(e)}")
            
        return discoveries
    
    def _is_funding_related_url(self, url: str) -> bool:
        """Check if URL likely contains funding information."""
        funding_indicators = [
            'funding', 'award', 'grant', 'million', 'investment',
            'announces', 'selects', 'recipients', 'projects'
        ]
        url_lower = url.lower()
        return any(indicator in url_lower for indicator in funding_indicators)
    
    def _process_arpae_article(self, soup: BeautifulSoup, url: str) -> Optional[Dict]:
        """Process individual ARPA-E article for funding information."""
        try:
            # Extract title using multiple selectors
            title_selectors = ['h1', 'title', '.page-title', '.article-title']
            title = None
            
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    break
            
            if not title:
                title = "ARPA-E Announcement"
            
            # Extract date using multiple approaches
            date_str = None
            date_selectors = [
                '[datetime]',
                'time',
                '.date',
                '.published',
                '.post-date'
            ]
            
            for selector in date_selectors:
                date_elem = soup.select_one(selector)
                if date_elem:
                    date_str = date_elem.get('datetime') or date_elem.get_text(strip=True)
                    break
            
            # Extract main content
            content_selectors = [
                'main',
                '.content',
                '.article-body',
                '.post-content',
                'article',
                '.page-content'
            ]
            
            content = ""
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    content = content_elem.get_text(separator=' ', strip=True)
                    break
            
            if not content:
                # Fallback to body content
                content = soup.get_text(separator=' ', strip=True)
            
            # Check if this is funding-related
            funding_keywords = [
                'funding', 'award', 'grant', 'million', 'billion', '$',
                'investment', 'recipients', 'selected', 'announces'
            ]
            
            title_lower = title.lower()
            content_lower = content.lower()
            
            is_funding_related = any(
                keyword in title_lower or keyword in content_lower 
                for keyword in funding_keywords
            )
            
            if not is_funding_related:
                return None
            
            # Extract funding amount
            funding_amount = self._extract_funding_amount(content)
            
            # Extract companies
            companies = self._extract_companies(content)
            
            # Check for climate tech relevance
            climate_keywords = [
                'climate', 'energy', 'carbon', 'renewable', 'clean tech', 'sustainability',
                'solar', 'wind', 'battery', 'storage', 'grid', 'electric', 'hydrogen',
                'biofuel', 'geothermal', 'nuclear', 'efficiency', 'emissions'
            ]
            
            climate_relevant = any(
                keyword in title_lower or keyword in content_lower 
                for keyword in climate_keywords
            )
            
            # Only include if climate relevant or has companies mentioned
            if not climate_relevant and not companies:
                return None
                
            discovery = {
                'source': 'ARPA-E',
                'source_type': 'government_funding',
                'title': title,
                'url': url,
                'content_preview': content[:500] + "..." if len(content) > 500 else content,
                'funding_amount': funding_amount,
                'companies_mentioned': companies,
                'discovery_date': datetime.now().isoformat(),
                'article_date': date_str,
                'climate_relevance': climate_relevant,
                'funding_stage': 'Government Grant',
                'technology_focus': self._extract_technology_focus(content),
                'commercialization_timeline': '2-3 years',  # ARPA-E typical timeline
                'confidence_score': self._calculate_confidence_score(content, funding_amount, companies)
            }
            
            return discovery
            
        except Exception as e:
            logger.error(f"Error processing ARPA-E article {url}: {str(e)}")
            return None
    
    def _extract_technology_focus(self, content: str) -> List[str]:
        """Extract technology focus areas from content."""
        tech_patterns = {
            'energy_storage': ['battery', 'storage', 'grid storage', 'lithium', 'solid state'],
            'renewable_energy': ['solar', 'wind', 'photovoltaic', 'turbine', 'renewable'],
            'carbon_capture': ['carbon capture', 'ccus', 'direct air capture', 'carbon removal'],
            'hydrogen': ['hydrogen', 'fuel cell', 'electrolysis', 'green hydrogen'],
            'nuclear': ['nuclear', 'reactor', 'fusion', 'fission', 'nuclear energy'],
            'smart_grid': ['grid', 'smart grid', 'transmission', 'distribution', 'utility'],
            'efficiency': ['efficiency', 'optimization', 'performance improvement'],
            'transportation': ['electric vehicle', 'ev', 'transportation', 'mobility']
        }
        
        focus_areas = []
        content_lower = content.lower()
        
        for category, keywords in tech_patterns.items():
            if any(keyword in content_lower for keyword in keywords):
                focus_areas.append(category)
                
        return focus_areas
    
    def _calculate_confidence_score(self, content: str, funding_amount: Optional[str], companies: List[str]) -> int:
        """Calculate confidence score for the discovery (0-100)."""
        score = 70  # Base score for ARPA-E source
        
        # Boost for funding amount
        if funding_amount:
            score += 15
            
        # Boost for company mentions
        if companies:
            score += min(len(companies) * 5, 15)
            
        # Check for strong indicators
        strong_indicators = ['breakthrough', 'innovative', 'novel', 'first-of-its-kind', 'revolutionary']
        if any(indicator in content.lower() for indicator in strong_indicators):
            score += 10
            
        return min(score, 100)

class DOETechTransferScraper(GovernmentSourcesTracker):
    """Scraper for DOE technology transfer and licensing announcements."""
    
    def __init__(self):
        super().__init__("DOE-TechTransfer")
        
    def scrape_tech_transfers(self) -> List[Dict]:
        """Scrape DOE technology transfer announcements."""
        discoveries = []
        
        # DOE Office of Technology Transitions
        urls_to_check = [
            "https://www.energy.gov/technologytransitions/office-technology-transitions",
            "https://www.energy.gov/articles",  # General DOE news
        ]
        
        for url in urls_to_check:
            soup = self._make_request(url)
            if soup:
                page_discoveries = self._process_doe_page(soup, url)
                discoveries.extend(page_discoveries)
                time.sleep(2)
                
        logger.info(f"Found {len(discoveries)} DOE tech transfer discoveries")
        return discoveries
    
    def _process_doe_page(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Process DOE page for technology transfer announcements."""
        discoveries = []
        
        try:
            # Look for news articles or announcements
            article_links = soup.find_all('a', href=re.compile(r'/articles/|/news/'))
            
            for link in article_links[:5]:  # Process recent articles
                article_url = link.get('href')
                if not article_url.startswith('http'):
                    article_url = "https://www.energy.gov" + article_url
                    
                article_soup = self._make_request(article_url)
                if article_soup:
                    discovery = self._process_doe_article(article_soup, article_url)
                    if discovery:
                        discoveries.append(discovery)
                        
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"Error processing DOE page {base_url}: {str(e)}")
            
        return discoveries
    
    def _process_doe_article(self, soup: BeautifulSoup, url: str) -> Optional[Dict]:
        """Process individual DOE article for tech transfer information."""
        try:
            title_elem = soup.find('h1') or soup.find('title')
            title = title_elem.get_text(strip=True) if title_elem else "DOE Technology Announcement"
            
            content_elem = soup.find('div', class_=re.compile(r'content|body|article'))
            content = content_elem.get_text(separator=' ', strip=True) if content_elem else ""
            
            # Check for tech transfer relevance
            tech_transfer_keywords = [
                'license', 'licensing', 'technology transfer', 'commercialize', 
                'startup', 'spin-off', 'partnership', 'private sector'
            ]
            
            if not any(keyword in content.lower() for keyword in tech_transfer_keywords):
                return None
                
            companies = self._extract_companies(content)
            
            discovery = {
                'source': 'DOE Technology Transfer',
                'source_type': 'government_tech_transfer',
                'title': title,
                'url': url,
                'content_preview': content[:500] + "..." if len(content) > 500 else content,
                'companies_mentioned': companies,
                'discovery_date': datetime.now().isoformat(),
                'technology_focus': self._extract_technology_focus(content),
                'commercialization_stage': 'Technology Transfer',
                'confidence_score': 75
            }
            
            return discovery
            
        except Exception as e:
            logger.error(f"Error processing DOE article {url}: {str(e)}")
            return None

def main():
    """Main execution function for government sources scraping."""
    logger.info("Starting government sources intelligence gathering...")
    
    all_discoveries = []
    
    # ARPA-E Funding Scraper
    logger.info("Scraping ARPA-E funding announcements...")
    arpae_scraper = ARPAEFundingScraper()
    arpae_discoveries = arpae_scraper.scrape_funding_announcements()
    all_discoveries.extend(arpae_discoveries)
    
    # DOE Tech Transfer Scraper
    logger.info("Scraping DOE technology transfers...")
    doe_scraper = DOETechTransferScraper()
    doe_discoveries = doe_scraper.scrape_tech_transfers()
    all_discoveries.extend(doe_discoveries)
    
    # Save discoveries to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"government_discoveries_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_discoveries, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Government intelligence gathering complete!")
    logger.info(f"Total discoveries: {len(all_discoveries)}")
    logger.info(f"ARPA-E discoveries: {len(arpae_discoveries)}")
    logger.info(f"DOE discoveries: {len(doe_discoveries)}")
    logger.info(f"Results saved to: {filename}")
    
    # Print summary
    print(f"\n🏛️ GOVERNMENT INTELLIGENCE SUMMARY")
    print(f"=" * 50)
    print(f"Total Discoveries: {len(all_discoveries)}")
    print(f"ARPA-E Funding: {len(arpae_discoveries)}")
    print(f"DOE Tech Transfer: {len(doe_discoveries)}")
    print(f"Results saved: {filename}")
    
    if all_discoveries:
        print(f"\n📋 Recent Discoveries:")
        for i, discovery in enumerate(all_discoveries[:3], 1):
            print(f"{i}. {discovery['title'][:80]}...")
            print(f"   Source: {discovery['source']}")
            if discovery.get('companies_mentioned'):
                print(f"   Companies: {', '.join(discovery['companies_mentioned'][:3])}")
            print()

if __name__ == "__main__":
    main()
