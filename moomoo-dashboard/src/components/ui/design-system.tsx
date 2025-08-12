'use client';

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import DashboardBackground from "@/components/ui/dashboard-background";
import { 
  Search, 
  Bell, 
  Plus, 
  TrendingUp, 
  DollarSign, 
  Building2, 
  Play, 
  Pause, 
  Eye, 
  Settings,
  Filter,
  MoreHorizontal 
} from "lucide-react";

export default function DesignSystem() {
  return (
    <div className="min-h-screen bg-white p-8">
      <div className="max-w-7xl mx-auto space-y-12">
        
        {/* Header */}
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold text-gray-900">
            Moo Climate Design System
          </h1>
          <p className="text-lg text-gray-600">
            Minimalistic, modern, and consistent design components
          </p>
        </div>

        {/* Color Palette */}
        <section className="space-y-6">
          <h2 className="text-3xl font-semibold text-gray-900">Color Palette</h2>
          
          <div className="space-y-4">
            <h3 className="text-xl font-medium text-gray-800">Brand Colors</h3>
            <div className="flex gap-4">
              <div className="space-y-2">
                <div className="w-20 h-20 rounded-xl shadow-sm border" style={{ backgroundColor: '#F7D774' }}></div>
                <p className="text-sm text-gray-600">Moo Yellow</p>
                <p className="text-xs text-gray-400">#F7D774</p>
                <p className="text-xs text-gray-500">Primary actions</p>
              </div>
              <div className="space-y-2">
                <div className="w-20 h-20 rounded-xl shadow-sm border" style={{ backgroundColor: '#2E5E4E' }}></div>
                <p className="text-sm text-gray-600">Moo Green</p>
                <p className="text-xs text-gray-400">#2E5E4E</p>
                <p className="text-xs text-gray-500">Climate focus</p>
              </div>
              <div className="space-y-2">
                <div className="w-20 h-20 rounded-xl shadow-sm border" style={{ backgroundColor: '#69B8E5' }}></div>
                <p className="text-sm text-gray-600">Sidebar Blue</p>
                <p className="text-xs text-gray-400">#69B8E5</p>
                <p className="text-xs text-gray-500">Navigation</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-xl font-medium text-gray-800">Neutral Palette</h3>
            <div className="flex gap-2">
              <div className="space-y-2">
                <div className="w-16 h-16 bg-gray-50 rounded-lg shadow-sm border"></div>
                <p className="text-xs text-gray-600">Gray 50</p>
              </div>
              <div className="space-y-2">
                <div className="w-16 h-16 bg-gray-100 rounded-lg shadow-sm border"></div>
                <p className="text-xs text-gray-600">Gray 100</p>
              </div>
              <div className="space-y-2">
                <div className="w-16 h-16 bg-gray-200 rounded-lg shadow-sm border"></div>
                <p className="text-xs text-gray-600">Gray 200</p>
              </div>
              <div className="space-y-2">
                <div className="w-16 h-16 bg-gray-400 rounded-lg shadow-sm border"></div>
                <p className="text-xs text-gray-600">Gray 400</p>
              </div>
              <div className="space-y-2">
                <div className="w-16 h-16 bg-gray-600 rounded-lg shadow-sm border"></div>
                <p className="text-xs text-gray-600">Gray 600</p>
              </div>
              <div className="space-y-2">
                <div className="w-16 h-16 bg-gray-900 rounded-lg shadow-sm border"></div>
                <p className="text-xs text-gray-600">Gray 900</p>
              </div>
            </div>
          </div>

          {/* Color Usage Guidelines */}
          <div className="space-y-4">
            <h3 className="text-xl font-medium text-gray-800">Color Usage Guidelines</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card className="p-4 border-l-4" style={{ borderLeftColor: '#F7D774' }}>
                <h4 className="font-semibold text-gray-900 mb-2">Moo Yellow (#F7D774)</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• Primary action buttons</li>
                  <li>• <strong>Active navigation states</strong></li>
                  <li>• Important highlights</li>
                  <li>• Success indicators</li>
                  <li>• Featured badges</li>
                  <li>• Focus states</li>
                </ul>
              </Card>
              
              <Card className="p-4 border-l-4" style={{ borderLeftColor: '#2E5E4E' }}>
                <h4 className="font-semibold text-gray-900 mb-2">Moo Green (#2E5E4E)</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• Climate tech tags</li>
                  <li>• Secondary actions</li>
                  <li>• Environmental indicators</li>
                  <li>• Success states</li>
                  <li>• Nature-related content</li>
                </ul>
              </Card>
              
              <Card className="p-4 border-l-4" style={{ borderLeftColor: '#69B8E5' }}>
                <h4 className="font-semibold text-gray-900 mb-2">Sidebar Blue (#69B8E5)</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• Sidebar background</li>
                  <li>• Navigation elements</li>
                  <li>• Active states in nav</li>
                  <li>• Information badges</li>
                  <li>• Data visualization accents</li>
                </ul>
              </Card>
            </div>
          </div>
        </section>

        {/* Typography */}
        <section className="space-y-6">
          <h2 className="text-3xl font-semibold text-gray-900">Typography</h2>
          
          <div className="space-y-4">
            <div className="space-y-2">
              <h1 className="text-4xl font-bold text-gray-900">Heading 1 - Dashboard Title</h1>
              <p className="text-xs text-gray-500">32px/40px, font-weight: 700, letter-spacing: -0.02em</p>
            </div>
            
            <div className="space-y-2">
              <h2 className="text-3xl font-semibold text-gray-900">Heading 2 - Section Title</h2>
              <p className="text-xs text-gray-500">24px/32px, font-weight: 600, letter-spacing: -0.01em</p>
            </div>
            
            <div className="space-y-2">
              <h3 className="text-2xl font-medium text-gray-900">Heading 3 - Card Title</h3>
              <p className="text-xs text-gray-500">20px/28px, font-weight: 600</p>
            </div>
            
            <div className="space-y-2">
              <h4 className="text-xl font-medium text-gray-900">Heading 4 - Component Title</h4>
              <p className="text-xs text-gray-500">18px/24px, font-weight: 500</p>
            </div>
            
            <div className="space-y-2">
              <p className="text-lg text-gray-700">Body Large - Important information</p>
              <p className="text-xs text-gray-500">16px/24px, font-weight: 400</p>
            </div>
            
            <div className="space-y-2">
              <p className="text-base text-gray-600">Body Text - Standard paragraph text</p>
              <p className="text-xs text-gray-500">14px/20px, font-weight: 400</p>
            </div>
            
            <div className="space-y-2">
              <p className="text-sm text-gray-500">Small Text - Secondary information</p>
              <p className="text-xs text-gray-500">12px/16px, font-weight: 400</p>
            </div>
            
            <div className="space-y-2">
              <p className="text-caption">CAPTION TEXT</p>
              <p className="text-xs text-gray-500">11px/16px, font-weight: 500, letter-spacing: 0.02em</p>
            </div>
          </div>
        </section>

        {/* Buttons */}
        <section className="space-y-6">
          <h2 className="text-3xl font-semibold text-gray-900">Buttons</h2>
          
          <div className="flex flex-wrap gap-4">
            <Button style={{ backgroundColor: '#F7D774' }} className="hover:opacity-90 text-gray-900 font-medium rounded-lg px-4 py-2 shadow-sm">
              Primary Button
            </Button>
            
            <Button variant="secondary" className="bg-white text-gray-700 border border-gray-200 hover:bg-gray-50 rounded-lg px-4 py-2">
              Secondary Button
            </Button>
            
            <Button variant="ghost" className="text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-lg px-3 py-2">
              Ghost Button
            </Button>
            
            <Button size="sm" style={{ backgroundColor: '#F7D774' }} className="hover:opacity-90 text-gray-900 text-sm px-3 py-1.5 rounded-lg">
              Small Primary
            </Button>
            
            <Button variant="ghost" size="sm" className="text-gray-500 hover:text-gray-700 hover:bg-gray-50 p-2 rounded-lg">
              <Settings className="h-4 w-4" />
            </Button>
          </div>
        </section>

        {/* Navigation & Sidebar */}
        <section className="space-y-6">
          <h2 className="text-3xl font-semibold text-gray-900">Navigation & Sidebar</h2>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Sidebar Example */}
            <div className="space-y-4">
              <h3 className="text-lg font-medium text-gray-800">Sidebar Navigation</h3>
              <div className="p-4 rounded-xl border border-gray-200">
                <div className="w-48 h-64 rounded-lg shadow-lg" style={{ backgroundColor: '#69B8E5' }}>
                  <div className="p-4 space-y-3">
                    <div className="flex items-center space-x-3 mb-6">
                      <div className="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center">
                        <Building2 className="h-5 w-5 text-white" />
                      </div>
                      <span className="text-white font-semibold">MooMoo Climate</span>
                    </div>
                    
                    <div className="space-y-2">
                      {['Dashboard', 'Advanced Search', 'History', 'Saved Searches', 'Reports'].map((item, i) => (
                        <div key={item} className={`p-3 rounded-2xl text-sm transition-all duration-200 font-medium ${
                          i === 0 ? 'text-gray-900 font-semibold shadow-sm' : 'text-white/80 hover:bg-white/10 hover:text-white'
                        }`} style={i === 0 ? { backgroundColor: '#F7D774' } : {}}>
                          {item}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Navigation Buttons */}
            <div className="space-y-4">
              <h3 className="text-lg font-medium text-gray-800">Navigation Elements</h3>
              <div className="space-y-3">
                <Button 
                  style={{ backgroundColor: '#F7D774' }}
                  className="w-full justify-start text-gray-900 hover:opacity-90 rounded-2xl px-4 py-3 font-semibold shadow-sm"
                >
                  <TrendingUp className="h-4 w-4 mr-3" />
                  Dashboard (Active)
                </Button>
                
                <Button 
                  variant="ghost"
                  className="w-full justify-start text-white/80 hover:bg-white/10 hover:text-white rounded-2xl px-4 py-3 font-medium transition-all duration-200"
                  style={{ backgroundColor: 'transparent' }}
                >
                  <Search className="h-4 w-4 mr-3" />
                  Advanced Search
                </Button>
                
                <Button 
                  variant="ghost"
                  className="w-full justify-start text-white/80 hover:bg-white/10 hover:text-white rounded-2xl px-4 py-3 font-medium transition-all duration-200"
                  style={{ backgroundColor: 'transparent' }}
                >
                  <Bell className="h-4 w-4 mr-3" />
                  Alerts
                </Button>

                {/* Navigation State Examples */}
                <div className="pt-4">
                  <p className="text-sm font-medium text-gray-700 mb-3">Navigation States</p>
                  <div className="space-y-2">
                    <div className="text-xs text-gray-600">
                      <strong>Active State:</strong> Yellow background (#F7D774) with dark gray text (Gray 900)
                    </div>
                    <div className="text-xs text-gray-600">
                      <strong>Hover State:</strong> White overlay (white/10) with white text
                    </div>
                    <div className="text-xs text-gray-600">
                      <strong>Normal State:</strong> Semi-transparent white text (white/80)
                    </div>
                  </div>
                  
                  <div className="flex gap-2 mt-3">
                    <Badge style={{ backgroundColor: '#F7D774', color: '#111827' }} className="rounded-full px-3 py-1 text-xs font-semibold">
                      Active
                    </Badge>
                    <Badge style={{ 
                      backgroundColor: 'rgba(255, 255, 255, 0.1)', 
                      color: 'white',
                      borderColor: 'rgba(255, 255, 255, 0.2)'
                    }} className="border rounded-full px-3 py-1 text-xs">
                      Hover
                    </Badge>
                    <Badge style={{ 
                      backgroundColor: 'transparent', 
                      color: 'rgba(255, 255, 255, 0.8)',
                      borderColor: 'rgba(255, 255, 255, 0.3)'
                    }} className="border rounded-full px-3 py-1 text-xs">
                      Normal
                    </Badge>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Cards */}
        <section className="space-y-6">
          <h2 className="text-3xl font-semibold text-gray-900">Cards</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <Card className="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200">
              <CardHeader className="pb-4">
                <CardTitle className="text-lg font-semibold text-gray-900">Standard Card</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600">
                  Clean white background with subtle border and shadow
                </p>
                <div className="mt-4 flex gap-2">
                  <Badge className="bg-gray-100 text-gray-700 rounded-full px-3 py-1 text-xs">
                    Tag
                  </Badge>
                  <Badge style={{ backgroundColor: '#F7D774', color: '#1F2937' }} className="rounded-full px-3 py-1 text-xs">
                    Featured
                  </Badge>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-white border border-gray-200 rounded-xl shadow-md hover:shadow-lg transition-shadow duration-200">
              <CardHeader className="pb-4">
                <CardTitle className="text-lg font-semibold text-gray-900">Elevated Card</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600">
                  Enhanced shadow for important content
                </p>
                <div className="mt-4">
                  <div className="flex items-center gap-2 text-sm text-gray-500">
                    <TrendingUp className="h-4 w-4" />
                    <span>Performance metrics</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="rounded-xl shadow-sm" style={{ 
              background: 'linear-gradient(to bottom right, rgba(247, 215, 116, 0.1), rgba(46, 94, 78, 0.1))',
              borderColor: 'rgba(247, 215, 116, 0.2)'
            }}>
              <CardHeader className="pb-4">
                <CardTitle className="text-lg font-semibold text-gray-900">Accent Card</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600">
                  Subtle brand accent for special content
                </p>
                <div className="mt-4">
                  <Button size="sm" style={{ backgroundColor: '#F7D774' }} className="hover:opacity-90 text-gray-900 rounded-lg px-3 py-1.5 text-sm">
                    Take Action
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </section>

        {/* Form Elements */}
        <section className="space-y-6">
          <h2 className="text-3xl font-semibold text-gray-900">Form Elements</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Search Input
                </label>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                  <Input 
                    placeholder="Search companies..." 
                    className="pl-10 bg-white border border-gray-200 rounded-lg px-3 py-2"
                    style={{
                      '--tw-ring-color': '#F7D774'
                    } as React.CSSProperties}
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Standard Input
                </label>
                <Input 
                  placeholder="Enter value..." 
                  className="bg-white border border-gray-200 rounded-lg px-3 py-2"
                  style={{
                    '--tw-ring-color': '#F7D774'
                  } as React.CSSProperties}
                />
              </div>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Filter Tags
                </label>
                <div className="flex flex-wrap gap-2">
                  <Badge className="bg-gray-100 text-gray-700 border border-gray-200 rounded-full px-3 py-1 text-sm">
                    Series A
                  </Badge>
                  <Badge style={{ 
                    backgroundColor: 'rgba(46, 94, 78, 0.1)', 
                    color: '#2E5E4E',
                    borderColor: 'rgba(46, 94, 78, 0.2)'
                  }} className="border rounded-full px-3 py-1 text-sm">
                    Climate Tech
                  </Badge>
                  <Badge style={{ backgroundColor: '#F7D774', color: '#1F2937' }} className="rounded-full px-3 py-1 text-sm">
                    AI Focus
                  </Badge>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Data Display */}
        <section className="space-y-6">
          <h2 className="text-3xl font-semibold text-gray-900">Data Display</h2>
          
          <Card className="bg-white border border-gray-200 rounded-xl shadow-sm">
            <CardHeader>
              <CardTitle className="text-lg font-semibold text-gray-900">Recent Funding Rounds</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {/* Sample data rows */}
                {[
                  { company: "SolarTech AI", stage: "Series A", amount: "$15M", sector: "Solar Energy" },
                  { company: "CarbonCapture Plus", stage: "Series B", amount: "$32M", sector: "Carbon Capture" },
                  { company: "GridFlow Energy", stage: "Seed", amount: "$8M", sector: "Energy Storage" },
                ].map((deal, i) => (
                  <div key={i} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-100">
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900">{deal.company}</h4>
                      <p className="text-sm text-gray-600">{deal.sector}</p>
                    </div>
                    <div className="flex items-center gap-4">
                      <Badge className="bg-gray-100 text-gray-700 rounded-full px-3 py-1 text-sm">
                        {deal.stage}
                      </Badge>
                      <div className="text-right">
                        <p className="font-semibold text-gray-900">{deal.amount}</p>
                      </div>
                      <Button variant="ghost" size="sm" className="text-gray-400 hover:text-gray-600 p-2 rounded-lg">
                        <Eye className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Dashboard Background */}
        <section className="space-y-6">
          <h2 className="text-3xl font-semibold text-gray-900">Dashboard Background</h2>
          
          <div className="space-y-4">
            <h3 className="text-xl font-medium text-gray-800">Animated Background Component</h3>
            <p className="text-gray-600">
              A sophisticated animated background that creates depth and visual interest while maintaining focus on content.
            </p>
            
            {/* Live Preview */}
            <div className="border border-gray-200 rounded-lg overflow-hidden">
              <div className="relative h-96">
                <DashboardBackground>
                  <div className="w-full h-full flex items-center justify-center">
                    <Card className="w-80 bg-white/90 backdrop-blur-sm shadow-lg">
                      <CardHeader>
                        <CardTitle className="text-xl text-gray-900">Sample Dashboard Content</CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-2">
                            <DollarSign className="h-5 w-5 text-[#F7D774]" />
                            <span className="font-medium text-gray-900">$24.5M</span>
                          </div>
                          <Badge className="bg-[#2E5E4E] text-white rounded-full px-3 py-1">
                            Series A
                          </Badge>
                        </div>
                        <div className="space-y-2">
                          <div className="h-2 bg-gray-200 rounded-full">
                            <div className="h-2 bg-[#F7D774] rounded-full w-3/4"></div>
                          </div>
                          <p className="text-sm text-gray-600">Climate tech funding progress</p>
                        </div>
                        <div className="flex space-x-2">
                          <Button size="sm" className="bg-[#F7D774] hover:bg-[#F7D774]/90 text-gray-900 flex-1">
                            View Details
                          </Button>
                          <Button variant="outline" size="sm" className="border-[#2E5E4E] text-[#2E5E4E] hover:bg-[#2E5E4E]/10">
                            <Eye className="h-4 w-4" />
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                </DashboardBackground>
              </div>
              <div className="p-4 bg-gray-50 border-t border-gray-200">
                <p className="text-sm text-gray-600">
                  <strong>Interactive Preview:</strong> The background features gentle pulsing elements, floating particles, and subtle drifting animations.
                </p>
              </div>
            </div>
            
            {/* Component Code */}
            <div className="space-y-4">
              <h4 className="text-lg font-medium text-gray-800">Component Usage</h4>
              <div className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
                <pre className="text-green-400 text-sm">
{`import DashboardBackground from '@/components/ui/dashboard-background';

export default function MyDashboard() {
  return (
    <DashboardBackground>
      {/* Your dashboard content here */}
      <div className="p-8">
        <h1>My Dashboard</h1>
        {/* Cards, widgets, etc. */}
      </div>
    </DashboardBackground>
  );
}`}
                </pre>
              </div>
            </div>
            
            {/* Animation Details */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card className="p-4">
                <h4 className="font-semibold text-gray-900 mb-2">Gentle Pulse</h4>
                <p className="text-sm text-gray-600 mb-3">
                  Large background orbs with 6-second breathing animation using brand colors.
                </p>
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 bg-[#F7D774]/30 rounded-full animate-gentle-pulse"></div>
                  <div className="w-4 h-4 bg-[#2E5E4E]/30 rounded-full animate-gentle-pulse delay-1000"></div>
                  <div className="w-4 h-4 bg-[#AEE1F6]/30 rounded-full animate-gentle-pulse delay-2000"></div>
                </div>
              </Card>
              
              <Card className="p-4">
                <h4 className="font-semibold text-gray-900 mb-2">Float Animation</h4>
                <p className="text-sm text-gray-600 mb-3">
                  Small floating elements that rise and fall with 8-second cycles.
                </p>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-[#F7D774]/40 rounded-full animate-float"></div>
                  <div className="w-3 h-3 bg-[#2E5E4E]/50 rounded-full animate-float delay-700"></div>
                  <div className="w-3 h-3 bg-[#AEE1F6]/40 rounded-full animate-float delay-1100"></div>
                </div>
              </Card>
              
              <Card className="p-4">
                <h4 className="font-semibold text-gray-900 mb-2">Drift Movement</h4>
                <p className="text-sm text-gray-600 mb-3">
                  Subtle horizontal drift with rotation over 12-second periods.
                </p>
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 bg-[#F7D774]/30 rounded-full animate-drift"></div>
                  <div className="w-3 h-3 bg-[#2E5E4E]/40 rounded-full animate-drift delay-1500"></div>
                </div>
              </Card>
            </div>
            
            {/* Design Guidelines */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-semibold text-blue-900 mb-2">Design Guidelines</h4>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• Use as a container for main dashboard layouts</li>
                <li>• Orbs are positioned to avoid sidebar overlap (main content area only)</li>
                <li>• Background elements are pointer-events-none to avoid interaction conflicts</li>
                <li>• Colors use low opacity (15-40%) to maintain content readability</li>
                <li>• Multiple orb sizes create depth: large (40-56px), medium (28-36px), small (12-20px)</li>
                <li>• Animations are performance-optimized with CSS transforms</li>
                <li>• Pattern overlay is constrained to main content area (left-64 offset)</li>
                <li>• Consider reduced motion preferences for accessibility</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Status & Feedback */}
        <section className="space-y-6">
          <h2 className="text-3xl font-semibold text-gray-900">Status & Feedback</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <p className="text-sm font-medium text-green-800">Success State</p>
              </div>
              <p className="text-sm text-green-600 mt-1">Operation completed successfully</p>
            </div>
            
            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                <p className="text-sm font-medium text-yellow-800">Warning State</p>
              </div>
              <p className="text-sm text-yellow-600 mt-1">Please review this information</p>
            </div>
            
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                <p className="text-sm font-medium text-red-800">Error State</p>
              </div>
              <p className="text-sm text-red-600 mt-1">An error occurred, please try again</p>
            </div>
          </div>
        </section>

      </div>
    </div>
  );
}
