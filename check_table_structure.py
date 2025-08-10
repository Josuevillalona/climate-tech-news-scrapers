#!/usr/bin/env python3
"""
Check deals_new table structure and get sample data
"""

import os
from dotenv import load_dotenv
from supabase import create_client

def check_table_structure():
    load_dotenv()
    url = os.getenv('SUPABASE_URL').strip(' "')
    key = os.getenv('SUPABASE_KEY').strip(' "')
    supabase = create_client(url, key)

    print('🔍 Checking deals_new table structure...')
    print('=' * 50)

    # Get one record to see all columns
    result = supabase.table('deals_new').select('*').limit(1).execute()
    if result.data:
        entry = result.data[0]
        print('📋 DEALS_NEW COLUMNS:')
        for key, value in entry.items():
            print(f'  {key}: {str(value)[:100]}{"..." if len(str(value)) > 100 else ""}')
        print()

    # Get samples by source type
    print('🔍 Getting samples by source type...')
    print('=' * 50)

    # Government research
    gov_result = supabase.table('deals_new').select('*').eq('source_type', 'government_research').limit(1).execute()
    if gov_result.data:
        gov_entry = gov_result.data[0]
        print('📋 GOVERNMENT RESEARCH SAMPLE:')
        print(f'ID: {gov_entry["id"]}')
        print(f'Source URL: {gov_entry.get("source_url", "N/A")}')
        print(f'Content: {str(gov_entry.get("raw_text_content", ""))[:200]}...')
        print()

    # VC portfolio  
    vc_result = supabase.table('deals_new').select('*').eq('source_type', 'vc_portfolio').limit(1).execute()
    if vc_result.data:
        vc_entry = vc_result.data[0]
        print('💼 VC PORTFOLIO SAMPLE:')
        print(f'ID: {vc_entry["id"]}')
        print(f'Source URL: {vc_entry.get("source_url", "N/A")}')
        print(f'Content: {str(vc_entry.get("raw_text_content", ""))[:200]}...')

if __name__ == "__main__":
    check_table_structure()
