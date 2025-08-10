#!/usr/bin/env python3
"""
Comprehensive Codebase Cleanup - Layer 2 Complete
================================================

Removes unnecessary files after successful Layer 2 deployment:
- Old/backup documentation files
- Debug and development scripts  
- Test files and reset utilities
- Temporary JSON export files
- Superseded v1 scrapers
- Development analysis scripts

Preserves essential files for production system.
"""

import os
import json
from datetime import datetime

def cleanup_codebase():
    """Remove unnecessary files from the codebase."""
    
    cleanup_report = {
        'cleanup_date': datetime.now().isoformat(),
        'files_removed': [],
        'files_preserved': [],
        'categories': {
            'documentation_backups': [],
            'debug_scripts': [],
            'test_utilities': [],
            'temp_json_exports': [],
            'superseded_scrapers': [],
            'development_scripts': []
        },
        'space_saved_bytes': 0
    }
    
    # Files to remove by category
    files_to_remove = {
        'documentation_backups': [
            'README_OLD.md',
            'README_UPDATED.md', 
            'PROJECT_STATUS_OLD.md',
            'PROJECT_STATUS_UPDATED.md',
            'IMPLEMENTATION_TASKS_OLD.md',
            'IMPLEMENTATION_TASKS_UPDATED.md'
        ],
        'debug_scripts': [
            'debug_arpae_structure.py',
            'debug_bev_website.py', 
            'debug_eip_portfolio_detailed.py',
            'debug_eip_website.py',
            'debug_supabase.html',
            'debug_table_extraction.py',
            'debug_table_structure.py',
            'debug_vc_sites_advanced.py'
        ],
        'test_utilities': [
            'test_supabase_connection.py',
            'test_schema_adapter.py',
            'test_reset_deals.py',
            'test_pagination_content.py',
            'test_government_urls.py'
        ],
        'temp_json_exports': [
            'workspace_cleanup_report_20250809_140025.json',
            'vc_portfolio_discoveries_20250809.json',
            'national_labs_intelligence_20250809_133527.json', 
            'layer2_discovery_session_20250809_134037.json',
            'layer2_database_integration_20250809_135738.json'
        ],
        'superseded_scrapers': [
            'scrape_climateinsider_daily.py',  # Replaced by v2
            'scrape_ctvc_daily.py',           # Replaced by v2
            'scrape_techcrunch_daily.py'      # Replaced by v2
            # Keep: scrape_agfundernews_daily.py, scrape_techfundingnews_daily.py (no v2 yet)
        ],
        'development_scripts': [
            'reset_specific_deals.py',
            'reset_no_dates.py',
            'check_deals_status.py',
            'check_deal_dates.py', 
            'check_dates_status.py',
            'find_funding_deals.py',
            'cleanup_irrelevant_type.py',
            'analyze_mvp_portfolio.py',
            'fix_deal_dates.py'
        ]
    }
    
    # Essential files to preserve (double-check)
    essential_files = [
        'schema_design_v1.sql',      # Master schema
        'migration_v1.py',           # Database migration script
        'layer2_orchestrator.py',    # Core Layer 2 system
        'schema_adapter.py',         # Core integration layer
        'deploy_schema.py',          # Deployment automation
        'process_articles_ai_v2.py', # AI processing engine
        'scrape_vc_portfolios.py',   # VC intelligence
        'scrape_national_labs.py',   # Government intelligence
        'source_intelligence_manager.py' # Source management
    ]
    
    total_removed = 0
    
    print("🧹 Starting comprehensive codebase cleanup...")
    print("=" * 60)
    
    for category, files in files_to_remove.items():
        print(f"\n📂 {category.replace('_', ' ').title()}:")
        
        for filename in files:
            if os.path.exists(filename):
                try:
                    # Get file size before removal
                    file_size = os.path.getsize(filename)
                    
                    # Remove the file
                    os.remove(filename)
                    
                    cleanup_report['files_removed'].append(filename)
                    cleanup_report['categories'][category].append(filename)
                    cleanup_report['space_saved_bytes'] += file_size
                    total_removed += 1
                    
                    print(f"  ✅ Removed: {filename} ({file_size:,} bytes)")
                    
                except Exception as e:
                    print(f"  ❌ Failed to remove {filename}: {e}")
            else:
                print(f"  ⚠️  Not found: {filename}")
    
    # Verify essential files are preserved
    print(f"\n🔍 Verifying Essential Files:")
    for essential_file in essential_files:
        if os.path.exists(essential_file):
            cleanup_report['files_preserved'].append(essential_file) 
            print(f"  ✅ Preserved: {essential_file}")
        else:
            print(f"  ⚠️  Missing essential file: {essential_file}")
    
    # Generate summary
    space_saved_mb = cleanup_report['space_saved_bytes'] / (1024 * 1024)
    
    print(f"\n🎉 Cleanup Complete!")
    print(f"Files removed: {total_removed}")
    print(f"Space saved: {space_saved_mb:.2f} MB")
    
    # Save cleanup report
    report_filename = f"codebase_cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_filename, 'w') as f:
        json.dump(cleanup_report, f, indent=2)
    
    print(f"📊 Cleanup report saved: {report_filename}")
    
    return cleanup_report

if __name__ == "__main__":
    cleanup_codebase()
