# Visual Asset Taxonomy & ChatGPT Visual GPT Prompts

## Strategic Context

Visual assets are specified in every post but must be optimized for user's custom ChatGPT Visual GPT. This file defines asset types, when to use each, and provides ChatGPT-ready prompt templates.

**Research backing:**
- PDF Carousels: 21.77% engagement (3x more than video) ([360Brew data](https://falia.co/en/360brew-linkedins-new-algorithm-explained-2026/))
- Single Image Posters: 4.85% engagement
- Text-only posts: 4% baseline engagement
- Dwell time + saves > impressions

**Key principle:** Visual assets should stop the scroll with highlights from the post, NOT copy the full post text.

---

## Asset Type Taxonomy

### 1. PDF Carousel

**When to use:**
- Frameworks, lists, multi-step processes
- Contrast posts (A vs. B, old way vs. new way)
- Authority bucket posts with educational content
- Enemy posts with multiple angles to visualize

**Engagement data:** 21.77% (highest performing format)

**Content specs:**
- 5-10 slides maximum
- Max 12 words per slide
- Content only (no design specifications)

**Best for buckets:**
- Authority (frameworks, lists)
- Growth (contrast posts, industry enemy angles)

**Examples of carousel-worthy posts:**
- "8 reasons armchair agents win by default" (Enemy post)
- "How safari demand actually forms: 5 stages" (Authority post)
- "Old safari marketing vs. new" (Contrast growth post)

---

### 2. Single Image Poster

**When to use:**
- Quote highlights from post
- Counterintuitive stats
- Hook amplification (make first line visual)
- Growth posts with sharp one-liner hooks

**Engagement data:** 4.85%

**Content specs:**
- Max 15-20 words
- Single quote or stat
- Content only (no design specifications)

**Best for buckets:**
- Growth (hot takes, sharp hooks)
- Enemy (irony angle, sharp statement)

**Examples of poster-worthy posts:**
- Hook: "Expertise that can't be found doesn't exist" (with minimal visual)
- Stat: "90% of safaris start with Google. Real operators aren't there."
- Quote: "Fanaticism compounds. Credentials expire."

---

### 3. Text Highlight (No Image)

**When to use:**
- Personal posts (authenticity over production)
- Story posts with emotional arc
- Conversion posts with clear CTA
- Insight posts where visual adds no value

**Engagement data:** 4% baseline

**Best for buckets:**
- Personal (authenticity prioritized)
- Conversion (cleanest format for CTA)

**When to default to this:**
- Personal vulnerability stories
- Founder moment posts
- When carousel/poster would feel forced

---

**IMPORTANT: Content-Only Specifications**

ChatGPT Visual GPT already has Wandar's design system configured (colors, fonts, dimensions, logo placement).

**For all visual asset prompts:**
- Include ONLY the content to visualize (quotes, key points, data, slide text)
- NO color codes, font specifications, dimensions, backgrounds, or design instructions
- Format: list the content for each slide/element

---

## Content-Only Templates for Visual Assets

**CRITICAL:** ChatGPT Visual GPT already has Wandar's design system (colors, fonts, dimensions, logo). Include ONLY content below.

### Template A: Carousel (Enemy/Growth Post)

VISUAL ASSET TYPE: Carousel

VISUAL ASSET CONTENT:
Slide 1: [Hook - main point]
Slide 2: [Problem statement]
Slide 3: [Evidence/data point 1]
Slide 4: [Evidence/data point 2]
Slide 5: [Evidence/data point 3]
Slide 6: [Consequence]
Slide 7: [Solution/call to action]

**Example:**
Slide 1: "Armchair agents selling safaris they've never experienced"
Slide 2: "Travelers lose: Inexperienced advice leads to mismatched expectations"
Slide 3: "Operators lose: Real expertise invisible on Google"
Slide 4: "Conservation loses: 40% margins pull funds from community projects"
Slide 5: "The gap: Credible operators need tools to show up"
Slide 6: "Social listening closes this gap"
Slide 7: "Knowledgeable operators must be where travelers ask questions"

---

### Template B: Carousel (Authority/Framework Post)

VISUAL ASSET TYPE: Carousel

VISUAL ASSET CONTENT:
Slide 1: [Framework title/hook]
Slide 2-6: [Each framework stage/point - one per slide]
Slide 7: [Summary/application]

**Example:**
Slide 1: "Why safari demand forms publicly before operators see it"
Slide 2: "Stage 1: Traveler research (Reddit, forums, communities)"
Slide 3: "Stage 2: Shortlisting (Before contact, based on visibility)"
Slide 4: "Stage 3: Inquiry (Only to pre-selected operators)"
Slide 5: "Stage 4: Conversion (Speed + expertise wins)"
Slide 6: "The gap: Operators enter at Stage 3, miss Stages 1-2"
Slide 7: "Solution: Visibility where demand forms, not just where it converts"

---

### Template C: Poster (Hook Amplification)

VISUAL ASSET TYPE: Poster

VISUAL ASSET CONTENT:
[Single powerful quote or stat from post]

**Example:**
"80% of safari inquiries come after travelers already decided where to go"

---

### Template D: Poster (Stat Highlight)

VISUAL ASSET TYPE: Poster

VISUAL ASSET CONTENT:
[Key number + context]

**Example:**
"4-7 days
The response time gap that loses bookings"

---

### Template E: Text Highlight (Personal Post)

VISUAL ASSET TYPE: Text Highlight

VISUAL ASSET CONTENT:
[Pulled quote from post]
— [Attribution]

**Example:**
"Proximity to an industry doesn't guarantee you'll see what's broken. Sometimes distance gives you the pattern recognition insiders miss."
— on building Wandar

**When to use:**
- Personal posts (default to text-only for authenticity)
- Quotable insights from personal stories
- Founder moments with synthesis worth highlighting

---

## Writer Workflow: Content-Only Visual Assets

**Step 1: Identify asset type**
- Enemy/Growth post → Carousel or Poster
- Authority framework → Carousel
- Personal story → Text Highlight (default)

**Step 2: Extract content only**
- Pull key quotes, stats, or slide points from post
- NO design specifications (colors, fonts, dimensions)
- List content in logical sequence

**Step 3: Output format**
```
VISUAL ASSET TYPE: [Carousel / Poster / Text Highlight]

VISUAL ASSET CONTENT:
[Content only - quotes, slide text, or stats]
```

**Example outputs:**
- Carousel: Slide 1: "Hook" / Slide 2: "Point" / Slide 3: "Point" / etc.
- Poster: "Single stat or quote"
- Text Highlight: "Quote" — attribution

---

## Quality Checklist (Content-Only)

Before including in post output, verify:

**For All Assets:**
- [ ] Content only (NO colors, fonts, dimensions, logos)
- [ ] Slide text or quotes extracted from post
- [ ] Logical flow for carousels (cover → build → CTA)
- [ ] Text Highlight for personal posts (default)

**For Carousels:**
- [ ] 5-10 slides listed
- [ ] Each slide ≤ 12 words
- [ ] Content follows post narrative

**For Posters:**
- [ ] Single stat or quote
- [ ] ≤ 20 words total

---

## Learning Loop Integration

**Track by asset type:**
- Carousel engagement vs. text-only
- Poster engagement vs. text-only
- Which carousel structures drive highest saves
- Optimal slide count (5 vs. 8 vs. 10 slides)

**Promote winning patterns:**
- Best-performing carousel flows
- Highest-engagement poster formats
- When text-only outperforms visuals (update defaults)

**Update quarterly** based on Learning Loop findings.
