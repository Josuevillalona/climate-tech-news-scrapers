#!/usr/bin/env python3
"""
LAYER 3C: STRATEGIC INTELLIGENCE & EXECUTIVE REPORTING
====================================================
Advanced strategic analysis, executive reporting, and investment intelligence system.
Builds on Layer 3A (Discovery Patterns) and 3B (Investment Optimization) to provide
comprehensive strategic insights and executive-level reporting capabilities.

Key Components:
- 3C.1: Strategic Insights Generator
- 3C.2: Executive Reporting System  
- 3C.3: Market Intelligence Engine
- 3C.4: Risk Assessment Framework
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import statistics
import re
from dotenv import load_dotenv
from supabase import create_client, Client

# Import Layer 3A and 3B components
from layer3_discovery_patterns import DiscoveryPatternAnalyzer
from layer3_investment_timing import InvestmentTimingPredictor
from layer3_market_trends import MarketTrendForecaster
from layer3b_investment_optimizer import InvestmentStrategyOptimizer

# Load environment
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class InsightType(Enum):
    """Types of strategic insights."""
    INVESTMENT_THESIS = "investment_thesis"
    COMPETITIVE_ANALYSIS = "competitive_analysis"
    MARKET_OPPORTUNITY = "market_opportunity"
    RISK_ASSESSMENT = "risk_assessment"
    TECHNOLOGY_TREND = "technology_trend"
    TIMING_RECOMMENDATION = "timing_recommendation"
    PORTFOLIO_OPTIMIZATION = "portfolio_optimization"
    MARKET_INTELLIGENCE = "market_intelligence"

class RiskLevel(Enum):
    """Risk assessment levels."""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class StrategicInsight:
    """Strategic insight with actionable recommendations."""
    insight_id: str
    insight_type: InsightType
    title: str
    summary: str
    detailed_analysis: str
    confidence_score: float
    risk_level: RiskLevel
    actionable_recommendations: List[str]
    supporting_data: Dict[str, Any]
    created_at: datetime
    expires_at: Optional[datetime] = None
    priority_score: float = 0.0
    tags: List[str] = None

@dataclass
class ExecutiveReport:
    """Executive-level strategic report."""
    report_id: str
    report_type: str
    title: str
    executive_summary: str
    key_insights: List[StrategicInsight]
    market_outlook: Dict[str, Any]
    investment_recommendations: List[Dict[str, Any]]
    risk_assessment: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    next_actions: List[str]
    generated_at: datetime
    report_period: str

@dataclass
class MarketIntelligence:
    """Comprehensive market intelligence."""
    sector: str
    market_size_usd: float
    growth_rate_percent: float
    key_players: List[Dict[str, Any]]
    emerging_technologies: List[str]
    investment_trends: Dict[str, Any]
    competitive_landscape: Dict[str, Any]
    opportunities: List[Dict[str, Any]]
    threats: List[Dict[str, Any]]
    intelligence_confidence: float

@dataclass
class RiskAssessment:
    """Comprehensive risk assessment."""
    assessment_id: str
    entity_type: str  # company, sector, investment
    entity_id: str
    overall_risk_score: float
    risk_factors: List[Dict[str, Any]]
    mitigation_strategies: List[str]
    probability_estimates: Dict[str, float]
    impact_analysis: Dict[str, Any]
    monitoring_recommendations: List[str]
    assessment_confidence: float

class StrategicInsightsGenerator:
    """Generate strategic insights using Layer 3A and 3B intelligence."""
    
    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.discovery_analyzer = DiscoveryPatternAnalyzer(supabase)
        self.timing_predictor = InvestmentTimingPredictor(supabase)
        self.trend_forecaster = MarketTrendForecaster(supabase)
        self.investment_optimizer = InvestmentStrategyOptimizer(supabase)
        
    def generate_investment_thesis(self, company_id: str) -> StrategicInsight:
        """Generate comprehensive investment thesis for a company."""
        
        # Get company data
        company_data = self.supabase.table('deals_new').select('*').eq('company_id', company_id).execute()
        if not company_data.data:
            raise ValueError(f"Company {company_id} not found")
        
        company = company_data.data[0]
        
        # Analyze discovery patterns
        discovery_prediction = self.discovery_analyzer.predict_commercialization_timeline(company_id)
        
        # Get investment timing
        timing_prediction = self.timing_predictor.predict_optimal_timing(company_id)
        
        # Analyze market trends for this sector
        tech_sectors = self.discovery_analyzer._extract_tech_sectors(company.get('raw_text_content', ''))
        sector_trends = []
        for sector in tech_sectors[:3]:  # Top 3 sectors
            forecast = self.trend_forecaster.forecast_sector_growth(sector, 12)
            if forecast:
                sector_trends.append({
                    'sector': sector,
                    'growth_prediction': forecast.growth_prediction,
                    'confidence': forecast.forecast_confidence  # Use correct attribute name
                })
        
        # Generate thesis
        confidence_score = self._calculate_thesis_confidence(
            discovery_prediction, timing_prediction, sector_trends
        )
        
        risk_level = self._assess_thesis_risk(company, discovery_prediction, timing_prediction)
        
        thesis_analysis = self._build_investment_thesis_analysis(
            company, discovery_prediction, timing_prediction, sector_trends
        )
        
        recommendations = self._generate_thesis_recommendations(
            company, discovery_prediction, timing_prediction, sector_trends
        )
        
        return StrategicInsight(
            insight_id=f"thesis_{company_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            insight_type=InsightType.INVESTMENT_THESIS,
            title=f"Investment Thesis: {company.get('company_name', 'Unknown Company')}",
            summary=f"Strategic investment analysis for {company.get('company_name')} in {', '.join(tech_sectors[:2])} sector(s)",
            detailed_analysis=thesis_analysis,
            confidence_score=confidence_score,
            risk_level=risk_level,
            actionable_recommendations=recommendations,
            supporting_data={
                'company_data': company,
                'discovery_prediction': discovery_prediction.__dict__ if discovery_prediction else None,
                'timing_prediction': timing_prediction.__dict__ if timing_prediction else None,
                'sector_trends': sector_trends
            },
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=30),
            priority_score=confidence_score * 100,
            tags=tech_sectors
        )
    
    def analyze_competitive_landscape(self, sector: str, timeframe_months: int = 12) -> StrategicInsight:
        """Analyze competitive landscape for a given sector."""
        
        # Get companies in this sector
        sector_companies = self._get_sector_companies(sector)
        
        # Analyze funding patterns
        funding_analysis = self._analyze_sector_funding_patterns(sector_companies)
        
        # Identify key players
        key_players = self._identify_key_players(sector_companies)
        
        # Analyze technology trends
        tech_trends = self._analyze_sector_technology_trends(sector_companies)
        
        # Generate competitive analysis
        competitive_analysis = self._build_competitive_analysis(
            sector, sector_companies, funding_analysis, key_players, tech_trends
        )
        
        confidence_score = min(len(sector_companies) / 10, 1.0)  # More companies = higher confidence
        
        risk_level = RiskLevel.MODERATE  # Default for competitive analysis
        
        recommendations = self._generate_competitive_recommendations(
            sector, funding_analysis, key_players, tech_trends
        )
        
        return StrategicInsight(
            insight_id=f"competitive_{sector}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            insight_type=InsightType.COMPETITIVE_ANALYSIS,
            title=f"Competitive Landscape Analysis: {sector.replace('_', ' ').title()}",
            summary=f"Comprehensive competitive analysis of {sector} sector with {len(sector_companies)} companies analyzed",
            detailed_analysis=competitive_analysis,
            confidence_score=confidence_score,
            risk_level=risk_level,
            actionable_recommendations=recommendations,
            supporting_data={
                'sector': sector,
                'companies_analyzed': len(sector_companies),
                'funding_analysis': funding_analysis,
                'key_players': key_players,
                'tech_trends': tech_trends
            },
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=45),
            priority_score=confidence_score * 80,
            tags=[sector, 'competitive_analysis']
        )
    
    def identify_market_opportunities(self, investment_amount: float = 5000000) -> List[StrategicInsight]:
        """Identify top market opportunities using Layer 3A and 3B intelligence."""
        
        # Get investment opportunities from Layer 3B
        opportunities = self.timing_predictor.batch_analyze_investment_opportunities()
        
        # Get sector trends
        sector_trends = self.trend_forecaster.analyze_sector_trends()
        
        # Generate portfolio optimization
        portfolio_optimization = self.investment_optimizer.optimize_portfolio(investment_amount)
        
        insights = []
        
        # Top opportunities analysis
        top_opportunities = sorted(opportunities, key=lambda x: x.opportunity_score, reverse=True)[:5]
        
        for i, opp in enumerate(top_opportunities):
            opportunity_analysis = self._build_opportunity_analysis(opp, sector_trends)
            
            recommendations = self._generate_opportunity_recommendations(opp, portfolio_optimization)
            
            # Extract sectors safely - InvestmentTiming doesn't have primary_sectors
            sectors = ['climate_tech', 'energy']  # Default sectors for testing
            
            insight = StrategicInsight(
                insight_id=f"opportunity_{i+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                insight_type=InsightType.MARKET_OPPORTUNITY,
                title=f"Market Opportunity #{i+1}: {opp.company_name}",
                summary=f"High-potential investment opportunity with {opp.opportunity_score:.1f} opportunity score",
                detailed_analysis=opportunity_analysis,
                confidence_score=opp.timing_confidence,  # Use correct attribute name
                risk_level=self._assess_opportunity_risk(opp),
                actionable_recommendations=recommendations,
                supporting_data={
                    'opportunity': opp.__dict__,
                    'sector_trends': [t.__dict__ for t in sector_trends if hasattr(t, 'sector') and t.sector in sectors],
                    'portfolio_context': portfolio_optimization.__dict__
                },
                created_at=datetime.now(),
                expires_at=datetime.now() + timedelta(days=21),
                priority_score=opp.opportunity_score,
                tags=sectors + ['market_opportunity']
            )
            
            insights.append(insight)
        
        return insights
    
    def _calculate_thesis_confidence(self, discovery_pred, timing_pred, sector_trends) -> float:
        """Calculate confidence score for investment thesis."""
        confidence_factors = []
        
        if discovery_pred:
            confidence_factors.append(discovery_pred.confidence_score)
        
        if timing_pred:
            confidence_factors.append(timing_pred.timing_confidence)  # Use correct attribute name
        
        if sector_trends:
            avg_sector_confidence = statistics.mean([t['confidence'] for t in sector_trends])
            confidence_factors.append(avg_sector_confidence)
        
        return statistics.mean(confidence_factors) if confidence_factors else 0.5
    
    def _assess_thesis_risk(self, company, discovery_pred, timing_pred) -> RiskLevel:
        """Assess risk level for investment thesis."""
        risk_score = 0
        
        # Funding stage risk
        stage = company.get('funding_stage', '').lower()
        if 'seed' in stage:
            risk_score += 3
        elif 'series a' in stage:
            risk_score += 2
        elif 'series b' in stage:
            risk_score += 1
        
        # Timing prediction risk
        if timing_pred and timing_pred.optimal_timing_weeks > 52:
            risk_score += 2
        
        # Discovery stage risk
        if discovery_pred and discovery_pred.predicted_funding_weeks > 104:
            risk_score += 2
        
        if risk_score >= 6:
            return RiskLevel.HIGH
        elif risk_score >= 4:
            return RiskLevel.MODERATE
        else:
            return RiskLevel.LOW
    
    def _build_investment_thesis_analysis(self, company, discovery_pred, timing_pred, sector_trends) -> str:
        """Build detailed investment thesis analysis."""
        
        analysis_parts = []
        
        # Company overview
        analysis_parts.append(f"**Company Analysis: {company.get('company_name', 'Unknown')}**")
        analysis_parts.append(f"Source: {company.get('source_type', 'Unknown')}")
        analysis_parts.append(f"Funding Stage: {company.get('funding_stage', 'Unknown')}")
        
        # Discovery pattern analysis
        if discovery_pred:
            analysis_parts.append(f"\n**Technology Commercialization Timeline**")
            analysis_parts.append(f"Predicted funding timeline: {discovery_pred.predicted_funding_weeks} weeks")
            analysis_parts.append(f"Commercialization confidence: {discovery_pred.confidence_score:.2f}")
            analysis_parts.append(f"Technology readiness level: {discovery_pred.technology_readiness_level}")
        
        # Investment timing analysis
        if timing_pred:
            analysis_parts.append(f"\n**Investment Timing Analysis**")
            analysis_parts.append(f"Optimal investment timing: {timing_pred.optimal_timing_weeks} weeks")
            analysis_parts.append(f"Opportunity score: {timing_pred.opportunity_score:.1f}")
            analysis_parts.append(f"Investment signals: {len(timing_pred.key_signals)} identified")
        
        # Sector trends analysis
        if sector_trends:
            analysis_parts.append(f"\n**Market Sector Analysis**")
            for trend in sector_trends:
                analysis_parts.append(f"- {trend['sector']}: {trend['growth_prediction']:.1f}% predicted growth")
        
        return "\n".join(analysis_parts)
    
    def _generate_thesis_recommendations(self, company, discovery_pred, timing_pred, sector_trends) -> List[str]:
        """Generate actionable recommendations for investment thesis."""
        
        recommendations = []
        
        # Timing recommendations
        if timing_pred:
            if timing_pred.optimal_timing_weeks <= 4:
                recommendations.append("IMMEDIATE ACTION: Optimal investment window is now open")
            elif timing_pred.optimal_timing_weeks <= 12:
                recommendations.append("NEAR-TERM: Begin due diligence process within next quarter")
            else:
                recommendations.append("MONITOR: Continue tracking for future investment consideration")
        
        # Technology recommendations
        if discovery_pred:
            if discovery_pred.technology_readiness_level >= 7:
                recommendations.append("TECHNOLOGY READY: Technology appears market-ready")
            else:
                recommendations.append("TECHNOLOGY DEVELOPMENT: Monitor technology maturation progress")
        
        # Market recommendations
        if sector_trends:
            high_growth_sectors = [t for t in sector_trends if t['growth_prediction'] > 15]
            if high_growth_sectors:
                recommendations.append(f"MARKET TAILWIND: Strong growth expected in {high_growth_sectors[0]['sector']}")
        
        # Due diligence recommendations
        recommendations.append("NEXT STEPS: Conduct technology due diligence and market validation")
        recommendations.append("RISK MITIGATION: Validate competitive positioning and IP landscape")
        
        return recommendations
    
    def _get_sector_companies(self, sector: str) -> List[Dict[str, Any]]:
        """Get companies in a specific sector."""
        
        # Search for companies with sector keywords in their content
        if not sector:
            return []
        
        sector_keywords = sector.replace('_', ' ').split()
        
        companies = []
        all_companies = self.supabase.table('deals_new').select('*').execute()
        
        for company in all_companies.data:
            content = company.get('raw_text_content', '')
            if content:  # Check content exists
                content_lower = content.lower()
                if any(keyword.lower() in content_lower for keyword in sector_keywords):
                    companies.append(company)
        
        return companies
    
    def _analyze_sector_funding_patterns(self, companies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze funding patterns for sector companies."""
        
        funding_stages = {}
        funding_amounts = []
        funding_sources = {}
        
        for company in companies:
            stage = company.get('funding_stage', 'unknown')
            funding_stages[stage] = funding_stages.get(stage, 0) + 1
            
            # Extract funding amount if available
            content = company.get('raw_text_content', '')
            amount_match = re.search(r'\$(\d+(?:\.\d+)?)\s*(million|billion|M|B)', content, re.IGNORECASE)
            if amount_match:
                amount = float(amount_match.group(1))
                if 'billion' in amount_match.group(2).lower() or 'B' in amount_match.group(2):
                    amount *= 1000
                funding_amounts.append(amount)
            
            source = company.get('source_type', 'unknown')
            funding_sources[source] = funding_sources.get(source, 0) + 1
        
        return {
            'funding_stages': funding_stages,
            'average_funding_amount': statistics.mean(funding_amounts) if funding_amounts else 0,
            'funding_sources': funding_sources,
            'total_companies': len(companies)
        }
    
    def _identify_key_players(self, companies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify key players in the sector."""
        
        # Rank companies by various factors
        scored_companies = []
        
        for company in companies:
            score = 0
            
            # Score by funding stage (later stages = higher score)
            stage = company.get('funding_stage', '').lower()
            if 'series c' in stage or 'growth' in stage:
                score += 10
            elif 'series b' in stage:
                score += 7
            elif 'series a' in stage:
                score += 5
            elif 'seed' in stage:
                score += 3
            
            # Score by source type (VC portfolio = higher score)
            if company.get('source_type') == 'vc_portfolio':
                score += 5
            
            # Score by content length (more content = more significant)
            content_length = len(company.get('raw_text_content', ''))
            score += min(content_length / 1000, 5)
            
            scored_companies.append({
                'company': company,
                'score': score
            })
        
        # Return top 5 players
        return sorted(scored_companies, key=lambda x: x['score'], reverse=True)[:5]
    
    def _analyze_sector_technology_trends(self, companies: List[Dict[str, Any]]) -> List[str]:
        """Analyze technology trends in the sector."""
        
        tech_keywords = {}
        
        for company in companies:
            content = company.get('raw_text_content', '').lower()
            
            # Common climate tech keywords
            keywords = [
                'ai', 'artificial intelligence', 'machine learning', 'ml',
                'solar', 'wind', 'battery', 'storage', 'grid',
                'carbon capture', 'hydrogen', 'electric vehicle', 'ev',
                'sustainable', 'renewable', 'clean energy',
                'automation', 'iot', 'sensors', 'data analytics',
                'blockchain', 'smart grid', 'optimization'
            ]
            
            for keyword in keywords:
                if keyword in content:
                    tech_keywords[keyword] = tech_keywords.get(keyword, 0) + 1
        
        # Return top trending technologies
        return sorted(tech_keywords.items(), key=lambda x: x[1], reverse=True)[:10]
    
    def _build_competitive_analysis(self, sector, companies, funding_analysis, key_players, tech_trends) -> str:
        """Build comprehensive competitive analysis."""
        
        analysis_parts = []
        
        analysis_parts.append(f"**Competitive Landscape: {sector.replace('_', ' ').title()}**")
        analysis_parts.append(f"Total companies analyzed: {len(companies)}")
        
        analysis_parts.append(f"\n**Funding Landscape**")
        analysis_parts.append(f"Average funding amount: ${funding_analysis['average_funding_amount']:.1f}M")
        analysis_parts.append(f"Funding stage distribution: {funding_analysis['funding_stages']}")
        
        analysis_parts.append(f"\n**Key Market Players**")
        for i, player in enumerate(key_players[:3]):
            company = player['company']
            analysis_parts.append(f"{i+1}. {company.get('company_name', 'Unknown')} (Score: {player['score']:.1f})")
        
        analysis_parts.append(f"\n**Technology Trends**")
        for tech, count in tech_trends[:5]:
            analysis_parts.append(f"- {tech}: mentioned in {count} companies")
        
        return "\n".join(analysis_parts)
    
    def _generate_competitive_recommendations(self, sector, funding_analysis, key_players, tech_trends) -> List[str]:
        """Generate competitive analysis recommendations."""
        
        recommendations = []
        
        # Market positioning recommendations
        if funding_analysis['average_funding_amount'] > 10:
            recommendations.append("HIGH CAPITAL SECTOR: Prepare for significant funding requirements")
        else:
            recommendations.append("CAPITAL EFFICIENT: Sector shows reasonable funding requirements")
        
        # Technology trend recommendations
        if tech_trends:
            top_tech = tech_trends[0][0]
            recommendations.append(f"TECHNOLOGY FOCUS: {top_tech} is the dominant technology trend")
        
        # Competition recommendations
        if len(key_players) >= 3:
            recommendations.append("COMPETITIVE MARKET: Multiple established players present")
        else:
            recommendations.append("EMERGING MARKET: Limited competition, potential for market leadership")
        
        recommendations.append("MONITORING: Track key players for partnership or acquisition opportunities")
        recommendations.append("DIFFERENTIATION: Focus on unique technology or market positioning")
        
        return recommendations
    
    def _build_opportunity_analysis(self, opportunity, sector_trends) -> str:
        """Build detailed opportunity analysis."""
        
        analysis_parts = []
        
        analysis_parts.append(f"**Investment Opportunity: {opportunity.company_name}**")
        analysis_parts.append(f"Opportunity Score: {opportunity.opportunity_score:.1f}/100")
        analysis_parts.append(f"Confidence Level: {getattr(opportunity, 'timing_confidence', 0.5):.2f}")  # Use correct attribute
        
        analysis_parts.append(f"\n**Timing Analysis**")
        analysis_parts.append(f"Optimal investment timing: {opportunity.optimal_timing_weeks} weeks")
        analysis_parts.append(f"Risk factors identified: {len(opportunity.risk_factors)}")
        
        analysis_parts.append(f"\n**Market Context**")
        # Use default sectors since InvestmentTiming doesn't have primary_sectors
        default_sectors = ['climate_tech', 'energy']
        relevant_trends = [t for t in sector_trends if hasattr(t, 'sector') and t.sector in default_sectors]
        for trend in relevant_trends[:2]:
            analysis_parts.append(f"- {trend.sector}: {trend.momentum_score:.1f} momentum score")
        
        return "\n".join(analysis_parts)
    
    def _generate_opportunity_recommendations(self, opportunity, portfolio_optimization) -> List[str]:
        """Generate opportunity-specific recommendations."""
        
        recommendations = []
        
        # Timing recommendations
        if opportunity.optimal_timing_weeks <= 2:
            recommendations.append("URGENT: Immediate action required - optimal timing window")
        elif opportunity.optimal_timing_weeks <= 8:
            recommendations.append("NEAR-TERM: Begin due diligence process within next month")
        else:
            recommendations.append("MONITOR: Track for future investment consideration")
        
        # Score-based recommendations
        if opportunity.opportunity_score >= 80:
            recommendations.append("HIGH PRIORITY: Top-tier investment opportunity")
        elif opportunity.opportunity_score >= 60:
            recommendations.append("STRONG CANDIDATE: Solid investment potential")
        else:
            recommendations.append("EVALUATE: Requires further analysis")
        
        # Portfolio context recommendations
        if portfolio_optimization.recommended_actions:
            action = portfolio_optimization.recommended_actions[0]
            recommendations.append(f"PORTFOLIO FIT: {action}")
        
        return recommendations
    
    def _assess_opportunity_risk(self, opportunity) -> RiskLevel:
        """Assess risk level for market opportunity."""
        
        risk_factors = len(opportunity.risk_factors)
        
        if risk_factors >= 5:
            return RiskLevel.HIGH
        elif risk_factors >= 3:
            return RiskLevel.MODERATE
        else:
            return RiskLevel.LOW

class ExecutiveReportingSystem:
    """Generate executive-level strategic reports."""
    
    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.insights_generator = StrategicInsightsGenerator(supabase)
        self.investment_optimizer = InvestmentStrategyOptimizer(supabase)
    
    def generate_weekly_intelligence_briefing(self) -> ExecutiveReport:
        """Generate comprehensive weekly intelligence briefing."""
        
        print("📊 Generating Weekly Intelligence Briefing...")
        
        # Generate market opportunities
        market_opportunities = self.insights_generator.identify_market_opportunities()
        
        # Analyze top sectors
        sector_insights = []
        top_sectors = ['energy_storage', 'solar_energy', 'electric_vehicles', 'carbon_capture']
        
        for sector in top_sectors:
            try:
                competitive_analysis = self.insights_generator.analyze_competitive_landscape(sector)
                sector_insights.append(competitive_analysis)
            except Exception as e:
                print(f"Warning: Could not analyze sector {sector}: {e}")
        
        # Generate investment recommendations
        portfolio_optimization = self.investment_optimizer.optimize_portfolio(10000000)  # $10M portfolio
        
        investment_recommendations = [
            {
                'type': 'portfolio_optimization',
                'recommendation': action,
                'priority': 'high'
            }
            for action in portfolio_optimization.recommended_actions[:3]
        ]
        
        # Market outlook
        market_outlook = self._generate_market_outlook()
        
        # Risk assessment
        risk_assessment = self._generate_risk_assessment(market_opportunities, sector_insights)
        
        # Performance metrics
        performance_metrics = self._calculate_performance_metrics()
        
        # Next actions
        next_actions = self._generate_next_actions(market_opportunities, investment_recommendations)
        
        # Executive summary
        executive_summary = self._generate_executive_summary(
            market_opportunities, sector_insights, investment_recommendations
        )
        
        return ExecutiveReport(
            report_id=f"weekly_briefing_{datetime.now().strftime('%Y%m%d')}",
            report_type="weekly_intelligence_briefing",
            title=f"Weekly Intelligence Briefing - {datetime.now().strftime('%B %d, %Y')}",
            executive_summary=executive_summary,
            key_insights=market_opportunities + sector_insights,
            market_outlook=market_outlook,
            investment_recommendations=investment_recommendations,
            risk_assessment=risk_assessment,
            performance_metrics=performance_metrics,
            next_actions=next_actions,
            generated_at=datetime.now(),
            report_period=f"{(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}"
        )
    
    def generate_investment_committee_report(self, investment_amount: float = 25000000) -> ExecutiveReport:
        """Generate investment committee decision support report."""
        
        print(f"📈 Generating Investment Committee Report (${investment_amount:,.0f})...")
        
        # Optimize portfolio for investment committee
        portfolio_optimization = self.investment_optimizer.optimize_portfolio(
            investment_amount, risk_profile='moderate'
        )
        
        # Generate thesis for top opportunities
        top_opportunities = self.insights_generator.identify_market_opportunities(investment_amount)
        
        # Get detailed thesis for top 3 opportunities
        detailed_insights = []
        for opp in top_opportunities[:3]:
            try:
                # Find company_id from opportunity data
                company_id = opp.supporting_data['opportunity'].company_id
                thesis = self.insights_generator.generate_investment_thesis(company_id)
                detailed_insights.append(thesis)
            except Exception as e:
                print(f"Warning: Could not generate thesis for opportunity: {e}")
        
        # Investment recommendations
        investment_recommendations = [
            {
                'type': 'direct_investment',
                'company': opp.title,
                'recommended_amount': investment_amount / len(top_opportunities),
                'confidence': opp.confidence_score,
                'timeline': f"{opp.supporting_data['opportunity'].optimal_timing_weeks} weeks",
                'priority': 'high' if opp.priority_score >= 70 else 'medium'
            }
            for opp in top_opportunities[:5]
        ]
        
        # Risk assessment for investment committee
        risk_assessment = {
            'portfolio_risk_score': portfolio_optimization.portfolio_risk_score,
            'diversification_score': portfolio_optimization.diversification_score,
            'key_risks': [
                'Technology commercialization timing uncertainty',
                'Market adoption rate variability',
                'Competitive landscape evolution',
                'Regulatory environment changes'
            ],
            'mitigation_strategies': [
                'Diversified sector allocation',
                'Staged investment approach',
                'Active portfolio monitoring',
                'Strategic partnerships'
            ]
        }
        
        executive_summary = f"""
        Investment Committee Report Summary:
        
        Portfolio Optimization Results:
        - Recommended allocation across {len(portfolio_optimization.optimized_allocation)} sectors
        - Expected portfolio return: {portfolio_optimization.expected_portfolio_return:.1f}%
        - Portfolio risk score: {portfolio_optimization.portfolio_risk_score:.2f}
        - Diversification score: {portfolio_optimization.diversification_score:.2f}
        
        Top Investment Opportunities:
        {chr(10).join([f"- {opp.title} (Score: {opp.priority_score:.1f})" for opp in top_opportunities[:3]])}
        
        Strategic Recommendation: Proceed with diversified investment approach focusing on high-confidence opportunities.
        """
        
        return ExecutiveReport(
            report_id=f"investment_committee_{datetime.now().strftime('%Y%m%d')}",
            report_type="investment_committee_report",
            title=f"Investment Committee Report - ${investment_amount:,.0f} Allocation",
            executive_summary=executive_summary,
            key_insights=top_opportunities + detailed_insights,
            market_outlook=self._generate_market_outlook(),
            investment_recommendations=investment_recommendations,
            risk_assessment=risk_assessment,
            performance_metrics={
                'total_opportunities_analyzed': len(top_opportunities),
                'high_confidence_opportunities': len([o for o in top_opportunities if o.confidence_score >= 0.7]),
                'portfolio_expected_return': portfolio_optimization.expected_portfolio_return,
                'risk_adjusted_return': portfolio_optimization.expected_portfolio_return / max(portfolio_optimization.portfolio_risk_score, 0.1)
            },
            next_actions=[
                'Review individual investment theses',
                'Conduct due diligence on top 3 opportunities',
                'Validate market timing assumptions',
                'Prepare term sheets for priority investments'
            ],
            generated_at=datetime.now(),
            report_period=f"Investment Analysis - {datetime.now().strftime('%Y-%m-%d')}"
        )
    
    def _generate_market_outlook(self) -> Dict[str, Any]:
        """Generate comprehensive market outlook."""
        
        # Get overall market data
        all_companies = self.supabase.table('deals_new').select('*').execute()
        
        total_companies = len(all_companies.data)
        
        # Analyze by source type
        source_distribution = {}
        for company in all_companies.data:
            source = company.get('source_type', 'unknown')
            source_distribution[source] = source_distribution.get(source, 0) + 1
        
        # Recent activity (last 30 days) - handle timezone comparison safely
        recent_activity = 0
        cutoff_date = datetime.now() - timedelta(days=30)
        
        for c in all_companies.data:
            if c.get('created_at'):
                try:
                    # Parse datetime and make timezone-aware comparison
                    created_at = datetime.fromisoformat(c['created_at'].replace('Z', '+00:00'))
                    if created_at.replace(tzinfo=None) > cutoff_date:
                        recent_activity += 1
                except:
                    continue  # Skip entries with parsing issues
        
        return {
            'total_market_size': total_companies,
            'source_distribution': source_distribution,
            'recent_activity_30_days': recent_activity,
            'market_momentum': 'positive' if recent_activity > total_companies * 0.1 else 'stable',
            'growth_indicators': {
                'government_research_pipeline': source_distribution.get('government_research', 0),
                'vc_portfolio_expansion': source_distribution.get('vc_portfolio', 0),
                'news_coverage_volume': source_distribution.get('news', 0)
            }
        }
    
    def _generate_risk_assessment(self, opportunities, sector_insights) -> Dict[str, Any]:
        """Generate comprehensive risk assessment."""
        
        # Calculate average risk levels
        risk_levels = [opp.risk_level.value for opp in opportunities]
        high_risk_count = len([r for r in risk_levels if r == 'high'])
        
        return {
            'overall_risk_level': 'high' if high_risk_count > len(opportunities) * 0.3 else 'moderate',
            'risk_distribution': {
                'high': len([r for r in risk_levels if r == 'high']),
                'moderate': len([r for r in risk_levels if r == 'moderate']),
                'low': len([r for r in risk_levels if r == 'low'])
            },
            'key_risk_factors': [
                'Technology commercialization uncertainty',
                'Market timing volatility',
                'Competitive dynamics',
                'Regulatory environment'
            ],
            'risk_mitigation_recommendations': [
                'Diversify across technology sectors',
                'Implement staged investment approach',
                'Monitor competitive landscape actively',
                'Maintain regulatory compliance awareness'
            ]
        }
    
    def _calculate_performance_metrics(self) -> Dict[str, Any]:
        """Calculate system performance metrics."""
        
        # Get recent system activity
        all_companies = self.supabase.table('deals_new').select('*').execute()
        
        total_discoveries = len(all_companies.data)
        
        # Calculate data quality metrics
        companies_with_content = len([
            c for c in all_companies.data 
            if c.get('raw_text_content') and len(c['raw_text_content']) > 100
        ])
        
        data_quality_score = (companies_with_content / total_discoveries) * 100 if total_discoveries > 0 else 0
        
        return {
            'total_discoveries': total_discoveries,
            'data_quality_score': data_quality_score,
            'coverage_metrics': {
                'government_research': len([c for c in all_companies.data if c.get('source_type') == 'government_research']),
                'vc_portfolios': len([c for c in all_companies.data if c.get('source_type') == 'vc_portfolio']),
                'news_sources': len([c for c in all_companies.data if c.get('source_type') == 'news'])
            },
            'system_health': 'excellent' if data_quality_score > 90 else 'good' if data_quality_score > 70 else 'needs_attention'
        }
    
    def _generate_next_actions(self, opportunities, investment_recommendations) -> List[str]:
        """Generate prioritized next actions."""
        
        actions = []
        
        # High priority opportunities
        urgent_opportunities = [o for o in opportunities if 'URGENT' in str(o.actionable_recommendations)]
        if urgent_opportunities:
            actions.append(f"IMMEDIATE: Review {len(urgent_opportunities)} urgent investment opportunities")
        
        # Investment committee actions
        high_priority_investments = [r for r in investment_recommendations if r.get('priority') == 'high']
        if high_priority_investments:
            actions.append(f"PREPARE: Investment committee materials for {len(high_priority_investments)} high-priority deals")
        
        # Routine actions
        actions.extend([
            "MONITOR: Track competitive landscape developments",
            "ANALYZE: Update market trend forecasts",
            "REVIEW: Portfolio allocation optimization",
            "PREPARE: Next week's intelligence briefing"
        ])
        
        return actions[:7]  # Top 7 actions
    
    def _generate_executive_summary(self, opportunities, sector_insights, investment_recommendations) -> str:
        """Generate executive summary for the report."""
        
        high_confidence_opps = len([o for o in opportunities if o.confidence_score >= 0.7])
        total_insights = len(opportunities) + len(sector_insights)
        
        summary = f"""
        Executive Summary - Strategic Intelligence Report
        
        Key Findings:
        - {len(opportunities)} investment opportunities identified
        - {high_confidence_opps} high-confidence opportunities (70%+ confidence)
        - {len(sector_insights)} sector competitive analyses completed
        - {len(investment_recommendations)} strategic recommendations generated
        
        Investment Landscape:
        The climate tech investment environment shows continued strong momentum with multiple high-quality 
        opportunities across key sectors. Our intelligence system has identified several time-sensitive 
        opportunities requiring immediate attention.
        
        Strategic Recommendations:
        1. Focus on high-confidence opportunities with near-term optimal timing
        2. Maintain diversified sector allocation for risk management
        3. Accelerate due diligence for top-tier opportunities
        4. Continue monitoring competitive landscape evolution
        
        Risk Assessment: Moderate
        Overall market conditions remain favorable with manageable risk levels across 
        the identified opportunity set.
        """
        
        return summary.strip()

class MarketIntelligenceEngine:
    """Comprehensive market intelligence and analysis engine."""
    
    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.insights_generator = StrategicInsightsGenerator(supabase)
        self.trend_forecaster = MarketTrendForecaster(supabase)
    
    def generate_sector_intelligence(self, sector: str) -> MarketIntelligence:
        """Generate comprehensive market intelligence for a sector."""
        
        print(f"🔍 Generating Market Intelligence: {sector}")
        
        # Get sector companies
        sector_companies = self.insights_generator._get_sector_companies(sector)
        
        # Analyze market size (simplified estimation)
        market_size = len(sector_companies) * 50  # Estimate $50M average per company
        
        # Growth rate analysis
        forecast = self.trend_forecaster.forecast_sector_growth(sector, 12)
        growth_rate = forecast.growth_prediction if forecast else 10.0
        
        # Key players analysis
        key_players_data = self.insights_generator._identify_key_players(sector_companies)
        key_players = [
            {
                'company_name': player['company'].get('company_name', 'Unknown'),
                'funding_stage': player['company'].get('funding_stage', 'Unknown'),
                'score': player['score'],
                'source_type': player['company'].get('source_type', 'Unknown')
            }
            for player in key_players_data
        ]
        
        # Technology trends
        tech_trends = self.insights_generator._analyze_sector_technology_trends(sector_companies)
        emerging_technologies = [tech for tech, count in tech_trends[:5]]
        
        # Investment trends
        funding_analysis = self.insights_generator._analyze_sector_funding_patterns(sector_companies)
        investment_trends = {
            'average_funding_size': funding_analysis['average_funding_amount'],
            'funding_stage_distribution': funding_analysis['funding_stages'],
            'funding_sources': funding_analysis['funding_sources']
        }
        
        # Competitive landscape
        competitive_landscape = {
            'total_companies': len(sector_companies),
            'market_concentration': 'fragmented' if len(sector_companies) > 20 else 'concentrated',
            'competition_intensity': 'high' if len(key_players_data) >= 5 else 'moderate'
        }
        
        # Opportunities
        opportunities = [
            {
                'type': 'market_gap',
                'description': f"Limited competition in {sector} subsectors",
                'confidence': 0.7
            },
            {
                'type': 'technology_trend',
                'description': f"Emerging trend in {emerging_technologies[0] if emerging_technologies else 'AI integration'}",
                'confidence': 0.8
            }
        ]
        
        # Threats
        threats = [
            {
                'type': 'competition',
                'description': 'Increasing competition from established players',
                'probability': 0.6
            },
            {
                'type': 'technology',
                'description': 'Rapid technology evolution risk',
                'probability': 0.5
            }
        ]
        
        return MarketIntelligence(
            sector=sector,
            market_size_usd=market_size * 1000000,  # Convert to USD
            growth_rate_percent=growth_rate,
            key_players=key_players,
            emerging_technologies=emerging_technologies,
            investment_trends=investment_trends,
            competitive_landscape=competitive_landscape,
            opportunities=opportunities,
            threats=threats,
            intelligence_confidence=0.75
        )

class RiskAssessmentFramework:
    """Advanced risk assessment and management framework."""
    
    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.insights_generator = StrategicInsightsGenerator(supabase)
    
    def assess_company_risk(self, company_id: str) -> RiskAssessment:
        """Comprehensive risk assessment for a specific company."""
        
        print(f"⚠️ Assessing Company Risk: {company_id}")
        
        # Get company data
        company_data = self.supabase.table('deals_new').select('*').eq('company_id', company_id).execute()
        if not company_data.data:
            raise ValueError(f"Company {company_id} not found")
        
        company = company_data.data[0]
        
        # Technology risk assessment
        tech_risks = self._assess_technology_risks(company)
        
        # Market risk assessment
        market_risks = self._assess_market_risks(company)
        
        # Financial risk assessment
        financial_risks = self._assess_financial_risks(company)
        
        # Operational risk assessment
        operational_risks = self._assess_operational_risks(company)
        
        # Combine all risk factors
        all_risk_factors = tech_risks + market_risks + financial_risks + operational_risks
        
        # Calculate overall risk score
        overall_risk_score = statistics.mean([rf['severity_score'] for rf in all_risk_factors])
        
        # Generate mitigation strategies
        mitigation_strategies = self._generate_mitigation_strategies(all_risk_factors)
        
        # Probability estimates
        probability_estimates = {
            'technology_failure': 0.15,
            'market_rejection': 0.25,
            'funding_difficulties': 0.20,
            'competitive_displacement': 0.30
        }
        
        # Impact analysis
        impact_analysis = {
            'financial_impact': {
                'low': 0.1,
                'medium': 0.3,
                'high': 0.6
            },
            'timeline_impact': {
                'minimal': 0.2,
                'moderate': 0.5,
                'severe': 0.3
            }
        }
        
        # Monitoring recommendations
        monitoring_recommendations = [
            'Track technology development milestones',
            'Monitor competitive landscape changes',
            'Assess market adoption metrics',
            'Review financial performance indicators'
        ]
        
        return RiskAssessment(
            assessment_id=f"risk_{company_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            entity_type='company',
            entity_id=company_id,
            overall_risk_score=overall_risk_score,
            risk_factors=all_risk_factors,
            mitigation_strategies=mitigation_strategies,
            probability_estimates=probability_estimates,
            impact_analysis=impact_analysis,
            monitoring_recommendations=monitoring_recommendations,
            assessment_confidence=0.75
        )
    
    def _assess_technology_risks(self, company: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Assess technology-related risks."""
        
        risks = []
        content = company.get('raw_text_content', '').lower()
        
        # Technology maturity risk
        if 'prototype' in content or 'early stage' in content:
            risks.append({
                'category': 'technology',
                'factor': 'technology_maturity',
                'description': 'Technology appears to be in early development stage',
                'severity_score': 0.7,
                'likelihood': 0.6
            })
        
        # IP risk
        if 'patent' not in content and 'intellectual property' not in content:
            risks.append({
                'category': 'technology',
                'factor': 'intellectual_property',
                'description': 'Limited evidence of intellectual property protection',
                'severity_score': 0.6,
                'likelihood': 0.5
            })
        
        # Technology complexity risk
        if any(keyword in content for keyword in ['ai', 'machine learning', 'quantum', 'nanotechnology']):
            risks.append({
                'category': 'technology',
                'factor': 'complexity',
                'description': 'High technology complexity may pose development challenges',
                'severity_score': 0.5,
                'likelihood': 0.4
            })
        
        return risks
    
    def _assess_market_risks(self, company: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Assess market-related risks."""
        
        risks = []
        
        # Market adoption risk
        risks.append({
            'category': 'market',
            'factor': 'adoption_rate',
            'description': 'Climate tech market adoption can be slow and uncertain',
            'severity_score': 0.6,
            'likelihood': 0.5
        })
        
        # Regulatory risk
        risks.append({
            'category': 'market',
            'factor': 'regulation',
            'description': 'Regulatory changes may impact market dynamics',
            'severity_score': 0.5,
            'likelihood': 0.6
        })
        
        # Competition risk
        risks.append({
            'category': 'market',
            'factor': 'competition',
            'description': 'Increasing competition in climate tech space',
            'severity_score': 0.7,
            'likelihood': 0.7
        })
        
        return risks
    
    def _assess_financial_risks(self, company: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Assess financial risks."""
        
        risks = []
        stage = company.get('funding_stage', '').lower()
        
        # Funding risk based on stage
        if 'seed' in stage:
            risks.append({
                'category': 'financial',
                'factor': 'funding_risk',
                'description': 'Early-stage funding risk is inherently high',
                'severity_score': 0.8,
                'likelihood': 0.6
            })
        elif 'series a' in stage:
            risks.append({
                'category': 'financial',
                'factor': 'funding_risk',
                'description': 'Series A funding carries moderate risk',
                'severity_score': 0.6,
                'likelihood': 0.4
            })
        
        # Burn rate risk
        risks.append({
            'category': 'financial',
            'factor': 'burn_rate',
            'description': 'High burn rate common in climate tech development',
            'severity_score': 0.6,
            'likelihood': 0.7
        })
        
        return risks
    
    def _assess_operational_risks(self, company: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Assess operational risks."""
        
        risks = []
        
        # Team risk
        risks.append({
            'category': 'operational',
            'factor': 'team_experience',
            'description': 'Team experience in climate tech may be limited',
            'severity_score': 0.5,
            'likelihood': 0.4
        })
        
        # Execution risk
        risks.append({
            'category': 'operational',
            'factor': 'execution',
            'description': 'Technology commercialization execution risk',
            'severity_score': 0.7,
            'likelihood': 0.5
        })
        
        return risks
    
    def _generate_mitigation_strategies(self, risk_factors: List[Dict[str, Any]]) -> List[str]:
        """Generate risk mitigation strategies."""
        
        strategies = []
        
        # Technology risks
        tech_risks = [rf for rf in risk_factors if rf['category'] == 'technology']
        if tech_risks:
            strategies.append("Conduct thorough technology due diligence and IP assessment")
            strategies.append("Implement milestone-based funding to reduce technology risk")
        
        # Market risks
        market_risks = [rf for rf in risk_factors if rf['category'] == 'market']
        if market_risks:
            strategies.append("Develop comprehensive market validation strategy")
            strategies.append("Monitor regulatory environment and policy changes")
        
        # Financial risks
        financial_risks = [rf for rf in risk_factors if rf['category'] == 'financial']
        if financial_risks:
            strategies.append("Structure investment with staged capital deployment")
            strategies.append("Establish clear financial milestones and monitoring")
        
        # Operational risks
        operational_risks = [rf for rf in risk_factors if rf['category'] == 'operational']
        if operational_risks:
            strategies.append("Assess management team experience and provide support")
            strategies.append("Implement operational oversight and guidance")
        
        # General strategies
        strategies.append("Diversify investment portfolio to spread risk")
        strategies.append("Maintain active monitoring and early warning systems")
        
        return strategies

class Layer3COrchestrator:
    """Main orchestrator for Layer 3C Strategic Intelligence system."""
    
    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.insights_generator = StrategicInsightsGenerator(self.supabase)
        self.reporting_system = ExecutiveReportingSystem(self.supabase)
        self.market_intelligence = MarketIntelligenceEngine(self.supabase)
        self.risk_framework = RiskAssessmentFramework(self.supabase)
    
    def run_comprehensive_analysis(self, investment_amount: float = 5000000) -> Dict[str, Any]:
        """Run comprehensive Layer 3C analysis."""
        
        print("🎯 LAYER 3C: STRATEGIC INTELLIGENCE & EXECUTIVE REPORTING")
        print("=" * 80)
        
        start_time = time.time()
        results = {}
        
        try:
            # 1. Generate Weekly Intelligence Briefing
            print("\n📊 Generating Weekly Intelligence Briefing...")
            weekly_briefing = self.reporting_system.generate_weekly_intelligence_briefing()
            results['weekly_briefing'] = weekly_briefing
            
            # 2. Generate Investment Committee Report
            print(f"\n📈 Generating Investment Committee Report (${investment_amount:,.0f})...")
            investment_report = self.reporting_system.generate_investment_committee_report(investment_amount)
            results['investment_committee_report'] = investment_report
            
            # 3. Generate Market Intelligence for Key Sectors
            print("\n🔍 Generating Market Intelligence...")
            key_sectors = ['energy_storage', 'solar_energy', 'electric_vehicles']
            market_intelligence = {}
            
            for sector in key_sectors:
                try:
                    intelligence = self.market_intelligence.generate_sector_intelligence(sector)
                    market_intelligence[sector] = intelligence
                except Exception as e:
                    print(f"Warning: Could not generate intelligence for {sector}: {e}")
            
            results['market_intelligence'] = market_intelligence
            
            # 4. Risk Assessment for Top Opportunities
            print("\n⚠️ Conducting Risk Assessments...")
            top_opportunities = weekly_briefing.key_insights[:3]  # Top 3 market opportunities
            risk_assessments = []
            
            for opportunity in top_opportunities:
                if opportunity.insight_type == InsightType.MARKET_OPPORTUNITY:
                    try:
                        # Extract company_id from opportunity
                        company_id = opportunity.supporting_data['opportunity'].company_id
                        risk_assessment = self.risk_framework.assess_company_risk(company_id)
                        risk_assessments.append(risk_assessment)
                    except Exception as e:
                        print(f"Warning: Could not assess risk for opportunity: {e}")
            
            results['risk_assessments'] = risk_assessments
            
            execution_time = time.time() - start_time
            
            # 5. Generate Summary Analytics
            summary_analytics = self._generate_summary_analytics(results, execution_time)
            results['summary_analytics'] = summary_analytics
            
            print(f"\n✅ Layer 3C Analysis Complete! ({execution_time:.2f} seconds)")
            return results
            
        except Exception as e:
            print(f"❌ Layer 3C Analysis Failed: {e}")
            return {'error': str(e), 'execution_time': time.time() - start_time}
    
    def _generate_summary_analytics(self, results: Dict[str, Any], execution_time: float) -> Dict[str, Any]:
        """Generate summary analytics for Layer 3C execution."""
        
        summary = {
            'execution_time_seconds': round(execution_time, 2),
            'timestamp': datetime.now().isoformat(),
            'components_executed': [],
            'insights_generated': 0,
            'reports_generated': 0,
            'risk_assessments_completed': 0,
            'market_intelligence_sectors': 0,
            'performance_rating': 'excellent'
        }
        
        # Count components executed
        if 'weekly_briefing' in results:
            summary['components_executed'].append('weekly_intelligence_briefing')
            summary['reports_generated'] += 1
            summary['insights_generated'] += len(results['weekly_briefing'].key_insights)
        
        if 'investment_committee_report' in results:
            summary['components_executed'].append('investment_committee_report')
            summary['reports_generated'] += 1
            summary['insights_generated'] += len(results['investment_committee_report'].key_insights)
        
        if 'market_intelligence' in results:
            summary['components_executed'].append('market_intelligence_engine')
            summary['market_intelligence_sectors'] = len(results['market_intelligence'])
        
        if 'risk_assessments' in results:
            summary['components_executed'].append('risk_assessment_framework')
            summary['risk_assessments_completed'] = len(results['risk_assessments'])
        
        # Performance rating
        if execution_time > 180:  # > 3 minutes
            summary['performance_rating'] = 'slow'
        elif execution_time > 120:  # > 2 minutes
            summary['performance_rating'] = 'good'
        elif len(summary['components_executed']) < 3:
            summary['performance_rating'] = 'partial'
        
        return summary

def main():
    """Run Layer 3C Strategic Intelligence system."""
    
    try:
        orchestrator = Layer3COrchestrator()
        results = orchestrator.run_comprehensive_analysis(investment_amount=10000000)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"layer3c_strategic_intelligence_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Layer 3C results saved to: {results_file}")
        
        # Print summary
        if 'summary_analytics' in results:
            summary = results['summary_analytics']
            print(f"\n🎯 LAYER 3C EXECUTION SUMMARY")
            print(f"Components Executed: {len(summary['components_executed'])}")
            print(f"Insights Generated: {summary['insights_generated']}")
            print(f"Reports Generated: {summary['reports_generated']}")
            print(f"Risk Assessments: {summary['risk_assessments_completed']}")
            print(f"Execution Time: {summary['execution_time_seconds']} seconds")
            print(f"Performance Rating: {summary['performance_rating'].upper()}")
        
    except Exception as e:
        print(f"❌ Layer 3C execution failed: {e}")

if __name__ == "__main__":
    main()
