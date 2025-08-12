# Moo Climate Coding Standards

## Tech Stack-Specific Best Practices

### Frontend (Next.js, TypeScript, Tailwind CSS, shadcn/ui)

#### Next.js Architecture

- Use the App Router for all new development
- Implement server components for data fetching and client components for interactivity
- Follow the page-based routing structure with dynamic routes for entity details
- Utilize Next.js API routes for backend communication proxying

#### TypeScript Best Practices

- Define explicit interfaces for all data structures
- Use discriminated unions for state management
- Leverage TypeScript utility types (Pick, Omit, Partial) to derive types
- Avoid using ny type; use unknown with type guards instead

#### UI Component Standards

- Use shadcn/ui components as the foundation for all UI elements
- Extend shadcn/ui components with custom styling via Tailwind
- Implement responsive design using Tailwind's breakpoint system
- Create atomic, reusable components in the components directory

#### Brand Implementation

- **Color Usage:**
  - Primary Yellow (#F7D774): Use for actionable elements, highlights, and primary buttons
  - Deep Green (#2E5E4E): Use for climate-related tags, headers, and secondary actions
  - Charcoal Gray (#2D2D2D): Use for text and chart structure
  - Light Neutral Gray (#F3F3F3): Use for backgrounds and neutral UI elements
  - White (#FFFFFF): Use for card backgrounds and negative space
  - Soft Sky Blue (#AEE1F6): Use sparingly for alerts and highlights

- **Typography Implementation:**
  - Configure Tailwind to use Inter as primary font and Poppins as secondary font
  - Follow the hierarchy guidelines for consistent text sizing
  - Use proper font weights (Bold for H1, Semi-Bold for H2, Regular for body text)

- **UI Elements:**
  - Cards: Implement with rounded corners (16-20px), soft shadows, and muted backgrounds
  - Buttons: Use pill shape with appropriate color scheme (Yellow for primary, Green or Gray for secondary)
  - Icons: Use Lucide or Feather icons with rounded, minimal line style

### Backend (Python, FastAPI, Supabase)

#### FastAPI Structure

- Organize routes by domain (deals, users, analytics)
- Use Pydantic models for request/response validation
- Implement dependency injection for database and service access
- Document all endpoints with OpenAPI comments

#### Database Access

- Use SQLAlchemy Core (not ORM) for database operations
- Implement repository pattern for data access
- Use transactions for multi-step operations
- Include proper error handling and retries for database operations

#### Data Processing Pipeline

- Build modular scrapers with clear separation of concerns
- Implement robust error handling and logging
- Use NLP models efficiently with proper caching
- Design for idempotent operations that can be safely retried

## Code Quality Standards

### Naming Conventions

- **Frontend**:
  - React components: PascalCase (e.g., DealCard.tsx)
  - Hooks: camelCase with " use\ prefix (e.g., useDeals.ts)
 - Utility functions: camelCase (e.g., ormatCurrency.ts)
 
- **Backend**:
 - Python files: snake_case (e.g., deal_repository.py)
 - Classes: PascalCase (e.g., DealProcessor)
 - Functions and variables: snake_case (e.g., get_recent_deals())

### Code Organization

- **Frontend**: Organize by feature with shared components, hooks, and utilities
- **Backend**: Structure by domain with clear separation of API routes, models, services, and repositories

### Error Handling

- **Frontend**: Implement error boundaries and toast notifications
- **Backend**: Use structured error responses with appropriate HTTP status codes
- **Both**: Log errors with context for debugging

### Performance Considerations

- **Frontend**: Implement virtualization for long lists, optimize images, use memoization
- **Backend**: Use async operations, implement caching, optimize database queries
