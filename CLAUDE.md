
LinkedIn Strategist + Writer Agent

For  true inbound from LinkedIn: EVERY SINGLE post needs a JOB. This four-bucket funnel has been employed successfully to build constant virality and  six-seven figure pipelines from content alone.Most people post whatever comes to mind and hope for the best. That's a slot machine, not a strategy.


LinkedIn - keeps us visible daily. It warms people up, drives DMs, and puts us in front of our ICP while they're already thinking about business. It's the platform with the highest buying power audience, and one of the best places to build a real network around your brand.


Wandar’s LinkedIn Authority Pillars
1. How Safari Demand Forms
(Main Pillar)
This is Wandar’s core territory.
Focus on:
where travelers start planning
how safari demand appears publicly
how travelers ask for recommendations
how operators get shortlisted
why inquiries happen late
public intent signals
Topics:
Reddit safari planning behavior
travelers sharing budgets and itineraries publicly
why travelers trust communities first
how travelers research safaris today
invisible safari demand online
how travelers narrow down operators before contact

2. Discovery & Distribution in Safari
This pillar explains how safari operators get discovered today and why traditional marketing alone is becoming less effective.
Focus on:
changing safari discovery behavior
community-driven discovery
why visibility before inquiries matters
how travelers discover operators early
why operators relying only on inbound lose opportunities
Topics:
why traditional safari marketing enters too late
the future of safari distribution
discovery before booking
search vs recommendation behavior
why the first credible response matters
why travelers trust conversations more than ads
why referrals alone are no longer enough

3. Trust & Conversion
Safari is a high-trust purchase.
This pillar focuses on why some operators convert and others don't.
Focus on:
response timing
expertise
credibility
trust formation
traveler confidence
Topics:
why expertise converts
how travelers evaluate operators
why speed matters
why many operators lose bookings early
how trust forms before inquiries
why authority matters more than polished marketing
why the first helpful operator often wins the relationship

4. Social Listening & Demand Capture in Safari
This pillar explains why safari is one of the strongest industries for social listening.
Focus on:
how social listening transformed other industries
why safari travelers publicly plan trips
why luxury travel creates strong intent signals
why safari operators can benefit massively from social listening
Topics:
how airlines and hotel brands use social listening
why safari buyers ask communities before operators
why public traveler conversations matter
demand capture vs brand monitoring
why safari naturally creates visible intent online
how traveler conversations become booking opportunities
why safari is uniquely suited for social listening

5. Safari Buyer Intelligence
This is where Wandar becomes the market observer.
Focus on:
what travelers are asking
changing booking behavior
budget trends
itinerary patterns
traveler concerns
Topics:
family safari demand
luxury traveler behavior
multi-country itineraries
destination trends
seasonal booking patterns
emerging traveler behavior
common traveler objections

6. Operator Growth & Positioning
This pillar connects directly to operator business challenges.
Focus on:
how operators stand out
authority positioning
trust signals
communicating expertise
why some operators consistently win
Topics:
why operators blend together online
positioning mistakes
building authority in luxury safari
referral dependence risks
how expertise creates differentiation
what makes travelers remember operators
why some operators dominate recommendations

7. Founder Perspective
This is important on LinkedIn.
People follow conviction and insight before products.
Focus on:
what you're learning from operators
observations about traveler behavior
why Wandar exists
what the industry is missing
lessons from building Wandar
This should feel:
grounded
observational
thoughtful
honest
Not startup-guru content.

8. The Future of Safari Travel
Use this pillar carefully.
Focus on:
AI changing trip planning
changing traveler expectations
always-on safari front offices
technology changing discovery
how safari operators may evolve over time
The goal is not hype.
The goal is to show where safari travel is heading.

Strategic Verdict
This direction positions Wandar around a market shift, not just a product.
That is what gives it long-term authority potential on LinkedIn.
The pillars reinforce a consistent narrative:
safari demand forms publicly
discovery behavior is changing
trust forms before inquiries
traditional marketing often enters too late
social listening creates a new demand capture layer for safari operators
If executed consistently, Wandar can become:
a recognized voice in safari travel
an authority on safari demand and discovery
a founder-led category brand
a trusted source safari operators follow regularly
The key is staying grounded in:
real traveler behavior
operator pain points
market observations
conversion insights
public demand signals
Not generic AI commentary or startup content.

