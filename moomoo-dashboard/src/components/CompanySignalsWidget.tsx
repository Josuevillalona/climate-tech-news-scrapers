'use client';

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { TrendingUp, Users, MapPin, FileText, Zap, Brain, Building2, Star, ArrowRight } from "lucide-react";

interface CompanySignal {
  id: string;
  companyName: string;
  signalType: 'hiring' | 'patent' | 'product' | 'funding' | 'expansion' | 'partnership';
  title: string;
  description: string;
  strength: number; // 1-100
  detectedAt: string;
  source: string;
  actionable: boolean;
  metadata: {
    hiringCount?: number;
    patentCount?: number;
    fundingStage?: string;
    partnerCompany?: string;
    newLocations?: string[];
  };
}

const mockSignalsData: CompanySignal[] = [
  {
    id: '1',
    companyName: 'CarbonIQ',
    signalType: 'hiring',
    title: 'Aggressive Engineering Hiring Surge',
    description: 'Posted 15 new engineering positions in past 2 weeks, including ML Engineers and Platform Architects',
    strength: 92,
    detectedAt: '2025-08-10T08:00:00Z',
    source: 'LinkedIn Jobs API',
    actionable: true,
    metadata: {
      hiringCount: 15
    }
  },
  {
    id: '2',
    companyName: 'PowerGrid Solutions',
    signalType: 'patent',
    title: 'AI Patent Filing Spree',
    description: '3 new AI-related patents filed for battery optimization algorithms',
    strength: 88,
    detectedAt: '2025-08-10T06:30:00Z',
    source: 'USPTO',
    actionable: true,
    metadata: {
      patentCount: 3
    }
  },
  {
    id: '3',
    companyName: 'FarmTech AI',
    signalType: 'product',
    title: 'Major Product Launch Preparation',
    description: 'Updated website with new product pages, increased marketing spend, beta customer testimonials',
    strength: 85,
    detectedAt: '2025-08-10T05:15:00Z',
    source: 'Web Monitoring',
    actionable: true,
    metadata: {}
  },
  {
    id: '4',
    companyName: 'CleanEnergy Corp',
    signalType: 'expansion',
    title: 'Geographic Expansion Signal',
    description: 'Job postings for Regional Managers in 3 new markets: Texas, California, Florida',
    strength: 78,
    detectedAt: '2025-08-09T14:20:00Z',
    source: 'Job Boards',
    actionable: false,
    metadata: {
      newLocations: ['Texas', 'California', 'Florida']
    }
  },
  {
    id: '5',
    companyName: 'SolarTech Innovation',
    signalType: 'funding',
    title: 'Series B Preparation Indicators',
    description: 'CFO hiring, investment bank meetings, updated pitch deck on website',
    strength: 82,
    detectedAt: '2025-08-09T11:45:00Z',
    source: 'Multiple Sources',
    actionable: true,
    metadata: {
      fundingStage: 'Series B'
    }
  }
];

