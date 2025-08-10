#!/usr/bin/env python3
"""
Source Intelligence Manager
===========================

Layer 2 infrastructure for managing data source health, reliability, and duplicate detection.
Critical for maintaining high-quality climate tech intelligence pipeline.

Features:
- Source health monitoring
- Duplicate detection across sources
- Source priority scoring
- Content freshness tracking
- Data quality metrics
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Set
import logging
from dataclasses import dataclass
from collections import defaultdict
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DataSource:
    """Represents a data source with health metrics."""
    name: str
    url: str
    source_type: str  # 'news', 'government_funding', 'vc_portfolio', 'national_lab_research'
    last_successful_scrape: Optional[datetime] = None
    last_attempt: Optional[datetime] = None
    success_rate: float = 100.0
    total_attempts: int = 0
    successful_attempts: int = 0
    priority_score: int = 75  # 0-100
    is_active: bool = True
    avg_articles_per_day: float = 0.0
    unique_content_ratio: float = 100.0  # Percentage of non-duplicate content

@dataclass
class ContentFingerprint:
    """Represents a content fingerprint for duplicate detection."""
    source: str
    title_hash: str
    content_hash: str
    url_hash: str
    discovery_date: datetime
    companies_mentioned: List[str]
    funding_amount: Optional[str]

class SourceIntelligenceManager:
    """Manages source reliability, health, and duplicate detection."""
    
    def __init__(self):
        self.sources: Dict[str, DataSource] = {}
        self.content_fingerprints: List[ContentFingerprint] = []
        self.duplicate_clusters: Dict[str, List[ContentFingerprint]] = defaultdict(list)
        self.load_source_registry()
        
    def register_source(self, name: str, url: str, source_type: str, priority_score: int = 75):
        """Register a new data source."""
        if name not in self.sources:
            self.sources[name] = DataSource(
                name=name,
                url=url,
                source_type=source_type,
                priority_score=priority_score
            )
            logger.info(f"Registered new source: {name}")
        
    def record_scrape_attempt(self, source_name: str, success: bool, articles_found: int = 0):
        """Record a scraping attempt for source health tracking."""
        if source_name not in self.sources:
            logger.warning(f"Unknown source: {source_name}")
            return
            
        source = self.sources[source_name]
        source.last_attempt = datetime.now()
        source.total_attempts += 1
        
        if success:
            source.last_successful_scrape = datetime.now()
            source.successful_attempts += 1
            
            # Update average articles per day
            if source.total_attempts > 1:
                days_active = (datetime.now() - source.last_successful_scrape).days or 1
                source.avg_articles_per_day = (source.avg_articles_per_day + articles_found) / 2
        
        # Recalculate success rate
        source.success_rate = (source.successful_attempts / source.total_attempts) * 100
        
        # Update priority score based on performance
        self._update_priority_score(source_name)
        
        logger.info(f"Source {source_name}: Success rate {source.success_rate:.1f}%, Articles: {articles_found}")
    
    def process_discoveries(self, discoveries: List[Dict], source_name: str) -> List[Dict]:
        """Process discoveries for duplicate detection and quality scoring."""
        if not discoveries:
            return []
            
        # Create fingerprints
        new_fingerprints = []
        for discovery in discoveries:
            fingerprint = self._create_fingerprint(discovery, source_name)
            new_fingerprints.append(fingerprint)
            
        # Detect duplicates
        unique_discoveries = []
        duplicate_count = 0
        
        for i, discovery in enumerate(discoveries):
            fingerprint = new_fingerprints[i]
            
            if not self._is_duplicate(fingerprint):
                # Add to content database
                self.content_fingerprints.append(fingerprint)
                unique_discoveries.append(discovery)
            else:
                duplicate_count += 1
                logger.info(f"Duplicate detected: {discovery['title'][:50]}...")
        
        # Update source uniqueness ratio
        if source_name in self.sources:
            total_articles = len(discoveries)
            unique_ratio = ((total_articles - duplicate_count) / total_articles * 100) if total_articles > 0 else 100
            source = self.sources[source_name]
            source.unique_content_ratio = (source.unique_content_ratio + unique_ratio) / 2
        
        logger.info(f"Processed {len(discoveries)} discoveries from {source_name}: {len(unique_discoveries)} unique, {duplicate_count} duplicates")
        
        return unique_discoveries
    
    def get_source_health_report(self) -> Dict:
        """Generate comprehensive source health report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_sources': len(self.sources),
            'active_sources': len([s for s in self.sources.values() if s.is_active]),
            'sources': {},
            'summary': {
                'avg_success_rate': 0,
                'total_content_pieces': len(self.content_fingerprints),
                'detected_duplicates': len(self.duplicate_clusters),
                'top_performing_sources': [],
                'underperforming_sources': []
            }
        }
        
        success_rates = []
        
        for name, source in self.sources.items():
            source_report = {
                'name': source.name,
                'url': source.url,
                'type': source.source_type,
                'success_rate': source.success_rate,
                'priority_score': source.priority_score,
                'is_active': source.is_active,
                'total_attempts': source.total_attempts,
                'successful_attempts': source.successful_attempts,
                'avg_articles_per_day': source.avg_articles_per_day,
                'unique_content_ratio': source.unique_content_ratio,
                'last_successful_scrape': source.last_successful_scrape.isoformat() if source.last_successful_scrape else None,
                'health_status': self._get_health_status(source)
            }
            
            report['sources'][name] = source_report
            success_rates.append(source.success_rate)
        
        # Calculate summary statistics
        if success_rates:
            report['summary']['avg_success_rate'] = sum(success_rates) / len(success_rates)
            
        # Identify top and underperforming sources
        sorted_sources = sorted(self.sources.items(), key=lambda x: x[1].priority_score, reverse=True)
        report['summary']['top_performing_sources'] = [name for name, _ in sorted_sources[:3]]
        report['summary']['underperforming_sources'] = [
            name for name, source in sorted_sources 
            if source.success_rate < 50 or source.priority_score < 40
        ]
        
        return report
    
    def get_priority_source_list(self) -> List[str]:
        """Get list of sources sorted by priority for optimal scraping order."""
        active_sources = [(name, source) for name, source in self.sources.items() if source.is_active]
        
        # Sort by priority score, then by success rate
        sorted_sources = sorted(
            active_sources, 
            key=lambda x: (x[1].priority_score, x[1].success_rate),
            reverse=True
        )
        
        return [name for name, _ in sorted_sources]
    
    def detect_content_clusters(self) -> Dict[str, List[Dict]]:
        """Detect clusters of similar content across sources."""
        clusters = defaultdict(list)
        
        # Group by similar title hashes
        title_groups = defaultdict(list)
        for fp in self.content_fingerprints:
            # Use first 8 characters of hash for loose grouping
            title_prefix = fp.title_hash[:8]
            title_groups[title_prefix].append(fp)
        
        # Find clusters with multiple sources
        for prefix, fingerprints in title_groups.items():
            if len(fingerprints) > 1:
                # Check if they're actually similar
                similar_fps = self._find_similar_fingerprints(fingerprints)
                if len(similar_fps) > 1:
                    cluster_key = f"cluster_{prefix}"
                    clusters[cluster_key] = [
                        {
                            'source': fp.source,
                            'title_hash': fp.title_hash,
                            'discovery_date': fp.discovery_date.isoformat(),
                            'companies': fp.companies_mentioned
                        }
                        for fp in similar_fps
                    ]
        
        return dict(clusters)
    
    def save_intelligence_data(self, filename: str = None):
        """Save source intelligence data to file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"source_intelligence_{timestamp}.json"
        
        data = {
            'sources': {
                name: {
                    'name': source.name,
                    'url': source.url,
                    'source_type': source.source_type,
                    'priority_score': source.priority_score,
                    'success_rate': source.success_rate,
                    'total_attempts': source.total_attempts,
                    'successful_attempts': source.successful_attempts,
                    'avg_articles_per_day': source.avg_articles_per_day,
                    'unique_content_ratio': source.unique_content_ratio,
                    'is_active': source.is_active,
                    'last_successful_scrape': source.last_successful_scrape.isoformat() if source.last_successful_scrape else None
                }
                for name, source in self.sources.items()
            },
            'content_fingerprints_count': len(self.content_fingerprints),
            'duplicate_clusters_count': len(self.duplicate_clusters),
            'last_updated': datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
        logger.info(f"Source intelligence data saved to {filename}")
        return filename
    
    def load_source_registry(self):
        """Load default source registry."""
        # Register known climate tech sources
        default_sources = [
            # News Sources
            ('TechCrunch Climate', 'https://techcrunch.com', 'news', 90),
            ('Climate Insider', 'https://climateinsider.com', 'news', 85),
            ('CTVC', 'https://www.ctvc.co', 'news', 80),
            ('Axios Energy', 'https://axios.com', 'news', 85),
            ('Greentech Media', 'https://greentechmedia.com', 'news', 75),
            ('Climate Capital', 'https://climatecapital.co', 'news', 70),
            ('Energy Central', 'https://energycentral.com', 'news', 65),
            
            # Government Sources
            ('ARPA-E', 'https://arpa-e.energy.gov', 'government_funding', 95),
            ('DOE Newsroom', 'https://energy.gov/news', 'government_funding', 90),
            ('NREL', 'https://nrel.gov/news', 'national_lab_research', 85),
            ('ORNL', 'https://ornl.gov/news', 'national_lab_research', 85),
            
            # VC Portfolio Sources
            ('Breakthrough Energy Ventures', 'https://breakthroughenergy.org', 'vc_portfolio', 95),
            ('Energy Impact Partners', 'https://energyimpactpartners.com', 'vc_portfolio', 90),
        ]
        
        for name, url, source_type, priority in default_sources:
            self.register_source(name, url, source_type, priority)
            
        logger.info(f"Loaded {len(default_sources)} default sources")
    
    def _create_fingerprint(self, discovery: Dict, source_name: str) -> ContentFingerprint:
        """Create content fingerprint for duplicate detection."""
        title = discovery.get('title', '').lower().strip()
        content = discovery.get('content_preview', '').lower().strip()
        url = discovery.get('url', '').strip()
        
        # Normalize text for better matching
        title_normalized = re.sub(r'[^\w\s]', '', title)
        content_normalized = re.sub(r'[^\w\s]', '', content[:200])  # First 200 chars
        
        return ContentFingerprint(
            source=source_name,
            title_hash=hashlib.md5(title_normalized.encode()).hexdigest(),
            content_hash=hashlib.md5(content_normalized.encode()).hexdigest(),
            url_hash=hashlib.md5(url.encode()).hexdigest(),
            discovery_date=datetime.now(),
            companies_mentioned=discovery.get('companies_mentioned', []),
            funding_amount=discovery.get('funding_amount')
        )
    
    def _is_duplicate(self, fingerprint: ContentFingerprint) -> bool:
        """Check if content is a duplicate of existing content."""
        # Check exact matches first
        for existing_fp in self.content_fingerprints:
            # Same URL = definitely duplicate
            if fingerprint.url_hash == existing_fp.url_hash:
                return True
                
            # Same title and similar content = likely duplicate
            if (fingerprint.title_hash == existing_fp.title_hash and 
                fingerprint.content_hash == existing_fp.content_hash):
                return True
                
            # Same companies and funding amount within 7 days = possible duplicate
            if (fingerprint.companies_mentioned and existing_fp.companies_mentioned and
                set(fingerprint.companies_mentioned) == set(existing_fp.companies_mentioned) and
                fingerprint.funding_amount == existing_fp.funding_amount and
                abs((fingerprint.discovery_date - existing_fp.discovery_date).days) <= 7):
                return True
        
        return False
    
    def _find_similar_fingerprints(self, fingerprints: List[ContentFingerprint]) -> List[ContentFingerprint]:
        """Find fingerprints that are actually similar (not just hash collisions)."""
        # For simplicity, return fingerprints with matching title hashes
        # In production, this could use more sophisticated similarity algorithms
        if len(fingerprints) < 2:
            return fingerprints
            
        # Group by exact title hash
        title_groups = defaultdict(list)
        for fp in fingerprints:
            title_groups[fp.title_hash].append(fp)
        
        # Return the largest group
        largest_group = max(title_groups.values(), key=len)
        return largest_group if len(largest_group) > 1 else []
    
    def _update_priority_score(self, source_name: str):
        """Update source priority score based on performance metrics."""
        source = self.sources[source_name]
        
        # Base score from success rate
        score = source.success_rate
        
        # Bonus for high content volume
        if source.avg_articles_per_day > 5:
            score += 10
        elif source.avg_articles_per_day > 2:
            score += 5
            
        # Bonus for unique content
        if source.unique_content_ratio > 90:
            score += 10
        elif source.unique_content_ratio > 70:
            score += 5
            
        # Penalty for government sources (they're slower but valuable)
        if source.source_type == 'government_funding':
            score += 15  # Bonus for strategic value
        elif source.source_type == 'national_lab_research':
            score += 10
            
        # Ensure score stays within bounds
        source.priority_score = max(0, min(100, int(score)))
    
    def _get_health_status(self, source: DataSource) -> str:
        """Get human-readable health status."""
        if not source.is_active:
            return "INACTIVE"
        elif source.success_rate > 80 and source.priority_score > 70:
            return "EXCELLENT"
        elif source.success_rate > 60 and source.priority_score > 50:
            return "GOOD"
        elif source.success_rate > 40:
            return "FAIR"
        else:
            return "POOR"

def main():
    """Test the Source Intelligence Manager."""
    logger.info("Testing Source Intelligence Manager...")
    
    # Initialize manager
    manager = SourceIntelligenceManager()
    
    # Test some mock scraping attempts
    test_sources = ['TechCrunch Climate', 'ORNL', 'ARPA-E']
    
    for source in test_sources:
        # Simulate successful scrape
        manager.record_scrape_attempt(source, success=True, articles_found=5)
        # Simulate some failed attempts
        manager.record_scrape_attempt(source, success=False)
        manager.record_scrape_attempt(source, success=True, articles_found=3)
    
    # Generate health report
    health_report = manager.get_source_health_report()
    
    # Get priority list
    priority_sources = manager.get_priority_source_list()
    
    # Save intelligence data
    filename = manager.save_intelligence_data()
    
    # Print summary
    print(f"\n🔍 SOURCE INTELLIGENCE SUMMARY")
    print(f"=" * 50)
    print(f"Total Sources: {health_report['total_sources']}")
    print(f"Active Sources: {health_report['active_sources']}")
    print(f"Average Success Rate: {health_report['summary']['avg_success_rate']:.1f}%")
    print(f"Total Content Pieces: {health_report['summary']['total_content_pieces']}")
    
    print(f"\n🏆 TOP PRIORITY SOURCES:")
    for i, source in enumerate(priority_sources[:5], 1):
        source_info = manager.sources[source]
        print(f"{i}. {source} ({source_info.source_type}) - Priority: {source_info.priority_score}")
    
    print(f"\n📊 HEALTH STATUS:")
    for name, source_data in health_report['sources'].items():
        status = source_data['health_status']
        success_rate = source_data['success_rate']
        print(f"  {name}: {status} ({success_rate:.1f}% success)")
    
    print(f"\n💾 Intelligence data saved to: {filename}")

if __name__ == "__main__":
    main()
