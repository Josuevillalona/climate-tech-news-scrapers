# Moo Climate Documentation Requirements

## Documentation Philosophy

For this data intelligence platform, comprehensive documentation is essential to:

1. **Maintain Context** - Preserve knowledge about complex data processing decisions
2. **Enable Collaboration** - Support parallel development between frontend and backend teams
3. **Ensure Consistency** - Maintain a unified approach to the user experience
4. **Facilitate Onboarding** - Allow new team members to quickly understand the system

## Required Documentation Files

All documentation should be maintained in the cline_docs folder at the project root.

### 1. Project Roadmap (projectRoadmap.md)

**Purpose:** Track high-level goals, features, and progress.

**Format:**
`markdown
# Moo Climate Project Roadmap

## Project Goals
- [ ] Goal 1: Description
- [ ] Goal 2: Description

## MVP Features
- [ ] Feature 1: Description and acceptance criteria
- [ ] Feature 2: Description and acceptance criteria

## Future Enhancements
- Feature idea 1
- Feature idea 2

## Completed Tasks
- [x] Task 1 (Date)
- [x] Task 2 (Date)
`

**Update Frequency:** After completing major milestones or when project goals change.

### 2. Current Task (currentTask.md)

**Purpose:** Document active development focus and next steps.

**Format:**
`markdown
# Current Development Focus

## Active Task: [Task Name]
- **Description:** Detailed explanation
- **Success Criteria:** List of requirements to consider this complete
- **Related Roadmap Item:** Link to item in projectRoadmap.md

## Implementation Approach
- Step 1
- Step 2

## Technical Considerations
- Consideration 1
- Consideration 2

## Next Steps
- [ ] Step 1
- [ ] Step 2
`

**Update Frequency:** After each task completion or significant progress.

### 3. Tech Stack Documentation (	echStack.md)

**Purpose:** Document technology choices and architecture decisions.

**Format:**
`markdown
# Moo Climate Tech Stack

## Frontend
- **Framework:** Next.js with TypeScript
- **UI Components:** shadcn/ui with Tailwind CSS
- **State Management:** React Context + SWR for data fetching
- **Visualization:** Recharts

## Backend
- **API Framework:** FastAPI
- **Database:** Supabase (PostgreSQL)
- **Data Processing:** Python with Hugging Face Transformers
- **Scraping:** BeautifulSoup/Scrapy

## Infrastructure
- **Frontend Hosting:** Vercel
- **Backend Hosting:** Render
- **CI/CD:** GitHub Actions

## Architecture Decisions
- Decision 1: Rationale
- Decision 2: Rationale
`

**Update Frequency:** When new technologies are added or architecture decisions change.

### 4. Codebase Summary (codebaseSummary.md)

**Purpose:** Provide an overview of project structure and recent changes.

**Format:**
`markdown
# Codebase Summary

## Frontend Structure
- Key components and their relationships
- Data flow patterns

## Backend Structure
- API endpoints organization
- Data processing pipeline

## Key Integration Points
- How frontend and backend connect
- Authentication flow

## Recent Changes
- Change 1: Impact and rationale
- Change 2: Impact and rationale
`

**Update Frequency:** After significant structural changes.

### 5. Lessons Learned (lessonsLearned.md)

**Purpose:** Document solutions to problems and useful patterns.

**Format:**
`markdown
# Lessons Learned

## Technical Challenges
- **Challenge 1:** Description
  - **Solution:** How it was resolved
  - **Prevention:** How to avoid in future

## Useful Patterns
- Pattern 1: Description and example
- Pattern 2: Description and example

## Performance Optimizations
- Optimization 1: Description and metrics
`

**Update Frequency:** When encountering and solving significant issues.

### 6. Brand Guidelines (randGuidelines.md)

**Purpose:** Document brand identity and implementation guidelines.

**Format:**
`markdown
# Moo Climate Brand Guidelines

## Color Palette
- **Primary Yellow (Energy):** #F7D774 - For actionable elements, highlights, and primary buttons
- **Deep Green (Climate):** #2E5E4E - For climate-related tags, headers, and secondary actions
- **Charcoal Gray (Data):** #2D2D2D - For text and chart structure
- **Light Neutral Gray:** #F3F3F3 - For backgrounds and neutral UI elements
- **White:** #FFFFFF - For card backgrounds and negative space
- **Soft Sky Blue (Optional accent):** #AEE1F6 - For alerts and highlights

## Typography
- **Primary Typeface:** Inter (Google Fonts)
- **Alternate Typeface:** Poppins
- **Hierarchy:**
  - H1 (Titles): 32px / Bold
  - H2 (Subtitles): 24px / Semi-Bold
  - Body Text: 16px / Regular
  - Captions/Labels: 12px / Medium

## UI Elements
- **Cards:** Rounded 16-20px, soft shadow, muted backgrounds
- **Buttons:** Pill shape; Primary in Yellow, Secondary in Green or Gray
- **Progress Bars & Rings:** Slim with Yellow or Green fills
- **Charts:** Minimalistic, highlight key metrics in Yellow/Green, muted grays for secondary data
- **Icons:** Rounded minimal line icons (Lucide or Feather)

## Tone & Voice
- **Professional yet approachable:** Data-driven but friendly for startups
- **Optimistic:** Climate-positive outlook, empowering smaller funds/founders
- **Clear and Insightful:** Simplifies complex funding data for faster decisions
`

**Update Frequency:** When brand elements are refined or expanded.

## API Documentation

### OpenAPI Specification

- Maintain a complete OpenAPI/Swagger specification for the backend API
- Document all endpoints, request/response schemas, and error codes
- Include example requests and responses
- Update whenever API changes

### Data Dictionary

- Document all data entities and their relationships
- Define all fields, their types, and validation rules
- Include business logic rules that apply to the data
- Explain how entities map to UI components

## Code Documentation Standards

### Frontend

- Document all React components with JSDoc comments
- Include prop definitions and examples
- Document custom hooks with usage examples
- Add inline comments for complex logic

### Backend

- Document all API endpoints with docstrings
- Include parameter descriptions and validation rules
- Document data processing functions with examples
- Add type hints to all Python functions

## Documentation Review Process

1. **Documentation Updates:** Should accompany all code changes
2. **Review Checklist:**
   - Is the documentation clear and concise?
   - Does it explain the why, not just the what?
   - Are there examples for complex features?
   - Is it up-to-date with the current implementation?
   - Does it adhere to brand guidelines?
3. **Regular Audits:** Schedule monthly documentation reviews

## Common Documentation Pitfalls

1. **Outdated Information:** Documentation that no longer reflects the code
2. **Missing Context:** Explaining what but not why decisions were made
3. **Excessive Detail:** Too much low-level information obscuring the big picture
4. **Insufficient Examples:** Lack of concrete usage examples
5. **Undocumented Assumptions:** Implicit knowledge that isn't captured
6. **Brand Inconsistency:** Documentation that doesn't follow brand guidelines
