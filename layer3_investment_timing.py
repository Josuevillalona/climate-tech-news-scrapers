#!/usr/bin/env python3
"""
LAYER 3: INVESTMENT TIMING PREDICTOR
====================================
Predicts optimal investment timing using integrated signals from government research,
VC portfolio data, and market trends.

Phase 3A.2: Investment Timing Model
- Multi-source signal integration
- Government research maturity scoring
- VC portfolio positioning analysis  
- Market readiness confidence scoring
"""

import os
import re
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dotenv import load_dotenv
from supabase import create_client, Client
from dataclasses import dataclass
from collections import defaultdict
import json
from layer3_discovery_patterns import DiscoveryPatternAnalyzer, CommercializationPrediction

# Load environment
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

@dataclass
class InvestmentSignal:
    """Data class for investment signals."""
    signal_type: str  # government_research, vc_interest, market_activity
    strength: float  # 0.0 to 1.0
    timeframe_weeks: int
    source_count: int
    confidence: float
    details: Dict[str, Any]

@dataclass
class InvestmentTiming:
    """Data class for investment timing predictions."""
    company_id: str
    company_name: str
    optimal_timing_weeks: int
    timing_confidence: float
    investment_signals: List[InvestmentSignal]
    risk_factors: List[str]
    opportunity_score: float
    recommendation: str

