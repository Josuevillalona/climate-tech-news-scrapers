-- SQL Script to Revert Deal Status from 'PROCESSED_AI' and 'PROCESSED' back to 'NEW'
-- This will allow the improved AI processor to re-evaluate all deals with better filtering
-- Run this in Supabase SQL Editor
-- Date: August 9, 2025

-- First, let's check current status distribution
SELECT 
    'Current status distribution' as description,
    processing_status,
    COUNT(*) as count
FROM deals_new 
GROUP BY processing_status
ORDER BY processing_status;

-- Check how many deals we'll be reverting
SELECT 
    'Deals to revert (PROCESSED_AI + PROCESSED)' as description,
    COUNT(*) as count
FROM deals_new 
WHERE processing_status IN ('PROCESSED_AI', 'PROCESSED');

-- Check recent IRRELEVANT deals (should show our enhanced filtering is working)
SELECT 
    'Recent IRRELEVANT deals (enhanced filtering working)' as description,
    COUNT(*) as count
FROM deals_new 
WHERE processing_status = 'IRRELEVANT' AND updated_at >= NOW() - INTERVAL '1 day';

-- Revert all PROCESSED_AI and PROCESSED deals back to NEW status
-- This allows the improved AI processor to re-evaluate with better climate filtering
UPDATE deals_new 
SET 
    processing_status = 'NEW',
    updated_at = NOW()
WHERE processing_status IN ('PROCESSED_AI', 'PROCESSED');

-- Confirm the update by checking status distribution again
SELECT 
    'After revert - status distribution' as description,
    status,
    COUNT(*) as count
FROM deals_new 
GROUP BY status
ORDER BY status;

-- Show sample of reverted deals
SELECT 
    deals_new.id,
    deals_new.status,
    deals_new.source_type,
    deals_new.updated_at,
    companies.name as company_name
FROM deals_new 
LEFT JOIN companies ON deals_new.company_id = companies.id
WHERE deals_new.status = 'NEW'
ORDER BY deals_new.updated_at DESC
LIMIT 15;
