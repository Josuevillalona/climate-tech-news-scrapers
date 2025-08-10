#!/usr/bin/env python3
"""
Supabase Connection Test
=======================

Quick test to verify Supabase credentials and connection before running the full integration.
"""

import os
import sys

# Load environment variables from .env file
def load_env_file():
    """Load environment variables from .env file."""
    env_path = '.env'
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    os.environ[key] = value

# Load environment variables
load_env_file()

def test_supabase_connection():
    """Test Supabase connection and provide setup guidance."""
    
    print("🔍 SUPABASE CONNECTION TEST")
    print("=" * 50)
    
    # Check environment variables
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    
    print("1. Environment Variables Check:")
    print(f"   SUPABASE_URL: {'✅ Set' if url else '❌ Not Set'}")
    print(f"   SUPABASE_KEY: {'✅ Set' if key else '❌ Not Set'}")
    print()
    
    if not url or not key:
        print("🔧 SETUP INSTRUCTIONS:")
        print("Set your Supabase credentials in PowerShell:")
        print()
        print("$env:SUPABASE_URL='https://your-project-id.supabase.co'")
        print("$env:SUPABASE_KEY='your-anon-or-service-role-key'")
        print()
        print("📖 How to find your credentials:")
        print("1. Go to https://app.supabase.com/projects")
        print("2. Select your project")
        print("3. Go to Settings > API")
        print("4. Copy 'Project URL' and 'anon public' or 'service_role' key")
        print()
        return False
    
    # Test Supabase import
    print("2. Supabase Library Check:")
    try:
        from supabase import create_client, Client
        print("   ✅ supabase-py library installed")
    except ImportError:
        print("   ❌ supabase-py library not found")
        print("   Install with: pip install supabase-py")
        return False
    
    # Test connection
    print("3. Connection Test:")
    try:
        supabase = create_client(url, key)
        
        # Try a simple query to test connection
        result = supabase.table('deals').select('id').limit(1).execute()
        print("   ✅ Successfully connected to Supabase")
        print(f"   📊 Database accessible (deals table found)")
        
        # Check if schema_adapter works
        try:
            from schema_adapter import SchemaAwareDealInserter
            inserter = SchemaAwareDealInserter(supabase)
            print("   ✅ Schema adapter loaded successfully")
        except ImportError as e:
            print(f"   ⚠️ Schema adapter issue: {e}")
            print("   Integration may need manual schema handling")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Connection failed: {str(e)}")
        print()
        print("   Common issues:")
        print("   - Wrong project URL")
        print("   - Invalid API key")
        print("   - Network connectivity")
        print("   - Database permissions")
        return False

def main():
    """Main test function."""
    
    success = test_supabase_connection()
    
    print()
    if success:
        print("🎯 READY FOR INTEGRATION!")
        print("Run: python layer2_database_integration.py")
        print()
        print("📊 Integration will process:")
        print("   • 11 government discoveries")
        print("   • 895 VC portfolio companies")
        print("   • 906 total database entries")
    else:
        print("🔧 SETUP REQUIRED")
        print("Complete the setup steps above, then run this test again.")
    
    return success

if __name__ == "__main__":
    main()
