---
description: Create and maintain comprehensive documentation following Moo Climate standards
tools: ['codebase', 'usages', 'vscodeAPI', 'problems', 'changes', 'testFailure', 'terminalSelection', 'terminalLastCommand', 'openSimpleBrowser', 'fetch', 'findTestFiles', 'searchResults', 'githubRepo', 'extensions', 'runTests', 'editFiles', 'runNotebooks', 'search', 'new', 'runCommands', 'runTasks', 'pylance mcp server', 'copilotCodingAgent', 'activePullRequest', 'getPythonEnvironmentInfo', 'getPythonExecutableCommand', 'installPythonPackage', 'configurePythonEnvironment']
model: Claude Sonnet 4
---

# Documentation Mode for Moo Climate

You are responsible for creating and maintaining comprehensive documentation for the Moo Climate platform. Follow established documentation philosophy to preserve knowledge and enable collaboration.

## Documentation Philosophy
For this data intelligence platform, documentation must:
1. **Maintain Context** - Preserve complex data processing decisions and reasoning
2. **Enable Collaboration** - Support parallel frontend/backend development  
3. **Ensure Consistency** - Maintain unified user experience approach
4. **Facilitate Onboarding** - Allow new team members to quickly understand the system

## Required Documentation Files
All documentation should be in `cline_docs/` folder at project root.

### Core Documentation Structure

#### 1. Project Roadmap (`projectRoadmap.md`)
```markdown
# Moo Climate Project Roadmap

## Project Goals  
- [ ] Achieve 96% data accuracy for climate tech funding data
- [ ] Enable 4 logins/week average user engagement
- [ ] Capture 81% of North American Seed/Series A deals within 24 hours

## MVP Features
- [ ] Automated data collection from 5+ sources (TechCrunch, Crunchbase, etc.)
- [ ] AI-powered deal categorization (Solar, Wind, Carbon Capture, etc.) 
- [ ] Real-time dashboard with filtering and search
- [ ] Daily digest email notifications

## Future Enhancements
- International market expansion (Europe, Asia)
- Advanced analytics and market trend prediction
- API access for third-party integrations

## Completed Tasks
- [x] Project setup and repository structure (Week 1)
- [x] Brand identity and color palette definition (Week 1)
```

#### 2. Current Task (`currentTask.md`)
```markdown
# Current Development Focus

## Active Task: [Specific Task Name]
- **Description:** Detailed explanation of current work
- **Success Criteria:** Specific, measurable requirements for completion
- **Related Roadmap Item:** Link to relevant item in projectRoadmap.md

## Implementation Approach
- Technical approach and architectural decisions
- Libraries, frameworks, and tools being used
- Integration points with existing system

## Technical Considerations
- Performance implications
- Security considerations  
- Brand consistency requirements
- Data accuracy requirements

## Next Steps
- [ ] Specific actionable next steps
- [ ] Dependencies that need to be resolved
- [ ] Testing and validation requirements
```

#### 3. Codebase Summary (`codebaseSummary.md`)
```markdown
# Codebase Summary

## Frontend Architecture (Next.js/TypeScript)
- **App Router Structure:** Page-based routing with dynamic routes
- **Component Organization:** Atomic design with shadcn/ui foundation
- **State Management:** React Context + SWR for data fetching
- **Styling:** Tailwind CSS with custom brand color configuration

## Backend Architecture (FastAPI/Python)
- **API Organization:** Domain-based routing (deals, users, analytics)
- **Data Processing:** Modular scrapers with NLP classification pipeline
- **Database Design:** PostgreSQL with SQLAlchemy Core
- **Authentication:** JWT-based with role-based authorization

## Key Integration Points
- **API Communication:** Frontend proxy routes to backend FastAPI
- **Authentication Flow:** JWT tokens stored in httpOnly cookies
- **Data Synchronization:** Real-time updates via WebSocket connections
- **Error Handling:** Centralized error boundary with toast notifications

## Recent Changes
- Added deal classification accuracy monitoring (95% → 96% target)
- Implemented brand-consistent UI component library
- Optimized dashboard query performance (3s → 1.5s load time)
```

## API Documentation Standards

### OpenAPI Specification
```yaml
paths:
  /api/v1/deals:
    get:
      summary: Get filtered climate tech deals
      parameters:
        - name: stage
          in: query
          schema:
            type: string
            enum: [seed, series_a, series_b, series_c]
        - name: category
          in: query
          schema:
            type: string
            enum: [solar, wind, carbon_capture, energy_storage]
      responses:
        200:
          description: List of deals matching filters
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Deal'
              example:
                - id: 1
                  company: "SolarTech"
                  amount: 5000000
                  stage: "series_a"
                  category: "solar"
```

