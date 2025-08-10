#!/usr/bin/env python3
"""
Layer 2 Database Integration Script
==================================

Integrates all Layer 2 discoveries into the Supabase database:
- Government intelligence discoveries (ORNL, NREL, DOE)
- VC portfolio companies (BEV, EIP) 
- Source health and performance data
- Layer 2 session analytics

Converts JSON exports to normalized database entries using existing schema.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from supabase import create_client, Client
from schema_adapter import SchemaAwareDealInserter

# Load environment variables from .env file
def load_env_file():
    """Load environment variables from .env file."""
    env_path = '.env'
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    os.environ[key] = value

# Load environment variables
load_env_file()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Layer2DatabaseIntegrator:
    """Integrates Layer 2 discoveries with the Supabase database."""
    
    def __init__(self):
        self.supabase = self._init_supabase()
        if self.supabase:
            self.deal_inserter = SchemaAwareDealInserter(self.supabase)
        else:
            self.deal_inserter = None
            
        self.integration_stats = {
            'government_discoveries_processed': 0,
            'government_discoveries_inserted': 0,
            'vc_companies_processed': 0,
            'vc_companies_inserted': 0,
            'sources_updated': 0,
            'errors': []
        }
    
    def _init_supabase(self) -> Optional[Client]:
        """Initialize Supabase client."""
        try:
            url = os.getenv('SUPABASE_URL')
            key = os.getenv('SUPABASE_KEY')
            
            if not url or not key:
                logger.warning("Supabase credentials not found in environment variables")
                logger.info("Please set SUPABASE_URL and SUPABASE_KEY environment variables")
                return None
                
            return create_client(url, key)
        except Exception as e:
            logger.error(f"Failed to initialize Supabase: {e}")
            return None
    
    def integrate_all_layer2_data(self) -> Dict:
        """Integrate all Layer 2 data into database."""
        logger.info("🚀 Starting Layer 2 Database Integration...")
        
        if not self.supabase:
            logger.error("❌ Cannot proceed without Supabase connection")
            return self._generate_integration_report()
        
        # 1. Integrate Government Intelligence
        logger.info("🏛️ Integrating Government Intelligence...")
        self._integrate_government_discoveries()
        
        # 2. Integrate VC Portfolio Companies
        logger.info("💼 Integrating VC Portfolio Companies...")
        self._integrate_vc_portfolio_companies()
        
        # 3. Update Source Health Data
        logger.info("📊 Updating Source Health Data...")
        self._update_source_health_data()
        
        # 4. Create Data Sources Table (if needed)
        logger.info("🔧 Setting up data sources tracking...")
        self._setup_data_sources_table()
        
        # 5. Generate Integration Report
        report = self._generate_integration_report()
        
        # Save integration report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"layer2_database_integration_{timestamp}.json"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📁 Integration report saved to: {report_filename}")
        self._print_integration_summary(report)
        
        return report
    
    def _integrate_government_discoveries(self):
        """Integrate government intelligence discoveries into deals/companies tables."""
        try:
            # Find the latest government intelligence file
            gov_files = [f for f in os.listdir('.') if f.startswith('national_labs_intelligence_')]
            
            if not gov_files:
                logger.warning("No government intelligence files found")
                return
            
            latest_file = max(gov_files, key=lambda x: os.path.getmtime(x))
            logger.info(f"Loading government discoveries from: {latest_file}")
            
            with open(latest_file, 'r', encoding='utf-8') as f:
                discoveries = json.load(f)
            
            logger.info(f"Found {len(discoveries)} government discoveries to process")
            
            for discovery in discoveries:
                self.integration_stats['government_discoveries_processed'] += 1
                
                try:
                    # Extract key information
                    title = discovery.get('title', 'Government Research Discovery')
                    source = discovery.get('source', 'Government')
                    url = discovery.get('url', '')
                    content = discovery.get('content_preview', '')
                    companies_mentioned = discovery.get('companies_mentioned', [])
                    funding_amount = discovery.get('funding_amount')
                    tech_focus = discovery.get('technology_focus', [])
                    
                    # Determine if this should be a deal or just a company entry
                    if funding_amount or 'funding' in title.lower() or 'award' in title.lower():
                        # Treat as a funding deal
                        company_name = companies_mentioned[0] if companies_mentioned else f"{source} Research Project"
                        
                        deal_id = self.deal_inserter.insert_deal(
                            company_name=company_name,
                            source_url=url,
                            raw_text_content=content,
                            source_type='government_research',
                            source_name=source,
                            detected_funding_stage='Government Grant',
                            detected_amount=funding_amount,
                            detected_investors=[source],
                            detected_sector=tech_focus[0] if tech_focus else 'Climate Tech',
                            detected_country='United States',
                            has_ai_focus='quantum' in content.lower() or 'ai' in content.lower()
                        )
                        
                        if deal_id:
                            self.integration_stats['government_discoveries_inserted'] += 1
                            logger.info(f"✅ Inserted government deal: {title[:50]}...")
                        else:
                            self.integration_stats['errors'].append(f"Failed to insert deal: {title}")
                    
                    else:
                        # Treat as research/technology discovery
                        for company_name in companies_mentioned[:3]:  # Limit to first 3 companies
                            if len(company_name.strip()) > 3:  # Valid company name
                                deal_id = self.deal_inserter.insert_deal(
                                    company_name=company_name,
                                    source_url=url,
                                    raw_text_content=f"Government research discovery: {content}",
                                    source_type='government_research',
                                    source_name=source,
                                    detected_funding_stage='Research',
                                    detected_amount=None,
                                    detected_investors=[],
                                    detected_sector=tech_focus[0] if tech_focus else 'Climate Tech',
                                    detected_country='United States',
                                    has_ai_focus='quantum' in content.lower() or 'ai' in content.lower()
                                )
                                
                                if deal_id:
                                    self.integration_stats['government_discoveries_inserted'] += 1
                                    logger.info(f"✅ Inserted research discovery: {company_name}")
                
                except Exception as e:
                    error_msg = f"Error processing government discovery '{title}': {str(e)}"
                    self.integration_stats['errors'].append(error_msg)
                    logger.error(error_msg)
                    
        except Exception as e:
            error_msg = f"Error integrating government discoveries: {str(e)}"
            self.integration_stats['errors'].append(error_msg)
            logger.error(error_msg)
    
    def _integrate_vc_portfolio_companies(self):
        """Integrate VC portfolio companies into companies table."""
        try:
            # Find the latest VC portfolio file
            vc_files = [f for f in os.listdir('.') if f.startswith('vc_portfolio_discoveries_')]
            
            if not vc_files:
                logger.warning("No VC portfolio files found")
                return
            
            latest_file = max(vc_files, key=lambda x: os.path.getmtime(x))
            logger.info(f"Loading VC portfolio companies from: {latest_file}")
            
            with open(latest_file, 'r', encoding='utf-8') as f:
                portfolio_data = json.load(f)
            
            # Handle the actual data structure (array of companies)
            all_companies = []
            
            if isinstance(portfolio_data, list):
                # It's a flat list of companies
                all_companies = portfolio_data
            elif isinstance(portfolio_data, dict):
                # Check for nested structure
                if 'bev_companies' in portfolio_data:
                    for company in portfolio_data['bev_companies']:
                        company['vc_source'] = 'Breakthrough Energy Ventures'
                        all_companies.append(company)
                
                if 'eip_companies' in portfolio_data:
                    for company in portfolio_data['eip_companies']:
                        company['vc_source'] = 'Energy Impact Partners'
                        all_companies.append(company)
                        
                # If no nested structure, treat as single company
                if not all_companies and 'name' in portfolio_data:
                    all_companies = [portfolio_data]
            
            logger.info(f"Found {len(all_companies)} VC portfolio companies to process")
            
            for company in all_companies:
                self.integration_stats['vc_companies_processed'] += 1
                
                try:
                    company_name = company.get('name', 'Unknown Company')
                    description = company.get('description', '')
                    website = company.get('website', '')
                    vc_source = company.get('vc_source') or company.get('vc_firm', 'VC Portfolio')
                    sector = company.get('sector', 'Climate Tech')
                    
                    # Create a deal entry for VC portfolio tracking
                    deal_id = self.deal_inserter.insert_deal(
                        company_name=company_name,
                        source_url=website or f"https://{vc_source.lower().replace(' ', '')}.com",
                        raw_text_content=f"VC Portfolio Company ({vc_source}): {description}",
                        source_type='vc_portfolio',
                        source_name=vc_source,
                        detected_funding_stage=company.get('funding_stage') or 'Portfolio Company',
                        detected_amount=None,
                        detected_investors=[vc_source],
                        detected_sector=sector,
                        detected_country=company.get('headquarters') or 'United States',
                        has_ai_focus='ai' in description.lower() or 'artificial intelligence' in description.lower()
                    )
                    
                    if deal_id:
                        self.integration_stats['vc_companies_inserted'] += 1
                        if self.integration_stats['vc_companies_inserted'] % 10 == 0:
                            logger.info(f"✅ Processed {self.integration_stats['vc_companies_inserted']} VC companies...")
                    else:
                        self.integration_stats['errors'].append(f"Failed to insert VC company: {company_name}")
                
                except Exception as e:
                    error_msg = f"Error processing VC company '{company_name}': {str(e)}"
                    self.integration_stats['errors'].append(error_msg)
                    logger.error(error_msg)
                    
        except Exception as e:
            error_msg = f"Error integrating VC portfolio companies: {str(e)}"
            self.integration_stats['errors'].append(error_msg)
            logger.error(error_msg)
    
    def _update_source_health_data(self):
        """Update source health and performance data."""
        try:
            # Find the latest source intelligence file
            source_files = [f for f in os.listdir('.') if f.startswith('source_intelligence_')]
            
            if not source_files:
                logger.warning("No source intelligence files found")
                return
            
            latest_file = max(source_files, key=lambda x: os.path.getmtime(x))
            logger.info(f"Loading source intelligence from: {latest_file}")
            
            with open(latest_file, 'r', encoding='utf-8') as f:
                source_data = json.load(f)
            
            # For now, we'll store this as a comment or in a simple table
            # In a full implementation, we'd create a dedicated data_sources table
            logger.info(f"Source intelligence data loaded: {len(source_data.get('sources', {}))} sources")
            self.integration_stats['sources_updated'] = len(source_data.get('sources', {}))
            
        except Exception as e:
            error_msg = f"Error updating source health data: {str(e)}"
            self.integration_stats['errors'].append(error_msg)
            logger.error(error_msg)
    
    def _setup_data_sources_table(self):
        """Create data_sources table if it doesn't exist."""
        try:
            if not self.supabase:
                return
                
            # Check if data_sources table exists, create if not
            # This would typically be done via SQL migration
            logger.info("Data sources table setup would be handled via database migration")
            
        except Exception as e:
            error_msg = f"Error setting up data sources table: {str(e)}"
            self.integration_stats['errors'].append(error_msg)
            logger.error(error_msg)
    
    def _generate_integration_report(self) -> Dict:
        """Generate comprehensive integration report."""
        return {
            'integration_timestamp': datetime.now().isoformat(),
            'database_connection': self.supabase is not None,
            'statistics': self.integration_stats,
            'summary': {
                'total_items_processed': (
                    self.integration_stats['government_discoveries_processed'] + 
                    self.integration_stats['vc_companies_processed']
                ),
                'total_items_inserted': (
                    self.integration_stats['government_discoveries_inserted'] + 
                    self.integration_stats['vc_companies_inserted']
                ),
                'success_rate': self._calculate_success_rate(),
                'error_count': len(self.integration_stats['errors'])
            },
            'errors': self.integration_stats['errors'][:10],  # First 10 errors
            'recommendations': self._generate_recommendations()
        }
    
    def _calculate_success_rate(self) -> float:
        """Calculate overall success rate."""
        total_processed = (
            self.integration_stats['government_discoveries_processed'] + 
            self.integration_stats['vc_companies_processed']
        )
        total_inserted = (
            self.integration_stats['government_discoveries_inserted'] + 
            self.integration_stats['vc_companies_inserted']
        )
        
        if total_processed == 0:
            return 0.0
        
        return (total_inserted / total_processed) * 100
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on integration results."""
        recommendations = []
        
        success_rate = self._calculate_success_rate()
        
        if success_rate < 50:
            recommendations.append("Low success rate - check database schema compatibility")
        elif success_rate < 80:
            recommendations.append("Moderate success rate - review error patterns for improvements")
        else:
            recommendations.append("High success rate - integration working well")
        
        if len(self.integration_stats['errors']) > 10:
            recommendations.append("High error count - consider data validation improvements")
        
        if self.integration_stats['vc_companies_inserted'] > 100:
            recommendations.append("Large number of VC companies integrated - consider portfolio analysis features")
        
        if self.integration_stats['government_discoveries_inserted'] > 5:
            recommendations.append("Government discoveries integrated - enable early-stage opportunity tracking")
        
        return recommendations
    
    def _print_integration_summary(self, report: Dict):
        """Print integration summary to console."""
        stats = report['statistics']
        summary = report['summary']
        
        print(f"\n🎯 LAYER 2 DATABASE INTEGRATION COMPLETE")
        print(f"=" * 60)
        print(f"Integration Time: {report['integration_timestamp']}")
        print(f"Database Connected: {'✅' if report['database_connection'] else '❌'}")
        print()
        
        print(f"📊 INTEGRATION STATISTICS")
        print(f"  Government Discoveries: {stats['government_discoveries_inserted']}/{stats['government_discoveries_processed']} inserted")
        print(f"  VC Portfolio Companies: {stats['vc_companies_inserted']}/{stats['vc_companies_processed']} inserted")
        print(f"  Sources Updated: {stats['sources_updated']}")
        print(f"  Total Success Rate: {summary['success_rate']:.1f}%")
        print()
        
        if summary['error_count'] > 0:
            print(f"⚠️ ERRORS ENCOUNTERED: {summary['error_count']}")
            for i, error in enumerate(report['errors'][:3], 1):
                print(f"  {i}. {error}")
            if summary['error_count'] > 3:
                print(f"  ... and {summary['error_count'] - 3} more errors")
            print()
        
        print(f"💡 RECOMMENDATIONS")
        for rec in report['recommendations']:
            print(f"  • {rec}")
        print()
        
        if summary['total_items_inserted'] > 0:
            print(f"✅ SUCCESS: {summary['total_items_inserted']} items integrated into database!")
            print(f"Your Supabase dashboard now includes Layer 2 discoveries!")

def main():
    """Main execution function."""
    print("🚀 Layer 2 Database Integration Starting...")
    
    integrator = Layer2DatabaseIntegrator()
    
    if not integrator.supabase:
        print("\n❌ DATABASE CONNECTION REQUIRED")
        print("Please set environment variables:")
        print("  SUPABASE_URL=your_supabase_url")
        print("  SUPABASE_KEY=your_supabase_key")
        print("\nExample:")
        print("  $env:SUPABASE_URL='https://your-project.supabase.co'")
        print("  $env:SUPABASE_KEY='your-anon-key'")
        return
    
    # Run integration
    report = integrator.integrate_all_layer2_data()
    
    return report

if __name__ == "__main__":
    main()
