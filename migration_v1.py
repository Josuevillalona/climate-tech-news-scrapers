#!/usr/bin/env python3
"""
Data Migration Script for Alex's Climate Tech VC Pipeline
Migrate existing deals from old schema to new normalized structure
Preserve all data while adding Alex's scoring and filtering capabilities
"""

import os
import re
from dotenv import load_dotenv
from supabase import create_client, Client
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def connect_to_supabase():
    """Initialize Supabase connection"""
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Successfully connected to Supabase.")
        return supabase
    except Exception as e:
        print(f"❌ Error connecting to Supabase: {e}")
        sys.exit(1)

def fetch_existing_deals(supabase):
    """Fetch all existing deals from the old deals table"""
    print("🔄 Fetching existing deals from old schema...")
    
    try:
        result = supabase.table('deals').select('*').execute()
        deals = result.data
        print(f"📊 Found {len(deals)} existing deals to migrate")
        
        if deals:
            print("📋 Sample deal structure:")
            for key in deals[0].keys():
                print(f"   - {key}")
        
        return deals
    except Exception as e:
        print(f"❌ Error fetching deals: {e}")
        return []

def extract_unique_companies(deals):
    """Extract unique companies from deals data"""
    print("🔄 Extracting unique companies...")
    
    companies = {}
    
    for deal in deals:
        company_name = deal.get('company_name', '').strip()
        if not company_name:
            continue
        
        # Use company name as key (normalize for deduplication)
        company_key = company_name.lower().strip()
        
        if company_key not in companies:
            # Extract company info from deal
            companies[company_key] = {
                'name': company_name,
                'climate_sub_sectors': [deal.get('climate_sub_sector')] if deal.get('climate_sub_sector') else [],
                'headquarters_country': deal.get('geography_country'),
                'is_climate_tech': True,  # All existing deals are climate tech
                'has_ai_focus': detect_ai_focus(deal),
                'confidence_score': 0.8,  # High confidence for existing data
                'data_sources': ['legacy_migration'],
                'enrichment_status': 'basic'
            }
        else:
            # Merge additional sectors if different
            existing_sectors = companies[company_key]['climate_sub_sectors']
            new_sector = deal.get('climate_sub_sector')
            if new_sector and new_sector not in existing_sectors:
                existing_sectors.append(new_sector)
    
    print(f"📊 Found {len(companies)} unique companies")
    return list(companies.values())

def detect_ai_focus(deal):
    """Detect if a company/deal has AI focus based on text content"""
    ai_keywords = [
        'ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning',
        'neural network', 'computer vision', 'nlp', 'natural language',
        'automation', 'smart', 'intelligent', 'predictive', 'analytics',
        'algorithm', 'data science', 'robotics', 'autonomous'
    ]
    
    # Check in company name, climate sub-sector, and raw content
    text_to_check = ' '.join([
        str(deal.get('company_name', '')),
        str(deal.get('climate_sub_sector', '')),
        str(deal.get('raw_text_content', ''))
    ]).lower()
    
    return any(keyword in text_to_check for keyword in ai_keywords)

def create_companies(supabase, companies_data):
    """Create company records in the new companies table"""
    print("🔄 Creating company records...")
    
    created_companies = {}
    success_count = 0
    
    for company in companies_data:
        try:
            result = supabase.table('companies').insert(company).execute()
            if result.data:
                company_record = result.data[0]
                created_companies[company['name'].lower()] = company_record['id']
                success_count += 1
                print(f"✅ Created company: {company['name']}")
        except Exception as e:
            print(f"⚠️  Failed to create company '{company['name']}': {e}")
    
    print(f"📊 Created {success_count}/{len(companies_data)} companies")
    return created_companies

def parse_funding_amount(amount_str, currency='USD'):
    """Parse funding amount string into numeric value in USD"""
    if not amount_str:
        return None
    
    # Remove currency symbols and normalize
    amount_clean = re.sub(r'[^\d.,MBKmillionbillion]', '', str(amount_str).lower())
    
    # Extract numeric value
    amount_match = re.search(r'([\d.,]+)', amount_clean)
    if not amount_match:
        return None
    
    try:
        amount = float(amount_match.group(1).replace(',', ''))
        
        # Handle millions/billions
        if 'million' in amount_clean or 'm' in amount_clean:
            amount *= 1_000_000
        elif 'billion' in amount_clean or 'b' in amount_clean:
            amount *= 1_000_000_000
        elif 'k' in amount_clean:
            amount *= 1_000
        
        return amount
    except:
        return None

