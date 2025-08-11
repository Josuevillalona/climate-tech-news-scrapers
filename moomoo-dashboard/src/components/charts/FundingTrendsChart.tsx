'use client';

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingUp, TrendingDown, Calendar, AlertCircle, Loader2 } from "lucide-react";
import { useDeals } from "@/hooks/useData";
import { useMemo } from "react";

interface TrendDataPoint {
  month: string;
  deals: number;
  funding: number;
  avgScore: number;
}

// Helper function to parse funding amounts
function parseFundingAmount(amount: string): number {
  if (!amount || amount === 'Undisclosed') return 0;
  
  const cleanAmount = amount.replace(/[$,\s]/g, '').toLowerCase();
  
  if (cleanAmount.includes('b')) {
    return parseFloat(cleanAmount.replace('b', '')) * 1000;
  } else if (cleanAmount.includes('m')) {
    return parseFloat(cleanAmount.replace('m', ''));
  } else if (cleanAmount.includes('k')) {
    return parseFloat(cleanAmount.replace('k', '')) / 1000;
  } else {
    const numValue = parseFloat(cleanAmount);
    return numValue > 1000 ? numValue / 1000000 : numValue;
  }
}

// Helper function to get sector insights
function getSectorInsights(deals: any[]) {
  const sectorCounts: Record<string, number> = {};
  const countryCounts: Record<string, number> = {};
  let totalFunding = 0;
  let totalDeals = 0;
  
  deals.forEach(deal => {
    // Count sectors
    if (deal.sector && Array.isArray(deal.sector)) {
      deal.sector.forEach((s: string) => {
        sectorCounts[s] = (sectorCounts[s] || 0) + 1;
      });
    }
    
    // Count countries
    if (deal.country) {
      countryCounts[deal.country] = (countryCounts[deal.country] || 0) + 1;
    }
    
    // Sum funding
    totalFunding += parseFundingAmount(deal.amount);
    totalDeals++;
  });
  
  const topSector = Object.entries(sectorCounts).sort((a, b) => b[1] - a[1])[0];
  const topCountry = Object.entries(countryCounts).sort((a, b) => b[1] - a[1])[0];
  const avgDealSize = totalDeals > 0 ? totalFunding / totalDeals : 0;
  
  return {
    hotSector: topSector ? topSector[0] : 'Climate Tech',
    topLocation: topCountry ? topCountry[0] : 'Not Available',
    avgDealSize: Math.round(avgDealSize)
  };
}

