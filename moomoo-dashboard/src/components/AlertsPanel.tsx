'use client';

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Bell, Plus, Trash2, Edit, Play, Pause, Eye, Zap, TrendingUp, ChevronLeft, ChevronRight, DollarSign, Building2 } from "lucide-react";
import { useAlertSystem } from "@/contexts/AlertContext";
import { useEffect, useState } from "react";

export default function AlertsPanel() {
  const { presets, isLoading, togglePreset, deletePreset, requestNotificationPermission } = useAlertSystem();
  const [hasRequestedPermission, setHasRequestedPermission] = useState(false);
  const [carouselStates, setCarouselStates] = useState<Record<string, number>>({});

  // Request notification permission on first load
  useEffect(() => {
    if (!hasRequestedPermission && presets.some(p => p.isActive)) {
      requestNotificationPermission();
      setHasRequestedPermission(true);
    }
  }, [presets, hasRequestedPermission, requestNotificationPermission]);

  const activePresets = presets.filter(p => p.isActive);
  const totalNewMatches = presets.reduce((sum, p) => sum + (p.newMatches || 0), 0);

  const formatTimeAgo = (dateString?: string) => {
    if (!dateString) return 'Never';
    
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    return `${diffDays}d ago`;
  };

  const formatAmount = (amount?: string | number) => {
    if (!amount) return 'Undisclosed';
    if (typeof amount === 'string') return amount;
    
    if (amount >= 1000000000) return `$${(amount / 1000000000).toFixed(1)}B`;
    if (amount >= 1000000) return `$${(amount / 1000000).toFixed(1)}M`;
    if (amount >= 1000) return `$${(amount / 1000).toFixed(0)}K`;
    return `$${amount.toLocaleString()}`;
  };

  const handleCarouselNext = (presetId: string, totalDeals: number) => {
    setCarouselStates(prev => {
      const currentIndex = prev[presetId] || 0;
      const maxIndex = Math.max(0, totalDeals - 1);
      return {
        ...prev,
        [presetId]: currentIndex >= maxIndex ? 0 : currentIndex + 1
      };
    });
  };

  const handleCarouselPrev = (presetId: string, totalDeals: number) => {
    setCarouselStates(prev => {
      const currentIndex = prev[presetId] || 0;
      const maxIndex = Math.max(0, totalDeals - 1);
      return {
        ...prev,
        [presetId]: currentIndex <= 0 ? maxIndex : currentIndex - 1
      };
    });
  };

  if (isLoading) {
    return (
      <Card className="bg-white rounded-2xl shadow-lg border-0">
        <CardHeader>
          <div className="flex items-center space-x-2">
            <Bell className="h-4 w-4 text-[#F7D774] animate-pulse" />
            <CardTitle className="text-sm font-semibold text-[#2D2D2D]">
              Loading Alerts...
            </CardTitle>
          </div>
        </CardHeader>
      </Card>
    );
  }

  return (
    <Card className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 border border-gray-200">
      <CardHeader className="pb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="p-2 bg-orange-50 rounded-lg">
              <Bell className="h-5 w-5 text-orange-600" />
            </div>
            <div>
              <CardTitle className="text-lg font-semibold text-gray-900">
                Investment Alerts
              </CardTitle>
              <p className="text-sm text-gray-600 mt-1">Real-time deal monitoring</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <Badge className="text-xs bg-green-100 text-green-800 rounded-full px-3 py-1 font-medium">
              {activePresets.length} active
            </Badge>
            {totalNewMatches > 0 && (
              <Badge className="text-xs bg-orange-100 text-orange-800 rounded-full px-3 py-1 font-medium">
                {totalNewMatches} new
              </Badge>
            )}
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Alert Presets */}
        {presets.map(preset => (
          <div
            key={preset.id}
            className={`p-4 rounded-lg transition-all duration-200 border ${
              preset.isActive 
                ? 'bg-green-50 border-green-200' 
                : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-3">
                  <h4 className="text-base font-semibold text-[#2D2D2D]">
                    {preset.name}
                  </h4>
                  {preset.isActive && (
                    <Badge variant="outline" className="text-xs text-[#2E5E4E] border-[#2E5E4E] bg-[#2E5E4E]/10 rounded-full px-2 py-1 font-medium">
                      <Play className="h-3 w-3 mr-1" />
                      Active
                    </Badge>
                  )}
                  {preset.newMatches > 0 && (
                    <Badge variant="default" className="text-xs bg-[#F7D774] text-[#2D2D2D] shadow-sm rounded-full px-2 py-1 font-medium animate-pulse">
                      {preset.newMatches} new
                    </Badge>
                  )}
                </div>
                <p className="text-sm text-gray-600 mb-4 leading-relaxed">
                  {preset.description}
                </p>
                
                {/* Alert Stats */}
                <div className="flex items-center space-x-4 text-xs text-gray-600">
                  <span className="flex items-center">
                    <TrendingUp className="h-3 w-3 mr-1" />
                    {preset.totalMatches} total
                  </span>
                  <span>Last: {formatTimeAgo(preset.lastChecked)}</span>
                  {preset.lastTriggered && (
                    <span className="text-green-600">
                      Triggered: {formatTimeAgo(preset.lastTriggered)}
                    </span>
                  )}
                </div>

                {/* Enhanced Company Carousel - One Company Per Card */}
                {preset.lastMatchedDeals && preset.lastMatchedDeals.length > 0 && (
                  <div className="mt-3 p-4 bg-gradient-to-r from-[#F7D774]/5 to-[#2E5E4E]/5 rounded-2xl border border-[#F7D774]/20">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-2">
                        <Building2 className="h-4 w-4 text-[#F7D774]" />
                        <span className="text-sm font-semibold text-[#2D2D2D]">Recent Matches</span>
                        <Badge className="text-xs bg-[#2E5E4E] text-white rounded-full px-2 py-1">
                          {preset.lastMatchedDeals.length}
                        </Badge>
                      </div>
                      {preset.lastMatchedDeals.length > 1 && (
                        <div className="flex items-center space-x-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleCarouselPrev(preset.id, preset.lastMatchedDeals.length)}
                            className="h-7 w-7 p-0 rounded-full hover:bg-[#F7D774]/20"
                          >
                            <ChevronLeft className="h-4 w-4 text-[#2D2D2D]" />
                          </Button>
                          <span className="text-xs text-gray-600 min-w-[3rem] text-center">
                            {(carouselStates[preset.id] || 0) + 1} of {preset.lastMatchedDeals.length}
                          </span>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleCarouselNext(preset.id, preset.lastMatchedDeals.length)}
                            className="h-7 w-7 p-0 rounded-full hover:bg-[#F7D774]/20"
                          >
                            <ChevronRight className="h-4 w-4 text-[#2D2D2D]" />
                          </Button>
                        </div>
                      )}
                    </div>
                    
                    {/* Single Company Card Display */}
                    <div className="relative">
                      {preset.lastMatchedDeals.length > 0 && (
                        <div className="bg-white rounded-2xl border border-gray-200/60 p-4 shadow-sm hover:shadow-md transition-all duration-300">
                          {(() => {
                            const currentIndex = carouselStates[preset.id] || 0;
                            const deal = preset.lastMatchedDeals[currentIndex];
                            return (
                              <div className="space-y-3">
                                {/* Company Header */}
                                <div className="flex items-start justify-between">
                                  <div className="flex-1 min-w-0">
                                    <h4 className="text-lg font-bold text-[#2D2D2D] mb-1 truncate">
                                      {deal.companyName}
                                    </h4>
                                    <p className="text-sm text-gray-600 line-clamp-2">
                                      {deal.companyDescription}
                                    </p>
                                  </div>
                                  <div className={`w-3 h-3 rounded-full ml-3 mt-1 ${
                                    deal.scoreColor === 'green' ? 'bg-green-500' :
                                    deal.scoreColor === 'yellow' ? 'bg-yellow-500' : 'bg-red-500'
                                  }`} title={`Alex Score: ${deal.score}`} />
                                </div>

                                {/* Deal Details */}
                                <div className="flex items-center justify-between">
                                  <div className="flex items-center space-x-3">
                                    <div className="flex items-center space-x-1">
                                      <DollarSign className="h-4 w-4 text-[#F7D774]" />
                                      <span className="text-base font-semibold text-[#2D2D2D]">
                                        {formatAmount(deal.amount)}
                                      </span>
                                    </div>
                                    {deal.stage && (
                                      <Badge variant="outline" className="text-xs bg-[#2E5E4E]/10 text-[#2E5E4E] border-[#2E5E4E]/30 rounded-full px-3 py-1">
                                        {deal.stage}
                                      </Badge>
                                    )}
                                  </div>
                                  <Button
                                    variant="ghost"
                                    size="sm"
                                    className="h-9 w-9 p-0 rounded-full hover:bg-[#F7D774]/20 text-[#2D2D2D]"
                                    onClick={() => window.open(deal.sourceUrl, '_blank')}
                                  >
                                    <Eye className="h-4 w-4" />
                                  </Button>
                                </div>

                                {/* Badges Row */}
                                <div className="flex flex-wrap gap-2">
                                  {deal.hasAiFocus && (
                                    <Badge variant="secondary" className="text-xs bg-[#F7D774] text-[#2D2D2D] rounded-full px-3 py-1">
                                      🤖 AI Focus
                                    </Badge>
                                  )}
                                  {deal.sector && deal.sector.slice(0, 2).map(sector => (
                                    <Badge key={sector} variant="outline" className="text-xs bg-gray-100 text-gray-700 border-gray-300 rounded-full px-3 py-1">
                                      {sector}
                                    </Badge>
                                  ))}
                                  {deal.sector && deal.sector.length > 2 && (
                                    <Badge variant="outline" className="text-xs bg-gray-100 text-gray-500 border-gray-300 rounded-full px-3 py-1">
                                      +{deal.sector.length - 2} more
                                    </Badge>
                                  )}
                                  {deal.country && (
                                    <Badge variant="outline" className="text-xs bg-blue-50 text-blue-700 border-blue-200 rounded-full px-3 py-1">
                                      🌍 {deal.country}
                                    </Badge>
                                  )}
                                </div>
                              </div>
                            );
                          })()}
                        </div>
                      )}
                    </div>
                    
                    {/* Pagination Dots */}
                    {preset.lastMatchedDeals.length > 1 && (
                      <div className="flex justify-center space-x-2 mt-4">
                        {preset.lastMatchedDeals.map((_, index) => (
                          <button
                            key={index}
                            onClick={() => setCarouselStates(prev => ({ ...prev, [preset.id]: index }))}
                            className={`h-2 w-2 rounded-full transition-all duration-200 ${
                              index === (carouselStates[preset.id] || 0)
                                ? 'bg-[#F7D774] scale-125'
                                : 'bg-gray-300 hover:bg-gray-400'
                            }`}
                          />
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
              
              <div className="flex items-center space-x-1">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => togglePreset(preset.id)}
                  className={`text-xs rounded-full p-2 ${
                    preset.isActive 
                      ? 'text-[#2E5E4E] hover:bg-[#2E5E4E]/10' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  {preset.isActive ? (
                    <Pause className="h-3 w-3" />
                  ) : (
                    <Play className="h-3 w-3" />
                  )}
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="text-xs text-gray-600 hover:text-gray-700 rounded-full p-2 hover:bg-gray-100"
                >
                  <Eye className="h-3 w-3" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => deletePreset(preset.id)}
                  className="text-xs text-gray-600 hover:text-red-500 rounded-full p-2 hover:bg-red-50"
                >
                  <Trash2 className="h-3 w-3" />
                </Button>
              </div>
            </div>
          </div>
        ))}

        {presets.length === 0 && (
          <div className="text-center py-6 text-gray-600">
            <Bell className="h-8 w-8 mx-auto mb-2 opacity-50" />
            <p className="text-sm">No investment alerts configured</p>
            <p className="text-xs mt-1">
              Set up filters and click "Set Alert" to get notified of matching deals
            </p>
          </div>
        )}

        {/* Notification Permission Notice */}
        {'Notification' in window && Notification.permission === 'default' && activePresets.length > 0 && (
          <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
            <div className="flex items-center space-x-2">
              <Bell className="h-4 w-4 text-yellow-600" />
              <span className="text-xs text-yellow-600">
                Enable notifications to receive real-time alerts
              </span>
            </div>
            <Button 
              variant="outline" 
              size="sm" 
              className="mt-2 text-xs"
              onClick={requestNotificationPermission}
            >
              Enable Notifications
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
