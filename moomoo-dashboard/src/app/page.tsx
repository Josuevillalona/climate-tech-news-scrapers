'use client';

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, TrendingUp, DollarSign, Users, Building2, Settings, Bell, Filter, MoreHorizontal, Loader2, AlertCircle, FileText, BarChart3, Globe } from "lucide-react";
import { useDeals, useDashboardStats } from "@/hooks/useData";
import { formatLargeNumber } from "@/lib/utils";
import { FilterProvider, useFilters } from "@/contexts/FilterContext";
import FilterPanel from "@/components/FilterPanel";
import AlertsPanel from "@/components/AlertsPanel";
import CreateAlertModal from "@/components/CreateAlertModal";
import NewsIntelligenceFeed from "@/components/NewsIntelligenceFeed";
import CompanySignalsWidget from "@/components/CompanySignalsWidget";
import ReportGenerationPanel from "@/components/ReportGenerationPanel";
import FundingTrendsChart from "@/components/charts/FundingTrendsChart";

type ActiveView = 'deals' | 'news' | 'signals' | 'reports';

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
  if (!deals || deals.length === 0) return null;
  
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
    topLocation: topCountry ? topCountry[0] : 'Global',
    avgDealSize: Math.round(avgDealSize)
  };
}

function DashboardContent() {
  const { filters, activeFilterCount } = useFilters();
  const { deals, loading: dealsLoading, error: dealsError } = useDeals(filters);
  const { stats, loading: statsLoading } = useDashboardStats();
  const [showCreateAlert, setShowCreateAlert] = useState(false);
  const [activeView, setActiveView] = useState<ActiveView>('deals');
  const [showMobileMenu, setShowMobileMenu] = useState(false);

  // Calculate quick insights from real deals data
  const quickInsights = getSectorInsights(deals);

  const getStageVariant = (stage: string): "error" | "warning" | "success" | "secondary" | "outline" | "climate" | "default" => {
    if (!stage) return 'outline';
    switch (stage.toLowerCase()) {
      case 'seed':
      case 'pre-seed':
        return 'warning';
      case 'series a':
        return 'success';
      case 'series b':
      case 'series c':
        return 'secondary';
      default:
        return 'outline';
    }
  };

  const getSectorVariant = (sectors: string[]): "error" | "warning" | "success" | "secondary" | "outline" | "climate" | "default" => {
    if (!sectors || sectors.length === 0) return 'climate';
    if (sectors.some(s => s && (s.includes('AI') || s.includes('Software')))) {
      return 'climate';
    }
    return 'climate';
  };

  return (
    <div className="min-h-screen bg-white text-gray-900 flex">
      {/* Left Sidebar - Beautiful Blue - Mobile Responsive */}
      <div className="hidden md:flex w-64 flex-col shadow-lg" style={{ backgroundColor: '#69B8E5' }}>
        {/* Logo */}
        <div className="p-6">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center">
              <Building2 className="h-5 w-5 text-white" />
            </div>
            <span className="text-white font-semibold">MooMoo Climate</span>
          </div>
        </div>
        
        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2">
          <button 
            onClick={() => setActiveView('deals')}
            className={`w-full flex items-center justify-start text-left rounded-2xl h-12 px-4 font-medium transition-all duration-200 ${
              activeView === 'deals' 
                ? 'text-gray-900 font-semibold shadow-sm' 
                : 'text-white/80 hover:bg-white/10 hover:text-white'
            }`}
            style={activeView === 'deals' ? { backgroundColor: '#F7D774' } : {}}
          >
            <DollarSign className="h-5 w-5 mr-3" />
            Deals
          </button>
          <button 
            onClick={() => setActiveView('news')}
            className={`w-full flex items-center justify-start text-left rounded-2xl h-12 px-4 font-medium transition-all duration-200 ${
              activeView === 'news' 
                ? 'text-gray-900 font-semibold shadow-sm' 
                : 'text-white/80 hover:bg-white/10 hover:text-white'
            }`}
            style={activeView === 'news' ? { backgroundColor: '#F7D774' } : {}}
          >
            <Globe className="h-5 w-5 mr-3" />
            Climate Tech News
          </button>
          <button 
            onClick={() => setActiveView('signals')}
            className={`w-full flex items-center justify-start text-left rounded-2xl h-12 px-4 font-medium transition-all duration-200 ${
              activeView === 'signals' 
                ? 'text-gray-900 font-semibold shadow-sm' 
                : 'text-white/80 hover:bg-white/10 hover:text-white'
            }`}
            style={activeView === 'signals' ? { backgroundColor: '#F7D774' } : {}}
          >
            <BarChart3 className="h-5 w-5 mr-3" />
            Company Signals
          </button>
          <button 
            onClick={() => setActiveView('reports')}
            className={`w-full flex items-center justify-start text-left rounded-2xl h-12 px-4 font-medium transition-all duration-200 ${
              activeView === 'reports' 
                ? 'text-gray-900 font-semibold shadow-sm' 
                : 'text-white/80 hover:bg-white/10 hover:text-white'
            }`}
            style={activeView === 'reports' ? { backgroundColor: '#F7D774' } : {}}
          >
            <FileText className="h-5 w-5 mr-3" />
            Reports
          </button>
          
          {/* Additional Navigation Items */}
          <button className="w-full flex items-center justify-start text-left text-white/80 hover:bg-white/10 hover:text-white rounded-2xl h-12 px-4 font-medium transition-all duration-200">
            <Bell className="h-5 w-5 mr-3" />
            Notifications
          </button>
          <button className="w-full flex items-center justify-start text-left text-white/80 hover:bg-white/10 hover:text-white rounded-2xl h-12 px-4 font-medium transition-all duration-200">
            <Settings className="h-5 w-5 mr-3" />
            Settings
          </button>
        </nav>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col bg-gray-50">
        {/* Mobile Header - Only visible on small screens */}
        <div className="md:hidden bg-white shadow-sm border-b border-gray-200 px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ backgroundColor: '#69B8E5' }}>
                <Building2 className="h-5 w-5 text-white" />
              </div>
              <span className="font-semibold text-gray-900">MooMoo Climate</span>
            </div>
            <button 
              onClick={() => setShowMobileMenu(!showMobileMenu)}
              className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
          
          {/* Mobile Menu Dropdown */}
          {showMobileMenu && (
            <div className="mt-4 pb-4 border-t border-gray-200 pt-4">
              <nav className="space-y-2">
                {[
                  { key: 'deals', label: 'Deals', icon: DollarSign },
                  { key: 'news', label: 'Climate Tech News', icon: Globe },
                  { key: 'signals', label: 'Company Signals', icon: BarChart3 },
                  { key: 'reports', label: 'Reports', icon: FileText }
                ].map(({ key, label, icon: Icon }) => (
                  <button
                    key={key}
                    onClick={() => {
                      setActiveView(key as ActiveView);
                      setShowMobileMenu(false);
                    }}
                    className={`w-full flex items-center justify-start text-left rounded-2xl px-4 py-3 font-medium transition-all duration-200 ${
                      activeView === key 
                        ? 'text-gray-900 font-semibold shadow-sm' 
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                    style={activeView === key ? { backgroundColor: '#F7D774' } : {}}
                  >
                    <Icon className="h-5 w-5 mr-3" />
                    {label}
                  </button>
                ))}
              </nav>
            </div>
          )}
        </div>

        {/* Top Header */}
        <header className="bg-white shadow-sm border-b border-gray-200 px-4 md:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3 md:space-x-6">
              <h2 className="text-xl md:text-3xl font-bold text-gray-900">
                {activeView === 'deals' && 'Recent Funding Rounds'}
                {activeView === 'news' && 'Climate Tech News Intelligence'}
                {activeView === 'signals' && 'Company Signals Intelligence'}
                {activeView === 'reports' && 'Professional Reports'}
              </h2>
              <Button variant="outline" size="sm" className="hidden md:flex text-gray-700 border-gray-200 hover:bg-gray-50 rounded-lg px-4 py-2 font-medium">
                + Add widgets
              </Button>
              <Button variant="ghost" size="sm" className="hidden md:flex text-gray-600 hover:bg-gray-50 rounded-lg px-4 py-2 font-medium">
                <Settings className="h-4 w-4 mr-2" />
                Refresh
              </Button>
              <div className="flex items-center space-x-2 bg-green-50 px-3 py-2 rounded-full border border-green-200">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm text-green-700 font-medium">Live</span>
              </div>
            </div>
            
            <div className="flex items-center space-x-3 md:space-x-6">
              <div className="relative hidden md:block">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  placeholder="Search Climate Data"
                  className="pl-12 w-80 bg-white border border-gray-200 text-gray-900 rounded-lg h-12 focus:ring-1 focus:ring-moo-yellow focus:border-moo-yellow shadow-sm"
                />
              </div>
              <Button variant="ghost" size="sm" className="hidden md:flex text-gray-600 hover:bg-gray-50 rounded-lg px-4 py-2 font-medium">
                Help
              </Button>
              <div className="flex items-center space-x-3">
                <div className="w-8 md:w-10 h-8 md:h-10 rounded-xl flex items-center justify-center shadow-sm" style={{ background: 'linear-gradient(135deg, #69B8E5, #4A90B8)' }}>
                  <span className="text-xs md:text-sm font-bold text-white">AC</span>
                </div>
                <span className="hidden md:block text-sm font-medium text-gray-700">Alex Chen</span>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 p-4 md:p-8 space-y-6 md:space-y-8 overflow-auto">
          {/* Welcome Section */}
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-2">Welcome back, Alex</h2>
              <p className="text-base md:text-lg text-gray-600">
                {activeView === 'deals' && "Here's what's happening in climate tech funding today"}
                {activeView === 'news' && "Stay updated with the latest climate tech intelligence"}
                {activeView === 'signals' && "Monitor company signals and market movements"}
                {activeView === 'reports' && "Generate and manage your investment reports"}
              </p>
            </div>
            {activeView === 'deals' && (
              <div className="flex items-center space-x-4">
                <Badge variant="success" className="px-4 py-2 rounded-full shadow-sm font-medium">
                  {deals.filter(d => d.score >= 70).length} High Score
                </Badge>
                <Badge variant="warning" className="px-4 py-2 rounded-full shadow-sm font-medium">
                  {deals.filter(d => d.reviewStatus?.toLowerCase().includes('pending') || d.reviewStatus === 'PENDING_REVIEW').length} Pending Review
                </Badge>
              </div>
            )}
          </div>

          {/* Deals View */}
          {activeView === 'deals' && (
            <>
              {/* Filter and Alert Panels */}
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                <FilterPanel onCreateAlert={() => setShowCreateAlert(true)} />
                <AlertsPanel />
              </div>

              {/* Analytics and Trends */}
              <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
                <div className="xl:col-span-2">
                  <FundingTrendsChart />
                </div>
                <div className="space-y-6">
                  {/* Quick Insights with Real Data */}
                  <Card className="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all duration-200">
                    <CardHeader className="pb-4">
                      <CardTitle className="text-lg font-semibold text-gray-900">
                        Quick Insights
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      {dealsLoading ? (
                        <div className="flex items-center justify-center py-8">
                          <Loader2 className="h-6 w-6 animate-spin text-[#2E5E4E]" />
                          <span className="ml-2 text-gray-700">Loading insights...</span>
                        </div>
                      ) : quickInsights ? (
                        <>
                          <div className="flex items-center justify-between p-4 bg-[#2E5E4E]/5 rounded-xl border border-[#2E5E4E]/10">
                            <span className="text-sm font-medium text-[#2E5E4E]">Hot Sector</span>
                            <span className="text-sm font-semibold text-gray-900">{quickInsights.hotSector}</span>
                          </div>
                          <div className="flex items-center justify-between p-4 bg-[#F7D774]/10 rounded-xl border border-[#F7D774]/20">
                            <span className="text-sm font-medium text-gray-900">Avg Deal Size</span>
                            <span className="text-sm font-semibold text-gray-900">
                              {quickInsights.avgDealSize > 0 ? `$${quickInsights.avgDealSize}M` : 'Calculating...'}
                            </span>
                          </div>
                          <div className="flex items-center justify-between p-4 bg-[#AEE1F6]/20 rounded-xl border border-[#AEE1F6]/30">
                            <span className="text-sm font-medium text-[#2E5E4E]">Top Location</span>
                            <span className="text-sm font-semibold text-gray-900">{quickInsights.topLocation}</span>
                          </div>
                        </>
                      ) : (
                        <div className="text-center py-8 text-gray-500">
                          <p className="font-medium">No insights available yet</p>
                          <p className="text-xs text-gray-400 mt-1">Data will update as deals are processed</p>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                </div>
              </div>

              {/* Stats Overview */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <Card className="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all duration-200">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
                    <CardTitle className="text-sm font-semibold text-gray-900">
                      Deals
                    </CardTitle>
                    <div className="p-2 bg-[#2E5E4E]/10 rounded-xl">
                      <Building2 className="h-5 w-5 text-[#2E5E4E]" />
                    </div>
                  </CardHeader>
                  <CardContent>
                    {statsLoading ? (
                      <Loader2 className="h-8 w-8 animate-spin text-[#2E5E4E]" />
                    ) : (
                      <>
                        <div className="text-4xl font-bold text-gray-900 mb-2">
                          {stats.totalDeals.toLocaleString()}
                        </div>
                        <p className="text-sm text-[#2E5E4E] flex items-center font-medium">
                          <TrendingUp className="w-4 h-4 mr-1" />
                          Processing pipeline
                        </p>
                      </>
                    )}
                  </CardContent>
                </Card>

                <Card className="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all duration-200">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
                    <CardTitle className="text-sm font-semibold text-gray-900">
                      Volume
                    </CardTitle>
                    <div className="p-2 bg-[#F7D774]/20 rounded-xl">
                      <DollarSign className="h-5 w-5 text-gray-900" />
                    </div>
                  </CardHeader>
                  <CardContent>
                    {statsLoading ? (
                      <Loader2 className="h-8 w-8 animate-spin text-[#2E5E4E]" />
                    ) : (
                      <>
                        <div className="text-4xl font-bold text-gray-900 mb-2">
                          ${formatLargeNumber(stats.totalFunding)}
                        </div>
                        <p className="text-sm text-[#2E5E4E] flex items-center font-medium">
                          <TrendingUp className="w-4 h-4 mr-1" />
                          Total tracked funding
                        </p>
                      </>
                    )}
                  </CardContent>
                </Card>

                <Card className="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all duration-200">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
                    <CardTitle className="text-sm font-semibold text-gray-900">
                      Avg. Deal
                    </CardTitle>
                    <div className="p-2 bg-[#AEE1F6]/30 rounded-xl">
                      <TrendingUp className="h-5 w-5 text-[#2E5E4E]" />
                    </div>
                  </CardHeader>
                  <CardContent>
                    {statsLoading ? (
                      <Loader2 className="h-8 w-8 animate-spin text-[#2E5E4E]" />
                    ) : (
                      <>
                        <div className="text-4xl font-bold text-gray-900 mb-2">
                          ${formatLargeNumber(stats.avgDealSize)}
                        </div>
                        <p className="text-sm text-[#2E5E4E] flex items-center font-medium">
                          <TrendingUp className="w-4 h-4 mr-1" />
                          Climate tech average
                        </p>
                      </>
                    )}
                  </CardContent>
                </Card>

                <Card className="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all duration-200">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
                    <CardTitle className="text-sm font-semibold text-gray-900">
                      Avg Score
                    </CardTitle>
                    <div className="p-2 bg-[#F3F3F3] rounded-xl">
                      <Users className="h-5 w-5 text-gray-700" />
                    </div>
                  </CardHeader>
                  <CardContent>
                    {statsLoading ? (
                      <Loader2 className="h-8 w-8 animate-spin text-[#2E5E4E]" />
                    ) : (
                      <>
                        <div className="text-4xl font-bold text-gray-900 mb-2">
                          {stats.avgScore.toFixed(1)}/10
                        </div>
                        <p className="text-sm text-[#2E5E4E] flex items-center font-medium">
                          <TrendingUp className="w-4 h-4 mr-1" />
                          Alex's filter match
                        </p>
                      </>
                    )}
                  </CardContent>
                </Card>
              </div>

              {/* Recent Funding Rounds - Main Table */}
              <Card className="bg-white rounded-xl shadow-sm border border-gray-200">
                <CardHeader className="pb-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <CardTitle className="text-2xl font-bold text-gray-900">Recent Funding Rounds</CardTitle>
                      <div className="flex items-center space-x-3">
                        <span className="text-sm text-gray-600 font-medium">
                          Showing {deals.length} deals
                        </span>
                    {filters.stages.length > 0 && (
                      <Badge variant="outline" className="text-xs border-gray-300 text-gray-700 rounded-full">
                        {filters.stages.length} stage{filters.stages.length > 1 ? 's' : ''}
                      </Badge>
                    )}
                    {filters.hasAiFocus === true && (
                      <Badge variant="secondary" className="text-xs bg-blue-100 text-blue-800 rounded-full">
                        AI Focus
                      </Badge>
                    )}
                    {filters.minScore > 0 && (
                      <Badge variant="secondary" className="text-xs bg-blue-100 text-blue-800 rounded-full">
                        Score ≥{filters.minScore}
                      </Badge>
                    )}
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <Button variant="ghost" size="sm" className="text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-lg px-3 py-2">
                    Export
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-0">
              {dealsError ? (
                <div className="flex items-center justify-center p-8 text-red-600">
                  <AlertCircle className="w-5 h-5 mr-2" />
                  {dealsError}
                </div>
              ) : dealsLoading ? (
                <div className="flex items-center justify-center p-8">
                  <Loader2 className="h-6 w-6 animate-spin text-gray-400 mr-2" />
                  <span className="text-gray-600">Loading deals...</span>
                </div>
              ) : (
                <div className="overflow-hidden rounded-lg">
                  <table className="w-full">
                    <thead>
                      <tr className="bg-gray-50 border-b border-gray-200">
                        <th className="text-left px-6 py-4 text-sm font-semibold text-gray-700">
                          Company
                        </th>
                        <th className="text-left px-6 py-4 text-sm font-semibold text-gray-700">
                          Amount
                        </th>
                        <th className="text-left px-6 py-4 text-sm font-semibold text-gray-700">
                          Stage
                        </th>
                        <th className="text-left px-6 py-4 text-sm font-semibold text-gray-700">
                          Sector
                        </th>
                        <th className="text-left px-6 py-4 text-sm font-semibold text-gray-700">
                          Date
                        </th>
                        <th className="text-left px-6 py-4 text-sm font-semibold text-gray-700">
                          Score
                        </th>
                        <th className="w-10"></th>
                      </tr>
                    </thead>
                    <tbody>
                      {deals.map((deal) => (
                        <tr key={deal.id} className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                          <td className="px-6 py-4">
                            <div className="flex items-center space-x-3">
                              <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                                deal.hasAiFocus ? 'bg-blue-50' : 'bg-green-50'
                              }`}>
                                <span className={`text-sm font-semibold ${
                                  deal.hasAiFocus ? 'text-blue-600' : 'text-green-600'
                                }`}>
                                  {deal.companyName.substring(0, 2).toUpperCase()}
                                </span>
                              </div>
                              <div>
                                <div className="font-semibold text-gray-900">{deal.companyName}</div>
                                <div className="text-sm text-gray-500 truncate max-w-xs">
                                  {deal.companyDescription}
                                </div>
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4 font-semibold text-gray-900">{deal.amount}</td>
                          <td className="px-6 py-4">
                            <Badge variant={getStageVariant(deal.stage)} className="rounded-lg px-3 py-1 font-medium">{deal.stage}</Badge>
                          </td>
                          <td className="px-6 py-4">
                            <Badge variant={getSectorVariant(deal.sector)} className="rounded-lg px-3 py-1 font-medium">
                              {deal.sector[0] || 'Climate Tech'}
                            </Badge>
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-500">{deal.date}</td>
                          <td className="px-6 py-4">
                            <div className="flex items-center space-x-2">
                              <div className={`w-2.5 h-2.5 rounded-full ${
                                deal.scoreColor === 'green' ? 'bg-green-500' :
                                deal.scoreColor === 'yellow' ? 'bg-yellow-500' : 'bg-red-500'
                              }`}></div>
                              <span className="text-sm font-semibold text-gray-900">{deal.score}</span>
                            </div>
                          </td>
                          <td className="px-6 py-4">
                            <Button 
                              variant="ghost" 
                              size="icon" 
                              className="h-8 w-8 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg"
                              onClick={() => window.open(deal.sourceUrl, '_blank')}
                            >
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {deals.length === 0 && (
                    <div className="text-center p-12 text-gray-500">
                      <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
                        <Building2 className="w-8 h-8 text-gray-400" />
                      </div>
                      <p className="text-lg font-medium mb-2">No deals found</p>
                      <p className="text-sm">Check your database connection or adjust your filters.</p>
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        </>
      )}

      {/* News View */}
      {activeView === 'news' && (
        <>
          <NewsIntelligenceFeed />
        </>
      )}

      {/* Company Signals View */}
      {activeView === 'signals' && (
        <>
          <CompanySignalsWidget />
        </>
      )}

      {/* Reports View */}
      {activeView === 'reports' && (
        <>
          <ReportGenerationPanel />
        </>
      )}
        </main>

        {/* Create Alert Modal */}
        <CreateAlertModal 
          isOpen={showCreateAlert} 
          onClose={() => setShowCreateAlert(false)} 
        />
      </div>
    </div>
  );
}

export default function Dashboard() {
  return (
    <FilterProvider>
      <DashboardContent />
    </FilterProvider>
  );
}
