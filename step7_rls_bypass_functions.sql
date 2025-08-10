-- =============================================================================
-- STEP 7: RLS BYPASS FUNCTIONS FOR AUTOMATED PROCESSES (V2)
-- =============================================================================
-- These functions allow the schema_adapter.py and AI processors to bypass
-- Row Level Security when inserting data programmatically.

-- Use V2 function names to avoid conflicts
-- Function to safely create or get a company (bypasses RLS)
CREATE OR REPLACE FUNCTION create_company_safe_v2(
    company_name TEXT,
    country TEXT DEFAULT NULL,
    sector TEXT DEFAULT NULL,
    ai_focus BOOLEAN DEFAULT FALSE
)
RETURNS UUID
SECURITY DEFINER
SET search_path = public
LANGUAGE plpgsql
AS $$
DECLARE
    company_id UUID;
BEGIN
    -- Try to find existing company first
    SELECT id INTO company_id
    FROM companies
    WHERE LOWER(name) = LOWER(company_name)
    LIMIT 1;
    
    -- If company exists, return its ID
    IF company_id IS NOT NULL THEN
        RETURN company_id;
    END IF;
    
    -- Create new company
    INSERT INTO companies (
        name,
        headquarters_country,
        climate_sub_sectors,
        has_ai_focus,
        is_climate_tech,
        enrichment_status
    ) VALUES (
        company_name,
        COALESCE(country, 'Unknown'),
        CASE WHEN sector IS NOT NULL THEN ARRAY[sector] ELSE ARRAY[]::TEXT[] END,
        ai_focus,
        TRUE,
        'pending'
    )
    RETURNING id INTO company_id;
    
    RETURN company_id;
END;
$$;

-- Function to safely create a deal (bypasses RLS)
CREATE OR REPLACE FUNCTION create_deal_safe_v2(
    company_id UUID,
    source_url TEXT,
    raw_content TEXT,
    funding_stage TEXT DEFAULT NULL,
    amount_usd NUMERIC DEFAULT NULL,
    original_amount TEXT DEFAULT NULL,
    source_type TEXT DEFAULT 'news',
    source_name TEXT DEFAULT NULL,
    detected_country TEXT DEFAULT NULL,
    has_ai BOOLEAN DEFAULT FALSE
)
RETURNS UUID
SECURITY DEFINER
SET search_path = public
LANGUAGE plpgsql
AS $$
DECLARE
    deal_id UUID;
    alex_score INTEGER DEFAULT 50; -- Default score
BEGIN
    -- Use a simple default Alex score for now
    -- The AI processor can update this later
    alex_score := 50;
    
    -- Insert the deal
    INSERT INTO deals_new (
        company_id,
        amount_raised_usd,
        original_amount,
        funding_stage,
        source_url,
        source_type,
        source_name,
        raw_text_content,
        confidence_score,
        investment_score,
        alex_review_status,
        status
    ) VALUES (
        company_id,
        amount_usd,
        original_amount,
        funding_stage,
        source_url,
        source_type,
        COALESCE(source_name, 'Unknown'),
        raw_content,
        0.8,
        alex_score,
        'pending',
        'new'
    )
    RETURNING id INTO deal_id;
    
    RETURN deal_id;
END;
$$;

-- Function to safely create an investor (bypasses RLS)
CREATE OR REPLACE FUNCTION create_investor_safe_v2(
    investor_name TEXT,
    investor_type TEXT DEFAULT 'vc'
)
RETURNS UUID
SECURITY DEFINER
SET search_path = public
LANGUAGE plpgsql
AS $$
DECLARE
    investor_id UUID;
BEGIN
    -- Try to find existing investor first
    SELECT id INTO investor_id
    FROM investors
    WHERE LOWER(name) = LOWER(investor_name)
    LIMIT 1;
    
    -- If investor exists, return its ID
    IF investor_id IS NOT NULL THEN
        RETURN investor_id;
    END IF;
    
    -- Create new investor
    INSERT INTO investors (
        name,
        type,
        climate_focus,
        enrichment_status
    ) VALUES (
        investor_name,
        investor_type,
        TRUE, -- Assume climate focus for our pipeline
        'pending'
    )
    RETURNING id INTO investor_id;
    
    RETURN investor_id;
END;
$$;

-- Grant execute permissions to authenticated users
GRANT EXECUTE ON FUNCTION create_company_safe_v2 TO authenticated;
GRANT EXECUTE ON FUNCTION create_deal_safe_v2 TO authenticated;
GRANT EXECUTE ON FUNCTION create_investor_safe_v2 TO authenticated;

-- =============================================================================
-- VERIFICATION QUERIES
-- =============================================================================

-- Test the functions work correctly
DO $$
DECLARE
    test_company_id UUID;
    test_deal_id UUID;
    test_investor_id UUID;
BEGIN
    -- Test company creation
    SELECT create_company_safe_v2('Test Company RLS', 'United States', 'Energy Storage', TRUE) INTO test_company_id;
    RAISE NOTICE 'Created test company with ID: %', test_company_id;
    
    -- Test deal creation
    SELECT create_deal_safe_v2(
        test_company_id,
        'https://test.com/test-deal',
        'Test deal content for RLS bypass testing',
        'seed',
        1000000,
        '$1M',
        'test',
        'Test Source'
    ) INTO test_deal_id;
    RAISE NOTICE 'Created test deal with ID: %', test_deal_id;
    
    -- Test investor creation
    SELECT create_investor_safe_v2('Test VC Firm', 'vc') INTO test_investor_id;
    RAISE NOTICE 'Created test investor with ID: %', test_investor_id;
    
    -- Clean up test data
    DELETE FROM deals_new WHERE id = test_deal_id;
    DELETE FROM investors WHERE id = test_investor_id;
    DELETE FROM companies WHERE id = test_company_id;
    
    RAISE NOTICE 'RLS bypass functions verified and test data cleaned up successfully!';
END;
$$;

-- =============================================================================
-- COMPLETION MESSAGE
-- =============================================================================

DO $$
BEGIN
    RAISE NOTICE '✅ RLS Bypass Functions V2 Deployed Successfully!';
    RAISE NOTICE '🔧 Functions created: create_company_safe_v2, create_deal_safe_v2, create_investor_safe_v2';
    RAISE NOTICE '🔒 Security: Functions use SECURITY DEFINER to bypass RLS';
    RAISE NOTICE '✨ Your schema_adapter.py should now work correctly!';
    RAISE NOTICE '';
    RAISE NOTICE '🎯 Next Steps:';
    RAISE NOTICE '1. Test schema_adapter: python test_schema_adapter.py';
    RAISE NOTICE '2. Run updated scrapers with new schema integration';
    RAISE NOTICE '3. Verify data appears in companies, deals, investors tables';
END;
$$;
