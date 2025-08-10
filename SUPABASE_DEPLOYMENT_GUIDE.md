# 🚀 Supabase Schema Deployment Guide

## Overview
Deploy Alex's Climate Tech VC Pipeline normalized schema to Supabase in 4 easy steps.

## Prerequisites
- Access to your Supabase Dashboard
- SQL Editor access in Supabase
- Backup of current `deals` table (we have 150 deals to preserve)

## Deployment Steps

### Step 1: Create Tables
1. Open your Supabase Dashboard: https://app.supabase.com/
2. Navigate to your project: `gpxbbzdxxtlibsjymmsy`
3. Go to **SQL Editor** (left sidebar)
4. Create a new query
5. Copy and paste the contents of `step1_create_tables.sql`
6. Click **Run** to execute

**What this creates:**
- `companies` table - Normalized company information
- `deals_new` table - New deals structure (keeps original `deals` intact)
- `investors` table - VC firms and investor data
- `deal_investors` table - Many-to-many relationships
- `alex_filter_settings` table - Alex's configurable preferences
- `alex_deal_views` table - Saved filter combinations
- `enrichment_queue` table - Automated processing queue
- `data_sources` table - Source health monitoring

### Step 2: Create Indexes
1. In the same SQL Editor, create another new query
2. Copy and paste the contents of `step2_create_indexes.sql`
3. Click **Run** to execute

**What this creates:**
- Performance indexes on all key columns
- Foreign key relationship indexes
- Search optimization indexes

### Step 3: Enable Row Level Security
1. Create another new query in SQL Editor
2. Copy and paste the contents of `step3_enable_rls.sql`
3. Click **Run** to execute

**What this creates:**
- Row Level Security policies
- Authenticated user access controls
- Security for all tables

### Step 4: Create Functions and Views
1. Create another new query in SQL Editor
2. Copy and paste the contents of `step4_create_functions_views.sql`
3. Click **Run** to execute

**What this creates:**
- Auto-update timestamp triggers
- `alex_daily_prospects` view for high-score deals
- `pipeline_health` view for monitoring

### Step 5: Insert Default Data
1. In your terminal, run: `python setup_default_data.py`

**What this creates:**
- Alex's default filter settings
- Alex's default deal view
- Data source configurations

## Verification

After deployment, verify success by running:
```bash
python deploy_schema.py
```

You should see:
```
🎉 All 8 tables exist!
✅ Alex's filter settings configured
✅ Data sources configured
✅ Ready for Phase 1C: Data Migration
```

## What's Next

After successful deployment:
1. **Phase 1C**: Migrate existing 150 deals to new schema
2. **Phase 1D**: Test data integrity and relationships
3. **Phase 1E**: Implement Alex's scoring system

## Schema Overview

### New Tables Created:
- ✅ `companies` - Normalized company data
- ✅ `deals_new` - Enhanced deal structure with Alex's scoring
- ✅ `investors` - VC firm and investor tracking
- ✅ `deal_investors` - Investment relationship mapping
- ✅ `alex_filter_settings` - Flexible filter configuration
- ✅ `alex_deal_views` - Saved filter combinations
- ✅ `enrichment_queue` - Automated data enhancement
- ✅ `data_sources` - Source reliability monitoring

### Key Features:
- **Flexible Filtering**: Toggle strict/flexible modes
- **Auto-Scoring**: Investment score calculation for Alex
- **Data Quality**: Confidence scores and verification
- **Performance**: Strategic indexes for fast queries
- **Scalability**: Normalized design supports growth

## Troubleshooting

### Common Issues:

1. **Permission Error**: Ensure you're using the correct Supabase project
2. **Syntax Error**: Copy the entire SQL file content, don't modify
3. **Table Exists Error**: Tables may already exist, check current state first
4. **RLS Error**: Make sure you're authenticated in Supabase

### Get Help:
- Check the deployment logs in `deploy_schema.py`
- Verify table creation in Supabase Dashboard > Database > Tables
- Test queries in SQL Editor

## Files Reference:
- `step1_create_tables.sql` - Main table creation
- `step2_create_indexes.sql` - Performance indexes
- `step3_enable_rls.sql` - Security policies
- `step4_create_functions_views.sql` - Helper functions and views
- `setup_default_data.py` - Insert Alex's configurations
- `deploy_schema.py` - Verification and status checking
