#!/usr/bin/env python3
"""
VC Portfolio Monitoring System - Phase 2A
=========================================

Monitors top climate tech VC firm portfolios for:
1. New portfolio company additions
2. Follow-on funding rounds
3. Co-investment pattern analysis
4. Portfolio company intelligence

Target VC Firms:
- Breakthrough Energy Ventures (Bill Gates)
- Energy Impact Partners
- Congruent Ventures  
- Generate2
- DCVC
- Prelude Ventures

Author: Climate Tech VC Pipeline
Date: August 9, 2025
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import logging
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
import os
from supabase import create_client, Client
from schema_adapter import SchemaAwareDealInserter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vc_portfolio_scraper.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class PortfolioCompany:
    """Data structure for portfolio company information"""
    name: str
    website: str
    description: str
    sector: str
    funding_stage: Optional[str] = None
    last_funding_date: Optional[str] = None
    last_funding_amount: Optional[str] = None
    headquarters: Optional[str] = None
    founding_year: Optional[int] = None
    vc_firm: str = ""
    portfolio_url: str = ""
    confidence_score: float = 0.7

class VCPortfolioScraper:
    """Base class for VC portfolio monitoring"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Initialize Supabase connection
        self.supabase = self._init_supabase()
        self.deal_inserter = SchemaAwareDealInserter(self.supabase) if self.supabase else None
        
        # Track discovered companies
        self.discovered_companies: List[PortfolioCompany] = []
        self.existing_companies = set()
        
    def _init_supabase(self) -> Optional[Client]:
        """Initialize Supabase client"""
        try:
            url = os.getenv('SUPABASE_URL')
            key = os.getenv('SUPABASE_KEY')
            
            if not url or not key:
                logger.warning("Supabase credentials not found in environment variables")
                return None
                
            return create_client(url, key)
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            return None
    
    def _load_existing_companies(self) -> None:
        """Load existing companies from database to avoid duplicates"""
        if not self.supabase:
            return
            
        try:
            response = self.supabase.table('companies').select('name, website').execute()
            for company in response.data:
                self.existing_companies.add(company['name'].lower().strip())
                if company.get('website'):
                    self.existing_companies.add(company['website'].lower().strip())
        except Exception as e:
            logger.error(f"Error loading existing companies: {e}")
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        return re.sub(r'\s+', ' ', text.strip())
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            return urlparse(url).netloc.lower().replace('www.', '')
        except:
            return ""
    
    def _is_climate_related(self, description: str, sectors: List[str] = None) -> bool:
        """Determine if company is climate tech related"""
        climate_keywords = [
            'climate', 'carbon', 'renewable', 'solar', 'wind', 'energy storage',
            'battery', 'ev', 'electric vehicle', 'clean energy', 'green',
            'sustainability', 'decarbonization', 'emissions', 'net zero',
            'hydrogen', 'geothermal', 'hydroelectric', 'biofuel', 'cleantech',
            'buildings', 'manufacturing', 'agriculture', 'metal', 'materials'
        ]
        
        # For Breakthrough Energy companies, assume all are climate tech
        # since it's a dedicated climate VC fund
        if "Breakthrough Energy" in (description or ""):
            return True
        
        text_to_check = (description or "").lower()
        if sectors:
            text_to_check += " " + " ".join(sectors).lower()
            
        is_climate = any(keyword in text_to_check for keyword in climate_keywords)
        logger.debug(f"Climate check: '{description[:50]}' -> {is_climate}")
        
        return is_climate
    
    def save_to_database(self, company: PortfolioCompany) -> bool:
        """Save portfolio company to database using schema adapter"""
        if not self.deal_inserter:
            logger.warning("No database connection - saving to JSON instead")
            return self._save_to_json(company)
        
        try:
            # Create synthetic deal announcement for portfolio company
            deal_content = f"""
            Portfolio Company: {company.name}
            VC Firm: {company.vc_firm}
            Description: {company.description}
            Sector: {company.sector}
            Headquarters: {company.headquarters or 'Unknown'}
            Website: {company.website}
            
            Source: VC Portfolio Monitoring
            """
            
            # Insert as a "portfolio_discovery" type deal
            deal_id = self.deal_inserter.insert_deal(
                company_name=company.name,
                source_url=company.portfolio_url,
                raw_text_content=deal_content,
                source_type='vc_portfolio',
                source_name=company.vc_firm,
                detected_funding_stage=company.funding_stage,
                detected_amount=company.last_funding_amount,
                detected_investors=[company.vc_firm] if company.vc_firm else None,
                detected_sector=company.sector,
                detected_country=self._extract_country(company.headquarters),
                has_ai_focus=self._has_ai_focus(company.description)
            )
            
            if deal_id:
                logger.info(f"Saved {company.name} to database (Deal ID: {deal_id[:8]}...)")
                return True
            else:
                logger.error(f"Failed to save {company.name} to database")
                return False
                
        except Exception as e:
            logger.error(f"Error saving {company.name} to database: {e}")
            return False
    
    def _extract_country(self, headquarters: str) -> Optional[str]:
        """Extract country from headquarters string"""
        if not headquarters:
            return None
            
        # Simple country extraction - can be enhanced
        headquarters = headquarters.lower()
        if any(term in headquarters for term in ['usa', 'united states', 'california', 'new york', 'texas']):
            return 'United States'
        elif 'canada' in headquarters:
            return 'Canada'
        elif any(term in headquarters for term in ['uk', 'united kingdom', 'london']):
            return 'United Kingdom'
        elif 'germany' in headquarters:
            return 'Germany'
        elif 'france' in headquarters:
            return 'France'
        
        return None
    
    def _has_ai_focus(self, description: str) -> bool:
        """Determine if company has AI focus"""
        if not description:
            return False
            
        ai_keywords = [
            'ai', 'artificial intelligence', 'machine learning', 'ml',
            'deep learning', 'neural network', 'computer vision',
            'nlp', 'natural language', 'algorithm', 'automation'
        ]
        
        description = description.lower()
        return any(keyword in description for keyword in ai_keywords)
    
    def _save_to_json(self, company: PortfolioCompany) -> bool:
        """Fallback: Save to JSON file if database unavailable"""
        try:
            filename = f"vc_portfolio_discoveries_{datetime.now().strftime('%Y%m%d')}.json"
            
            # Load existing data
            data = []
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    data = json.load(f)
            
            # Add new company
            data.append({
                'name': company.name,
                'website': company.website,
                'description': company.description,
                'sector': company.sector,
                'vc_firm': company.vc_firm,
                'headquarters': company.headquarters,
                'funding_stage': company.funding_stage,
                'discovered_at': datetime.now().isoformat(),
                'confidence_score': company.confidence_score
            })
            
            # Save updated data
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved {company.name} to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")
            return False
    
    def _is_new_company(self, company: PortfolioCompany) -> bool:
        """Check if company is new (not in existing database)"""
        name_check = company.name.lower().strip() not in self.existing_companies
        website_check = True
        
        if company.website:
            domain = self._extract_domain(company.website)
            website_check = domain not in self.existing_companies
        
        return name_check and website_check
    
    def _filter_new_companies(self, companies: List[PortfolioCompany]) -> List[PortfolioCompany]:
        """Filter out companies that already exist in our database"""
        return [company for company in companies if self._is_new_company(company)]

