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
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 overflow-y-auto">
      <div className="w-full max-w-md mx-auto my-8">
        <Card className="bg-[#2D2D2D] border-[#2E5E4E] shadow-2xl rounded-2xl">
          <CardHeader className="pb-4">
            <div className="flex items-center justify-between">
              <CardTitle className="text-lg font-semibold text-white">
                Create Investment Alert
              </CardTitle>
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={onClose}
                className="text-gray-400 hover:text-white hover:bg-gray-700/50 rounded-full"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          </CardHeader>
        
        <CardContent className="space-y-4">
          {/* Current Filter Summary */}
          <div className="p-3 bg-[#2E5E4E]/20 border border-[#2E5E4E]/30 rounded-2xl">
            <div className="flex items-center space-x-2 mb-2">
              <Zap className="h-4 w-4 text-[#F7D774]" />
              <span className="text-sm font-medium text-white">Current Filters</span>
              <Badge variant="secondary" className="text-xs bg-[#F7D774] text-[#2D2D2D] rounded-full px-2 py-1">
                {activeFilterCount} active
              </Badge>
            </div>
            <p className="text-xs text-gray-300">
              {generateDescription()}
            </p>
          </div>

          {/* Alert Name */}
          <div>
            <label className="text-sm font-medium text-white mb-2 block">
              Alert Name *
            </label>
            <Input
              placeholder="e.g., High-Score AI Seed Deals"
              value={alertName}
              onChange={(e) => setAlertName(e.target.value)}
              className="w-full bg-gray-700/50 border-gray-600 text-white placeholder-gray-400 rounded-xl focus:border-[#F7D774] focus:ring-[#F7D774]"
              autoFocus
            />
          </div>

          {/* Alert Description */}
          <div>
            <label className="text-sm font-medium text-white mb-2 block">
              Description (optional)
            </label>
            <Input
              placeholder={generateDescription()}
              value={alertDescription}
              onChange={(e) => setAlertDescription(e.target.value)}
              className="w-full bg-gray-700/50 border-gray-600 text-white placeholder-gray-400 rounded-xl focus:border-[#F7D774] focus:ring-[#F7D774]"
            />
          </div>

          {/* Filter Preview */}
          <div className="space-y-2">
            <span className="text-sm font-medium text-white">Alert Criteria:</span>
            <div className="flex flex-wrap gap-2">
              {filters.stages.map(stage => (
                <Badge key={stage} variant="outline" className="text-xs bg-[#2E5E4E]/30 text-white border-[#2E5E4E] rounded-full">
                  {stage}
                </Badge>
              ))}
              {filters.hasAiFocus === true && (
                <Badge variant="secondary" className="text-xs bg-[#F7D774] text-[#2D2D2D] rounded-full">
                  AI Focus
                </Badge>
              )}
              {filters.minScore > 0 && (
                <Badge variant="secondary" className="text-xs bg-[#F7D774] text-[#2D2D2D] rounded-full">
                  Score ≥{filters.minScore}
                </Badge>
              )}
              {filters.sectors.slice(0, 3).map(sector => (
                <Badge key={sector} variant="outline" className="text-xs bg-[#2E5E4E]/30 text-white border-[#2E5E4E] rounded-full">
                  {sector}
                </Badge>
              ))}
              {filters.sectors.length > 3 && (
                <Badge variant="outline" className="text-xs bg-[#2E5E4E]/30 text-white border-[#2E5E4E] rounded-full">
                  +{filters.sectors.length - 3} more
                </Badge>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="flex space-x-3 pt-4">
            <Button 
              variant="outline" 
              onClick={onClose} 
              className="flex-1 bg-transparent border-gray-600 text-gray-300 hover:bg-gray-700/50 hover:text-white rounded-xl"
            >
              Cancel
            </Button>
            <Button 
              onClick={handleCreate}
              disabled={!alertName.trim()}
              className="flex-1 bg-[#F7D774] hover:bg-[#F7D774]/90 text-[#2D2D2D] font-semibold rounded-xl disabled:opacity-50 disabled:cursor-not-allowed"
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
