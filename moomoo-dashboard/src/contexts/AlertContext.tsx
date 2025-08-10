'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { fetchDeals } from '@/lib/api';
import type { FilterState } from '@/contexts/FilterContext';
import type { FormattedDeal } from '@/lib/supabase';

export interface AlertPreset {
  id: string;
  name: string;
  description: string;
  filters: FilterState;
  isActive: boolean;
  createdAt: string;
  lastChecked?: string;
  lastTriggered?: string;
  totalMatches: number;
  newMatches: number;
  lastMatchedDeals: FormattedDeal[];
}

interface AlertContextType {
  presets: AlertPreset[];
  isLoading: boolean;
  createPreset: (name: string, description: string, filters: FilterState) => AlertPreset;
  updatePreset: (id: string, updatedPreset: AlertPreset) => void;
  deletePreset: (id: string) => void;
  togglePreset: (id: string) => void;
  requestNotificationPermission: () => Promise<void>;
}

const STORAGE_KEY = 'alex_investment_alerts';

const AlertContext = createContext<AlertContextType | undefined>(undefined);

export function AlertProvider({ children }: { children: ReactNode }) {
  const [presets, setPresets] = useState<AlertPreset[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Load saved presets from localStorage
  useEffect(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        try {
          const parsedPresets = JSON.parse(saved);
          console.log('✅ Loaded presets from localStorage:', parsedPresets);
          setPresets(parsedPresets);
        } catch (parseError) {
          console.error('❌ Error parsing saved presets:', parseError);
          // Clear corrupted data
          localStorage.removeItem(STORAGE_KEY);
        }
      }
    } catch (storageError) {
      console.warn('⚠️ localStorage unavailable:', storageError);
      // Continue with empty presets array
    }
    setIsLoading(false);
  }, []);

  // Save presets to localStorage whenever they change
  useEffect(() => {
    if (!isLoading && presets.length >= 0) {
      try {
        console.log('💾 Saving presets to localStorage:', presets);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(presets));
      } catch (error) {
        console.warn('⚠️ Failed to save presets to localStorage:', error);
        // Continue silently - user will lose data on refresh but app won't break
      }
    }
  }, [presets, isLoading]);

  // Check for new matches every 5 minutes for active alerts
  useEffect(() => {
    const checkAlerts = async () => {
      const activePresets = presets.filter(p => p.isActive);
      
      for (const preset of activePresets) {
        try {
          const matchingDeals = await fetchDeals(100, preset.filters);
          
          // Check for new deals since last check
          const lastCheckedTime = preset.lastChecked ? new Date(preset.lastChecked) : new Date(0);
          const newDeals = matchingDeals.filter(deal => 
            new Date(deal.date) > lastCheckedTime
          );

          if (newDeals.length > 0) {
            updatePreset(preset.id, {
              ...preset,
              lastChecked: new Date().toISOString(),
              lastTriggered: new Date().toISOString(),
              totalMatches: matchingDeals.length,
              newMatches: newDeals.length,
              lastMatchedDeals: newDeals.slice(0, 5) // Keep last 5 matches
            });

            // Trigger notification
            if ('Notification' in window && Notification.permission === 'granted') {
              new Notification(`Investment Alert: ${preset.name}`, {
                body: `${newDeals.length} new deals matching your criteria`,
                icon: '/favicon.ico'
              });
            }
          } else {
            // Update last checked time even if no new matches
            updatePreset(preset.id, {
              ...preset,
              lastChecked: new Date().toISOString(),
              totalMatches: matchingDeals.length
            });
          }
        } catch (error) {
          console.error(`Error checking alert ${preset.name}:`, error);
        }
      }
    };

    if (presets.length > 0) {
      checkAlerts(); // Check immediately
      const interval = setInterval(checkAlerts, 5 * 60 * 1000); // Then every 5 minutes
      return () => clearInterval(interval);
    }
  }, [presets]);

  const createPreset = (name: string, description: string, filters: FilterState): AlertPreset => {
    // Generate mock matched deals for demonstration
    const mockDeals: FormattedDeal[] = [
      {
        id: '1',
        companyName: 'SolarTech AI',
        companyDescription: 'AI-powered solar panel optimization platform',
        amount: '$15M',
        stage: 'Series A',
        sector: ['Solar Energy', 'AI'],
        date: new Date().toISOString(),
        score: 85,
        scoreColor: 'green' as const,
        sourceUrl: 'https://example.com/deal1',
        hasAiFocus: true,
        country: 'United States',
        reviewStatus: 'APPROVED'
      },
      {
        id: '2', 
        companyName: 'CarbonCapture Plus',
        companyDescription: 'Direct air capture technology for carbon removal',
        amount: '$32M',
        stage: 'Series B',
        sector: ['Carbon Capture'],
        date: new Date().toISOString(),
        score: 92,
        scoreColor: 'green' as const,
        sourceUrl: 'https://example.com/deal2',
        hasAiFocus: false,
        country: 'Canada',
        reviewStatus: 'APPROVED'
      },
      {
        id: '3',
        companyName: 'GridFlow Energy',
        companyDescription: 'Smart grid optimization software',
        amount: '$8M',
        stage: 'Seed',
        sector: ['Energy Storage', 'Software'],
        date: new Date().toISOString(),
        score: 78,
        scoreColor: 'yellow' as const,
        sourceUrl: 'https://example.com/deal3',
        hasAiFocus: true,
        country: 'Germany',
        reviewStatus: 'APPROVED'
      },
      {
        id: '4',
        companyName: 'AgriSense IoT',
        companyDescription: 'IoT sensors for precision agriculture',
        amount: '$12M',
        stage: 'Series A',
        sector: ['AgTech', 'IoT'],
        date: new Date().toISOString(),
        score: 81,
        scoreColor: 'green' as const,
        sourceUrl: 'https://example.com/deal4',
        hasAiFocus: false,
        country: 'Netherlands',
        reviewStatus: 'APPROVED'
      },
      {
        id: '5',
        companyName: 'Ocean Clean',
        companyDescription: 'Ocean plastic removal technology',
        amount: '$25M',
        stage: 'Series B',
        sector: ['Water Tech', 'Robotics'],
        date: new Date().toISOString(),
        score: 88,
        scoreColor: 'green' as const,
        sourceUrl: 'https://example.com/deal5',
        hasAiFocus: true,
        country: 'Norway',
        reviewStatus: 'APPROVED'
      }
    ];

    const newPreset: AlertPreset = {
      id: `alert_${Date.now()}`,
      name,
      description,
      filters,
      isActive: true, // Start active by default
      createdAt: new Date().toISOString(),
      totalMatches: mockDeals.length,
      newMatches: 2, // Simulate 2 new matches
      lastMatchedDeals: mockDeals
    };

    console.log('Creating new preset:', newPreset);
    setPresets(prev => {
      const updated = [...prev, newPreset];
      console.log('Updated presets context:', updated);
      return updated;
    });
    return newPreset;
  };

  const updatePreset = (id: string, updatedPreset: AlertPreset) => {
    setPresets(prev => prev.map(preset => 
      preset.id === id ? updatedPreset : preset
    ));
  };

  const deletePreset = (id: string) => {
    setPresets(prev => prev.filter(preset => preset.id !== id));
  };

  const togglePreset = (id: string) => {
    setPresets(prev => prev.map(preset => 
      preset.id === id ? { ...preset, isActive: !preset.isActive } : preset
    ));
  };

  const requestNotificationPermission = async () => {
    if ('Notification' in window && Notification.permission === 'default') {
      await Notification.requestPermission();
    }
  };

  return (
    <AlertContext.Provider value={{
      presets,
      isLoading,
      createPreset,
      updatePreset,
      deletePreset,
      togglePreset,
      requestNotificationPermission
    }}>
      {children}
    </AlertContext.Provider>
  );
}

export function useAlertSystem() {
  const context = useContext(AlertContext);
  if (context === undefined) {
    throw new Error('useAlertSystem must be used within an AlertProvider');
  }
  return context;
}
