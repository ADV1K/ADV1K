---
name: job-search
description: Analyzes a job description against Advik's resume, extracts what the company is looking for, and generates polished human-sounding answers to job portal screening questions. Use when applying to a job and need to answer portal questions or assess fit. Invoke with /job-search and paste the JD, then ===, then numbered questions.
allowed-tools: Read, Write, Bash, AskUserQuestion, WebFetch
argument-hint: "[JD text === Q1: ... Q2: ... (NOTE: extra context, TONE: override)] or REFRESH-CONTEXT [blog=URL1,URL2]"
---

# Job Search Assistant

Helps Advik apply to jobs by analyzing JDs against his resume and writing polished screening answers.

## Input format

Paste everything after invoking `/job-search`. Use `===` on its own line to separate the job description from your questions:

```
<job description — paste as-is>
===
1. Why do you want to work here?
2. Describe your experience with Kubernetes.
NOTE: mention the infra migration project
TONE: startup casual
```

To build or refresh the context file, use: `REFRESH-CONTEXT [blog=URL1,URL2]`

If you only paste a JD (no `===`), see Step 1.

## Step 1 — Parse input

**REFRESH-CONTEXT check (run before anything else):**
If the entire input (trimmed) starts with `REFRESH-CONTEXT` (case-insensitive), parse the optional `blog=URL1,URL2` argument and early-exit to the REFRESH-CONTEXT step. Do not proceed with normal parsing.

Split the user's message on a line containing only `===` (trim surrounding whitespace).
- **Block 1** (before `===`): job description
- **Block 2** (after `===`): screening questions — parse as a numbered list

After parsing Block 2:
- Scan for lines starting with `NOTE:` (case-insensitive). Collect as `{extra_context}`, remove from questions list.
- Scan for a line starting with `TONE:`. If found, use that value as `{tone_override}` and remove the line. This skips Step 5 tone detection.

**If no `===` line is found:** Use `AskUserQuestion` with:
```json
{
  "question": "No questions found — what would you like?",
  "options": ["Fit analysis only", "Fit analysis + write a pitch"]
}
```
Do not proceed to Step 2 until they answer.

Note: the REFRESH-CONTEXT check at the top of this step only fires when the entire input starts with that keyword. If it does not, this step continues normally regardless of any other keywords present.

## Step 2 — Read resume and context

Read `~/fun/adv1k/job-search/customize.toml` to get configured paths. If the file is missing or a key is absent, use defaults: `resume_path = ~/fun/adv1k/resume.toml`, `context_file = ~/fun/adv1k/job-search/context.md`.

Read the resume from the configured `resume_path`. If the file is missing, halt: "Resume not found at {resume_path} — please check the path."

After reading resume.toml, check for a context file at the configured `context_file` path.
- If it exists: read it and note "Loaded: resume.toml + context.md (N sections)" where N is the count of `##` headings. Store all section content for use in Step 4.
- If it does not exist: continue silently — no error, no mention.

## Step 3 — What they're looking for

Analyze the JD. Ignore filler ("fast-paced", "passion for excellence"). Focus on hard signals.

Output **3-5 points max**. Lead with tech stack, end with soft skills and collaboration signals. Pack each line: tool/skill name + what they actually want from it.

```
**What they're looking for:**
- Node.js, GraphQL, PostgreSQL — backend feature ownership, not just integration
- Scripting and data work — analytics queries, migration scripts, cron jobs
- AWS (Lambda, SQS, CloudWatch) — infra exposure, nice to have
- End-to-end ownership — scoping through post-release, not just tickets
- Cross-functional mindset — tight loop with Product, QA, and Support
```

## Step 4 — Resume match

Map each requirement against the resume silently:

| Match type | How to handle |
|---|---|
| **Direct match** | Use it confidently in answers |
| **Adjacent/partial** | Bridge: frame related experience + emphasize ramp-up speed |
| **No coverage** | Skip in answers, log the gap |

