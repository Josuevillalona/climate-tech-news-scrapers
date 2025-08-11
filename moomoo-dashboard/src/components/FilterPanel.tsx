'use client';

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useFilters } from "@/contexts/FilterContext";
import { Filter, X, ChevronDown, Zap, TrendingUp, Globe, Calendar, DollarSign, Bell } from "lucide-react";
import { useState } from "react";

interface FilterPanelProps {
  onCreateAlert?: () => void;
}

const FUNDING_STAGES = [
  'Pre-Seed', 'Seed', 'Series A', 'Series B', 'Series C', 'Series D+', 'Growth', 'IPO'
];

const CLIMATE_SECTORS = [
  'Energy Storage', 'Solar', 'Wind', 'Hydrogen', 'Carbon Capture', 'EV/Transport',
  'AgTech', 'Food Tech', 'Waste Management', 'Water Tech', 'Green Finance', 'Climate Analytics'
];

const COUNTRIES = [
  'United States', 'United Kingdom', 'Germany', 'France', 'Canada', 'Australia',
  'Netherlands', 'Sweden', 'Israel', 'Singapore', 'India', 'China'
];

const REVIEW_STATUSES = [
  'PENDING_REVIEW', 'APPROVED', 'REJECTED', 'FLAGGED', 'ARCHIVED'
];

