---
applyTo: "frontend, react, nextjs, typescript, tailwind"
description: Frontend coding standards for Next.js, TypeScript, and Tailwind CSS
---

# Frontend Coding Standards

## Next.js Architecture
- **App Router:** Use for all new development
- **Server Components:** For data fetching 
- **Client Components:** For interactivity
- **API Routes:** For backend communication proxying
- **Dynamic Routes:** For entity details

## TypeScript Best Practices
- Define explicit interfaces for all data structures
- Use discriminated unions for state management
- Leverage utility types (Pick, Omit, Partial)
- Avoid `any` type; use `unknown` with type guards

## UI Component Standards
- **Base:** shadcn/ui components as foundation
- **Styling:** Extend with Tailwind CSS
- **Responsive:** Use Tailwind's breakpoint system
- **Structure:** Atomic, reusable components in `/components`

## Brand Implementation
### Color Usage (Tailwind Classes)
```css
/* Primary Yellow #F7D774 */
bg-[#F7D774] text-[#F7D774] border-[#F7D774]

/* Deep Green #2E5E4E */
bg-[#2E5E4E] text-[#2E5E4E] border-[#2E5E4E] 

/* Charcoal Gray #2D2D2D */
bg-[#2D2D2D] text-[#2D2D2D] border-[#2D2D2D]

/* Light Neutral Gray #F3F3F3 */
bg-[#F3F3F3] text-[#F3F3F3] border-[#F3F3F3]

/* Soft Sky Blue #AEE1F6 */
bg-[#AEE1F6] text-[#AEE1F6] border-[#AEE1F6]
```

### Typography Implementation
- **Primary:** Inter font via Google Fonts
- **Secondary:** Poppins font
- **Hierarchy:** 
  - H1: `text-3xl font-bold` (32px/Bold)
  - H2: `text-2xl font-semibold` (24px/Semi-Bold)
  - Body: `text-base font-normal` (16px/Regular)
  - Caption: `text-xs font-medium` (12px/Medium)

### UI Elements
- **Cards:** `rounded-2xl shadow-sm bg-white` (16-20px rounded corners)
- **Buttons:** `rounded-full` (pill shape)
  - Primary: `bg-[#F7D774] hover:bg-[#F7D774]/90`
  - Secondary: `bg-[#2E5E4E] hover:bg-[#2E5E4E]/90`
- **Icons:** Use Lucide React with minimal, rounded style

## Naming Conventions
- **Components:** PascalCase (e.g., `DealCard.tsx`)
- **Hooks:** camelCase with "use" prefix (e.g., `useDeals.ts`)
- **Utilities:** camelCase (e.g., `formatCurrency.ts`)

## Code Organization
```
src/
├── app/                 # Next.js App Router pages
├── components/          # Reusable UI components
│   ├── ui/             # shadcn/ui base components
│   └── feature/        # Feature-specific components
├── hooks/              # Custom React hooks
├── lib/                # Utility functions
├── types/              # TypeScript type definitions
└── styles/             # Global styles and Tailwind config
```

## Performance Considerations
- Implement virtualization for long lists
- Optimize images with Next.js Image component
- Use React.memo for expensive components
- Implement proper loading states

## Error Handling
- Implement error boundaries for component tree protection
- Use toast notifications for user feedback
- Provide fallback UI for failed states
- Log errors with context for debugging