**Bridging rules:**
- Never invent a job title, company, or metric that isn't in the resume
- Never claim direct production use of something never mentioned
- DO frame adjacent tools as related work: Envoy experience applies to service mesh concepts in Istio
- DO use the fast-learner framing where it's real: Advik has shipped across infra, backend, and observability stacks quickly

**Context enrichment:** If context.md was loaded in Step 2, use its sections as supplementary evidence:
- `## Resume Narrative` subsections: when writing about a matching experience, prefer specific language and detail from here over the raw TOML bullets — it's richer
- `## Blog Posts`: if a post covers a relevant skill or project, use it to add depth to adjacent-match framing
- `## Projects Deep Dive`: pull from here when a project is directly relevant to a JD requirement
- `## Additional Material` and any other sections: treat as fair game — pull from them when relevant to a specific requirement

**Fit score:** Count matches silently. Output one line after Step 3:
```
Fit: X/Y direct matches, Z adjacent — [strong / decent / stretch]
```
Where Y = total JD requirements mapped, X = direct hits, Z = bridgeable gaps.

## Step 5 — Tone detection

Skip this step if `{tone_override}` was set in Step 1 — use that value directly.

Otherwise scan the JD for register markers and set `{tone}`:
- Emoji, "you'll own", "no fluff", "move fast" → **startup casual**: direct, first-person, energetic
- "The successful candidate", "responsibilities include", compliance/legal language → **enterprise formal**: polished, measured
- Default to professional but human when ambiguous

## Step 6 — Write answers

Classify each question before writing:

| Question type | Format |
|---|---|
| **Interest / motivation** (why this company, what attracts you, why this role) | 3-4 numbered short points, 1-2 sentences each, conversational |
| **Behavioral** (tell me about a time, describe a situation) | Prose, 3-5 sentences, first person |
| **Skills / stack** (describe your experience with X) | Prose intro + bullet list of relevant items |

**Interest/motivation format — target this style:**
```
1. [Direct honest reason — why this type of work or company genuinely appeals]

2. [Domain or product point — specific to what they build and who uses it]

3. [Growth or culture point — what the company's structure or roadmap signals]
```

**Writing rules:**
- Active voice. "I built X" not "X was built."
- Address the company directly when natural. "I'd bring X to your team."
- Short punches mixed with medium elaboration. No walls of text.
- Real language. Not corporate script.
- Plain words. "Improve" not "leverage." "Fix" not "remediate." "Problem" not "challenge space."
- No clichés or jargon. Back every claim with something specific.
- No semicolons. No em dashes. No emojis. No hashtags. Standard punctuation only.
- If `{extra_context}` is non-empty, apply each NOTE as an additional constraint.

**Answer template:**

```
**Q1: [question text]**

[answer]

---
```

## Step 7 — Output

Print in this order:

1. `**What they're looking for:**` list (Step 3 output)
2. Fit score line (Step 4)
3. Blank line + `---`
4. Each answer block (Step 6), separated by `---`

## Step 7.5 — Why hire me?

Always generate this section.

Draw from the strongest resume-to-JD matches. Write 4-6 tight bullet points. Each bullet names a specific skill, project, or pattern from the resume and connects it directly to something the JD asks for. No filler.

```
---

**Why hire me:**
- [specific match — direct connection to JD requirement]
```

## Step 8 — Log the session

**Infer company name** from the JD. Slugify it (lowercase, hyphens). If unclear, use `unknown`.

**Log path:** `~/fun/adv1k/job-search/logs/`

**Filename:** run `date +%Y-%m-%d-%H%M%S`, then `{timestamp}-{company}.md`.

**Before writing:** run `ls ~/fun/adv1k/job-search/logs/{filename} 2>/dev/null` — if exists, append `-2`, `-3`, etc.

Create the logs directory if needed (`mkdir -p`).

**Log format:**

