---
mode: edit
tools: ['codebase', 'terminal']
description: Generate comprehensive documentation following Moo Climate documentation standards
---

# Documentation Generation Prompt

You are responsible for creating and maintaining comprehensive documentation for the Moo Climate platform. Follow the established documentation philosophy and standards.

## Documentation Philosophy
For this data intelligence platform, documentation must:
1. **Maintain Context** - Preserve knowledge about complex data processing decisions
2. **Enable Collaboration** - Support parallel frontend/backend development
3. **Ensure Consistency** - Maintain unified user experience approach  
4. **Facilitate Onboarding** - Allow quick system understanding

## Required Documentation Structure

### 1. Project Roadmap (projectRoadmap.md)
```markdown
# Moo Climate Project Roadmap

## Project Goals
- [ ] Goal: Description and success criteria

## MVP Features  
- [ ] Feature: Description and acceptance criteria

## Future Enhancements
- Enhancement ideas and rationale

## Completed Tasks
- [x] Task (Date completed)
```

### 2. Current Task (currentTask.md)
```markdown
# Current Development Focus

## Active Task: [Task Name]
- **Description:** Detailed explanation
- **Success Criteria:** Requirements for completion
- **Related Roadmap Item:** Link to projectRoadmap.md

## Implementation Approach
- Step-by-step approach

## Technical Considerations
- Important technical decisions and constraints

## Next Steps
- [ ] Specific actionable steps
```

### 3. Tech Stack Documentation (techStack.md)
Document technology choices and architecture decisions:
- Frontend: Next.js, TypeScript, Tailwind CSS, shadcn/ui
- Backend: FastAPI, Supabase, Python data processing
- Infrastructure: Vercel, Render, GitHub Actions
- Include rationale for each choice

### 4. Codebase Summary (codebaseSummary.md)
```markdown
# Codebase Summary

## Frontend Structure
- Component organization and relationships
- Data flow patterns
- State management approach

## Backend Structure  
- API endpoint organization
- Data processing pipeline
- Database design patterns

## Key Integration Points
- Frontend-backend connections
- Authentication flow
- Data synchronization

## Recent Changes
- Change: Impact and rationale
```

### 5. Lessons Learned (lessonsLearned.md)
```markdown
# Lessons Learned

## Technical Challenges
- **Challenge:** Description
  - **Solution:** Resolution approach
  - **Prevention:** Future avoidance strategy

## Useful Patterns
- Pattern: Description and implementation example

## Performance Optimizations
- Optimization: Description, implementation, and metrics
```

### 6. Brand Guidelines (brandGuidelines.md)
Document complete brand implementation:
- Color palette with usage guidelines
- Typography hierarchy and implementation
- UI element specifications
- Code examples for brand consistency

## API Documentation Standards

### OpenAPI Specification
- Complete endpoint documentation
- Request/response schemas
- Error code definitions  
- Example requests and responses
- Authentication requirements

### Data Dictionary
```markdown
## Entity: Deal
- **Field:** `company_name` (string, required)
  - Description: Name of the funded company
  - Validation: 1-100 characters, no special chars
  - UI Usage: Primary display in deal cards

- **Field:** `funding_amount` (integer, required)  
  - Description: Funding amount in USD
  - Validation: > 0, < 1 billion
  - UI Usage: Formatted display with currency
```

## Code Documentation Standards

### Frontend Documentation
```typescript
/**
 * DealCard component displays funding deal information
 * 
 * @param deal - Deal object containing company and funding info
 * @param onSelect - Callback when deal is selected
 * @example
 * <DealCard 
 *   deal={{company: "ClimaTech", amount: 5000000}} 
 *   onSelect={(deal) => console.log(deal)}
 * />
 */
interface DealCardProps {
  deal: Deal;
  onSelect?: (deal: Deal) => void;
}
```

### Backend Documentation
```python
async def get_deals_by_stage(
    stage: FundingStage,
    limit: int = 50,
    db: Database = Depends(get_database)
) -> List[Deal]:
    """
    Retrieve deals filtered by funding stage.
    
    Args:
        stage: Funding stage filter (seed, series_a, etc.)
        limit: Maximum number of deals to return (default 50)
        db: Database connection dependency
        
    Returns:
        List of Deal objects matching the stage filter
        
    Raises:
        HTTPException: If stage is invalid or database error occurs
        
    Example:
        deals = await get_deals_by_stage(FundingStage.SERIES_A, limit=25)
    """
```

## Documentation Quality Standards

### Content Guidelines
- **Clear and Concise:** Explain concepts without unnecessary complexity
- **Examples Included:** Provide concrete usage examples
- **Why Not Just What:** Explain reasoning behind decisions
- **Current and Accurate:** Keep documentation synchronized with code
- **Brand Consistent:** Follow Moo Climate brand guidelines

### Review Checklist
- [ ] Is information current and accurate?
- [ ] Are examples provided for complex features?
- [ ] Is the business context explained?
- [ ] Does it follow brand guidelines?
- [ ] Are code examples properly formatted?
- [ ] Is navigation between documents clear?

When generating documentation:
1. Always include relevant code examples
2. Explain the business context and user impact
3. Follow the established file structure and naming
4. Include proper cross-references between documents
5. Maintain consistency with project branding and tone
