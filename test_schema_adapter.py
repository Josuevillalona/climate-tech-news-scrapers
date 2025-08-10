#!/usr/bin/env python3

"""
Test the Schema Adapter with RLS Bypass Functions V2
"""

import os
from dotenv import load_dotenv
from supabase import create_client
from schema_adapter import SchemaAwareDealInserter

def test_schema_adapter():
    """Test the schema adapter with V2 RLS bypass functions."""
    
    # Load environment variables
    load_dotenv()
    
    # Initialize Supabase client
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Missing Supabase credentials. Set SUPABASE_URL and SUPABASE_KEY")
        return False
    
    try:
        supabase = create_client(supabase_url, supabase_key)
        inserter = SchemaAwareDealInserter(supabase)
        
        print("🧪 Testing Schema Adapter V2...")
        
        # Test deal insertion
        deal_id = inserter.insert_deal(
            company_name="Test Climate Co V2",
            source_url="https://test.example.com/test-deal-v2",
            raw_text_content="Test climate tech company raised Series A funding for carbon capture technology.",
            source_type="test",
            source_name="Test Source",
            detected_funding_stage="series_a",
            detected_amount="$5M",
            detected_investors=["Test Ventures", "Climate Fund"],
            detected_sector="carbon_capture",
            detected_country="USA",
            has_ai_focus=True
        )
        
        if deal_id:
            print(f"✅ Successfully inserted test deal: {deal_id}")
            print("✅ Schema Adapter V2 is working correctly!")
            return True
        else:
            print("❌ Failed to insert test deal")
            return False
            
    except Exception as e:
        print(f"❌ Schema Adapter test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_schema_adapter()
    exit(0 if success else 1)
