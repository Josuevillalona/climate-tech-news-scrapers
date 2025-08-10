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
// import AlertsPanel from "@/components/AlertsPanel"; // Temporarily disabled
// import CreateAlertModal from "@/components/CreateAlertModal"; // Temporarily disabled
import NewsIntelligenceFeed from "@/components/NewsIntelligenceFeed";
import CompanySignalsWidget from "@/components/CompanySignalsWidget";
import ReportGenerationPanel from "@/components/ReportGenerationPanel";

type ActiveView = 'deals' | 'news' | 'signals' | 'reports';

function DashboardContent() {
  const { filters, activeFilterCount } = useFilters();
  const { deals, loading: dealsLoading, error: dealsError } = useDeals(filters);
  const { stats, loading: statsLoading } = useDashboardStats();
  const [showCreateAlert, setShowCreateAlert] = useState(false);
  const [activeView, setActiveView] = useState<ActiveView>('deals');

  const getStageVariant = (stage: string): "error" | "warning" | "success" | "secondary" | "outline" | "climate" | "default" => {
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
    if (sectors.some(s => s.includes('AI') || s.includes('Software'))) {
      return 'climate';
    }
    return 'climate';
  };

  return (
    <div className="min-h-screen bg-[#F3F3F3] text-[#2D2D2D] flex">
      {/* Left Sidebar */}
      <div className="w-64 bg-gradient-to-b from-[#4285F4] to-[#3367D6] text-white flex flex-col shadow-2xl">
        {/* Logo */}
        <div className="p-6 border-b border-white/10">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-white rounded-2xl flex items-center justify-center shadow-lg">
              <span className="text-[#4285F4] font-bold text-lg">M</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">MooMoo</h1>
              <p className="text-sm text-blue-100">Climate</p>
            </div>
          </div>
        </div>
        
        {/* Navigation */}
        <nav className="flex-1 p-6 space-y-3">
          <Button 
            variant="ghost" 
            onClick={() => setActiveView('deals')}
            className={`w-full justify-start text-left rounded-2xl h-12 font-medium transition-all duration-200 ${
              activeView === 'deals' 
                ? 'bg-[#F7D774] text-[#2D2D2D] hover:bg-[#F7D774]/90 shadow-lg' 
                : 'text-white hover:bg-white/10'
            }`}
          >
            <DollarSign className="h-5 w-5 mr-3" />
            Deals
          </Button>
          <Button 
            variant="ghost" 
            onClick={() => setActiveView('news')}
            className={`w-full justify-start text-left rounded-2xl h-12 font-medium transition-all duration-200 ${
              activeView === 'news' 
                ? 'bg-[#F7D774] text-[#2D2D2D] hover:bg-[#F7D774]/90 shadow-lg' 
                : 'text-white hover:bg-white/10'
            }`}
          >
            <Globe className="h-5 w-5 mr-3" />
            Climate Tech News
          </Button>
          <Button 
            variant="ghost" 
            onClick={() => setActiveView('signals')}
            className={`w-full justify-start text-left rounded-2xl h-12 font-medium transition-all duration-200 ${
              activeView === 'signals' 
                ? 'bg-[#F7D774] text-[#2D2D2D] hover:bg-[#F7D774]/90 shadow-lg' 
                : 'text-white hover:bg-white/10'
            }`}
          >
            <BarChart3 className="h-5 w-5 mr-3" />
            Company Signals
          </Button>
          <Button 
            variant="ghost" 
            onClick={() => setActiveView('reports')}
            className={`w-full justify-start text-left rounded-2xl h-12 font-medium transition-all duration-200 ${
              activeView === 'reports' 
                ? 'bg-[#F7D774] text-[#2D2D2D] hover:bg-[#F7D774]/90 shadow-lg' 
                : 'text-white hover:bg-white/10'
            }`}
          >
            <FileText className="h-5 w-5 mr-3" />
            Reports
          </Button>
          
          {/* Divider */}
          <div className="border-t border-white/10 my-4"></div>
          
          {/* Additional Navigation Items */}
          <Button variant="ghost" className="w-full justify-start text-left text-white hover:bg-white/10 rounded-2xl h-12 font-medium transition-all duration-200">
            <Bell className="h-5 w-5 mr-3" />
            Notifications
          </Button>
          <Button variant="ghost" className="w-full justify-start text-left text-white hover:bg-white/10 rounded-2xl h-12 font-medium transition-all duration-200">
            <Settings className="h-5 w-5 mr-3" />
            Settings
          </Button>
        </nav>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col">
        {/* Top Header */}
        <header className="bg-white shadow-sm px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-6">
              <h2 className="text-2xl font-bold text-[#F7D774]">
                {activeView === 'deals' && 'Recent Funding Rounds'}
                {activeView === 'news' && 'Climate Tech News Intelligence'}
                {activeView === 'signals' && 'Company Signals Intelligence'}
                {activeView === 'reports' && 'Professional Reports'}
              </h2>
              <Button variant="outline" size="sm" className="text-[#2D2D2D] border-gray-300 hover:bg-gray-50 rounded-full px-4 py-2 font-medium transition-all duration-200">
                + Add widgets
              </Button>
              <Button variant="ghost" size="sm" className="text-[#2D2D2D] hover:bg-gray-50 rounded-full px-4 py-2 font-medium transition-all duration-200">
                <Settings className="h-4 w-4 mr-2" />
                Refresh
              </Button>
              <div className="flex items-center space-x-2 bg-green-50 px-3 py-2 rounded-full">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm text-green-700 font-medium">Live</span>
              </div>
            </div>
            
            <div className="flex items-center space-x-6">
              <div className="relative">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  placeholder="Search Climate Data"
                  className="pl-12 w-80 bg-gray-50 border-0 text-[#2D2D2D] rounded-2xl h-12 focus:bg-white focus:shadow-lg transition-all duration-200"
                />
              </div>
              <Button variant="ghost" size="sm" className="text-[#2D2D2D] hover:bg-gray-50 rounded-full px-4 py-2 font-medium transition-all duration-200">
                Help
              </Button>
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg">
                  <span className="text-sm font-bold text-white">AC</span>
                </div>
                <span className="text-sm font-medium text-[#2D2D2D]">Alex Chen</span>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 p-8 space-y-8 bg-[#F3F3F3] overflow-auto">
          {/* Welcome Section */}
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-3xl font-bold text-[#2D2D2D] mb-2">Welcome back, Alex</h2>
              <p className="text-lg text-gray-600">
                {activeView === 'deals' && "Here's what's happening in climate tech funding today"}
                {activeView === 'news' && "Stay updated with the latest climate tech intelligence"}
                {activeView === 'signals' && "Monitor company signals and market movements"}
                {activeView === 'reports' && "Generate and manage your investment reports"}
              </p>
            </div>
            {activeView === 'deals' && (
              <div className="flex items-center space-x-4">
                <Badge variant="success" className="px-4 py-2 bg-green-100 text-green-800 rounded-full shadow-sm font-medium">
                  {deals.filter(d => d.score >= 70).length} High Score
                </Badge>
                <Badge variant="warning" className="px-4 py-2 bg-yellow-100 text-yellow-800 rounded-full shadow-sm font-medium">
                  {deals.filter(d => d.reviewStatus?.toLowerCase().includes('pending') || d.reviewStatus === 'PENDING_REVIEW').length} Pending Review
                </Badge>
              </div>
            )}
          </div>

          {/* Deals View */}
          {activeView === 'deals' && (
            <>
              {/* Filter and Alert Panels */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <FilterPanel onCreateAlert={() => setShowCreateAlert(true)} />
                {/* <AlertsPanel /> - Temporarily disabled due to context issue */}
                <Card className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-shadow duration-300 border-0">
                  <CardHeader className="pb-4">
                    <CardTitle className="text-lg font-bold text-[#2D2D2D] flex items-center">
                      <Bell className="h-5 w-5 mr-2 text-orange-600" />
                      Alert Management
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-600 text-sm">
                      Alert system temporarily unavailable. Working on fixing context provider.
                    </p>
                  </CardContent>
                </Card>
              </div>

              {/* Stats Overview */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <Card className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-shadow duration-300 border-0">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
                    <CardTitle className="text-sm font-semibold text-gray-700">
                      Deals
                    </CardTitle>
                    <div className="p-2 bg-blue-50 rounded-xl">
                      <Building2 className="h-5 w-5 text-blue-600" />
                    </div>
                  </CardHeader>
                  <CardContent>
                    {statsLoading ? (
                      <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
                    ) : (
                      <>
                        <div className="text-4xl font-bold text-[#2D2D2D] mb-2">
                          {stats.totalDeals.toLocaleString()}
                        </div>
                        <p className="text-sm text-green-600 flex items-center font-medium">
                          <TrendingUp className="w-4 h-4 mr-1" />
                          Processing pipeline
                        </p>
                      </>
                    )}
                  </CardContent>
                </Card>

                <Card className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-shadow duration-300 border-0">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
                    <CardTitle className="text-sm font-semibold text-gray-700">
                      Volume
                    </CardTitle>
                    <div className="p-2 bg-green-50 rounded-xl">
                      <DollarSign className="h-5 w-5 text-green-600" />
                    </div>
                  </CardHeader>
                  <CardContent>
                    {statsLoading ? (
                      <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
                    ) : (
                      <>
                        <div className="text-4xl font-bold text-[#2D2D2D] mb-2">
                          ${formatLargeNumber(stats.totalFunding)}
                        </div>
                        <p className="text-sm text-green-600 flex items-center font-medium">
                          <TrendingUp className="w-4 h-4 mr-1" />
                          Total tracked funding
                        </p>
                      </>
                    )}
                  </CardContent>
                </Card>

                <Card className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-shadow duration-300 border-0">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
                    <CardTitle className="text-sm font-semibold text-gray-700">
                      Avg. Deal
                    </CardTitle>
                    <div className="p-2 bg-yellow-50 rounded-xl">
                      <TrendingUp className="h-5 w-5 text-yellow-600" />
                    </div>
                  </CardHeader>
                  <CardContent>
                    {statsLoading ? (
                      <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
                    ) : (
                      <>
                        <div className="text-4xl font-bold text-[#2D2D2D] mb-2">
                          ${formatLargeNumber(stats.avgDealSize)}
                        </div>
                        <p className="text-sm text-yellow-600 flex items-center font-medium">
                          <TrendingUp className="w-4 h-4 mr-1" />
                          Climate tech average
                        </p>
                      </>
                    )}
                  </CardContent>
                </Card>

                <Card className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-shadow duration-300 border-0">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
                    <CardTitle className="text-sm font-semibold text-gray-700">
                      Avg Score
                    </CardTitle>
                    <div className="p-2 bg-purple-50 rounded-xl">
                      <Users className="h-5 w-5 text-purple-600" />
                    </div>
                  </CardHeader>
                  <CardContent>
                    {statsLoading ? (
                      <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
                    ) : (
                      <>
                        <div className="text-4xl font-bold text-[#2D2D2D] mb-2">
                          {stats.avgScore.toFixed(1)}/10
                        </div>
                        <p className="text-sm text-green-600 flex items-center font-medium">
                          <TrendingUp className="w-4 h-4 mr-1" />
                          Alex's filter match
                        </p>
                      </>
                    )}
                  </CardContent>
                </Card>
              </div>

              {/* Recent Funding Rounds - Main Table */}
              <Card className="bg-white rounded-2xl shadow-lg border-0">
                <CardHeader className="pb-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <CardTitle className="text-2xl font-bold text-[#2D2D2D]">Recent Funding Rounds</CardTitle>
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
                  <Button variant="ghost" size="sm" className="text-gray-600 hover:text-gray-900">
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
                <div className="overflow-hidden">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-gray-200">
                        <th className="text-left px-6 py-4 text-sm font-medium text-gray-600">
                          Company
                        </th>
                        <th className="text-left px-6 py-4 text-sm font-medium text-gray-600">
                          Amount
                        </th>
                        <th className="text-left px-6 py-4 text-sm font-medium text-gray-600">
                          Stage
                        </th>
                        <th className="text-left px-6 py-4 text-sm font-medium text-gray-600">
                          Sector
                        </th>
                        <th className="text-left px-6 py-4 text-sm font-medium text-gray-600">
                          Date
                        </th>
                        <th className="text-left px-6 py-4 text-sm font-medium text-gray-600">
                          Score
                        </th>
                        <th className="w-10"></th>
                      </tr>
                    </thead>
                    <tbody>
                      {deals.map((deal) => (
                        <tr key={deal.id} className="border-b border-gray-200 hover:bg-gray-50 transition-colors">
                          <td className="px-6 py-4">
                            <div className="flex items-center space-x-3">
                              <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                                deal.hasAiFocus ? 'bg-blue-100' : 'bg-green-100'
                              }`}>
                                <span className={`text-sm font-semibold ${
                                  deal.hasAiFocus ? 'text-blue-600' : 'text-green-600'
                                }`}>
                                  {deal.companyName.substring(0, 2).toUpperCase()}
                                </span>
                              </div>
                              <div>
                                <div className="font-semibold text-gray-900">{deal.companyName}</div>
                                <div className="text-sm text-gray-600 truncate max-w-xs">
                                  {deal.companyDescription}
                                </div>
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4 font-semibold text-gray-900">{deal.amount}</td>
                          <td className="px-6 py-4">
                            <Badge variant={getStageVariant(deal.stage)}>{deal.stage}</Badge>
                          </td>
                          <td className="px-6 py-4">
                            <Badge variant={getSectorVariant(deal.sector)}>
                              {deal.sector[0] || 'Climate Tech'}
                            </Badge>
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-600">{deal.date}</td>
                          <td className="px-6 py-4">
                            <div className="flex items-center space-x-2">
                              <div className={`w-3 h-3 rounded-full ${
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
                              className="h-8 w-8 text-gray-400 hover:text-gray-600"
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
                    <div className="text-center p-8 text-gray-600">
                      No deals found. Check your database connection.
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

        {/* Create Alert Modal - Temporarily disabled due to context issue */}
        {/* <CreateAlertModal 
          isOpen={showCreateAlert} 
          onClose={() => setShowCreateAlert(false)} 
        /> */}
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
