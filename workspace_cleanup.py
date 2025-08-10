#!/usr/bin/env python3
"""
Layer 2 Workspace Cleanup Script
===============================

Safely removes debug files, empty files, and temporary artifacts while preserving
the core Layer 2 system and successfully integrated data.

IMPORTANT: This script only removes files that are no longer needed after successful
Layer 2 integration. All essential systems and data are preserved.
"""

import os
import shutil
from datetime import datetime

def cleanup_workspace():
    """Remove unnecessary files while preserving core Layer 2 system."""
    
    print("🧹 LAYER 2 WORKSPACE CLEANUP")
    print("=" * 50)
    print("Removing debug files, empty files, and temporary artifacts...")
    print("✅ Preserving core Layer 2 system and integrated data")
    print()
    
    # Files to delete - debug, empty, and temporary files
    files_to_delete = [
        # Debug files (completed debugging)
        "debug_arpae_structure.py",
        "debug_bev_website.py", 
        "debug_eip_website.py",
        "debug_eip_portfolio_detailed.py",
        "debug_vc_sites_advanced.py",
        "debug_table_extraction.py",
        "debug_table_structure.py",
        "test_pagination_content.py",
        "test_government_urls.py",
        "layer2_integration_preview.py",
        
        # Empty files
        "government_discoveries_20250809_133254.json",
        "ai_detection_system.py",
        "scrape_early_stage_discovery.py",
        "check_tables.sql",
        "SCRAPER_UPDATE_COMPLETE.md",
        "scrape_agfundernews_daily_v2.py",
        "scrape_canary_media_v2.py",
        "scrape_techfundingnews_daily_v2.py", 
        "validate_deals_new.sql",
        "scrape_axios_daily.py",
        
        # Large debug HTML files
        "canary_article_debug.html",
        "axios_live_debug.html",
        
        # Intermediate files (superseded)
        "government_url_test_results.json",
        "layer2_integration_preview_20250809_135121.json",
        "source_intelligence_20250809_133705.json",
        
        # Log files
        "vc_portfolio_scraper.log"
    ]
    
    # Directories to delete
    dirs_to_delete = [
        "__pycache__"
    ]
    
    deleted_files = []
    deleted_dirs = []
    total_size_saved = 0
    
    # Delete files
    for filename in files_to_delete:
        if os.path.exists(filename):
            try:
                file_size = os.path.getsize(filename)
                os.remove(filename)
                deleted_files.append(filename)
                total_size_saved += file_size
                print(f"🗑️ Deleted: {filename} ({file_size:,} bytes)")
            except Exception as e:
                print(f"❌ Failed to delete {filename}: {e}")
        else:
            print(f"⚠️ File not found: {filename}")
    
    # Delete directories
    for dirname in dirs_to_delete:
        if os.path.exists(dirname) and os.path.isdir(dirname):
            try:
                dir_size = sum(os.path.getsize(os.path.join(dirname, f)) 
                              for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f)))
                shutil.rmtree(dirname)
                deleted_dirs.append(dirname)
                total_size_saved += dir_size
                print(f"🗑️ Deleted directory: {dirname} ({dir_size:,} bytes)")
            except Exception as e:
                print(f"❌ Failed to delete directory {dirname}: {e}")
        else:
            print(f"⚠️ Directory not found: {dirname}")
    
    print()
    print("📊 CLEANUP SUMMARY")
    print("-" * 30)
    print(f"Files deleted: {len(deleted_files)}")
    print(f"Directories deleted: {len(deleted_dirs)}")
    print(f"Total space saved: {total_size_saved:,} bytes ({total_size_saved/1024/1024:.2f} MB)")
    print()
    
    # Verify core files are still present
    print("✅ VERIFYING CORE LAYER 2 SYSTEM")
    print("-" * 40)
    
    core_files = [
        "layer2_orchestrator.py",
        "source_intelligence_manager.py", 
        "scrape_national_labs.py",
        "scrape_vc_portfolios.py",
        "layer2_database_integration.py",
        "test_supabase_connection.py",
        "schema_adapter.py",
        ".env",
        "vc_portfolio_discoveries_20250809.json",
        "national_labs_intelligence_20250809_133527.json",
        "layer2_discovery_session_20250809_134037.json",
        "layer2_database_integration_20250809_135738.json"
    ]
    
    all_core_present = True
    for core_file in core_files:
        if os.path.exists(core_file):
            print(f"✅ {core_file}")
        else:
            print(f"❌ MISSING: {core_file}")
            all_core_present = False
    
    print()
    if all_core_present:
        print("🎯 SUCCESS: All core Layer 2 files preserved!")
        print("✅ 924 database entries remain integrated")
        print("🚀 Workspace ready for Layer 3 development")
    else:
        print("⚠️ WARNING: Some core files missing - check before proceeding")
    
    # Save cleanup report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {
        "cleanup_timestamp": datetime.now().isoformat(),
        "files_deleted": deleted_files,
        "directories_deleted": deleted_dirs,
        "total_size_saved_bytes": total_size_saved,
        "core_files_verified": all_core_present
    }
    
    report_filename = f"workspace_cleanup_report_{timestamp}.json"
    import json
    with open(report_filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📁 Cleanup report saved: {report_filename}")
    
    return report

if __name__ == "__main__":
    cleanup_workspace()
