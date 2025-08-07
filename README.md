# Multi-Source Climate & Tech News Scraper

This project contains daily scrapers for climate and technology news from multiple sources.

## Sources
- **TechCrunch** - Startup news and funding announcements
- **Climate Insider** - Exclusive climate industry coverage
- **CTVC** - Climate tech venture capital insights
- **Axios Pro** - Climate deals and investment news

## Setup

### Dependencies
```bash
pip install -r requirements.txt
playwright install chromium  # Required for Axios scraper
```

### Environment Variables
Create a `.env` file with:
```
SUPABASE_URL="your_supabase_url"
SUPABASE_KEY="your_supabase_anon_key"
```

## Usage

### Run Individual Scrapers
```bash
python scrape_techcrunch_daily.py
python scrape_climateinsider_daily.py
python scrape_ctvc_daily.py
python scrape_axios_daily.py
```

## Deployment

This project is designed to run as cron jobs on Render with the following schedule:
- TechCrunch: Daily at 00:05
- Climate Insider: Daily at 00:10
- CTVC: Daily at 00:15
- Axios: Daily at 00:20

All scrapers save articles to the same Supabase database with `status='NEW'` for processing.
