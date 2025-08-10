---
mode: edit
tools: ['codebase', 'terminal', 'browser']
description: Generate comprehensive implementation plans for new features or refactoring tasks
---

# Implementation Planning Prompt

You are in planning mode for the Moo Climate platform. Generate detailed implementation plans that follow the project's phase-based methodology.

## Planning Framework

### Phase-Based Approach
1. **Foundation & API Contract** (Weeks 1-4)
   - Repository setup and structure
   - API contract definition using OpenAPI/Swagger
   - Database schema design
   - Authentication system implementation

2. **Parallel Development** (Weeks 5-10)
   - Frontend: UI components with mock data
   - Backend: Data pipeline and processing

3. **Integration & Deployment** (Weeks 11-18)
   - Connect frontend to live backend
   - Analytics implementation
   - Testing and optimization
   - Deployment configuration

## Feature Planning Template

For each feature request, provide:

### User Story
As a [user type], I want to [action] so that [benefit].

### Acceptance Criteria
- [ ] Specific, testable criteria
- [ ] Performance requirements (dashboard loads < 2 seconds)
- [ ] Data accuracy requirements (96% correct data points)
- [ ] Brand consistency requirements

### Technical Requirements
**Frontend:**
- Next.js App Router implementation
- TypeScript interfaces and types
- Tailwind CSS styling with brand colors
- shadcn/ui component usage
- Responsive design considerations

**Backend:**
- FastAPI endpoint design
- Pydantic model definitions
- Database schema changes
- Data processing pipeline updates

**Data:**
- Data source requirements
- Validation and cleaning rules
- NLP processing needs
- Performance optimization

### Dependencies
- External service integrations
- Database migrations
- Third-party library requirements
- Authentication/authorization needs

### Risk Assessment
Identify potential risks in these high-risk areas:
1. **Data Quality & Coverage**
2. **Performance Bottlenecks** 
3. **Integration Complexity**

### Task Breakdown
Break down into 1-2 day completable tasks:
- Each task has clear, testable outcome
- Frontend tasks include design reference and responsive requirements
- Backend tasks specify input/output contracts and error handling
- Data pipeline tasks include validation criteria

### Estimation
- Frontend development: [X] hours
- Backend development: [Y] hours
- Testing and validation: [Z] hours
- Documentation updates: [W] hours

### Success Metrics
- How will success be measured?
- What metrics align with project goals?
- Performance benchmarks
- User experience indicators

## Brand Considerations
Ensure all UI elements follow:
- **Colors:** Primary Yellow (#F7D774), Deep Green (#2E5E4E), Charcoal Gray (#2D2D2D)
- **Typography:** Inter (primary), Poppins (secondary)
- **UI Elements:** Rounded cards (16-20px), pill-shaped buttons, minimal line icons

## Documentation Requirements
Plan for updating:
- API documentation (OpenAPI spec)
- Component documentation
- Data dictionary updates
- User guide updates

Generate plans that are comprehensive, actionable, and aligned with the Moo Climate project goals and technical standards.