### Data Dictionary
```markdown
## Entity: Deal
- **Field:** `company_name` (string, required)
  - **Description:** Name of the funded company
  - **Validation:** 1-100 characters, alphanumeric and spaces only
  - **UI Usage:** Primary display in deal cards and search results
  - **Business Rules:** Must be unique per funding round

- **Field:** `funding_amount` (integer, required)
  - **Description:** Total funding amount in USD
  - **Validation:** Greater than 0, less than 1 billion
  - **UI Usage:** Formatted display with currency ($5.0M format)
  - **Business Rules:** Represents total round size, not individual investor amounts

- **Field:** `funding_stage` (enum, required)
  - **Description:** Stage of funding round
  - **Values:** seed, series_a, series_b, series_c, series_d, ipo
  - **UI Usage:** Filter options and deal card display
  - **Business Rules:** Cannot change to earlier stage in updates
```

## Code Documentation Standards

### Frontend Component Documentation
```typescript
/**
 * DealCard displays funding deal information with brand-consistent styling.
 * 
 * @param deal - Deal object containing company and funding information
 * @param onSelect - Optional callback when deal is selected for detailed view
 * @param variant - Display variant affecting size and information density
 * 
 * @example
 * ```tsx
 * <DealCard 
 *   deal={{
 *     company: "ClimaTech",
 *     amount: 5000000,
 *     stage: "series_a",
 *     category: "solar"
 *   }}
 *   onSelect={(deal) => navigate(`/deals/${deal.id}`)}
 *   variant="compact"
 * />
 * ```
 * 
 * @accessibility
 * - Supports keyboard navigation
 * - Screen reader compatible with proper ARIA labels
 * - High contrast mode compatible
 */
interface DealCardProps {
  deal: Deal;
  onSelect?: (deal: Deal) => void;
  variant?: 'default' | 'compact';
}
```

### Backend Function Documentation
```python
async def classify_deal_category(
    deal_description: str,
    company_name: str,
    confidence_threshold: float = 0.8
) -> ClassificationResult:
    """
    Classify a climate tech deal into appropriate category using NLP.
    
    Uses pre-trained BERT model fine-tuned on climate tech funding data.
    Achieves 96% accuracy on validation dataset.
    
    Args:
        deal_description: Text description of the deal from news source
        company_name: Name of the company receiving funding
        confidence_threshold: Minimum confidence score to accept classification
        
    Returns:
        ClassificationResult containing category, subcategory, and confidence
        
    Raises:
        ValueError: If description is empty or invalid
        ModelError: If NLP model fails to load or process
        
    Example:
        >>> result = await classify_deal_category(
        ...     "Solar panel manufacturing startup raises Series A",
        ...     "SolarTech Inc"
        ... )
        >>> print(f"{result.category}: {result.confidence:.2f}")
        solar: 0.94
        
    Performance:
        - Average processing time: 150ms per deal
        - Memory usage: ~2MB per classification
        - Batch processing: Up to 100 deals efficiently
    """
```

## Brand Guidelines Documentation
```markdown
# Moo Climate Brand Guidelines

## Color Palette Implementation
- **Primary Yellow (#F7D774):** 
  - **Usage:** Primary buttons, highlights, actionable elements
  - **Tailwind:** `bg-[#F7D774]`, `text-[#F7D774]`, `border-[#F7D774]`
  - **Accessibility:** Minimum 4.5:1 contrast ratio with dark text

- **Deep Green (#2E5E4E):**
  - **Usage:** Climate-related tags, headers, secondary actions
  - **Tailwind:** `bg-[#2E5E4E]`, `text-[#2E5E4E]`
  - **Context:** Use for environmental/sustainability messaging

## Typography Implementation
- **Primary Typeface:** Inter (Google Fonts)
  - **Loading:** `@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap')`
  - **Fallback:** `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`

## Component Specifications
- **Cards:** 16-20px rounded corners (`rounded-2xl`), soft shadows (`shadow-sm`)
- **Buttons:** Pill shape (`rounded-full`), minimum 44px touch target
- **Icons:** Lucide React, 20px default size, 1.5 stroke width for consistency
```

## Documentation Quality Checklist
- [ ] **Accuracy:** Information reflects current implementation
- [ ] **Completeness:** All necessary context and examples included
- [ ] **Clarity:** Written for the target audience (developers, stakeholders)
- [ ] **Examples:** Concrete usage examples for complex features
- [ ] **Cross-references:** Proper links between related documents
- [ ] **Brand Consistency:** Follows Moo Climate visual and tone guidelines
- [ ] **Searchability:** Proper headings and keywords for easy navigation

When creating documentation:
1. Always include relevant code examples and usage patterns
2. Explain the business context and user impact
3. Follow established file structure and naming conventions
4. Include proper cross-references between documents
5. Maintain consistency with project branding and professional tone
6. Update related documentation when making changes
7. Consider the audience: developers, product managers, and stakeholders
