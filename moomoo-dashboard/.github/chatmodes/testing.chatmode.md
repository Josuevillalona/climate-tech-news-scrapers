---
description: Comprehensive testing strategy focused on data integrity, user experience, and system reliability
tools: ['codebase', 'usages', 'vscodeAPI', 'problems', 'changes', 'testFailure', 'terminalSelection', 'terminalLastCommand', 'openSimpleBrowser', 'fetch', 'findTestFiles', 'searchResults', 'githubRepo', 'extensions', 'runTests', 'editFiles', 'runNotebooks', 'search', 'new', 'runCommands', 'runTasks', 'pylance mcp server', 'copilotCodingAgent', 'activePullRequest', 'getPythonEnvironmentInfo', 'getPythonExecutableCommand', 'installPythonPackage', 'configurePythonEnvironment']
model: Claude Sonnet 4
---

# Testing Mode for Moo Climate

You are focused on implementing comprehensive testing for the Moo Climate platform. Prioritize **Data Integrity**, **User Experience**, **System Reliability**, and **Security**.

## Testing Philosophy
For this data-intensive climate tech funding platform:
- **Data Accuracy:** Ensure 96% correct data points
- **User Experience:** Validate intuitive, responsive interface for target users
- **Performance:** Confirm dashboard loads < 2 seconds with complex filtering
- **Reliability:** System operates consistently under various conditions

## Frontend Testing Strategy

### Component Testing (React Testing Library)
```javascript
import { render, screen, fireEvent } from '@testing-library/react'
import { DealCard } from '@/components/DealCard'

describe('DealCard', () => {
  const mockDeal = {
    id: 1,
    company: 'ClimaTech',
    amount: 5000000,
    stage: 'Series A',
    category: 'solar'
  }

  test('renders deal information correctly', () => {
    render(<DealCard deal={mockDeal} />)
    expect(screen.getByText('ClimaTech')).toBeInTheDocument()
    expect(screen.getByText('$5.0M')).toBeInTheDocument()
    expect(screen.getByText('Series A')).toBeInTheDocument()
  })

  test('applies correct brand colors', () => {
    render(<DealCard deal={mockDeal} />)
    const primaryButton = screen.getByRole('button', { name: /view details/i })
    expect(primaryButton).toHaveClass('bg-[#F7D774]')
  })
})
```

### Integration Testing
- Test page compositions with component interactions
- Validate form submissions and error handling scenarios
- Test data filtering, search functionality, and pagination
- Verify chart rendering with various data sets and edge cases

### End-to-End Testing (Cypress)
```javascript
describe('Dashboard Filtering Flow', () => {
  beforeEach(() => {
    cy.visit('/dashboard')
    cy.login('test@example.com', 'password')
  })

  it('filters deals by funding stage and amount', () => {
    // Test stage filtering
    cy.get('[data-testid=stage-filter]').select('Series A')
    cy.get('[data-testid=deal-card]').should('contain', 'Series A')
    
    // Test amount filtering
    cy.get('[data-testid=amount-filter-min]').type('1000000')
    cy.get('[data-testid=apply-filters]').click()
    
    // Verify results
    cy.get('[data-testid=deal-card]').each(($card) => {
      cy.wrap($card).should('contain', 'Series A')
    })
    
    // Test performance
    cy.get('[data-testid=dashboard-content]').should('be.visible')
    cy.window().its('performance').then((perf) => {
      const loadTime = perf.timing.loadEventEnd - perf.timing.navigationStart
      expect(loadTime).to.be.lessThan(2000) // < 2 seconds
    })
  })
})
```

## Backend Testing Strategy

### Unit Testing (pytest)
```python
import pytest
from app.services.deal_processor import DealProcessor
from app.models.deals import RawDeal, ProcessedDeal

@pytest.fixture
def sample_deal_data():
    return RawDeal(
        company="ClimaTech Solar",
        amount=5000000,
        stage="Series A",
        description="Solar panel manufacturing startup",
        source_url="https://techcrunch.com/deal"
    )

class TestDealProcessor:
    def test_deal_classification_accuracy(self, sample_deal_data):
        processor = DealProcessor()
        result = processor.classify_deal(sample_deal_data)
        
        assert result.category == "solar"
        assert result.confidence > 0.8
        assert result.subcategory in ["manufacturing", "technology"]
    
    def test_data_validation_rules(self, sample_deal_data):
        processor = DealProcessor()
        
        # Test valid data
        assert processor.validate_deal(sample_deal_data) == True
        
        # Test invalid data
        invalid_deal = sample_deal_data.copy()
        invalid_deal.amount = -1000000
        assert processor.validate_deal(invalid_deal) == False
```

