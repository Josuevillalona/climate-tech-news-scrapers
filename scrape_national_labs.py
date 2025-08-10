#!/usr/bin/env python3
"""
National Labs Intelligence Scraper
==================================

Scrapes accessible national laboratory sources for climate tech funding and technology transfer news:
- NREL (National Renewable Energy Laboratory)
- ORNL (Oak Ridge National Laboratory)  
- DOE Newsroom

These sources provide early indicators of government-funded research moving toward commercialization.
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

class NationalLabsIntelligenceScraper:
    """Scraper for national laboratory news and funding announcements."""
    
    def __init__(self):
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
    
    def scrape_nrel_news(self) -> List[Dict]:
        """Scrape NREL news for climate tech developments."""
        discoveries = []
        
        soup = self._make_request("https://www.nrel.gov/news/")
        if not soup:
            return discoveries
            
        try:
            # Find news article links
            article_links = soup.find_all('a', href=re.compile(r'/news/program/|/news/feature/'))
            
            logger.info(f"Found {len(article_links)} NREL article links")
            
            for link in article_links[:10]:  # Process last 10 articles
                article_url = link.get('href')
                if not article_url.startswith('http'):
                    article_url = 'https://www.nrel.gov' + article_url
                
                article_soup = self._make_request(article_url)
                if article_soup:
                    discovery = self._process_nrel_article(article_soup, article_url)
                    if discovery:
                        discoveries.append(discovery)
                        
                time.sleep(1)  # Rate limiting
                
        except Exception as e:
            logger.error(f"Error processing NREL news: {str(e)}")
            
        logger.info(f"Found {len(discoveries)} NREL discoveries")
        return discoveries
    
    def scrape_ornl_news(self) -> List[Dict]:
        """Scrape ORNL news for technology transfer and funding announcements."""
        discoveries = []
        
        soup = self._make_request("https://www.ornl.gov/news")
        if not soup:
            return discoveries
            
        try:
            # Find news article links
            article_selectors = [
                'a[href*="/news/"]',
                '.news-item a',
                '.article-link',
                'article a'
            ]
            
            article_links = set()
            for selector in article_selectors:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href and '/news/' in href:
                        if not href.startswith('http'):
                            href = 'https://www.ornl.gov' + href
                        article_links.add(href)
            
            logger.info(f"Found {len(article_links)} ORNL article links")
            
            for article_url in list(article_links)[:10]:  # Process first 10 articles
                article_soup = self._make_request(article_url)
                if article_soup:
                    discovery = self._process_ornl_article(article_soup, article_url)
                    if discovery:
                        discoveries.append(discovery)
                        
                time.sleep(1)  # Rate limiting
                
        except Exception as e:
            logger.error(f"Error processing ORNL news: {str(e)}")
            
        logger.info(f"Found {len(discoveries)} ORNL discoveries")
        return discoveries
    
    def scrape_doe_newsroom(self) -> List[Dict]:
        """Scrape DOE main newsroom for funding announcements."""
        discoveries = []
        
        soup = self._make_request("https://www.energy.gov/news")
        if not soup:
            return discoveries
            
        try:
            # Find news article links
            article_links = soup.find_all('a', href=re.compile(r'/articles/'))
            
            logger.info(f"Found {len(article_links)} DOE newsroom article links")
            
            for link in article_links[:15]:  # Process first 15 articles
                article_url = link.get('href')
                if not article_url.startswith('http'):
                    article_url = 'https://www.energy.gov' + article_url
                
                # Skip if not funding related based on URL
                if not self._is_funding_related_url(article_url):
                    continue
                
                article_soup = self._make_request(article_url)
                if article_soup:
                    discovery = self._process_doe_article(article_soup, article_url)
                    if discovery:
                        discoveries.append(discovery)
                        
                time.sleep(1)  # Rate limiting
                
        except Exception as e:
            logger.error(f"Error processing DOE newsroom: {str(e)}")
            
        logger.info(f"Found {len(discoveries)} DOE newsroom discoveries")
        return discoveries
    
    def _is_funding_related_url(self, url: str) -> bool:
        """Check if URL likely contains funding information."""
        funding_indicators = [
            'funding', 'award', 'grant', 'million', 'investment',
            'announces', 'selects', 'recipients', 'projects', 'program'
        ]
        url_lower = url.lower()
        return any(indicator in url_lower for indicator in funding_indicators)
    
    def _process_nrel_article(self, soup: BeautifulSoup, url: str) -> Optional[Dict]:
        """Process individual NREL article."""
        return self._process_generic_article(soup, url, 'NREL', 'national_lab_research')
    
    def _process_ornl_article(self, soup: BeautifulSoup, url: str) -> Optional[Dict]:
        """Process individual ORNL article."""
        return self._process_generic_article(soup, url, 'ORNL', 'national_lab_research')
    
    def _process_doe_article(self, soup: BeautifulSoup, url: str) -> Optional[Dict]:
        """Process individual DOE article."""
        return self._process_generic_article(soup, url, 'DOE', 'government_funding')
    
    def _process_generic_article(self, soup: BeautifulSoup, url: str, source: str, source_type: str) -> Optional[Dict]:
        """Generic article processing for government sources."""
        try:
            # Extract title
            title_selectors = ['h1', '.page-title', '.article-title', 'title']
            title = None
            
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    break
            
            if not title:
                title = f"{source} Research Update"
            
            # Extract date
            date_str = None
            date_selectors = [
                '[datetime]',
                'time',
                '.date',
                '.published',
                '.post-date',
                '.article-date'
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
                '.page-content',
                '.entry-content'
            ]
            
            content = ""
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    content = content_elem.get_text(separator=' ', strip=True)
                    break
            
            if not content:
                # Fallback to all text
                content = soup.get_text(separator=' ', strip=True)
            
            # Check relevance
            if not self._is_climate_tech_relevant(title, content):
                return None
            
            # Extract funding information
            funding_amount = self._extract_funding_amount(content)
            companies = self._extract_companies(content)
            technology_focus = self._extract_technology_focus(content)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(
                source, content, funding_amount, companies, technology_focus
            )
            
            discovery = {
                'source': source,
                'source_type': source_type,
                'title': title,
                'url': url,
                'content_preview': content[:500] + "..." if len(content) > 500 else content,
                'funding_amount': funding_amount,
                'companies_mentioned': companies,
                'discovery_date': datetime.now().isoformat(),
                'article_date': date_str,
                'technology_focus': technology_focus,
                'commercialization_stage': 'Research',
                'confidence_score': confidence_score
            }
            
            return discovery
            
        except Exception as e:
            logger.error(f"Error processing {source} article {url}: {str(e)}")
            return None
    
    def _is_climate_tech_relevant(self, title: str, content: str) -> bool:
        """Check if content is climate tech relevant."""
        climate_keywords = [
            'climate', 'energy', 'carbon', 'renewable', 'clean', 'sustainability',
            'solar', 'wind', 'battery', 'storage', 'grid', 'electric', 'hydrogen',
            'biofuel', 'geothermal', 'nuclear', 'efficiency', 'emissions',
            'photovoltaic', 'turbine', 'fuel cell', 'smart grid', 'ev'
        ]
        
        text_to_check = (title + " " + content).lower()
        return any(keyword in text_to_check for keyword in climate_keywords)
    
    def _extract_funding_amount(self, text: str) -> Optional[str]:
        """Extract funding amounts from text."""
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
        """Extract company names from text."""
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
                if 3 < len(company) < 80:  # Reasonable company name length
                    companies.add(company)
        
        return list(companies)
    
    def _extract_technology_focus(self, content: str) -> List[str]:
        """Extract technology focus areas."""
        tech_patterns = {
            'energy_storage': ['battery', 'storage', 'lithium', 'solid state'],
            'renewable_energy': ['solar', 'wind', 'photovoltaic', 'turbine'],
            'carbon_capture': ['carbon capture', 'ccus', 'direct air capture'],
            'hydrogen': ['hydrogen', 'fuel cell', 'electrolysis'],
            'nuclear': ['nuclear', 'reactor', 'fusion', 'fission'],
            'smart_grid': ['grid', 'smart grid', 'transmission'],
            'efficiency': ['efficiency', 'optimization'],
            'transportation': ['electric vehicle', 'ev', 'transportation']
        }
        
        focus_areas = []
        content_lower = content.lower()
        
        for category, keywords in tech_patterns.items():
            if any(keyword in content_lower for keyword in keywords):
                focus_areas.append(category)
                
        return focus_areas
    
    def _calculate_confidence_score(self, source: str, content: str, 
                                  funding_amount: Optional[str], companies: List[str],
                                  technology_focus: List[str]) -> int:
        """Calculate confidence score (0-100)."""
        score = 60  # Base score for national lab sources
        
        # Source credibility bonus
        if source in ['NREL', 'ORNL']:
            score += 15
        elif source == 'DOE':
            score += 10
            
        # Content quality indicators
        if funding_amount:
            score += 10
        if companies:
            score += min(len(companies) * 3, 10)
        if technology_focus:
            score += min(len(technology_focus) * 2, 10)
            
        # Check for strong research indicators
        strong_indicators = [
            'breakthrough', 'innovation', 'patent', 'license', 'commercialize',
            'partnership', 'startup', 'spin-off', 'technology transfer'
        ]
        
        if any(indicator in content.lower() for indicator in strong_indicators):
            score += 5
            
        return min(score, 100)

def main():
    """Main execution function."""
    logger.info("Starting National Labs intelligence gathering...")
    
    scraper = NationalLabsIntelligenceScraper()
    all_discoveries = []
    
    # NREL News
    logger.info("Scraping NREL news...")
    nrel_discoveries = scraper.scrape_nrel_news()
    all_discoveries.extend(nrel_discoveries)
    
    # ORNL News  
    logger.info("Scraping ORNL news...")
    ornl_discoveries = scraper.scrape_ornl_news()
    all_discoveries.extend(ornl_discoveries)
    
    # DOE Newsroom
    logger.info("Scraping DOE newsroom...")
    doe_discoveries = scraper.scrape_doe_newsroom()
    all_discoveries.extend(doe_discoveries)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"national_labs_intelligence_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_discoveries, f, indent=2, ensure_ascii=False)
    
    # Summary
    logger.info(f"National Labs intelligence gathering complete!")
    logger.info(f"Total discoveries: {len(all_discoveries)}")
    logger.info(f"NREL discoveries: {len(nrel_discoveries)}")
    logger.info(f"ORNL discoveries: {len(ornl_discoveries)}")
    logger.info(f"DOE discoveries: {len(doe_discoveries)}")
    logger.info(f"Results saved to: {filename}")
    
    # Print summary
    print(f"\n🏛️ NATIONAL LABS INTELLIGENCE SUMMARY")
    print(f"=" * 50)
    print(f"Total Discoveries: {len(all_discoveries)}")
    print(f"NREL Research: {len(nrel_discoveries)}")
    print(f"ORNL Research: {len(ornl_discoveries)}")
    print(f"DOE Funding: {len(doe_discoveries)}")
    print(f"Results saved: {filename}")
    
    if all_discoveries:
        print(f"\n📋 Recent Climate Tech Discoveries:")
        for i, discovery in enumerate(all_discoveries[:5], 1):
            print(f"{i}. {discovery['title'][:70]}...")
            print(f"   Source: {discovery['source']} | Score: {discovery['confidence_score']}")
            if discovery.get('technology_focus'):
                print(f"   Tech: {', '.join(discovery['technology_focus'][:3])}")
            if discovery.get('funding_amount'):
                print(f"   Funding: {discovery['funding_amount']}")
            print()

if __name__ == "__main__":
    main()
