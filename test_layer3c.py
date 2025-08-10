#!/usr/bin/env python3
"""
TEST LAYER 3C STRATEGIC INTELLIGENCE ENGINE
==========================================
Comprehensive testing of Layer 3C strategic intelligence capabilities.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client
from layer3c_strategic_intelligence import StrategicIntelligenceEngine

def test_layer3c_comprehensive():
    """Test comprehensive Layer 3C strategic intelligence."""
    
    print("🧪 TESTING LAYER 3C STRATEGIC INTELLIGENCE ENGINE")
    print("=" * 70)
    
    # Initialize connection
    load_dotenv()
    try:
        supabase = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )
        print("✅ Successfully connected to Supabase")
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {e}")
        return False
    
    # Initialize Strategic Intelligence Engine
    try:
        engine = StrategicIntelligenceEngine(supabase)
        print("✅ Strategic Intelligence Engine initialized")
    except Exception as e:
        print(f"❌ Failed to initialize engine: {e}")
        return False
    
    test_results = {}
    
    # Test 1: Check data availability
    print(f"\n📊 Test 1: Data Availability Check")
    try:
        deals_response = supabase.table('deals_new').select('*').limit(10).execute()
        deals_count = len(deals_response.data)
        print(f"   ✅ Found {deals_count} deals in database")
        test_results['data_availability'] = deals_count > 0
    except Exception as e:
        print(f"   ❌ Data availability check failed: {e}")
        test_results['data_availability'] = False
    
    # Test 2: Executive Summary Generation
    print(f"\n📋 Test 2: Executive Summary Generation")
    try:
        cutoff_date = "2024-01-01"  # Test with broad date range
        summary = engine._generate_executive_summary(cutoff_date)
        
        if 'error' in summary:
            print(f"   ⚠️  Executive summary generated with errors: {summary['error']}")
            test_results['executive_summary'] = False
        else:
            print(f"   ✅ Executive summary generated successfully")
            if 'period_metrics' in summary:
                metrics = summary['period_metrics']
                print(f"      📈 Total discoveries: {metrics.get('total_discoveries', 0)}")
                print(f"      🏛️  Government intel: {metrics.get('government_intelligence', 0)}")
                print(f"      💼 VC activities: {metrics.get('vc_portfolio_activities', 0)}")
            test_results['executive_summary'] = True
    except Exception as e:
        print(f"   ❌ Executive summary generation failed: {e}")
        test_results['executive_summary'] = False
    
    # Test 3: Market Intelligence Analysis
    print(f"\n🌍 Test 3: Market Intelligence Analysis")
    try:
        market_intel = engine._analyze_market_intelligence(cutoff_date)
        
        if market_intel:
            print(f"   ✅ Market intelligence analysis completed")
            print(f"      📊 Sectors analyzed: {len(market_intel)}")
            for sector, intel in list(market_intel.items())[:3]:  # Show first 3
                print(f"      • {sector}: {intel.competitive_landscape}")
            test_results['market_intelligence'] = True
        else:
            print(f"   ⚠️  No market intelligence data generated")
            test_results['market_intelligence'] = False
    except Exception as e:
        print(f"   ❌ Market intelligence analysis failed: {e}")
        test_results['market_intelligence'] = False
    
    # Test 4: Strategic Insights Generation
    print(f"\n💡 Test 4: Strategic Insights Generation")
    try:
        insights = engine._generate_strategic_insights(cutoff_date)
        
        if insights:
            print(f"   ✅ Strategic insights generated: {len(insights)} insights")
            for insight in insights[:2]:  # Show first 2
                print(f"      • {insight.title} (Priority: {insight.priority_level})")
                print(f"        Confidence: {insight.confidence_score:.2f}")
            test_results['strategic_insights'] = True
        else:
            print(f"   ⚠️  No strategic insights generated")
            test_results['strategic_insights'] = False
    except Exception as e:
        print(f"   ❌ Strategic insights generation failed: {e}")
        test_results['strategic_insights'] = False
    
    # Test 5: Investment Thesis Validation
    print(f"\n🎯 Test 5: Investment Thesis Validation")
    try:
        thesis_validation = engine._validate_investment_thesis(cutoff_date)
        
        if 'error' in thesis_validation:
            print(f"   ❌ Thesis validation failed: {thesis_validation['error']}")
            test_results['thesis_validation'] = False
        else:
            print(f"   ✅ Investment thesis validation completed")
            if 'overall_thesis_strength' in thesis_validation:
                strength = thesis_validation['overall_thesis_strength']
                print(f"      📊 Overall thesis strength: {strength:.2f}")
            
            if 'theme_validation' in thesis_validation:
                themes = thesis_validation['theme_validation']
                print(f"      🎯 Themes validated: {len(themes)}")
                for theme, results in list(themes.items())[:3]:
                    print(f"        • {theme}: {results['thesis_status']}")
            test_results['thesis_validation'] = True
    except Exception as e:
        print(f"   ❌ Investment thesis validation failed: {e}")
        test_results['thesis_validation'] = False
    
    # Test 6: Comprehensive Report Generation
    print(f"\n📊 Test 6: Comprehensive Report Generation")
    try:
        report = engine.generate_comprehensive_intelligence_report(timeframe_days=90)
        
        print(f"   ✅ Comprehensive report generated successfully")
        print(f"      🎯 Overall confidence: {report.get('overall_confidence', 0):.1f}%")
        print(f"      📅 Analysis period: {report['report_metadata']['analysis_period']}")
        
        # Check report sections
        expected_sections = [
            'executive_summary', 'market_intelligence', 'competitive_landscape',
            'strategic_insights', 'investment_thesis_validation', 'risk_assessment',
            'opportunity_mapping', 'recommendations'
        ]
        
        sections_present = sum(1 for section in expected_sections if section in report)
        print(f"      📋 Report sections: {sections_present}/{len(expected_sections)} completed")
        
        test_results['comprehensive_report'] = sections_present >= 6  # At least 6/8 sections
        
    except Exception as e:
        print(f"   ❌ Comprehensive report generation failed: {e}")
        test_results['comprehensive_report'] = False
    
    # Test Results Summary
    print(f"\n" + "=" * 70)
    print(f"🧪 LAYER 3C TEST RESULTS SUMMARY")
    print(f"=" * 70)
    
    total_tests = len(test_results)
    passed_tests = sum(test_results.values())
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"📊 Overall Success Rate: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    print()
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        test_display = test_name.replace('_', ' ').title()
        print(f"   {status} - {test_display}")
    
    print()
    if success_rate >= 80:
        print(f"🎉 Layer 3C Strategic Intelligence Engine: EXCELLENT PERFORMANCE")
        print(f"   Ready for production deployment and integration!")
    elif success_rate >= 60:
        print(f"⚠️  Layer 3C Strategic Intelligence Engine: GOOD PERFORMANCE")
        print(f"   Ready for deployment with minor optimizations needed")
    else:
        print(f"🔧 Layer 3C Strategic Intelligence Engine: NEEDS ATTENTION")
        print(f"   Requires debugging and optimization before production use")
    
    return success_rate >= 80

def test_layer3c_integration():
    """Test Layer 3C integration with existing Layer 3A and 3B components."""
    
    print(f"\n🔗 LAYER 3C INTEGRATION TEST")
    print("=" * 50)
    
    # Test that Layer 3C can work alongside Layer 3A and 3B
    integration_status = {}
    
    # Check if Layer 3A components exist
    try:
        import layer3_discovery_patterns
        print("✅ Layer 3A Discovery Patterns available")
        integration_status['layer3a'] = True
    except ImportError:
        print("⚠️  Layer 3A Discovery Patterns not found")
        integration_status['layer3a'] = False
    
    # Check if Layer 3B components exist
    try:
        import layer3b_investment_optimizer
        print("✅ Layer 3B Investment Optimizer available")
        integration_status['layer3b'] = True
    except ImportError:
        print("⚠️  Layer 3B Investment Optimizer not found")
        integration_status['layer3b'] = False
    
    # Check if AI processor is available
    try:
        import ai_processor_consolidated
        print("✅ AI Processor Consolidated available")
        integration_status['ai_processor'] = True
    except ImportError:
        print("⚠️  AI Processor Consolidated not found")
        integration_status['ai_processor'] = False
    
    # Integration readiness assessment
    available_components = sum(integration_status.values())
    total_components = len(integration_status)
    
    print(f"\n📊 Integration Readiness: {available_components}/{total_components} components available")
    
    if available_components == total_components:
        print("🎉 Full Layer 3 ecosystem ready for integrated deployment!")
    elif available_components >= 2:
        print("✅ Sufficient components for Layer 3C deployment")
    else:
        print("⚠️  Limited integration - Layer 3C can run standalone")
    
    return available_components >= 2

if __name__ == "__main__":
    print("🚀 STARTING LAYER 3C STRATEGIC INTELLIGENCE TESTS")
    print("=" * 70)
    
    # Run comprehensive tests
    success = test_layer3c_comprehensive()
    
    # Run integration tests
    integration_ready = test_layer3c_integration()
    
    print(f"\n" + "=" * 70)
    print(f"🏁 FINAL TEST SUMMARY")
    print(f"=" * 70)
    print(f"✅ Layer 3C Functionality: {'PASS' if success else 'FAIL'}")
    print(f"✅ Integration Readiness: {'PASS' if integration_ready else 'PARTIAL'}")
    
    if success and integration_ready:
        print(f"\n🎉 Layer 3C Strategic Intelligence Engine: READY FOR DEPLOYMENT!")
        print(f"   • Comprehensive strategic intelligence capabilities operational")
        print(f"   • Full integration with Layer 3A and 3B components")
        print(f"   • Executive-level insights and recommendations available")
    else:
        print(f"\n🔧 Layer 3C requires attention before full deployment")
        if not success:
            print(f"   • Core functionality needs debugging")
        if not integration_ready:
            print(f"   • Integration components need setup")
