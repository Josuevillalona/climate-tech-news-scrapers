'use client';

import { useState, useEffect } from 'react';
import { fetchDeals, fetchDashboardStats, type UIFormattedDeal } from '@/lib/api';
import type { FilterState } from '@/contexts/FilterContext';

export function useDeals(filters?: FilterState) {
  const [deals, setDeals] = useState<UIFormattedDeal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadDeals = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchDeals(50, filters);
      setDeals(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load deals');
      console.error('Error loading deals:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDeals();
  }, [filters]); // Re-fetch when filters change

  return { deals, loading, error, refetch: loadDeals };
}

interface DashboardStats {
  totalDeals: number;
  totalFunding: number;
  avgDealSize: number;
  avgScore: number;
}

export function useDashboardStats() {
  const [stats, setStats] = useState<DashboardStats>({
    totalDeals: 0,
    totalFunding: 0,
    avgDealSize: 0,
    avgScore: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadStats() {
      try {
        setLoading(true);
        setError(null);
        const data = await fetchDashboardStats();
        setStats(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load stats');
        console.error('Error loading stats:', err);
      } finally {
        setLoading(false);
      }
    }

    loadStats();
  }, []);

  return { stats, loading, error };
}
