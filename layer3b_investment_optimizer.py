#!/usr/bin/env python3
"""
LAYER 3B: MARKET PREDICTION ENGINE
==================================
Advanced predictive analytics building on Layer 3A intelligence.
Provides sophisticated market predictions and investment strategy optimization.

Phase 3B.1: Investment Strategy Optimizer
- Portfolio optimization algorithms
- Risk-adjusted return predictions
- Diversification recommendations
- Capital allocation strategies
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

# Import Layer 3A components
from layer3_discovery_patterns import DiscoveryPatternAnalyzer, CommercializationPrediction
from layer3_investment_timing import InvestmentTimingPredictor, InvestmentTiming
from layer3_market_trends import MarketTrendForecaster, MarketTrend, SectorForecast

# Load environment
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

@dataclass
class InvestmentStrategy:
    """Data class for investment strategy recommendations."""
    strategy_name: str
    risk_profile: str  # conservative, moderate, aggressive
    expected_return: float  # %
    risk_score: float  # 0.0 to 1.0
    recommended_allocation: Dict[str, float]  # sector -> percentage
    investment_timeline: int  # months
    confidence_score: float
    key_opportunities: List[str]

@dataclass
class PortfolioOptimization:
    """Data class for portfolio optimization results."""
    portfolio_id: str
    total_capital: float
    optimized_allocation: Dict[str, Dict[str, Any]]  # sector -> {companies, allocation, rationale}
    expected_portfolio_return: float
    portfolio_risk_score: float
    diversification_score: float
    recommended_actions: List[str]
    rebalancing_suggestions: List[Dict[str, Any]]

@dataclass
class MarketPrediction:
    """Data class for advanced market predictions."""
    prediction_type: str  # sector_growth, technology_adoption, funding_cycle
    timeframe_months: int
    prediction_value: float
    confidence_interval: Tuple[float, float]  # (lower, upper)
    key_drivers: List[str]
    risk_factors: List[str]
    supporting_evidence: Dict[str, Any]

class InvestmentStrategyOptimizer:
    """Advanced investment strategy optimization engine."""
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        
        # Import Layer 3A components
        self.discovery_analyzer = DiscoveryPatternAnalyzer(supabase_client)
        self.timing_predictor = InvestmentTimingPredictor(supabase_client)
        self.trend_forecaster = MarketTrendForecaster(supabase_client)
        
        # Investment strategy profiles
        self.strategy_profiles = {
            'conservative': {
                'risk_tolerance': 0.3,
                'return_target': 15,  # 15% annual return
                'sector_concentration_limit': 0.4,  # Max 40% in any sector
                'early_stage_limit': 0.2,  # Max 20% in early-stage
                'timeline_preference': 'medium_term'  # 2-5 years
            },
            'moderate': {
                'risk_tolerance': 0.5,
                'return_target': 25,  # 25% annual return
                'sector_concentration_limit': 0.5,
                'early_stage_limit': 0.4,
                'timeline_preference': 'mixed'
            },
            'aggressive': {
                'risk_tolerance': 0.8,
                'return_target': 40,  # 40% annual return
                'sector_concentration_limit': 0.7,
                'early_stage_limit': 0.6,
                'timeline_preference': 'long_term'  # 5+ years
            }
        }

    def generate_investment_strategies(self, capital_amount: float = 1000000) -> List[InvestmentStrategy]:
        """Generate optimized investment strategies for different risk profiles."""
        
        print("🎯 Generating Investment Strategies...")
        
        # Get Layer 3A intelligence
        market_outlook = self.trend_forecaster.generate_market_outlook(12)
        investment_opportunities = self.timing_predictor.batch_analyze_investment_opportunities()
        
        strategies = []
        
        for profile_name, profile in self.strategy_profiles.items():
            strategy = self._create_strategy_for_profile(
                profile_name, profile, market_outlook, investment_opportunities, capital_amount
            )
            strategies.append(strategy)
        
        return strategies

    def optimize_portfolio(self, capital_amount: float, risk_profile: str = 'moderate') -> PortfolioOptimization:
        """Optimize portfolio allocation using Layer 3A intelligence."""
        
        print(f"📊 Optimizing Portfolio (${capital_amount:,.0f}, {risk_profile} risk)...")
        
        # Get investment opportunities
        opportunities = self.timing_predictor.batch_analyze_investment_opportunities()
        
        # Get sector trends
        sector_trends = self.trend_forecaster.analyze_sector_trends()
        
        # Filter opportunities by risk profile
        profile = self.strategy_profiles[risk_profile]
        filtered_opportunities = self._filter_opportunities_by_risk(opportunities, profile)
        
        # Optimize allocation
        optimized_allocation = self._optimize_sector_allocation(
            filtered_opportunities, sector_trends, capital_amount, profile
        )
        
        # Calculate portfolio metrics
        portfolio_return = self._calculate_portfolio_return(optimized_allocation, sector_trends)
        portfolio_risk = self._calculate_portfolio_risk(optimized_allocation, sector_trends)
        diversification_score = self._calculate_diversification_score(optimized_allocation)
        
        # Generate recommendations
        recommended_actions = self._generate_portfolio_recommendations(
            optimized_allocation, sector_trends, profile
        )
        
        return PortfolioOptimization(
            portfolio_id=f"climate_tech_{risk_profile}_{datetime.now().strftime('%Y%m%d')}",
            total_capital=capital_amount,
            optimized_allocation=optimized_allocation,
            expected_portfolio_return=portfolio_return,
            portfolio_risk_score=portfolio_risk,
            diversification_score=diversification_score,
            recommended_actions=recommended_actions,
            rebalancing_suggestions=[]
        )

    def predict_market_movements(self, timeframe_months: int = 12) -> List[MarketPrediction]:
        """Generate advanced market movement predictions."""
        
        print(f"🔮 Predicting Market Movements ({timeframe_months} months)...")
        
        predictions = []
        
        # Sector growth predictions
        sector_predictions = self._predict_sector_growth_patterns(timeframe_months)
        predictions.extend(sector_predictions)
        
        # Technology adoption predictions
        adoption_predictions = self._predict_technology_adoption(timeframe_months)
        predictions.extend(adoption_predictions)
        
        # Funding cycle predictions
        funding_predictions = self._predict_funding_cycles(timeframe_months)
        predictions.extend(funding_predictions)
        
        return predictions

    def generate_strategic_recommendations(self, capital_amount: float) -> Dict[str, Any]:
        """Generate comprehensive strategic investment recommendations."""
        
        print("🚀 Generating Strategic Recommendations...")
        
        # Generate strategies for all risk profiles
        strategies = self.generate_investment_strategies(capital_amount)
        
        # Optimize portfolios
        portfolios = {}
        for risk_profile in ['conservative', 'moderate', 'aggressive']:
            portfolios[risk_profile] = self.optimize_portfolio(capital_amount, risk_profile)
        
        # Generate market predictions
        predictions = self.predict_market_movements(12)
        
        # Identify top opportunities
        top_opportunities = self._identify_top_opportunities()
        
        # Generate strategic insights
        strategic_insights = self._generate_strategic_insights(strategies, portfolios, predictions)
        
        return {
            'capital_amount': capital_amount,
            'investment_strategies': [s.__dict__ for s in strategies],
            'optimized_portfolios': {k: v.__dict__ for k, v in portfolios.items()},
            'market_predictions': [p.__dict__ for p in predictions],
            'top_opportunities': top_opportunities,
            'strategic_insights': strategic_insights,
            'generated_at': datetime.now().isoformat()
        }

    # Strategy creation methods
    
    def _create_strategy_for_profile(self, profile_name: str, profile: Dict, market_outlook: Dict, 
                                   opportunities: List[InvestmentTiming], capital_amount: float) -> InvestmentStrategy:
        """Create investment strategy for specific risk profile."""
        
        # Filter opportunities by risk tolerance
        suitable_opportunities = []
        for opp in opportunities:
            risk_score = len(opp.risk_factors) / 5.0  # Normalize risk score
            if risk_score <= profile['risk_tolerance']:
                suitable_opportunities.append(opp)
        
        # Calculate sector allocation based on trends and risk profile
        sector_allocation = self._calculate_sector_allocation(market_outlook, profile)
        
        # Calculate expected return
        expected_return = self._calculate_expected_return(sector_allocation, market_outlook, profile)
        
        # Identify key opportunities
        key_opportunities = [
            opp.company_name for opp in suitable_opportunities[:5]
        ]
        
        return InvestmentStrategy(
            strategy_name=f"Climate Tech {profile_name.title()} Strategy",
            risk_profile=profile_name,
            expected_return=expected_return,
            risk_score=profile['risk_tolerance'],
            recommended_allocation=sector_allocation,
            investment_timeline=24 if profile['timeline_preference'] == 'medium_term' else 36,
            confidence_score=market_outlook['outlook_confidence'],
            key_opportunities=key_opportunities
        )

    def _calculate_sector_allocation(self, market_outlook: Dict, profile: Dict) -> Dict[str, float]:
        """Calculate optimal sector allocation for risk profile."""
        
        sector_trends = market_outlook.get('sector_trends', [])
        allocation = {}
        
        # Start with base allocation
        total_weight = 0
        for trend in sector_trends:
            # Weight by momentum and risk tolerance
            weight = trend['momentum_score'] * (1 + profile['risk_tolerance'])
            allocation[trend['sector']] = weight
            total_weight += weight
        
        # Normalize to percentages
        if total_weight > 0:
            for sector in allocation:
                allocation[sector] = (allocation[sector] / total_weight) * 100
        
        # Apply concentration limits
        max_allocation = profile['sector_concentration_limit'] * 100
        
        # Cap allocations and redistribute excess
        excess = 0
        for sector in allocation:
            if allocation[sector] > max_allocation:
                excess += allocation[sector] - max_allocation
                allocation[sector] = max_allocation
        
        # Redistribute excess proportionally
        if excess > 0:
            under_limit_sectors = [s for s in allocation if allocation[s] < max_allocation]
            if under_limit_sectors:
                excess_per_sector = excess / len(under_limit_sectors)
                for sector in under_limit_sectors:
                    allocation[sector] += excess_per_sector
        
        return allocation

    def _calculate_expected_return(self, sector_allocation: Dict[str, float], 
                                 market_outlook: Dict, profile: Dict) -> float:
        """Calculate expected portfolio return."""
        
        base_return = profile['return_target']
        
        # Adjust based on market momentum
        market_momentum = market_outlook.get('overall_momentum', {}).get('score', 0.5)
        momentum_adjustment = (market_momentum - 0.5) * 20  # ±10% adjustment
        
        # Adjust based on sector allocation
        sector_forecasts = market_outlook.get('sector_forecasts', [])
        weighted_sector_return = 0
        total_allocation = sum(sector_allocation.values())
        
        for forecast in sector_forecasts:
            sector = forecast['sector']
            if sector in sector_allocation and total_allocation > 0:
                weight = sector_allocation[sector] / total_allocation
                weighted_sector_return += forecast['growth_prediction'] * weight
        
        # Combine base return with market and sector adjustments
        expected_return = base_return + momentum_adjustment + (weighted_sector_return * 0.3)
        
        return max(5, min(60, expected_return))  # Cap between 5% and 60%

    # Portfolio optimization methods
    
    def _filter_opportunities_by_risk(self, opportunities: List[InvestmentTiming], 
                                    profile: Dict) -> List[InvestmentTiming]:
        """Filter opportunities by risk tolerance."""
        
        filtered = []
        for opp in opportunities:
            risk_score = len(opp.risk_factors) / 5.0  # Normalize
            if risk_score <= profile['risk_tolerance']:
                filtered.append(opp)
        
        return filtered

    def _optimize_sector_allocation(self, opportunities: List[InvestmentTiming], 
                                  sector_trends: List[MarketTrend], capital_amount: float,
                                  profile: Dict) -> Dict[str, Dict[str, Any]]:
        """Optimize allocation across sectors and companies."""
        
        allocation = {}
        
        # Group opportunities by sector
        sector_opportunities = defaultdict(list)
        for opp in opportunities:
            # Extract sector from company analysis (simplified)
            company_data = self.supabase.table('deals_new').select('raw_text_content').eq('company_id', opp.company_id).limit(1).execute()
            if company_data.data:
                content = company_data.data[0]['raw_text_content']
                sectors = self.discovery_analyzer._extract_tech_sectors(content)
                if sectors:
                    sector_opportunities[sectors[0]].append(opp)
        
        # Calculate allocation for each sector
        for sector_trend in sector_trends[:8]:  # Top 8 sectors
            sector = sector_trend.sector
            if sector in sector_opportunities:
                sector_opps = sector_opportunities[sector]
                
                # Calculate sector allocation
                sector_weight = sector_trend.momentum_score * (1 + profile['risk_tolerance'])
                sector_allocation = min(profile['sector_concentration_limit'], sector_weight * 0.3)
                sector_capital = capital_amount * sector_allocation
                
                # Select top companies in sector
                sector_opps.sort(key=lambda x: x.opportunity_score, reverse=True)
                top_companies = sector_opps[:3]  # Top 3 per sector
                
                if top_companies:
                    company_allocation = sector_capital / len(top_companies)
                    
                    allocation[sector] = {
                        'total_allocation': sector_capital,
                        'allocation_percentage': sector_allocation * 100,
                        'companies': [
                            {
                                'name': comp.company_name,
                                'allocation': company_allocation,
                                'opportunity_score': comp.opportunity_score,
                                'timing_weeks': comp.optimal_timing_weeks,
                                'rationale': comp.recommendation
                            }
                            for comp in top_companies
                        ],
                        'sector_momentum': sector_trend.momentum_score,
                        'rationale': f"High momentum ({sector_trend.momentum_score:.2f}) with {len(top_companies)} strong opportunities"
                    }
        
        return allocation

    def _calculate_portfolio_return(self, allocation: Dict[str, Dict[str, Any]], 
                                  sector_trends: List[MarketTrend]) -> float:
        """Calculate expected portfolio return."""
        
        weighted_return = 0
        total_allocation = sum(sector['allocation_percentage'] for sector in allocation.values())
        
        # Map sector trends for quick lookup
        trend_map = {trend.sector: trend for trend in sector_trends}
        
        for sector, data in allocation.items():
            if sector in trend_map:
                # Base sector return from momentum
                sector_return = trend_map[sector].momentum_score * 30  # Scale to percentage
                
                # Weight by allocation
                weight = data['allocation_percentage'] / total_allocation if total_allocation > 0 else 0
                weighted_return += sector_return * weight
        
        return weighted_return

    def _calculate_portfolio_risk(self, allocation: Dict[str, Dict[str, Any]], 
                                sector_trends: List[MarketTrend]) -> float:
        """Calculate portfolio risk score."""
        
        total_risk = 0
        total_weight = 0
        
        for sector, data in allocation.items():
            # Risk based on sector concentration and company risk
            concentration_risk = data['allocation_percentage'] / 100
            
            # Company risk (average of risk factors)
            company_risks = []
            for company in data['companies']:
                # Simplified risk calculation
                timing_risk = min(1.0, company['timing_weeks'] / 104)  # 2-year max
                opportunity_risk = 1 - company['opportunity_score']
                company_risks.append((timing_risk + opportunity_risk) / 2)
            
            avg_company_risk = np.mean(company_risks) if company_risks else 0.5
            sector_risk = (concentration_risk + avg_company_risk) / 2
            
            weight = data['allocation_percentage']
            total_risk += sector_risk * weight
            total_weight += weight
        
        return total_risk / total_weight if total_weight > 0 else 0.5

    def _calculate_diversification_score(self, allocation: Dict[str, Dict[str, Any]]) -> float:
        """Calculate portfolio diversification score."""
        
        if not allocation:
            return 0.0
        
        # Calculate Herfindahl-Hirschman Index (HHI) for concentration
        allocations = [data['allocation_percentage'] / 100 for data in allocation.values()]
        hhi = sum(alloc ** 2 for alloc in allocations)
        
        # Convert to diversification score (1 - HHI, scaled)
        diversification = (1 - hhi) * (len(allocation) / 10)  # Bonus for more sectors
        
        return min(1.0, diversification)

    def _generate_portfolio_recommendations(self, allocation: Dict[str, Dict[str, Any]], 
                                          sector_trends: List[MarketTrend], 
                                          profile: Dict) -> List[str]:
        """Generate portfolio recommendations."""
        
        recommendations = []
        
        # Check sector concentration
        max_allocation = max((data['allocation_percentage'] for data in allocation.values()), default=0)
        if max_allocation > profile['sector_concentration_limit'] * 100:
            recommendations.append(f"Consider reducing concentration in top sector (currently {max_allocation:.1f}%)")
        
        # Check diversification
        if len(allocation) < 3:
            recommendations.append("Consider diversifying across more sectors for risk reduction")
        
        # Check timing alignment
        quick_opportunities = sum(1 for data in allocation.values() 
                                for company in data['companies'] 
                                if company['timing_weeks'] < 26)
        
        if quick_opportunities > len(allocation) * 2:
            recommendations.append("Portfolio heavy on short-term opportunities - consider longer-term balance")
        
        # Sector-specific recommendations
        trend_map = {trend.sector: trend for trend in sector_trends}
        for sector, data in allocation.items():
            if sector in trend_map and trend_map[sector].trend_direction == 'declining':
                recommendations.append(f"Monitor {sector} closely - showing declining trend")
        
        return recommendations

    # Market prediction methods
    
    def _predict_sector_growth_patterns(self, timeframe_months: int) -> List[MarketPrediction]:
        """Predict sector growth patterns."""
        
        predictions = []
        sector_trends = self.trend_forecaster.analyze_sector_trends()
        
        for trend in sector_trends[:5]:  # Top 5 sectors
            # Base prediction from momentum
            base_growth = trend.momentum_score * 50  # Scale to percentage
            
            # Add confidence interval
            confidence_range = (1 - trend.confidence) * 20  # ±range based on confidence
            lower_bound = max(0, base_growth - confidence_range)
            upper_bound = base_growth + confidence_range
            
            predictions.append(MarketPrediction(
                prediction_type='sector_growth',
                timeframe_months=timeframe_months,
                prediction_value=base_growth,
                confidence_interval=(lower_bound, upper_bound),
                key_drivers=trend.key_drivers,
                risk_factors=[f"Low confidence ({trend.confidence:.2f})" if trend.confidence < 0.7 else "Market volatility"],
                supporting_evidence={
                    'momentum_score': trend.momentum_score,
                    'trend_direction': trend.trend_direction,
                    'data_points': trend.market_signals.get('data_points', 0)
                }
            ))
        
        return predictions

    def _predict_technology_adoption(self, timeframe_months: int) -> List[MarketPrediction]:
        """Predict technology adoption rates."""
        
        predictions = []
        
        # Simplified adoption prediction based on government research patterns
        gov_data = self.supabase.table('deals_new').select('raw_text_content').eq('source_type', 'government_research').limit(20).execute()
        
        # Extract technology readiness levels
        trl_counts = defaultdict(int)
        for item in gov_data.data:
            content = item['raw_text_content']
            trl = self.discovery_analyzer._extract_trl(content)
            if trl:
                trl_counts[trl] += 1
        
        # Predict adoption based on TRL distribution
        total_projects = sum(trl_counts.values())
        if total_projects > 0:
            high_trl_percentage = sum(trl_counts[trl] for trl in range(7, 10)) / total_projects * 100
            
            predictions.append(MarketPrediction(
                prediction_type='technology_adoption',
                timeframe_months=timeframe_months,
                prediction_value=high_trl_percentage,
                confidence_interval=(high_trl_percentage * 0.8, high_trl_percentage * 1.2),
                key_drivers=['Government research investment', 'Technology maturity progression'],
                risk_factors=['Regulatory delays', 'Market acceptance'],
                supporting_evidence={
                    'total_projects': total_projects,
                    'trl_distribution': dict(trl_counts),
                    'high_trl_count': sum(trl_counts[trl] for trl in range(7, 10))
                }
            ))
        
        return predictions

    def _predict_funding_cycles(self, timeframe_months: int) -> List[MarketPrediction]:
        """Predict funding cycle patterns."""
        
        predictions = []
        
        # Analyze VC portfolio data for funding patterns
        vc_data = self.supabase.table('deals_new').select('raw_text_content,created_at').eq('source_type', 'vc_portfolio').limit(50).execute()
        
        if vc_data.data:
            # Simple funding cycle prediction
            recent_activity = len([item for item in vc_data.data if item.get('created_at')])
            activity_score = min(1.0, recent_activity / 25)  # Normalize
            
            predicted_funding_increase = activity_score * 30  # Scale to percentage
            
            predictions.append(MarketPrediction(
                prediction_type='funding_cycle',
                timeframe_months=timeframe_months,
                prediction_value=predicted_funding_increase,
                confidence_interval=(predicted_funding_increase * 0.7, predicted_funding_increase * 1.3),
                key_drivers=['VC portfolio activity', 'Market momentum'],
                risk_factors=['Economic conditions', 'Regulatory changes'],
                supporting_evidence={
                    'vc_activity_count': recent_activity,
                    'activity_score': activity_score,
                    'data_sources': len(vc_data.data)
                }
            ))
        
        return predictions

    def _identify_top_opportunities(self) -> List[Dict[str, Any]]:
        """Identify top investment opportunities across all analyses."""
        
        opportunities = self.timing_predictor.batch_analyze_investment_opportunities()
        
        # Rank by opportunity score and timing
        top_opportunities = []
        for opp in opportunities[:5]:
            top_opportunities.append({
                'company_name': opp.company_name,
                'opportunity_score': opp.opportunity_score,
                'optimal_timing_weeks': opp.optimal_timing_weeks,
                'recommendation': opp.recommendation,
                'risk_factors': opp.risk_factors,
                'confidence': opp.timing_confidence
            })
        
        return top_opportunities

    def _generate_strategic_insights(self, strategies: List[InvestmentStrategy], 
                                   portfolios: Dict[str, PortfolioOptimization],
                                   predictions: List[MarketPrediction]) -> List[str]:
        """Generate high-level strategic insights."""
        
        insights = []
        
        # Strategy insights
        best_strategy = max(strategies, key=lambda s: s.expected_return)
        insights.append(f"Highest return potential: {best_strategy.strategy_name} ({best_strategy.expected_return:.1f}% expected return)")
        
        # Portfolio insights
        best_portfolio = max(portfolios.values(), key=lambda p: p.expected_portfolio_return)
        insights.append(f"Best risk-adjusted portfolio: {best_portfolio.portfolio_id} ({best_portfolio.expected_portfolio_return:.1f}% return, {best_portfolio.portfolio_risk_score:.2f} risk)")
        
        # Market insights
        growth_predictions = [p for p in predictions if p.prediction_type == 'sector_growth']
        if growth_predictions:
            top_growth = max(growth_predictions, key=lambda p: p.prediction_value)
            insights.append(f"Highest growth sector predicted: {top_growth.prediction_value:.1f}% growth potential")
        
        # Risk insights
        high_risk_sectors = sum(1 for p in portfolios.values() if p.portfolio_risk_score > 0.7)
        if high_risk_sectors > 0:
            insights.append(f"Monitor risk levels: {high_risk_sectors} portfolios show elevated risk")
        
        # Diversification insights
        avg_diversification = np.mean([p.diversification_score for p in portfolios.values()])
        if avg_diversification < 0.6:
            insights.append("Consider increasing diversification across portfolios")
        
        return insights

def main():
    """Main execution for Investment Strategy Optimizer."""
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        optimizer = InvestmentStrategyOptimizer(supabase)
        
        print("🚀 LAYER 3B: INVESTMENT STRATEGY OPTIMIZER")
        print("=" * 60)
        
        # Generate comprehensive strategic recommendations
        capital_amount = 5000000  # $5M example
        recommendations = optimizer.generate_strategic_recommendations(capital_amount)
        
        print(f"\n💰 Strategic Investment Analysis (${capital_amount:,.0f})")
        print("-" * 50)
        
        # Display investment strategies
        print(f"\n📊 Investment Strategies:")
        for strategy in recommendations['investment_strategies']:
            print(f"• {strategy['strategy_name']}")
            print(f"  Expected Return: {strategy['expected_return']:.1f}%")
            print(f"  Risk Score: {strategy['risk_score']:.2f}")
            print(f"  Timeline: {strategy['investment_timeline']} months")
            print(f"  Top Sectors: {', '.join(list(strategy['recommended_allocation'].keys())[:3])}")
            print()
        
        # Display portfolio optimizations
        print(f"🎯 Optimized Portfolios:")
        for risk_profile, portfolio in recommendations['optimized_portfolios'].items():
            print(f"• {risk_profile.title()} Portfolio")
            print(f"  Expected Return: {portfolio['expected_portfolio_return']:.1f}%")
            print(f"  Risk Score: {portfolio['portfolio_risk_score']:.2f}")
            print(f"  Diversification: {portfolio['diversification_score']:.2f}")
            print(f"  Sectors: {len(portfolio['optimized_allocation'])}")
            print()
        
        # Display market predictions
        print(f"🔮 Market Predictions:")
        for prediction in recommendations['market_predictions'][:3]:
            print(f"• {prediction['prediction_type'].replace('_', ' ').title()}")
            print(f"  Predicted Value: {prediction['prediction_value']:.1f}%")
            print(f"  Confidence Range: {prediction['confidence_interval'][0]:.1f}% - {prediction['confidence_interval'][1]:.1f}%")
            print(f"  Timeframe: {prediction['timeframe_months']} months")
            print()
        
        # Display top opportunities
        print(f"⭐ Top Investment Opportunities:")
        for i, opp in enumerate(recommendations['top_opportunities'][:3], 1):
            print(f"{i}. {opp['company_name']}")
            print(f"   Score: {opp['opportunity_score']:.2f} | Timing: {opp['optimal_timing_weeks']} weeks")
            print(f"   Recommendation: {opp['recommendation']}")
            print()
        
        # Display strategic insights
        print(f"💡 Strategic Insights:")
        for insight in recommendations['strategic_insights']:
            print(f"• {insight}")
        
        print("\n✅ Investment Strategy Optimization Complete!")
        
    except Exception as e:
        print(f"❌ Error in investment strategy optimization: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
