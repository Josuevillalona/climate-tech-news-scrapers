#!/usr/bin/env python3
"""
LAYER 3: MARKET TREND FORECASTER
===============================
Predicts market trends and sector momentum using cross-source intelligence.
Provides market timing insights for optimal investment decisions.

Phase 3A.3: Market Trend Forecasting
- Sector momentum tracking
- Technology adoption curve analysis
- Government policy trend analysis
- VC flow pattern recognition
"""

import os
import re
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dotenv import load_dotenv
from supabase import create_client, Client
from dataclasses import dataclass
from collections import defaultdict, Counter
import json

# Load environment
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

@dataclass
class MarketTrend:
    """Data class for market trend analysis."""
    sector: str
    trend_direction: str  # rising, stable, declining
    momentum_score: float  # 0.0 to 1.0
    confidence: float
    timeframe_months: int
    key_drivers: List[str]
    market_signals: Dict[str, Any]

@dataclass
class SectorForecast:
    """Data class for sector forecasting."""
    sector: str
    growth_prediction: float  # % growth expected
    investment_flow_trend: str  # increasing, stable, decreasing
    adoption_stage: str  # early, growth, maturity, decline
    risk_level: str  # low, medium, high
    recommended_action: str
    forecast_confidence: float

class MarketTrendForecaster:
    """Analyzes market trends and predicts sector movements."""
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        
        # Climate tech sectors
        self.climate_sectors = {
            'energy_storage': ['battery', 'storage', 'grid', 'lithium'],
            'solar_energy': ['solar', 'photovoltaic', 'pv', 'renewable'],
            'hydrogen': ['hydrogen', 'fuel cell', 'electrolysis'],
            'carbon_capture': ['carbon capture', 'ccus', 'direct air capture', 'dac'],
            'wind_energy': ['wind', 'turbine', 'offshore wind'],
            'geothermal': ['geothermal', 'heat pump', 'thermal'],
            'electric_vehicles': ['electric vehicle', 'ev', 'battery vehicle'],
            'smart_grid': ['smart grid', 'grid management', 'demand response'],
            'biotech': ['bioengineering', 'synthetic biology', 'biofuels'],
            'quantum': ['quantum', 'quantum computing', 'quantum sensing'],
            'ai_climate': ['ai', 'machine learning', 'climate modeling'],
            'fusion': ['fusion', 'nuclear fusion', 'tokamak']
        }
        
        # Government funding patterns
        self.gov_funding_keywords = {
            'doe': ['department of energy', 'doe', 'energy.gov'],
            'darpa': ['darpa', 'defense advanced research'],
            'nsf': ['national science foundation', 'nsf'],
            'nih': ['national institutes of health', 'nih'],
            'nasa': ['nasa', 'space administration'],
            'arpa-e': ['arpa-e', 'advanced research projects agency']
        }

    def analyze_sector_trends(self) -> List[MarketTrend]:
        """Analyze trends across all climate tech sectors."""
        
        print("📈 Analyzing sector trends...")
        
        trends = []
        
        for sector, keywords in self.climate_sectors.items():
            trend = self._analyze_single_sector_trend(sector, keywords)
            if trend:
                trends.append(trend)
        
        # Sort by momentum score
        trends.sort(key=lambda x: x.momentum_score, reverse=True)
        
        return trends

    def forecast_sector_growth(self, sector: str, months_ahead: int = 12) -> Optional[SectorForecast]:
        """Forecast growth for a specific sector."""
        
        # Get sector data
        keywords = self.climate_sectors.get(sector, [])
        if not keywords:
            return None
        
        # Analyze current trend
        current_trend = self._analyze_single_sector_trend(sector, keywords)
        if not current_trend:
            return None
        
        # Analyze investment flow
        investment_flow = self._analyze_investment_flow(sector, keywords)
        
        # Analyze government support
        gov_support = self._analyze_government_support(sector, keywords)
        
        # Predict growth
        growth_prediction = self._predict_sector_growth(current_trend, investment_flow, gov_support)
        
        # Determine adoption stage
        adoption_stage = self._determine_adoption_stage(current_trend, investment_flow)
        
        # Assess risk level
        risk_level = self._assess_sector_risk(current_trend, adoption_stage)
        
        # Generate recommendation
        recommendation = self._generate_sector_recommendation(growth_prediction, risk_level, adoption_stage)
        
        return SectorForecast(
            sector=sector,
            growth_prediction=growth_prediction,
            investment_flow_trend=investment_flow['trend'],
            adoption_stage=adoption_stage,
            risk_level=risk_level,
            recommended_action=recommendation,
            forecast_confidence=current_trend.confidence
        )

    def identify_emerging_trends(self) -> List[Dict[str, Any]]:
        """Identify emerging trends not yet in major sectors."""
        
        print("🔍 Identifying emerging trends...")
        
        # Get all content and extract trending keywords
        all_data = self.supabase.table('deals_new').select('raw_text_content,source_type,created_at').limit(100).execute()
        
        # Extract trending technologies
        emerging_keywords = self._extract_trending_keywords(all_data.data)
        
        emerging_trends = []
        
        for keyword, data in emerging_keywords.items():
            if data['frequency'] >= 3 and data['growth_rate'] > 0.5:  # Filter for meaningful trends
                emerging_trends.append({
                    'keyword': keyword,
                    'frequency': data['frequency'],
                    'growth_rate': data['growth_rate'],
                    'sources': data['sources'],
                    'trend_score': data['frequency'] * data['growth_rate']
                })
        
        # Sort by trend score
        emerging_trends.sort(key=lambda x: x['trend_score'], reverse=True)
        
        return emerging_trends[:10]  # Top 10 emerging trends

    def generate_market_outlook(self, timeframe_months: int = 12) -> Dict[str, Any]:
        """Generate comprehensive market outlook."""
        
        print(f"🔮 Generating {timeframe_months}-month market outlook...")
        
        # Analyze sector trends
        sector_trends = self.analyze_sector_trends()
        
        # Generate sector forecasts
        sector_forecasts = []
        for trend in sector_trends[:8]:  # Top 8 sectors
            forecast = self.forecast_sector_growth(trend.sector, timeframe_months)
            if forecast:
                sector_forecasts.append(forecast)
        
        # Identify emerging trends
        emerging_trends = self.identify_emerging_trends()
        
        # Analyze overall market momentum
        overall_momentum = self._calculate_overall_market_momentum(sector_trends)
        
        # Generate investment recommendations
        investment_recs = self._generate_investment_recommendations(sector_forecasts)
        
        return {
            'timeframe_months': timeframe_months,
            'overall_momentum': overall_momentum,
            'sector_trends': [
                {
                    'sector': t.sector,
                    'momentum_score': t.momentum_score,
                    'trend_direction': t.trend_direction,
                    'confidence': t.confidence
                }
                for t in sector_trends
            ],
            'sector_forecasts': [
                {
                    'sector': f.sector,
                    'growth_prediction': f.growth_prediction,
                    'adoption_stage': f.adoption_stage,
                    'recommended_action': f.recommended_action,
                    'risk_level': f.risk_level
                }
                for f in sector_forecasts
            ],
            'emerging_trends': emerging_trends,
            'investment_recommendations': investment_recs,
            'outlook_confidence': np.mean([t.confidence for t in sector_trends]) if sector_trends else 0.5
        }

    # Helper methods
    
    def _analyze_single_sector_trend(self, sector: str, keywords: List[str]) -> Optional[MarketTrend]:
        """Analyze trend for a single sector."""
        
        # Build search pattern
        keyword_pattern = '|'.join(keywords)
        
        # Get sector-related data
        sector_data = []
        for keyword in keywords[:3]:  # Limit to top 3 keywords for performance
            data = self.supabase.table('deals_new').select('raw_text_content,source_type,created_at').ilike('raw_text_content', f'%{keyword}%').limit(20).execute()
            sector_data.extend(data.data)
        
        if not sector_data:
            return None
        
        # Analyze momentum
        momentum_score = self._calculate_sector_momentum(sector_data, keywords)
        
        # Determine trend direction
        trend_direction = self._determine_trend_direction(momentum_score)
        
        # Extract key drivers
        key_drivers = self._extract_key_drivers(sector_data, keywords)
        
        # Calculate confidence
        confidence = min(0.9, len(sector_data) / 20.0 + 0.3)  # More data = higher confidence
        
        return MarketTrend(
            sector=sector,
            trend_direction=trend_direction,
            momentum_score=momentum_score,
            confidence=confidence,
            timeframe_months=12,
            key_drivers=key_drivers,
            market_signals={
                'data_points': len(sector_data),
                'source_diversity': len(set(d['source_type'] for d in sector_data)),
                'recent_mentions': len([d for d in sector_data if d.get('created_at')])
            }
        )

    def _calculate_sector_momentum(self, sector_data: List[Dict], keywords: List[str]) -> float:
        """Calculate momentum score for sector."""
        
        # Count keyword matches
        total_matches = 0
        for data in sector_data:
            content = data.get('raw_text_content', '').lower()
            matches = sum(1 for keyword in keywords if keyword in content)
            total_matches += matches
        
        # Base momentum from match frequency
        momentum = min(0.7, total_matches / len(sector_data) / len(keywords))
        
        # Source diversity bonus
        source_types = set(d['source_type'] for d in sector_data)
        source_bonus = len(source_types) * 0.1  # Bonus for diverse sources
        
        # Government research bonus (early indicator)
        gov_count = sum(1 for d in sector_data if d['source_type'] == 'government_research')
        gov_bonus = min(0.2, gov_count / len(sector_data))
        
        return min(1.0, momentum + source_bonus + gov_bonus)

    def _determine_trend_direction(self, momentum_score: float) -> str:
        """Determine trend direction from momentum."""
        
        if momentum_score > 0.7:
            return 'rising'
        elif momentum_score > 0.4:
            return 'stable'
        else:
            return 'declining'

    def _extract_key_drivers(self, sector_data: List[Dict], keywords: List[str]) -> List[str]:
        """Extract key drivers for sector trend."""
        
        drivers = []
        
        # Government funding
        gov_data = [d for d in sector_data if d['source_type'] == 'government_research']
        if len(gov_data) > len(sector_data) * 0.3:
            drivers.append('Government research investment')
        
        # VC interest
        vc_data = [d for d in sector_data if d['source_type'] == 'vc_portfolio']
        if len(vc_data) > len(sector_data) * 0.2:
            drivers.append('VC portfolio inclusion')
        
        # News coverage
        news_data = [d for d in sector_data if d['source_type'] == 'news']
        if len(news_data) > len(sector_data) * 0.4:
            drivers.append('Media attention')
        
        # Technology keywords
        tech_keywords = ['breakthrough', 'innovation', 'patent', 'prototype', 'commercial']
        tech_mentions = 0
        for data in sector_data:
            content = data.get('raw_text_content', '').lower()
            tech_mentions += sum(1 for kw in tech_keywords if kw in content)
        
        if tech_mentions > len(sector_data):
            drivers.append('Technology advancement')
        
        return drivers[:3]  # Top 3 drivers

    def _analyze_investment_flow(self, sector: str, keywords: List[str]) -> Dict[str, Any]:
        """Analyze investment flow patterns for sector."""
        
        # Get VC portfolio data
        vc_data = self.supabase.table('deals_new').select('raw_text_content,created_at').eq('source_type', 'vc_portfolio').limit(50).execute()
        
        sector_vc_count = 0
        for data in vc_data.data:
            content = data.get('raw_text_content', '').lower()
            if any(keyword in content for keyword in keywords):
                sector_vc_count += 1
        
        # Simple investment flow analysis
        total_vc = len(vc_data.data)
        sector_percentage = sector_vc_count / total_vc if total_vc > 0 else 0
        
        if sector_percentage > 0.15:
            trend = 'increasing'
        elif sector_percentage > 0.05:
            trend = 'stable'
        else:
            trend = 'decreasing'
        
        return {
            'trend': trend,
            'sector_percentage': sector_percentage,
            'vc_mentions': sector_vc_count
        }

    def _analyze_government_support(self, sector: str, keywords: List[str]) -> Dict[str, Any]:
        """Analyze government support for sector."""
        
        # Get government research data
        gov_data = self.supabase.table('deals_new').select('raw_text_content').eq('source_type', 'government_research').limit(50).execute()
        
        sector_gov_count = 0
        agencies = []
        
        for data in gov_data.data:
            content = data.get('raw_text_content', '').lower()
            if any(keyword in content for keyword in keywords):
                sector_gov_count += 1
                
                # Extract agencies
                for agency, patterns in self.gov_funding_keywords.items():
                    if any(pattern in content for pattern in patterns):
                        agencies.append(agency)
        
        support_level = 'high' if sector_gov_count > 3 else 'medium' if sector_gov_count > 1 else 'low'
        
        return {
            'support_level': support_level,
            'project_count': sector_gov_count,
            'agencies': list(set(agencies))
        }

    def _predict_sector_growth(self, trend: MarketTrend, investment_flow: Dict, gov_support: Dict) -> float:
        """Predict sector growth percentage."""
        
        # Base growth from momentum
        base_growth = trend.momentum_score * 50  # 0-50% base growth
        
        # Investment flow modifier
        flow_multiplier = {
            'increasing': 1.5,
            'stable': 1.0,
            'decreasing': 0.7
        }
        
        growth_with_investment = base_growth * flow_multiplier.get(investment_flow['trend'], 1.0)
        
        # Government support modifier
        gov_multiplier = {
            'high': 1.3,
            'medium': 1.1,
            'low': 0.9
        }
        
        final_growth = growth_with_investment * gov_multiplier.get(gov_support['support_level'], 1.0)
        
        return min(100, max(5, final_growth))  # Cap between 5% and 100%

    def _determine_adoption_stage(self, trend: MarketTrend, investment_flow: Dict) -> str:
        """Determine adoption stage for sector."""
        
        # Simple adoption stage logic
        if trend.momentum_score > 0.8 and investment_flow['trend'] == 'increasing':
            return 'growth'
        elif trend.momentum_score > 0.6:
            return 'early'
        elif trend.momentum_score > 0.3:
            return 'maturity'
        else:
            return 'decline'

    def _assess_sector_risk(self, trend: MarketTrend, adoption_stage: str) -> str:
        """Assess risk level for sector."""
        
        if adoption_stage == 'early' and trend.confidence < 0.6:
            return 'high'
        elif adoption_stage in ['decline'] or trend.momentum_score < 0.3:
            return 'high'
        elif adoption_stage == 'growth' and trend.confidence > 0.7:
            return 'low'
        else:
            return 'medium'

    def _generate_sector_recommendation(self, growth_prediction: float, risk_level: str, adoption_stage: str) -> str:
        """Generate investment recommendation for sector."""
        
        if growth_prediction > 40 and risk_level == 'low':
            return 'Strong Buy - High growth, low risk'
        elif growth_prediction > 30 and risk_level in ['low', 'medium']:
            return 'Buy - Good growth potential'
        elif growth_prediction > 20:
            return 'Hold - Moderate growth expected'
        elif risk_level == 'high':
            return 'Caution - High risk sector'
        else:
            return 'Monitor - Limited growth potential'

    def _extract_trending_keywords(self, data: List[Dict]) -> Dict[str, Dict]:
        """Extract trending keywords from content."""
        
        # Simple keyword extraction (in production, use more sophisticated NLP)
        tech_patterns = [
            r'\b([A-Z][a-zA-Z]*(?:tech|Tech|technology|Technology))\b',
            r'\b([A-Z][a-zA-Z]*(?:energy|Energy))\b',
            r'\b([A-Z][a-zA-Z]*(?:bio|Bio))\b',
            r'\b([A-Z][a-zA-Z]*(?:quantum|Quantum))\b'
        ]
        
        keyword_counts = Counter()
        
        for item in data:
            content = item.get('raw_text_content', '')
            for pattern in tech_patterns:
                matches = re.findall(pattern, content)
                keyword_counts.update(matches)
        
        # Calculate growth rates (simplified)
        trending_keywords = {}
        for keyword, count in keyword_counts.most_common(20):
            if count >= 2:  # Minimum threshold
                trending_keywords[keyword] = {
                    'frequency': count,
                    'growth_rate': min(1.0, count / 10.0),  # Simplified growth rate
                    'sources': ['multiple']  # Simplified source tracking
                }
        
        return trending_keywords

    def _calculate_overall_market_momentum(self, sector_trends: List[MarketTrend]) -> Dict[str, Any]:
        """Calculate overall market momentum."""
        
        if not sector_trends:
            return {'score': 0.5, 'direction': 'stable', 'confidence': 0.3}
        
        avg_momentum = np.mean([t.momentum_score for t in sector_trends])
        rising_count = sum(1 for t in sector_trends if t.trend_direction == 'rising')
        
        direction = 'rising' if rising_count > len(sector_trends) / 2 else 'stable'
        confidence = np.mean([t.confidence for t in sector_trends])
        
        return {
            'score': avg_momentum,
            'direction': direction,
            'confidence': confidence,
            'sectors_analyzed': len(sector_trends)
        }

    def _generate_investment_recommendations(self, forecasts: List[SectorForecast]) -> List[Dict[str, Any]]:
        """Generate investment recommendations from forecasts."""
        
        recommendations = []
        
        for forecast in forecasts:
            if 'Strong Buy' in forecast.recommended_action:
                priority = 'High'
            elif 'Buy' in forecast.recommended_action:
                priority = 'Medium'
            else:
                priority = 'Low'
            
            recommendations.append({
                'sector': forecast.sector,
                'action': forecast.recommended_action,
                'priority': priority,
                'growth_potential': forecast.growth_prediction,
                'risk_level': forecast.risk_level
            })
        
        # Sort by priority and growth potential
        priority_order = {'High': 3, 'Medium': 2, 'Low': 1}
        recommendations.sort(key=lambda x: (priority_order.get(x['priority'], 0), x['growth_potential']), reverse=True)
        
        return recommendations

