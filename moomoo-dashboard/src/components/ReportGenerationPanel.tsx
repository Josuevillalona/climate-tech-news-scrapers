'use client';

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { FileText, Download, Share2, Eye, BarChart3, Building2, DollarSign, TrendingUp, Clock } from "lucide-react";

interface ReportTemplate {
  id: string;
  name: string;
  description: string;
  type: 'deal_summary' | 'market_intelligence' | 'pipeline' | 'custom';
  icon: React.ReactNode;
  estimatedTime: string;
  sections: string[];
  sampleCompany?: string;
}

const reportTemplates: ReportTemplate[] = [
  {
    id: 'deal_summary',
    name: 'Deal Summary Report',
    description: 'Comprehensive company overview with investment thesis, market analysis, and risk assessment',
    type: 'deal_summary',
    icon: <Building2 className="h-5 w-5" />,
    estimatedTime: '2 minutes',
    sections: [
      'Executive Summary',
      'Company Overview',
      'Market Analysis',
      'Technology Assessment',
      'Financial Highlights',
      'Investment Thesis',
      'Risk Analysis',
      'Next Steps'
    ],
    sampleCompany: 'CarbonIQ'
  },
  {
    id: 'market_intelligence',
    name: 'Market Intelligence Report',
    description: 'Sector trends, competitive landscape, and market timing analysis for specific climate tech verticals',
    type: 'market_intelligence',
    icon: <BarChart3 className="h-5 w-5" />,
    estimatedTime: '3 minutes',
    sections: [
      'Market Overview',
      'Competitive Landscape',
      'Technology Trends',
      'Funding Patterns',
      'Key Players Analysis',
      'Market Timing',
      'Investment Opportunities',
      'Strategic Recommendations'
    ]
  },
  {
    id: 'pipeline',
    name: 'Pipeline Report',
    description: 'Current opportunities ranked by Alex Score with key metrics and action items',
    type: 'pipeline',
    icon: <TrendingUp className="h-5 w-5" />,
    estimatedTime: '1 minute',
    sections: [
      'Pipeline Overview',
      'High Priority Deals',
      'Deal Flow Analysis',
      'Sector Distribution',
      'Geographic Breakdown',
      'Funding Stage Analysis',
      'Action Items',
      'Weekly Summary'
    ]
  },
  {
    id: 'custom',
    name: 'Custom Report Builder',
    description: 'Build custom reports with specific data points and branding for partner presentations',
    type: 'custom',
    icon: <FileText className="h-5 w-5" />,
    estimatedTime: '5 minutes',
    sections: [
      'Custom Sections',
      'Data Selection',
      'Branding Options',
      'Export Formats'
    ]
  }
];

interface GeneratedReport {
  id: string;
  name: string;
  type: string;
  generatedAt: string;
  pages: number;
  status: 'generating' | 'ready' | 'error';
}