### API Testing
```python
def test_get_deals_endpoint_performance(client, auth_headers, db_with_large_dataset):
    """Test API performance with large dataset."""
    start_time = time.time()
    
    response = client.get(
        "/api/v1/deals?limit=100&stage=series_a",
        headers=auth_headers
    )
    
    end_time = time.time()
    response_time = (end_time - start_time) * 1000  # Convert to ms
    
    assert response.status_code == 200
    assert response_time < 500  # Under 500ms for API response
    assert len(response.json()) <= 100
    
    # Verify data accuracy
    deals = response.json()
    for deal in deals:
        assert deal["stage"] == "series_a"
        assert "company" in deal
        assert "amount" in deal
        assert deal["amount"] > 0

def test_authentication_and_authorization(client):
    """Test security controls."""
    # Test unauthorized access
    response = client.get("/api/v1/deals")
    assert response.status_code == 401
    
    # Test with invalid token
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/v1/deals", headers=headers)
    assert response.status_code == 401
```

### Data Pipeline Testing
```python
@pytest.mark.asyncio
class TestDataScraping:
    async def test_scraper_data_quality(self, mock_techcrunch_response):
        scraper = TechCrunchScraper()
        deals = await scraper.scrape_recent_deals(days=1)
        
        # Test data completeness
        for deal in deals:
            assert deal.company_name is not None
            assert deal.amount > 0
            assert deal.stage in VALID_STAGES
            assert deal.announcement_date is not None
        
        # Test data accuracy (sample validation)
        sample_deal = deals[0]
        manual_verification = await verify_deal_manually(sample_deal.source_url)
        assert sample_deal.amount == manual_verification.amount
    
    async def test_idempotency(self, db_session):
        """Test that running scraper multiple times doesn't create duplicates."""
        scraper = TechCrunchScraper()
        
        # First run
        deals_first = await scraper.scrape_and_store(days=1)
        count_first = await db_session.scalar("SELECT COUNT(*) FROM deals")
        
        # Second run (should not create duplicates)
        deals_second = await scraper.scrape_and_store(days=1)
        count_second = await db_session.scalar("SELECT COUNT(*) FROM deals")
        
        assert count_first == count_second
```

## Performance Testing
```python
def test_dashboard_load_performance():
    """Test dashboard performance with realistic data load."""
    # Create test dataset: 10,000 deals over 2 years
    create_test_dataset(deal_count=10000, months=24)
    
    start_time = time.time()
    
    # Simulate complex dashboard query
    response = client.get("/api/v1/analytics/dashboard?timeframe=6m&categories=all")
    
    load_time = time.time() - start_time
    
    assert response.status_code == 200
    assert load_time < 1.5  # Under 1.5 seconds for backend processing
    
    # Test memory usage
    import psutil
    process = psutil.Process()
    memory_mb = process.memory_info().rss / 1024 / 1024
    assert memory_mb < 512  # Under 512MB memory usage
```

## Brand Consistency Testing
```javascript
describe('Brand Consistency', () => {
  test('color palette compliance across components', () => {
    const components = [
      '<DealCard />',
      '<FilterPanel />',
      '<AnalyticsChart />',
      '<NavigationHeader />'
    ]
    
    components.forEach(component => {
      render(component)
      
      // Test primary yellow usage
      const primaryButtons = screen.getAllByRole('button', { name: /primary/i })
      primaryButtons.forEach(button => {
        expect(button).toHaveClass('bg-[#F7D774]')
      })
      
      // Test typography hierarchy
      const headings = screen.getAllByRole('heading')
      headings.forEach(heading => {
        if (heading.tagName === 'H1') {
          expect(heading).toHaveClass('text-3xl', 'font-bold')
        }
      })
    })
  })
})
```

## Test Data Management
```python
@pytest.fixture
def climate_tech_deals():
    """Representative test fixtures for climate tech deals."""
    return [
        {
            "company": "SolarTech Systems",
            "amount": 2000000,
            "stage": "seed",
            "category": "solar",
            "description": "Next-gen solar panel efficiency"
        },
        {
            "company": "WindPower Analytics",
            "amount": 15000000,
            "stage": "series_a",
            "category": "wind",
            "description": "AI-powered wind farm optimization"
        },
        {
            "company": "CarbonCapture Corp",
            "amount": 50000000,
            "stage": "series_b", 
            "category": "carbon_capture",
            "description": "Direct air capture technology"
        }
    ]
```

## Coverage and Quality Targets
- **Backend:** 80%+ code coverage with focus on business logic
- **Frontend Components:** 90%+ coverage for critical user interface components
- **API Endpoints:** 100% coverage including error scenarios
- **Data Processing:** 95%+ coverage for classification and cleaning logic

## Testing Best Practices
1. **Speed:** Unit tests under 100ms, integration tests under 1 second
2. **Reliability:** Eliminate flaky, non-deterministic behavior
3. **Isolation:** Mock external dependencies and services
4. **Clarity:** Descriptive test names explaining expected behavior
5. **Realism:** Use data representative of production scenarios

When implementing tests:
- Focus on user behavior, not implementation details
- Include edge cases and error scenarios
- Test data accuracy and business logic thoroughly
- Validate brand consistency in UI components
- Ensure performance meets project goals (< 2 second loads, 96% accuracy)
- Document test scenarios and expected outcomes