def main():
    """Main execution for Market Trend Forecasting."""
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        forecaster = MarketTrendForecaster(supabase)
        
        print("🔮 LAYER 3: MARKET TREND FORECASTER")
        print("=" * 60)
        
        # Generate comprehensive market outlook
        outlook = forecaster.generate_market_outlook(12)
        
        print(f"\n📊 12-Month Market Outlook")
        print("-" * 40)
        print(f"Overall Momentum: {outlook['overall_momentum']['score']:.2f} ({outlook['overall_momentum']['direction']})")
        print(f"Analysis Confidence: {outlook['outlook_confidence']:.2f}")
        print(f"Sectors Analyzed: {outlook['overall_momentum']['sectors_analyzed']}")
        
        print(f"\n🚀 Top Sector Trends:")
        print("-" * 30)
        for i, trend in enumerate(outlook['sector_trends'][:5], 1):
            print(f"#{i} {trend['sector'].replace('_', ' ').title()}")
            print(f"   Momentum: {trend['momentum_score']:.2f} ({trend['trend_direction']})")
            print(f"   Confidence: {trend['confidence']:.2f}")
        
        print(f"\n💰 Investment Recommendations:")
        print("-" * 35)
        for i, rec in enumerate(outlook['investment_recommendations'][:3], 1):
            print(f"#{i} {rec['sector'].replace('_', ' ').title()}")
            print(f"   Action: {rec['action']}")
            print(f"   Priority: {rec['priority']}")
            print(f"   Growth: {rec['growth_potential']:.1f}%")
            print(f"   Risk: {rec['risk_level']}")
            print()
        
        print(f"🔍 Emerging Trends:")
        print("-" * 20)
        for trend in outlook['emerging_trends'][:3]:
            print(f"• {trend['keyword']} (Score: {trend['trend_score']:.1f})")
        
        print("\n✅ Market Trend Forecasting Complete!")
        
    except Exception as e:
        print(f"❌ Error in market trend forecasting: {e}")

if __name__ == "__main__":
    main()
