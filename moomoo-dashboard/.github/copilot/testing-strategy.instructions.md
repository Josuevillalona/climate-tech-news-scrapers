---
applyTo: ["test", "testing", "jest", "cypress", "pytest"]
description: Comprehensive testing strategy for data integrity, UX, and reliability
---

# Testing Strategy

## Testing Philosophy
Prioritize **Data Integrity**, **User Experience**, **System Reliability**, and **Security** for this data-intensive climate tech platform.

## Frontend Testing Stack

### Component Testing (React Testing Library)
```javascript
// Component test example
import { render, screen } from '@testing-library/react'
import { DealCard } from '@/components/DealCard'

test('renders deal information correctly', () => {
  const mockDeal = {
    company: 'ClimaTech',
    amount: 5000000,
    stage: 'Series A'
  }
  
  render(<DealCard deal={mockDeal} />)
  expect(screen.getByText('ClimaTech')).toBeInTheDocument()
  expect(screen.getByText('$5.0M')).toBeInTheDocument()
})
```

### Integration Testing
- Test page compositions with component interactions
- Validate form submissions and error handling
- Test data filtering and search functionality
- Verify chart rendering with various data sets

### End-to-End Testing (Cypress)
```javascript
// E2E test example
describe('Dashboard Flow', () => {
  it('filters deals by funding stage', () => {
    cy.visit('/dashboard')
    cy.get('[data-testid=stage-filter]').select('Series A')
    cy.get('[data-testid=deal-card]').should('contain', 'Series A')
  })
})
```

## Backend Testing Stack

### Unit Testing (pytest)
```python
# Unit test example
import pytest
from app.services.deal_processor import DealProcessor

@pytest.fixture
def sample_deal_data():
    return {
        "company": "ClimaTech",
        "amount": 5000000,
        "stage": "Series A"
    }

def test_deal_classification(sample_deal_data):
    processor = DealProcessor()
    result = processor.classify_deal(sample_deal_data)
    assert result.category == "renewable_energy"
    assert result.confidence > 0.8
```

### API Testing
```python
# API test example
def test_get_deals_endpoint(client, auth_headers):
    response = client.get("/api/v1/deals", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert "company" in response.json()[0]
```

### Data Pipeline Testing
- Test scraper modules independently with mock data
- Validate data transformation and cleaning logic
- Test NLP classification accuracy with benchmark datasets
- Verify idempotency of pipeline operations

## Test Data Management
```python
# Test fixtures example
@pytest.fixture
def climate_deal_samples():
    return [
        {
            "company": "SolarTech",
            "amount": 2000000,
            "stage": "Seed",
            "category": "solar"
        },
        {
            "company": "WindPower",
            "amount": 10000000,
            "stage": "Series A", 
            "category": "wind"
        }
    ]
```

## Performance Testing
- **API Response Times:** Benchmark under various loads
- **Dashboard Rendering:** Test with large datasets (1000+ deals)
- **Search Performance:** Validate complex query response times
- **Memory Usage:** Monitor during data processing operations

## Brand Consistency Testing
```javascript
// Brand test example
test('components use correct brand colors', () => {
  render(<DealCard />)
  const primaryButton = screen.getByRole('button', { name: /view details/i })
  expect(primaryButton).toHaveClass('bg-[#F7D774]')
})

test('typography follows brand guidelines', () => {
  render(<DashboardHeader />)
  const heading = screen.getByRole('heading', { level: 1 })
  expect(heading).toHaveClass('text-3xl', 'font-bold')
})
```

## Security Testing
- **Input Validation:** Test for SQL injection and XSS
- **Authentication:** Verify JWT handling and expiration
- **Authorization:** Test role-based access controls
- **Data Protection:** Validate encryption and privacy controls

## Test Environment Setup
```yaml
# Test environment example
test_environment:
  database: "moo_climate_test"
  redis_cache: "localhost:6379/1"
  external_apis: "mock_mode"
  log_level: "DEBUG"
```

## Coverage Targets
- **Backend:** 80%+ code coverage
- **Frontend Components:** 90%+ for critical UI components
- **API Endpoints:** 100% coverage for all endpoints
- **Data Processing:** 95%+ for classification and cleaning logic

## Testing Best Practices
1. **Fast Tests:** Keep unit tests under 100ms
2. **Deterministic:** Eliminate flaky, non-deterministic behavior
3. **Isolated:** Tests shouldn't depend on external services
4. **Descriptive:** Clear test names describing expected behavior
5. **Data-Driven:** Use realistic test data representing edge cases

## Common Pitfalls to Avoid
- Testing implementation details instead of user behavior
- Slow test suites that discourage frequent running
- Brittle tests that break with minor UI changes
- Insufficient edge case coverage for data processing
- Missing error handling validation
