#!/usr/bin/env python3
"""
Test if RLS bypass functions exist in Supabase
"""

import os
from dotenv import load_dotenv
from supabase import create_client

def test_rls_functions():
    load_dotenv()
    url = os.getenv('SUPABASE_URL').strip(' "')
    key = os.getenv('SUPABASE_KEY').strip(' "')
    supabase = create_client(url, key)
    
    print('🔍 Testing if RLS bypass functions exist...')
    print('=' * 50)
    
    # Test each function
    functions_to_test = ['create_company_safe', 'create_deal_safe', 'create_investor_safe']
    
    missing_functions = []
    
    for func_name in functions_to_test:
        try:
            # Try to call the function (this will fail if function doesn't exist)
            result = supabase.rpc(func_name, {}).execute()
            print(f'✅ {func_name}: EXISTS')
        except Exception as e:
            error_str = str(e).lower()
            if 'function' in error_str and ('does not exist' in error_str or 'not found' in error_str):
                print(f'❌ {func_name}: MISSING')
                missing_functions.append(func_name)
            else:
                print(f'⚠️ {func_name}: EXISTS but parameter error: {str(e)[:60]}...')
    
    print('=' * 50)
    
    if missing_functions:
        print('❌ MISSING FUNCTIONS DETECTED!')
        print(f'Missing: {", ".join(missing_functions)}')
        print('')
        print('🚨 THIS IS WHY YOUR AI PROCESSING WILL FAIL:')
        print('• schema_adapter.py calls these RPC functions')
        print('• Without them, data insertion fails')
        print('• Your Layer 2 system cannot process new deals')
        print('')
        print('✅ SOLUTION:')
        print('1. Go to Supabase Dashboard SQL Editor')
        print('2. Run the content of step7_rls_bypass_functions.sql')
        print('3. This will create the missing functions')
        return False
    else:
        print('✅ ALL FUNCTIONS EXIST!')
        print('Your AI processing should work correctly.')
        return True

if __name__ == '__main__':
    test_rls_functions()