class EnergyImpactPartnersScraper(VCPortfolioScraper):
    """Scraper for Energy Impact Partners portfolio"""
    
    def __init__(self):
        super().__init__()
        self.vc_name = "Energy Impact Partners"
        self.base_url = "https://www.energyimpactpartners.com/_portfolio/"
        
        # Update session headers for EIP (they require proper headers)
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
    
    def scrape_portfolio(self) -> List[PortfolioCompany]:
        """Scrape Energy Impact Partners portfolio (single page)"""
        logger.info(f"Starting {self.vc_name} portfolio scrape...")
        
        self._load_existing_companies()
        
        try:
            logger.info(f"Scraping: {self.base_url}")
            
            response = self.session.get(self.base_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract companies from the page
            companies = self._extract_companies(soup)
            
            if not companies:
                logger.warning(f"No companies found on {self.vc_name} portfolio")
                return []
            
            logger.info(f"Found {len(companies)} companies from {self.vc_name}")
            
            # Filter out companies we already have
            new_companies = self._filter_new_companies(companies)
            logger.info(f"New companies to process: {len(new_companies)}")
            
            if new_companies:
                # Show first few companies found
                for i, company in enumerate(new_companies[:5], 1):
                    logger.info(f"Company {i}: {company.name} - {company.description[:50]}...")
            
            return new_companies
            
        except Exception as e:
            logger.error(f"Error scraping {self.vc_name} portfolio: {e}")
            return []
    
    def _extract_companies(self, soup: BeautifulSoup) -> List[PortfolioCompany]:
        """Extract companies from EIP portfolio page"""
        companies = []
        
        # EIP uses .portfolio-item class for each company
        portfolio_items = soup.select('.portfolio-item')
        
        logger.info(f"Found {len(portfolio_items)} company elements (.portfolio-item)")
        
        for item in portfolio_items:
            try:
                company = self._extract_company_from_element(item)
                if company and company.name and len(company.name) > 1:
                    companies.append(company)
                    logger.debug(f"Successfully extracted: {company.name}")
                else:
                    logger.debug(f"Failed extraction or invalid company")
            except Exception as e:
                logger.warning(f"Error extracting company: {e}")
                continue
        
        return companies
    
    def _extract_company_from_element(self, element) -> Optional[PortfolioCompany]:
        """Extract company information from portfolio item element"""
        try:
            # Get the full text content for analysis
            full_text = element.get_text().strip()
            
            # Extract company name - simpler approach for EIP format
            name = ""
            description = full_text
            
            # Split into sentences and analyze first sentence for company name
            sentences = [s.strip() for s in full_text.split('.') if s.strip()]
            
            if sentences:
                first_sentence = sentences[0].strip()
                
                # Pattern 1: "CompanyName's mission is..."
                if "'s mission is" in first_sentence.lower():
                    name = first_sentence.split("'s")[0].strip()
                
                # Pattern 2: "Founded in YEAR, CompanyName is/does..."
                elif "founded in" in first_sentence.lower():
                    # Find text after year and comma
                    parts = first_sentence.split(',')
                    if len(parts) >= 2:
                        # Get part after comma, take first word(s) before verb
                        after_comma = parts[1].strip()
                        words = after_comma.split()
                        # Look for company name before verbs
                        verbs = ['is', 'was', 'has', 'develops', 'provides', 'creates', 'offers']
                        for i, word in enumerate(words):
                            if word.lower() in verbs and i > 0:
                                name = ' '.join(words[:i]).strip()
                                break
                        if not name and len(words) > 0:
                            # If no verb found, take first 1-2 words
                            name = ' '.join(words[:2]).strip()
                
                # Pattern 3: "CompanyName develops/provides/creates..."
                else:
                    words = first_sentence.split()
                    if len(words) >= 2:
                        verbs = ['develops', 'provides', 'creates', 'builds', 'offers', 'has', 'is', 'was']
                        for i, word in enumerate(words):
                            if word.lower() in verbs and i > 0:
                                name = ' '.join(words[:i]).strip()
                                break
                        
                        # If no verb pattern found, try first word/phrase
                        if not name and len(words) > 0:
                            # Take first word or two if they look like a company name
                            potential = words[0]
                            if len(words) > 1 and len(words[1]) > 1 and not words[1].lower() in ['the', 'is', 'was']:
                                potential = f"{words[0]} {words[1]}"
                            if len(potential) > 1 and potential[0].isupper():
                                name = potential
            
            # Extract website from links
            website = ""
            links = element.find_all('a', href=True)
            for link in links:
                href = link.get('href', '')
                link_text = link.get_text().strip().lower()
                if href and href.startswith('http') and ('visit' in link_text or 'site' in link_text):
                    website = href
                    break
                elif href and href.startswith('http') and link_text == '':
                    # Sometimes links have no text
                    website = href
                    break
            
            # Clean up extracted name
            if name:
                name = re.sub(r'\s+', ' ', name.strip())
                name = re.sub(r'^(the\s+)', '', name, flags=re.IGNORECASE)
                name = name.strip(".,!?()[]{}\"'")
                
                # Remove possessive 's if accidentally included
                if name.endswith("'s"):
                    name = name[:-2]
            
            # Validation
            if not name or len(name) < 2:
                logger.debug(f"No valid name extracted from: {full_text[:100]}")
                return None
            
            # Skip obvious non-company patterns
            skip_patterns = ['portfolio', 'investment', 'company description', 'visit site']
            if any(pattern in name.lower() for pattern in skip_patterns):
                logger.debug(f"Skipping non-company entry: {name}")
                return None
            
            # Limit description length
            if len(description) > 300:
                description = description[:300] + "..."
            
            logger.debug(f"Extracted EIP company: '{name}' from: {full_text[:50]}")
            
            return PortfolioCompany(
                name=name,
                website=website,
                description=description,
                sector="Energy Infrastructure",  # EIP focus area
                vc_firm=self.vc_name,
                portfolio_url=self.base_url,
                confidence_score=0.8
            )
            
        except Exception as e:
            logger.warning(f"Error extracting EIP company: {e}")
            return None
    
    def _supports_pagination(self) -> bool:
        """EIP shows all companies on one page"""
        return False


class BreakthroughEnergyVenturesScraper(VCPortfolioScraper):
    """Scraper for Breakthrough Energy Ventures portfolio"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.breakthroughenergy.org"
        self.portfolio_url = "https://www.breakthroughenergy.org/lookbook/"
        self.vc_name = "Breakthrough Energy Ventures"
    
    def scrape_portfolio(self) -> List[PortfolioCompany]:
        """Scrape Breakthrough Energy Ventures portfolio with pagination support"""
        logger.info(f"Starting {self.vc_name} portfolio scrape...")
        
        self._load_existing_companies()
        all_companies = []
        page = 1
        max_pages = 10  # Safety limit
        
        try:
            while page <= max_pages:
                # Construct URL for current page
                if page == 1:
                    url = self.portfolio_url
                else:
                    url = f"{self.portfolio_url}?paginate={page}&order=DESC"
                
                logger.info(f"Scraping page {page}: {url}")
                
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract companies from current page
                companies = self._extract_companies(soup)
                
                if not companies:
                    logger.info(f"No companies found on page {page}, stopping pagination")
                    break
                
                logger.info(f"Found {len(companies)} companies on page {page}")
                all_companies.extend(companies)
                
                # Check if there's a "Load More" button or next page
                load_more = soup.find('a', class_='load-more')
                next_page_link = soup.find('a', string=re.compile(r'next|load more|show more', re.IGNORECASE))
                
                if not load_more and not next_page_link:
                    logger.info("No more pages available, stopping pagination")
                    break
                
                page += 1
                
                # Rate limiting between pages
                time.sleep(2)
            
            logger.info(f"Total companies found across {page-1} pages: {len(all_companies)}")
            
            # Debug: show first few companies
            for i, company in enumerate(all_companies[:5]):
                logger.info(f"Company {i+1}: {company.name} - {company.description[:50]}...")
            
            # Filter for climate tech and new companies
            filtered_companies = []
            for company in all_companies:
                is_new = self._is_new_company(company)
                is_climate = self._is_climate_related(company.description)
                
                logger.debug(f"Company {company.name}: new={is_new}, climate={is_climate}")
                
                # If no database connection, consider all companies as new
                if not self.supabase:
                    is_new = True
                
                if is_new and is_climate:
                    filtered_companies.append(company)
                    
            logger.info(f"New climate tech companies to process: {len(filtered_companies)}")
            
            self.discovered_companies = filtered_companies
            return filtered_companies
            
        except Exception as e:
            logger.error(f"Error scraping {self.vc_name} portfolio: {e}")
            # Log the response content for debugging
            try:
                if 'response' in locals():
                    logger.debug(f"Response status: {response.status_code}")
                    logger.debug(f"Response URL: {response.url}")
            except:
                pass
            return []
    
    def _extract_companies(self, soup: BeautifulSoup) -> List[PortfolioCompany]:
        """Extract company information from portfolio page"""
        companies = []
        
        # Use table tbody tr method to get paginated content
        table_row_elements = soup.select('table tbody tr')
        
        logger.info(f"Found {len(table_row_elements)} company elements (table tbody tr)")
        
        for element in table_row_elements:
            try:
                company = self._extract_company_from_element(element)
                if company and company.name and len(company.name) > 1:
                    companies.append(company)
                    logger.debug(f"Successfully extracted: {company.name}")
                else:
                    logger.debug(f"Failed extraction or invalid company: {company}")
            except Exception as e:
                logger.debug(f"Error extracting company from element: {e}")
                continue
        
        return companies
    
    def _extract_company_from_element(self, element) -> Optional[PortfolioCompany]:
        """Extract company information from table row element"""
        try:
            # For table rows, we have a structured format
            cells = element.find_all(['td', 'th'])
            if len(cells) < 2:
                return None
            
            # Extract company name from first cell with class='name'
            name_cell = cells[0]
            name = ""
            
            # Look for span with class="title" (this contains the company name)
            title_span = name_cell.find('span', class_='title')
            if title_span:
                name = self._clean_text(title_span.get_text())
            
            # If no title span, try to extract from the cell text
            if not name:
                cell_text = name_cell.get_text().strip()
                # Split and take first part as company name
                parts = cell_text.split()
                if parts:
                    name = parts[0]
            
            # Extract description from second cell with class='description'
            description = ""
            if len(cells) > 1:
                desc_cell = cells[1]
                description = self._clean_text(desc_cell.get_text())
                if len(description) > 200:
                    description = description[:200] + "..."
            
            # Extract sector from third cell if available
            sector = "Climate Tech"
            if len(cells) > 2:
                sector_cell = cells[2]
                sector_text = self._clean_text(sector_cell.get_text())
                if sector_text and sector_text not in ['Ventures']:
                    sector = sector_text
            
            # Look for website link in the actions cell
            website = ""
            if len(cells) > 5:  # Actions cell is usually last
                actions_cell = cells[5]
                links = actions_cell.find_all('a', href=True)
                for link in links:
                    href = link.get('href')
                    if href and 'lookbook' in href:
                        # This is the BEV detail page, we can try to extract actual website later
                        # For now, just note that we found the company
                        break
            
            # Basic validation
            if not name or len(name) < 2:
                return None
            
            # Clean up the name
            name = re.sub(r'\s+', ' ', name.strip())
            
            # Skip obvious non-company entries
            skip_patterns = [
                'company', 'description', 'sector', 'program', 'technology',
                'load more', 'view all', 'filter', 'search'
            ]
            
            if any(pattern in name.lower() for pattern in skip_patterns):
                logger.debug(f"Skipping non-company entry: {name}")
                return None
            
            if not description:
                description = f"Portfolio company of {self.vc_name}"
            
            logger.debug(f"Extracted company: {name}")
            
            return PortfolioCompany(
                name=name,
                website=website,
                description=description,
                sector=sector,
                vc_firm=self.vc_name,
                portfolio_url=self.portfolio_url,
                confidence_score=0.8  # High confidence for BEV portfolio
            )
            
        except Exception as e:
            logger.debug(f"Error extracting company info from element: {e}")
            return None
    
    def _looks_like_company_link(self, link) -> bool:
        """Determine if a link looks like it points to a company"""
        href = link.get('href', '').lower()
        text = link.get_text().strip()
        
        # Skip navigation, footer, and other non-company links
        skip_patterns = [
            'about', 'contact', 'news', 'blog', 'careers', 'privacy',
            'terms', 'cookie', 'linkedin', 'twitter', 'facebook',
            'mailto:', '#', 'javascript:', '.pdf', '.jpg', '.png'
        ]
        
        if any(pattern in href for pattern in skip_patterns):
            return False
        
        # Look for external links (potential company websites) or portfolio paths
        if (href.startswith('http') and 'breakthroughenergy.org' not in href) or 'portfolio' in href:
            return True
            
        return False
    
    def _extract_company_info(self, element) -> Optional[PortfolioCompany]:
        """Extract company information from HTML element"""
        try:
            # Try to extract company name
            name = ""
            name_selectors = ['h1', 'h2', 'h3', 'h4', '.company-name', '.name', 'strong']
            for selector in name_selectors:
                name_elem = element.select_one(selector)
                if name_elem:
                    name = self._clean_text(name_elem.get_text())
                    break
            
            if not name:
                # Use link text as fallback
                name = self._clean_text(element.get_text())
            
            # Try to extract website
            website = ""
            if element.name == 'a' and element.get('href'):
                website = element.get('href')
                if not website.startswith('http'):
                    website = urljoin(self.base_url, website)
            else:
                link = element.find('a', href=True)
                if link:
                    website = link.get('href')
                    if not website.startswith('http'):
                        website = urljoin(self.base_url, website)
            
            # Try to extract description
            description = ""
            desc_selectors = ['.description', '.summary', 'p', '.company-description']
            for selector in desc_selectors:
                desc_elem = element.select_one(selector)
                if desc_elem:
                    description = self._clean_text(desc_elem.get_text())
                    break
            
            if not description:
                # Use all text content as fallback
                description = self._clean_text(element.get_text())
            
            # Basic validation
            if not name or len(name) < 2:
                return None
            
            return PortfolioCompany(
                name=name,
                website=website,
                description=description,
                sector="Climate Tech",  # Default for Breakthrough Energy
                vc_firm=self.vc_name,
                portfolio_url=self.portfolio_url,
                confidence_score=0.8  # High confidence for BEV portfolio
            )
            
        except Exception as e:
            logger.debug(f"Error extracting company info: {e}")
            return None
    
    def _is_new_company(self, company: PortfolioCompany) -> bool:
        """Check if company is new (not in existing database)"""
        name_check = company.name.lower().strip() not in self.existing_companies
        website_check = True
        
        if company.website:
            domain = self._extract_domain(company.website)
            website_check = domain not in self.existing_companies
        
        return name_check and website_check
    
    def _filter_new_companies(self, companies: List[PortfolioCompany]) -> List[PortfolioCompany]:
        """Filter out companies that already exist in our database"""
        return [company for company in companies if self._is_new_company(company)]

def main():
    """Main execution function - scrape multiple VC portfolios"""
    print("Climate Tech VC Portfolio Monitor - Phase 2A Extended")
    print("=" * 55)
    
    # Initialize scrapers
    scrapers = [
        BreakthroughEnergyVenturesScraper(),
        EnergyImpactPartnersScraper()
    ]
    
    all_companies = []
    
    for scraper in scrapers:
        print(f"\n🏢 Scraping {scraper.vc_name} Portfolio...")
        print("=" * (len(scraper.vc_name) + 20))
        
        # Scrape portfolio
        companies = scraper.scrape_portfolio()
        
        if companies:
            print(f"✅ Discovered {len(companies)} companies from {scraper.vc_name}")
            all_companies.extend(companies)
        else:
            print(f"❌ No companies found from {scraper.vc_name}")
    
    if not all_companies:
        print("\n❌ No companies discovered from any VC")
        return
    
    print(f"\n🎯 PORTFOLIO SUMMARY")
    print("=" * 20)
    
    # Group by VC for summary
    vc_counts = {}
    for company in all_companies:
        vc = company.vc_firm
        vc_counts[vc] = vc_counts.get(vc, 0) + 1
    
    for vc, count in vc_counts.items():
        print(f"📊 {vc}: {count} companies")
    
    print(f"📊 Total: {len(all_companies)} companies")
    
    print(f"\n🔄 Processing {len(all_companies)} companies...")
    
    # Save companies to database
    saved_count = 0
    for i, company in enumerate(all_companies, 1):
        print(f"\n[{i}/{len(all_companies)}] Processing {company.name} ({company.vc_firm})...")
        
        # Use the appropriate scraper for saving
        for scraper in scrapers:
            if scraper.vc_name == company.vc_firm:
                if scraper.save_to_database(company):
                    saved_count += 1
                break
        
        # Rate limiting
        time.sleep(1)
    
    print(f"\n🎉 SUCCESS SUMMARY")
    print("=" * 20)
    print(f"✅ Successfully saved {saved_count}/{len(all_companies)} companies")
    print(f"📋 Check vc_portfolio_scraper.log for detailed logs")
    
    # Show sample of discovered companies
    print(f"\n🌟 Sample Discoveries:")
    print("-" * 25)
    for company in all_companies[:5]:
        print(f"• {company.name} ({company.vc_firm}) - {company.sector}")

if __name__ == "__main__":
    main()