export default function FilterPanel({ onCreateAlert }: FilterPanelProps = {}) {
  const { filters, updateFilter, resetFilters, activeFilterCount } = useFilters();
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <Card className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 border border-gray-200">
      <CardHeader className="pb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="p-2 bg-blue-50 rounded-lg">
              <Filter className="h-5 w-5 text-blue-600" />
            </div>
            <div>
              <CardTitle className="text-lg font-semibold text-gray-900">
                Investment Filters
              </CardTitle>
              <p className="text-sm text-gray-600 mt-1">Customize your deal discovery</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            {activeFilterCount > 0 && (
              <Badge className="text-xs bg-blue-100 text-blue-800 rounded-full px-3 py-1 font-medium">
                {activeFilterCount} active
              </Badge>
            )}
            {activeFilterCount > 0 && (
              <Button
                variant="ghost"
                size="sm"
                onClick={resetFilters}
                className="text-sm text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg px-3 py-2"
              >
                <X className="h-4 w-4 mr-1" />
                Clear
              </Button>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsExpanded(!isExpanded)}
              className="text-gray-500 hover:text-gray-700 hover:bg-gray-50 rounded-lg p-2"
            >
              <ChevronDown className={`h-5 w-5 transition-transform duration-200 ${isExpanded ? 'rotate-180' : ''}`} />
            </Button>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Quick Filters Row */}
        <div className="flex items-center space-x-3 flex-wrap gap-3">
          <Button
            variant={filters.hasAiFocus === true ? "default" : "outline"}
            size="sm"
            onClick={() => updateFilter('hasAiFocus', filters.hasAiFocus === true ? null : true)}
            className={`text-sm h-10 px-4 rounded-lg font-medium transition-colors ${
              filters.hasAiFocus === true 
                ? 'bg-green-600 text-white hover:bg-green-700' 
                : 'text-gray-700 border-gray-200 hover:bg-gray-50'
            }`}
          >
            <Zap className="h-4 w-4 mr-2" />
            AI Focus
          </Button>
          
          <Button
            variant={filters.stages.includes('Seed') ? "default" : "outline"}
            size="sm"
            onClick={() => {
              const newStages = filters.stages.includes('Seed')
                ? filters.stages.filter(s => s !== 'Seed')
                : [...filters.stages, 'Seed'];
              updateFilter('stages', newStages);
            }}
            className={`text-sm h-10 px-4 rounded-lg font-medium transition-colors ${
              filters.stages.includes('Seed') 
                ? 'bg-green-600 text-white hover:bg-green-700' 
                : 'text-gray-700 border-gray-200 hover:bg-gray-50'
            }`}
          >
            Seed Stage
          </Button>

          <Button
            variant={filters.stages.includes('Series A') ? "default" : "outline"}
            size="sm"
            onClick={() => {
              const newStages = filters.stages.includes('Series A')
                ? filters.stages.filter(s => s !== 'Series A')
                : [...filters.stages, 'Series A'];
              updateFilter('stages', newStages);
            }}
            className={`text-sm h-10 px-4 rounded-lg font-medium transition-colors ${
              filters.stages.includes('Series A') 
                ? 'bg-green-600 text-white hover:bg-green-700' 
                : 'text-gray-700 border-gray-200 hover:bg-gray-50'
            }`}
          >
            Series A
          </Button>

          <Button
            variant={filters.minScore > 70 ? "default" : "outline"}
            size="sm"
            onClick={() => updateFilter('minScore', filters.minScore > 70 ? 0 : 70)}
            className={`text-sm h-10 px-4 rounded-lg font-medium transition-colors ${
              filters.minScore > 70 
                ? 'bg-green-600 text-white hover:bg-green-700' 
                : 'text-gray-700 border-gray-200 hover:bg-gray-50'
            }`}
          >
            <TrendingUp className="h-4 w-4 mr-2" />
            High Score (70+)
          </Button>
        </div>

        {/* Expanded Filters */}
        {isExpanded && (
          <div className="space-y-6 pt-6 border-t border-gray-100">
            {/* Funding Stages */}
            <div className="bg-gradient-to-r from-[#F3F3F3] to-[#AEE1F6]/20 p-5 rounded-2xl">
              <label className="text-sm font-semibold text-[#2D2D2D] mb-4 block flex items-center">
                <DollarSign className="h-4 w-4 mr-2 text-[#2E5E4E]" />
                Funding Stages
              </label>
              <div className="flex flex-wrap gap-3">
                {FUNDING_STAGES.map(stage => (
                  <Button
                    key={stage}
                    variant={filters.stages.includes(stage) ? "default" : "outline"}
                    size="sm"
                    onClick={() => {
                      const newStages = filters.stages.includes(stage)
                        ? filters.stages.filter(s => s !== stage)
                        : [...filters.stages, stage];
                      updateFilter('stages', newStages);
                    }}
                    className={`text-sm h-9 px-4 rounded-full font-medium transition-all duration-200 ${
                      filters.stages.includes(stage) 
                        ? 'bg-[#2E5E4E] text-white hover:bg-[#2E5E4E]/90 shadow-md' 
                        : 'text-[#2D2D2D] border-gray-300 hover:bg-white hover:border-[#2E5E4E] bg-white'
                    }`}
                  >
                    {stage}
                  </Button>
                ))}
              </div>
            </div>

            {/* Investment Score Range */}
            <div className="bg-gradient-to-r from-[#F7D774]/20 to-[#F7D774]/10 p-5 rounded-2xl">
              <label className="text-sm font-semibold text-[#2D2D2D] mb-4 block flex items-center">
                <TrendingUp className="h-4 w-4 mr-2 text-[#2E5E4E]" />
                Alex Score Range: {filters.minScore} - {filters.maxScore}
              </label>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white p-4 rounded-xl shadow-sm">
                  <label className="text-xs font-medium text-gray-600 mb-2 block">Minimum Score</label>
                  <Input
                    type="range"
                    min="0"
                    max="100"
                    value={filters.minScore}
                    onChange={(e) => updateFilter('minScore', parseInt(e.target.value))}
                    className="w-full h-2 bg-[#F3F3F3] rounded-lg appearance-none cursor-pointer accent-[#2E5E4E]"
                  />
                  <div className="text-sm font-semibold text-[#2D2D2D] mt-2">{filters.minScore}</div>
                </div>
                <div className="bg-white p-4 rounded-xl shadow-sm">
                  <label className="text-xs font-medium text-gray-600 mb-2 block">Maximum Score</label>
                  <Input
                    type="range"
                    min="0"
                    max="100"
                    value={filters.maxScore}
                    onChange={(e) => updateFilter('maxScore', parseInt(e.target.value))}
                    className="w-full h-2 bg-[#F3F3F3] rounded-lg appearance-none cursor-pointer accent-[#2E5E4E]"
                  />
                  <div className="text-sm font-semibold text-[#2D2D2D] mt-2">{filters.maxScore}</div>
                </div>
              </div>
            </div>

            {/* Funding Amount Range */}
            <div className="bg-gradient-to-r from-[#2E5E4E]/10 to-[#F7D774]/20 p-5 rounded-2xl">
              <label className="text-sm font-semibold text-[#2D2D2D] mb-4 block flex items-center">
                <DollarSign className="h-4 w-4 mr-2 text-[#2E5E4E]" />
                Funding Amount (USD)
              </label>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white p-4 rounded-xl shadow-sm">
                  <label className="text-xs font-medium text-gray-600 mb-2 block">Minimum Amount</label>
                  <Input
                    type="number"
                    placeholder="Min amount"
                    value={filters.minAmount || ''}
                    onChange={(e) => updateFilter('minAmount', e.target.value ? parseInt(e.target.value) : null)}
                    className="text-sm text-[#2D2D2D] placeholder:text-gray-500 border-gray-300 rounded-xl focus:border-[#2E5E4E] focus:ring-[#2E5E4E]"
                  />
                </div>
                <div className="bg-white p-4 rounded-xl shadow-sm">
                  <label className="text-xs font-medium text-gray-600 mb-2 block">Maximum Amount</label>
                  <Input
                    type="number"
                    placeholder="Max amount"
                    value={filters.maxAmount || ''}
                    onChange={(e) => updateFilter('maxAmount', e.target.value ? parseInt(e.target.value) : null)}
                    className="text-sm text-[#2D2D2D] placeholder:text-gray-500 border-gray-300 rounded-xl focus:border-[#2E5E4E] focus:ring-[#2E5E4E]"
                  />
                </div>
              </div>
            </div>

            {/* Climate Sectors */}
            <div className="bg-gradient-to-r from-[#AEE1F6]/20 to-[#F3F3F3] p-5 rounded-2xl">
              <label className="text-sm font-semibold text-[#2D2D2D] mb-4 block flex items-center">
                <Globe className="h-4 w-4 mr-2 text-[#2E5E4E]" />
                Climate Sectors
              </label>
              <div className="flex flex-wrap gap-3">
                {CLIMATE_SECTORS.map(sector => (
                  <Button
                    key={sector}
                    variant={filters.sectors.includes(sector) ? "secondary" : "outline"}
                    size="sm"
                    onClick={() => {
                      const newSectors = filters.sectors.includes(sector)
                        ? filters.sectors.filter(s => s !== sector)
                        : [...filters.sectors, sector];
                      updateFilter('sectors', newSectors);
                    }}
                    className={`text-sm h-9 px-4 rounded-full font-medium transition-all duration-200 ${
                      filters.sectors.includes(sector) 
                        ? 'bg-[#2E5E4E] text-white hover:bg-[#2E5E4E]/90 shadow-md' 
                        : 'text-[#2D2D2D] border-gray-300 hover:bg-white hover:border-[#2E5E4E] bg-white'
                    }`}
                  >
                    {sector}
                  </Button>
                ))}
              </div>
            </div>

            {/* Countries */}
            <div className="bg-gradient-to-r from-[#F3F3F3] to-[#2E5E4E]/10 p-5 rounded-2xl">
              <label className="text-sm font-semibold text-[#2D2D2D] mb-4 block flex items-center">
                <Globe className="h-4 w-4 mr-2 text-[#2E5E4E]" />
                Countries
              </label>
              <div className="flex flex-wrap gap-3">
                {COUNTRIES.slice(0, 8).map(country => (
                  <Button
                    key={country}
                    variant={filters.countries.includes(country) ? "default" : "outline"}
                    size="sm"
                    onClick={() => {
                      const newCountries = filters.countries.includes(country)
                        ? filters.countries.filter(c => c !== country)
                        : [...filters.countries, country];
                      updateFilter('countries', newCountries);
                    }}
                    className={`text-sm h-9 px-4 rounded-full font-medium transition-all duration-200 ${
                      filters.countries.includes(country) 
                        ? 'bg-[#2E5E4E] text-white hover:bg-[#2E5E4E]/90 shadow-md' 
                        : 'text-[#2D2D2D] border-gray-300 hover:bg-white hover:border-[#2E5E4E] bg-white'
                    }`}
                  >
                    {country}
                  </Button>
                ))}
              </div>
            </div>

            {/* Date Range */}
            <div className="bg-gradient-to-r from-[#F7D774]/10 to-[#AEE1F6]/20 p-5 rounded-2xl">
              <label className="text-sm font-semibold text-[#2D2D2D] mb-4 block flex items-center">
                <Calendar className="h-4 w-4 mr-2 text-[#2E5E4E]" />
                Date Range
              </label>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white p-4 rounded-xl shadow-sm">
                  <label className="text-xs font-medium text-gray-600 mb-2 block">From Date</label>
                  <Input
                    type="date"
                    value={filters.dateRange.start || ''}
                    onChange={(e) => updateFilter('dateRange', { ...filters.dateRange, start: e.target.value })}
                    className="text-sm text-[#2D2D2D] border-gray-300 rounded-xl focus:border-[#2E5E4E] focus:ring-[#2E5E4E]"
                  />
                </div>
                <div className="bg-white p-4 rounded-xl shadow-sm">
                  <label className="text-xs font-medium text-gray-600 mb-2 block">To Date</label>
                  <Input
                    type="date"
                    value={filters.dateRange.end || ''}
                    onChange={(e) => updateFilter('dateRange', { ...filters.dateRange, end: e.target.value })}
                    className="text-sm text-[#2D2D2D] border-gray-300 rounded-xl focus:border-[#2E5E4E] focus:ring-[#2E5E4E]"
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Set Alert Button */}
        {activeFilterCount > 0 && onCreateAlert && (
          <div className="pt-6 border-t border-gray-200">
            <Button 
              onClick={onCreateAlert}
              className="w-full bg-[#F7D774] hover:bg-[#F7D774]/90 text-[#2D2D2D] font-semibold py-4 px-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-200 text-base"
            >
              <Bell className="h-5 w-5 mr-3" />
              Set Alert for Current Filters
            </Button>
            <p className="text-sm text-gray-600 mt-3 text-center">
              Get notified when new deals match your criteria
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
