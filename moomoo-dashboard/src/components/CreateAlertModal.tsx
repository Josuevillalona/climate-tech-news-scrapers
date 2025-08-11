'use client';

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { useFilters } from "@/contexts/FilterContext";
import { useAlertSystem } from "@/contexts/AlertContext";
import { Plus, Save, X, Zap } from "lucide-react";
import { useState } from "react";

export default function CreateAlertModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const { filters, activeFilterCount } = useFilters();
  const { createPreset } = useAlertSystem();
  const [alertName, setAlertName] = useState('');
  const [alertDescription, setAlertDescription] = useState('');

  if (!isOpen) return null;

  const handleCreate = () => {
    if (!alertName.trim()) return;

    const description = alertDescription || generateDescription();
    const newAlert = createPreset(alertName, description, filters);
    
    setAlertName('');
    setAlertDescription('');
    onClose();
  };

  const generateDescription = () => {
    const parts = [];
    
    if (filters.stages.length > 0) {
      parts.push(`${filters.stages.join(', ')} stage${filters.stages.length > 1 ? 's' : ''}`);
    }
    
    if (filters.hasAiFocus === true) {
      parts.push('AI-focused companies');
    }
    
    if (filters.minAmount || filters.maxAmount) {
      const min = filters.minAmount ? `$${(filters.minAmount / 1000000).toFixed(1)}M` : '';
      const max = filters.maxAmount ? `$${(filters.maxAmount / 1000000).toFixed(1)}M` : '';
      if (min && max) {
        parts.push(`funding between ${min}-${max}`);
      } else if (min) {
        parts.push(`funding above ${min}`);
      } else if (max) {
        parts.push(`funding below ${max}`);
      }
    }
    
    if (filters.minScore > 0) {
      parts.push(`Alex score ≥${filters.minScore}`);
    }
    
    if (filters.sectors.length > 0) {
      parts.push(`in ${filters.sectors.slice(0, 2).join(', ')}${filters.sectors.length > 2 ? `+${filters.sectors.length - 2} more` : ''}`);
    }

    return parts.length > 0 ? parts.join(', ') : 'All deals matching current filters';
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4 overflow-y-auto backdrop-blur-sm">
      <div className="w-full max-w-md mx-auto my-8">
        <Card className="bg-white border border-gray-200 shadow-2xl rounded-2xl">
          <CardHeader className="pb-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-orange-50 rounded-lg">
                  <Zap className="h-5 w-5 text-orange-600" />
                </div>
                <CardTitle className="text-lg font-semibold text-gray-900">
                  Create Investment Alert
                </CardTitle>
              </div>
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg p-2"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          </CardHeader>
        
        <CardContent className="space-y-6">
          {/* Current Filter Summary */}
          <div className="p-4 bg-orange-50 border border-orange-200 rounded-xl">
            <div className="flex items-center space-x-2 mb-2">
              <Zap className="h-4 w-4 text-orange-600" />
              <span className="text-sm font-medium text-orange-900">Current Filters</span>
              <Badge className="text-xs bg-orange-100 text-orange-800 border border-orange-200 rounded-full px-2 py-1">
                {activeFilterCount} active
              </Badge>
            </div>
            <p className="text-sm text-orange-700">
              {generateDescription()}
            </p>
          </div>

          {/* Alert Name */}
          <div>
            <label className="text-sm font-medium text-gray-900 mb-2 block">
              Alert Name *
            </label>
            <Input
              placeholder="e.g., High-Score AI Seed Deals"
              value={alertName}
              onChange={(e) => setAlertName(e.target.value)}
              className="w-full bg-white border border-gray-200 text-gray-900 placeholder-gray-500 rounded-lg focus:ring-1 focus:ring-moo-yellow focus:border-moo-yellow"
              autoFocus
            />
          </div>

          {/* Alert Description */}
          <div>
            <label className="text-sm font-medium text-gray-900 mb-2 block">
              Description (optional)
            </label>
            <Input
              placeholder={generateDescription()}
              value={alertDescription}
              onChange={(e) => setAlertDescription(e.target.value)}
              className="w-full bg-white border border-gray-200 text-gray-900 placeholder-gray-500 rounded-lg focus:ring-1 focus:ring-moo-yellow focus:border-moo-yellow"
            />
          </div>

          {/* Filter Preview */}
          <div className="space-y-3">
            <span className="text-sm font-medium text-gray-900">Alert Criteria:</span>
            <div className="flex flex-wrap gap-2">
              {filters.stages.map(stage => (
                <Badge key={stage} className="text-xs bg-blue-50 text-blue-800 border border-blue-200 rounded-full px-3 py-1">
                  {stage}
                </Badge>
              ))}
              {filters.hasAiFocus === true && (
                <Badge style={{ backgroundColor: '#F7D774', color: '#1F2937' }} className="text-xs rounded-full px-3 py-1 font-medium">
                  AI Focus
                </Badge>
              )}
              {filters.minScore > 0 && (
                <Badge style={{ backgroundColor: '#F7D774', color: '#1F2937' }} className="text-xs rounded-full px-3 py-1 font-medium">
                  Score ≥{filters.minScore}
                </Badge>
              )}
              {filters.sectors.slice(0, 3).map(sector => (
                <Badge key={sector} className="text-xs bg-green-50 text-green-800 border border-green-200 rounded-full px-3 py-1">
                  {sector}
                </Badge>
              ))}
              {filters.sectors.length > 3 && (
                <Badge className="text-xs bg-gray-50 text-gray-600 border border-gray-200 rounded-full px-3 py-1">
                  +{filters.sectors.length - 3} more
                </Badge>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="flex space-x-3 pt-4">
            <Button 
              variant="secondary" 
              onClick={onClose} 
              className="flex-1 bg-white border border-gray-200 text-gray-700 hover:bg-gray-50 rounded-lg px-4 py-2"
            >
              Cancel
            </Button>
            <Button 
              onClick={handleCreate}
              disabled={!alertName.trim()}
              style={{ backgroundColor: '#F7D774' }}
              className="flex-1 hover:opacity-90 text-gray-900 font-semibold rounded-lg px-4 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Save className="h-4 w-4 mr-2" />
              Create Alert
            </Button>
          </div>
        </CardContent>
        </Card>
      </div>
    </div>
  );
}