Every Linkedin post falls into one of four buckets.

 Each one has a specific job in the funnel:

 → Growth (40% of posts)
 Gets you discovered by new people. Hot takes, industry commentary, bold observations. This is your top of funnel. Broad enough to attract, sharp enough to stand out.

 → Authority (30% of posts)
 Makes them trust you. Frameworks, systems, case studies, client results. This is where you prove you can actually deliver.

 → Conversion (20% of posts)
 Turns followers into clients. Direct offers, lead magnets, clear CTAs. This is where content becomes revenue.

 → Personal (10% of posts)
 Makes them remember YOU. Stories, behind the scenes, real moments. People buy from people they feel connected to.

 Each type feeds the next.

 Growth posts bring new eyes → Authority posts build trust → Conversion posts drive action → Personal posts keep them engaged.

 That's a flywheel, not just a content calendar.


Here are 4  posts strategy to use for consistent virality:

→ Brandjacking
→ Namejacking
→ Newsjacking
→ Hot takes

The problem? All four require heavy research. You need to know what's trending, who said what, and which conversations your audience already cares about.

X/Twitter  is always 10 steps ahead of LinkedIn when it comes to trends.

By the time something hits LinkedIn, it's already been chewed up on X for 48 hours.


So we built an AI agent that:

→ Monitors X and news sources for trending topics in our clients' industries
→ Filters what's actually relevant (not every trend deserves a post)
→ Drafts post outlines matched to each Wandar's voice and content strategy

---

# WANDAR LINKEDIN ENGINE — COMMANDS

## Pipeline commands

| Command | When | What it does |
|---------|------|--------------|
| `run pipeline` | Every Sunday (auto-scheduled 08:00) | KB Agent → Scanner → Strategist → Writer → .xlsx + .docx output |
| `run learning loop` | Every Saturday (manual) | Ingests analytics → updates KB → regenerates HTML dashboard |
| `build kb` | Once at setup (already done) | Builds KB from scratch from all credible sources |
| `update pillar intel` | Bi-weekly (manual) | Refreshes pillar-intel/, traveler-intel/, operator-lang/ from credible sources |
| `refresh kb sources` | On-demand | Fetches latest Brew360 + LinkedIn algorithm publications into algorithm-intel/ |
| `hot take on this` | Any time (manual) | Paste an X post or trend. Rapid Scanner → Strategist → Writer. 2 post variations in minutes. |

## Agent files

All agent system prompts live in `agents/`:
- `00-knowledge-bank.md` — institutional memory, context assembly, KB updates
- `01-scanner.md` — external signal scanner (X, Google Trends, SEO, AEO, Reddit, news)
- `02-content-strategist.md` — strategy + algorithm intel embedded, all decisions
- `03-writer.md` — pure copywriter, executes brief, applies voice + Unicode rules
- `04-learning-loop.md` — performance analysis, KB updates, HTML dashboard

## Knowledge Bank

Lives in `knowledge-bank/`. Built once. Updated by:
- Learning Loop (weekly): engagement/, hooks/
- update pillar intel (bi-weekly): pillar-intel/, traveler-intel/, operator-lang/
- refresh kb sources (on-demand): algorithm-intel/
- Pipeline end (automatic): new traveler language and operator observations filed by KB Agent

## Outputs

| Output | Location | Format |
|--------|----------|--------|
| Scanner trend brief | outputs/research/ | .md + .xlsx |
| Content strategy brief | outputs/strategy/ | .md + .xlsx |
| Finished posts | outputs/drafts/ | .md + .docx |
| Learning Loop report | outputs/analytics/ | .md + .docx |
| Performance dashboard | dashboard/index.html | HTML (open in browser) |

## Slack notifications

Configure webhook URL in `tools/config.json`. Notifications fire when:
- Sunday pipeline completes
- Scanner flags a hot take signal scoring 8+/10

## Analytics input

Drop LinkedIn CSV export → `analytics/linkedin-export.csv`
OR fill `analytics/manual-input.md`
Then run: `run learning loop`

## Optimizing for

1. Qualified Operator Conversations
2. Conversation Quality
3. Saves
4. Relevant Impressions
5. Reposts by Relevant People
