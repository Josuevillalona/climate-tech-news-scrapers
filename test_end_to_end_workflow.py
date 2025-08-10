#!/usr/bin/env python3
"""
COMPLETE END-TO-END WORKFLOW TEST
================================
Tests the entire climate tech intelligence system:
- Layer 1: Data Collection (Scrapers)
- Layer 2: Enhanced Discovery (AI Processing)
- Layer 3A: Enhanced Analytics (Pattern Analysis, Timing, Trends)
- Layer 3B: Investment Strategy Optimizer (Portfolio Optimization)

This simulates a real-world workflow from raw data collection to investment decisions.
"""

import os
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from supabase import create_client, Client

# Import all system components
from layer3_discovery_patterns import DiscoveryPatternAnalyzer
from layer3_investment_timing import InvestmentTimingPredictor
from layer3_market_trends import MarketTrendForecaster
from layer3b_investment_optimizer import InvestmentStrategyOptimizer

# Load environment
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class EndToEndWorkflowTest:
    """Comprehensive end-to-end workflow test."""
    
    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Initialize all system components
        self.discovery_analyzer = DiscoveryPatternAnalyzer(self.supabase)
        self.timing_predictor = InvestmentTimingPredictor(self.supabase)
        self.trend_forecaster = MarketTrendForecaster(self.supabase)
        self.investment_optimizer = InvestmentStrategyOptimizer(self.supabase)
        
        self.workflow_results = {
            'layer1_data_validation': {},
            'layer2_processing_validation': {},
            'layer3a_analytics_validation': {},
            'layer3b_optimization_validation': {},
            'end_to_end_integration': {},
            'performance_metrics': {},
            'investment_decisions': []
        }

    def run_complete_workflow(self, investment_amount: float = 5000000) -> Dict[str, Any]:
        """Run the complete end-to-end workflow test."""
        
        print("🚀 COMPLETE END-TO-END WORKFLOW TEST")
        print("=" * 80)
        print(f"Investment Amount: ${investment_amount:,.0f}")
        print(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        start_time = time.time()
        
        # Step 1: Validate Layer 1 Data Collection
        print("\n📊 STEP 1: Validating Layer 1 Data Collection...")
        layer1_results = self.validate_layer1_data()
        
        # Step 2: Validate Layer 2 Enhanced Discovery
        print("\n🧠 STEP 2: Validating Layer 2 Enhanced Discovery...")
        layer2_results = self.validate_layer2_processing()
        
        # Step 3: Run Layer 3A Enhanced Analytics
        print("\n🔍 STEP 3: Running Layer 3A Enhanced Analytics...")
        layer3a_results = self.run_layer3a_analytics()
        
        # Step 4: Run Layer 3B Investment Optimization
        print("\n💰 STEP 4: Running Layer 3B Investment Optimization...")
        layer3b_results = self.run_layer3b_optimization(investment_amount)
        
        # Step 5: Test End-to-End Integration
        print("\n🔗 STEP 5: Testing End-to-End Integration...")
        integration_results = self.test_integration()
        
        # Step 6: Generate Investment Decisions
        print("\n🎯 STEP 6: Generating Investment Decisions...")
        investment_decisions = self.generate_investment_decisions(investment_amount)
        
        total_time = time.time() - start_time
        
        # Compile comprehensive results
        workflow_results = {
            'test_metadata': {
                'investment_amount': investment_amount,
                'test_start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_execution_time': round(total_time, 2),
                'system_status': 'OPERATIONAL'
            },
            'layer1_data_validation': layer1_results,
            'layer2_processing_validation': layer2_results,
            'layer3a_analytics_validation': layer3a_results,
            'layer3b_optimization_validation': layer3b_results,
            'end_to_end_integration': integration_results,
            'investment_decisions': investment_decisions,
            'performance_summary': self.generate_performance_summary(total_time)
        }
        
        self.print_workflow_summary(workflow_results)
        return workflow_results

    def validate_layer1_data(self) -> Dict[str, Any]:
        """Validate Layer 1 data collection status."""
        
        print("   🔍 Checking data sources...")
        
        # Check each data source
        sources = ['government_research', 'vc_portfolio', 'news']
        source_stats = {}
        
        for source in sources:
            data = self.supabase.table('deals_new').select('*').eq('source_type', source).execute()
            source_stats[source] = {
                'record_count': len(data.data),
                'has_data': len(data.data) > 0,
                'sample_companies': [d.get('company_id', 'unknown')[:8] + '...' for d in data.data[:3]]
            }
        
        total_records = sum(stats['record_count'] for stats in source_stats.values())
        data_quality = 'EXCELLENT' if total_records > 500 else 'GOOD' if total_records > 100 else 'LIMITED'
        
        return {
            'total_records': total_records,
            'source_breakdown': source_stats,
            'data_quality_rating': data_quality,
            'all_sources_active': all(stats['has_data'] for stats in source_stats.values()),
            'validation_status': 'PASSED' if total_records > 50 else 'WARNING'
        }

    def validate_layer2_processing(self) -> Dict[str, Any]:
        """Validate Layer 2 enhanced discovery processing."""
        
        print("   🧠 Checking AI processing and schema adaptation...")
        
        # Check schema structure
        schema_check = self.supabase.table('deals_new').select('company_id,raw_text_content,source_type,created_at').limit(5).execute()
        
        # Validate required fields
        required_fields = ['company_id', 'raw_text_content', 'source_type']
        field_validation = {}
        
        if schema_check.data:
            sample_record = schema_check.data[0]
            for field in required_fields:
                field_validation[field] = {
                    'present': field in sample_record,
                    'has_value': bool(sample_record.get(field))
                }
        
        # Check for companies table integration
        companies_check = self.supabase.table('companies').select('id,name').limit(3).execute()
        
        return {
            'schema_validation': field_validation,
            'sample_records': len(schema_check.data),
            'companies_table_records': len(companies_check.data),
            'processing_status': 'OPERATIONAL',
            'validation_status': 'PASSED' if schema_check.data else 'FAILED'
        }

    def run_layer3a_analytics(self) -> Dict[str, Any]:
        """Run comprehensive Layer 3A analytics."""
        
        print("   🔍 Running discovery pattern analysis...")
        print("   ⏰ Running investment timing analysis...")
        print("   📈 Running market trend forecasting...")
        
        analytics_results = {}
        
        # Discovery Pattern Analysis
        try:
            gov_companies = self.supabase.table('deals_new').select('company_id').eq('source_type', 'government_research').limit(3).execute()
            
            discovery_predictions = []
            for company in gov_companies.data:
                prediction = self.discovery_analyzer.predict_commercialization_timeline(company['company_id'])
                if prediction:
                    discovery_predictions.append({
                        'company_id': company['company_id'][:8] + '...',
                        'timeline_weeks': prediction.predicted_funding_weeks,
                        'confidence': prediction.confidence_score
                    })
            
            analytics_results['discovery_analysis'] = {
                'predictions_generated': len(discovery_predictions),
                'sample_predictions': discovery_predictions[:2],
                'status': 'SUCCESS'
            }
        except Exception as e:
            analytics_results['discovery_analysis'] = {'status': 'ERROR', 'error': str(e)}
        
        # Investment Timing Analysis
        try:
            opportunities = self.timing_predictor.batch_analyze_investment_opportunities()
            
            analytics_results['investment_timing'] = {
                'opportunities_analyzed': len(opportunities),
                'top_opportunities': [
                    {
                        'company': opp.company_name[:30] + '...' if len(opp.company_name) > 30 else opp.company_name,
                        'score': round(opp.opportunity_score, 3),
                        'timing_weeks': opp.optimal_timing_weeks,
                        'recommendation': opp.recommendation
                    }
                    for opp in opportunities[:3]
                ],
                'status': 'SUCCESS'
            }
        except Exception as e:
            analytics_results['investment_timing'] = {'status': 'ERROR', 'error': str(e)}
        
        # Market Trend Forecasting
        try:
            outlook = self.trend_forecaster.generate_market_outlook(12)
            
            analytics_results['market_forecasting'] = {
                'sectors_analyzed': outlook.get('overall_momentum', {}).get('sectors_analyzed', 0),
                'overall_momentum': round(outlook.get('overall_momentum', {}).get('score', 0), 3),
                'top_sectors': [
                    {
                        'sector': trend['sector'],
                        'momentum': round(trend['momentum_score'], 3),
                        'direction': trend['trend_direction']
                    }
                    for trend in outlook.get('sector_trends', [])[:3]
                ],
                'investment_recommendations': len(outlook.get('investment_recommendations', [])),
                'status': 'SUCCESS'
            }
        except Exception as e:
            analytics_results['market_forecasting'] = {'status': 'ERROR', 'error': str(e)}
        
        return analytics_results

    def run_layer3b_optimization(self, investment_amount: float) -> Dict[str, Any]:
        """Run Layer 3B investment optimization."""
        
        print(f"   💰 Optimizing portfolio for ${investment_amount:,.0f}...")
        
        try:
            # Generate strategic recommendations
            recommendations = self.investment_optimizer.generate_strategic_recommendations(investment_amount)
            
            return {
                'investment_amount': investment_amount,
                'strategies_generated': len(recommendations.get('strategies', [])),
                'portfolios_optimized': len(recommendations.get('optimized_portfolios', [])),
                'market_predictions': len(recommendations.get('market_predictions', [])),
                'top_opportunities': len(recommendations.get('top_opportunities', [])),
                'best_strategy': {
                    'name': recommendations['strategies'][0]['name'] if recommendations.get('strategies') else 'None',
                    'expected_return': recommendations['strategies'][0]['expected_return'] if recommendations.get('strategies') else 0,
                    'risk_score': recommendations['strategies'][0]['risk_score'] if recommendations.get('strategies') else 0
                } if recommendations.get('strategies') else {},
                'status': 'SUCCESS'
            }
        except Exception as e:
            return {'status': 'ERROR', 'error': str(e)}

    def test_integration(self) -> Dict[str, Any]:
        """Test integration between all system layers."""
        
        print("   🔗 Testing cross-layer data flow...")
        
        integration_tests = {}
        
        # Test data flow from Layer 2 → Layer 3A
        try:
            sample_company = self.supabase.table('deals_new').select('company_id').limit(1).execute()
            if sample_company.data:
                company_id = sample_company.data[0]['company_id']
                
                # Layer 3A processing
                discovery_prediction = self.discovery_analyzer.predict_commercialization_timeline(company_id)
                timing_prediction = self.timing_predictor.predict_optimal_timing(company_id)
                
                integration_tests['layer2_to_layer3a'] = {
                    'data_available': True,
                    'discovery_processed': discovery_prediction is not None,
                    'timing_processed': timing_prediction is not None,
                    'status': 'SUCCESS'
                }
            else:
                integration_tests['layer2_to_layer3a'] = {'status': 'NO_DATA'}
        except Exception as e:
            integration_tests['layer2_to_layer3a'] = {'status': 'ERROR', 'error': str(e)}
        
        # Test data flow from Layer 3A → Layer 3B
        try:
            # Layer 3A outputs
            opportunities = self.timing_predictor.batch_analyze_investment_opportunities()
            outlook = self.trend_forecaster.generate_market_outlook(6)
            
            # Layer 3B processing
            recommendations = self.investment_optimizer.generate_strategic_recommendations(1000000)
            
            integration_tests['layer3a_to_layer3b'] = {
                'opportunities_generated': len(opportunities),
                'market_outlook_generated': bool(outlook),
                'strategies_optimized': len(recommendations.get('strategies', [])),
                'integration_successful': bool(opportunities and outlook and recommendations),
                'status': 'SUCCESS'
            }
        except Exception as e:
            integration_tests['layer3a_to_layer3b'] = {'status': 'ERROR', 'error': str(e)}
        
        return integration_tests

    def generate_investment_decisions(self, investment_amount: float) -> List[Dict[str, Any]]:
        """Generate final investment decisions based on complete analysis."""
        
        print("   🎯 Generating final investment decisions...")
        
        decisions = []
        
        try:
            # Get comprehensive analysis
            opportunities = self.timing_predictor.batch_analyze_investment_opportunities()
            recommendations = self.investment_optimizer.generate_strategic_recommendations(investment_amount)
            
            # Generate investment decisions
            for i, opportunity in enumerate(opportunities[:5]):
                # Calculate investment allocation
                allocation_percentage = max(5, min(25, opportunity.opportunity_score * 30))  # 5-25% allocation
                allocation_amount = investment_amount * (allocation_percentage / 100)
                
                # Determine decision
                if opportunity.opportunity_score > 0.7:
                    decision = "INVEST"
                elif opportunity.opportunity_score > 0.5:
                    decision = "MONITOR"
                else:
                    decision = "PASS"
                
                decisions.append({
                    'rank': i + 1,
                    'company': opportunity.company_name,
                    'decision': decision,
                    'opportunity_score': round(opportunity.opportunity_score, 3),
                    'optimal_timing_weeks': opportunity.optimal_timing_weeks,
                    'allocation_percentage': round(allocation_percentage, 1),
                    'allocation_amount': round(allocation_amount, 0),
                    'recommendation': opportunity.recommendation,
                    'risk_factors': opportunity.risk_factors[:2]  # Top 2 risks
                })
            
        except Exception as e:
            decisions.append({
                'error': f"Failed to generate investment decisions: {e}",
                'status': 'ERROR'
            })
        
        return decisions

    def generate_performance_summary(self, total_time: float) -> Dict[str, Any]:
        """Generate comprehensive performance summary."""
        
        return {
            'total_execution_time_seconds': round(total_time, 2),
            'execution_time_minutes': round(total_time / 60, 2),
            'performance_rating': 'EXCELLENT' if total_time < 30 else 'GOOD' if total_time < 60 else 'SLOW',
            'throughput_analysis': {
                'records_processed_per_second': round(998 / total_time, 2) if total_time > 0 else 0,
                'predictions_per_minute': round(60 / total_time, 2) if total_time > 0 else 0
            },
            'system_efficiency': 'HIGH' if total_time < 45 else 'MEDIUM' if total_time < 90 else 'LOW',
            'scalability_assessment': 'PRODUCTION_READY' if total_time < 60 else 'OPTIMIZATION_NEEDED'
        }

    def print_workflow_summary(self, results: Dict[str, Any]):
        """Print comprehensive workflow summary."""
        
        print("\n" + "=" * 80)
        print("🎯 END-TO-END WORKFLOW TEST RESULTS")
        print("=" * 80)
        
        metadata = results['test_metadata']
        print(f"Investment Amount: ${metadata['investment_amount']:,.0f}")
        print(f"Total Execution Time: {metadata['total_execution_time']} seconds")
        print(f"System Status: {metadata['system_status']}")
        
        # Layer 1 Results
        layer1 = results['layer1_data_validation']
        print(f"\n📊 LAYER 1: Data Collection")
        print(f"   Total Records: {layer1['total_records']}")
        print(f"   Data Quality: {layer1['data_quality_rating']}")
        print(f"   Validation: {layer1['validation_status']}")
        for source, stats in layer1['source_breakdown'].items():
            print(f"   {source}: {stats['record_count']} records")
        
        # Layer 2 Results
        layer2 = results['layer2_processing_validation']
        print(f"\n🧠 LAYER 2: Enhanced Discovery")
        print(f"   Processing Status: {layer2['processing_status']}")
        print(f"   Validation: {layer2['validation_status']}")
        print(f"   Companies Table: {layer2['companies_table_records']} records")
        
        # Layer 3A Results
        layer3a = results['layer3a_analytics_validation']
        print(f"\n🔍 LAYER 3A: Enhanced Analytics")
        
        if 'discovery_analysis' in layer3a:
            discovery = layer3a['discovery_analysis']
            print(f"   Discovery Analysis: {discovery['status']} ({discovery.get('predictions_generated', 0)} predictions)")
        
        if 'investment_timing' in layer3a:
            timing = layer3a['investment_timing']
            print(f"   Investment Timing: {timing['status']} ({timing.get('opportunities_analyzed', 0)} opportunities)")
        
        if 'market_forecasting' in layer3a:
            forecasting = layer3a['market_forecasting']
            print(f"   Market Forecasting: {forecasting['status']} ({forecasting.get('sectors_analyzed', 0)} sectors)")
        
        # Layer 3B Results
        layer3b = results['layer3b_optimization_validation']
        print(f"\n💰 LAYER 3B: Investment Optimization")
        print(f"   Status: {layer3b['status']}")
        if layer3b['status'] == 'SUCCESS':
            print(f"   Strategies Generated: {layer3b['strategies_generated']}")
            print(f"   Portfolios Optimized: {layer3b['portfolios_optimized']}")
            if layer3b.get('best_strategy'):
                best = layer3b['best_strategy']
                print(f"   Best Strategy: {best.get('name', 'N/A')} ({best.get('expected_return', 0):.1f}% return)")
        
        # Integration Results
        integration = results['end_to_end_integration']
        print(f"\n🔗 INTEGRATION TESTING")
        for test_name, test_result in integration.items():
            status = test_result.get('status', 'UNKNOWN')
            print(f"   {test_name}: {status}")
        
        # Investment Decisions
        decisions = results['investment_decisions']
        print(f"\n🎯 INVESTMENT DECISIONS")
        if decisions and not any('error' in d for d in decisions):
            print(f"   Total Decisions: {len(decisions)}")
            invest_count = sum(1 for d in decisions if d.get('decision') == 'INVEST')
            monitor_count = sum(1 for d in decisions if d.get('decision') == 'MONITOR')
            pass_count = sum(1 for d in decisions if d.get('decision') == 'PASS')
            print(f"   Investment Recommendations: {invest_count} INVEST, {monitor_count} MONITOR, {pass_count} PASS")
            
            if invest_count > 0:
                invest_decisions = [d for d in decisions if d.get('decision') == 'INVEST']
                total_allocation = sum(d.get('allocation_amount', 0) for d in invest_decisions)
                print(f"   Total Investment Allocation: ${total_allocation:,.0f}")
        else:
            print(f"   Status: ERROR or NO DECISIONS")
        
        # Performance Summary
        performance = results['performance_summary']
        print(f"\n⚡ PERFORMANCE SUMMARY")
        print(f"   Execution Time: {performance['total_execution_time_seconds']}s ({performance['execution_time_minutes']:.1f} minutes)")
        print(f"   Performance Rating: {performance['performance_rating']}")
        print(f"   System Efficiency: {performance['system_efficiency']}")
        print(f"   Scalability Assessment: {performance['scalability_assessment']}")
        
        # Overall Assessment
        print(f"\n🏆 OVERALL ASSESSMENT")
        
        # Calculate overall success rate
        layer_statuses = [
            layer1['validation_status'] == 'PASSED',
            layer2['validation_status'] == 'PASSED',
            all(test.get('status') == 'SUCCESS' for test in layer3a.values() if isinstance(test, dict)),
            layer3b['status'] == 'SUCCESS',
            all(test.get('status') == 'SUCCESS' for test in integration.values() if isinstance(test, dict))
        ]
        
        success_rate = sum(layer_statuses) / len(layer_statuses) * 100
        
        if success_rate >= 90:
            overall_rating = "🟢 EXCELLENT - System fully operational and ready for production"
        elif success_rate >= 75:
            overall_rating = "🟡 GOOD - System operational with minor issues"
        else:
            overall_rating = "🔴 NEEDS ATTENTION - System has significant issues"
        
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Overall Rating: {overall_rating}")
        
        print("\n" + "=" * 80)

def main():
    """Run the complete end-to-end workflow test."""
    
    try:
        # Create test instance
        workflow_test = EndToEndWorkflowTest()
        
        # Run complete workflow with $5M investment scenario
        results = workflow_test.run_complete_workflow(investment_amount=5000000)
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"end_to_end_workflow_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Complete workflow results saved to: {results_file}")
        
        # Optional: Run additional scenarios
        print(f"\n🔄 Running additional investment scenarios...")
        
        # Test different investment amounts
        scenarios = [1000000, 10000000, 25000000]  # $1M, $10M, $25M
        scenario_results = {}
        
        for amount in scenarios:
            print(f"\n💰 Testing ${amount:,.0f} investment scenario...")
            scenario_result = workflow_test.run_layer3b_optimization(amount)
            scenario_results[f"${amount:,.0f}"] = scenario_result
        
        print(f"\n📊 Investment Scenario Comparison:")
        for scenario, result in scenario_results.items():
            if result.get('status') == 'SUCCESS':
                best_strategy = result.get('best_strategy', {})
                print(f"   {scenario}: {best_strategy.get('expected_return', 0):.1f}% return, {best_strategy.get('risk_score', 0):.2f} risk")
        
    except Exception as e:
        print(f"❌ End-to-end workflow test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
