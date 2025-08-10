#!/usr/bin/env python3
"""
Quick test of the consolidated AI processor
"""

import os
from dotenv import load_dotenv
from supabase import create_client
from ai_processor_consolidated import ConsolidatedAIProcessor

def quick_test():
    load_dotenv()
    url = os.getenv('SUPABASE_URL').strip(' "')
    key = os.getenv('SUPABASE_KEY').strip(' "')
    supabase = create_client(url, key)
    
    processor = ConsolidatedAIProcessor(supabase)
    
    print('🧪 TESTING CONSOLIDATED AI PROCESSOR')
    print('=' * 50)
    print('Testing on 2 sample entries...')
    
    # Process just 2 entries for testing
    processed = processor.process_all_pending(limit=2)
    
    print(f'✅ Test complete! Processed {processed} entries.')
    print('=' * 50)

if __name__ == "__main__":
    quick_test()
