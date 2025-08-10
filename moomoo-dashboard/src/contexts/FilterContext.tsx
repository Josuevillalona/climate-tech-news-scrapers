'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';

export interface FilterState {
  stages: string[];
  minAmount: number | null;
  maxAmount: number | null;
  hasAiFocus: boolean | null;
  sectors: string[];
  minScore: number;
  maxScore: number;
  countries: string[];
  dateRange: {
    start: string | null;
    end: string | null;
  };
  reviewStatus: string[];
}

interface FilterContextType {
  filters: FilterState;
  updateFilter: (key: keyof FilterState, value: any) => void;
  resetFilters: () => void;
  activeFilterCount: number;
}

const defaultFilters: FilterState = {
  stages: [],
  minAmount: null,
  maxAmount: null,
  hasAiFocus: null,
  sectors: [],
  minScore: 0,
  maxScore: 100,
  countries: [],
  dateRange: {
    start: null,
    end: null
  },
  reviewStatus: []
};

const FilterContext = createContext<FilterContextType | undefined>(undefined);

export function FilterProvider({ children }: { children: ReactNode }) {
  const [filters, setFilters] = useState<FilterState>(defaultFilters);

  const updateFilter = (key: keyof FilterState, value: any) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const resetFilters = () => {
    setFilters(defaultFilters);
  };

  const activeFilterCount = Object.entries(filters).reduce((count, [key, value]) => {
    if (key === 'minScore' && value === 0) return count;
    if (key === 'maxScore' && value === 100) return count;
    if (key === 'dateRange' && (!value.start && !value.end)) return count;
    if (Array.isArray(value) && value.length === 0) return count;
    if (value === null || value === undefined) return count;
    return count + 1;
  }, 0);

  return (
    <FilterContext.Provider value={{ filters, updateFilter, resetFilters, activeFilterCount }}>
      {children}
    </FilterContext.Provider>
  );
}

export function useFilters() {
  const context = useContext(FilterContext);
  if (context === undefined) {
    throw new Error('useFilters must be used within a FilterProvider');
  }
  return context;
}
