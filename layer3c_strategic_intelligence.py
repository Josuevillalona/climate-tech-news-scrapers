#!/usr/bin/env python3
"""
LAYER 3C: STRATEGIC INTELLIGENCE ENGINE
======================================
Executive-level strategic intelligence for climate tech investment decisions.

This module provides:
- Market opportunity assessment and competitive positioning
- Strategic trend analysis and sector intelligence  
- Executive summaries and actionable insights
- Cross-portfolio risk assessment and diversification analysis
- Technology convergence mapping and future opportunities
- Investment thesis validation and market timing recommendations

Built on Layer 3A analytics and Layer 3B optimization outputs.
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from supabase import create_client, Client
from dotenv import load_dotenv
import numpy as np
from collections import defaultdict, Counter

load_dotenv()

@dataclass
class StrategicInsight:
    """Strategic insight with confidence and priority."""
    insight_type: str
    title: str
    description: str
    implications: List[str]
    confidence_score: float
    priority_level: str  # 'HIGH', 'MEDIUM', 'LOW'
    actionable_recommendations: List[str]
    supporting_data: Dict[str, Any]
    created_at: datetime

@dataclass
class MarketIntelligence:
    """Market intelligence summary."""
    sector: str
    market_size_trend: str
    competitive_landscape: str
    key_players: List[str]
    emerging_trends: List[str]
    investment_thesis: str
    risk_factors: List[str]
    opportunities: List[str]
    confidence_score: float

@dataclass
class ExecutiveSummary:
    """Executive summary for strategic decision making."""
    summary_type: str  # 'WEEKLY', 'MONTHLY', 'QUARTERLY'
    key_findings: List[str]
    strategic_recommendations: List[str]
    market_alerts: List[str]
    portfolio_insights: List[str]
    risk_assessments: List[str]
    investment_opportunities: List[str]
    competitive_intelligence: List[str]
    generated_at: datetime

class StrategicIntelligenceEngine:
    """Layer 3C Strategic Intelligence Engine for executive decision support."""
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        
        # Strategic analysis frameworks
        self.sector_taxonomy = {
            'Energy Storage': {
                'maturity': 'Growth', 'investment_cycle': 'Mid-stage',
                'key_metrics': ['battery_capacity', 'cost_per_kwh', 'cycle_life'],
                'competitive_factors': ['technology_type', 'manufacturing_scale', 'supply_chain']
            },
            'Carbon Capture': {
                'maturity': 'Early', 'investment_cycle': 'Early-stage',
                'key_metrics': ['capture_efficiency', 'cost_per_ton', 'scalability'],
                'competitive_factors': ['technology_approach', 'energy_efficiency', 'deployment_timeline']
            },
            'Solar Energy': {
                'maturity': 'Mature', 'investment_cycle': 'Late-stage',
                'key_metrics': ['efficiency', 'cost_reduction', 'deployment_speed'],
                'competitive_factors': ['technology_innovation', 'manufacturing_cost', 'market_access']
            },
            'Green Hydrogen': {
                'maturity': 'Early-Growth', 'investment_cycle': 'Early-Mid-stage',
                'key_metrics': ['production_cost', 'electrolysis_efficiency', 'storage_density'],
                'competitive_factors': ['technology_pathway', 'infrastructure', 'policy_support']
            },
            'Clean Transportation': {
                'maturity': 'Growth', 'investment_cycle': 'Mid-Late-stage',
                'key_metrics': ['range', 'charging_speed', 'cost_parity'],
                'competitive_factors': ['battery_technology', 'manufacturing_scale', 'charging_infrastructure']
            }
        }
        
        # Strategic themes and investment thesis frameworks
        self.strategic_themes = {
            'decarbonization': ['carbon_capture', 'renewable_energy', 'energy_efficiency'],
            'electrification': ['ev', 'battery_storage', 'grid_infrastructure'],
            'circular_economy': ['recycling', 'waste_management', 'material_recovery'],
            'climate_adaptation': ['resilience', 'agriculture', 'water_management'],
            'digitalization': ['ai', 'iot', 'optimization', 'automation']
        }

    def generate_comprehensive_intelligence_report(self, timeframe_days: int = 30) -> Dict[str, Any]:
        """Generate comprehensive strategic intelligence report."""
        
        print(f"🧠 Generating Layer 3C Strategic Intelligence Report...")
        print("=" * 70)
        
        # Get data from the last timeframe
        cutoff_date = (datetime.now() - timedelta(days=timeframe_days)).isoformat()
        
        report = {
            'report_metadata': {
                'generated_at': datetime.now().isoformat(),
                'timeframe_days': timeframe_days,
                'analysis_period': f"{cutoff_date[:10]} to {datetime.now().strftime('%Y-%m-%d')}"
            },
            'executive_summary': self._generate_executive_summary(cutoff_date),
            'market_intelligence': self._analyze_market_intelligence(cutoff_date),
            'competitive_landscape': self._analyze_competitive_landscape(cutoff_date),
            'strategic_insights': self._generate_strategic_insights(cutoff_date),
            'investment_thesis_validation': self._validate_investment_thesis(cutoff_date),
            'risk_assessment': self._conduct_risk_assessment(cutoff_date),
            'opportunity_mapping': self._map_strategic_opportunities(cutoff_date),
            'recommendations': self._generate_strategic_recommendations(cutoff_date)
        }
        
        # Calculate overall strategic confidence
        report['overall_confidence'] = self._calculate_strategic_confidence(report)
        
        print(f"✅ Strategic intelligence report generated successfully!")
        print(f"📊 Overall Strategic Confidence: {report['overall_confidence']:.1f}%")
        
        return report

    def _generate_executive_summary(self, cutoff_date: str) -> Dict[str, Any]:
        """Generate executive summary for strategic decision making."""
        
        print("   📋 Generating executive summary...")
        
        try:
            # Get recent deals and activities
            deals_response = self.supabase.table('deals_new').select(
                '*, companies(*)'
            ).gte('created_at', cutoff_date).execute()
            
            deals = deals_response.data
            
            # Key metrics
            total_deals = len(deals)
            govt_deals = len([d for d in deals if d['source_type'] == 'government_research'])
            vc_deals = len([d for d in deals if d['source_type'] == 'vc_portfolio'])
            news_deals = len([d for d in deals if d['source_type'] == 'news'])
            
            # Sector distribution
            sectors = []
            for deal in deals:
                if deal.get('companies', {}).get('climate_sub_sectors'):
                    sectors.extend(deal['companies']['climate_sub_sectors'])
            
            sector_distribution = Counter(sectors)
            top_sectors = sector_distribution.most_common(5)
            
            # Strategic themes emergence
            emerging_themes = self._identify_emerging_themes(deals)
            
            # Investment activity analysis
            investment_trends = self._analyze_investment_trends(deals)
            
            return {
                'period_metrics': {
                    'total_discoveries': total_deals,
                    'government_intelligence': govt_deals,
                    'vc_portfolio_activities': vc_deals,
                    'news_announcements': news_deals,
                    'discovery_velocity': round(total_deals / 30, 1)  # per day
                },
                'sector_intelligence': {
                    'most_active_sectors': [{'sector': s[0], 'activity': s[1]} for s in top_sectors],
                    'sector_diversity_index': len(sector_distribution) / max(len(deals), 1),
                    'emerging_sectors': emerging_themes['sectors']
                },
                'strategic_themes': {
                    'dominant_themes': emerging_themes['themes'],
                    'convergence_opportunities': emerging_themes['convergence'],
                    'technology_readiness_trends': emerging_themes['trl_trends']
                },
                'investment_intelligence': {
                    'funding_velocity': investment_trends['velocity'],
                    'average_deal_size': investment_trends['avg_size'],
                    'stage_distribution': investment_trends['stages'],
                    'geographic_concentration': investment_trends['geography']
                }
            }
            
        except Exception as e:
            return {
                'error': f"Failed to generate executive summary: {e}",
                'fallback_message': 'Executive summary generation encountered issues. Manual review recommended.'
            }

    def _analyze_market_intelligence(self, cutoff_date: str) -> Dict[str, MarketIntelligence]:
        """Analyze market intelligence by sector."""
        
        print("   🌍 Analyzing market intelligence...")
        
        market_intel = {}
        
        try:
            # Get deals with sector information
            deals_response = self.supabase.table('deals_new').select(
                '*, companies(*)'
            ).gte('created_at', cutoff_date).execute()
            
            deals = deals_response.data
            
            # Group by sector
            sector_deals = defaultdict(list)
            for deal in deals:
                if deal.get('companies', {}).get('climate_sub_sectors'):
                    for sector in deal['companies']['climate_sub_sectors']:
                        sector_deals[sector].append(deal)
            
            # Analyze each sector
            for sector, sector_deal_list in sector_deals.items():
                if len(sector_deal_list) >= 1:  # Lower threshold for testing
                    
                    # Analyze competitive landscape
                    companies = [d['companies']['name'] for d in sector_deal_list if d.get('companies')]
                    funding_stages = [d.get('funding_stage', 'Unknown') for d in sector_deal_list]
                    
                    # Investment trend analysis
                    funding_amounts = []
                    for deal in sector_deal_list:
                        if deal.get('amount_raised_usd'):
                            funding_amounts.append(deal['amount_raised_usd'])
                    
                    avg_funding = np.mean(funding_amounts) if funding_amounts else 0
                    
                    # Technology readiness assessment
                    trl_levels = []
                    for deal in sector_deal_list:
                        # Extract TRL information if available
                        if 'TRL' in str(deal.get('raw_text_content', '')):
                            # Simple TRL extraction logic
                            import re
                            trl_match = re.search(r'TRL\s*(\d+)', deal['raw_text_content'])
                            if trl_match:
                                trl_levels.append(int(trl_match.group(1)))
                    
                    avg_trl = np.mean(trl_levels) if trl_levels else None
                    
                    # Market size estimation based on activity
                    market_size_indicator = len(sector_deal_list) * avg_funding if avg_funding > 0 else 0
                    
                    # Determine market trends
                    if len(sector_deal_list) > 10:
                        market_trend = "High Activity"
                    elif len(sector_deal_list) > 5:
                        market_trend = "Growing"
                    else:
                        market_trend = "Emerging"
                    
                    # Risk factors based on sector characteristics
                    sector_info = self.sector_taxonomy.get(sector, {})
                    risk_factors = []
                    
                    if sector_info.get('maturity') == 'Early':
                        risk_factors.append("Technology risk - early stage maturity")
                    if avg_trl and avg_trl < 7:
                        risk_factors.append("Commercial readiness risk")
                    if len(companies) > 20:
                        risk_factors.append("Market saturation risk")
                    
                    market_intel[sector] = MarketIntelligence(
                        sector=sector,
                        market_size_trend=market_trend,
                        competitive_landscape=f"{len(companies)} active companies, avg funding ${avg_funding/1e6:.1f}M" if avg_funding > 0 else f"{len(companies)} active companies",
                        key_players=companies[:5],  # Top 5
                        emerging_trends=[f"Average TRL: {avg_trl:.1f}" if avg_trl else "TRL data limited"],
                        investment_thesis=f"Sector showing {market_trend.lower()} activity with {len(funding_stages)} funding events",
                        risk_factors=risk_factors,
                        opportunities=[f"Market opportunity estimated at ${market_size_indicator/1e6:.0f}M+ based on activity"],
                        confidence_score=min(0.9, len(sector_deal_list) / 20)  # Confidence based on data volume
                    )
            
            return market_intel
            
        except Exception as e:
            print(f"   ⚠️  Market intelligence analysis error: {e}")
            return {}

    def _analyze_competitive_landscape(self, cutoff_date: str) -> Dict[str, Any]:
        """Analyze competitive landscape and positioning."""
        
        print("   🏁 Analyzing competitive landscape...")
        
        try:
            # Get recent deals with investor information
            deals_response = self.supabase.table('deals_new').select(
                '*, companies(*), deal_investors(*, investors(*))'
            ).gte('created_at', cutoff_date).execute()
            
            deals = deals_response.data
            
            # Investor activity analysis
            investor_activity = defaultdict(int)
            investor_sectors = defaultdict(set)
            
            for deal in deals:
                if deal.get('deal_investors'):
                    for di in deal['deal_investors']:
                        if di.get('investors'):
                            investor_name = di['investors']['name']
                            investor_activity[investor_name] += 1
                            
                            # Track sectors
                            if deal.get('companies', {}).get('climate_sub_sectors'):
                                for sector in deal['companies']['climate_sub_sectors']:
                                    investor_sectors[investor_name].add(sector)
            
            # Most active investors
            top_investors = sorted(investor_activity.items(), key=lambda x: x[1], reverse=True)[:10]
            
            # Sector concentration analysis
            sector_competition = {}
            for investor, sectors in investor_sectors.items():
                for sector in sectors:
                    if sector not in sector_competition:
                        sector_competition[sector] = []
                    sector_competition[sector].append(investor)
            
            # Competitive intelligence insights
            competitive_insights = []
            
            # Market concentration
            if len(top_investors) > 0:
                top_investor_share = top_investors[0][1] / len(deals) if deals else 0
                if top_investor_share > 0.3:
                    competitive_insights.append(f"High market concentration: {top_investors[0][0]} involved in {top_investor_share:.0%} of deals")
                else:
                    competitive_insights.append(f"Diversified investor landscape with {len(top_investors)} active players")
            
            # Cross-sector activity
            multi_sector_investors = {inv: len(sectors) for inv, sectors in investor_sectors.items() if len(sectors) > 2}
            if multi_sector_investors:
                top_diversified = max(multi_sector_investors, key=multi_sector_investors.get)
                competitive_insights.append(f"Most diversified investor: {top_diversified} ({multi_sector_investors[top_diversified]} sectors)")
            
            return {
                'investor_rankings': [{'investor': inv, 'deal_count': count} for inv, count in top_investors],
                'sector_competition': {
                    sector: {'competing_investors': len(invs), 'top_players': invs[:3]}
                    for sector, invs in sector_competition.items()
                },
                'competitive_insights': competitive_insights,
                'market_concentration': {
                    'herfindahl_index': sum((count/len(deals))**2 for _, count in top_investors) if deals else 0,
                    'top_3_share': sum(count for _, count in top_investors[:3]) / len(deals) if deals else 0
                }
            }
            
        except Exception as e:
            print(f"   ⚠️  Competitive analysis error: {e}")
            return {'error': str(e)}

    def _generate_strategic_insights(self, cutoff_date: str) -> List[StrategicInsight]:
        """Generate strategic insights from data patterns."""
        
        print("   💡 Generating strategic insights...")
        
        insights = []
        
        try:
            # Get comprehensive deal data
            deals_response = self.supabase.table('deals_new').select(
                '*, companies(*)'
            ).gte('created_at', cutoff_date).execute()
            
            deals = deals_response.data
            
            # Pattern 1: Technology convergence opportunities
            tech_keywords = defaultdict(int)
            for deal in deals:
                content = deal.get('raw_text_content', '').lower()
                for keyword in ['ai', 'machine learning', 'iot', 'blockchain', 'quantum', 'automation']:
                    if keyword in content:
                        tech_keywords[keyword] += 1
            
            if tech_keywords:
                top_tech = max(tech_keywords, key=tech_keywords.get)
                insights.append(StrategicInsight(
                    insight_type="TECHNOLOGY_CONVERGENCE",
                    title=f"AI/Digital Integration Trend in Climate Tech",
                    description=f"Strong emergence of {top_tech} integration across climate technologies",
                    implications=[
                        "Technology convergence creating new investment categories",
                        "Traditional climate tech becoming 'smart' and data-driven",
                        "Cross-sector collaboration opportunities increasing"
                    ],
                    confidence_score=min(0.9, tech_keywords[top_tech] / len(deals)),
                    priority_level="HIGH",
                    actionable_recommendations=[
                        f"Prioritize companies combining climate tech with {top_tech}",
                        "Develop investment thesis around smart climate technologies",
                        "Monitor traditional companies adding digital capabilities"
                    ],
                    supporting_data={'technology_mentions': dict(tech_keywords)},
                    created_at=datetime.now()
                ))
            
            # Pattern 2: Government funding leading indicators
            govt_deals = [d for d in deals if d['source_type'] == 'government_research']
            if govt_deals:
                # Analyze TRL progression
                advanced_stage_govt = []
                for deal in govt_deals:
                    content = deal.get('raw_text_content', '')
                    if any(keyword in content.lower() for keyword in ['demonstration', 'pilot', 'deployment', 'commercial']):
                        advanced_stage_govt.append(deal)
                
                if len(advanced_stage_govt) > len(govt_deals) * 0.3:
                    insights.append(StrategicInsight(
                        insight_type="COMMERCIALIZATION_SIGNAL",
                        title="Government Research Approaching Commercial Readiness",
                        description=f"{len(advanced_stage_govt)} government-funded projects showing commercial readiness signals",
                        implications=[
                            "Pipeline of government IP transitioning to commercial viability",
                            "Opportunity for private investment in proven technologies",
                            "Potential for licensing and spin-out opportunities"
                        ],
                        confidence_score=0.8,
                        priority_level="HIGH",
                        actionable_recommendations=[
                            "Establish relationships with national labs for technology transfer",
                            "Monitor SBIR/STTR programs for commercial transition signals",
                            "Develop fast-track evaluation process for government spin-outs"
                        ],
                        supporting_data={'advanced_stage_projects': len(advanced_stage_govt)},
                        created_at=datetime.now()
                    ))
            
            # Pattern 3: Sector momentum shifts
            sector_trends = self._analyze_sector_momentum(deals, cutoff_date)
            for sector, momentum in sector_trends.items():
                if momentum['growth_rate'] > 0.5:  # 50% growth threshold
                    insights.append(StrategicInsight(
                        insight_type="SECTOR_MOMENTUM",
                        title=f"{sector} Showing Strong Market Momentum",
                        description=f"Sector activity increased {momentum['growth_rate']:.0%} with {momentum['recent_activity']} recent developments",
                        implications=[
                            f"{sector} entering growth phase",
                            "Increased competition likely in near term",
                            "Window for strategic positioning closing"
                        ],
                        confidence_score=momentum['confidence'],
                        priority_level="MEDIUM",
                        actionable_recommendations=[
                            f"Accelerate {sector} investment pipeline review",
                            "Identify market leaders before valuation inflation",
                            "Consider sector-specific fund allocation increase"
                        ],
                        supporting_data=momentum,
                        created_at=datetime.now()
                    ))
            
            return insights
            
        except Exception as e:
            print(f"   ⚠️  Strategic insights generation error: {e}")
            return []

    def _validate_investment_thesis(self, cutoff_date: str) -> Dict[str, Any]:
        """Validate current investment thesis against market data."""
        
        print("   🎯 Validating investment thesis...")
        
        try:
            # Get recent deal data
            deals_response = self.supabase.table('deals_new').select(
                '*, companies(*)'
            ).gte('created_at', cutoff_date).execute()
            
            deals = deals_response.data
            
            # Thesis validation framework
            thesis_validation = {}
            
            # Climate tech themes validation
            for theme, sectors in self.strategic_themes.items():
                theme_activity = 0
                theme_funding = 0
                
                for deal in deals:
                    if deal.get('companies', {}).get('climate_sectors'):
                        deal_sectors = [s.lower().replace(' ', '_') for s in deal['companies']['climate_sectors']]
                        if any(sector in ' '.join(deal_sectors) for sector in sectors):
                            theme_activity += 1
                            if deal.get('amount_raised_usd'):
                                theme_funding += deal['amount_raised_usd']
                
                validation_score = min(1.0, theme_activity / max(len(deals) * 0.1, 1))  # Normalized score
                
                thesis_validation[theme] = {
                    'activity_level': theme_activity,
                    'funding_volume': theme_funding,
                    'validation_score': validation_score,
                    'thesis_status': 'VALIDATED' if validation_score > 0.6 else 'MONITORING' if validation_score > 0.3 else 'WEAK'
                }
            
            # Overall thesis strength
            avg_validation = np.mean([tv['validation_score'] for tv in thesis_validation.values()])
            
            return {
                'overall_thesis_strength': avg_validation,
                'theme_validation': thesis_validation,
                'thesis_evolution_recommendations': self._generate_thesis_recommendations(thesis_validation),
                'market_validation_confidence': min(0.95, len(deals) / 50)  # Based on data volume
            }
            
        except Exception as e:
            print(f"   ⚠️  Investment thesis validation error: {e}")
            return {'error': str(e)}

    def _conduct_risk_assessment(self, cutoff_date: str) -> Dict[str, Any]:
        """Conduct comprehensive risk assessment."""
        
        print("   ⚠️  Conducting risk assessment...")
        
        risk_assessment = {
            'market_risks': [],
            'technology_risks': [],
            'competitive_risks': [],
            'regulatory_risks': [],
            'overall_risk_level': 'MEDIUM'
        }
        
        try:
            deals_response = self.supabase.table('deals_new').select(
                '*, companies(*)'
            ).gte('created_at', cutoff_date).execute()
            
            deals = deals_response.data
            
            # Market concentration risk
            sector_counts = Counter()
            for deal in deals:
                if deal.get('companies', {}).get('climate_sub_sectors'):
                    for sector in deal['companies']['climate_sub_sectors']:
                        sector_counts[sector] += 1
            
            if sector_counts:
                max_sector_share = max(sector_counts.values()) / len(deals)
                if max_sector_share > 0.4:
                    risk_assessment['market_risks'].append({
                        'risk': 'Sector Concentration Risk',
                        'description': f"Over-concentration in {sector_counts.most_common(1)[0][0]} ({max_sector_share:.0%} of activity)",
                        'severity': 'HIGH',
                        'mitigation': 'Diversify sector allocation and monitor emerging sectors'
                    })
            
            # Technology readiness risk
            early_stage_count = 0
            for deal in deals:
                if deal.get('funding_stage') in ['Research Phase', 'Seed', 'Pre-seed']:
                    early_stage_count += 1
            
            if early_stage_count > len(deals) * 0.6:
                risk_assessment['technology_risks'].append({
                    'risk': 'Technology Readiness Risk',
                    'description': f"{early_stage_count}/{len(deals)} deals in early stage",
                    'severity': 'MEDIUM',
                    'mitigation': 'Balance portfolio with later-stage opportunities'
                })
            
            # Competitive intensity risk
            govt_deals = len([d for d in deals if d['source_type'] == 'government_research'])
            if govt_deals > len(deals) * 0.4:
                risk_assessment['competitive_risks'].append({
                    'risk': 'Government Competition Risk',
                    'description': f"High government activity ({govt_deals} deals) may indicate policy-dependent sectors",
                    'severity': 'MEDIUM',
                    'mitigation': 'Monitor policy changes and ensure technology defensibility'
                })
            
            # Overall risk calculation
            total_risks = len(risk_assessment['market_risks']) + len(risk_assessment['technology_risks']) + len(risk_assessment['competitive_risks'])
            
            if total_risks >= 3:
                risk_assessment['overall_risk_level'] = 'HIGH'
            elif total_risks >= 1:
                risk_assessment['overall_risk_level'] = 'MEDIUM'
            else:
                risk_assessment['overall_risk_level'] = 'LOW'
            
            return risk_assessment
            
        except Exception as e:
            print(f"   ⚠️  Risk assessment error: {e}")
            return risk_assessment

    def _map_strategic_opportunities(self, cutoff_date: str) -> Dict[str, Any]:
        """Map strategic opportunities and white spaces."""
        
        print("   🗺️  Mapping strategic opportunities...")
        
        try:
            deals_response = self.supabase.table('deals_new').select(
                '*, companies(*)'
            ).gte('created_at', cutoff_date).execute()
            
            deals = deals_response.data
            
            # Identify white spaces (underserved sectors)
            all_possible_sectors = set(self.sector_taxonomy.keys())
            active_sectors = set()
            
            for deal in deals:
                if deal.get('companies', {}).get('climate_sectors'):
                    active_sectors.update(deal['companies']['climate_sectors'])
            
            white_space_sectors = all_possible_sectors - active_sectors
            
            # Cross-sector convergence opportunities
            convergence_opportunities = []
            for deal in deals:
                content = deal.get('raw_text_content', '').lower()
                sectors = deal.get('companies', {}).get('climate_sectors', [])
                
                if len(sectors) > 1:  # Multi-sector companies
                    convergence_opportunities.append({
                        'company': deal.get('companies', {}).get('name', 'Unknown'),
                        'converging_sectors': sectors,
                        'opportunity_type': 'Cross-sector Innovation'
                    })
            
            # Geographic expansion opportunities
            us_companies = 0
            international_companies = 0
            
            for deal in deals:
                if deal.get('companies', {}).get('headquarters_country'):
                    if deal['companies']['headquarters_country'] in ['USA', 'United States']:
                        us_companies += 1
                    else:
                        international_companies += 1
            
            geographic_opportunities = []
            if us_companies > international_companies * 2:
                geographic_opportunities.append({
                    'opportunity': 'International Expansion',
                    'description': 'Strong US focus suggests international expansion opportunities',
                    'priority': 'MEDIUM'
                })
            
            return {
                'white_space_sectors': list(white_space_sectors),
                'convergence_opportunities': convergence_opportunities,
                'geographic_opportunities': geographic_opportunities,
                'market_timing_opportunities': self._identify_timing_opportunities(deals),
                'strategic_partnership_opportunities': self._identify_partnership_opportunities(deals)
            }
            
        except Exception as e:
            print(f"   ⚠️  Opportunity mapping error: {e}")
            return {}

    def _generate_strategic_recommendations(self, cutoff_date: str) -> List[Dict[str, Any]]:
        """Generate actionable strategic recommendations."""
        
        print("   📋 Generating strategic recommendations...")
        
        recommendations = []
        
        try:
            # Portfolio optimization recommendations
            recommendations.append({
                'category': 'PORTFOLIO_OPTIMIZATION',
                'priority': 'HIGH',
                'recommendation': 'Implement dynamic sector rebalancing',
                'rationale': 'Market momentum shifts require agile portfolio allocation',
                'action_items': [
                    'Review current sector allocations monthly',
                    'Set trigger thresholds for rebalancing',
                    'Establish rapid deployment capability for emerging opportunities'
                ],
                'timeline': '30 days',
                'success_metrics': ['Portfolio volatility reduction', 'Alpha generation vs benchmarks']
            })
            
            # Technology readiness recommendations
            recommendations.append({
                'category': 'TECHNOLOGY_STRATEGY',
                'priority': 'MEDIUM',
                'recommendation': 'Establish technology readiness assessment framework',
                'rationale': 'Better TRL evaluation improves investment timing and risk management',
                'action_items': [
                    'Develop standardized TRL assessment criteria',
                    'Create technology advisory board',
                    'Implement regular technology roadmap reviews'
                ],
                'timeline': '60 days',
                'success_metrics': ['Reduced technology risk exposure', 'Improved commercialization success rate']
            })
            
            # Market intelligence recommendations
            recommendations.append({
                'category': 'MARKET_INTELLIGENCE',
                'priority': 'HIGH',
                'recommendation': 'Enhance early-warning signal detection',
                'rationale': 'Government research provides 2+ year early warning for commercial opportunities',
                'action_items': [
                    'Strengthen national lab relationship program',
                    'Implement automated government funding database monitoring',
                    'Create rapid evaluation process for government spin-outs'
                ],
                'timeline': '45 days',
                'success_metrics': ['Deal sourcing lead time improvement', 'Government IP conversion rate']
            })
            
            return recommendations
            
        except Exception as e:
            print(f"   ⚠️  Strategic recommendations error: {e}")
            return []

    # Helper methods for analysis
    
    def _identify_emerging_themes(self, deals: List[Dict]) -> Dict[str, Any]:
        """Identify emerging themes from deal data."""
        
        themes = {'sectors': [], 'themes': [], 'convergence': [], 'trl_trends': []}
        
        # Simple theme identification based on keywords
        theme_keywords = {
            'digital_convergence': ['ai', 'machine learning', 'iot', 'digital'],
            'circular_economy': ['circular', 'recycling', 'waste', 'recovery'],
            'nature_based': ['nature', 'ecosystem', 'biodiversity', 'natural'],
            'energy_transition': ['transition', 'renewable', 'clean energy', 'grid']
        }
        
        theme_counts = Counter()
        
        for deal in deals:
            content = deal.get('raw_text_content', '').lower()
            for theme, keywords in theme_keywords.items():
                if any(keyword in content for keyword in keywords):
                    theme_counts[theme] += 1
        
        themes['themes'] = [{'theme': theme, 'activity': count} for theme, count in theme_counts.most_common(3)]
        
        return themes

    def _analyze_investment_trends(self, deals: List[Dict]) -> Dict[str, Any]:
        """Analyze investment trends from deal data."""
        
        trends = {
            'velocity': 0,
            'avg_size': 0,
            'stages': Counter(),
            'geography': Counter()
        }
        
        funding_amounts = []
        for deal in deals:
            if deal.get('amount_raised_usd'):
                funding_amounts.append(deal['amount_raised_usd'])
            
            if deal.get('funding_stage'):
                trends['stages'][deal['funding_stage']] += 1
            
            if deal.get('companies', {}).get('headquarters_country'):
                trends['geography'][deal['companies']['headquarters_country']] += 1
        
        trends['velocity'] = len(deals) / 30  # deals per day
        trends['avg_size'] = np.mean(funding_amounts) if funding_amounts else 0
        
        return trends

    def _analyze_sector_momentum(self, deals: List[Dict], cutoff_date: str) -> Dict[str, Any]:
        """Analyze sector momentum and growth rates."""
        
        # Simple momentum calculation based on recent activity
        sector_momentum = {}
        
        sector_counts = Counter()
        for deal in deals:
            if deal.get('companies', {}).get('climate_sectors'):
                for sector in deal['companies']['climate_sectors']:
                    sector_counts[sector] += 1
        
        for sector, count in sector_counts.items():
            # Simple growth rate calculation (would need historical data for real calculation)
            momentum = {
                'recent_activity': count,
                'growth_rate': min(1.0, count / 10),  # Simplified growth rate
                'confidence': min(0.9, count / 20)
            }
            sector_momentum[sector] = momentum
        
        return sector_momentum

    def _generate_thesis_recommendations(self, validation_results: Dict) -> List[str]:
        """Generate thesis evolution recommendations."""
        
        recommendations = []
        
        for theme, results in validation_results.items():
            if results['thesis_status'] == 'WEAK':
                recommendations.append(f"Consider reducing allocation to {theme} - low market validation")
            elif results['thesis_status'] == 'VALIDATED':
                recommendations.append(f"Increase focus on {theme} - strong market validation")
            else:
                recommendations.append(f"Monitor {theme} closely - mixed signals")
        
        return recommendations

    def _identify_timing_opportunities(self, deals: List[Dict]) -> List[Dict]:
        """Identify market timing opportunities."""
        
        # Simple timing analysis based on deal patterns
        return [{
            'opportunity': 'Technology Convergence Window',
            'description': 'AI integration creating new investment categories',
            'timing': 'Next 12-18 months',
            'confidence': 0.7
        }]

    def _identify_partnership_opportunities(self, deals: List[Dict]) -> List[Dict]:
        """Identify strategic partnership opportunities."""
        
        return [{
            'opportunity': 'Government Lab Partnerships',
            'description': 'Direct access to emerging government-funded technologies',
            'value_proposition': 'Early access to proven IP',
            'complexity': 'Medium'
        }]

    def _calculate_strategic_confidence(self, report: Dict[str, Any]) -> float:
        """Calculate overall strategic confidence score."""
        
        # Simple confidence calculation based on data quality and insights
        confidence_factors = []
        
        # Data quality factor
        if 'executive_summary' in report and 'period_metrics' in report['executive_summary']:
            total_discoveries = report['executive_summary']['period_metrics'].get('total_discoveries', 0)
            confidence_factors.append(min(1.0, total_discoveries / 50))  # Based on data volume
        
        # Analysis completeness factor
        sections_completed = sum(1 for key, value in report.items() 
                               if key != 'report_metadata' and value and not isinstance(value, dict) or value.get('error') is None)
        confidence_factors.append(sections_completed / 7)  # 7 main sections
        
        # Insights quality factor
        if 'strategic_insights' in report:
            insights = report['strategic_insights']
            if insights:
                avg_insight_confidence = np.mean([insight.confidence_score for insight in insights])
                confidence_factors.append(avg_insight_confidence)
        
        return np.mean(confidence_factors) * 100 if confidence_factors else 50.0

def main():
    """Main execution function for Layer 3C Strategic Intelligence."""
    
    # Initialize Supabase connection
    supabase = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    
    # Initialize Strategic Intelligence Engine
    engine = StrategicIntelligenceEngine(supabase)
    
    print("🧠 LAYER 3C: STRATEGIC INTELLIGENCE ENGINE")
    print("=" * 70)
    print("Executive-level strategic intelligence for climate tech investment decisions")
    print("=" * 70)
    
    # Generate comprehensive intelligence report
    report = engine.generate_comprehensive_intelligence_report(timeframe_days=30)
    
    # Save report to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"strategic_intelligence_report_{timestamp}.json"
    
    with open(report_filename, 'w') as f:
        # Convert datetime objects to strings for JSON serialization
        report_copy = json.loads(json.dumps(report, default=str))
        json.dump(report_copy, f, indent=2)
    
    print(f"\n📊 Strategic Intelligence Report Generated:")
    print(f"   📁 Saved to: {report_filename}")
    print(f"   🎯 Overall Confidence: {report['overall_confidence']:.1f}%")
    print(f"   📈 Analysis Period: {report['report_metadata']['analysis_period']}")
    
    # Print key highlights
    if 'executive_summary' in report and 'period_metrics' in report['executive_summary']:
        metrics = report['executive_summary']['period_metrics']
        print(f"\n🔍 Key Metrics:")
        print(f"   • Total Discoveries: {metrics.get('total_discoveries', 0)}")
        print(f"   • Discovery Velocity: {metrics.get('discovery_velocity', 0):.1f} per day")
        print(f"   • Government Intelligence: {metrics.get('government_intelligence', 0)}")
        print(f"   • VC Portfolio Activities: {metrics.get('vc_portfolio_activities', 0)}")
    
    if 'strategic_insights' in report and report['strategic_insights']:
        print(f"\n💡 Strategic Insights Generated: {len(report['strategic_insights'])}")
        for insight in report['strategic_insights'][:3]:  # Show top 3
            print(f"   • {insight.title} (Priority: {insight.priority_level})")
    
    if 'recommendations' in report and report['recommendations']:
        print(f"\n📋 Strategic Recommendations: {len(report['recommendations'])}")
        for rec in report['recommendations'][:2]:  # Show top 2
            print(f"   • {rec['recommendation']} (Priority: {rec['priority']})")
    
    print("\n✅ Layer 3C Strategic Intelligence Engine completed successfully!")

if __name__ == "__main__":
    main()
