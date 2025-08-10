'use client';

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, TrendingUp, DollarSign, Users, Building2, Settings, Bell, Filter, MoreHorizontal, Loader2, AlertCircle } from "lucide-react";
import { useDeals, useDashboardStats } from "@/hooks/useData";
import { formatLargeNumber } from "@/lib/utils";
import { FilterProvider, useFilters } from "@/contexts/FilterContext";
import { AlertProvider } from "@/contexts/AlertContext";
import FilterPanel from "@/components/FilterPanel";
import AlertsPanel from "@/components/AlertsPanel";
import CreateAlertModal from "@/components/CreateAlertModal";

function DashboardContent() {
  const { filters, activeFilterCount } = useFilters();
  const { deals, loading: dealsLoading, error: dealsError } = useDeals(filters);
  const { stats, loading: statsLoading } = useDashboardStats();
  const [showCreateAlert, setShowCreateAlert] = useState(false);

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
    <div className="min-h-screen bg-background text-foreground">
      {/* Header */}
      <header className="border-b border-border px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-6">
            <h1 className="text-2xl font-bold font-heading text-white">
              Moo Climate
            </h1>
            <nav className="flex items-center space-x-1">
              <Button variant="ghost" size="sm" className="text-primary-yellow font-medium">
                Dashboard
              </Button>
              <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-white">
                Deals
              </Button>
              <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-white">
                Companies
              </Button>
              <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-white">
                Investors
              </Button>
              <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-white">
                Analytics
              </Button>
            </nav>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
              <Input
                placeholder="Search deals, companies..."
                className="pl-10 w-80 bg-card border-border text-white placeholder:text-muted-foreground"
              />
            </div>
            <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-white">
              <Bell className="h-5 w-5" />
            </Button>
            <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-white">
              <Settings className="h-5 w-5" />
            </Button>
            <div className="w-8 h-8 bg-primary-yellow rounded-full flex items-center justify-center">
              <span className="text-xs font-semibold text-black">AC</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto p-6 space-y-8">
        {/* Welcome Section */}
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold text-white mb-2">Welcome back, Alex</h2>
            <p className="text-muted-foreground">Here's what's happening in climate tech funding today</p>
          </div>
          <div className="flex items-center space-x-3">
            <Badge variant="success" className="px-3 py-1">
              {deals.filter(d => d.score >= 70).length} High Score
            </Badge>
            <Badge variant="warning" className="px-3 py-1">
              {deals.filter(d => d.reviewStatus?.toLowerCase().includes('pending') || d.reviewStatus === 'PENDING_REVIEW').length} Pending Review
            </Badge>
          </div>
        </div>

        {/* Filter and Alert Panels */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <FilterPanel onCreateAlert={() => setShowCreateAlert(true)} />
          <AlertsPanel />
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card className="bg-gradient-to-br from-card to-card/80">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Deals
              </CardTitle>
              <Building2 className="h-5 w-5 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {statsLoading ? (
                <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
              ) : (
                <>
                  <div className="text-3xl font-bold text-white mb-1">
                    {stats.totalDeals.toLocaleString()}
                  </div>
                  <p className="text-xs text-green-400 flex items-center">
                    <TrendingUp className="w-3 h-3 mr-1" />
                    Processing pipeline
                  </p>
                </>
              )}
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-card to-card/80">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Volume
              </CardTitle>
              <DollarSign className="h-5 w-5 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {statsLoading ? (
                <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
              ) : (
                <>
                  <div className="text-3xl font-bold text-white mb-1">
                    ${formatLargeNumber(stats.totalFunding)}
                  </div>
                  <p className="text-xs text-green-400 flex items-center">
                    <TrendingUp className="w-3 h-3 mr-1" />
                    Total tracked funding
                  </p>
                </>
              )}
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-card to-card/80">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Avg. Deal
              </CardTitle>
              <TrendingUp className="h-5 w-5 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {statsLoading ? (
                <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
              ) : (
                <>
                  <div className="text-3xl font-bold text-white mb-1">
                    ${formatLargeNumber(stats.avgDealSize)}
                  </div>
                  <p className="text-xs text-yellow-400 flex items-center">
                    <TrendingUp className="w-3 h-3 mr-1" />
                    Climate tech average
                  </p>
                </>
              )}
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-card to-card/80">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Avg Score
              </CardTitle>
              <Users className="h-5 w-5 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {statsLoading ? (
                <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
              ) : (
                <>
                  <div className="text-3xl font-bold text-white mb-1">
                    {stats.avgScore.toFixed(1)}/10
                  </div>
                  <p className="text-xs text-green-400 flex items-center">
                    <TrendingUp className="w-3 h-3 mr-1" />
                    Alex's filter match
                  </p>
                </>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Recent Funding Rounds - Main Table */}
        <Card className="bg-gradient-to-br from-card to-card/80">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <CardTitle className="text-2xl font-heading text-white">Recent Funding Rounds</CardTitle>
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-muted-foreground">
                    Showing {deals.length} deals
                  </span>
                  {filters.stages.length > 0 && (
                    <Badge variant="outline" className="text-xs">
                      {filters.stages.length} stage{filters.stages.length > 1 ? 's' : ''}
                    </Badge>
                  )}
                  {filters.hasAiFocus === true && (
                    <Badge variant="secondary" className="text-xs">
                      AI Focus
                    </Badge>
                  )}
                  {filters.minScore > 0 && (
                    <Badge variant="secondary" className="text-xs">
                      Score ≥{filters.minScore}
                    </Badge>
                  )}
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-white">
                  Export
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent className="p-0">
            {dealsError ? (
              <div className="flex items-center justify-center p-8 text-red-400">
                <AlertCircle className="w-5 h-5 mr-2" />
                {dealsError}
              </div>
            ) : dealsLoading ? (
              <div className="flex items-center justify-center p-8">
                <Loader2 className="h-6 w-6 animate-spin text-muted-foreground mr-2" />
                <span className="text-muted-foreground">Loading deals...</span>
              </div>
            ) : (
              <div className="overflow-hidden">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-border">
                      <th className="text-left px-6 py-4 text-sm font-medium text-muted-foreground">
                        Company
                      </th>
                      <th className="text-left px-6 py-4 text-sm font-medium text-muted-foreground">
                        Amount
                      </th>
                      <th className="text-left px-6 py-4 text-sm font-medium text-muted-foreground">
                        Stage
                      </th>
                      <th className="text-left px-6 py-4 text-sm font-medium text-muted-foreground">
                        Sector
                      </th>
                      <th className="text-left px-6 py-4 text-sm font-medium text-muted-foreground">
                        Date
                      </th>
                      <th className="text-left px-6 py-4 text-sm font-medium text-muted-foreground">
                        Score
                      </th>
                      <th className="w-10"></th>
                    </tr>
                  </thead>
                  <tbody>
                    {deals.map((deal) => (
                      <tr key={deal.id} className="border-b border-border hover:bg-muted/50 transition-colors">
                        <td className="px-6 py-4">
                          <div className="flex items-center space-x-3">
                            <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                              deal.hasAiFocus ? 'bg-blue-500/20' : 'bg-green-500/20'
                            }`}>
                              <span className={`text-sm font-semibold ${
                                deal.hasAiFocus ? 'text-blue-400' : 'text-green-400'
                              }`}>
                                {deal.companyName.substring(0, 2).toUpperCase()}
                              </span>
                            </div>
                            <div>
                              <div className="font-semibold text-white">{deal.companyName}</div>
                              <div className="text-sm text-muted-foreground truncate max-w-xs">
                                {deal.companyDescription}
                              </div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 font-semibold text-white">{deal.amount}</td>
                        <td className="px-6 py-4">
                          <Badge variant={getStageVariant(deal.stage)}>{deal.stage}</Badge>
                        </td>
                        <td className="px-6 py-4">
                          <Badge variant={getSectorVariant(deal.sector)}>
                            {deal.sector[0] || 'Climate Tech'}
                          </Badge>
                        </td>
                        <td className="px-6 py-4 text-sm text-muted-foreground">{deal.date}</td>
                        <td className="px-6 py-4">
                          <div className="flex items-center space-x-2">
                            <div className={`w-3 h-3 rounded-full ${
                              deal.scoreColor === 'green' ? 'bg-green-500' :
                              deal.scoreColor === 'yellow' ? 'bg-yellow-500' : 'bg-red-500'
                            }`}></div>
                            <span className="text-sm font-semibold text-white">{deal.score}</span>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <Button 
                            variant="ghost" 
                            size="icon" 
                            className="h-8 w-8 text-muted-foreground hover:text-white"
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
                  <div className="text-center p-8 text-muted-foreground">
                    No deals found. Check your database connection.
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      </main>

      {/* Create Alert Modal */}
      <CreateAlertModal 
        isOpen={showCreateAlert} 
        onClose={() => setShowCreateAlert(false)} 
      />
    </div>
  );
}

export default function Dashboard() {
  return (
    <AlertProvider>
      <FilterProvider>
        <DashboardContent />
      </FilterProvider>
    </AlertProvider>
  );
}
