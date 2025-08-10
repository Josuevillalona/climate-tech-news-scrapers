#!/usr/bin/env python3
"""
Setup Default Data for Alex's Climate Tech VC Pipeline
Insert Alex's filter settings, deal views, and data sources
Run this AFTER creating the schema in Supabase
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
import sys

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

def setup_alex_filter_settings(supabase):
    """Insert Alex's default filter settings"""
    print("🔄 Setting up Alex's filter settings...")
    
    filter_settings = [
        {
            'setting_name': 'stage_filter',
            'is_enabled': True,
            'filter_values': {
                "enabled": True,
                "allowed_stages": ["seed", "series a", "series-a", "pre-seed"],
                "strict_mode": False
            }
        },
        {
            'setting_name': 'ai_filter',
            'is_enabled': True,
            'filter_values': {
                "enabled": True,
                "require_ai": True,
                "strict_mode": False
            }
        },
        {
            'setting_name': 'sector_filter',
            'is_enabled': True,
            'filter_values': {
                "enabled": True,
                "target_sectors": [
                    "Climate Tech - Energy & Grid",
                    "Climate Tech - Industrial Software", 
                    "Climate Tech - Energy Storage",
                    "Climate Tech - Smart Manufacturing",
                    "Climate Tech - Carbon & Emissions"
                ],
                "strict_mode": False
            }
        },
        {
            'setting_name': 'geography_filter',
            'is_enabled': True,
            'filter_values': {
                "enabled": True,
                "preferred_countries": ["US", "Canada", "UK"],
                "strict_mode": False
            }
        },
        {
            'setting_name': 'funding_size_filter',
            'is_enabled': True,
            'filter_values': {
                "enabled": True,
                "min_amount": 500000,
                "max_amount": 15000000,
                "optimal_min": 1000000,
                "optimal_max": 8000000,
                "strict_mode": False
            }
        }
    ]
    
    success_count = 0
    for setting in filter_settings:
        try:
            result = supabase.table('alex_filter_settings').upsert(setting).execute()
            print(f"✅ Filter setting '{setting['setting_name']}' configured")
            success_count += 1
        except Exception as e:
            print(f"⚠️  Failed to set '{setting['setting_name']}': {e}")
    
    print(f"📊 Configured {success_count}/{len(filter_settings)} filter settings")
    return success_count == len(filter_settings)

def setup_alex_deal_views(supabase):
    """Insert Alex's default deal views"""
    print("🔄 Setting up Alex's deal views...")
    
    deal_views = [
        {
            'view_name': 'alex_default',
            'filter_criteria': {
                "stage_filter": {"enabled": True, "strict_mode": False},
                "ai_filter": {"enabled": True, "strict_mode": False},
                "sector_filter": {"enabled": True, "strict_mode": False},
                "geography_filter": {"enabled": True, "strict_mode": False},
                "funding_size_filter": {"enabled": True, "strict_mode": False}
            },
            'is_active': True
        },
        {
            'view_name': 'alex_strict',
            'filter_criteria': {
                "stage_filter": {"enabled": True, "strict_mode": True},
                "ai_filter": {"enabled": True, "strict_mode": True},
                "sector_filter": {"enabled": True, "strict_mode": True},
                "geography_filter": {"enabled": True, "strict_mode": True},
                "funding_size_filter": {"enabled": True, "strict_mode": True}
            },
            'is_active': False
        },
        {
            'view_name': 'all_deals',
            'filter_criteria': {
                "stage_filter": {"enabled": False, "strict_mode": False},
                "ai_filter": {"enabled": False, "strict_mode": False},
                "sector_filter": {"enabled": False, "strict_mode": False},
                "geography_filter": {"enabled": False, "strict_mode": False},
                "funding_size_filter": {"enabled": False, "strict_mode": False}
            },
            'is_active': False
        }
    ]
    
    success_count = 0
    for view in deal_views:
        try:
            result = supabase.table('alex_deal_views').upsert(view).execute()
            print(f"✅ Deal view '{view['view_name']}' configured")
            success_count += 1
        except Exception as e:
            print(f"⚠️  Failed to set view '{view['view_name']}': {e}")
    
    print(f"📊 Configured {success_count}/{len(deal_views)} deal views")
    return success_count == len(deal_views)

