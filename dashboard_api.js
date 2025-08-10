// Supabase API Configuration for Alex's Dashboard
class SupabaseAPI {
    constructor() {
        // Replace with your actual Supabase URL and anon key
        this.supabaseUrl = 'YOUR_SUPABASE_URL';
        this.supabaseKey = 'YOUR_SUPABASE_ANON_KEY';
        this.baseUrl = `${this.supabaseUrl}/rest/v1`;
        this.headers = {
            'apikey': this.supabaseKey,
            'Authorization': `Bearer ${this.supabaseKey}`,
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        };
    }

    // Fetch all deals with company and investor data
    async fetchDeals() {
        try {
            console.log('🔗 Making API request to:', `${this.baseUrl}/deals_new`);
            
            // Try simple query first, then enrich with relationships
            const response = await fetch(`${this.baseUrl}/deals_new`, {
                headers: this.headers
            });
            
            console.log('📡 Response status:', response.status);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('❌ API Error Response:', errorText);
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }
            
            const deals = await response.json();
            console.log('📊 Raw deals from API:', deals);
            console.log(`📊 Found ${deals.length} raw deals`);
            
            // Enrich deals with company data
            const enrichedDeals = await this.enrichDealsWithCompanyData(deals);
            console.log('🔄 Enriched deals:', enrichedDeals);
            
            const transformedDeals = this.transformDealsData(enrichedDeals);
            console.log('🔄 Transformed deals:', transformedDeals);
            console.log(`🔄 Transformed to ${transformedDeals.length} deals`);
            
            return transformedDeals;
        } catch (error) {
            console.error('❌ Error fetching deals:', error);
            return [];
        }
    }

    // Enrich deals with company data separately to avoid complex JOIN issues
    async enrichDealsWithCompanyData(deals) {
        try {
            // Get all unique company IDs
            const companyIds = [...new Set(deals.map(deal => deal.company_id).filter(Boolean))];
            console.log('🏢 Fetching company data for IDs:', companyIds);
            
            if (companyIds.length === 0) {
                console.log('⚠️ No company IDs found, returning deals as-is');
                return deals.map(deal => ({ ...deal, companies: null }));
            }
            
            // Fetch companies data
            const companiesResponse = await fetch(
                `${this.baseUrl}/companies?id=in.(${companyIds.join(',')})`, 
                { headers: this.headers }
            );
            
            if (!companiesResponse.ok) {
                console.error('Failed to fetch companies data');
                return deals.map(deal => ({ ...deal, companies: null }));
            }
            
            const companies = await companiesResponse.json();
            console.log('🏢 Fetched companies:', companies);
            
            // Create company lookup map
            const companyMap = {};
            companies.forEach(company => {
                companyMap[company.id] = company;
            });
            
            // Enrich deals with company data
            const enrichedDeals = deals.map(deal => ({
                ...deal,
                companies: companyMap[deal.company_id] || null
            }));
            
            console.log('✨ Enriched deals with company data');
            return enrichedDeals;
            
        } catch (error) {
            console.error('❌ Error enriching with company data:', error);
            return deals.map(deal => ({ ...deal, companies: null }));
        }
    }

    // Transform raw Supabase data to dashboard format
    transformDealsData(deals) {
        return deals.map(deal => {
            const company = deal.companies || {};
            // For now, skip investor relationships to get basic functionality working
            const investors = []; // deal.deal_investors?.map(di => di.investors?.name).filter(Boolean) || [];
            
            return {
                id: deal.id,
                company_name: company.name || deal.company_name || 'Unknown Company',
                alex_investment_score: deal.alex_investment_score || 0,
                funding_stage: this.normalizeFundingStage(deal.funding_stage),
                original_amount: deal.original_amount || 'Unknown',
                amount_usd: deal.amount_usd,
                has_ai_focus: company.has_ai_focus || deal.has_ai_focus || false,
                climate_sectors: this.parseClimateSecors(company.climate_sectors || deal.climate_sectors),
                climate_sub_sectors: this.parseClimateSecors(company.climate_sub_sectors || deal.climate_sub_sectors),
                headquarters_country: company.headquarters_country || deal.headquarters_country || 'Unknown',
                headquarters_city: company.headquarters_city || deal.headquarters_city,
                source_type: deal.source_type || 'unknown',
                deal_date: deal.deal_date,
                investors: investors,
                company_description: company.description || deal.company_description,
                founded_year: company.founded_year,
                employee_count: company.employee_count,
                website: company.website,
                crunchbase_url: deal.crunchbase_url || company.crunchbase_url,
                created_at: deal.created_at
            };
        });
    }

    // Normalize funding stage names
    normalizeFundingStage(stage) {
        if (!stage) return 'Unknown';
        
        const stageMap = {
            'pre-seed': 'Pre-seed',
            'preseed': 'Pre-seed',
            'seed': 'Seed',
            'series-a': 'Series A',
            'series-b': 'Series B',
            'series-c': 'Series C',
            'series-d': 'Series D',
            'bridge': 'Bridge',
            'ipo': 'IPO',
            'acquisition': 'Acquisition'
        };
        
        return stageMap[stage.toLowerCase()] || stage;
    }

    // Parse climate sectors (handle both string and array formats)
    parseClimateSecors(sectors) {
        if (!sectors) return [];
        if (Array.isArray(sectors)) return sectors;
        if (typeof sectors === 'string') {
            // Handle JSON string format
            try {
                const parsed = JSON.parse(sectors);
                return Array.isArray(parsed) ? parsed : [sectors];
            } catch {
                // Handle comma-separated string
                return sectors.split(',').map(s => s.trim()).filter(Boolean);
            }
        }
        return [];
    }

    // Fetch dashboard statistics
    async fetchDashboardStats() {
        try {
            const deals = await this.fetchDeals();
            
            const totalDeals = deals.length;
            const highPriority = deals.filter(d => d.alex_investment_score >= 70).length;
            const aiDeals = deals.filter(d => d.has_ai_focus).length;
            const avgScore = totalDeals > 0 ? 
                deals.reduce((sum, d) => sum + d.alex_investment_score, 0) / totalDeals : 0;
            
            // Additional insights
            const topSectors = this.getTopSectors(deals);
            const recentDeals = deals.filter(d => {
                if (!d.deal_date) return false;
                const dealDate = new Date(d.deal_date);
                const thirtyDaysAgo = new Date();
                thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
                return dealDate >= thirtyDaysAgo;
            }).length;
            
            return {
                totalDeals,
                highPriority,
                aiDeals,
                avgScore: Math.round(avgScore * 10) / 10,
                topSectors,
                recentDeals,
                deals
            };
        } catch (error) {
            console.error('Error fetching dashboard stats:', error);
            return {
                totalDeals: 0,
                highPriority: 0,
                aiDeals: 0,
                avgScore: 0,
                topSectors: [],
                recentDeals: 0,
                deals: []
            };
        }
    }

    // Get top climate sectors
    getTopSectors(deals) {
        const sectorCount = {};
        deals.forEach(deal => {
            const sectors = [...deal.climate_sectors, ...deal.climate_sub_sectors];
            sectors.forEach(sector => {
                sectorCount[sector] = (sectorCount[sector] || 0) + 1;
            });
        });
        
        return Object.entries(sectorCount)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 5)
            .map(([sector, count]) => ({ sector, count }));
    }

    // Search deals with advanced filtering
    searchDeals(deals, filters) {
        return deals.filter(deal => {
            // Score filter
            if (filters.minScore && deal.alex_investment_score < filters.minScore) {
                return false;
            }
            
            // Stage filter
            if (filters.stage && !deal.funding_stage?.toLowerCase().includes(filters.stage.toLowerCase())) {
                return false;
            }
            
            // AI filter
            if (filters.aiFilter === 'true' && !deal.has_ai_focus) return false;
            if (filters.aiFilter === 'false' && deal.has_ai_focus) return false;
            
            // Country filter
            if (filters.country && !deal.headquarters_country?.toLowerCase().includes(filters.country.toLowerCase())) {
                return false;
            }
            
            // Sector filter
            if (filters.sector) {
                const allSectors = [...deal.climate_sectors, ...deal.climate_sub_sectors];
                if (!allSectors.some(s => s.toLowerCase().includes(filters.sector.toLowerCase()))) {
                    return false;
                }
            }
            
            // Search filter (company name, description, sectors)
            if (filters.search) {
                const searchTerm = filters.search.toLowerCase();
                const searchableText = [
                    deal.company_name,
                    deal.company_description,
                    deal.funding_stage,
                    deal.headquarters_country,
                    deal.headquarters_city,
                    ...deal.climate_sectors,
                    ...deal.climate_sub_sectors,
                    ...deal.investors
                ].join(' ').toLowerCase();
                
                if (!searchableText.includes(searchTerm)) {
                    return false;
                }
            }
            
            return true;
        }).sort((a, b) => b.alex_investment_score - a.alex_investment_score);
    }

    // Format currency amounts
    formatAmount(amount, usdAmount) {
        if (usdAmount && usdAmount > 0) {
            return this.formatCurrency(usdAmount);
        }
        if (amount && typeof amount === 'string') {
            return amount;
        }
        return 'Unknown';
    }

    formatCurrency(amount) {
        if (amount >= 1000000000) {
            return `$${(amount / 1000000000).toFixed(1)}B`;
        } else if (amount >= 1000000) {
            return `$${(amount / 1000000).toFixed(1)}M`;
        } else if (amount >= 1000) {
            return `$${(amount / 1000).toFixed(0)}K`;
        } else {
            return `$${amount.toLocaleString()}`;
        }
    }

    // Get color for investment score
    getScoreColor(score) {
        if (score >= 80) return '#22543d'; // Dark green
        if (score >= 70) return '#2b6cb0'; // Blue
        if (score >= 60) return '#d69e2e'; // Orange
        return '#e53e3e'; // Red
    }

    // Get priority level
    getPriorityLevel(score) {
        if (score >= 80) return 'Highest';
        if (score >= 70) return 'High';
        if (score >= 60) return 'Medium';
        return 'Low';
    }
}

// Initialize API
const dashboardAPI = new SupabaseAPI();

// Export for use in dashboard
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SupabaseAPI;
}