export default function ReportGenerationPanel() {
  const [generatedReports, setGeneratedReports] = useState<GeneratedReport[]>([
    {
      id: '1',
      name: 'CarbonIQ Deal Summary',
      type: 'Deal Summary Report',
      generatedAt: '2025-08-10T08:30:00Z',
      pages: 12,
      status: 'ready'
    },
    {
      id: '2',
      name: 'Q3 Pipeline Review',
      type: 'Pipeline Report',
      generatedAt: '2025-08-10T07:15:00Z',
      pages: 8,
      status: 'ready'
    }
  ]);

  const [isGenerating, setIsGenerating] = useState<string | null>(null);

  const handleGenerateReport = async (templateId: string, templateName: string) => {
    setIsGenerating(templateId);
    
    // Simulate report generation
    setTimeout(() => {
      const newReport: GeneratedReport = {
        id: Date.now().toString(),
        name: `${templateName} - ${new Date().toLocaleDateString()}`,
        type: templateName,
        generatedAt: new Date().toISOString(),
        pages: Math.floor(Math.random() * 15) + 5,
        status: 'ready'
      };
      
      setGeneratedReports(prev => [newReport, ...prev]);
      setIsGenerating(null);
    }, 3000);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ready':
        return 'bg-green-100 text-green-800';
      case 'generating':
        return 'bg-yellow-100 text-yellow-800';
      case 'error':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-8">
      {/* Report Templates */}
      <Card className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 border-0">
        <CardHeader className="pb-6 bg-gradient-to-r from-[#2E5E4E]/10 to-[#F7D774]/20 rounded-t-2xl">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-orange-100 rounded-2xl shadow-sm">
              <FileText className="h-5 w-5 text-orange-600" />
            </div>
            <div>
              <CardTitle className="text-lg font-bold text-[#2D2D2D]">
                Professional Report Generator
              </CardTitle>
              <p className="text-sm text-gray-600 mt-1">
                Generate presentation-ready reports instantly for partner meetings and investment decisions
              </p>
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="space-y-6 p-6">
          {reportTemplates.map((template) => (
            <Card key={template.id} className="p-6 hover:shadow-lg transition-all duration-300 rounded-2xl border border-gray-200 bg-gradient-to-r from-white to-gray-50">
              <div className="flex items-start justify-between gap-6">
                  <div className="flex items-start gap-4 flex-1">
                    <div className="p-3 bg-orange-100 rounded-2xl shadow-sm">
                      {template.icon}
                    </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-base mb-2 text-[#2D2D2D]">{template.name}</h3>
                    <p className="text-sm text-gray-600 mb-4 leading-relaxed">{template.description}</p>
                    
                    <div className="flex items-center gap-6 text-sm text-gray-500 mb-4">
                      <div className="flex items-center gap-2 bg-gray-100 px-3 py-1 rounded-full">
                        <Clock className="h-3 w-3" />
                        {template.estimatedTime}
                      </div>
                      <div className="flex items-center gap-2 bg-blue-100 px-3 py-1 rounded-full text-blue-700">
                        <FileText className="h-3 w-3" />
                        {template.sections.length} sections
                      </div>
                    </div>
                    
                    {/* Preview sections */}
                    <div className="flex flex-wrap gap-2">
                      {template.sections.slice(0, 4).map((section, index) => (
                        <Badge key={index} variant="outline" className="text-xs border-gray-300 text-gray-600 rounded-full">
                          {section}
                        </Badge>
                      ))}
                      {template.sections.length > 4 && (
                        <Badge variant="outline" className="text-xs border-gray-300 text-gray-600 rounded-full">
                          +{template.sections.length - 4} more
                        </Badge>
                      )}
                    </div>
                  </div>
                </div>
                
                <div className="flex flex-col gap-3">
                  <Button
                    size="sm"
                    onClick={() => handleGenerateReport(template.id, template.name)}
                    disabled={isGenerating === template.id}
                    className="text-sm bg-[#F7D774] hover:bg-[#F7D774]/90 text-[#2D2D2D] rounded-full px-6 py-2 font-medium shadow-md transition-all duration-200"
                  >
                    {isGenerating === template.id ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-[#2D2D2D] mr-2"></div>
                        Generating...
                      </>
                    ) : (
                      <>
                        <FileText className="h-4 w-4 mr-2" />
                        Generate
                      </>
                    )}
                  </Button>
                  
                  {template.sampleCompany && (
                    <Button variant="outline" size="sm" className="text-sm rounded-full px-6 py-2 font-medium border-gray-300 text-gray-600 hover:bg-gray-50 transition-all duration-200">
                      <Eye className="h-4 w-4 mr-2" />
                      Preview
                    </Button>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </CardContent>
      </Card>

      {/* Generated Reports */}
      <Card className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 border-0">
        <CardHeader className="pb-6 bg-gradient-to-r from-[#AEE1F6]/20 to-[#F3F3F3] rounded-t-2xl">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-orange-100 rounded-2xl shadow-sm">
              <Download className="h-5 w-5 text-orange-600" />
            </div>
            <div>
              <CardTitle className="text-lg font-bold text-[#2D2D2D]">
                Recent Reports
              </CardTitle>
              <p className="text-sm text-gray-600 mt-1">Access and share your generated reports</p>
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="space-y-3">
          {generatedReports.map((report) => (
            <Card key={report.id} className="p-3">
              <div className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-3 flex-1">
                  <FileText className="h-4 w-4 text-gray-400" />
                  
                  <div className="flex-1">
                    <h4 className="font-medium text-sm">{report.name}</h4>
                    <div className="flex items-center gap-3 text-xs text-gray-500">
                      <span>{report.type}</span>
                      <span>•</span>
                      <span>{report.pages} pages</span>
                      <span>•</span>
                      <span>{new Date(report.generatedAt).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  <Badge className={`text-xs ${getStatusColor(report.status)}`}>
                    {report.status}
                  </Badge>
                  
                  {report.status === 'ready' && (
                    <div className="flex gap-1">
                      <Button variant="outline" size="sm" className="text-xs">
                        <Download className="h-3 w-3" />
                      </Button>
                      <Button variant="outline" size="sm" className="text-xs">
                        <Share2 className="h-3 w-3" />
                      </Button>
                    </div>
                  )}
                </div>
              </div>
            </Card>
          ))}
          
          {generatedReports.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <FileText className="h-8 w-8 mx-auto mb-2" />
              <p className="text-sm">No reports generated yet</p>
              <p className="text-xs">Generate your first report using the templates above</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