class InvestmentTimingPredictor:
    """Predicts optimal investment timing using multi-source signals."""
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.pattern_analyzer = DiscoveryPatternAnalyzer(supabase_client)
        
        # Investment timing windows
        self.optimal_windows = {
            'pre_seed': {'weeks_before_funding': 52, 'risk': 'high', 'return_potential': 'highest'},
            'seed_stage': {'weeks_before_funding': 26, 'risk': 'medium', 'return_potential': 'high'},
            'series_a_prep': {'weeks_before_funding': 12, 'risk': 'low', 'return_potential': 'medium'},
            'market_ready': {'weeks_before_funding': 4, 'risk': 'lowest', 'return_potential': 'lower'}
        }
        
        # Signal weights for different sources
        self.signal_weights = {
            'government_research': 0.4,  # High weight for early signals
            'vc_interest': 0.3,          # Medium weight for validation
            'market_activity': 0.2,      # Lower weight for current activity
            'news_sentiment': 0.1        # Lowest weight for publicity
        }

    def analyze_investment_signals(self, company_id: str) -> List[InvestmentSignal]:
        """Analyze all investment signals for a company."""
        
        signals = []
        
        # Government research signal
        gov_signal = self._analyze_government_signal(company_id)
        if gov_signal:
            signals.append(gov_signal)
        
        # VC portfolio interest signal
        vc_signal = self._analyze_vc_interest_signal(company_id)
        if vc_signal:
            signals.append(vc_signal)
        
        # Market activity signal
        market_signal = self._analyze_market_activity_signal(company_id)
        if market_signal:
            signals.append(market_signal)
        
        # News sentiment signal
        news_signal = self._analyze_news_sentiment_signal(company_id)
        if news_signal:
            signals.append(news_signal)
        
        return signals

    def predict_optimal_timing(self, company_id: str) -> Optional[InvestmentTiming]:
        """Predict optimal investment timing for a company."""
        
        # Get company data
        company_data = self.supabase.table('deals_new').select(
            '*,companies(name)'
        ).eq('company_id', company_id).limit(1).execute()
        
        if not company_data.data:
            return None
        
        entry = company_data.data[0]
        company_name = entry.get('companies', {}).get('name', 'Unknown')
        
        # Analyze all signals
        signals = self.analyze_investment_signals(company_id)
        
        if not signals:
            return None
        
        # Calculate optimal timing
        optimal_weeks = self._calculate_optimal_timing(signals, entry)
        timing_confidence = self._calculate_timing_confidence(signals)
        
        # Assess risk factors
        risk_factors = self._assess_risk_factors(signals, entry)
        
        # Calculate opportunity score
        opportunity_score = self._calculate_opportunity_score(signals, optimal_weeks)
        
        # Generate recommendation
        recommendation = self._generate_investment_recommendation(optimal_weeks, opportunity_score, risk_factors)
        
        return InvestmentTiming(
            company_id=company_id,
            company_name=company_name,
            optimal_timing_weeks=optimal_weeks,
            timing_confidence=timing_confidence,
            investment_signals=signals,
            risk_factors=risk_factors,
            opportunity_score=opportunity_score,
            recommendation=recommendation
        )

    def batch_analyze_investment_opportunities(self, source_types: List[str] = None) -> List[InvestmentTiming]:
        """Analyze investment timing for multiple companies."""
        
        print("🔍 Analyzing investment opportunities...")
        
        # Get companies to analyze
        query = self.supabase.table('deals_new').select('company_id,companies(name)')
        
        if source_types:
            query = query.in_('source_type', source_types)
        
        companies = query.limit(10).execute()  # Limit for initial analysis
        
        opportunities = []
        
        for company in companies.data:
            timing = self.predict_optimal_timing(company['company_id'])
            if timing and timing.opportunity_score > 0.3:  # Filter for viable opportunities
                opportunities.append(timing)
        
        # Sort by opportunity score
        opportunities.sort(key=lambda x: x.opportunity_score, reverse=True)
        
        return opportunities

    # Signal analysis methods
    
    def _analyze_government_signal(self, company_id: str) -> Optional[InvestmentSignal]:
        """Analyze government research signal strength."""
        
        # Get government research data for this company
        gov_data = self.supabase.table('deals_new').select('*').eq('company_id', company_id).eq('source_type', 'government_research').execute()
        
        if not gov_data.data:
            return None
        
        entry = gov_data.data[0]
        content = entry.get('raw_text_content', '')
        
        # Extract signal strength factors
        agencies = self.pattern_analyzer._extract_agencies(content)
        trl = self.pattern_analyzer._extract_trl(content)
        keywords = self.pattern_analyzer._extract_keywords(content)
        
        # Calculate signal strength
        strength = 0.3  # Base strength for government research
        
        if trl and trl >= 6:
            strength += 0.4  # High TRL = strong signal
        elif trl and trl >= 4:
            strength += 0.2  # Medium TRL = moderate signal
        
        strength += min(0.3, len(agencies) * 0.1)  # Multiple agencies
        strength += min(0.2, len(keywords) * 0.02)  # Technical keywords
        
        # Estimate timeframe
        prediction = self.pattern_analyzer.predict_commercialization_timeline(company_id)
        timeframe_weeks = prediction.predicted_funding_weeks if prediction else 156
        
        return InvestmentSignal(
            signal_type='government_research',
            strength=min(1.0, strength),
            timeframe_weeks=timeframe_weeks,
            source_count=len(agencies),
            confidence=prediction.confidence_score if prediction else 0.5,
            details={
                'trl': trl,
                'agencies': agencies,
                'keywords': keywords,
                'research_stage': self.pattern_analyzer._classify_research_stage(content)
            }
        )

    def _analyze_vc_interest_signal(self, company_id: str) -> Optional[InvestmentSignal]:
        """Analyze VC portfolio interest signal."""
        
        # Check if company is in any VC portfolios
        vc_data = self.supabase.table('deals_new').select('*').eq('company_id', company_id).eq('source_type', 'vc_portfolio').execute()
        
        if not vc_data.data:
            return None
        
        entry = vc_data.data[0]
        content = entry.get('raw_text_content', '')
        
        # Extract VC firms
        vc_patterns = [
            r'([A-Z][a-zA-Z\s&]+(?:Ventures|Capital|Partners|Fund|Investing))',
            r'(Breakthrough Energy[^,\.]*)'
        ]
        
        vc_firms = []
        for pattern in vc_patterns:
            matches = re.findall(pattern, content)
            vc_firms.extend(matches)
        
        # Calculate signal strength
        strength = 0.7  # Base strength for VC validation
        
        if len(vc_firms) > 1:
            strength += 0.2  # Multiple VCs = stronger signal
        
        if 'breakthrough energy' in content.lower():
            strength += 0.1  # Tier 1 VC = stronger signal
        
        return InvestmentSignal(
            signal_type='vc_interest',
            strength=min(1.0, strength),
            timeframe_weeks=52,  # VC portfolio companies typically 1 year to next funding
            source_count=len(vc_firms),
            confidence=0.8,  # High confidence for VC validation
            details={
                'vc_firms': list(set(vc_firms)),
                'portfolio_status': 'active'
            }
        )

    def _analyze_market_activity_signal(self, company_id: str) -> Optional[InvestmentSignal]:
        """Analyze market activity signal around the company's sector."""
        
        # Get company's technology sectors
        company_data = self.supabase.table('deals_new').select('*').eq('company_id', company_id).limit(1).execute()
        
        if not company_data.data:
            return None
        
        content = company_data.data[0].get('raw_text_content', '')
        tech_sectors = self.pattern_analyzer._extract_tech_sectors(content)
        
        if not tech_sectors:
            return None
        
        # Analyze market activity in these sectors (simplified for now)
        # In a full implementation, this would analyze:
        # - Recent funding rounds in the sector
        # - Market growth trends
        # - Competitor activity
        # - Technology adoption rates
        
        # For now, use basic sector activity scoring
        sector_activity = {
            'energy_storage': 0.9,  # High activity
            'solar_energy': 0.8,
            'hydrogen': 0.7,
            'carbon_capture': 0.6,
            'quantum': 0.4,  # Lower current activity
            'fusion': 0.3
        }
        
        max_activity = max([sector_activity.get(sector, 0.5) for sector in tech_sectors])
        
        return InvestmentSignal(
            signal_type='market_activity',
            strength=max_activity,
            timeframe_weeks=26,  # Market signals are shorter term
            source_count=len(tech_sectors),
            confidence=0.6,  # Medium confidence for market signals
            details={
                'sectors': tech_sectors,
                'activity_level': 'high' if max_activity > 0.7 else 'medium' if max_activity > 0.5 else 'low'
            }
        )

    def _analyze_news_sentiment_signal(self, company_id: str) -> Optional[InvestmentSignal]:
        """Analyze news sentiment signal."""
        
        # Get news data for this company
        news_data = self.supabase.table('deals_new').select('*').eq('company_id', company_id).eq('source_type', 'news').execute()
        
        if not news_data.data:
            return None
        
        # Basic sentiment analysis (simplified)
        positive_words = ['breakthrough', 'innovative', 'revolutionary', 'leading', 'advanced', 'successful']
        negative_words = ['challenge', 'problem', 'delay', 'issue', 'concern']
        
        total_positive = 0
        total_negative = 0
        
        for entry in news_data.data:
            content = entry.get('raw_text_content', '').lower()
            total_positive += sum(1 for word in positive_words if word in content)
            total_negative += sum(1 for word in negative_words if word in content)
        
        # Calculate sentiment strength
        if total_positive + total_negative == 0:
            strength = 0.5  # Neutral
        else:
            strength = total_positive / (total_positive + total_negative)
        
        return InvestmentSignal(
            signal_type='news_sentiment',
            strength=strength,
            timeframe_weeks=4,  # News signals are very short term
            source_count=len(news_data.data),
            confidence=0.4,  # Lower confidence for sentiment
            details={
                'positive_mentions': total_positive,
                'negative_mentions': total_negative,
                'sentiment': 'positive' if strength > 0.6 else 'negative' if strength < 0.4 else 'neutral'
            }
        )

    # Calculation methods
    
    def _calculate_optimal_timing(self, signals: List[InvestmentSignal], company_data: Dict) -> int:
        """Calculate optimal investment timing in weeks."""
        
        # Weight signals by their importance and strength
        weighted_timing = 0
        total_weight = 0
        
        for signal in signals:
            weight = self.signal_weights.get(signal.signal_type, 0.1) * signal.strength
            weighted_timing += signal.timeframe_weeks * weight
            total_weight += weight
        
        if total_weight == 0:
            return 52  # Default 1 year
        
        optimal_weeks = int(weighted_timing / total_weight)
        
        # Adjust based on current status
        current_stage = company_data.get('funding_stage', 'unknown')
        if current_stage and 'research' in current_stage.lower():
            optimal_weeks = max(optimal_weeks, 26)  # Don't invest too early in research
        
        return max(4, optimal_weeks)  # Minimum 1 month
    
    def _calculate_timing_confidence(self, signals: List[InvestmentSignal]) -> float:
        """Calculate confidence in timing prediction."""
        
        if not signals:
            return 0.0
        
        # Average confidence weighted by signal strength
        weighted_confidence = sum(signal.confidence * signal.strength for signal in signals)
        total_weight = sum(signal.strength for signal in signals)
        
        return weighted_confidence / total_weight if total_weight > 0 else 0.0
    
    def _assess_risk_factors(self, signals: List[InvestmentSignal], company_data: Dict) -> List[str]:
        """Assess risk factors for the investment."""
        
        risks = []
        
        # Early stage risk
        gov_signals = [s for s in signals if s.signal_type == 'government_research']
        if gov_signals:
            trl = gov_signals[0].details.get('trl', 0)
            if trl is not None and trl < 4:
                risks.append('Early-stage technology (TRL < 4)')
        
        # Market timing risk
        market_signals = [s for s in signals if s.signal_type == 'market_activity']
        if market_signals and market_signals[0].strength < 0.5:
            risks.append('Low market activity in sector')
        
        # Competition risk
        vc_signals = [s for s in signals if s.signal_type == 'vc_interest']
        if vc_signals and len(vc_signals[0].details.get('vc_firms', [])) > 2:
            risks.append('High VC interest may increase competition')
        
        # News sentiment risk
        news_signals = [s for s in signals if s.signal_type == 'news_sentiment']
        if news_signals and news_signals[0].strength < 0.4:
            risks.append('Negative news sentiment')
        
        return risks
    
    def _calculate_opportunity_score(self, signals: List[InvestmentSignal], timing_weeks: int) -> float:
        """Calculate overall opportunity score."""
        
        if not signals:
            return 0.0
        
        # Base score from signal strengths
        signal_score = sum(signal.strength * self.signal_weights.get(signal.signal_type, 0.1) for signal in signals)
        
        # Timing bonus (sooner = higher score for near-term opportunities)
        timing_bonus = max(0, (104 - timing_weeks) / 104 * 0.3)  # 2 year max timeline
        
        # Multi-source bonus
        source_types = set(signal.signal_type for signal in signals)
        multi_source_bonus = (len(source_types) - 1) * 0.1  # Bonus for multiple signal types
        
        opportunity_score = signal_score + timing_bonus + multi_source_bonus
        
        return min(1.0, opportunity_score)
    
    def _generate_investment_recommendation(self, timing_weeks: int, opportunity_score: float, risk_factors: List[str]) -> str:
        """Generate investment recommendation."""
        
        if opportunity_score > 0.8:
            if timing_weeks <= 12:
                return 'STRONG BUY - High opportunity, immediate timing'
            elif timing_weeks <= 26:
                return 'BUY - High opportunity, near-term timing'
            else:
                return 'WATCH - High opportunity, longer-term timing'
        elif opportunity_score > 0.6:
            if timing_weeks <= 26:
                return 'CONSIDER - Moderate opportunity, good timing'
            else:
                return 'WATCH - Moderate opportunity, monitor progress'
        elif opportunity_score > 0.4:
            return 'MONITOR - Limited opportunity, track developments'
        else:
            return 'PASS - Low opportunity score'

def main():
    """Main execution for Investment Timing Prediction."""
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        predictor = InvestmentTimingPredictor(supabase)
        
        print("🚀 LAYER 3: INVESTMENT TIMING PREDICTOR")
        print("=" * 60)
        
        # Analyze investment opportunities
        opportunities = predictor.batch_analyze_investment_opportunities()
        
        print(f"\n💰 Top Investment Opportunities:")
        print("-" * 50)
        
        for i, opportunity in enumerate(opportunities[:5], 1):
            print(f"#{i} {opportunity.company_name}")
            print(f"   Opportunity Score: {opportunity.opportunity_score:.2f}")
            print(f"   Optimal Timing: {opportunity.optimal_timing_weeks} weeks")
            print(f"   Confidence: {opportunity.timing_confidence:.2f}")
            print(f"   Recommendation: {opportunity.recommendation}")
            print(f"   Signals: {len(opportunity.investment_signals)}")
            if opportunity.risk_factors:
                print(f"   Risks: {', '.join(opportunity.risk_factors[:2])}")
            print()
        
        print("✅ Investment Timing Analysis Complete!")
        
    except Exception as e:
        print(f"❌ Error in investment timing analysis: {e}")

if __name__ == "__main__":
    main()
