#!/usr/bin/env python3
"""
Check deals_new table for Layer 2 data
"""

import os
from dotenv import load_dotenv
from supabase import create_client
from collections import Counter

def main():
    load_dotenv()
    url = os.getenv('SUPABASE_URL').strip(' "')
    key = os.getenv('SUPABASE_KEY').strip(' "')
    
    supabase = create_client(url, key)
    
    print('🔍 Checking DEALS_NEW table (the correct Layer 2 table)...')
    print('=' * 60)
    
    try:
        # Check deals_new table
        deals_new = supabase.table('deals_new').select('*').execute()
        print(f'📊 DEALS_NEW TABLE: {len(deals_new.data)} records')
        
        if deals_new.data:
            # Count by source type
            source_types = Counter([deal.get('source_type', 'unknown') for deal in deals_new.data])
            print('📈 SOURCE TYPES in deals_new:')
            for source_type, count in sorted(source_types.items()):
                print(f'  • {source_type}: {count} deals')
            print()
            
            # Show government research samples
            gov_deals = [d for d in deals_new.data if d.get('source_type') == 'government_research']
            if gov_deals:
                print('🏛️ GOVERNMENT RESEARCH (ORNL, NREL, DOE):')
                for i, deal in enumerate(gov_deals[:3], 1):
                    source_url = deal.get('source_url', 'No URL')
                    print(f'  {i}. Source: {source_url[:80]}...')
                print()
            
            # Show VC portfolio samples
            vc_deals = [d for d in deals_new.data if d.get('source_type') == 'vc_portfolio']
            if vc_deals:
                print('🏢 VC PORTFOLIO (Breakthrough Energy):')
                for i, deal in enumerate(vc_deals[:3], 1):
                    source_url = deal.get('source_url', 'No URL')
                    print(f'  {i}. Source: {source_url[:80]}...')
                print()
            
            print('✅ This is the CORRECT table with Layer 2 data!')
            
    except Exception as e:
        print(f'❌ Error accessing deals_new: {e}')
    
    # Also check the old deals table for comparison
    try:
        deals_old = supabase.table('deals').select('*').execute()
        print(f'📊 OLD DEALS TABLE: {len(deals_old.data)} records (legacy data)')
    except Exception as e:
        print(f'❌ Error accessing deals: {e}')

if __name__ == '__main__':
    main()