def setup_data_sources(supabase):
    """Insert data source configurations"""
    print("🔄 Setting up data sources...")
    
    data_sources = [
        {'name': 'TechCrunch', 'type': 'news', 'url': 'https://techcrunch.com/category/startups/', 'is_active': True, 'reliability_score': 0.9},
        {'name': 'Climate Insider', 'type': 'news', 'url': 'https://climateinsider.com/category/exclusives/', 'is_active': True, 'reliability_score': 0.95},
        {'name': 'CTVC', 'type': 'news', 'url': 'https://www.ctvc.co/tag/insights/', 'is_active': True, 'reliability_score': 0.85},
        {'name': 'Axios Pro Climate', 'type': 'news', 'url': 'https://pro.axios.com/climate-deals', 'is_active': True, 'reliability_score': 0.9},
        {'name': 'AgFunder News', 'type': 'news', 'url': 'https://agfundernews.com/', 'is_active': True, 'reliability_score': 0.8},
        {'name': 'Tech Funding News', 'type': 'news', 'url': 'https://techfundingnews.com/category/climate-tech/', 'is_active': True, 'reliability_score': 0.8},
        {'name': 'Canary Media', 'type': 'news', 'url': 'https://www.canarymedia.com/articles', 'is_active': True, 'reliability_score': 0.9}
    ]
    
    success_count = 0
    for source in data_sources:
        try:
            result = supabase.table('data_sources').upsert(source).execute()
            print(f"✅ Data source '{source['name']}' configured")
            success_count += 1
        except Exception as e:
            print(f"⚠️  Failed to set data source '{source['name']}': {e}")
    
    print(f"📊 Configured {success_count}/{len(data_sources)} data sources")
    return success_count == len(data_sources)

def verify_schema_exists(supabase):
    """Verify that all required tables exist"""
    print("🔍 Verifying schema exists...")
    
    required_tables = [
        'companies', 'deals_new', 'investors', 'deal_investors',
        'alex_filter_settings', 'alex_deal_views', 'enrichment_queue', 'data_sources'
    ]
    
    existing_tables = []
    missing_tables = []
    
    for table_name in required_tables:
        try:
            result = supabase.table(table_name).select('*', count='exact').limit(1).execute()
            existing_tables.append(table_name)
            print(f"✅ Table '{table_name}' exists")
        except Exception as e:
            missing_tables.append(table_name)
            print(f"❌ Table '{table_name}' missing")
    
    if missing_tables:
        print(f"\n⚠️  Missing tables: {', '.join(missing_tables)}")
        print("Please run the SQL deployment steps first:")
        print("1. step1_create_tables.sql")
        print("2. step2_create_indexes.sql") 
        print("3. step3_enable_rls.sql")
        print("4. step4_create_functions_views.sql")
        return False
    
    print(f"🎉 All {len(existing_tables)} required tables exist!")
    return True

def main():
    """Main setup process"""
    print("🚀 Starting Alex's Default Data Setup")
    print("=" * 50)
    
    # Connect to Supabase
    supabase = connect_to_supabase()
    
    # Verify schema exists
    if not verify_schema_exists(supabase):
        print("\n❌ Schema verification failed. Please deploy schema first.")
        return False
    
    print("\n⚙️  Setting up Alex's configurations...")
    
    # Setup filter settings
    filter_success = setup_alex_filter_settings(supabase)
    
    # Setup deal views
    views_success = setup_alex_deal_views(supabase)
    
    # Setup data sources
    sources_success = setup_data_sources(supabase)
    
    # Final summary
    print("\n" + "=" * 50)
    if filter_success and views_success and sources_success:
        print("🎉 DEFAULT DATA SETUP SUCCESSFUL!")
        print("✅ Alex's filter settings configured")
        print("✅ Alex's deal views configured")
        print("✅ Data sources configured")
        print("✅ Ready for Phase 1C: Data Migration")
        
        print("\n📋 Next Steps:")
        print("1. Run: python deploy_schema.py (to verify everything)")
        print("2. Start Phase 1C: Data Migration")
        print("3. Migrate existing 150 deals to new schema")
        
        return True
    else:
        print("⚠️  SETUP INCOMPLETE")
        print("Please review the errors above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
