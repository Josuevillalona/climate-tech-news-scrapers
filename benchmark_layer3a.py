#!/usr/bin/env python3
"""
LAYER 3A: PERFORMANCE BENCHMARK
==============================
Benchmarks Layer 3A system performance and generates performance report.
"""

import os
import time
import statistics
from typing import Dict, List
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

def benchmark_layer3a():
    """Benchmark Layer 3A performance."""
    
    print("⚡ LAYER 3A: PERFORMANCE BENCHMARK")
    print("=" * 50)
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Initialize components
    discovery_analyzer = DiscoveryPatternAnalyzer(supabase)
    timing_predictor = InvestmentTimingPredictor(supabase)
    trend_forecaster = MarketTrendForecaster(supabase)
    
    benchmarks = {}
    
    # Benchmark 1: Discovery Pattern Analysis
    print("\n🔍 Benchmarking Discovery Pattern Analysis...")
    times = []
    for i in range(3):
        start = time.time()
        # Get sample company
        companies = supabase.table('deals_new').select('company_id').eq('source_type', 'government_research').limit(1).execute()
        if companies.data:
            prediction = discovery_analyzer.predict_commercialization_timeline(companies.data[0]['company_id'])
        times.append(time.time() - start)
    
    benchmarks['discovery_analysis'] = {
        'avg_time': round(statistics.mean(times), 2),
        'min_time': round(min(times), 2),
        'max_time': round(max(times), 2),
        'rating': 'Excellent' if statistics.mean(times) < 2 else 'Good' if statistics.mean(times) < 5 else 'Slow'
    }
    
    # Benchmark 2: Investment Timing Analysis
    print("⏰ Benchmarking Investment Timing Analysis...")
    times = []
    for i in range(3):
        start = time.time()
        opportunities = timing_predictor.batch_analyze_investment_opportunities()
        times.append(time.time() - start)
    
    benchmarks['investment_timing'] = {
        'avg_time': round(statistics.mean(times), 2),
        'min_time': round(min(times), 2),
        'max_time': round(max(times), 2),
        'opportunities_per_second': round(10 / statistics.mean(times), 2),  # Assuming 10 companies analyzed
        'rating': 'Excellent' if statistics.mean(times) < 5 else 'Good' if statistics.mean(times) < 10 else 'Slow'
    }
    
    # Benchmark 3: Market Trend Forecasting
    print("📈 Benchmarking Market Trend Forecasting...")
    times = []
    for i in range(3):
        start = time.time()
        outlook = trend_forecaster.generate_market_outlook(6)
        times.append(time.time() - start)
    
    benchmarks['market_forecasting'] = {
        'avg_time': round(statistics.mean(times), 2),
        'min_time': round(min(times), 2),
        'max_time': round(max(times), 2),
        'sectors_per_second': round(12 / statistics.mean(times), 2),  # Assuming 12 sectors analyzed
        'rating': 'Excellent' if statistics.mean(times) < 8 else 'Good' if statistics.mean(times) < 15 else 'Slow'
    }
    
    # Benchmark 4: End-to-End Analysis
    print("🚀 Benchmarking End-to-End Analysis...")
    start = time.time()
    
    # Simulate full analysis workflow
    companies = supabase.table('deals_new').select('company_id').limit(3).execute()
    for company in companies.data:
        # Discovery analysis
        discovery_prediction = discovery_analyzer.predict_commercialization_timeline(company['company_id'])
        
        # Investment timing
        timing_prediction = timing_predictor.predict_optimal_timing(company['company_id'])
    
    # Market trends
    outlook = trend_forecaster.generate_market_outlook(6)
    
    end_to_end_time = time.time() - start
    
    benchmarks['end_to_end'] = {
        'total_time': round(end_to_end_time, 2),
        'companies_analyzed': len(companies.data),
        'time_per_company': round(end_to_end_time / len(companies.data), 2),
        'rating': 'Excellent' if end_to_end_time < 15 else 'Good' if end_to_end_time < 30 else 'Slow'
    }
    
    # Print benchmark results
    print("\n" + "=" * 50)
    print("📊 PERFORMANCE BENCHMARK RESULTS")
    print("=" * 50)
    
    for test_name, results in benchmarks.items():
        print(f"\n⚡ {test_name.replace('_', ' ').title()}:")
        for metric, value in results.items():
            if metric == 'rating':
                emoji = "🟢" if value == 'Excellent' else "🟡" if value == 'Good' else "🔴"
                print(f"   {emoji} {metric.title()}: {value}")
            else:
                print(f"   📊 {metric.replace('_', ' ').title()}: {value}")
    
    # Overall performance rating
    ratings = [b['rating'] for b in benchmarks.values()]
    excellent_count = ratings.count('Excellent')
    good_count = ratings.count('Good')
    
    if excellent_count >= 3:
        overall_rating = "🟢 EXCELLENT"
    elif excellent_count + good_count >= 3:
        overall_rating = "🟡 GOOD"
    else:
        overall_rating = "🔴 NEEDS OPTIMIZATION"
    
    print(f"\n🎯 OVERALL PERFORMANCE: {overall_rating}")
    
    # Performance recommendations
    print(f"\n💡 PERFORMANCE INSIGHTS:")
    slow_components = [name for name, data in benchmarks.items() if data['rating'] == 'Slow']
    if slow_components:
        print(f"   ⚠️  Consider optimizing: {', '.join(slow_components)}")
    else:
        print(f"   ✅ All components performing well!")
    
    if benchmarks['end_to_end']['time_per_company'] < 5:
        print(f"   🚀 Ready for production scale")
    else:
        print(f"   📈 Consider caching for production")
    
    return benchmarks

if __name__ == "__main__":
    benchmark_layer3a()
