# Scraper Status Dashboard

This file is automatically updated by the monitoring workflow.

## Last Run Status

| Scraper | Status | Last Run |
|---------|--------|----------|
| TechCrunch | ✅ | Check Actions tab |
| Climate Insider | ✅ | Check Actions tab |
| CTVC | ✅ | Check Actions tab |
| Axios | ✅ | Check Actions tab |

## How to Monitor

### 1. **GitHub Actions Tab**
- Go to: https://github.com/Josuevillalona/climate-tech-news-scrapers/actions
- See all workflow runs and their status

### 2. **Manual Testing**
- Click any workflow → "Run workflow" → "Run workflow"
- Watch the logs in real-time

### 3. **Check Your Database**
- Look at your Supabase dashboard
- Check for new articles with `status='NEW'`

### 4. **Email Notifications**
- GitHub will email you if workflows fail
- Go to: Settings → Notifications → Actions

## Troubleshooting

If a scraper fails:
1. Check the logs in GitHub Actions
2. Verify your GitHub Secrets are set correctly
3. Run the scraper manually to test
4. Check if the target website changed structure

## Reliability Notes

- GitHub Actions scheduled workflows are very reliable
- During high load, may be delayed 5-15 minutes (but will still run)
- Free tier includes 2,000 minutes/month (plenty for these scrapers)
- Each scraper takes ~1-3 minutes to run