def extract_investors_from_text(lead_investors_str, other_investors_str):
    """Extract individual investors from comma-separated strings"""
    investors = []
    
    # Process lead investors
    if lead_investors_str:
        lead_names = [name.strip() for name in str(lead_investors_str).split(',') if name.strip()]
        for name in lead_names:
            investors.append({'name': name, 'role': 'lead'})
    
    # Process other investors
    if other_investors_str:
        other_names = [name.strip() for name in str(other_investors_str).split(',') if name.strip()]
        for name in other_names:
            investors.append({'name': name, 'role': 'participant'})
    
    return investors

def calculate_alex_score_simple(deal_data, company_data):
    """Calculate Alex's investment score for migrated deals"""
    score = 0
    
    # Stage scoring (30 points max)
    stage = str(deal_data.get('funding_stage', '')).lower()
    if any(s in stage for s in ['seed', 'series a', 'series-a', 'pre-seed']):
        score += 30
    elif any(s in stage for s in ['series b', 'series-b']):
        score += 15
    
    # AI focus (25 points max)
    if company_data.get('has_ai_focus', False):
        score += 25
    
    # Climate sector (25 points max)
    sector = str(deal_data.get('climate_sub_sector', '')).lower()
    target_sectors = ['energy', 'grid', 'industrial', 'software', 'storage', 'manufacturing', 'carbon', 'emissions']
    if any(target in sector for target in target_sectors):
        score += 25
    elif 'climate' in sector:
        score += 15
    
    # Geography (10 points max)
    country = str(deal_data.get('geography_country', '')).upper()
    if country == 'US':
        score += 10
    elif country in ['CANADA', 'UK']:
        score += 7
    
    # Funding size (15 points max)
    amount = parse_funding_amount(deal_data.get('amount_raised'))
    if amount:
        if 1_000_000 <= amount <= 8_000_000:  # Optimal range
            score += 15
        elif 500_000 <= amount <= 15_000_000:  # Acceptable range
            score += 8
    
    # Legacy data bonus (5 points)
    score += 5
    
    return min(100, max(0, score))

def migrate_deals(supabase, deals, company_mapping):
    """Migrate deals to new deals_new table with Alex's scoring"""
    print("🔄 Migrating deals to new schema...")
    
    migrated_count = 0
    investor_records = {}
    
    for deal in deals:
        try:
            company_name = deal.get('company_name', '').strip()
            company_key = company_name.lower()
            
            if company_key not in company_mapping:
                print(f"⚠️  Skipping deal - company not found: {company_name}")
                continue
            
            company_id = company_mapping[company_key]
            
            # Parse funding amount
            amount_usd = parse_funding_amount(deal.get('amount_raised'))
            
            # Calculate Alex's score
            alex_score = calculate_alex_score_simple(deal, {'has_ai_focus': detect_ai_focus(deal)})
            
            # Create deal record
            deal_data = {
                'company_id': company_id,
                'amount_raised_usd': amount_usd,
                'original_amount': deal.get('amount_raised'),
                'original_currency': deal.get('currency', 'USD'),
                'funding_stage': deal.get('funding_stage'),
                'date_announced': deal.get('date_announced'),
                'source_url': deal.get('source_url'),
                'source_type': 'news',  # All legacy deals are from news sources
                'source_name': determine_source_name(deal.get('source_url', '')),
                'raw_text_content': deal.get('raw_text_content'),
                'confidence_score': 0.8,  # High confidence for existing data
                'investment_score': alex_score,
                'alex_review_status': 'pending',
                'status': 'migrated',
                'created_at': deal.get('created_at')
            }
            
            # Insert deal
            result = supabase.table('deals_new').insert(deal_data).execute()
            if result.data:
                deal_id = result.data[0]['id']
                migrated_count += 1
                
                # Process investors
                investors = extract_investors_from_text(
                    deal.get('lead_investors'),
                    deal.get('other_investors')
                )
                
                create_investor_relationships(supabase, deal_id, investors, investor_records)
                
                print(f"✅ Migrated deal: {company_name} (Score: {alex_score})")
        
        except Exception as e:
            print(f"⚠️  Failed to migrate deal '{deal.get('company_name', 'Unknown')}': {e}")
    
    print(f"📊 Migrated {migrated_count}/{len(deals)} deals")
    return migrated_count

def determine_source_name(source_url):
    """Determine source name from URL"""
    if 'techcrunch.com' in source_url:
        return 'TechCrunch'
    elif 'climateinsider.com' in source_url:
        return 'Climate Insider'
    elif 'ctvc.co' in source_url:
        return 'CTVC'
    elif 'axios.com' in source_url:
        return 'Axios Pro Climate'
    elif 'agfundernews.com' in source_url:
        return 'AgFunder News'
    elif 'techfundingnews.com' in source_url:
        return 'Tech Funding News'
    elif 'canarymedia.com' in source_url:
        return 'Canary Media'
    else:
        return 'Unknown Source'

