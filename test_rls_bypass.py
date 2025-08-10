#!/usr/bin/env python3
"""
Test the Schema Adapter with RLS Bypass Functions
This script verifies that the schema_adapter.py works correctly
after deploying the RLS bypass functions.
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def test_rls_bypass_functions():
    """Test that RLS bypass functions work correctly."""
    
    print("🔧 Testing RLS Bypass Functions...")
    
    try:
        # Connect to Supabase
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            print("❌ Missing SUPABASE_URL or SUPABASE_KEY environment variables")
            return False
        
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Connected to Supabase")
        
        # Test 1: RPC function availability
        print("\n📡 Testing RPC function availability...")
        
        # Test create_company_safe
        test_company_id = supabase.rpc('create_company_safe', {
            'company_name': 'RLS Test Company',
            'country': 'United States',
            'sector': 'Clean Energy',
            'ai_focus': True
        }).execute()
        
        if test_company_id.data:
            print(f"✅ create_company_safe works - Created company ID: {test_company_id.data}")
        else:
            print("❌ create_company_safe failed")
            return False
        
        # Test create_deal_safe
        test_deal_id = supabase.rpc('create_deal_safe', {
            'company_id': test_company_id.data,
            'source_url': 'https://test-rls.com/test-deal',
            'raw_content': 'Test deal for RLS bypass verification',
            'funding_stage': 'seed',
            'amount_usd': 2000000,
            'original_amount': '$2M',
            'source_type': 'test',
            'source_name': 'RLS Test Source'
        }).execute()
        
        if test_deal_id.data:
            print(f"✅ create_deal_safe works - Created deal ID: {test_deal_id.data}")
        else:
            print("❌ create_deal_safe failed")
            return False
        
        # Test create_investor_safe
        test_investor_id = supabase.rpc('create_investor_safe', {
            'investor_name': 'RLS Test VC',
            'investor_type': 'vc'
        }).execute()
        
        if test_investor_id.data:
            print(f"✅ create_investor_safe works - Created investor ID: {test_investor_id.data}")
        else:
            print("❌ create_investor_safe failed")
            return False
        
        # Test 2: Schema Adapter Integration
        print("\n🔄 Testing Schema Adapter Integration...")
        
        try:
            from schema_adapter import SchemaAwareDealInserter
            inserter = SchemaAwareDealInserter(supabase)
            print("✅ Schema adapter imported successfully")
            
            # Test deal insertion through schema adapter
            deal_id = inserter.insert_deal(
                company_name="Schema Adapter Test Co",
                source_url="https://test.com/schema-adapter-test",
                raw_text_content="Testing schema adapter with RLS bypass functions",
                source_type='test',
                detected_funding_stage='series-a',
                detected_amount='$5M',
                detected_investors=['Test Investor 1', 'Test Investor 2'],
                detected_sector='Climate Tech',
                detected_country='United States',
                has_ai_focus=True
            )
            
            if deal_id:
                print(f"✅ Schema adapter deal insertion works - Deal ID: {deal_id}")
            else:
                print("❌ Schema adapter deal insertion failed")
                return False
                
        except ImportError as e:
            print(f"❌ Failed to import schema_adapter: {e}")
            return False
        
        # Test 3: Data Verification
        print("\n📊 Verifying data was created correctly...")
        
        # Check companies table
        companies = supabase.table('companies').select('*').execute()
        print(f"✅ Companies table accessible - {len(companies.data)} companies found")
        
        # Check deals table
        deals = supabase.table('deals').select('*').execute()
        print(f"✅ Deals table accessible - {len(deals.data)} deals found")
        
        # Check investors table
        investors = supabase.table('investors').select('*').execute()
        print(f"✅ Investors table accessible - {len(investors.data)} investors found")
        
        # Clean up test data
        print("\n🧹 Cleaning up test data...")
        
        # Delete test data (in reverse order due to foreign key constraints)
        supabase.table('deals').delete().eq('source_type', 'test').execute()
        supabase.table('investors').delete().like('name', '%Test%').execute()
        supabase.table('companies').delete().like('name', '%Test%').execute()
        
        print("✅ Test data cleaned up")
        
        print("\n🎉 All tests passed! RLS bypass functions are working correctly.")
        print("✨ Your schema_adapter.py is ready for production use!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def test_table_structure():
    """Verify that all required tables exist with correct structure."""
    
    print("\n📋 Verifying table structure...")
    
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        supabase: Client = create_client(supabase_url, supabase_key)
        
        required_tables = ['companies', 'deals', 'investors', 'deal_investors', 
                          'alex_filter_settings', 'alex_deal_views']
        
        for table in required_tables:
            try:
                result = supabase.table(table).select('*').limit(1).execute()
                print(f"✅ {table} table exists and accessible")
            except Exception as e:
                print(f"❌ {table} table issue: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Table structure verification failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Schema Adapter RLS Bypass Function Test")
    print("=" * 50)
    
    # Test table structure first
    if not test_table_structure():
        print("\n❌ Table structure verification failed. Please run schema deployment first.")
        sys.exit(1)
    
    # Test RLS bypass functions
    if test_rls_bypass_functions():
        print("\n🎯 Ready for Layer 2 integration!")
        print("🔄 You can now run your updated scrapers with confidence")
        sys.exit(0)
    else:
        print("\n❌ RLS bypass function test failed")
        print("📋 Next steps:")
        print("1. Make sure you ran step7_rls_bypass_functions.sql in Supabase SQL Editor")
        print("2. Check your Supabase connection credentials")
        print("3. Verify RLS policies are configured correctly")
        sys.exit(1)
