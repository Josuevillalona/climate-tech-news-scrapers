# Multi-Source Climate & Tech News Scraper with AI Processing

This project contains automated daily scrapers for climate and technology news from multiple sources, plus an AI processor that analyzes the articles for climate tech funding announcements.

## Architecture

### Data Collection (Scrapers)
- **TechCrunch** - Startup news and funding announcements
- **Climate Insider** - Exclusive climate industry coverage
- **CTVC** - Climate tech venture capital insights
- **Axios Pro** - Climate deals and investment news

### AI Processing Pipeline
- **Article Classification** - Identifies funding announcements vs general news
- **Sector Analysis** - Categorizes companies into climate tech sectors
- **Data Extraction** - Extracts funding amounts, stages, investors, etc.

## Setup

### Dependencies
```bash
pip install -r requirements.txt
playwright install chromium  # Required for Axios scraper
```

### Environment Variables
For local development, create a `.env` file with:
```
SUPABASE_URL="your_supabase_url"
SUPABASE_KEY="your_supabase_anon_key"
```

## Usage

### Run Individual Components Locally
```bash
# Scrapers
python scrape_techcrunch_daily.py
python scrape_climateinsider_daily.py
python scrape_ctvc_daily.py
python scrape_axios_daily.py

# AI Processor
python process_articles_ai.py
```

## Automated Deployment

This project runs automatically using **GitHub Actions** (completely FREE!) with the following schedule:

### Data Collection Phase
- **TechCrunch**: Daily at 00:05 UTC
- **Climate Insider**: Daily at 00:10 UTC  
- **CTVC**: Daily at 00:15 UTC
- **Axios**: Daily at 00:20 UTC

### AI Processing Phase
- **AI Processor**: Daily at 01:00 UTC (after all scrapers complete)
- Analyzes all articles with `status='NEW'`
- Classifies articles and extracts funding data
- Updates database with processed information

### GitHub Secrets Required
Add these secrets in your GitHub repository settings:
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Your Supabase anon key

### Manual Trigger
You can manually trigger any workflow from the GitHub Actions tab for testing.

## Data Flow

1. **Scrapers** collect articles → Save to database with `status='NEW'`
2. **AI Processor** analyzes articles → Updates with extracted data and new status:
   - `PROCESSED_AI` - Successfully analyzed climate tech funding
   - `IRRELEVANT_TYPE` - Not a funding announcement
   - `IRRELEVANT_SECTOR` - Not climate tech related
