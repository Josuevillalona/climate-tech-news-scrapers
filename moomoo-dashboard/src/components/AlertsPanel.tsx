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
      <Card className="bg-card border-border">
        <CardHeader>
          <div className="flex items-center space-x-2">
            <Bell className="h-4 w-4 text-primary-yellow animate-pulse" />
            <CardTitle className="text-sm font-semibold text-white">
              Loading Alerts...
            </CardTitle>
          </div>
        </CardHeader>
      </Card>
    );
  }

  return (
    <Card className="bg-card border-border">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Bell className="h-4 w-4 text-primary-yellow" />
            <CardTitle className="text-sm font-semibold text-white">
              Investment Alerts
            </CardTitle>
            <Badge variant="secondary" className="text-xs">
              {activePresets.length} active
            </Badge>
            {totalNewMatches > 0 && (
              <Badge variant="default" className="text-xs bg-green-600">
                {totalNewMatches} new
              </Badge>
            )}
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-3">
        {/* Alert Presets */}
        {presets.map(preset => (
          <div
            key={preset.id}
            className={`p-3 border rounded-lg transition-colors ${
              preset.isActive 
                ? 'border-primary-yellow bg-primary-yellow/5' 
                : 'border-border bg-muted/5'
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-1">
                  <h4 className="text-sm font-medium text-white">
                    {preset.name}
                  </h4>
                  {preset.isActive && (
                    <Badge variant="outline" className="text-xs text-primary-yellow border-primary-yellow">
                      <Play className="h-3 w-3 mr-1" />
                      Active
                    </Badge>
                  )}
                  {preset.newMatches > 0 && (
                    <Badge variant="default" className="text-xs bg-green-600">
                      {preset.newMatches} new
                    </Badge>
                  )}
                </div>
                <p className="text-xs text-muted-foreground mb-2">
                  {preset.description}
                </p>
                
                {/* Alert Stats */}
                <div className="flex items-center space-x-4 text-xs text-muted-foreground">
                  <span className="flex items-center">
                    <TrendingUp className="h-3 w-3 mr-1" />
                    {preset.totalMatches} total
                  </span>
                  <span>Last: {formatTimeAgo(preset.lastChecked)}</span>
                  {preset.lastTriggered && (
                    <span className="text-green-400">
                      Triggered: {formatTimeAgo(preset.lastTriggered)}
                    </span>
                  )}
                </div>

                {/* Recent Matches Preview */}
                {preset.lastMatchedDeals && preset.lastMatchedDeals.length > 0 && (
                  <div className="mt-2 p-2 bg-muted/10 rounded border">
                    <div className="text-xs font-medium text-white mb-1">Recent Matches:</div>
                    {preset.lastMatchedDeals.slice(0, 2).map(deal => (
                      <div key={deal.id} className="text-xs text-muted-foreground">
                        • {deal.companyName} - {deal.amount} ({deal.stage})
                      </div>
                    ))}
                    {preset.lastMatchedDeals.length > 2 && (
                      <div className="text-xs text-muted-foreground">
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
                      ? 'text-primary-yellow hover:text-white' 
                      : 'text-muted-foreground hover:text-white'
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
                  className="text-xs text-muted-foreground hover:text-white"
                >
                  <Eye className="h-3 w-3" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => deletePreset(preset.id)}
                  className="text-xs text-muted-foreground hover:text-red-400"
                >
                  <Trash2 className="h-3 w-3" />
                </Button>
              </div>
            </div>
          </div>
        ))}

        {presets.length === 0 && (
          <div className="text-center py-6 text-muted-foreground">
            <Bell className="h-8 w-8 mx-auto mb-2 opacity-50" />
            <p className="text-sm">No investment alerts configured</p>
            <p className="text-xs mt-1">
              Set up filters and click "Set Alert" to get notified of matching deals
            </p>
          </div>
        )}

        {/* Notification Permission Notice */}
        {'Notification' in window && Notification.permission === 'default' && activePresets.length > 0 && (
          <div className="p-3 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
            <div className="flex items-center space-x-2">
              <Bell className="h-4 w-4 text-yellow-500" />
              <span className="text-xs text-yellow-500">
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