export default function FundingTrendsChart() {
  const { deals, loading, error } = useDeals();

  const trendData = useMemo(() => {
    if (!deals || deals.length === 0) return [];

    // Group deals by month
    const monthlyData: Record<string, TrendDataPoint> = {};
    
    deals.forEach(deal => {
      const date = new Date(deal.date);
      const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
      const monthLabel = date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
      
      if (!monthlyData[monthKey]) {
        monthlyData[monthKey] = {
          month: monthLabel,
          deals: 0,
          funding: 0,
          avgScore: 0
        };
      }
      
      monthlyData[monthKey].deals += 1;
      monthlyData[monthKey].funding += parseFundingAmount(deal.amount);
      monthlyData[monthKey].avgScore += deal.score;
    });

    // Calculate average scores and sort by month
    const sortedData = Object.values(monthlyData)
      .map(data => ({
        ...data,
        avgScore: data.deals > 0 ? data.avgScore / data.deals : 0
      }))
      .sort((a, b) => a.month.localeCompare(b.month))
      .slice(-6); // Show last 6 months

    return sortedData;
  }, [deals]);

  const insights = useMemo(() => {
    return getSectorInsights(deals);
  }, [deals]);

  if (loading) {
    return (
      <Card className="bg-white rounded-xl shadow-sm border border-gray-200">
        <CardContent className="flex items-center justify-center h-64">
          <div className="flex items-center space-x-3">
            <Loader2 className="h-6 w-6 animate-spin text-gray-400" />
            <span className="text-gray-600">Loading funding trends...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="bg-white rounded-xl shadow-sm border border-gray-200">
        <CardContent className="flex items-center justify-center h-64">
          <div className="flex items-center space-x-3 text-red-600">
            <AlertCircle className="h-6 w-6" />
            <span>Failed to load funding trends</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (trendData.length === 0) {
    return (
      <Card className="bg-white rounded-xl shadow-sm border border-gray-200">
        <CardContent className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
              <TrendingUp className="w-8 h-8 text-gray-400" />
            </div>
            <p className="text-gray-600">No trend data available</p>
            <p className="text-sm text-gray-500">Data will appear as deals are processed</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const maxDeals = Math.max(...trendData.map(d => d.deals));
  const maxFunding = Math.max(...trendData.map(d => d.funding));
  
  const currentMonth = trendData[trendData.length - 1];
  const previousMonth = trendData[trendData.length - 2];
  
  const dealsTrend = previousMonth ? ((currentMonth.deals - previousMonth.deals) / previousMonth.deals) * 100 : 0;
  const fundingTrend = previousMonth ? ((currentMonth.funding - previousMonth.funding) / previousMonth.funding) * 100 : 0;

  return (
    <Card className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 border border-gray-200">
      <CardHeader className="pb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-purple-50 rounded-lg">
              <TrendingUp className="h-5 w-5 text-purple-600" />
            </div>
            <div>
              <CardTitle className="text-lg font-semibold text-gray-900">
                Funding Trends
              </CardTitle>
              <p className="text-sm text-gray-600">6-month climate tech overview</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Calendar className="h-4 w-4 text-gray-400" />
            <span className="text-sm text-gray-500">Last 6 months</span>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-6">
        {/* Summary Stats */}
        <div className="grid grid-cols-2 gap-4">
          <div className="p-4 bg-blue-50 rounded-lg border border-blue-100">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-blue-900">Total Deals</span>
              <div className={`flex items-center text-xs font-medium ${
                dealsTrend > 0 ? 'text-green-600' : dealsTrend < 0 ? 'text-red-600' : 'text-gray-600'
              }`}>
                {dealsTrend !== 0 && (
                  <>
                    {dealsTrend > 0 ? (
                      <TrendingUp className="h-3 w-3 mr-1" />
                    ) : (
                      <TrendingDown className="h-3 w-3 mr-1" />
                    )}
                    {Math.abs(dealsTrend).toFixed(1)}%
                  </>
                )}
              </div>
            </div>
            <div className="text-2xl font-bold text-blue-900">
              {trendData.reduce((sum, d) => sum + d.deals, 0)}
            </div>
          </div>
          
          <div className="p-4 bg-green-50 rounded-lg border border-green-100">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-green-900">Total Funding</span>
              <div className={`flex items-center text-xs font-medium ${
                fundingTrend > 0 ? 'text-green-600' : fundingTrend < 0 ? 'text-red-600' : 'text-gray-600'
              }`}>
                {fundingTrend !== 0 && (
                  <>
                    {fundingTrend > 0 ? (
                      <TrendingUp className="h-3 w-3 mr-1" />
                    ) : (
                      <TrendingDown className="h-3 w-3 mr-1" />
                    )}
                    {Math.abs(fundingTrend).toFixed(1)}%
                  </>
                )}
              </div>
            </div>
            <div className="text-2xl font-bold text-green-900">
              ${(trendData.reduce((sum, d) => sum + d.funding, 0) / 1000).toFixed(1)}B
            </div>
          </div>
        </div>

        {/* Simple Bar Chart */}
        <div className="space-y-4">
          <h4 className="text-sm font-medium text-gray-700">Monthly Deal Volume</h4>
          <div className="space-y-3">
            {trendData.map((dataPoint, index) => (
              <div key={dataPoint.month} className="flex items-center space-x-3">
                <span className="text-sm text-gray-600 w-12">{dataPoint.month}</span>
                <div className="flex-1 flex items-center space-x-2">
                  <div className="flex-1 bg-gray-100 rounded-full h-2 overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-blue-400 to-blue-600 rounded-full transition-all duration-500 ease-out"
                      style={{ 
                        width: maxDeals > 0 ? `${(dataPoint.deals / maxDeals) * 100}%` : '0%',
                        animationDelay: `${index * 100}ms`
                      }}
                    />
                  </div>
                  <span className="text-sm font-medium text-gray-900 w-8">
                    {dataPoint.deals}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Funding Chart */}
        <div className="space-y-4">
          <h4 className="text-sm font-medium text-gray-700">Monthly Funding ($M)</h4>
          <div className="space-y-3">
            {trendData.map((dataPoint, index) => (
              <div key={`funding-${dataPoint.month}`} className="flex items-center space-x-3">
                <span className="text-sm text-gray-600 w-12">{dataPoint.month}</span>
                <div className="flex-1 flex items-center space-x-2">
                  <div className="flex-1 bg-gray-100 rounded-full h-2 overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-green-400 to-green-600 rounded-full transition-all duration-500 ease-out"
                      style={{ 
                        width: maxFunding > 0 ? `${(dataPoint.funding / maxFunding) * 100}%` : '0%',
                        animationDelay: `${index * 100}ms`
                      }}
                    />
                  </div>
                  <span className="text-sm font-medium text-gray-900 w-12 text-right">
                    ${dataPoint.funding.toFixed(0)}M
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
