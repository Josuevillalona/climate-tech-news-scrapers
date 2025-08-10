# 🎠 Interactive Company Carousel for Investment Alerts

## ✨ New Feature: Company Deal Carousel

We've enhanced the AlertsPanel with an interactive carousel that displays matching companies for each investment alert. This provides Alex with a quick, visual way to preview deals without leaving the alert management interface.

### 🎯 Key Features

#### **3-Company Display per Page**
- Shows 3 companies at a time in beautifully designed cards
- Clean, scannable layout with company details
- Each card includes company name, funding stage, amount, and sector

#### **Navigation Controls**
- **Left/Right Arrows**: Navigate through company pages
- **Progress Indicator**: Shows percentage completion (e.g., "33%" for page 1 of 3)
- **Pagination Dots**: Visual indicators for each page with click-to-jump functionality

#### **Rich Company Information**
Each company card displays:
- **Company Name**: Prominently displayed with truncation for long names
- **Funding Stage**: Color-coded badges (Seed, Series A, Series B, etc.)
- **AI Focus Badge**: Special "AI" badge for AI-focused companies
- **Funding Amount**: Formatted currency (e.g., $15M, $32M)
- **Sector Tags**: Climate tech sectors with overflow indicators (e.g., "Solar Energy +1")
- **Score Indicator**: Color-coded dot (green/yellow/red) based on Alex's scoring
- **View Button**: Eye icon to open the source deal URL

#### **Responsive Design**
- **Auto-adapts**: Shows navigation only when >3 companies
- **Smooth Transitions**: 200ms hover effects and color changes
- **Brand Compliance**: Uses Moo Climate colors (Yellow #F7D774, Green #2E5E4E, Charcoal #2D2D2D)

### 🛠️ Technical Implementation

#### **State Management**
```tsx
const [carouselStates, setCarouselStates] = useState<Record<string, number>>({});
```
- Tracks current page index for each alert independently
- Persists across alert interactions

#### **Navigation Logic**
```tsx
const handleCarouselNext = (presetId: string, totalDeals: number) => {
  const maxIndex = Math.max(0, Math.ceil(totalDeals / 3) - 1);
  // Loops back to start when reaching end
};
```

#### **Pagination Calculation**
- **Page Size**: 3 companies per page
- **Total Pages**: `Math.ceil(totalDeals / 3)`
- **Current Page**: Stored in `carouselStates[presetId]`
- **Slice Logic**: `deals.slice(currentIndex * 3, (currentIndex + 1) * 3)`

### 🎨 Visual Design

#### **Layout Structure**
```
┌─────────────────────────────────────────────────────┐
│ [🏢] Recent Matches [5] [←] 33% [→]                 │
├─────────────────────────────────────────────────────┤
│ [SolarTech AI] [Series A] [AI] [$15M] [👁]          │
│ [CarbonCapture Plus] [Series B] [$32M] [👁]         │
│ [GridFlow Energy] [Seed] [AI] [$8M] [👁]            │
├─────────────────────────────────────────────────────┤
│ ● ○ ○                                               │
└─────────────────────────────────────────────────────┘
```

#### **Color Coding**
- **Header**: Yellow accent (#F7D774) with building icon
- **Company Cards**: White background with subtle borders
- **Badges**: Green (#2E5E4E) for stages, Yellow (#F7D774) for AI focus
- **Navigation**: Subtle hover effects with brand colors

### 🧪 Mock Data Integration

For demonstration purposes, each new alert is populated with 5 sample companies:

1. **SolarTech AI** - Series A, $15M (Solar Energy, AI)
2. **CarbonCapture Plus** - Series B, $32M (Carbon Capture)
3. **GridFlow Energy** - Seed, $8M (Energy Storage, Software)
4. **AgriSense IoT** - Series A, $12M (AgTech, IoT)
5. **Ocean Clean** - Series B, $25M (Water Tech, Robotics)

### 🚀 User Experience Flow

1. **Alert Creation**: User creates alert with filters
2. **Auto-Population**: Alert immediately shows with 5 mock companies and "2 new" badge
3. **Carousel Interaction**: 
   - First 3 companies (SolarTech AI, CarbonCapture Plus, GridFlow Energy) visible
   - Navigation arrows appear since there are >3 companies
   - Progress shows "0%" (first page)
4. **Navigation**: 
   - Click right arrow → Shows companies 4-5 (AgriSense IoT, Ocean Clean)
   - Progress updates to "60%" 
   - Click right again → Loops back to first page
5. **Company Details**: Click eye icon → Opens source URL in new tab

### 🎯 Benefits for Alex

#### **Quick Deal Preview**
- No need to leave alert interface to see matching companies
- Visual scanning of company names, stages, and amounts
- Immediate identification of AI-focused companies

#### **Efficient Navigation**
- Arrow keys and pagination dots for quick browsing
- Progress indicator shows completion status
- Smooth transitions maintain context

#### **Rich Context**
- Sector information helps categorize opportunities
- Score indicators show deal quality at a glance
- Direct links to source material for deeper research

### 🔮 Future Enhancements

#### **Real-Time Updates**
- Connect to actual deal data from Supabase
- Live filtering based on alert criteria
- Automatic refresh when new deals match

#### **Enhanced Interactions**
- Keyboard navigation (arrow keys)
- Quick actions (save, flag, share)
- Expandable company details

#### **Performance Optimizations**
- Virtualized scrolling for large datasets
- Lazy loading of company details
- Caching of frequently accessed deals

This carousel transforms static alert lists into dynamic, interactive deal browsers that align perfectly with Alex's investment workflow! 🎯
