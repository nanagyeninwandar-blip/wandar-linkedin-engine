---
section: algorithm-intel/linkedin-algorithm
description: Running knowledge base of LinkedIn algorithm intelligence. Sourced from credible publications only. Update via refresh kb sources command when new data is available.
updated: 2026-05-07
sources: Seed intelligence + 360Brew live refresh May 2026. See brew360-latest.md for full 360Brew detail.
---

# LinkedIn Algorithm Intelligence

## How LinkedIn distributes content (seed knowledge)

LinkedIn's algorithm prioritizes content that keeps people on the platform longer and generates meaningful engagement. Key signals:

### Primary ranking signals

1. **Dwell time** — how long people pause on your post before scrolling. A post that gets read (not just liked) ranks higher.
2. **Early engagement velocity** — likes, comments, and saves in the first 60-90 minutes after posting. Early engagement tells the algorithm the content is worth distributing.
3. **Save rate** — saves signal high-value content that people want to return to. Heavily weighted.
4. **Comment quality** — substantive comments (more than 5 words) outweigh emoji reactions.
5. **Connection strength** — engagement from 1st-degree connections matters more than strangers.

### Secondary signals

- **Repost rate** — reshares extend reach to new audiences. Reposts by people with large, relevant followings are disproportionately valuable.
- **Profile click-through** — if people click to view the poster's profile after reading, that's a strong authority signal.
- **Reply rate to comments** — responding to comments within 2 hours keeps the post active in feeds.

---

## What LinkedIn penalizes

- External links in the post body (moves the algorithm to suppress distribution)
- Engagement pods (artificial early spikes get filtered)
- Hashtag stuffing (3 or fewer hashtags is optimal)
- Low-quality engagement bait ("Comment YES if you agree")
- Posting frequency mismatch (posting too fast after a previous post)

---

## Format signals

| Format | Algorithm behavior | Best use |
|--------|-------------------|----------|
| Text-only post | Native to platform — favored | Insight, story, direct truth |
| Carousel (PDF) | High dwell time — very favored | Framework, list, educational |
| Image post | Moderate — depends on image quality | Hook + strong visual |
| Video | High reach, lower save rate | Founder personality, behind scenes |
| Poll | High early engagement, low save | Engagement posts only |

---

## Optimal posting windows (seed — update from Brew360)

| Day | Window | Reasoning |
|-----|--------|-----------|
| Monday | 07:30-08:30 | Professional mindset, first scroll of the week |
| Tuesday | 08:00-09:30 | Strong engagement day |
| Wednesday | 12:00-13:00 | Lunch break peak |
| Thursday | 07:30-09:00 | High creator activity day |
| Friday | 07:30-08:30 | Sharing mood, end of week |
| Sunday | 17:00-19:00 | Pre-week browsing |

---

## Hook optimization for dwell time

The first line is the only line visible before "see more." It must stop the scroll. LinkedIn shows approximately 140-200 characters before truncation.

Dwell time optimization:
- Hook that creates an open loop (question unanswered, tension unresolved)
- Short first line forces "see more" click — but only works if the hook earns it
- Numbered lists in hooks signal clear value ("3 things...")

---

## Engagement architecture

**Closing question types ranked by engagement quality:**

1. Specific operator question ("If you run a camp in [region], I'd genuinely like to know...")
2. Industry debate ("Do you think this changes in the next 5 years?")
3. Personal reflection ("When did you last check if your website speaks your guests' language?")
4. No question — weighted closing statement (generates saves, not comments; use for frameworks)

Avoid: "What do you think?", "Thoughts?", "Drop a comment below"

---

## May 2026 updates (from 360Brew deployment)

Key changes from seed intelligence:
- **External links penalty confirmed:** ~60% reach reduction. "Link in first comment" workaround is ALSO now penalized as of early 2026. No links in posts.
- **Daily posting penalized:** -45% reach vs. 2-3x/week. Wandar posts 4x/week — monitor for reach impact.
- **Saves weight elevated:** 5x more reach than a like. Design every post to be saveable.
- **Comment quality matters more:** Multi-sentence comments from industry people outweigh hundreds of generic likes.
- **PDF carousels dominate:** 21.77% median engagement. 3x more than video. Use for frameworks/lists.
- **Video underperforms:** -36% to -72% reach. Defer video until audience is larger.
- **First 60 minutes is the make-or-break window:** Monitor and respond to early comments immediately.

## Update this file

Run `refresh kb sources` to pull latest Brew360 and Richard van der Blom algorithm intelligence.
Check `knowledge-bank/algorithm-intel/brew360-latest.md` for the most recent Brew360 publication.
