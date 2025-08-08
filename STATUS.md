# Scraper Status Dashboard

This file is automatically updated by the monitoring workflow.

## Last Run Status

### Data Collection (Scrapers)
| Scraper | Status | Schedule | Last Run |
|---------|--------|----------|----------|
| TechCrunch | ✅ | 00:05 UTC | Check Actions tab |
| Climate Insider | ✅ | 00:10 UTC | Check Actions tab |
| CTVC | ✅ | 00:15 UTC | Check Actions tab |
| Axios | ✅ | 00:20 UTC | Check Actions tab |

### AI Processing
| Component | Status | Schedule | Last Run |
|-----------|--------|----------|----------|
| AI Article Processor | ✅ | 01:00 UTC | Check Actions tab |
| Monitor | ✅ | 01:00 UTC | Check Actions tab |

## Daily Workflow

1. **00:05 UTC** - TechCrunch scraper collects articles
2. **00:10 UTC** - Climate Insider scraper collects articles  
3. **00:15 UTC** - CTVC scraper collects articles
4. **00:20 UTC** - Axios scraper collects articles
5. **01:00 UTC** - AI processor analyzes all new articles
6. **01:00 UTC** - Monitor checks system health

## How to Monitor

### 1. **GitHub Actions Tab**
- Go to: https://github.com/Josuevillalona/climate-tech-news-scrapers/actions
- See all workflow runs and their status

### 2. **Manual Testing**
- Click any workflow → "Run workflow" → "Run workflow"
- Watch the logs in real-time

### 3. **Check Your Database**
- Look at your Supabase dashboard
- Check for new articles with different status values:
  - `NEW` - Recently scraped, waiting for AI processing
  - `PROCESSED_AI` - Successfully analyzed climate tech funding
  - `IRRELEVANT_TYPE` - Not a funding announcement
  - `IRRELEVANT_SECTOR` - Not climate tech related

### 4. **Email Notifications**
- GitHub will email you if workflows fail
- Go to: Settings → Notifications → Actions

## Troubleshooting

If a scraper fails:
1. Check the logs in GitHub Actions
2. Verify your GitHub Secrets are set correctly
3. Run the scraper manually to test
4. Check if the target website changed structure

If AI processing fails:
1. Check the logs for model loading errors
2. Verify sufficient memory/compute resources
3. Check for new articles in database with `status='NEW'`

## Reliability Notes

- GitHub Actions scheduled workflows are very reliable
- During high load, may be delayed 5-15 minutes (but will still run)
- Free tier includes 2,000 minutes/month
- Each scraper takes ~1-3 minutes to run
- AI processor takes ~3-10 minutes depending on article count
- AI models are downloaded automatically on first run
