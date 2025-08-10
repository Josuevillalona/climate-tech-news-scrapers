-- Alex's Climate Tech VC Pipeline - Database Schema
-- Complete normalized schema for Supabase implementation

-- =============================================================================
-- CORE TABLES
-- =============================================================================

-- Companies table - Normalized company information
CREATE TABLE companies (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    website VARCHAR(500),
    domain VARCHAR(255),
    description TEXT,
    founding_year INTEGER,
    employee_count_range VARCHAR(50), -- e.g., "1-10", "11-50", "51-200"
    employee_count_estimated INTEGER,
    headquarters_city VARCHAR(100),
    headquarters_state VARCHAR(100),
    headquarters_country VARCHAR(100),
    is_climate_tech BOOLEAN DEFAULT true,
    has_ai_focus BOOLEAN DEFAULT false,
    climate_sub_sectors TEXT[], -- Array of climate tech sectors
    target_markets TEXT[], -- Array of target markets
    verification_status VARCHAR(20) DEFAULT 'pending', -- 'verified', 'unverified', 'pending'
    legal_name VARCHAR(255),
    incorporation_date DATE,
    enrichment_status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'basic', 'complete'
    data_sources TEXT[], -- Array of sources used for enrichment
    confidence_score FLOAT DEFAULT 0.5, -- 0.0 to 1.0
    media_mentions INTEGER DEFAULT 0, -- Count of media mentions
    last_enriched_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Deals table - Funding rounds and announcements
CREATE TABLE deals (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    amount_raised_usd NUMERIC(15,2), -- Standardized USD amount
    original_amount VARCHAR(100), -- Original amount string from source
    original_currency VARCHAR(10) DEFAULT 'USD',
    funding_stage VARCHAR(50), -- 'seed', 'series-a', 'series-b', etc.
    date_announced DATE,
    source_url VARCHAR(1000) NOT NULL,
    source_type VARCHAR(50) NOT NULL, -- 'news', 'vc_website', 'government'
    source_name VARCHAR(100) NOT NULL, -- 'TechCrunch', 'Climate Insider', etc.
    raw_text_content TEXT,
    confidence_score FLOAT DEFAULT 0.5,
    investment_score INTEGER, -- Alex's score (0-100)
    alex_review_status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'interested', 'passed', 'auto_filtered'
    alex_notes TEXT,
    alex_review_date TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'new', -- 'new', 'processed', 'enriched'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Investors table - VC firms, angels, etc.
CREATE TABLE investors (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50), -- 'vc', 'angel', 'corporate_vc', 'family_office'
    website VARCHAR(500),
    climate_focus BOOLEAN DEFAULT false,
    geographic_focus TEXT[], -- Array of geographic regions
    typical_check_size_min NUMERIC(15,2), -- Minimum check size in USD
    typical_check_size_max NUMERIC(15,2), -- Maximum check size in USD
    portfolio_count INTEGER DEFAULT 0,
    enrichment_status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Deal-Investor relationships (many-to-many)
CREATE TABLE deal_investors (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    deal_id UUID REFERENCES deals(id) ON DELETE CASCADE,
    investor_id UUID REFERENCES investors(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'unknown', -- 'lead', 'participant', 'unknown'
    amount_invested NUMERIC(15,2), -- Specific amount if known
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(deal_id, investor_id)
);

-- =============================================================================
-- ALEX'S FILTER & PREFERENCES SYSTEM
-- =============================================================================

-- Alex's configurable filter preferences
CREATE TABLE alex_filter_settings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    setting_name VARCHAR(50) NOT NULL UNIQUE, -- 'stage_filter', 'sector_filter', etc.
    is_enabled BOOLEAN DEFAULT true,
    filter_values JSONB NOT NULL, -- Flexible storage for filter criteria
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Alex's saved deal views/filters
CREATE TABLE alex_deal_views (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    view_name VARCHAR(100) NOT NULL, -- 'default', 'all_deals', 'custom_filter_1'
    filter_criteria JSONB NOT NULL, -- Complete filter configuration
    is_active BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================================
-- ENRICHMENT & PROCESSING SYSTEM
-- =============================================================================

-- Enrichment queue for processing companies
CREATE TABLE enrichment_queue (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    enrichment_type VARCHAR(50) NOT NULL, -- 'basic', 'funding', 'verification', 'comprehensive'
    priority INTEGER DEFAULT 5, -- 1-10, higher number = higher priority
    attempts INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'failed'
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Data sources tracking and health monitoring
CREATE TABLE data_sources (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    type VARCHAR(50) NOT NULL, -- 'news', 'vc_portfolio', 'government'
    url VARCHAR(1000),
    is_active BOOLEAN DEFAULT true,
    reliability_score FLOAT DEFAULT 1.0, -- 0.0 to 1.0
    last_scraped_at TIMESTAMP WITH TIME ZONE,
    last_successful_scrape TIMESTAMP WITH TIME ZONE,
    error_count INTEGER DEFAULT 0,
    last_error_at TIMESTAMP WITH TIME ZONE,
    last_error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================================
-- INDEXES FOR PERFORMANCE
-- =============================================================================

-- Companies indexes
CREATE INDEX idx_companies_name ON companies(name);
CREATE INDEX idx_companies_domain ON companies(domain);
CREATE INDEX idx_companies_climate_tech ON companies(is_climate_tech);
CREATE INDEX idx_companies_ai_focus ON companies(has_ai_focus);
CREATE INDEX idx_companies_country ON companies(headquarters_country);
CREATE INDEX idx_companies_enrichment_status ON companies(enrichment_status);

-- Deals indexes
CREATE INDEX idx_deals_company_id ON deals(company_id);
CREATE INDEX idx_deals_source_url ON deals(source_url);
CREATE INDEX idx_deals_funding_stage ON deals(funding_stage);
CREATE INDEX idx_deals_date_announced ON deals(date_announced);
CREATE INDEX idx_deals_investment_score ON deals(investment_score);
CREATE INDEX idx_deals_alex_review_status ON deals(alex_review_status);
CREATE INDEX idx_deals_status ON deals(status);
CREATE INDEX idx_deals_created_at ON deals(created_at);

-- Investors indexes
CREATE INDEX idx_investors_name ON investors(name);
CREATE INDEX idx_investors_type ON investors(type);
CREATE INDEX idx_investors_climate_focus ON investors(climate_focus);

-- Deal-Investors indexes
CREATE INDEX idx_deal_investors_deal_id ON deal_investors(deal_id);
CREATE INDEX idx_deal_investors_investor_id ON deal_investors(investor_id);
CREATE INDEX idx_deal_investors_role ON deal_investors(role);

-- Enrichment queue indexes
CREATE INDEX idx_enrichment_queue_company_id ON enrichment_queue(company_id);
CREATE INDEX idx_enrichment_queue_status ON enrichment_queue(status);
CREATE INDEX idx_enrichment_queue_priority ON enrichment_queue(priority);
CREATE INDEX idx_enrichment_queue_created_at ON enrichment_queue(created_at);

-- Data sources indexes
CREATE INDEX idx_data_sources_name ON data_sources(name);
CREATE INDEX idx_data_sources_type ON data_sources(type);
CREATE INDEX idx_data_sources_is_active ON data_sources(is_active);

-- =============================================================================
-- FOREIGN KEY CONSTRAINTS (Already defined above, but listed for clarity)
-- =============================================================================

-- deals.company_id -> companies.id
-- deal_investors.deal_id -> deals.id
-- deal_investors.investor_id -> investors.id
-- enrichment_queue.company_id -> companies.id

-- =============================================================================
-- ROW LEVEL SECURITY (RLS) SETUP
-- =============================================================================

-- Enable RLS on all tables
ALTER TABLE companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE deals ENABLE ROW LEVEL SECURITY;
ALTER TABLE investors ENABLE ROW LEVEL SECURITY;
ALTER TABLE deal_investors ENABLE ROW LEVEL SECURITY;
ALTER TABLE alex_filter_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE alex_deal_views ENABLE ROW LEVEL SECURITY;
ALTER TABLE enrichment_queue ENABLE ROW LEVEL SECURITY;
ALTER TABLE data_sources ENABLE ROW LEVEL SECURITY;

-- Basic RLS policies (allow all for authenticated users for now)
-- Note: In production, you might want more restrictive policies

CREATE POLICY "Allow authenticated users to read companies" ON companies FOR SELECT TO authenticated USING (true);
CREATE POLICY "Allow authenticated users to write companies" ON companies FOR ALL TO authenticated USING (true);

CREATE POLICY "Allow authenticated users to read deals" ON deals FOR SELECT TO authenticated USING (true);
CREATE POLICY "Allow authenticated users to write deals" ON deals FOR ALL TO authenticated USING (true);

CREATE POLICY "Allow authenticated users to read investors" ON investors FOR SELECT TO authenticated USING (true);
CREATE POLICY "Allow authenticated users to write investors" ON investors FOR ALL TO authenticated USING (true);

CREATE POLICY "Allow authenticated users to read deal_investors" ON deal_investors FOR SELECT TO authenticated USING (true);
CREATE POLICY "Allow authenticated users to write deal_investors" ON deal_investors FOR ALL TO authenticated USING (true);

CREATE POLICY "Allow authenticated users to read alex_filter_settings" ON alex_filter_settings FOR SELECT TO authenticated USING (true);
CREATE POLICY "Allow authenticated users to write alex_filter_settings" ON alex_filter_settings FOR ALL TO authenticated USING (true);

CREATE POLICY "Allow authenticated users to read alex_deal_views" ON alex_deal_views FOR SELECT TO authenticated USING (true);
CREATE POLICY "Allow authenticated users to write alex_deal_views" ON alex_deal_views FOR ALL TO authenticated USING (true);

CREATE POLICY "Allow authenticated users to read enrichment_queue" ON enrichment_queue FOR SELECT TO authenticated USING (true);
CREATE POLICY "Allow authenticated users to write enrichment_queue" ON enrichment_queue FOR ALL TO authenticated USING (true);

CREATE POLICY "Allow authenticated users to read data_sources" ON data_sources FOR SELECT TO authenticated USING (true);
CREATE POLICY "Allow authenticated users to write data_sources" ON data_sources FOR ALL TO authenticated USING (true);

-- =============================================================================
-- ALEX'S DEFAULT FILTER SETTINGS
-- =============================================================================

-- Insert Alex's default filter preferences
INSERT INTO alex_filter_settings (setting_name, is_enabled, filter_values) VALUES
('stage_filter', true, '{
    "enabled": true,
    "allowed_stages": ["seed", "series a", "series-a", "pre-seed"],
    "strict_mode": false
}'),
('ai_filter', true, '{
    "enabled": true,
    "require_ai": true,
    "strict_mode": false
}'),
('sector_filter', true, '{
    "enabled": true,
    "target_sectors": [
        "Climate Tech - Energy & Grid",
        "Climate Tech - Industrial Software", 
        "Climate Tech - Energy Storage",
        "Climate Tech - Smart Manufacturing",
        "Climate Tech - Carbon & Emissions"
    ],
    "strict_mode": false
}'),
('geography_filter', true, '{
    "enabled": true,
    "preferred_countries": ["US", "Canada", "UK"],
    "strict_mode": false
}'),
('funding_size_filter', true, '{
    "enabled": true,
    "min_amount": 500000,
    "max_amount": 15000000,
    "optimal_min": 1000000,
    "optimal_max": 8000000,
    "strict_mode": false
}');

-- Insert Alex's default view
INSERT INTO alex_deal_views (view_name, filter_criteria, is_active) VALUES
('alex_default', '{
    "stage_filter": {"enabled": true, "strict_mode": false},
    "ai_filter": {"enabled": true, "strict_mode": false},
    "sector_filter": {"enabled": true, "strict_mode": false},
    "geography_filter": {"enabled": true, "strict_mode": false},
    "funding_size_filter": {"enabled": true, "strict_mode": false}
}', true);

-- =============================================================================
-- INITIAL DATA SOURCES
-- =============================================================================

-- Insert current data sources
INSERT INTO data_sources (name, type, url, is_active, reliability_score) VALUES
('TechCrunch', 'news', 'https://techcrunch.com/category/startups/', true, 0.9),
('Climate Insider', 'news', 'https://climateinsider.com/category/exclusives/', true, 0.95),
('CTVC', 'news', 'https://www.ctvc.co/tag/insights/', true, 0.85),
('Axios Pro Climate', 'news', 'https://pro.axios.com/climate-deals', true, 0.9),
('AgFunder News', 'news', 'https://agfundernews.com/', true, 0.8),
('Tech Funding News', 'news', 'https://techfundingnews.com/category/climate-tech/', true, 0.8),
('Canary Media', 'news', 'https://www.canarymedia.com/articles', true, 0.9);

-- =============================================================================
-- USEFUL VIEWS FOR ALEX
-- =============================================================================

-- View for Alex's daily prospects (deals with high scores)
CREATE VIEW alex_daily_prospects AS
SELECT 
    d.id,
    d.investment_score,
    c.name as company_name,
    c.has_ai_focus,
    c.climate_sub_sectors,
    c.headquarters_country,
    d.funding_stage,
    d.amount_raised_usd,
    d.date_announced,
    d.source_name,
    d.source_url,
    d.alex_review_status,
    d.created_at
FROM deals d
JOIN companies c ON d.company_id = c.id
WHERE d.investment_score >= 60
  AND d.alex_review_status = 'pending'
ORDER BY d.investment_score DESC, d.created_at DESC;

-- View for pipeline health monitoring
CREATE VIEW pipeline_health AS
SELECT 
    ds.name as source_name,
    ds.type as source_type,
    ds.is_active,
    ds.reliability_score,
    ds.last_scraped_at,
    ds.error_count,
    COUNT(d.id) as deals_found_last_7_days
FROM data_sources ds
LEFT JOIN deals d ON d.source_name = ds.name 
    AND d.created_at >= NOW() - INTERVAL '7 days'
GROUP BY ds.id, ds.name, ds.type, ds.is_active, ds.reliability_score, ds.last_scraped_at, ds.error_count
ORDER BY ds.reliability_score DESC;

-- =============================================================================
-- HELPER FUNCTIONS
-- =============================================================================

-- Function to calculate Alex's investment score
CREATE OR REPLACE FUNCTION calculate_alex_score(
    funding_stage_param text,
    amount_raised numeric,
    has_ai boolean,
    climate_sectors text[],
    headquarters_country text,
    media_mentions integer DEFAULT 0,
    confidence_score float DEFAULT 0.5
) RETURNS integer AS $$
DECLARE
    score integer := 0;
    target_sectors text[] := ARRAY[
        'Climate Tech - Energy & Grid',
        'Climate Tech - Industrial Software',
        'Climate Tech - Energy Storage', 
        'Climate Tech - Smart Manufacturing',
        'Climate Tech - Carbon & Emissions'
    ];
    filters jsonb;
    stage_filter jsonb;
    ai_filter jsonb;
    sector_filter jsonb;
    geo_filter jsonb;
    size_filter jsonb;
BEGIN
    -- Get current filter settings
    SELECT jsonb_object_agg(setting_name, filter_values) INTO filters
    FROM alex_filter_settings WHERE is_enabled = true;
    
    -- Extract individual filter settings
    stage_filter := filters->'stage_filter';
    ai_filter := filters->'ai_filter';
    sector_filter := filters->'sector_filter';
    geo_filter := filters->'geography_filter';
    size_filter := filters->'funding_size_filter';
    
    -- Stage scoring
    IF stage_filter->>'enabled' = 'true' THEN
        IF LOWER(funding_stage_param) = ANY(ARRAY['seed', 'series a', 'series-a', 'pre-seed']) THEN
            score := score + 30;
        ELSIF stage_filter->>'strict_mode' = 'true' THEN
            RETURN 0;
        ELSIF LOWER(funding_stage_param) = ANY(ARRAY['series b', 'series-b']) THEN
            score := score + 15;
        ELSIF LOWER(funding_stage_param) = ANY(ARRAY['series c', 'series-c', 'growth']) THEN
            score := score + 5;
        END IF;
    END IF;
    
    -- AI requirement
    IF ai_filter->>'enabled' = 'true' THEN
        IF has_ai THEN
            score := score + 25;
        ELSIF ai_filter->>'strict_mode' = 'true' THEN
            RETURN 0;
        ELSE
            score := score - 15;
        END IF;
    END IF;
    
    -- Sector matching
    IF sector_filter->>'enabled' = 'true' THEN
        IF climate_sectors && target_sectors THEN
            score := score + 25;
        ELSIF 'Climate Tech' = ANY(
            SELECT unnest(climate_sectors) 
            WHERE unnest(climate_sectors) LIKE 'Climate Tech%'
        ) THEN
            score := score + 10;
        ELSIF sector_filter->>'strict_mode' = 'true' THEN
            RETURN 0;
        END IF;
    END IF;
    
    -- Geographic preference
    IF geo_filter->>'enabled' = 'true' THEN
        IF headquarters_country = 'US' THEN
            score := score + 10;
        ELSIF headquarters_country IN ('Canada', 'UK') THEN
            score := score + 7;
        ELSIF geo_filter->>'strict_mode' = 'true' AND headquarters_country NOT IN ('US', 'Canada', 'UK') THEN
            score := score - 10;
        END IF;
    END IF;
    
    -- Funding size
    IF size_filter->>'enabled' = 'true' THEN
        IF amount_raised BETWEEN 1000000 AND 8000000 THEN
            score := score + 15;
        ELSIF amount_raised BETWEEN 500000 AND 15000000 THEN
            score := score + 8;
        ELSIF size_filter->>'strict_mode' = 'true' THEN
            IF amount_raised < 500000 OR amount_raised > 15000000 THEN
                RETURN 0;
            END IF;
        ELSE
            IF amount_raised > 15000000 THEN
                score := score - 10;
            ELSIF amount_raised < 500000 THEN
                score := score - 5;
            END IF;
        END IF;
    END IF;
    
    -- Proprietary deal flow bonus
    IF media_mentions < 3 THEN
        score := score + 10;
    ELSIF media_mentions > 10 THEN
        score := score - 5;
    END IF;
    
    -- Data confidence bonus
    score := score + (confidence_score * 10)::integer;
    
    RETURN LEAST(100, GREATEST(0, score));
END;
$$ LANGUAGE plpgsql;

-- Function to update company's updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for updated_at columns
CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON companies FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_deals_updated_at BEFORE UPDATE ON deals FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_investors_updated_at BEFORE UPDATE ON investors FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_data_sources_updated_at BEFORE UPDATE ON data_sources FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_alex_filter_settings_updated_at BEFORE UPDATE ON alex_filter_settings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_alex_deal_views_updated_at BEFORE UPDATE ON alex_deal_views FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- SCHEMA COMPLETE
-- =============================================================================

-- This schema provides:
-- 1. Normalized company and deal data
-- 2. Flexible investor tracking
-- 3. Alex's configurable filter system
-- 4. Enrichment queue for processing
-- 5. Data source health monitoring
-- 6. Performance indexes
-- 7. Alex's scoring function
-- 8. Useful views for dashboard
-- 9. Row Level Security
-- 10. Automatic timestamp updates
