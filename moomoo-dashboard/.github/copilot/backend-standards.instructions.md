---
applyTo: "backend, python, fastapi, api"
description: Backend coding standards for Python, FastAPI, and Supabase
---

# Backend Coding Standards

## FastAPI Structure
- **Route Organization:** Group by domain (deals, users, analytics)
- **Validation:** Use Pydantic models for request/response
- **Dependencies:** Implement dependency injection for database/service access
- **Documentation:** Document all endpoints with OpenAPI comments

## Database Access Patterns
- **ORM:** Use SQLAlchemy Core (not ORM) for database operations
- **Repository Pattern:** Implement for data access abstraction
- **Transactions:** Use for multi-step operations
- **Error Handling:** Include proper retries and rollback logic

## Data Processing Pipeline
- **Modularity:** Build scrapers with clear separation of concerns
- **Error Handling:** Robust logging and graceful failure handling
- **NLP Efficiency:** Use models with proper caching strategies
- **Idempotency:** Design operations to be safely retryable

## API Design Principles
```python
# Route organization example
@router.get("/deals", response_model=List[DealResponse])
async def get_deals(
    filters: DealFilters = Depends(),
    db: Database = Depends(get_database),
    current_user: User = Depends(get_current_user)
) -> List[DealResponse]:
    """
    Get filtered list of climate tech deals.
    
    Args:
        filters: Deal filtering parameters
        db: Database connection
        current_user: Authenticated user
        
    Returns:
        List of deals matching filters
    """
```

## Naming Conventions
- **Files:** snake_case (e.g., `deal_repository.py`)
- **Classes:** PascalCase (e.g., `DealProcessor`)
- **Functions/Variables:** snake_case (e.g., `get_recent_deals()`)
- **Constants:** UPPER_SNAKE_CASE (e.g., `MAX_RETRY_ATTEMPTS`)

## Code Organization
```
backend/
├── app/
│   ├── api/            # API route handlers
│   │   ├── v1/         # API version grouping
│   │   └── deps.py     # Common dependencies
│   ├── core/           # Core functionality
│   │   ├── config.py   # Configuration management
│   │   └── security.py # Authentication/authorization
│   ├── models/         # Pydantic models
│   ├── services/       # Business logic layer
│   ├── repositories/   # Data access layer
│   └── utils/          # Utility functions
├── tests/              # Test suites
└── migrations/         # Database migrations
```

## Error Handling Strategy
```python
# Structured error responses
class APIError(Exception):
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code

# Database operation example
async def get_deal_by_id(deal_id: int, db: Database) -> Deal:
    try:
        result = await db.fetch_one(
            "SELECT * FROM deals WHERE id = :deal_id", 
            {"deal_id": deal_id}
        )
        if not result:
            raise APIError(404, f"Deal with id {deal_id} not found", "DEAL_NOT_FOUND")
        return Deal(**result)
    except DatabaseError as e:
        logger.error(f"Database error retrieving deal {deal_id}: {e}")
        raise APIError(500, "Database error occurred", "DATABASE_ERROR")
```

## Performance Considerations
- **Async Operations:** Use async/await for I/O operations
- **Connection Pooling:** Proper database connection management
- **Caching:** Implement Redis for frequently accessed data
- **Query Optimization:** Use indexes and efficient query patterns

## Data Processing Best Practices
- **Validation:** Validate all incoming data at API boundary
- **Sanitization:** Clean and normalize data consistently  
- **Logging:** Comprehensive logging for debugging and monitoring
- **Monitoring:** Track performance metrics and error rates

## Security Standards
- **Input Validation:** Validate and sanitize all inputs
- **Authentication:** JWT-based authentication with proper expiration
- **Authorization:** Role-based access control
- **Data Protection:** Encrypt sensitive data at rest and in transit
