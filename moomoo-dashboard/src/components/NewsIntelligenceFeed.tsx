'use client';

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, ExternalLink, TrendingUp, DollarSign, Users, Building2, AlertCircle, Clock, Star, Loader2 } from "lucide-react";
import { fetchNews, type NewsItem } from "@/lib/api";

export default function NewsIntelligenceFeed() {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [filteredNews, setFilteredNews] = useState<NewsItem[]>([]);
  const [selectedType, setSelectedType] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load real news data
  useEffect(() => {
    async function loadNews() {
      try {
        setLoading(true);
        setError(null);
        const newsData = await fetchNews(20);
        setNews(newsData);
        setFilteredNews(newsData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load news');
        console.error('Error loading news:', err);
      } finally {
        setLoading(false);
      }
    }

    loadNews();
  }, []);

  useEffect(() => {
    let filtered = news;

    // Filter by type
    if (selectedType !== 'all') {
      filtered = filtered.filter(item => item.newsType === selectedType);
    }

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(item => 
        item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.companyMentions.some(company => 
          company.toLowerCase().includes(searchTerm.toLowerCase())
        )
      );
    }

    // Sort by relevance score
    filtered.sort((a, b) => b.relevanceScore - a.relevanceScore);

    setFilteredNews(filtered);
  }, [news, selectedType, searchTerm]);

  const getNewsTypeIcon = (type: string) => {
    switch (type) {
      case 'funding':
        return <DollarSign className="h-4 w-4" />;
      case 'product':
        return <TrendingUp className="h-4 w-4" />;
      case 'partnership':
        return <Users className="h-4 w-4" />;
      case 'general':
        return <Building2 className="h-4 w-4" />;
      default:
        return <AlertCircle className="h-4 w-4" />;
    }
  };

  const getNewsTypeColor = (type: string) => {
    switch (type) {
      case 'funding':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'product':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'partnership':
        return 'bg-purple-100 text-purple-800 border-purple-200';
      case 'general':
        return 'bg-orange-100 text-orange-800 border-orange-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getRelevanceColor = (score: number) => {
    if (score >= 90) return 'text-[#2E5E4E] bg-[#2E5E4E]/10';
    if (score >= 80) return 'text-[#2E5E4E] bg-[#AEE1F6]/30';
    if (score >= 70) return 'text-yellow-600 bg-yellow-50';
    return 'text-gray-600 bg-gray-50';
  };

  const newsTypes = [
    { value: 'all', label: 'All News', count: news.length },
    { value: 'funding', label: 'Funding', count: news.filter(n => n.newsType === 'funding').length },
    { value: 'product', label: 'Products', count: news.filter(n => n.newsType === 'product').length },
    { value: 'partnership', label: 'Partnerships', count: news.filter(n => n.newsType === 'partnership').length },
    { value: 'general', label: 'General', count: news.filter(n => n.newsType === 'general').length },
  ];

  return (
    <Card className="h-full bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 border-0">
      <CardHeader className="pb-6 bg-gradient-to-r from-[#AEE1F6]/20 to-[#F3F3F3] rounded-t-2xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-orange-100 rounded-2xl shadow-sm">
              <TrendingUp className="h-5 w-5 text-orange-600" />
            </div>
            <div>
              <CardTitle className="text-lg font-bold text-[#2D2D2D]">
                Climate Tech News Intelligence
              </CardTitle>
              <p className="text-sm text-gray-600 mt-1">AI-powered news analysis & insights</p>
            </div>
          </div>
          <Badge variant="secondary" className="text-xs bg-green-100 text-green-700 border-green-200 rounded-full shadow-sm px-3 py-1 font-medium">
            <div className="w-2 h-2 bg-[#2E5E4E] rounded-full mr-2 animate-pulse"></div>
            Live Feed
          </Badge>
        </div>
        
        {/* Search and Filters */}
        <div className="space-y-4 mt-6">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <Input
              placeholder="Search news or companies..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-12 bg-gray-50 border-0 text-[#2D2D2D] focus:bg-white focus:shadow-lg h-12 rounded-2xl transition-all duration-200"
            />
          </div>
          
          <div className="flex flex-wrap gap-2">
            {newsTypes.map((type) => (
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
        </div>
      </CardHeader>

      <CardContent className="space-y-4 max-h-[600px] overflow-y-auto">
        {loading && (
          <div className="text-center py-8">
            <Loader2 className="h-8 w-8 mx-auto mb-2 animate-spin text-[#2E5E4E]" />
            <p className="text-sm text-gray-500">Loading climate tech news...</p>
          </div>
        )}

        {error && (
          <div className="text-center py-8 text-red-500">
            <AlertCircle className="h-8 w-8 mx-auto mb-2" />
            <p className="text-sm">Error loading news: {error}</p>
            <Button 
              variant="outline" 
              size="sm" 
              className="mt-2"
              onClick={() => window.location.reload()}
            >
              Retry
            </Button>
          </div>
        )}

        {!loading && !error && filteredNews.map((item) => (
          <Card key={item.id} className="p-4 hover:shadow-md transition-shadow">
            <div className="space-y-3">
              {/* Header */}
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1">
                  <h3 className="font-medium text-sm leading-5 mb-2">{item.title}</h3>
                  <div className="flex items-center gap-2 text-xs text-gray-500">
                    <Clock className="h-3 w-3" />
                    {new Date(item.publishedAt).toLocaleDateString()}
                    <span>•</span>
                    <span>{item.source}</span>
                  </div>
                </div>
                
                <div className="flex flex-col items-end gap-2">
                  <div className={`px-2 py-1 rounded-full text-xs font-medium ${getRelevanceColor(item.relevanceScore)}`}>
                    {item.relevanceScore}% Match
                  </div>
                  <Button variant="ghost" size="sm" asChild>
                    <a href={item.url} target="_blank" rel="noopener noreferrer">
                      <ExternalLink className="h-3 w-3" />
                    </a>
                  </Button>
                </div>
              </div>

              {/* News Type and Funding Info */}
              <div className="flex items-center gap-2 flex-wrap">
                <Badge className={`text-xs ${getNewsTypeColor(item.newsType)}`}>
                  {getNewsTypeIcon(item.newsType)}
                  <span className="ml-1 capitalize">{item.newsType}</span>
                </Badge>
                
                {item.fundingAmount && (
                  <Badge variant="secondary" className="text-xs">
                    {item.fundingAmount}
                  </Badge>
                )}
                
                {item.fundingStage && (
                  <Badge variant="outline" className="text-xs">
                    {item.fundingStage}
                  </Badge>
                )}
              </div>

              {/* Company Mentions */}
              {item.companyMentions.length > 0 && (
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-xs text-gray-500">Companies:</span>
                  {item.companyMentions.map((company) => (
                    <Badge key={company} variant="secondary" className="text-xs">
                      <Building2 className="h-3 w-3 mr-1" />
                      {company}
                    </Badge>
                  ))}
                </div>
              )}

              {/* Key Signals */}
              <div className="flex items-center gap-2 flex-wrap">
                <span className="text-xs text-gray-500">Signals:</span>
                {item.keySignals.map((signal, index) => (
                  <Badge key={index} variant="outline" className="text-xs">
                    <Star className="h-3 w-3 mr-1" />
                    {signal}
                  </Badge>
                ))}
              </div>

              {/* AI Summary */}
              <div className="bg-[#AEE1F6]/20 rounded-lg p-3">
                <div className="flex items-start gap-2">
                  <div className="bg-orange-400 rounded-full p-1">
                    <TrendingUp className="h-3 w-3 text-white" />
                  </div>
                  <p className="text-xs text-gray-700 leading-relaxed">{item.aiSummary}</p>
                </div>
              </div>
            </div>
          </Card>
        ))}

        {!loading && !error && filteredNews.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            <AlertCircle className="h-8 w-8 mx-auto mb-2" />
            <p className="text-sm">No news items match your criteria</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