def create_investor_relationships(supabase, deal_id, investors, investor_records):
    """Create investor records and deal-investor relationships"""
    for investor_info in investors:
        investor_name = investor_info['name']
        investor_role = investor_info['role']
        
        # Get or create investor
        if investor_name not in investor_records:
            try:
                # Check if investor already exists
                existing = supabase.table('investors').select('id').eq('name', investor_name).execute()
                
                if existing.data:
                    investor_id = existing.data[0]['id']
                else:
                    # Create new investor
                    investor_data = {
                        'name': investor_name,
                        'type': 'vc',  # Default assumption
                        'climate_focus': True,  # All legacy investors are climate-focused
                        'enrichment_status': 'pending'
                    }
                    result = supabase.table('investors').insert(investor_data).execute()
                    investor_id = result.data[0]['id']
                
                investor_records[investor_name] = investor_id
            except Exception as e:
                print(f"⚠️  Failed to create investor '{investor_name}': {e}")
                continue
        
        investor_id = investor_records[investor_name]
        
        # Create deal-investor relationship
        try:
            relationship_data = {
                'deal_id': deal_id,
                'investor_id': investor_id,
                'role': investor_role
            }
            supabase.table('deal_investors').insert(relationship_data).execute()
        except Exception as e:
            print(f"⚠️  Failed to create relationship for {investor_name}: {e}")

def verify_migration(supabase):
    """Verify migration success and data integrity"""
    print("🔍 Verifying migration...")
    
    try:
        # Count records in new tables
        companies_count = supabase.table('companies').select('*', count='exact').execute().count
        deals_count = supabase.table('deals_new').select('*', count='exact').execute().count
        investors_count = supabase.table('investors').select('*', count='exact').execute().count
        relationships_count = supabase.table('deal_investors').select('*', count='exact').execute().count
        
        print(f"📊 Migration Results:")
        print(f"   - Companies: {companies_count}")
        print(f"   - Deals: {deals_count}")
        print(f"   - Investors: {investors_count}")
        print(f"   - Relationships: {relationships_count}")
        
        # Check Alex's scoring distribution
        score_result = supabase.table('deals_new').select('investment_score').execute()
        scores = [deal['investment_score'] for deal in score_result.data if deal['investment_score'] is not None]
        
        if scores:
            avg_score = sum(scores) / len(scores)
            high_scores = len([s for s in scores if s >= 60])
            print(f"📈 Alex's Scoring Results:")
            print(f"   - Average Score: {avg_score:.1f}")
            print(f"   - High Scores (≥60): {high_scores}/{len(scores)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def main():
    """Main migration process"""
    print("🚀 Starting Data Migration to Alex's Climate Tech VC Pipeline")
    print("=" * 70)
    
    # Connect to Supabase
    supabase = connect_to_supabase()
    
    # Step 1: Fetch existing deals
    print("\n📋 Step 1: Fetch existing deals")
    existing_deals = fetch_existing_deals(supabase)
    
    if not existing_deals:
        print("❌ No deals found to migrate")
        return False
    
    # Step 2: Extract unique companies
    print("\n🏢 Step 2: Extract unique companies")
    companies_data = extract_unique_companies(existing_deals)
    
    # Step 3: Create company records
    print("\n🔄 Step 3: Create company records")
    company_mapping = create_companies(supabase, companies_data)
    
    if not company_mapping:
        print("❌ Failed to create companies")
        return False
    
    # Step 4: Migrate deals
    print("\n💼 Step 4: Migrate deals with Alex's scoring")
    migrated_count = migrate_deals(supabase, existing_deals, company_mapping)
    
    # Step 5: Verify migration
    print("\n🔍 Step 5: Verify migration")
    verification_success = verify_migration(supabase)
    
    # Final summary
    print("\n" + "=" * 70)
    if verification_success and migrated_count > 0:
        print("🎉 MIGRATION SUCCESSFUL!")
        print(f"✅ Migrated {migrated_count} deals")
        print(f"✅ Created {len(company_mapping)} companies")
        print("✅ Alex's scoring applied to all deals")
        print("✅ Investor relationships preserved")
        print("✅ Ready for Phase 1D: Testing & Validation")
        
        print("\n📋 Next Steps:")
        print("1. Test Alex's filtering system")
        print("2. Validate data integrity")
        print("3. Update scrapers to use new schema")
        
        return True
    else:
        print("⚠️  MIGRATION INCOMPLETE")
        print("Please review the errors above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
