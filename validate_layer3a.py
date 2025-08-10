#!/usr/bin/env python3
"""
LAYER 3A: VALIDATION TEST SUITE
===============================
Focused validation tests for specific business logic and edge cases.
Validates the accuracy and reliability of Layer 3A predictions.
"""

import os
import json
from typing import Dict, List, Any
from dotenv import load_dotenv
from supabase import create_client, Client

# Import Layer 3A components
from layer3_discovery_patterns import DiscoveryPatternAnalyzer
from layer3_investment_timing import InvestmentTimingPredictor
from layer3_market_trends import MarketTrendForecaster

# Load environment
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class Layer3AValidationSuite:
    """Validation tests for Layer 3A business logic."""
    
    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.discovery_analyzer = DiscoveryPatternAnalyzer(self.supabase)
        self.timing_predictor = InvestmentTimingPredictor(self.supabase)
        self.trend_forecaster = MarketTrendForecaster(self.supabase)

    def validate_discovery_predictions(self) -> Dict[str, Any]:
        """Validate discovery pattern predictions for accuracy."""
        
        print("🔍 Validating Discovery Pattern Predictions...")
        
        validation_results = {
            'trl_extraction': self._validate_trl_extraction(),
            'sector_classification': self._validate_sector_classification(),
            'timeline_predictions': self._validate_timeline_predictions(),
            'confidence_scoring': self._validate_confidence_scoring()
        }
        
        return validation_results

    def validate_investment_timing(self) -> Dict[str, Any]:
        """Validate investment timing predictions."""
        
        print("⏰ Validating Investment Timing Predictions...")
        
        validation_results = {
            'signal_strength': self._validate_signal_strength(),
            'timing_logic': self._validate_timing_logic(),
            'risk_assessment': self._validate_risk_assessment(),
            'opportunity_scoring': self._validate_opportunity_scoring()
        }
        
        return validation_results

    def validate_market_trends(self) -> Dict[str, Any]:
        """Validate market trend predictions."""
        
        print("📈 Validating Market Trend Predictions...")
        
        validation_results = {
            'momentum_calculation': self._validate_momentum_calculation(),
            'growth_predictions': self._validate_growth_predictions(),
            'sector_analysis': self._validate_sector_analysis(),
            'recommendation_logic': self._validate_recommendation_logic()
        }
        
        return validation_results

    def _validate_trl_extraction(self) -> Dict[str, Any]:
        """Validate TRL extraction accuracy."""
        
        test_cases = [
            {"text": "Technology Readiness Level 6 achieved", "expected": 6},
            {"text": "TRL 3 - early prototype", "expected": 3},
            {"text": "TRL-9 commercial ready", "expected": 9},
            {"text": "No TRL mentioned here", "expected": None},
            {"text": "TRL 7-8 range for demonstration", "expected": 7}  # Should extract first number
        ]
        
        results = []
        for case in test_cases:
            extracted = self.discovery_analyzer._extract_trl(case["text"])
            correct = extracted == case["expected"]
            results.append({
                'text': case["text"],
                'expected': case["expected"],
                'extracted': extracted,
                'correct': correct
            })
        
        accuracy = sum(1 for r in results if r['correct']) / len(results)
        
        return {
            'test_cases': results,
            'accuracy': accuracy,
            'passed': accuracy >= 0.8  # 80% accuracy threshold
        }

    def _validate_sector_classification(self) -> Dict[str, Any]:
        """Validate technology sector classification."""
        
        test_cases = [
            {"text": "advanced battery storage technology", "expected_sectors": ["energy_storage"]},
            {"text": "solar photovoltaic panels renewable energy", "expected_sectors": ["solar_energy"]},
            {"text": "hydrogen fuel cell electrolysis", "expected_sectors": ["hydrogen"]},
            {"text": "carbon capture direct air capture technology", "expected_sectors": ["carbon_capture"]},
            {"text": "quantum computing quantum sensing breakthrough", "expected_sectors": ["quantum"]}
        ]
        
        results = []
        for case in test_cases:
            sectors = self.discovery_analyzer._extract_tech_sectors(case["text"])
            
            # Check if any expected sector is found
            found_expected = any(
                expected in sectors for expected in case["expected_sectors"]
            )
            
            results.append({
                'text': case["text"],
                'expected_sectors': case["expected_sectors"],
                'found_sectors': sectors,
                'correct': found_expected
            })
        
        accuracy = sum(1 for r in results if r['correct']) / len(results)
        
        return {
            'test_cases': results,
            'accuracy': accuracy,
            'passed': accuracy >= 0.8
        }

    def _validate_timeline_predictions(self) -> Dict[str, Any]:
        """Validate commercialization timeline predictions."""
        
        # Get sample government research companies
        gov_companies = self.supabase.table('deals_new').select(
            'company_id,raw_text_content'
        ).eq('source_type', 'government_research').limit(5).execute()
        
        results = []
        for company in gov_companies.data:
            prediction = self.discovery_analyzer.predict_commercialization_timeline(company['company_id'])
            
            if prediction:
                # Validate prediction logic
                reasonable_timeline = 4 <= prediction.predicted_funding_weeks <= 520  # 1 month to 10 years
                reasonable_confidence = 0.0 <= prediction.confidence_score <= 1.0
                
                results.append({
                    'company_id': company['company_id'],
                    'timeline_weeks': prediction.predicted_funding_weeks,
                    'confidence': prediction.confidence_score,
                    'reasonable_timeline': reasonable_timeline,
                    'reasonable_confidence': reasonable_confidence,
                    'valid': reasonable_timeline and reasonable_confidence
                })
        
        validity_rate = sum(1 for r in results if r['valid']) / len(results) if results else 0
        
        return {
            'predictions_tested': len(results),
            'validity_rate': validity_rate,
            'sample_predictions': results[:3],
            'passed': validity_rate >= 0.8
        }

    def _validate_confidence_scoring(self) -> Dict[str, Any]:
        """Validate confidence scoring logic."""
        
        # Test confidence scoring with different data qualities
        test_scenarios = [
            {"description": "High quality: Government research with TRL", "has_trl": True, "agencies": 2, "expected_confidence": "> 0.6"},
            {"description": "Medium quality: Some agencies, no TRL", "has_trl": False, "agencies": 1, "expected_confidence": "0.4-0.6"},
            {"description": "Low quality: Limited data", "has_trl": False, "agencies": 0, "expected_confidence": "< 0.4"}
        ]
        
        # Get actual companies and test
        sample_companies = self.supabase.table('deals_new').select(
            'company_id,raw_text_content'
        ).eq('source_type', 'government_research').limit(3).execute()
        
        results = []
        for i, company in enumerate(sample_companies.data):
            prediction = self.discovery_analyzer.predict_commercialization_timeline(company['company_id'])
            if prediction:
                confidence = prediction.confidence_score
                
                # Classify confidence level
                if confidence > 0.6:
                    level = "high"
                elif confidence > 0.4:
                    level = "medium"
                else:
                    level = "low"
                
                results.append({
                    'company_id': company['company_id'],
                    'confidence': confidence,
                    'level': level,
                    'reasonable': 0.0 <= confidence <= 1.0
                })
        
        reasonableness = sum(1 for r in results if r['reasonable']) / len(results) if results else 0
        
        return {
            'confidence_tests': results,
            'reasonableness_rate': reasonableness,
            'passed': reasonableness >= 0.9
        }

    def _validate_signal_strength(self) -> Dict[str, Any]:
        """Validate investment signal strength calculations."""
        
        # Test signal strength for different source types
        sample_companies = self.supabase.table('deals_new').select('company_id').limit(3).execute()
        
        results = []
        for company in sample_companies.data:
            signals = self.timing_predictor.analyze_investment_signals(company['company_id'])
            
            for signal in signals:
                valid_strength = 0.0 <= signal.strength <= 1.0
                valid_confidence = 0.0 <= signal.confidence <= 1.0
                reasonable_timeframe = 4 <= signal.timeframe_weeks <= 520
                
                results.append({
                    'signal_type': signal.signal_type,
                    'strength': signal.strength,
                    'confidence': signal.confidence,
                    'timeframe_weeks': signal.timeframe_weeks,
                    'valid': valid_strength and valid_confidence and reasonable_timeframe
                })
        
        validity_rate = sum(1 for r in results if r['valid']) / len(results) if results else 0
        
        return {
            'signals_tested': len(results),
            'validity_rate': validity_rate,
            'sample_signals': results[:5],
            'passed': validity_rate >= 0.8
        }

    def _validate_timing_logic(self) -> Dict[str, Any]:
        """Validate investment timing logic."""
        
        # Test timing predictions for consistency
        sample_companies = self.supabase.table('deals_new').select('company_id').limit(3).execute()
        
        results = []
        for company in sample_companies.data:
            timing = self.timing_predictor.predict_optimal_timing(company['company_id'])
            
            if timing:
                reasonable_timing = 4 <= timing.optimal_timing_weeks <= 520
                reasonable_confidence = 0.0 <= timing.timing_confidence <= 1.0
                reasonable_opportunity = 0.0 <= timing.opportunity_score <= 1.0
                
                # Check recommendation consistency
                rec_consistent = True
                if timing.opportunity_score > 0.8 and 'BUY' not in timing.recommendation.upper():
                    rec_consistent = False
                
                results.append({
                    'company_id': company['company_id'],
                    'timing_weeks': timing.optimal_timing_weeks,
                    'confidence': timing.timing_confidence,
                    'opportunity_score': timing.opportunity_score,
                    'recommendation': timing.recommendation,
                    'valid': reasonable_timing and reasonable_confidence and reasonable_opportunity and rec_consistent
                })
        
        validity_rate = sum(1 for r in results if r['valid']) / len(results) if results else 0
        
        return {
            'timing_predictions': results,
            'validity_rate': validity_rate,
            'passed': validity_rate >= 0.8
        }

    def _validate_risk_assessment(self) -> Dict[str, Any]:
        """Validate risk assessment logic."""
        
        # Test risk factor identification
        sample_companies = self.supabase.table('deals_new').select('company_id').limit(3).execute()
        
        results = []
        for company in sample_companies.data:
            timing = self.timing_predictor.predict_optimal_timing(company['company_id'])
            
            if timing:
                # Validate risk factors are strings
                valid_risks = all(isinstance(risk, str) for risk in timing.risk_factors)
                
                # Check risk-opportunity correlation
                high_risk_count = len(timing.risk_factors)
                if high_risk_count > 3 and timing.opportunity_score > 0.8:
                    # High risk but high opportunity should be flagged
                    risk_opportunity_consistent = False
                else:
                    risk_opportunity_consistent = True
                
                results.append({
                    'company_id': company['company_id'],
                    'risk_count': len(timing.risk_factors),
                    'risk_factors': timing.risk_factors,
                    'opportunity_score': timing.opportunity_score,
                    'valid_risks': valid_risks,
                    'consistent': risk_opportunity_consistent
                })
        
        consistency_rate = sum(1 for r in results if r['valid_risks'] and r['consistent']) / len(results) if results else 0
        
        return {
            'risk_assessments': results,
            'consistency_rate': consistency_rate,
            'passed': consistency_rate >= 0.8
        }

    def _validate_opportunity_scoring(self) -> Dict[str, Any]:
        """Validate opportunity scoring algorithm."""
        
        # Test opportunity scoring
        opportunities = self.timing_predictor.batch_analyze_investment_opportunities()
        
        results = []
        for opp in opportunities[:5]:  # Test top 5
            valid_score = 0.0 <= opp.opportunity_score <= 1.0
            
            # High scores should have good recommendations
            if opp.opportunity_score > 0.8:
                good_recommendation = 'BUY' in opp.recommendation.upper() or 'STRONG' in opp.recommendation.upper()
            else:
                good_recommendation = True  # No specific requirement for lower scores
            
            results.append({
                'company_name': opp.company_name,
                'opportunity_score': opp.opportunity_score,
                'recommendation': opp.recommendation,
                'valid_score': valid_score,
                'good_recommendation': good_recommendation
            })
        
        validity_rate = sum(1 for r in results if r['valid_score'] and r['good_recommendation']) / len(results) if results else 0
        
        return {
            'opportunity_tests': results,
            'validity_rate': validity_rate,
            'passed': validity_rate >= 0.8
        }

    def _validate_momentum_calculation(self) -> Dict[str, Any]:
        """Validate sector momentum calculations."""
        
        # Test momentum for known sectors
        trends = self.trend_forecaster.analyze_sector_trends()
        
        results = []
        for trend in trends[:5]:  # Test top 5 sectors
            valid_momentum = 0.0 <= trend.momentum_score <= 1.0
            valid_confidence = 0.0 <= trend.confidence <= 1.0
            
            # Check trend direction consistency
            if trend.momentum_score > 0.7:
                direction_consistent = trend.trend_direction == 'rising'
            elif trend.momentum_score < 0.3:
                direction_consistent = trend.trend_direction == 'declining'
            else:
                direction_consistent = trend.trend_direction == 'stable'
            
            results.append({
                'sector': trend.sector,
                'momentum_score': trend.momentum_score,
                'trend_direction': trend.trend_direction,
                'confidence': trend.confidence,
                'valid': valid_momentum and valid_confidence and direction_consistent
            })
        
        validity_rate = sum(1 for r in results if r['valid']) / len(results) if results else 0
        
        return {
            'momentum_tests': results,
            'validity_rate': validity_rate,
            'passed': validity_rate >= 0.8
        }

    def _validate_growth_predictions(self) -> Dict[str, Any]:
        """Validate sector growth predictions."""
        
        # Test growth predictions for key sectors
        test_sectors = ['energy_storage', 'solar_energy', 'hydrogen']
        
        results = []
        for sector in test_sectors:
            forecast = self.trend_forecaster.forecast_sector_growth(sector, 12)
            
            if forecast:
                reasonable_growth = 5 <= forecast.growth_prediction <= 100  # 5% to 100% growth
                valid_confidence = 0.0 <= forecast.forecast_confidence <= 1.0
                
                results.append({
                    'sector': sector,
                    'growth_prediction': forecast.growth_prediction,
                    'confidence': forecast.forecast_confidence,
                    'recommendation': forecast.recommended_action,
                    'valid': reasonable_growth and valid_confidence
                })
        
        validity_rate = sum(1 for r in results if r['valid']) / len(results) if results else 0
        
        return {
            'growth_tests': results,
            'validity_rate': validity_rate,
            'passed': validity_rate >= 0.8
        }

    def _validate_sector_analysis(self) -> Dict[str, Any]:
        """Validate sector analysis logic."""
        
        # Generate market outlook and validate
        outlook = self.trend_forecaster.generate_market_outlook(12)
        
        valid_momentum = 0.0 <= outlook['overall_momentum']['score'] <= 1.0
        valid_confidence = 0.0 <= outlook['outlook_confidence'] <= 1.0
        has_sectors = len(outlook['sector_trends']) > 0
        has_forecasts = len(outlook['sector_forecasts']) > 0
        
        return {
            'overall_momentum': outlook['overall_momentum']['score'],
            'outlook_confidence': outlook['outlook_confidence'],
            'sectors_analyzed': len(outlook['sector_trends']),
            'forecasts_generated': len(outlook['sector_forecasts']),
            'valid_momentum': valid_momentum,
            'valid_confidence': valid_confidence,
            'has_data': has_sectors and has_forecasts,
            'passed': valid_momentum and valid_confidence and has_sectors and has_forecasts
        }

    def _validate_recommendation_logic(self) -> Dict[str, Any]:
        """Validate investment recommendation logic."""
        
        # Test recommendation consistency
        outlook = self.trend_forecaster.generate_market_outlook(12)
        recommendations = outlook['investment_recommendations']
        
        results = []
        for rec in recommendations[:5]:  # Test top 5
            # High growth should correlate with Buy recommendations
            if rec['growth_potential'] > 40:
                good_rec = 'Buy' in rec['action'] or 'Strong Buy' in rec['action']
            elif rec['growth_potential'] < 15:
                good_rec = 'Monitor' in rec['action'] or 'Hold' in rec['action']
            else:
                good_rec = True  # Medium growth can have various recommendations
            
            # Priority should correlate with growth and action
            if 'Strong Buy' in rec['action']:
                priority_consistent = rec['priority'] == 'High'
            elif 'Monitor' in rec['action']:
                priority_consistent = rec['priority'] == 'Low'
            else:
                priority_consistent = True
            
            results.append({
                'sector': rec['sector'],
                'action': rec['action'],
                'priority': rec['priority'],
                'growth_potential': rec['growth_potential'],
                'good_recommendation': good_rec,
                'priority_consistent': priority_consistent
            })
        
        consistency_rate = sum(1 for r in results if r['good_recommendation'] and r['priority_consistent']) / len(results) if results else 0
        
        return {
            'recommendation_tests': results,
            'consistency_rate': consistency_rate,
            'passed': consistency_rate >= 0.8
        }