export default function CompanySignalsWidget() {
  const [signals] = useState<CompanySignal[]>(mockSignalsData);
  const [selectedType, setSelectedType] = useState<string>('all');

  const getSignalIcon = (type: string) => {
    switch (type) {
      case 'hiring':
        return <Users className="h-4 w-4" />;
      case 'patent':
        return <Brain className="h-4 w-4" />;
      case 'product':
        return <Zap className="h-4 w-4" />;
      case 'funding':
        return <TrendingUp className="h-4 w-4" />;
      case 'expansion':
        return <MapPin className="h-4 w-4" />;
      case 'partnership':
        return <Building2 className="h-4 w-4" />;
      default:
        return <Star className="h-4 w-4" />;
    }
  };

  const getSignalColor = (type: string) => {
    switch (type) {
      case 'hiring':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'patent':
        return 'bg-purple-100 text-purple-800 border-purple-200';
      case 'product':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'funding':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'expansion':
        return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'partnership':
        return 'bg-pink-100 text-pink-800 border-pink-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStrengthColor = (strength: number) => {
    if (strength >= 90) return 'text-[#2E5E4E] bg-[#2E5E4E]/10';
    if (strength >= 80) return 'text-[#2E5E4E] bg-[#AEE1F6]/30';
    if (strength >= 70) return 'text-yellow-600 bg-yellow-50';
    return 'text-gray-600 bg-gray-50';
  };

  const filteredSignals = selectedType === 'all' 
    ? signals 
    : signals.filter(signal => signal.signalType === selectedType);

  const signalTypes = [
    { value: 'all', label: 'All Signals', count: signals.length },
    { value: 'hiring', label: 'Hiring', count: signals.filter(s => s.signalType === 'hiring').length },
    { value: 'patent', label: 'Patents', count: signals.filter(s => s.signalType === 'patent').length },
    { value: 'product', label: 'Products', count: signals.filter(s => s.signalType === 'product').length },
    { value: 'funding', label: 'Funding', count: signals.filter(s => s.signalType === 'funding').length },
  ];

  return (
    <Card className="h-full bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 border-0">
      <CardHeader className="pb-6 bg-gradient-to-r from-[#F3F3F3] to-[#AEE1F6]/30 rounded-t-2xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-orange-100 rounded-2xl shadow-sm">
              <Star className="h-5 w-5 text-orange-600" />
            </div>
            <div>
              <CardTitle className="text-lg font-bold text-[#2D2D2D]">
                Company Signals Intelligence
              </CardTitle>
              <p className="text-sm text-gray-600 mt-1">Market activity & growth signals</p>
            </div>
          </div>
          <Badge variant="secondary" className="text-xs bg-green-100 text-green-700 border-green-200 rounded-full shadow-sm px-3 py-1 font-medium">
            {signals.filter(s => s.actionable).length} Actionable
          </Badge>
        </div>
        
        {/* Signal Type Filters */}
        <div className="flex flex-wrap gap-2 mt-6">
          {signalTypes.map((type) => (
            <Button
              key={type.value}
              variant={selectedType === type.value ? "default" : "outline"}
              size="sm"
              onClick={() => setSelectedType(type.value)}
              className={`text-xs h-9 px-4 rounded-full transition-all duration-200 font-medium ${
                selectedType === type.value 
                  ? 'bg-[#2E5E4E] text-white hover:bg-[#2E5E4E]/90 shadow-md' 
                  : 'text-gray-600 border-gray-300 hover:bg-gray-50 hover:border-gray-400'
              }`}
            >
              {type.label} <span className="ml-1 text-xs opacity-75">({type.count})</span>
            </Button>
          ))}
        </div>
      </CardHeader>

      <CardContent className="space-y-4 max-h-[600px] overflow-y-auto">
        {filteredSignals.map((signal) => (
          <Card key={signal.id} className={`p-4 transition-all hover:shadow-md ${signal.actionable ? 'border-l-4 border-l-[#F7D774] bg-[#F7D774]/10' : 'bg-[#F3F3F3]'}`}>
            <div className="space-y-3">
              {/* Header */}
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <h4 className="font-medium text-sm">{signal.companyName}</h4>
                    {signal.actionable && (
                      <Badge variant="secondary" className="text-xs">
                        Actionable
                      </Badge>
                    )}
                  </div>
                  <h3 className="font-medium text-xs text-gray-900 mb-1">{signal.title}</h3>
                  <div className="text-xs text-gray-600">{signal.description}</div>
                </div>
                
                <div className="flex flex-col items-end gap-2">
                  <div className={`px-2 py-1 rounded-full text-xs font-medium ${getStrengthColor(signal.strength)}`}>
                    {signal.strength}% Strong
                  </div>
                </div>
              </div>

              {/* Signal Type and Metadata */}
              <div className="flex items-center gap-2 flex-wrap">
                <Badge className={`text-xs ${getSignalColor(signal.signalType)}`}>
                  {getSignalIcon(signal.signalType)}
                  <span className="ml-1 capitalize">{signal.signalType}</span>
                </Badge>
                
                {/* Type-specific metadata */}
                {signal.signalType === 'hiring' && signal.metadata.hiringCount && (
                  <Badge variant="outline" className="text-xs">
                    {signal.metadata.hiringCount} new roles
                  </Badge>
                )}
                
                {signal.signalType === 'patent' && signal.metadata.patentCount && (
                  <Badge variant="outline" className="text-xs">
                    {signal.metadata.patentCount} patents
                  </Badge>
                )}
                
                {signal.signalType === 'funding' && signal.metadata.fundingStage && (
                  <Badge variant="outline" className="text-xs">
                    {signal.metadata.fundingStage}
                  </Badge>
                )}
                
                {signal.signalType === 'expansion' && signal.metadata.newLocations && (
                  <Badge variant="outline" className="text-xs">
                    {signal.metadata.newLocations.length} new markets
                  </Badge>
                )}
              </div>

              {/* Source and Timing */}
              <div className="flex items-center justify-between text-xs text-gray-500">
                <span>Source: {signal.source}</span>
                <span>{new Date(signal.detectedAt).toLocaleDateString()}</span>
              </div>

              {/* Action Button for Actionable Signals */}
              {signal.actionable && (
                <div className="pt-2 border-t border-gray-100">
                  <Button variant="outline" size="sm" className="w-full text-xs">
                    <FileText className="h-3 w-3 mr-1" />
                    Generate Investment Brief
                    <ArrowRight className="h-3 w-3 ml-1" />
                  </Button>
                </div>
              )}
            </div>
          </Card>
        ))}

        {filteredSignals.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            <Star className="h-8 w-8 mx-auto mb-2" />
            <p className="text-sm">No signals detected for this filter</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
