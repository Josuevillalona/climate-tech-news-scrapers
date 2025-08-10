#!/usr/bin/env python3
"""
LAYER 3: DISCOVERY PATTERN ANALYZER
====================================
Analyzes patterns in government research to predict commercialization timelines
and identify investment opportunities from Layer 2 intelligence.

Phase 3A.1: Discovery Pattern Analysis
- Research stage to funding timeline modeling
- Technology readiness level progression tracking  
- Government funding to VC interest correlation
- Market entry timing prediction algorithms
"""

import os
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dotenv import load_dotenv
from supabase import create_client, Client
import re
from dataclasses import dataclass
from collections import defaultdict
import json

# Load environment
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

@dataclass
class DiscoveryPattern:
    """Data class for discovery patterns."""
    technology_sector: str
    research_stage: str
    commercialization_timeline: int  # weeks
    government_agencies: List[str]
    confidence_score: float
    supporting_evidence: Dict[str, Any]

@dataclass
class CommercializationPrediction:
    """Data class for commercialization predictions."""
    company_id: str
    company_name: str
    predicted_funding_weeks: int
    confidence_score: float
    reasoning: List[str]
    trl_score: Optional[int]
    market_readiness: str

class DiscoveryPatternAnalyzer:
    """Analyzes government research patterns to predict commercialization timelines."""
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.patterns = {}
        self.government_to_vc_patterns = {}
        
        # Technology readiness level progression patterns
        self.trl_commercialization_weeks = {
            1: 520,  # Basic principles (10+ years)
            2: 416,  # Technology concept (8+ years)
            3: 312,  # Experimental proof (6+ years)
            4: 260,  # Technology validated (5+ years)
            5: 208,  # Technology validated in relevant environment (4+ years)
            6: 156,  # Technology demonstrated (3+ years)
            7: 104,  # System prototype demonstration (2+ years)
            8: 52,   # System complete and qualified (1+ year)
            9: 26    # Actual system proven (6+ months)
        }
        
        # Sector-specific commercialization patterns
        self.sector_patterns = {
            'energy_storage': {'avg_weeks': 156, 'variance': 52},
            'solar_energy': {'avg_weeks': 104, 'variance': 26},
            'carbon_capture': {'avg_weeks': 208, 'variance': 78},
            'hydrogen': {'avg_weeks': 130, 'variance': 39},
            'battery': {'avg_weeks': 104, 'variance': 26},
            'quantum': {'avg_weeks': 312, 'variance': 104},
            'fusion': {'avg_weeks': 520, 'variance': 156}
        }

    def analyze_government_patterns(self) -> Dict[str, DiscoveryPattern]:
        """Analyze patterns in government research data."""
        
        print("🔍 Analyzing government research patterns...")
        
        # Get government research data from Layer 2
        gov_data = self.supabase.table('deals_new').select(
            '*,companies(name)'
        ).eq('source_type', 'government_research').execute()
        
        if not gov_data.data:
            print("⚠️  No government research data found")
            return {}
        
        patterns = {}
        sector_analysis = defaultdict(list)
        
        for entry in gov_data.data:
            # Extract technology focus
            content = entry.get('raw_text_content', '')
            tech_sectors = self._extract_tech_sectors(content)
            
            # Extract TRL if mentioned
            trl = self._extract_trl(content)
            
            # Estimate commercialization timeline
            timeline = self._estimate_commercialization_timeline(content, tech_sectors, trl)
            
            # Build pattern
            for sector in tech_sectors:
                pattern = DiscoveryPattern(
                    technology_sector=sector,
                    research_stage=self._classify_research_stage(content),
                    commercialization_timeline=timeline,
                    government_agencies=self._extract_agencies(content),
                    confidence_score=self._calculate_pattern_confidence(content, trl),
                    supporting_evidence={
                        'trl': trl,
                        'content_keywords': self._extract_keywords(content),
                        'agency_count': len(self._extract_agencies(content)),
                        'source_url': entry.get('source_url', '')
                    }
                )
                
                sector_analysis[sector].append(pattern)
                
        # Generate sector-level patterns
        for sector, sector_patterns in sector_analysis.items():
            patterns[sector] = self._aggregate_sector_patterns(sector_patterns)
        
        print(f"✅ Analyzed {len(patterns)} technology sector patterns")
        self.patterns = patterns
        return patterns

    def predict_commercialization_timeline(self, company_id: str) -> Optional[CommercializationPrediction]:
        """Predict commercialization timeline for a specific company."""
        
        # Get company data
        company_data = self.supabase.table('deals_new').select(
            '*,companies(name)'
        ).eq('company_id', company_id).execute()
        
        if not company_data.data:
            return None
            
        entry = company_data.data[0]
        company_name = entry.get('companies', {}).get('name', 'Unknown')
        content = entry.get('raw_text_content', '')
        
        # Extract analysis factors
        tech_sectors = self._extract_tech_sectors(content)
        trl = self._extract_trl(content)
        research_stage = self._classify_research_stage(content)
        
        # Calculate prediction
        predicted_weeks = self._calculate_prediction(tech_sectors, trl, research_stage, content)
        confidence = self._calculate_prediction_confidence(tech_sectors, trl, content)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(tech_sectors, trl, research_stage, predicted_weeks)
        
        prediction = CommercializationPrediction(
            company_id=company_id,
            company_name=company_name,
            predicted_funding_weeks=predicted_weeks,
            confidence_score=confidence,
            reasoning=reasoning,
            trl_score=trl,
            market_readiness=self._assess_market_readiness(predicted_weeks)
        )
        
        return prediction

    def analyze_government_to_vc_correlation(self) -> Dict[str, Any]:
        """Analyze correlation between government research and VC portfolio companies."""
        
        print("🔍 Analyzing government research to VC correlation...")
        
        # Get both datasets
        gov_data = self.supabase.table('deals_new').select('*,companies(*)').eq('source_type', 'government_research').execute()
        vc_data = self.supabase.table('deals_new').select('*,companies(*)').eq('source_type', 'vc_portfolio').execute()
        
        if not gov_data.data or not vc_data.data:
            print("⚠️  Insufficient data for correlation analysis")
            return {}
        
        # Extract technology sectors from both sources
        gov_sectors = defaultdict(int)
        vc_sectors = defaultdict(int)
        
        for entry in gov_data.data:
            sectors = self._extract_tech_sectors(entry.get('raw_text_content', ''))
            for sector in sectors:
                gov_sectors[sector] += 1
        
        for entry in vc_data.data:
            sectors = self._extract_tech_sectors(entry.get('raw_text_content', ''))
            for sector in sectors:
                vc_sectors[sector] += 1
        
        # Calculate correlations
        correlations = {}
        all_sectors = set(list(gov_sectors.keys()) + list(vc_sectors.keys()))
        
        for sector in all_sectors:
            gov_count = gov_sectors.get(sector, 0)
            vc_count = vc_sectors.get(sector, 0)
            
            if gov_count > 0 and vc_count > 0:
                # Simple correlation based on relative interest
                correlation_strength = min(gov_count, vc_count) / max(gov_count, vc_count)
                
                correlations[sector] = {
                    'correlation_strength': correlation_strength,
                    'government_mentions': gov_count,
                    'vc_portfolio_mentions': vc_count,
                    'investment_signal': 'strong' if correlation_strength > 0.5 else 'moderate' if correlation_strength > 0.3 else 'weak'
                }
        
        print(f"✅ Analyzed correlations for {len(correlations)} technology sectors")
        self.government_to_vc_patterns = correlations
        return correlations

    # Helper methods for analysis
    
    def _extract_tech_sectors(self, content: str) -> List[str]:
        """Extract technology sectors from content."""
        sector_keywords = {
            'energy_storage': ['battery', 'storage', 'grid', 'lithium', 'energy storage'],
            'solar_energy': ['solar', 'photovoltaic', 'pv', 'solar panel'],
            'carbon_capture': ['carbon capture', 'carbon removal', 'ccus', 'co2 capture'],
            'hydrogen': ['hydrogen', 'electrolysis', 'fuel cell', 'h2'],
            'wind_energy': ['wind', 'wind energy', 'wind turbine'],
            'quantum': ['quantum', 'quantum computing', 'qubit'],
            'fusion': ['fusion', 'nuclear fusion', 'plasma'],
            'geothermal': ['geothermal', 'ground source'],
            'biofuel': ['biofuel', 'biomass', 'biogas'],
            'nuclear': ['nuclear', 'reactor', 'uranium']
        }
        
        content_lower = content.lower()
        detected_sectors = []
        
        for sector, keywords in sector_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                detected_sectors.append(sector)
        
        return detected_sectors if detected_sectors else ['general_cleantech']
    
    def _extract_trl(self, content: str) -> Optional[int]:
        """Extract Technology Readiness Level from content."""
        trl_patterns = [
            r'TRL\s*(\d+)', r'Technology Readiness Level\s*(\d+)',
            r'readiness level\s*(\d+)', r'maturity level\s*(\d+)'
        ]
        
        for pattern in trl_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                trl = int(match.group(1))
                if 1 <= trl <= 9:
                    return trl
        return None
    
    def _classify_research_stage(self, content: str) -> str:
        """Classify the research stage from content."""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['demonstration', 'pilot', 'prototype']):
            return 'demonstration'
        elif any(word in content_lower for word in ['development', 'testing', 'validation']):
            return 'development'
        elif any(word in content_lower for word in ['research', 'laboratory', 'experimental']):
            return 'research'
        else:
            return 'unknown'
    
    def _extract_agencies(self, content: str) -> List[str]:
        """Extract government agencies from content."""
        agencies = [
            'DOE', 'Department of Energy', 'ORNL', 'Oak Ridge',
            'NREL', 'National Renewable Energy', 'ARPA-E', 'NSF',
            'Lawrence Berkeley', 'Sandia', 'Argonne'
        ]
        
        found_agencies = []
        content_lower = content.lower()
        
        for agency in agencies:
            if agency.lower() in content_lower:
                found_agencies.append(agency)
        
        return found_agencies
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract key technology keywords from content."""
        tech_keywords = [
            'innovation', 'breakthrough', 'novel', 'advanced', 'cutting-edge',
            'efficient', 'sustainable', 'renewable', 'clean', 'green',
            'commercialization', 'deployment', 'scale', 'manufacturing'
        ]
        
        found_keywords = []
        content_lower = content.lower()
        
        for keyword in tech_keywords:
            if keyword in content_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def _estimate_commercialization_timeline(self, content: str, sectors: List[str], trl: Optional[int]) -> int:
        """Estimate commercialization timeline in weeks."""
        
        # Base estimate on TRL if available
        if trl:
            base_weeks = self.trl_commercialization_weeks.get(trl, 156)
        else:
            # Use sector-based estimates
            sector_weeks = []
            for sector in sectors:
                if sector in self.sector_patterns:
                    sector_weeks.append(self.sector_patterns[sector]['avg_weeks'])
            
            base_weeks = int(np.mean(sector_weeks)) if sector_weeks else 156
        
        # Adjust based on research stage
        stage = self._classify_research_stage(content)
        if stage == 'demonstration':
            base_weeks = int(base_weeks * 0.6)  # Closer to market
        elif stage == 'development':
            base_weeks = int(base_weeks * 0.8)  # Development stage
        # Research stage uses base estimate
        
        return max(12, base_weeks)  # Minimum 3 months
    
    def _calculate_pattern_confidence(self, content: str, trl: Optional[int]) -> float:
        """Calculate confidence score for pattern analysis."""
        confidence = 0.5  # Base confidence
        
        # TRL provides high confidence
        if trl:
            confidence += 0.3
        
        # Multiple agencies increase confidence
        agencies = self._extract_agencies(content)
        confidence += min(0.2, len(agencies) * 0.1)
        
        # Technical keywords increase confidence
        keywords = self._extract_keywords(content)
        confidence += min(0.2, len(keywords) * 0.02)
        
        return min(1.0, confidence)
    
    def _aggregate_sector_patterns(self, patterns: List[DiscoveryPattern]) -> DiscoveryPattern:
        """Aggregate multiple patterns into a sector-level pattern."""
        if not patterns:
            return None
        
        # Calculate averages
        avg_timeline = int(np.mean([p.commercialization_timeline for p in patterns]))
        avg_confidence = np.mean([p.confidence_score for p in patterns])
        
        # Aggregate agencies
        all_agencies = []
        for p in patterns:
            all_agencies.extend(p.government_agencies)
        unique_agencies = list(set(all_agencies))
        
        # Most common research stage
        stages = [p.research_stage for p in patterns]
        most_common_stage = max(set(stages), key=stages.count)
        
        return DiscoveryPattern(
            technology_sector=patterns[0].technology_sector,
            research_stage=most_common_stage,
            commercialization_timeline=avg_timeline,
            government_agencies=unique_agencies,
            confidence_score=avg_confidence,
            supporting_evidence={
                'pattern_count': len(patterns),
                'timeline_variance': int(np.std([p.commercialization_timeline for p in patterns])),
                'confidence_range': [min(p.confidence_score for p in patterns), max(p.confidence_score for p in patterns)]
            }
        )
    
    def _calculate_prediction(self, sectors: List[str], trl: Optional[int], stage: str, content: str) -> int:
        """Calculate commercialization prediction in weeks."""
        return self._estimate_commercialization_timeline(content, sectors, trl)
    
    def _calculate_prediction_confidence(self, sectors: List[str], trl: Optional[int], content: str) -> float:
        """Calculate prediction confidence score."""
        return self._calculate_pattern_confidence(content, trl)
    
    def _generate_reasoning(self, sectors: List[str], trl: Optional[int], stage: str, weeks: int) -> List[str]:
        """Generate reasoning for the prediction."""
        reasoning = []
        
        if trl:
            reasoning.append(f"TRL {trl} indicates {self.trl_commercialization_weeks[trl]//52:.1f} year typical timeline")
        
        if sectors:
            reasoning.append(f"Technology sectors: {', '.join(sectors)}")
        
        reasoning.append(f"Research stage: {stage}")
        reasoning.append(f"Predicted commercialization: {weeks//52:.1f} years ({weeks} weeks)")
        
        return reasoning
    
    def _assess_market_readiness(self, weeks: int) -> str:
        """Assess market readiness based on timeline."""
        if weeks <= 52:
            return 'market_ready'
        elif weeks <= 104:
            return 'near_term'
        elif weeks <= 208:
            return 'medium_term'
        else:
            return 'long_term'

def main():
    """Main execution for Discovery Pattern Analysis."""
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        analyzer = DiscoveryPatternAnalyzer(supabase)
        
        print("🚀 LAYER 3: DISCOVERY PATTERN ANALYZER")
        print("=" * 60)
        
        # Analyze government research patterns
        patterns = analyzer.analyze_government_patterns()
        
        # Analyze government to VC correlations
        correlations = analyzer.analyze_government_to_vc_correlation()
        
        # Generate sample predictions
        print("\n🔮 Sample Commercialization Predictions:")
        print("-" * 40)
        
        # Get a few government research companies for prediction
        gov_companies = supabase.table('deals_new').select('company_id,companies(name)').eq('source_type', 'government_research').limit(3).execute()
        
        for company in gov_companies.data:
            prediction = analyzer.predict_commercialization_timeline(company['company_id'])
            if prediction:
                print(f"📊 {prediction.company_name}")
                print(f"   Timeline: {prediction.predicted_funding_weeks//52:.1f} years")
                print(f"   Confidence: {prediction.confidence_score:.2f}")
                print(f"   Market Readiness: {prediction.market_readiness}")
                print(f"   TRL: {prediction.trl_score or 'Unknown'}")
                print()
        
        print("✅ Discovery Pattern Analysis Complete!")
        
    except Exception as e:
        print(f"❌ Error in discovery pattern analysis: {e}")

if __name__ == "__main__":
    main()
