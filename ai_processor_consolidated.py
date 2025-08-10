#!/usr/bin/env python3
"""
CONSOLIDATED AI PROCESSOR FOR LAYER 2 CLIMATE TECH DISCOVERY
=============================================================
This is the SINGLE AI processing file that handles all climate tech data processing:
- Date extraction from existing process_articles_ai_v2.py
- Source-aware processing (government, VC portfolio, news)
- Integration with V2 schema adapter
- Works with the new normalized schema
"""

import os
import re
from datetime import datetime, timedelta
from supabase import create_client, Client
from transformers import pipeline
import time
from dotenv import load_dotenv
from typing import Optional, Dict, List, Any
from schema_adapter import SchemaAwareDealInserter

# --- Configuration ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# --- Initialize Supabase Client ---
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Successfully connected to Supabase.")
except Exception as e:
    print(f"❌ Error connecting to Supabase: {e}")
    exit()

# --- Load the AI Models ---
try:
    print("🤖 Loading AI models...")
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")
    print("✅ AI models loaded successfully.")
except Exception as e:
    print(f"❌ Error loading AI models: {e}")
    exit()

class ConsolidatedAIProcessor:
    """THE definitive AI processor for all climate tech data processing."""
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.schema_inserter = SchemaAwareDealInserter(supabase_client)
        
        # Source-specific configurations
        self.government_agencies = [
            'DOE', 'Department of Energy', 'ORNL', 'Oak Ridge',
            'NREL', 'National Renewable Energy', 'ARPA-E', 'NSF',
            'Lawrence Berkeley', 'Sandia', 'Argonne'
        ]
        
        self.funding_stage_mapping = {
            'government_research': {
                'grant': 'Government Grant',
                'award': 'Research Award', 
                'funding': 'Government Funding',
                'research': 'Research Phase',
                'pilot': 'Pilot Project',
                'demonstration': 'Demonstration Phase'
            },
            'vc_portfolio': {
                'portfolio': 'Portfolio Company',
                'investment': 'Past Investment',
                'backed': 'VC Backed'
            },
            'news': {
                'seed': 'Seed',
                'series a': 'Series A',
                'series b': 'Series B',
                'pre-seed': 'Pre-seed'
            }
        }

    def process_all_pending(self, limit: int = 10, source_types: List[str] = None):
        """Process all pending deals from Layer 2 data."""
        
        print(f"\n🔍 Processing Layer 2 climate tech discoveries...")
        print("=" * 60)
        
        # Build query filter
        query = self.supabase.table('deals_new').select('*,companies(*)')
        
        if source_types:
            # Filter by specific source types
            query = query.in_('source_type', source_types)
        else:
            # Process all source types
            query = query.in_('source_type', ['government_research', 'vc_portfolio', 'news'])
            
        # Get pending deals
        response = query.eq('status', 'NEW').limit(limit).execute()
        
        if not response.data:
            print("✅ No deals need AI processing. All caught up!")
            return 0
            
        print(f"📊 Found {len(response.data)} deals to process")
        
        processed_count = 0
        for deal in response.data:
            if self.process_single_deal(deal):
                processed_count += 1
                time.sleep(1)  # Rate limiting
                
        print(f"\n🎉 Processed {processed_count} deals successfully!")
        return processed_count

    def process_single_deal(self, deal: Dict[str, Any]) -> bool:
        """Process a single deal with source-aware AI extraction."""
        
        deal_id = deal['id']
        source_type = deal['source_type']
        raw_content = deal['raw_text_content']
        company_name = deal.get('companies', {}).get('name', 'Unknown Company')
        
        print(f"\n🤖 Processing Deal ID: {deal_id}")
        print(f"   📋 Company: {company_name}")
        print(f"   🔧 Source Type: {source_type}")
        
        try:
            # Step 1: Source-aware relevance check
            if not self._is_relevant_for_source_type(raw_content, source_type):
                print("   ❌ Not relevant for climate tech - marking as irrelevant")
                self._update_deal_status(deal_id, 'IRRELEVANT')
                return True
            
            # Step 2: Extract information using source-aware AI
            extracted_data = self._extract_with_source_awareness(raw_content, deal, source_type)
            print(f"   📊 Extracted: {list(extracted_data.keys())}")
            
            # Step 3: Post-extraction climate tech validation
            if not self._validate_climate_tech_relevance(extracted_data, raw_content, source_type):
                print("   ❌ Post-extraction validation: Not climate tech - marking as irrelevant")
                self._update_deal_status(deal_id, 'IRRELEVANT')
                return True
            
            # Step 4: Update the deal with extracted information
            self._update_deal_with_ai_data(deal_id, extracted_data)
            
            # Step 4.5: Update company name if extracted from news (NEW)
            if extracted_data.get('company_name') and source_type == 'news':
                self._update_company_name(deal, extracted_data['company_name'])
            
            # Step 5: Create enhanced relationships (investors, etc.)
            self._create_enhanced_relationships(deal_id, extracted_data)
            
            # Step 6: Update status
            self._update_deal_status(deal_id, 'PROCESSED_AI')
            print(f"   ✅ Successfully processed {source_type} deal")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Processing failed: {e}")
            self._update_deal_status(deal_id, 'PROCESSING_ERROR')
            return False

    def _is_relevant_for_source_type(self, content: str, source_type: str) -> bool:
        """Check if content is relevant based on source type."""
        
        if source_type == 'government_research':
            # Government research is usually relevant if it mentions climate/energy/tech
            climate_keywords = ['climate', 'energy', 'renewable', 'carbon', 'emission', 'sustainable', 'green', 'cleantech']
            return any(keyword in content.lower() for keyword in climate_keywords)
            
        elif source_type == 'vc_portfolio':
            # VC portfolio entries are usually relevant by definition
            return True
            
        elif source_type == 'news':
            # Traditional news needs BOTH funding indicators AND climate relevance
            funding_keywords = ['funding', 'raised', 'investment', 'round', 'series', 'seed', 'venture']
            climate_keywords = ['climate', 'energy', 'renewable', 'carbon', 'emission', 'sustainable', 'green', 'cleantech', 'solar', 'wind', 'battery', 'electric', 'ev', 'clean tech', 'environmental']
            
            has_funding = any(keyword in content.lower() for keyword in funding_keywords)
            has_climate = any(keyword in content.lower() for keyword in climate_keywords)
            
            return has_funding and has_climate
            
        return True

    def _validate_climate_tech_relevance(self, extracted_data: Dict[str, Any], content: str, source_type: str) -> bool:
        """Post-extraction validation to ensure the deal is actually climate tech related."""
        
        # For government research and VC portfolio, we trust the initial filtering
        if source_type in ['government_research', 'vc_portfolio']:
            return True
        
        # For news articles, we need stricter validation after extraction
        if source_type == 'news':
            # Check if we extracted any climate-related sectors
            climate_sectors = extracted_data.get('climate_sectors', [])
            if climate_sectors and len(climate_sectors) > 0:
                # Filter out generic/weak climate indicators
                strong_climate_sectors = [s for s in climate_sectors if s.lower() not in ['general', 'other', 'unknown', 'tech']]
                if strong_climate_sectors:
                    return True
            
            # Check if the company description indicates climate focus
            company_description = extracted_data.get('company_description', '')
            if company_description:
                climate_indicators = [
                    'renewable energy', 'solar power', 'wind energy', 'battery technology',
                    'electric vehicle', 'carbon capture', 'climate change', 'sustainability',
                    'clean energy', 'green technology', 'environmental', 'emission reduction',
                    'energy storage', 'smart grid', 'cleantech', 'decarbonization',
                    'circular economy', 'waste reduction', 'energy efficiency'
                ]
                
                description_lower = company_description.lower()
                if any(indicator in description_lower for indicator in climate_indicators):
                    return True
            
            # Additional check: Look for AI companies that are not climate-focused
            # This specifically catches cases like Neuralk-AI
            has_ai_focus = extracted_data.get('has_ai_focus', False)
            if has_ai_focus:
                # If it's AI-focused, make sure it's climate-related AI
                non_climate_ai_indicators = [
                    'marketing', 'advertising', 'customer data', 'sales', 'crm',
                    'social media', 'content creation', 'game', 'gaming', 'entertainment',
                    'fintech', 'financial services', 'banking', 'insurance', 'real estate',
                    'healthcare', 'medical', 'pharmaceutical', 'biotech', 'education',
                    'e-commerce', 'retail', 'fashion', 'food delivery', 'restaurant'
                ]
                
                content_lower = content.lower()
                company_desc_lower = company_description.lower() if company_description else ''
                
                # If we find non-climate AI indicators and no strong climate indicators
                if any(indicator in content_lower or indicator in company_desc_lower for indicator in non_climate_ai_indicators):
                    # Double-check for climate relevance
                    strong_climate_keywords = [
                        'renewable energy', 'solar', 'wind', 'battery', 'electric vehicle',
                        'carbon capture', 'emission', 'climate', 'clean energy', 'grid',
                        'energy storage', 'sustainability', 'environmental monitoring'
                    ]
                    
                    if not any(keyword in content_lower for keyword in strong_climate_keywords):
                        return False
            
            # If we reach here and no amount was extracted (no funding details), likely not relevant
            if not extracted_data.get('amount_usd') and not extracted_data.get('original_amount'):
                return False
        
        return True

    def _extract_with_source_awareness(self, content: str, deal: Dict, source_type: str) -> Dict[str, Any]:
        """Extract information with awareness of source type."""
        
        extracted = {}
        
        if source_type == 'government_research':
            extracted = self._extract_government_research_data(content, deal)
        elif source_type == 'vc_portfolio':
            extracted = self._extract_vc_portfolio_data(content, deal)
        elif source_type == 'news':
            extracted = self._extract_news_data(content, deal)
        
        # Common extractions for all source types
        extracted.update({
            'climate_sectors': self._classify_climate_sector(content),
            'has_ai_focus': self._detect_ai_focus(content),
            'headquarters_country': self._extract_geography(content)
        })
        
        return extracted

    def _extract_government_research_data(self, content: str, deal: Dict) -> Dict[str, Any]:
        """Extract data specific to government research sources."""
        
        extracted = {
            'source_type': 'government_research',
            'confidence_adjustments': {
                'base_confidence': 0.7,  # Lower than VC/news due to early stage
                'trl_bonus': 0,
                'agency_bonus': 0.1 if any(agency.lower() in content.lower() for agency in self.government_agencies) else 0,
                'commercial_timeline_penalty': 0
            }
        }
        
        # Extract technology readiness level
        trl_patterns = [
            r'TRL\s*(\d+)', r'Technology Readiness Level\s*(\d+)',
            r'readiness level\s*(\d+)', r'maturity level\s*(\d+)'
        ]
        
        for pattern in trl_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                extracted['technology_readiness'] = int(match.group(1))
                if extracted['technology_readiness'] >= 7:
                    extracted['confidence_adjustments']['trl_bonus'] = 0.2
                break
        
        # Identify government agencies
        agencies_found = [agency for agency in self.government_agencies 
                         if agency.lower() in content.lower()]
        extracted['government_agencies'] = agencies_found
        extracted['investors'] = agencies_found  # Government agencies are "investors"
        
        # Extract research focus areas
        research_keywords = ['quantum', 'fusion', 'battery', 'solar', 'wind', 'carbon capture', 
                           'hydrogen', 'biofuel', 'geothermal', 'nuclear']
        extracted['research_focus'] = [kw for kw in research_keywords if kw in content.lower()]
        extracted['climate_sectors'] = extracted['research_focus']  # Same for government research
        
        # Estimate commercialization timeline
        if any(word in content.lower() for word in ['demonstration', 'pilot', 'deployment']):
            extracted['commercialization_timeline'] = '3-5 years'
        elif any(word in content.lower() for word in ['laboratory', 'research', 'development']):
            extracted['commercialization_timeline'] = '5-7 years'
        else:
            extracted['commercialization_timeline'] = '7+ years'
        
        # Government funding stage mapping
        extracted['funding_stage'] = 'Research Phase'  # Default for government research
        
        return extracted

    def _extract_vc_portfolio_data(self, content: str, deal: Dict) -> Dict[str, Any]:
        """Extract data specific to VC portfolio sources."""
        
        extracted = {
            'source_type': 'vc_portfolio',
            'confidence_adjustments': {
                'base_confidence': 0.9,  # High confidence - already validated by VCs
                'vc_validation_bonus': 0.1,
                'portfolio_status_bonus': 0.05
            }
        }
        
        # Extract VC firm names
        vc_patterns = [
            r'([A-Z][a-zA-Z\s&]+(?:Ventures|Capital|Partners|Fund|Investing))',
            r'(Breakthrough Energy[^,\.]*)',
            r'([A-Z][a-zA-Z\s]+VC)'
        ]
        
        investors_found = []
        for pattern in vc_patterns:
            matches = re.findall(pattern, content)
            investors_found.extend(matches)
        
        extracted['investors'] = list(set(investors_found))
        extracted['lead_investor'] = investors_found[0] if investors_found else None
        
        # VC funding stage
        extracted['funding_stage'] = 'Portfolio Company'
        
        # LIGHT DATE EXTRACTION for VC Portfolio (when available)
        investment_date_patterns = [
            r'invested in (\d{4})',
            r'joined portfolio in ([A-Za-z]+ \d{4})',
            r'(series [a-z]) in (\d{4})',
            r'(Q[1-4] \d{4})',
            r'(\d{4}) investment',
            r'funded in (\d{4})'
        ]
        
        for pattern in investment_date_patterns:
            match = re.search(pattern, content.lower())
            if match:
                date_text = match.group(1) if len(match.groups()) == 1 else match.group(0)
                # Try to parse the date
                parsed_date = self._parse_vc_investment_date(date_text)
                if parsed_date:
                    extracted['investment_date'] = parsed_date
                    print(f"   📅 VC Investment date found: {parsed_date}")
                    break
        
        # If no specific date found, use publication date as fallback
        if not extracted.get('investment_date'):
            article_date = self._get_article_publication_date(deal)
            if article_date:
                extracted['investment_date'] = article_date
                print(f"   📅 Using publication date for VC entry: {article_date}")
        
        # Extract investment thesis keywords
        thesis_keywords = ['net zero', 'carbon neutral', 'decarbonization', 'climate tech', 
                          'clean energy', 'sustainability', 'renewable']
        extracted['investment_thesis'] = [kw for kw in thesis_keywords if kw in content.lower()]
        
        # Competitive analysis
        extracted['competitive_analysis'] = {
            'portfolio_positioning': f"{extracted['lead_investor']} Portfolio Company" if extracted['lead_investor'] else 'VC Portfolio Company',
            'investment_validation': True,
            'market_segment': 'Climate Tech'
        }
        
        return extracted

    def _extract_news_data(self, content: str, deal: Dict) -> Dict[str, Any]:
        """Extract data from traditional news sources with enhanced date extraction."""
        
        extracted = {
            'source_type': 'news',
            'confidence_adjustments': {
                'base_confidence': 0.8,
                'news_recency_bonus': 0.1
            }
        }
        
        # ENHANCED DATE EXTRACTION (from process_articles_ai_v2.py)
        date_questions = [
            "When was this funding announced?",
            "What date was the funding round announced?", 
            "When did the company raise this money?",
            "When was this deal announced?",
            "What is the announcement date?"
        ]
        
        # Get article publication date as reference
        article_date = self._get_article_publication_date(deal)
        print(f"   📰 Article publication date: {article_date}")
        
        for question in date_questions:
            try:
                result = qa_pipeline(question=question, context=content)
                print(f"   📅 Date Q: '{question}' → '{result['answer']}' (score: {result['score']:.3f})")
                if result['score'] > 0.3:
                    parsed_date = self._parse_announcement_date(result['answer'], article_date)
                    if parsed_date:
                        extracted['announcement_date'] = parsed_date
                        print(f"   ✅ Extracted date: {parsed_date}")
                        break
            except Exception as e:
                print(f"   ⚠️  Date extraction error: {e}")
                continue
        
        # Fallback: Direct content scanning
        if not extracted.get('announcement_date'):
            print(f"   🔍 Attempting direct date scanning...")
            direct_date = self._scan_content_for_dates(content, article_date)
            if direct_date:
                extracted['announcement_date'] = direct_date
                print(f"   ✅ Found date via content scan: {direct_date}")
        
        # Extract company name (NEW - Extract clean company name from article)
        company_questions = [
            "What is the name of the company that raised funding?",
            "Which company is this article about?",
            "What is the startup's name?",
            "What company received the investment?"
        ]
        
        for question in company_questions:
            try:
                result = qa_pipeline(question=question, context=content)
                if result['score'] > 0.5:
                    extracted['company_name'] = self._clean_company_name(result['answer'])
                    break
            except:
                continue
        
        # Extract funding amount
        amount_questions = [
            "How much money was raised?",
            "What was the funding amount?",
            "How much did the company raise?"
        ]
        
        for question in amount_questions:
            try:
                result = qa_pipeline(question=question, context=content)
                if result['score'] > 0.4:
                    extracted['funding_amount_usd'] = self._parse_funding_amount(result['answer'])
                    extracted['funding_amount_text'] = result['answer']
                    break
            except:
                continue
        
        # Extract funding stage
        stage_questions = [
            "What funding round was this?",
            "What series was the funding?",
            "Was this seed, Series A, or Series B funding?"
        ]
        
        for question in stage_questions:
            try:
                result = qa_pipeline(question=question, context=content)
                if result['score'] > 0.3:
                    extracted['funding_stage'] = self._normalize_funding_stage(result['answer'])
                    break
            except:
                continue
        
        # Extract investors
        investor_questions = [
            "Which investors participated?",
            "Who invested in the company?",
            "Who were the investors in this round?"
        ]
        
        investors = set()
        for question in investor_questions:
            try:
                result = qa_pipeline(question=question, context=content)
                if result['score'] > 0.4:
                    investor_names = self._extract_investor_names(result['answer'])
                    investors.update(investor_names)
            except:
                continue
        
        extracted['investors'] = list(investors)
        
        return extracted

    # UTILITY METHODS (from process_articles_ai_v2.py)
    
    def _get_article_publication_date(self, deal: Dict) -> Optional[str]:
        """Get the article publication date as reference."""
        if deal.get('date_announced'):
            return deal['date_announced']
        if deal.get('created_at'):
            return deal['created_at'][:10]  # Extract date part
        return None

    def _parse_announcement_date(self, date_answer: str, reference_date: Optional[str] = None) -> Optional[str]:
        """Parse announcement date from AI answer."""
        
        # Clean the answer
        date_answer = date_answer.strip().lower()
        
        # Common date patterns
        date_patterns = [
            r'(\d{4})-(\d{1,2})-(\d{1,2})',  # YYYY-MM-DD
            r'(\d{1,2})/(\d{1,2})/(\d{4})',   # MM/DD/YYYY
            r'(\d{1,2})-(\d{1,2})-(\d{4})',   # MM-DD-YYYY
            r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2}),?\s+(\d{4})',  # Month DD, YYYY
            r'(\d{1,2})\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})'   # DD Month YYYY
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, date_answer)
            if match:
                try:
                    if len(match.groups()) == 3:
                        # Convert to standard format
                        if pattern.startswith(r'(\d{4})'):  # YYYY-MM-DD
                            return f"{match.group(1)}-{match.group(2).zfill(2)}-{match.group(3).zfill(2)}"
                        elif 'january|february' in pattern:  # Month name patterns
                            month_names = ['january', 'february', 'march', 'april', 'may', 'june',
                                          'july', 'august', 'september', 'october', 'november', 'december']
                            if match.group(1).lower() in month_names:
                                month_num = month_names.index(match.group(1).lower()) + 1
                                return f"{match.group(3)}-{str(month_num).zfill(2)}-{match.group(2).zfill(2)}"
                            elif match.group(2).lower() in month_names:
                                month_num = month_names.index(match.group(2).lower()) + 1
                                return f"{match.group(3)}-{str(month_num).zfill(2)}-{match.group(1).zfill(2)}"
                        else:  # MM/DD/YYYY or MM-DD-YYYY
                            return f"{match.group(3)}-{match.group(1).zfill(2)}-{match.group(2).zfill(2)}"
                except:
                    continue
        
        return None

    def _scan_content_for_dates(self, content: str, reference_date: Optional[str] = None) -> Optional[str]:
        """Direct scan for date patterns in content."""
        
        # Look for recent dates (within last 3 years)
        current_year = datetime.now().year
        recent_years = [current_year, current_year - 1, current_year - 2]
        
        date_patterns = [
            r'(\d{4})-(\d{1,2})-(\d{1,2})',
            r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2}),?\s+(\d{4})',
            r'(\d{1,2})\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})'
        ]
        
        for pattern in date_patterns:
            matches = re.finditer(pattern, content.lower())
            for match in matches:
                try:
                    year = int(match.group(3)) if len(match.groups()) >= 3 else int(match.group(1))
                    if year in recent_years:
                        # Found a recent date, try to parse it
                        parsed = self._parse_announcement_date(match.group(0), reference_date)
                        if parsed:
                            return parsed
                except:
                    continue
        
        return None

    def _parse_funding_amount(self, amount_text: str) -> Optional[float]:
        """Parse funding amount to USD float."""
        if not amount_text:
            return None
            
        # Clean the text
        amount_text = amount_text.lower().replace(',', '').replace('$', '')
        
        # Look for patterns like "5 million", "10M", etc.
        patterns = [
            (r'(\d+(?:\.\d+)?)\s*million', 1000000),
            (r'(\d+(?:\.\d+)?)\s*billion', 1000000000),
            (r'(\d+(?:\.\d+)?)\s*m\b', 1000000),
            (r'(\d+(?:\.\d+)?)\s*b\b', 1000000000),
            (r'(\d+(?:\.\d+)?)', 1)  # Plain number
        ]
        
        for pattern, multiplier in patterns:
            match = re.search(pattern, amount_text)
            if match:
                try:
                    return float(match.group(1)) * multiplier
                except:
                    continue
        
        return None

    def _parse_vc_investment_date(self, date_text: str) -> Optional[str]:
        """Parse VC investment date from text (light parsing for portfolio data)."""
        
        if not date_text:
            return None
            
        date_text = date_text.strip().lower()
        
        # Handle simple year patterns
        year_match = re.search(r'(\d{4})', date_text)
        if year_match:
            year = int(year_match.group(1))
            # Only accept recent years (2020-2025)
            if 2020 <= year <= 2025:
                return f"{year}-01-01"  # Default to January 1st for year-only dates
        
        # Handle quarter patterns (Q1 2024, etc.)
        quarter_match = re.search(r'q([1-4])\s+(\d{4})', date_text)
        if quarter_match:
            quarter = int(quarter_match.group(1))
            year = int(quarter_match.group(2))
            if 2020 <= year <= 2025:
                # Map quarters to months
                quarter_months = {1: '01', 2: '04', 3: '07', 4: '10'}
                return f"{year}-{quarter_months[quarter]}-01"
        
        # Handle month year patterns (january 2024, etc.)
        month_year_match = re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})', date_text)
        if month_year_match:
            month_names = ['january', 'february', 'march', 'april', 'may', 'june',
                          'july', 'august', 'september', 'october', 'november', 'december']
            month_name = month_year_match.group(1)
            year = int(month_year_match.group(2))
            if 2020 <= year <= 2025 and month_name in month_names:
                month_num = month_names.index(month_name) + 1
                return f"{year}-{str(month_num).zfill(2)}-01"
        
        return None

    def _normalize_funding_stage(self, stage_text: str) -> str:
        """Normalize funding stage text."""
        if not stage_text:
            return 'Unknown'
            
        stage_text = stage_text.lower().strip()
        
        # Common mappings
        if any(word in stage_text for word in ['seed', 'pre-seed']):
            return 'Seed'
        elif 'series a' in stage_text or ' a ' in stage_text:
            return 'Series A'
        elif 'series b' in stage_text or ' b ' in stage_text:
            return 'Series B'
        elif 'series c' in stage_text or ' c ' in stage_text:
            return 'Series C'
        elif any(word in stage_text for word in ['debt', 'loan', 'credit']):
            return 'Debt'
        elif any(word in stage_text for word in ['bridge', 'convertible']):
            return 'Bridge'
        
        return stage_text.title()

    def _extract_investor_names(self, investor_text: str) -> List[str]:
        """Extract individual investor names from text."""
        if not investor_text:
            return []
            
        # Split on common separators
        separators = [',', ' and ', ' & ', ';']
        investors = [investor_text]
        
        for sep in separators:
            new_investors = []
            for inv in investors:
                new_investors.extend(inv.split(sep))
            investors = new_investors
        
        # Clean and filter
        cleaned = []
        for inv in investors:
            inv = inv.strip().title()
            if len(inv) > 2 and not inv.lower() in ['the', 'and', 'or', 'also', 'including']:
                cleaned.append(inv)
        
        return cleaned

    def _classify_climate_sector(self, content: str) -> List[str]:
        """Classify climate tech sectors."""
        
        sector_keywords = {
            'Energy Storage': ['battery', 'storage', 'grid', 'lithium'],
            'Solar Energy': ['solar', 'photovoltaic', 'pv'],
            'Carbon Capture': ['carbon capture', 'carbon removal', 'ccus'],
            'Clean Transportation': ['electric vehicle', 'ev', 'mobility', 'transportation'],
            'Green Hydrogen': ['hydrogen', 'electrolysis', 'fuel cell'],
            'Renewable Energy': ['renewable', 'wind', 'geothermal'],
            'Climate Adaptation': ['climate adaptation', 'resilience', 'flooding'],
            'Sustainable Agriculture': ['agriculture', 'farming', 'food tech'],
            'Circular Economy': ['recycling', 'waste', 'circular'],
            'Clean Manufacturing': ['manufacturing', 'industrial', 'cement', 'steel']
        }
        
        detected_sectors = []
        content_lower = content.lower()
        
        for sector, keywords in sector_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                detected_sectors.append(sector)
        
        return detected_sectors

    def _detect_ai_focus(self, content: str) -> bool:
        """Detect if company has AI focus."""
        ai_keywords = ['artificial intelligence', 'machine learning', 'ai', 'ml', 'deep learning', 
                      'neural network', 'algorithm', 'automation', 'predictive']
        return any(keyword in content.lower() for keyword in ai_keywords)

    def _extract_geography(self, content: str) -> str:
        """Extract headquarters country/location."""
        
        # Common patterns
        location_patterns = [
            r'based in ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'headquartered in ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'located in ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, content)
            if match:
                location = match.group(1)
                # Map common locations to countries
                if location in ['California', 'New York', 'Texas', 'Massachusetts']:
                    return 'USA'
                elif location in ['London', 'Manchester']:
                    return 'UK'
                elif location in ['Berlin', 'Munich']:
                    return 'Germany'
                else:
                    return location
        
        # Default fallback
        return 'Unknown'

    # DATABASE UPDATE METHODS
    
    def _update_deal_status(self, deal_id: str, status: str):
        """Update deal status."""
        try:
            self.supabase.table('deals_new').update({
                'status': status,
                'updated_at': datetime.now().isoformat()
            }).eq('id', deal_id).execute()
        except Exception as e:
            print(f"   ⚠️  Failed to update status: {e}")

    def _update_deal_with_ai_data(self, deal_id: str, extracted_data: Dict):
        """Update deal with extracted AI data."""
        
        update_data = {
            'updated_at': datetime.now().isoformat()
        }
        
        # Map extracted data to database columns
        if extracted_data.get('announcement_date'):
            update_data['date_announced'] = extracted_data['announcement_date']
        
        # Handle VC investment dates (from portfolio data)
        if extracted_data.get('investment_date'):
            update_data['date_announced'] = extracted_data['investment_date']
        
        if extracted_data.get('funding_amount_usd'):
            update_data['amount_raised_usd'] = extracted_data['funding_amount_usd']
            
        if extracted_data.get('funding_amount_text'):
            update_data['original_amount'] = extracted_data['funding_amount_text']
            
        if extracted_data.get('funding_stage'):
            update_data['funding_stage'] = extracted_data['funding_stage']
        
        # Update confidence score based on source type
        base_confidence = extracted_data.get('confidence_adjustments', {}).get('base_confidence', 0.8)
        bonuses = sum([v for k, v in extracted_data.get('confidence_adjustments', {}).items() if k != 'base_confidence'])
        update_data['confidence_score'] = min(95, int((base_confidence + bonuses) * 100))
        
        try:
            self.supabase.table('deals_new').update(update_data).eq('id', deal_id).execute()
            print(f"   📊 Updated deal with AI data: {list(update_data.keys())}")
        except Exception as e:
            print(f"   ⚠️  Failed to update deal: {e}")

    def _update_company_name(self, deal: Dict, clean_company_name: str):
        """Update company name with clean extracted name."""
        
        company_id = deal.get('company_id')
        if not company_id:
            return
            
        current_name = deal.get('companies', {}).get('name', '')
        
        # Only update if the current name looks like an article title
        if len(current_name) > 50 or any(word in current_name.lower() for word in ['raises', 'funding', 'million', 'series', '$']):
            try:
                self.supabase.table('companies').update({
                    'name': clean_company_name,
                    'updated_at': datetime.now().isoformat()
                }).eq('id', company_id).execute()
                
                print(f"   🏢 Updated company name: '{current_name}' → '{clean_company_name}'")
            except Exception as e:
                print(f"   ⚠️  Failed to update company name: {e}")

    def _create_enhanced_relationships(self, deal_id: str, extracted_data: Dict):
        """Create investor relationships and other enhanced data."""
        
        investors = extracted_data.get('investors', [])
        if not investors:
            return
        
        print(f"   🤝 Creating relationships for {len(investors)} investors")
        
        for investor_name in investors:
            if not investor_name or len(investor_name.strip()) < 2:
                continue
                
            try:
                # Create investor using V2 RPC
                investor_result = self.supabase.rpc('create_investor_safe_v2', {
                    'investor_name': investor_name.strip(),
                    'investor_type': 'government' if extracted_data.get('source_type') == 'government_research' else 'vc'
                }).execute()
                
                if investor_result.data:
                    # Create relationship
                    self.supabase.table('deal_investors').insert({
                        'deal_id': deal_id,
                        'investor_id': investor_result.data,
                        'role': 'lead' if investor_name == extracted_data.get('lead_investor') else 'participant'
                    }).execute()
                    print(f"   ✅ Created investor relationship: {investor_name}")
                    
            except Exception as e:
                print(f"   ⚠️  Failed to create relationship for {investor_name}: {e}")

    def _clean_company_name(self, raw_name: str) -> str:
        """Clean and extract company name from AI response."""
        if not raw_name:
            return "Unknown Company"
        
        # Remove common prefixes/suffixes that indicate funding news
        clean_name = raw_name.strip()
        
        # Remove funding-related phrases
        funding_phrases = [
            r'\s+raises?\s+\$.*',
            r'\s+secured?\s+\$.*', 
            r'\s+announced?\s+\$.*',
            r'\s+gets?\s+\$.*',
            r'\s+closes?\s+\$.*',
            r'\s+funding.*',
            r'\s+investment.*',
            r'\s+round.*',
            r'\s+series\s+[a-z].*',
            r'.*startup\s+',
            r'.*company\s+',
            r"'s\s+.*",  # Remove possessive and everything after
        ]
        
        for phrase in funding_phrases:
            clean_name = re.sub(phrase, '', clean_name, flags=re.IGNORECASE)
        
        # Extract just the company name (first few words, capitalized)
        words = clean_name.split()
        if len(words) > 0:
            # Take first 1-3 words that look like a company name
            company_words = []
            for word in words[:3]:
                # Stop at common words that indicate end of company name
                if word.lower() in ['is', 'has', 'will', 'the', 'a', 'an', 'and', 'or']:
                    break
                company_words.append(word.strip('.,!?'))
            
            if company_words:
                return ' '.join(company_words)
        
        return "Unknown Company"

# MAIN EXECUTION
def main():
    """Main execution function."""
    
    processor = ConsolidatedAIProcessor(supabase)
    
    print("🚀 CONSOLIDATED AI PROCESSOR FOR CLIMATE TECH")
    print("=" * 60)
    print("This processor handles:")
    print("✅ Government research data (ORNL, DOE, etc.)")
    print("✅ VC portfolio data (Breakthrough Energy, etc.)")  
    print("✅ Traditional news with enhanced date extraction")
    print("✅ Integration with V2 schema adapter")
    print("=" * 60)
    
    # Process all pending deals
    processed = processor.process_all_pending(limit=50)
    
    print(f"\n🎉 Processing complete! Processed {processed} deals.")

if __name__ == "__main__":
    main()
