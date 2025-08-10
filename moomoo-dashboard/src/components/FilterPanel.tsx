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
    <Card className="bg-card border-border">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Filter className="h-4 w-4 text-primary-yellow" />
            <CardTitle className="text-sm font-semibold text-white">
              Alex's Investment Filters
            </CardTitle>
            {activeFilterCount > 0 && (
              <Badge variant="secondary" className="text-xs">
                {activeFilterCount} active
              </Badge>
            )}
          </div>
          <div className="flex items-center space-x-2">
            {activeFilterCount > 0 && (
              <Button
                variant="ghost"
                size="sm"
                onClick={resetFilters}
                className="text-xs text-muted-foreground hover:text-white"
              >
                <X className="h-3 w-3 mr-1" />
                Clear
              </Button>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsExpanded(!isExpanded)}
              className="text-muted-foreground hover:text-white"
            >
              <ChevronDown className={`h-4 w-4 transition-transform ${isExpanded ? 'rotate-180' : ''}`} />
            </Button>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Quick Filters Row */}
        <div className="flex items-center space-x-2 flex-wrap gap-2">
          <Button
            variant={filters.hasAiFocus === true ? "default" : "outline"}
            size="sm"
            onClick={() => updateFilter('hasAiFocus', filters.hasAiFocus === true ? null : true)}
            className="text-xs"
          >
            <Zap className="h-3 w-3 mr-1" />
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
            className="text-xs"
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
            className="text-xs"
          >
            Series A
          </Button>

          <Button
            variant={filters.minScore > 70 ? "default" : "outline"}
            size="sm"
            onClick={() => updateFilter('minScore', filters.minScore > 70 ? 0 : 70)}
            className="text-xs"
          >
            <TrendingUp className="h-3 w-3 mr-1" />
            High Score (70+)
          </Button>
        </div>

        {/* Expanded Filters */}
        {isExpanded && (
          <div className="space-y-4 pt-4 border-t border-border">
            {/* Funding Stages */}
            <div>
              <label className="text-sm font-medium text-white mb-2 block">
                Funding Stages
              </label>
              <div className="flex flex-wrap gap-2">
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
                    className="text-xs"
                  >
                    {stage}
                  </Button>
                ))}
              </div>
            </div>

            {/* Investment Score Range */}
            <div>
              <label className="text-sm font-medium text-white mb-2 block">
                Alex Score Range: {filters.minScore} - {filters.maxScore}
              </label>
              <div className="flex items-center space-x-4">
                <div className="flex-1">
                  <Input
                    type="range"
                    min="0"
                    max="100"
                    value={filters.minScore}
                    onChange={(e) => updateFilter('minScore', parseInt(e.target.value))}
                    className="w-full"
                  />
                  <div className="text-xs text-muted-foreground mt-1">Min: {filters.minScore}</div>
                </div>
                <div className="flex-1">
                  <Input
                    type="range"
                    min="0"
                    max="100"
                    value={filters.maxScore}
                    onChange={(e) => updateFilter('maxScore', parseInt(e.target.value))}
                    className="w-full"
                  />
                  <div className="text-xs text-muted-foreground mt-1">Max: {filters.maxScore}</div>
                </div>
              </div>
            </div>

            {/* Funding Amount Range */}
            <div>
              <label className="text-sm font-medium text-white mb-2 block">
                <DollarSign className="h-4 w-4 inline mr-1" />
                Funding Amount (USD)
              </label>
              <div className="grid grid-cols-2 gap-2">
                <Input
                  type="number"
                  placeholder="Min amount"
                  value={filters.minAmount || ''}
                  onChange={(e) => updateFilter('minAmount', e.target.value ? parseInt(e.target.value) : null)}
                  className="text-xs"
                />
                <Input
                  type="number"
                  placeholder="Max amount"
                  value={filters.maxAmount || ''}
                  onChange={(e) => updateFilter('maxAmount', e.target.value ? parseInt(e.target.value) : null)}
                  className="text-xs"
                />
              </div>
            </div>

            {/* Climate Sectors */}
            <div>
              <label className="text-sm font-medium text-white mb-2 block">
                Climate Sectors
              </label>
              <div className="flex flex-wrap gap-2">
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
                    className="text-xs"
                  >
                    {sector}
                  </Button>
                ))}
              </div>
            </div>

            {/* Countries */}
            <div>
              <label className="text-sm font-medium text-white mb-2 block">
                <Globe className="h-4 w-4 inline mr-1" />
                Countries
              </label>
              <div className="flex flex-wrap gap-2">
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
                    className="text-xs"
                  >
                    {country}
                  </Button>
                ))}
              </div>
            </div>

            {/* Date Range */}
            <div>
              <label className="text-sm font-medium text-white mb-2 block">
                <Calendar className="h-4 w-4 inline mr-1" />
                Date Range
              </label>
              <div className="grid grid-cols-2 gap-2">
                <Input
                  type="date"
                  value={filters.dateRange.start || ''}
                  onChange={(e) => updateFilter('dateRange', { ...filters.dateRange, start: e.target.value })}
                  className="text-xs"
                />
                <Input
                  type="date"
                  value={filters.dateRange.end || ''}
                  onChange={(e) => updateFilter('dateRange', { ...filters.dateRange, end: e.target.value })}
                  className="text-xs"
                />
              </div>
            </div>
          </div>
        )}

        {/* Set Alert Button */}
        {activeFilterCount > 0 && onCreateAlert && (
          <div className="pt-4 border-t border-border">
            <Button 
              onClick={onCreateAlert}
              style={{
                backgroundColor: '#F7D774',
                color: '#000000',
                borderColor: '#F7D774'
              }}
              className="w-full hover:opacity-90 font-semibold py-3 px-4 rounded-lg shadow-lg transition-all duration-200 hover:shadow-xl border-2"
            >
              <Bell className="h-4 w-4 mr-2 text-black" />
              Set Alert for Current Filters
            </Button>
            <p className="text-xs text-muted-foreground mt-2 text-center">
              Get notified when new deals match your criteria
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
