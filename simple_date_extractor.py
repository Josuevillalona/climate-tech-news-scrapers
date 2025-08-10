#!/usr/bin/env python3

import re
from datetime import datetime, timedelta
from typing import Optional

def extract_date_simple_robust(content: str, article_date: Optional[datetime] = None) -> Optional[str]:
    """
    Simple, high-success-rate date extraction using multiple fallback strategies.
    """
    
    if not content:
        return None
    
    content_lower = content.lower()
    
    # Strategy 1: Direct ISO/Standard date patterns (highest confidence)
    iso_patterns = [
        r'(\d{4})-(\d{1,2})-(\d{1,2})',  # 2025-01-22
        r'(\d{1,2})/(\d{1,2})/(\d{4})',  # 1/22/2025 or 01/22/2025
        r'(\d{1,2})-(\d{1,2})-(\d{4})',  # 1-22-2025
    ]
    
    print(f"   📅 Strategy 1: Looking for standard date formats...")
    
    for pattern in iso_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            try:
                if len(match[0]) == 4:  # YYYY-MM-DD format
                    year, month, day = match
                else:  # MM/DD/YYYY format
                    month, day, year = match
                
                # Basic validation
                year, month, day = int(year), int(month), int(day)
                if 2020 <= year <= 2025 and 1 <= month <= 12 and 1 <= day <= 31:
                    result = f"{year}-{month:02d}-{day:02d}"
                    print(f"   ✅ Found standard date: {result}")
                    return result
            except:
                continue
    
    # Strategy 2: Month name patterns (medium confidence)
    month_patterns = [
        r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2}),?\s*(\d{4})',
        r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+(\d{1,2}),?\s*(\d{4})',
        r'(\d{1,2})\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})',
    ]
    
    months_map = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
        'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12,
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    
    print(f"   📅 Strategy 2: Looking for month name patterns...")
    
    for pattern in month_patterns:
        matches = re.findall(pattern, content_lower)
        for match in matches:
            try:
                if match[0] in months_map:  # month first
                    month_name, day, year = match
                    month_num = months_map[month_name]
                else:  # day first
                    day, month_name, year = match
                    month_num = months_map[match[1]]
                
                year, day = int(year), int(day)
                if 2020 <= year <= 2025 and 1 <= month_num <= 12 and 1 <= day <= 31:
                    result = f"{year}-{month_num:02d}-{day:02d}"
                    print(f"   ✅ Found month name date: {result}")
                    return result
            except:
                continue
    
    # Strategy 3: URL-based date extraction (high confidence)
    print(f"   📅 Strategy 3: URL-based extraction (if article_date provided)...")
    if article_date:
        # If we have article date, use it as the announcement date
        result = article_date.strftime('%Y-%m-%d')
        print(f"   ✅ Using article publication date: {result}")
        return result
    
    # Strategy 4: Simple relative dates (with article context)
    reference_date = article_date if article_date else datetime.now()
    
    print(f"   📅 Strategy 4: Simple relative dates...")
    
    # Look for very clear patterns
    if 'yesterday' in content_lower:
        result = (reference_date - timedelta(days=1)).strftime('%Y-%m-%d')
        print(f"   ✅ Found 'yesterday': {result}")
        return result
    
    if 'today' in content_lower and 'announced today' in content_lower:
        result = reference_date.strftime('%Y-%m-%d')
        print(f"   ✅ Found 'announced today': {result}")
        return result
    
    # Strategy 5: Extract year and use article date for month/day
    print(f"   📅 Strategy 5: Year extraction with article date...")
    year_match = re.search(r'\b(202[0-5])\b', content)
    if year_match and article_date:
        year = int(year_match.group(1))
        # Use article month/day but with found year
        result = f"{year}-{article_date.month:02d}-{article_date.day:02d}"
        print(f"   ✅ Found year {year}, using article date for month/day: {result}")
        return result
    
    print(f"   ❌ No date patterns found with any strategy")
    return None

# Test the function
if __name__ == "__main__":
    # Test with various date formats
    test_cases = [
        "announced on January 22, 2025",
        "funding round closed 2025-01-22",
        "raised money on 1/22/2025",
        "deal announced yesterday",
        "announced Wednesday",  # This would need article_date context
        "in 2024 the company raised funds"
    ]
    
    for test in test_cases:
        print(f"\n🧪 Testing: '{test}'")
        result = extract_date_simple_robust(test)
        print(f"   Result: {result}")
