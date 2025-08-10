# =============================================================================
# NEW SCHEMA ADAPTER - SMART DEAL INSERTION
# =============================================================================
# This module provides functions to insert deals into the new normalized schema
# while maintaining compatibility with existing scrapers.

import os
from supabase import create_client, Client
from datetime import datetime
import re
from typing import Optional, Dict, Any, List

class SchemaAwareDealInserter:
    """
    Handles intelligent insertion of deals into the new normalized schema.
    Automatically creates companies and investor relationships as needed.
    """
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        
    def insert_deal(self, 
                   company_name: str,
                   source_url: str, 
                   raw_text_content: str,
                   source_type: str = 'news',
                   source_name: Optional[str] = None,
                   detected_funding_stage: Optional[str] = None,
                   detected_amount: Optional[str] = None,
                   detected_investors: Optional[List[str]] = None,
                   detected_sector: Optional[str] = None,
                   detected_country: Optional[str] = None,
                   has_ai_focus: bool = False) -> Optional[str]:
        """
        Insert a deal into the new normalized schema.
        Returns the deal_id if successful, None if failed.
        """
        
        try:
            # Step 1: Get or create company
            company_id = self._get_or_create_company(
                name=company_name,
                country=detected_country,
                sector=detected_sector,
                has_ai_focus=has_ai_focus
            )
            
            if not company_id:
                print(f"Failed to create/find company: {company_name}")
                return None
                
            # Step 2: Insert deal using RPC to bypass RLS
            deal_id = self.supabase.rpc('create_deal_safe_v2', {
                'company_id': company_id,
                'source_url': source_url,
                'raw_content': raw_text_content,
                'funding_stage': detected_funding_stage,
                'amount_usd': self._parse_funding_amount(detected_amount),
                'original_amount': detected_amount,
                'source_type': source_type,
                'source_name': source_name or self._extract_source_name(source_url)
            }).execute()
            
            if not deal_id.data:
                print(f"Failed to insert deal for {company_name}")
                return None
                
            deal_id = deal_id.data
            
            # Step 3: Create investor relationships if detected
            if detected_investors:
                self._create_investor_relationships(deal_id, detected_investors)
            
            print(f"Successfully inserted deal for {company_name} (ID: {deal_id})")
            return deal_id
            
        except Exception as e:
            print(f"Error inserting deal for {company_name}: {e}")
            return None
    
    def _get_or_create_company(self, name: str, country: Optional[str] = None, 
                              sector: Optional[str] = None, has_ai_focus: bool = False) -> Optional[str]:
        """Get existing company or create new one using RPC to bypass RLS."""
        
        try:
            # Use RPC function to bypass RLS
            result = self.supabase.rpc('create_company_safe_v2', {
                'company_name': name,
                'country': country,
                'sector': sector,
                'ai_focus': has_ai_focus
            }).execute()
            
            if result.data:
                return result.data
            
        except Exception as e:
            print(f"RPC company creation failed: {e}")
            
        return None
    
    def _create_investor_relationships(self, deal_id: str, investor_names: List[str]):
        """Create investor records and relationships using RPC."""
        
        for investor_name in investor_names:
            if not investor_name or len(investor_name.strip()) < 2:
                continue
                
            try:
                # Create investor using RPC
                investor_id = self.supabase.rpc('create_investor_safe_v2', {
                    'investor_name': investor_name.strip(),
                    'investor_type': 'vc'
                }).execute()
                
                if investor_id.data:
                    # Create relationship
                    self.supabase.table('deal_investors').insert({
                        'deal_id': deal_id,
                        'investor_id': investor_id.data,
                        'role': 'participant'
                    }).execute()
                    
            except Exception as e:
                print(f"Failed to create investor relationship for {investor_name}: {e}")
                continue
    
    def _parse_funding_amount(self, amount_str: Optional[str]) -> Optional[float]:
        """Parse funding amount string to USD float."""
        if not amount_str:
            return None
            
        # Remove currency symbols and clean
        clean_amount = re.sub(r'[^\d.,BbMmKk\s]', '', amount_str.upper())
        
        # Extract numeric value
        match = re.search(r'([\d.,]+)\s*([BMK]?)', clean_amount)
        if not match:
            return None
            
        value_str, multiplier = match.groups()
        
        try:
            value = float(value_str.replace(',', ''))
            
            if multiplier == 'B':
                return value * 1_000_000_000
            elif multiplier == 'M':
                return value * 1_000_000
            elif multiplier == 'K':
                return value * 1_000
            else:
                return value
        except:
            return None
    
    def _extract_source_name(self, url: str) -> str:
        """Extract source name from URL."""
        if 'techcrunch.com' in url:
            return 'TechCrunch'
        elif 'climateinsider.com' in url:
            return 'Climate Insider'
        elif 'axios.com' in url:
            return 'Axios'
        elif 'canary.media' in url:
            return 'Canary Media'
        elif 'ctvc.co' in url:
            return 'Climate Tech VC'
        elif 'agfundernews.com' in url:
            return 'AgFunder News'
        elif 'techfundingnews.com' in url:
            return 'Tech Funding News'
        else:
            # Extract domain
            import re
            match = re.search(r'https?://(?:www\.)?([^/]+)', url)
            return match.group(1) if match else 'Unknown'
    
    def _calculate_basic_alex_score(self, funding_stage: Optional[str] = None,
                                   amount: Optional[str] = None,
                                   has_ai_focus: bool = False,
                                   sector: Optional[str] = None,
                                   country: Optional[str] = None) -> int:
        """Calculate a basic Alex score for newly scraped deals."""
        
        score = 0
        
        # Stage scoring (0-30 points)
        if funding_stage:
            stage_lower = funding_stage.lower()
            if any(term in stage_lower for term in ['seed', 'series a', 'series-a']):
                score += 30
            elif 'series b' in stage_lower or 'series-b' in stage_lower:
                score += 25
            elif 'pre-seed' in stage_lower:
                score += 20
            else:
                score += 10
        
        # AI focus bonus (0-25 points)
        if has_ai_focus:
            score += 25
        
        # Sector bonus (0-15 points)
        if sector:
            sector_lower = sector.lower()
            if any(term in sector_lower for term in ['energy', 'industrial', 'transport']):
                score += 15
            elif any(term in sector_lower for term in ['climate', 'carbon', 'sustainable']):
                score += 12
        
        # Geography bonus (0-15 points)
        if country:
            country_lower = country.lower()
            if any(term in country_lower for term in ['us', 'usa', 'united states', 'america']):
                score += 15
            elif any(term in country_lower for term in ['uk', 'europe', 'germany', 'france']):
                score += 10
        
        # Amount bonus (0-15 points)
        if amount:
            amount_usd = self._parse_funding_amount(amount)
            if amount_usd:
                if 1_000_000 <= amount_usd <= 50_000_000:  # $1M-$50M sweet spot
                    score += 15
                elif amount_usd < 1_000_000:
                    score += 10
                elif amount_usd <= 100_000_000:
                    score += 8
        
        return min(100, max(0, score))