def main():
    """Run Layer 3A validation suite."""
    
    try:
        print("🎯 LAYER 3A: VALIDATION TEST SUITE")
        print("=" * 60)
        
        validator = Layer3AValidationSuite()
        
        # Run validation tests
        discovery_validation = validator.validate_discovery_predictions()
        timing_validation = validator.validate_investment_timing()
        trends_validation = validator.validate_market_trends()
        
        # Print results
        print("\n📊 VALIDATION RESULTS:")
        print("-" * 40)
        
        print(f"\n🔍 Discovery Pattern Validation:")
        for test, result in discovery_validation.items():
            status = "✅" if result.get('passed', False) else "❌"
            accuracy = result.get('accuracy', result.get('validity_rate', 'N/A'))
            print(f"   {status} {test}: {accuracy:.2f}" if isinstance(accuracy, float) else f"   {status} {test}: {accuracy}")
        
        print(f"\n⏰ Investment Timing Validation:")
        for test, result in timing_validation.items():
            status = "✅" if result.get('passed', False) else "❌"
            rate = result.get('validity_rate', result.get('consistency_rate', 'N/A'))
            print(f"   {status} {test}: {rate:.2f}" if isinstance(rate, float) else f"   {status} {test}: {rate}")
        
        print(f"\n📈 Market Trends Validation:")
        for test, result in trends_validation.items():
            status = "✅" if result.get('passed', False) else "❌"
            rate = result.get('validity_rate', result.get('consistency_rate', 'N/A'))
            print(f"   {status} {test}: {rate:.2f}" if isinstance(rate, float) else f"   {status} {test}: {rate}")
        
        # Overall validation score
        all_tests = list(discovery_validation.values()) + list(timing_validation.values()) + list(trends_validation.values())
        passed_tests = sum(1 for test in all_tests if test.get('passed', False))
        total_tests = len(all_tests)
        
        print(f"\n🎯 OVERALL VALIDATION:")
        print(f"   Tests Passed: {passed_tests}/{total_tests}")
        print(f"   Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        if passed_tests/total_tests >= 0.85:
            print("   🎉 LAYER 3A VALIDATION: EXCELLENT")
        elif passed_tests/total_tests >= 0.70:
            print("   ✅ LAYER 3A VALIDATION: GOOD")
        else:
            print("   ⚠️  LAYER 3A VALIDATION: NEEDS IMPROVEMENT")
        
        # Save validation results
        validation_results = {
            'discovery_patterns': discovery_validation,
            'investment_timing': timing_validation,
            'market_trends': trends_validation,
            'overall_score': passed_tests/total_tests
        }
        
        with open('layer3a_validation_results.json', 'w') as f:
            json.dump(validation_results, f, indent=2, default=str)
        
        print(f"\n💾 Validation results saved to: layer3a_validation_results.json")
        
    except Exception as e:
        print(f"❌ Validation suite failed: {e}")

if __name__ == "__main__":
    main()