```markdown
# Job Application Log — {Company} — {Date}

## Job Description

{full JD text}

## Questions

{questions text, NOTE and TONE lines removed}

## Extra Context (NOTEs)

{extra_context lines, or "none"}

## Tone

{tone label}

## What They're Looking For

{Step 3 output}

## Fit Score

{Step 4 fit score line}

## Answers

{Step 6 output — all answer blocks}

## Why Hire Me

{Step 7.5 output}

## Gaps (not surfaced in answers)

{requirements with no resume coverage, or "none"}
```

After writing, print: `Log saved → ~/fun/adv1k/job-search/logs/{filename}`

## REFRESH-CONTEXT step

Triggered when input starts with `REFRESH-CONTEXT` (case-insensitive). Builds or updates `~/fun/adv1k/job-search/context.md`.

**1. Load sources:**
- Read `customize.toml` (at `~/fun/adv1k/job-search/customize.toml`) for defaults: `context_file`, `resume_path`, `blog_urls`. If the file is missing, use defaults: `context_file = ~/fun/adv1k/job-search/context.md`, `resume_path = ~/fun/adv1k/resume.toml`, `blog_urls = []`
- If `context.md` already exists, read its frontmatter for stored `blog_urls` and `resume_path`. If frontmatter is missing or malformed, treat as no stored sources and use customize.toml defaults
- If `blog=URL1,URL2` was passed as an argument, merge those URLs with any from `customize.toml` and existing frontmatter (deduplicate)
- If `resume.toml` is missing: halt — "Resume not found at {resume_path} — check the path."

**2. Generate auto-generated sections:**

Read `resume.toml`. For each `[[experience]]` entry, write a `### {role} at {name} ({date})` subsection under `## Resume Narrative` with a short narrative paragraph (2-3 sentences) expanding on the bullet points — tell the story, not just the facts.

For each `[[projects]]` entry, write a `### {name}` subsection under `## Projects Deep Dive` with a 2-3 sentence paragraph on what was interesting or technically hard about it.

For each blog URL, use `WebFetch` to fetch the page, extract the main content (ignore nav/footer/boilerplate), and write a `### {page title}` subsection under `## Blog Posts` with a 2-3 sentence summary of the key technical point. If a URL is unreachable, returns no parseable content, or fails for any reason, write `(fetch failed — check URL)` under that subsection and continue to the next URL.

**3. Check for existing file:**

If `context.md` already exists:
- Compare the newly generated auto-generated sections to the current ones in the file
- If different: show what would change in the auto-generated sections and ask `[O] Overwrite | [A] Abort`
- If unchanged: print "No changes to auto-generated sections." and stop
- Human-owned sections are never included in the diff or overwritten. A section is human-owned when its first HTML comment immediately after the `##` header contains the exact text `human-owned` (hyphenated). Variants without a hyphen or on non-adjacent lines do not qualify

**4. Write the file:**

```markdown
---
resume_path: ~/fun/adv1k/resume.toml
blog_urls:
  - {url1}
generated: {today's date YYYY-MM-DD}
---

# Job Search Context

## Resume Narrative
<!-- auto-generated — rebuilt by REFRESH-CONTEXT -->

{experience subsections}

## Projects Deep Dive
<!-- auto-generated — rebuilt by REFRESH-CONTEXT -->

{project subsections}

## Blog Posts
<!-- auto-generated — rebuilt by REFRESH-CONTEXT from blog_urls in frontmatter -->

{blog post summaries, or "(none — add blog URLs via: /job-search REFRESH-CONTEXT blog=URL)" if no URLs}

## Additional Material
<!-- human-owned — REFRESH never modifies this section -->
<!-- Add: talks, certs, open source contributions, POCs, anything not in resume.toml -->

{preserve existing content verbatim if file existed, otherwise leave blank}
```

When updating an existing file: regenerate auto-generated sections only. Preserve human-owned sections verbatim.

**5. Confirm:**

Print: `Context refreshed → ~/fun/adv1k/job-search/context.md`

List each section written with a line count. If blog URLs were added or changed, confirm they are saved to frontmatter.
