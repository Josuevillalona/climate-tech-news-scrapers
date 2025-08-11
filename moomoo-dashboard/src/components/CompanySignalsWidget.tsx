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
        return 'bg-blue-50 text-blue-700';
      case 'patent':
        return 'bg-purple-50 text-purple-700';
      case 'product':
        return 'bg-emerald-50 text-emerald-700';
      case 'funding':
        return 'bg-orange-50 text-orange-700';
      case 'expansion':
        return 'bg-rose-50 text-rose-700';
      case 'partnership':
        return 'bg-indigo-50 text-indigo-700';
      default:
        return 'bg-gray-50 text-gray-700';
    }
  };

  const getStrengthColor = (strength: number) => {
    if (strength >= 90) return 'text-[#2E5E4E] bg-[#2E5E4E]/10 border border-[#2E5E4E]/20';
    if (strength >= 80) return 'text-[#F7D774] bg-[#F7D774]/10 border border-[#F7D774]/30';
    if (strength >= 70) return 'text-orange-600 bg-orange-50 border border-orange-200';
    return 'text-gray-600 bg-gray-50 border border-gray-200';
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
    <Card className="h-full bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 border border-gray-200">
      <CardHeader className="pb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-purple-50 rounded-lg">
              <Star className="h-5 w-5 text-purple-600" />
            </div>
            <div>
              <CardTitle className="text-lg font-semibold text-gray-900">
                Company Signals Intelligence
              </CardTitle>
              <p className="text-sm text-gray-600 mt-1">Market activity & growth signals</p>
            </div>
          </div>
          <Badge className="text-xs bg-purple-50 text-purple-700 border border-purple-200 rounded-full px-3 py-1 font-medium">
            {signals.filter(s => s.actionable).length} Actionable
          </Badge>
        </div>
        
        {/* Signal Type Filters */}
        <div className="flex flex-wrap gap-2 mt-6">
          {signalTypes.map((type) => (
            <Button
              key={type.value}
              variant={selectedType === type.value ? "default" : "secondary"}
              size="sm"
              onClick={() => setSelectedType(type.value)}
              className={`text-xs h-9 px-4 rounded-lg font-medium transition-all duration-200 ${
                selectedType === type.value 
                  ? 'text-gray-900 shadow-sm' 
                  : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
              }`}
              style={selectedType === type.value ? { backgroundColor: '#F7D774' } : {}}
            >
              {type.label} <span className="ml-1 text-xs opacity-75">({type.count})</span>
            </Button>
          ))}
        </div>
      </CardHeader>

      <CardContent className="space-y-3 max-h-[600px] overflow-y-auto">
        {filteredSignals.map((signal) => (
          <Card key={signal.id} className={`rounded-xl border transition-all duration-200 hover:shadow-md ${signal.actionable ? 'border-l-4 border-l-[#F7D774] bg-[#F7D774]/5' : 'border-gray-200 bg-white'}`}>
            <div className="p-4 space-y-3">
              {/* Header */}
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <h4 className="font-semibold text-sm text-gray-900">{signal.companyName}</h4>
                    {signal.actionable && (
                      <Badge className="text-xs bg-[#F7D774] text-gray-900 hover:bg-[#F7D774]/90">
                        Actionable
                      </Badge>
                    )}
                  </div>
                  <h3 className="font-medium text-sm text-gray-800 mb-1">{signal.title}</h3>
                  <p className="text-sm text-gray-600 leading-relaxed">{signal.description}</p>
                </div>
                
                <div className="flex flex-col items-end gap-2">
                  <div className={`px-3 py-1 rounded-full text-xs font-medium ${getStrengthColor(signal.strength)}`}>
                    {signal.strength}% Strong
                  </div>
                </div>
              </div>

              {/* Signal Type and Metadata */}
              <div className="flex items-center gap-2 flex-wrap">
                <Badge className={`text-xs border-0 ${getSignalColor(signal.signalType)}`}>
                  {getSignalIcon(signal.signalType)}
                  <span className="ml-1.5 capitalize">{signal.signalType}</span>
                </Badge>
                
                {/* Type-specific metadata */}
                {signal.signalType === 'hiring' && signal.metadata.hiringCount && (
                  <Badge variant="outline" className="text-xs border-gray-300 text-gray-700">
                    {signal.metadata.hiringCount} new roles
                  </Badge>
                )}
                
                {signal.signalType === 'patent' && signal.metadata.patentCount && (
                  <Badge variant="outline" className="text-xs border-gray-300 text-gray-700">
                    {signal.metadata.patentCount} patents
                  </Badge>
                )}
                
                {signal.signalType === 'funding' && signal.metadata.fundingStage && (
                  <Badge variant="outline" className="text-xs border-gray-300 text-gray-700">
                    {signal.metadata.fundingStage}
                  </Badge>
                )}
                
                {signal.signalType === 'expansion' && signal.metadata.newLocations && (
                  <Badge variant="outline" className="text-xs border-gray-300 text-gray-700">
                    {signal.metadata.newLocations.length} new markets
                  </Badge>
                )}
              </div>

              {/* Source and Timing */}
              <div className="flex items-center justify-between text-xs text-gray-500 pt-2 border-t border-gray-100">
                <span className="font-medium">Source: {signal.source}</span>
                <span>{new Date(signal.detectedAt).toLocaleDateString()}</span>
              </div>

              {/* Action Button for Actionable Signals */}
              {signal.actionable && (
                <div className="pt-2">
                  <Button variant="outline" size="sm" className="w-full text-xs border-[#F7D774] text-gray-900 hover:bg-[#F7D774]/10">
                    <FileText className="h-3 w-3 mr-1.5" />
                    Generate Investment Brief
                    <ArrowRight className="h-3 w-3 ml-1.5" />
                  </Button>
                </div>
              )}
            </div>
          </Card>
        ))}

        {filteredSignals.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            <Star className="h-10 w-10 mx-auto mb-3 text-gray-400" />
            <p className="text-sm font-medium">No signals detected for this filter</p>
            <p className="text-xs text-gray-400 mt-1">Try adjusting your filters or check back later</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
