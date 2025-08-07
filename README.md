# Multi-Source Climate & Tech News Scraper

This project contains automated daily scrapers for climate and technology news from multiple sources using GitHub Actions.

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
For local development, create a `.env` file with:
```
SUPABASE_URL="your_supabase_url"
SUPABASE_KEY="your_supabase_anon_key"
```

## Usage

### Run Individual Scrapers Locally
```bash
python scrape_techcrunch_daily.py
python scrape_climateinsider_daily.py
python scrape_ctvc_daily.py
python scrape_axios_daily.py
```

## Automated Deployment

This project runs automatically using **GitHub Actions** (completely FREE!) with the following schedule:
- **TechCrunch**: Daily at 00:05 UTC
- **Climate Insider**: Daily at 00:10 UTC  
- **CTVC**: Daily at 00:15 UTC
- **Axios**: Daily at 00:20 UTC

### GitHub Secrets Required
Add these secrets in your GitHub repository settings:
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Your Supabase anon key

### Manual Trigger
You can manually trigger any workflow from the GitHub Actions tab for testing.

All scrapers save articles to the same Supabase database with `status='NEW'` for processing.
