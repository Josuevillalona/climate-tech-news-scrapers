#!/usr/bin/env python3
"""
Get sample data for AI processing testing
"""

import os
from dotenv import load_dotenv
from supabase import create_client

def get_sample_data():
    load_dotenv()
    url = os.getenv('SUPABASE_URL').strip(' "')
    key = os.getenv('SUPABASE_KEY').strip(' "')
    supabase = create_client(url, key)

    print('🔍 Getting sample data for AI testing...')
    print('=' * 50)

    # Get one government research entry
    gov_result = supabase.table('deals_new').select('*').eq('source_type', 'government_research').limit(1).execute()
    if gov_result.data:
        gov_entry = gov_result.data[0]
        print('📋 GOVERNMENT RESEARCH SAMPLE:')
        print(f'ID: {gov_entry["id"]}')
        print(f'Company: {gov_entry["company_name"]}')
        print(f'URL: {gov_entry["source_url"]}')
        print(f'Content: {gov_entry["raw_text_content"][:200]}...')
        print()

    # Get one VC portfolio entry  
    vc_result = supabase.table('deals_new').select('*').eq('source_type', 'vc_portfolio').limit(1).execute()
    if vc_result.data:
        vc_entry = vc_result.data[0]
        print('💼 VC PORTFOLIO SAMPLE:')
        print(f'ID: {vc_entry["id"]}')
        print(f'Company: {vc_entry["company_name"]}')
        print(f'URL: {vc_entry["source_url"]}')
        print(f'Content: {vc_entry["raw_text_content"][:200]}...')
        print()

    return (gov_result.data[0] if gov_result.data else None, 
            vc_result.data[0] if vc_result.data else None)

if __name__ == "__main__":
    get_sample_data()
