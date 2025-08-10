#!/usr/bin/env python3
"""
Test AI Processing with Schema Updates
Process sample entries and update them with AI-extracted data
"""

import os
from dotenv import load_dotenv
from supabase import create_client
from enhanced_ai_processor import EnhancedAIProcessor
from schema_adapter import SchemaAwareDealInserter

def test_ai_with_schema_update():
    load_dotenv()
    url = os.getenv('SUPABASE_URL').strip(' "')
    key = os.getenv('SUPABASE_KEY').strip(' "')
    supabase = create_client(url, key)
    
    # Initialize processors
    ai_processor = EnhancedAIProcessor()
    schema_inserter = SchemaAwareDealInserter(supabase)
    
    print('🧪 Testing AI Processing with Schema Updates...')
    print('=' * 60)

    # Get samples
    gov_result = supabase.table('deals_new').select('*').eq('source_type', 'government_research').limit(1).execute()
    vc_result = supabase.table('deals_new').select('*').eq('source_type', 'vc_portfolio').limit(1).execute()

    if not gov_result.data or not vc_result.data:
        print("❌ Could not find sample data")
        return

    # Process Government Research Entry
    print('📋 PROCESSING GOVERNMENT RESEARCH WITH AI + SCHEMA')
    print('-' * 50)
    gov_entry = gov_result.data[0]
    
    # AI Analysis
    gov_analysis = ai_processor.process_by_source_type(
        content=gov_entry["raw_text_content"],
        source_type=gov_entry["source_type"], 
        source_url=gov_entry["source_url"]
    )
    
    # Get company info (we need company name from companies table)
    company_result = supabase.table('companies').select('name').eq('id', gov_entry['company_id']).execute()
    company_name = company_result.data[0]['name'] if company_result.data else 'Unknown Company'
    
    print(f'Company: {company_name}')
    print(f'AI Detected Investors: {gov_analysis.get("investors", [])}')
    print(f'AI Funding Stage: {gov_analysis.get("funding_stage", "Unknown")}')
    print(f'Climate Sectors: {gov_analysis.get("climate_sectors", [])}')
    
    # Test inserting with AI-enhanced data
    try:
        deal_id = schema_inserter.insert_deal(
            company_name=f"{company_name} (AI Enhanced)",
            source_url=gov_entry["source_url"] + "?ai_enhanced=true",
            raw_text_content=f"AI ENHANCED: {gov_entry['raw_text_content']}",
            source_type="government_research_ai",
            source_name=f"{gov_entry['source_name']} (AI)",
            detected_funding_stage=gov_analysis.get("funding_stage"),
            detected_amount=None,  # Government research typically doesn't have funding amounts
            detected_investors=gov_analysis.get("investors", []),
            detected_sector=", ".join(gov_analysis.get("climate_sectors", [])),
            detected_country="USA",  # Most gov research is US-based
            has_ai_focus=gov_analysis.get("has_ai_focus", False)
        )
        
        if deal_id:
            print(f'✅ Successfully created AI-enhanced government deal: {deal_id}')
        else:
            print('❌ Failed to create AI-enhanced government deal')
            
    except Exception as e:
        print(f'❌ Government processing failed: {e}')
    
    print()
    
    # Process VC Portfolio Entry
    print('💼 PROCESSING VC PORTFOLIO WITH AI + SCHEMA')
    print('-' * 50)
    vc_entry = vc_result.data[0]
    
    # AI Analysis
    vc_analysis = ai_processor.process_by_source_type(
        content=vc_entry["raw_text_content"],
        source_type=vc_entry["source_type"],
        source_url=vc_entry["source_url"]
    )
    
    # Get company info
    company_result = supabase.table('companies').select('name').eq('id', vc_entry['company_id']).execute()
    company_name = company_result.data[0]['name'] if company_result.data else 'Unknown Company'
    
    print(f'Company: {company_name}')
    print(f'AI Detected Investors: {vc_analysis.get("investors", [])}')
    print(f'AI Funding Stage: {vc_analysis.get("funding_stage", "Unknown")}')
    print(f'Lead Investor: {vc_analysis.get("lead_investor", "Unknown")}')
    
    # Test inserting with AI-enhanced data
    try:
        deal_id = schema_inserter.insert_deal(
            company_name=f"{company_name} (AI Enhanced)",
            source_url=vc_entry["source_url"] + "?ai_enhanced=true",
            raw_text_content=f"AI ENHANCED: {vc_entry['raw_text_content']}",
            source_type="vc_portfolio_ai",
            source_name=f"{vc_entry['source_name']} (AI)",
            detected_funding_stage=vc_analysis.get("funding_stage"),
            detected_amount=None,  # VC portfolio data typically doesn't include amounts
            detected_investors=vc_analysis.get("investors", []),
            detected_sector=", ".join(vc_analysis.get("climate_sectors", [])),
            detected_country="USA",
            has_ai_focus=vc_analysis.get("has_ai_focus", False)
        )
        
        if deal_id:
            print(f'✅ Successfully created AI-enhanced VC deal: {deal_id}')
        else:
            print('❌ Failed to create AI-enhanced VC deal')
            
    except Exception as e:
        print(f'❌ VC processing failed: {e}')

    print()
    print('=' * 60)
    print('🎉 AI + Schema Processing Test Complete!')
    print('Check your Supabase database for the new AI-enhanced entries')

if __name__ == "__main__":
    test_ai_with_schema_update()
