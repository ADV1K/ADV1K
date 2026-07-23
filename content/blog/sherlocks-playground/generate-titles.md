# Blog Title Generator — Sherlocks Playground Post

## Your Task

Generate a ranked shortlist of blog post titles for a technical blog post about the Sherlocks.ai playground infrastructure project. The titles should lead with the platform engineering achievement, not just the observability layer.

## Step 1: Load Context

Read these files in full before doing anything else:

1. `content/blog/sherlocks-playground/summary.txt` — what was built, the bigger picture, and the intended angles for the blog post.
2. `content/blog/sherlocks-playground/code/.planning/codebase/**.md` — Code context

## Step 2: Research the Blog's Voice

Fetch https://one2n.io/blog and read it carefully. Note:

- The tone and register of existing titles (punchy vs. descriptive, first-person vs. neutral, question-based vs. declarative)
- The technical depth signaled in titles (does the audience skew practitioner or manager?)
- Any recurring patterns in how they frame "we built X" posts vs. "we learned Y" posts
- The length and style of titles that appear most prominently

If individual blog post pages are accessible from that index, read 2–3 representative posts to get a feel for the prose style and what kind of hook they use in openers.

## Step 3: Generate Titles

Produce 12–15 candidate titles across these angles. Label each with its angle:

- **Platform Engineering** — lead with what was built (the multi-substrate chaos playground, the IaC, the nuke-and-pave lifecycle)
- **AI SRE** — lead with the "why" (Sherlocks.ai needed a realistic environment to train/demo an AI SRE)
- **Chaos Engineering** — lead with the chaos/fault-injection framing
- **Practitioner Insight** — "here's what we learned / here's what surprised us" framing
- **Provocation** — contrarian or opinionated take that challenges a common assumption (e.g., "your demo cluster is a lie")

## Step 4: Rank and Recommend

After listing all candidates, recommend your top 3 with one sentence explaining why each works for the one2n.io audience and the subject matter. Factor in:

- Whether the title matches the blog's existing voice
- Whether it signals the right technical depth
- Whether it earns a click from an SRE or platform engineer scrolling a feed

## Constraints

- Do not write the blog post itself — titles and recommendation only.
- Titles should be under 90 characters.
- Avoid generic words: "journey", "deep dive", "comprehensive", "ultimate guide".
- At least 3 titles should be usable as-is without further editing.
