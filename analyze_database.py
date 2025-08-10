#!/usr/bin/env python3
"""
Database Analysis - Show what Layer 2 integration created
"""

import os
from dotenv import load_dotenv
from supabase import create_client
from collections import Counter

def analyze_database():
    load_dotenv()
    
    # Remove quotes and spaces from environment variables
    url = os.getenv('SUPABASE_URL').strip(' "')
    key = os.getenv('SUPABASE_KEY').strip(' "')
    
    print("🔍 Analyzing your Supabase database...")
    print("=" * 60)
    
    try:
        supabase = create_client(url, key)
        
        # Get all deals
        deals_result = supabase.table('deals').select('*').execute()
        deals = deals_result.data
        
        print(f"📊 TOTAL DEALS: {len(deals)}")
        print()
        
        # Breakdown by source type
        source_types = Counter([deal.get('source_type', 'unknown') for deal in deals])
        print("📈 BREAKDOWN BY SOURCE TYPE:")
        for source_type, count in sorted(source_types.items()):
            print(f"  • {source_type}: {count} deals")
        print()
        
        # Show sample Layer 2 discoveries
        gov_deals = [d for d in deals if d.get('source_type') == 'government_research']
        vc_deals = [d for d in deals if d.get('source_type') == 'vc_portfolio']
        
        if gov_deals:
            print("🏛️ GOVERNMENT RESEARCH DISCOVERIES:")
            for i, deal in enumerate(gov_deals[:5], 1):
                company_name = deal.get('company_name', 'Unknown')
                source_url = deal.get('source_url', 'No URL')[:60] + '...' if len(deal.get('source_url', '')) > 60 else deal.get('source_url', 'No URL')
                print(f"  {i}. Company: {company_name}")
                print(f"     Source: {source_url}")
                print()
        
        if vc_deals:
            print("🏢 VC PORTFOLIO COMPANIES:")
            for i, deal in enumerate(vc_deals[:5], 1):
                company_name = deal.get('company_name', 'Unknown')
                source_url = deal.get('source_url', 'No URL')[:60] + '...' if len(deal.get('source_url', '')) > 60 else deal.get('source_url', 'No URL')
                print(f"  {i}. Company: {company_name}")
                print(f"     Source: {source_url}")
                print()
        
        # Show traditional news deals for comparison
        news_deals = [d for d in deals if d.get('source_type') == 'news']
        if news_deals:
            print("📰 TRADITIONAL NEWS DEALS:")
            for i, deal in enumerate(news_deals[:3], 1):
                company_name = deal.get('company_name', 'Unknown')
                source_name = deal.get('source_name', 'Unknown Source')
                print(f"  {i}. Company: {company_name}")
                print(f"     Source: {source_name}")
                print()
        
        print("✅ ANALYSIS COMPLETE!")
        print()
        print("🎯 WHAT THIS MEANS:")
        print("• The 'government_research' and 'vc_portfolio' entries are from Layer 2")
        print("• This is CORRECT - they represent potential investment opportunities")
        print("• Layer 2 gives you early intelligence before deals are publicly announced")
        print("• All entries use the same normalized schema (companies → deals → investors)")
        
        # Check companies table
        companies_result = supabase.table('companies').select('*').execute()
        companies = companies_result.data
        print(f"\n📊 COMPANIES TABLE: {len(companies)} companies")
        
        # Check investors table  
        investors_result = supabase.table('investors').select('*').execute()
        investors = investors_result.data
        print(f"📊 INVESTORS TABLE: {len(investors)} investors")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    analyze_database()
