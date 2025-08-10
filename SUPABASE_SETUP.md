# Supabase Dashboard Configuration
# Instructions for connecting Alex's Dashboard to live data

## Step 1: Get Your Supabase Credentials

1. Go to your Supabase project: https://supabase.com/dashboard
2. Select your project (the one where you deployed the climate tech schema)
3. Go to **Settings** → **API**
4. Copy these values:
   - **Project URL** (looks like: `https://your-project-id.supabase.co`)
   - **anon/public key** (starts with `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`)

## Step 2: Update Dashboard Configuration

Open `alex_dashboard.html` and find this section (around line 470):

```javascript
// Configuration - Replace with your actual Supabase credentials
const SUPABASE_CONFIG = {
    url: 'YOUR_SUPABASE_URL', // Replace with your project URL
    key: 'YOUR_SUPABASE_ANON_KEY' // Replace with your anon key
};
```

Replace with your actual values:

```javascript
const SUPABASE_CONFIG = {
    url: 'https://your-project-id.supabase.co',
    key: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
};
```

## Step 3: Deploy the Scoring System (Required)

Before the dashboard can show live data with scores, you need to apply Alex's scoring algorithm to your existing deals:

1. Go to your Supabase dashboard
2. Open the **SQL Editor**
3. Run the content from `alex_scoring_system.sql`

This will:
- Add the `alex_investment_score` column to your deals
- Calculate intelligent scores for all 37 deals
- Set up Alex's investment preferences

## Step 4: Enable Row Level Security (RLS) - Optional

If you want to make the dashboard publicly accessible:

```sql
-- Enable RLS on relevant tables
ALTER TABLE deals_new ENABLE ROW LEVEL SECURITY;
ALTER TABLE companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE investors ENABLE ROW LEVEL SECURITY;
ALTER TABLE deal_investors ENABLE ROW LEVEL SECURITY;

-- Allow public read access for dashboard
CREATE POLICY "Public read access" ON deals_new FOR SELECT USING (true);
CREATE POLICY "Public read access" ON companies FOR SELECT USING (true);
CREATE POLICY "Public read access" ON investors FOR SELECT USING (true);
CREATE POLICY "Public read access" ON deal_investors FOR SELECT USING (true);
```

## Step 5: Test the Connection

1. Open `alex_dashboard.html` in your browser
2. Check the browser console (F12) for any connection errors
3. You should see: "✅ Loaded X deals from Supabase"

## Dashboard Features with Live Data

Once connected, your dashboard will display:

### Real-time Data
- **37 actual deals** from your Supabase database
- **Live investment scores** calculated by Alex's algorithm
- **Company information** including sectors, locations, descriptions
- **Investor networks** showing who funded each deal
- **Deal metadata** like dates, amounts, stages

### Enhanced Filtering
- **Score-based filtering** (Alex's intelligent scoring)
- **AI-focus detection** (companies using AI technology)
- **Geographic filtering** (focus on US/North America)
- **Sector filtering** (Industrial, Energy, Transport, etc.)
- **Stage filtering** (Seed, Series A/B preference)
- **Full-text search** across companies, descriptions, sectors

### Auto-refresh
- Dashboard refreshes every 5 minutes
- Always shows the latest deal data
- Perfect for monitoring new opportunities

## Troubleshooting

### "Failed to load live data" Error
- Check your Supabase URL and API key
- Verify your project is active
- Ensure the tables exist (deals_new, companies, investors, deal_investors)

### "No deals found" 
- Run the migration script to populate deals_new table
- Check if alex_investment_score column exists
- Verify data was migrated correctly

### CORS Errors
- Make sure you're using the anon/public key (not service_role key)
- Supabase automatically handles CORS for browser requests

## Need Help?

1. Check the browser console (F12) for detailed error messages
2. Verify your Supabase project is active and accessible
3. Test the connection with a simple SQL query in Supabase dashboard
4. Make sure all required tables exist with proper schema

---

🎯 **Goal**: Connect Alex's intelligent dashboard to your live climate tech deal database for real-time investment analysis!
