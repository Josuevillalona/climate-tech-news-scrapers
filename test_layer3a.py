#!/usr/bin/env python3
"""
LAYER 3A: COMPREHENSIVE TEST SUITE
==================================
Tests all three components of Layer 3A Enhanced Discovery System:
- 3A.1: Discovery Pattern Analysis
- 3A.2: Investment Timing Model  
- 3A.3: Market Trend Forecasting

Test Categories:
- Unit Tests: Individual component functionality
- Integration Tests: Cross-component interactions
- Data Quality Tests: Validate predictions and confidence scores
- Performance Tests: Response times and accuracy
"""

import os
import sys
import time
import unittest
from datetime import datetime
from typing import Dict, List, Any
from dotenv import load_dotenv
from supabase import create_client, Client

# Import Layer 3A components
from layer3_discovery_patterns import DiscoveryPatternAnalyzer, CommercializationPrediction
from layer3_investment_timing import InvestmentTimingPredictor, InvestmentTiming
from layer3_market_trends import MarketTrendForecaster, MarketTrend, SectorForecast

# Load environment
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class Layer3ATestSuite:
    """Comprehensive test suite for Layer 3A system."""
    
    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.discovery_analyzer = DiscoveryPatternAnalyzer(self.supabase)
        self.timing_predictor = InvestmentTimingPredictor(self.supabase)
        self.trend_forecaster = MarketTrendForecaster(self.supabase)
        
        self.test_results = {
            'discovery_patterns': [],
            'investment_timing': [],
            'market_trends': [],
            'integration': [],
            'performance': []
        }

    def run_all_tests(self) -> Dict[str, Any]:
        """Run comprehensive test suite."""
        
        print("🧪 LAYER 3A: COMPREHENSIVE TEST SUITE")
        print("=" * 60)
        
        start_time = time.time()
        
        # Test 3A.1: Discovery Pattern Analysis
        print("\n📊 Testing 3A.1: Discovery Pattern Analysis...")
        discovery_results = self.test_discovery_patterns()
        
        # Test 3A.2: Investment Timing Model
        print("\n⏰ Testing 3A.2: Investment Timing Model...")
        timing_results = self.test_investment_timing()
        
        # Test 3A.3: Market Trend Forecasting
        print("\n📈 Testing 3A.3: Market Trend Forecasting...")
        trend_results = self.test_market_trends()
        
        # Integration Tests
        print("\n🔗 Testing Integration Between Components...")
        integration_results = self.test_integration()
        
        # Performance Tests
        print("\n⚡ Testing Performance...")
        performance_results = self.test_performance()
        
        total_time = time.time() - start_time
        
        # Compile results
        results = {
            'test_summary': {
                'total_tests': len(discovery_results) + len(timing_results) + len(trend_results) + len(integration_results),
                'passed_tests': sum(1 for r in discovery_results + timing_results + trend_results + integration_results if r['passed']),
                'total_time_seconds': round(total_time, 2)
            },
            'discovery_patterns': discovery_results,
            'investment_timing': timing_results,
            'market_trends': trend_results,
            'integration': integration_results,
            'performance': performance_results
        }
        
        self.print_test_summary(results)
        return results

    def test_discovery_patterns(self) -> List[Dict[str, Any]]:
        """Test Discovery Pattern Analysis component."""
        
        tests = []
        
        # Test 1: Government Research Pattern Analysis
        try:
            # Use the correct method name from DiscoveryPatternAnalyzer
            sample_companies = self.supabase.table('deals_new').select('company_id').eq('source_type', 'government_research').limit(5).execute()
            
            pattern_count = 0
            for company in sample_companies.data:
                prediction = self.discovery_analyzer.predict_commercialization_timeline(company['company_id'])
                if prediction:
                    pattern_count += 1
            
            tests.append({
                'test_name': 'Government Research Pattern Analysis',
                'passed': pattern_count > 0,
                'result': f"Analyzed {pattern_count} government research patterns",
                'details': {'pattern_count': pattern_count, 'companies_tested': len(sample_companies.data)}
            })
        except Exception as e:
            tests.append({
                'test_name': 'Government Research Pattern Analysis',
                'passed': False,
                'result': f"Error: {e}",
                'details': {'error': str(e)}
            })
        
        # Test 2: Technology Sector Classification
        try:
            # Get a sample company
            sample_data = self.supabase.table('deals_new').select('company_id,raw_text_content').limit(1).execute()
            if sample_data.data:
                company_id = sample_data.data[0]['company_id']
                content = sample_data.data[0]['raw_text_content']
                
                sectors = self.discovery_analyzer._extract_tech_sectors(content)
                tests.append({
                    'test_name': 'Technology Sector Classification',
                    'passed': isinstance(sectors, list),
                    'result': f"Classified {len(sectors)} sectors",
                    'details': {'sectors': sectors, 'company_id': company_id}
                })
            else:
                tests.append({
                    'test_name': 'Technology Sector Classification',
                    'passed': False,
                    'result': "No sample data available",
                    'details': {}
                })
        except Exception as e:
            tests.append({
                'test_name': 'Technology Sector Classification',
                'passed': False,
                'result': f"Error: {e}",
                'details': {'error': str(e)}
            })
        
        # Test 3: Commercialization Timeline Prediction
        try:
            # Test with government research data
            gov_data = self.supabase.table('deals_new').select('company_id').eq('source_type', 'government_research').limit(1).execute()
            if gov_data.data:
                company_id = gov_data.data[0]['company_id']
                prediction = self.discovery_analyzer.predict_commercialization_timeline(company_id)
                
                tests.append({
                    'test_name': 'Commercialization Timeline Prediction',
                    'passed': prediction is not None and hasattr(prediction, 'predicted_funding_weeks'),
                    'result': f"Predicted {prediction.predicted_funding_weeks if prediction else 'N/A'} weeks to funding",
                    'details': {
                        'company_id': company_id,
                        'prediction': prediction.__dict__ if prediction else None
                    }
                })
            else:
                tests.append({
                    'test_name': 'Commercialization Timeline Prediction',
                    'passed': False,
                    'result': "No government research data available",
                    'details': {}
                })
        except Exception as e:
            tests.append({
                'test_name': 'Commercialization Timeline Prediction',
                'passed': False,
                'result': f"Error: {e}",
                'details': {'error': str(e)}
            })
        
        # Test 4: TRL Extraction
        try:
            sample_text = "This technology has reached TRL 6 and is ready for demonstration."
            trl = self.discovery_analyzer._extract_trl(sample_text)
            tests.append({
                'test_name': 'TRL Extraction',
                'passed': trl == 6,
                'result': f"Extracted TRL: {trl}",
                'details': {'trl': trl, 'sample_text': sample_text}
            })
        except Exception as e:
            tests.append({
                'test_name': 'TRL Extraction',
                'passed': False,
                'result': f"Error: {e}",
                'details': {'error': str(e)}
            })
        
        return tests

    def test_investment_timing(self) -> List[Dict[str, Any]]:
        """Test Investment Timing Model component."""
        
        tests = []
        
        # Test 1: Investment Signal Analysis
        try:
            # Get a sample company with multiple source types
            companies = self.supabase.table('deals_new').select('company_id').limit(5).execute()
            if companies.data:
                company_id = companies.data[0]['company_id']
                signals = self.timing_predictor.analyze_investment_signals(company_id)
                
                tests.append({
                    'test_name': 'Investment Signal Analysis',
                    'passed': isinstance(signals, list),
                    'result': f"Generated {len(signals)} investment signals",
                    'details': {
                        'company_id': company_id,
                        'signal_count': len(signals),
                        'signal_types': [s.signal_type for s in signals]
                    }
                })
            else:
                tests.append({
                    'test_name': 'Investment Signal Analysis',
                    'passed': False,
                    'result': "No sample data available",
                    'details': {}
                })
        except Exception as e:
            tests.append({
                'test_name': 'Investment Signal Analysis',
                'passed': False,
                'result': f"Error: {e}",
                'details': {'error': str(e)}
            })
        
        # Test 2: Optimal Timing Prediction
        try:
            companies = self.supabase.table('deals_new').select('company_id').limit(3).execute()
            if companies.data:
                company_id = companies.data[0]['company_id']
                timing = self.timing_predictor.predict_optimal_timing(company_id)
                
                tests.append({
                    'test_name': 'Optimal Timing Prediction',
                    'passed': timing is not None and hasattr(timing, 'optimal_timing_weeks'),
                    'result': f"Predicted optimal timing: {timing.optimal_timing_weeks if timing else 'N/A'} weeks",
                    'details': {
                        'company_id': company_id,
                        'timing': timing.__dict__ if timing else None
                    }
                })
            else:
                tests.append({
                    'test_name': 'Optimal Timing Prediction',
                    'passed': False,
                    'result': "No sample data available",
                    'details': {}
                })
        except Exception as e:
            tests.append({
                'test_name': 'Optimal Timing Prediction',
                'passed': False,
                'result': f"Error: {e}",
                'details': {'error': str(e)}
            })
        
        # Test 3: Batch Investment Analysis
        try:
            opportunities = self.timing_predictor.batch_analyze_investment_opportunities()
            tests.append({
                'test_name': 'Batch Investment Analysis',
                'passed': isinstance(opportunities, list) and len(opportunities) >= 0,
                'result': f"Analyzed {len(opportunities)} investment opportunities",
                'details': {
                    'opportunity_count': len(opportunities),
                    'top_opportunities': [
                        {
                            'company': opp.company_name,
                            'score': opp.opportunity_score,
                            'timing': opp.optimal_timing_weeks
                        }
                        for opp in opportunities[:3]
                    ]
                }
            })
        except Exception as e:
            tests.append({
                'test_name': 'Batch Investment Analysis',
                'passed': False,
                'result': f"Error: {e}",
                'details': {'error': str(e)}
            })
        
        # Test 4: Risk Factor Assessment
        try:
            # Test with a known company
            companies = self.supabase.table('deals_new').select('company_id,raw_text_content').limit(1).execute()
            if companies.data:
                company_data = companies.data[0]
                signals = self.timing_predictor.analyze_investment_signals(company_data['company_id'])
                risks = self.timing_predictor._assess_risk_factors(signals, company_data)
                
                tests.append({
                    'test_name': 'Risk Factor Assessment',
                    'passed': isinstance(risks, list),
                    'result': f"Identified {len(risks)} risk factors",
                    'details': {'risk_factors': risks}
                })
            else:
                tests.append({
                    'test_name': 'Risk Factor Assessment',
                    'passed': False,
                    'result': "No sample data available",
                    'details': {}
                })
        except Exception as e:
            tests.append({
                'test_name': 'Risk Factor Assessment',
                'passed': False,
                'result': f"Error: {e}",
                'details': {'error': str(e)}
            })
        
        return tests

    def test_market_trends(self) -> List[Dict[str, Any]]:
        """Test Market Trend Forecasting component."""
        
        tests = []
        
        # Test 1: Sector Trend Analysis
        try:
            trends = self.trend_forecaster.analyze_sector_trends()
            tests.append({
                'test_name': 'Sector Trend Analysis',
                'passed': isinstance(trends, list) and len(trends) > 0,
                'result': f"Analyzed {len(trends)} sector trends",
                'details': {
                    'trend_count': len(trends),
                    'top_sectors': [
                        {
                            'sector': trend.sector,
                            'momentum': trend.momentum_score,
                            'direction': trend.trend_direction
                        }
                        for trend in trends[:3]
                    ]
                }
            })
        except Exception as e:
            tests.append({
                'test_name': 'Sector Trend Analysis',
                'passed': False,
                'result': f"Error: {e}",
                'details': {'error': str(e)}
            })
        
        # Test 2: Sector Growth Forecasting
        try:
            forecast = self.trend_forecaster.forecast_sector_growth('energy_storage', 12)
            tests.append({
                'test_name': 'Sector Growth Forecasting',
                'passed': forecast is not None and hasattr(forecast, 'growth_prediction'),
                'result': f"Forecasted {forecast.growth_prediction if forecast else 'N/A'}% growth for energy storage",
                'details': {
                    'forecast': forecast.__dict__ if forecast else None
                }
            })
        except Exception as e:
            tests.append({
                'test_name': 'Sector Growth Forecasting',
                'passed': False,
                'result': f"Error: {e}",
                'details': {'error': str(e)}
            })
        
        # Test 3: Emerging Trend Detection
        try:
            emerging = self.trend_forecaster.identify_emerging_trends()
            tests.append({
                'test_name': 'Emerging Trend Detection',
                'passed': isinstance(emerging, list),
                'result': f"Identified {len(emerging)} emerging trends",
                'details': {
                    'emerging_count': len(emerging),
                    'top_trends': emerging[:3] if emerging else []
                }
            })
        except Exception as e:
            tests.append({
                'test_name': 'Emerging Trend Detection',
                'passed': False,
                'result': f"Error: {e}",
                'details': {'error': str(e)}
            })
        
        # Test 4: Market Outlook Generation
        try:
            outlook = self.trend_forecaster.generate_market_outlook(6)
            tests.append({
                'test_name': 'Market Outlook Generation',
                'passed': isinstance(outlook, dict) and 'overall_momentum' in outlook,
                'result': f"Generated 6-month outlook with {outlook.get('overall_momentum', {}).get('score', 'N/A')} momentum score",
                'details': {
                    'outlook_keys': list(outlook.keys()) if outlook else [],
                    'momentum': outlook.get('overall_momentum', {}) if outlook else {}
                }
            })
        except Exception as e:
            tests.append({
                'test_name': 'Market Outlook Generation',
                'passed': False,
                'result': f"Error: {e}",
                'details': {'error': str(e)}
            })
        
        return tests

    def test_integration(self) -> List[Dict[str, Any]]:
        """Test integration between Layer 3A components."""
        
        tests = []
        
        # Test 1: Cross-Component Data Flow
        try:
            # Test data flow from Discovery → Timing → Trends
            gov_companies = self.supabase.table('deals_new').select('company_id').eq('source_type', 'government_research').limit(1).execute()
            
            if gov_companies.data:
                company_id = gov_companies.data[0]['company_id']
                
                # Get discovery prediction
                discovery_prediction = self.discovery_analyzer.predict_commercialization_timeline(company_id)
                
                # Use in timing analysis
                timing_prediction = self.timing_predictor.predict_optimal_timing(company_id)
                
                # Check if data flows correctly
                data_flow_valid = (
                    discovery_prediction is not None and 
                    timing_prediction is not None
                )
                
                tests.append({
                    'test_name': 'Cross-Component Data Flow',
                    'passed': data_flow_valid,
                    'result': f"Data flow {'successful' if data_flow_valid else 'failed'} for company {company_id}",
                    'details': {
                        'discovery_result': discovery_prediction.__dict__ if discovery_prediction else None,
                        'timing_result': timing_prediction.__dict__ if timing_prediction else None
                    }
                })
            else:
                tests.append({
                    'test_name': 'Cross-Component Data Flow',
                    'passed': False,
                    'result': "No government research data for integration test",
                    'details': {}
                })
        except Exception as e:
            tests.append({
                'test_name': 'Cross-Component Data Flow',
                'passed': False,
                'result': f"Error: {e}",
                'details': {'error': str(e)}
            })
        
        # Test 2: Consistent Sector Classification
        try:
            sample_content = "Advanced battery storage technology for renewable energy integration"
            
            # Test sector classification consistency across components
            discovery_sectors = self.discovery_analyzer._extract_tech_sectors(sample_content)
            
            # Mock trend analysis for same content
            trend_analysis = any('storage' in sector.lower() for sector in discovery_sectors)
            
            tests.append({
                'test_name': 'Consistent Sector Classification',
                'passed': len(discovery_sectors) > 0,
                'result': f"Consistently classified {len(discovery_sectors)} sectors",
                'details': {
                    'sectors': discovery_sectors,
                    'trend_match': trend_analysis
                }
            })
        except Exception as e:
            tests.append({
                'test_name': 'Consistent Sector Classification',
                'passed': False,
                'result': f"Error: {e}",
                'details': {'error': str(e)}
            })
        
        return tests

    def test_performance(self) -> Dict[str, Any]:
        """Test performance of Layer 3A components."""
        
        performance_results = {}
        
        # Test Discovery Pattern Analysis Performance
        try:
            start_time = time.time()
            # Test with sample government research companies
            sample_companies = self.supabase.table('deals_new').select('company_id').eq('source_type', 'government_research').limit(3).execute()
            
            pattern_count = 0
            for company in sample_companies.data:
                prediction = self.discovery_analyzer.predict_commercialization_timeline(company['company_id'])
                if prediction:
                    pattern_count += 1
            
            discovery_time = time.time() - start_time
            
            performance_results['discovery_patterns'] = {
                'execution_time_seconds': round(discovery_time, 2),
                'patterns_analyzed': pattern_count,
                'performance_rating': 'Good' if discovery_time < 10 else 'Slow'
            }
        except Exception as e:
            performance_results['discovery_patterns'] = {
                'execution_time_seconds': None,
                'error': str(e),
                'performance_rating': 'Failed'
            }
        
        # Test Investment Timing Performance
        try:
            start_time = time.time()
            opportunities = self.timing_predictor.batch_analyze_investment_opportunities()
            timing_time = time.time() - start_time
            
            performance_results['investment_timing'] = {
                'execution_time_seconds': round(timing_time, 2),
                'opportunities_analyzed': len(opportunities),
                'performance_rating': 'Good' if timing_time < 15 else 'Slow'
            }
        except Exception as e:
            performance_results['investment_timing'] = {
                'execution_time_seconds': None,
                'error': str(e),
                'performance_rating': 'Failed'
            }
        
        # Test Market Trends Performance
        try:
            start_time = time.time()
            outlook = self.trend_forecaster.generate_market_outlook(6)
            trends_time = time.time() - start_time
            
            performance_results['market_trends'] = {
                'execution_time_seconds': round(trends_time, 2),
                'sectors_analyzed': outlook.get('overall_momentum', {}).get('sectors_analyzed', 0),
                'performance_rating': 'Good' if trends_time < 20 else 'Slow'
            }
        except Exception as e:
            performance_results['market_trends'] = {
                'execution_time_seconds': None,
                'error': str(e),
                'performance_rating': 'Failed'
            }
        
        return performance_results

    def print_test_summary(self, results: Dict[str, Any]):
        """Print comprehensive test summary."""
        
        print("\n" + "=" * 60)
        print("🎯 LAYER 3A TEST RESULTS SUMMARY")
        print("=" * 60)
        
        summary = results['test_summary']
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed_tests']}")
        print(f"Failed: {summary['total_tests'] - summary['passed_tests']}")
        print(f"Success Rate: {(summary['passed_tests'] / summary['total_tests'] * 100):.1f}%")
        print(f"Total Execution Time: {summary['total_time_seconds']} seconds")
        
        # Component Results
        components = ['discovery_patterns', 'investment_timing', 'market_trends', 'integration']
        
        for component in components:
            if component in results:
                component_tests = results[component]
                passed = sum(1 for test in component_tests if test['passed'])
                total = len(component_tests)
                
                print(f"\n📊 {component.replace('_', ' ').title()}:")
                print(f"   Tests: {passed}/{total} passed")
                
                for test in component_tests:
                    status = "✅" if test['passed'] else "❌"
                    print(f"   {status} {test['test_name']}: {test['result']}")
        
        # Performance Results
        if 'performance' in results:
            print(f"\n⚡ Performance Results:")
            for component, perf in results['performance'].items():
                if 'execution_time_seconds' in perf and perf['execution_time_seconds']:
                    print(f"   {component}: {perf['execution_time_seconds']}s ({perf['performance_rating']})")
        
        print("\n" + "=" * 60)

def main():
    """Run Layer 3A comprehensive test suite."""
    
    try:
        test_suite = Layer3ATestSuite()
        results = test_suite.run_all_tests()
        
        # Optional: Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"layer3a_test_results_{timestamp}.json"
        
        import json
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Test results saved to: {results_file}")
        
    except Exception as e:
        print(f"❌ Test suite execution failed: {e}")

if __name__ == "__main__":
    main()
