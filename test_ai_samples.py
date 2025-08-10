#!/usr/bin/env python3
"""
Test Enhanced AI Processing on Sample Data
Tests one government research and one VC portfolio entry
"""

import os
from dotenv import load_dotenv
from supabase import create_client
from enhanced_ai_processor import EnhancedAIProcessor

def test_ai_processing():
    load_dotenv()
    url = os.getenv('SUPABASE_URL').strip(' "')
    key = os.getenv('SUPABASE_KEY').strip(' "')
    supabase = create_client(url, key)
    
    # Initialize AI processor
    processor = EnhancedAIProcessor()
    
    print('🧪 Testing Enhanced AI Processing...')
    print('=' * 60)

    # Get samples
    gov_result = supabase.table('deals_new').select('*').eq('source_type', 'government_research').limit(1).execute()
    vc_result = supabase.table('deals_new').select('*').eq('source_type', 'vc_portfolio').limit(1).execute()

    if not gov_result.data or not vc_result.data:
        print("❌ Could not find sample data")
        return

    # Test Government Research Processing
    print('📋 TESTING GOVERNMENT RESEARCH PROCESSING')
    print('-' * 40)
    gov_entry = gov_result.data[0]
    print(f'Entry ID: {gov_entry["id"]}')
    print(f'Source: {gov_entry["source_name"]} ({gov_entry["source_type"]})')
    print(f'Content Preview: {gov_entry["raw_text_content"][:150]}...')
    print()
    
    try:
        gov_analysis = processor.process_by_source_type(
            content=gov_entry["raw_text_content"],
            source_type=gov_entry["source_type"], 
            source_url=gov_entry["source_url"]
        )
        
        print('✅ GOVERNMENT RESEARCH ANALYSIS:')
        for key, value in gov_analysis.items():
            print(f'  {key}: {value}')
        print()
        
    except Exception as e:
        print(f'❌ Government processing failed: {e}')
        print()

    # Test VC Portfolio Processing  
    print('💼 TESTING VC PORTFOLIO PROCESSING')
    print('-' * 40)
    vc_entry = vc_result.data[0]
    print(f'Entry ID: {vc_entry["id"]}')
    print(f'Source: {vc_entry["source_name"]} ({vc_entry["source_type"]})')
    print(f'Content Preview: {vc_entry["raw_text_content"][:150]}...')
    print()
    
    try:
        vc_analysis = processor.process_by_source_type(
            content=vc_entry["raw_text_content"],
            source_type=vc_entry["source_type"],
            source_url=vc_entry["source_url"]
        )
        
        print('✅ VC PORTFOLIO ANALYSIS:')
        for key, value in vc_analysis.items():
            print(f'  {key}: {value}')
        print()
        
    except Exception as e:
        print(f'❌ VC processing failed: {e}')
        print()

    print('=' * 60)
    print('🎯 AI Processing Test Complete!')

if __name__ == "__main__":
    test_ai_processing()
