'use client';

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Bell, Plus, Trash2, Edit, Play, Pause, Eye, Zap, TrendingUp } from "lucide-react";
import { useAlertSystem } from "@/contexts/AlertContext";
import { useEffect, useState } from "react";

export default function AlertsPanel() {
  const { presets, isLoading, togglePreset, deletePreset, requestNotificationPermission } = useAlertSystem();
  const [hasRequestedPermission, setHasRequestedPermission] = useState(false);

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

  if (isLoading) {
    return (
      <Card className="bg-white border-gray-200">
        <CardHeader>
          <div className="flex items-center space-x-2">
            <Bell className="h-4 w-4 text-orange-400 animate-pulse" />
            <CardTitle className="text-sm font-semibold text-gray-900">
              Loading Alerts...
            </CardTitle>
          </div>
        </CardHeader>
      </Card>
    );
  }

  return (
    <Card className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 border-0">
      <CardHeader className="pb-6 bg-gradient-to-r from-[#F7D774]/20 to-[#F7D774]/10 rounded-t-2xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-orange-100 rounded-2xl shadow-sm">
              <Bell className="h-5 w-5 text-orange-600" />
            </div>
            <div>
              <CardTitle className="text-lg font-bold text-[#2D2D2D]">
                Investment Alerts
              </CardTitle>
              <p className="text-sm text-gray-600 mt-1">Real-time deal monitoring</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <Badge variant="secondary" className="text-xs bg-blue-100 text-blue-700 border-blue-200 rounded-full shadow-sm px-3 py-1 font-medium">
              {activePresets.length} active
            </Badge>
            {totalNewMatches > 0 && (
              <Badge variant="default" className="text-xs bg-green-600 text-white shadow-md rounded-full px-3 py-1 font-medium">
                {totalNewMatches} new
              </Badge>
            )}
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-6 p-6">
        {/* Alert Presets */}
        {presets.map(preset => (
          <div
            key={preset.id}
            className={`p-5 rounded-2xl transition-all duration-300 hover:shadow-md ${
              preset.isActive 
                ? 'bg-gradient-to-r from-[#F7D774]/20 to-[#F7D774]/10 border border-[#F7D774]/30 shadow-sm' 
                : 'bg-white border border-gray-200 hover:bg-gray-50'
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-3">
                  <h4 className="text-base font-semibold text-[#2D2D2D]">
                    {preset.name}
                  </h4>
                  {preset.isActive && (
                    <Badge variant="outline" className="text-xs text-orange-700 border-orange-400 bg-orange-100 rounded-full px-2 py-1 font-medium">
                      <Play className="h-3 w-3 mr-1" />
                      Active
                    </Badge>
                  )}
                  {preset.newMatches > 0 && (
                    <Badge variant="default" className="text-xs bg-green-600 text-white shadow-sm rounded-full px-2 py-1 font-medium">
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

                {/* Recent Matches Preview */}
                {preset.lastMatchedDeals && preset.lastMatchedDeals.length > 0 && (
                  <div className="mt-2 p-2 bg-gray-100 rounded border">
                    <div className="text-xs font-medium text-gray-900 mb-1">Recent Matches:</div>
                    {preset.lastMatchedDeals.slice(0, 2).map(deal => (
                      <div key={deal.id} className="text-xs text-gray-600">
                        • {deal.companyName} - {deal.amount} ({deal.stage})
                      </div>
                    ))}
                    {preset.lastMatchedDeals.length > 2 && (
                      <div className="text-xs text-gray-600">
                        +{preset.lastMatchedDeals.length - 2} more deals
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
                  className={`text-xs ${
                    preset.isActive 
                      ? 'text-orange-600 hover:text-orange-700' 
                      : 'text-gray-600 hover:text-gray-700'
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
                  className="text-xs text-gray-600 hover:text-gray-700"
                >
                  <Eye className="h-3 w-3" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => deletePreset(preset.id)}
                  className="text-xs text-gray-600 hover:text-red-500"
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