# =============================================================================
# LEGACY SCRAPER COMPATIBILITY FUNCTION
# =============================================================================

def insert_legacy_deal(supabase: Client, company_name: str, source_url: str, 
                      raw_text_content: str, status: str = 'NEW') -> bool:
    """
    Compatibility function for existing scrapers.
    Drop-in replacement for the old direct deals table insertion.
    """
    
    inserter = SchemaAwareDealInserter(supabase)
    
    # Detect AI focus from content
    has_ai_focus = any(term in raw_text_content.lower() 
                      for term in ['artificial intelligence', 'machine learning', 'ai-powered', 
                                  'ai technology', 'ai platform', 'ai solution'])
    
    # Attempt basic extraction from raw text
    detected_stage = _extract_funding_stage(raw_text_content)
    detected_amount = _extract_funding_amount(raw_text_content)
    detected_investors = _extract_investors(raw_text_content)
    
    deal_id = inserter.insert_deal(
        company_name=company_name,
        source_url=source_url,
        raw_text_content=raw_text_content,
        source_type='news',
        has_ai_focus=has_ai_focus,
        detected_funding_stage=detected_stage,
        detected_amount=detected_amount,
        detected_investors=detected_investors
    )
    
    return deal_id is not None


def _extract_funding_stage(text: str) -> Optional[str]:
    """Extract funding stage from raw text."""
    text_lower = text.lower()
    
    if 'series a' in text_lower or 'series-a' in text_lower:
        return 'Series A'
    elif 'series b' in text_lower or 'series-b' in text_lower:
        return 'Series B'  
    elif 'series c' in text_lower or 'series-c' in text_lower:
        return 'Series C'
    elif 'seed round' in text_lower or 'seed funding' in text_lower:
        return 'Seed'
    elif 'pre-seed' in text_lower:
        return 'Pre-seed'
    
    return None


def _extract_funding_amount(text: str) -> Optional[str]:
    """Extract funding amount from raw text."""
    import re
    
    # Look for patterns like "$5M", "$1.2 million", "raised $25 million"
    patterns = [
        r'\$(\d+(?:\.\d+)?)\s*(million|billion|M|B)',
        r'raised \$(\d+(?:\.\d+)?)\s*(million|billion|M|B)',
        r'(\d+(?:\.\d+)?)\s*(million|billion)\s*(?:dollar|USD|funding)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value, unit = match.groups()
            return f"${value} {unit}"
    
    return None


def _extract_investors(text: str) -> List[str]:
    """Extract investor names from raw text."""
    import re
    
    investors = []
    
    # Look for patterns like "led by X", "funded by Y", etc.
    patterns = [
        r'led by ([^,.]+(?:Capital|Ventures|Partners|Fund|VC))',
        r'funded by ([^,.]+(?:Capital|Ventures|Partners|Fund|VC))',
        r'investors include ([^,.]+(?:Capital|Ventures|Partners|Fund|VC))',
        r'from ([^,.]+(?:Capital|Ventures|Partners|Fund|VC))'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        investors.extend([match.strip() for match in matches])
    
    return list(set(investors))  # Remove duplicates
