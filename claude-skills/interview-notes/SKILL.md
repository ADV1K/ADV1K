---
name: interview-notes
description: Researches a company from their website and JD, then generates structured HR screener prep notes: company summary, what they want, a personal pitch, common-question answers, questions to ask, and a logistics checklist. Use when you have an HR call coming up. Invoke with /interview-notes, then paste the company URL on the first line, then === on its own line, then the full JD.
allowed-tools: Read, Write, Bash, WebFetch
argument-hint: "<company-url> then === then <JD text>"
---

# Interview Notes

Prepares Advik for HR screener calls by researching the company and generating a ready-to-use prep doc.

## Output rules (apply everywhere, not just Step 6)

- No em dashes anywhere in output or logs. Use a comma, colon, or rewrite the sentence. Em dashes break clipboard parsing in downstream tools.
- No clichés ("passion for", "fast-paced", "leverage"). Plain words.
- Active voice. Specific over generic.

## Input format

Paste everything after invoking `/interview-notes`:

```
https://company.com
===
<full job description — paste as-is>
```

The `===` must be on its own line with nothing else.

If only a URL is provided with no `===`, generate a light company summary (Step 2 only) and stop.

## Step 1 — Parse input

Split the user's message on a line containing only `===` (trim surrounding whitespace).

- **Block 1** (before `===`): company URL. Trim whitespace. Take the first non-empty line as `{url}`. If Block 1 contains more than one non-empty line, stop and tell the user: "Block 1 has multiple lines — expected only the company URL. Extra lines found: [list them]. Please re-paste with only the URL before ===."
- **Block 2** (after `===`): job description text. Store as `{jd}`.

If no `===` is found: if the entire input starts with `http`, generate a light company summary (Step 2 only) and stop. Otherwise, halt and tell the user the expected format.

**ATS detection:** Check whether `{url}`'s hostname is a known applicant tracking system: `greenhouse.io`, `lever.co`, `workday.com`, `ashbyhq.com`, `bamboohr.com`, `myworkdayjobs.com`, `jobs.lever.co`, `boards.greenhouse.io`, or any domain that is clearly a job board rather than the company's own site. If it is, halt and ask: "That URL looks like an ATS job posting, not the company's own site. What is the company name and their actual website URL? (e.g. https://stripe.com)" Wait for the user's reply, then set `{company}` and `{company_url}` from their answer. Otherwise, infer `{company}` from the hostname: strip `www.` and any other common subdomains, take the first meaningful segment, title-case it. Store the company's own website as `{company_url}` (same as `{url}` when not ATS).

## Step 2 — Research the company

Fetch `{company_url}` with WebFetch. Extract:

- **What they build**: product or service in one sentence.
- **Who they serve**: target customer / market.
- **Mission or tagline**: their stated purpose, if findable.
- **Stage and size**: startup / growth / enterprise, headcount or funding if visible on the page.
- **Recent signals**: news, launches, or blog posts visible on the homepage or linked from it. If nothing recent is surfaced, omit this field.
- **Culture cues**: language used about team, values, ways of working.

If the fetch fails or returns no parseable content, write "(site unavailable — research skipped)" for all fields and continue using JD signals only.

Do not fabricate details that are not on the page.

## Step 3 — Read resume and context

Read `~/fun/adv1k/job-search/customize.toml`. It uses top-level TOML keys: `resume_path` and `context_file`. If the file is missing or either key is absent, use defaults: `resume_path = ~/fun/adv1k/resume.toml`, `context_file = ~/fun/adv1k/job-search/context.md`.

Read the resume at `resume_path`. It is a TOML file. Relevant top-level structures:
- `[[experience]]` entries: each has `name` (company), `role`, `date` (range string), and a list of bullets describing what was done.
- `[[projects]]` entries: each has `name` and a list of bullets.
- Top-level `skills` or similar keys if present.

If the file is missing, halt: "Resume not found at {resume_path} -- check the path."

Check for a context file at `context_file`. If it exists, read it. It is a markdown file with these sections:
- `## Resume Narrative`: `###` subsections per role with richer prose than the resume bullets.
- `## Projects Deep Dive`: `###` subsections per project with technical depth.
- `## Blog Posts`: summaries of published writing.
- `## Additional Material`: anything else (talks, certs, open source).

Store all sections for use in Step 5.

## Step 4 — Analyze the JD

Ignore filler ("fast-paced", "collaborative environment", "passion for excellence"). Focus on hard signals.

Extract **3-5 requirements** max. Lead with tech stack or domain skills, end with soft signals and collaboration patterns. Pack each line: skill/domain + what they actually want from it.

```
**What they're looking for:**
- Kubernetes, Helm -- production ops ownership, not just deployment scripts
- Observability (Prometheus, Grafana, OpenTelemetry) -- own the signal quality
- Incident response -- structured runbooks and post-mortems, not ad-hoc firefighting
- Cross-functional communication -- explaining infra decisions to non-infra engineers
```

Map each requirement against the resume silently:

| Match type | How to handle |
|------------|---------------|
| **Direct match** | Use confidently in answers |
| **Adjacent/partial** | Bridge: related experience + ramp-up speed |
| **No coverage** | Log as gap, skip in answers |

Bridging rules: never invent a job title, company, or metric not in the resume. Frame adjacent tools as related work. Use fast-learner framing where real.

**Fit score formula:** Let Y = total requirements extracted (from the 3-5 list), X = direct matches, Z = adjacent matches.
- Strong: X >= Y - 1
- Decent: X >= ceil(Y / 2)
- Stretch: otherwise

Output one line: `Fit: X/Y direct, Z adjacent -- [strong / decent / stretch]`

## Step 5 — Build the prep doc

Generate each section below in order.

### 5a — Tell me about yourself (60-90 second pitch)

Write a first-person narrative, 4-6 sentences:

1. One sentence on current or most recent role and what you actually did (not just title).
2. One sentence connecting a key skill or project directly to what this role needs.
3. One sentence on why you're making this move now (forward-looking, no badmouthing).
4. One sentence closing on why this company specifically.

Use plain language. Specific beats generic.

If context.md was loaded in Step 3, prefer `## Resume Narrative` subsections over raw resume bullets for richer language.

### 5b — Why this company / why this role?

Write 3 numbered short points, 1-2 sentences each, conversational:

1. **Direct honest reason** -- what genuinely appeals about the product or problem space.
2. **Domain or product point** -- specific to what they build and who they serve (use Step 2 research).
3. **Growth or culture point** -- what the company's stage or signals say about how you'd grow there.

If Step 2 research was unavailable, draw from JD signals only and note that.

### 5c — Why are you leaving / why did you leave?

Check the resume: does the most recent `[[experience]]` entry have an end date in the past, or is it ongoing?

- **Currently employed**: frame as forward-looking ("I've learned X at Y; now I'm looking for Z").
- **Between jobs**: frame as past tense ("I left Y because X; I've been looking for a role where Z").

Either way: never criticize the previous employer. One short paragraph.

### 5d — What are you looking for in your next role?

One short paragraph connecting stated preferences to what this role offers. Honest, not a mirror of the JD verbatim.

### 5e — Resume examples ready to deploy

For each JD requirement with a direct or adjacent match, write a STAR-format note the user can use if the topic comes up:

```
**[Requirement]**
S/T: [situation and task in one phrase]
A: [what you did]
R: [outcome -- number or observable change if available]
```

Use specific numbers and details from resume and context.md. For adjacent matches, add one bridging sentence: "I haven't used X directly, but Y covered the same ground in Z way."

### 5f — Salary / logistics

Infer role seniority from the JD title and requirements. Write:

- **Salary range**: a reasonable range to give if asked. State it as a range. Add: "(based on training data -- verify against current market before the call, e.g. Levels.fyi or Glassdoor for this role level and location)".
- **Notice period**: check resume for current role status. If actively employed, use "2-4 weeks standard" unless the resume shows otherwise. If between jobs, note "available immediately or [date]".

### 5g — Questions to ask them

Write 3 questions, each genuinely useful for evaluating fit. Tie at least one to Step 2 company research and one to JD signals. Avoid generic filler.

```
1. [Question] -- why this is worth asking
2. [Question] -- why this is worth asking
3. [Question] -- why this is worth asking
```

### 5h — Logistics checklist

```
[ ] Interviewer name confirmed: ___
[ ] Time zone and dial-in/link confirmed
[ ] Audio tested
[ ] Camera / background checked (if video)
[ ] Quiet space arranged
[ ] Resume open in front of you
[ ] This prep doc open in front of you
[ ] Join 3-5 minutes early
```

## Step 6 — Output

Print in this order. No em dashes anywhere.

```
## Company: {Company}

**What they build:** [one sentence]
**Who they serve:** [one sentence]
**Stage:** [startup/growth/enterprise + size signal if any]
**Culture cues:** [1-2 phrases]
**Recent signals:** [if any, else omit this line]

---

**What they're looking for:**
[Step 4 list]

Fit: X/Y direct, Z adjacent -- [strong / decent / stretch]

---

## Prep Notes

### Tell me about yourself
[Step 5a]

---

### Why this company / why this role?
[Step 5b]

---

### Why are you leaving / why did you leave?
[Step 5c]

---

### What are you looking for?
[Step 5d]

---

### Resume examples to have ready
[Step 5e -- one block per requirement]

---

### Salary / logistics
[Step 5f]

---

### Questions to ask them
[Step 5g]

---

### Logistics checklist
[Step 5h]
```

## Step 7 — Save interview file

Slugify `{company}`: lowercase, replace spaces and special characters with hyphens.

**Save path:** `~/fun/adv1k/interview-notes/interviews/`

**Filename:** `{company-slug}.txt`

Create the directory if needed: `mkdir -p ~/fun/adv1k/interview-notes/interviews/`.

Extract the following from earlier steps:
- `{role_name}`: job title from the JD
- `{experience_range}`: years of experience required as stated in JD (e.g. "1-3 years"); if not stated, write "not specified"
- `{jd_salary_range}`: advertised salary range from JD, or "not disclosed"
- `{my_salary_range}`: the range computed in Step 5f (e.g. "16-22 LPA")
- `{my_salary_justification}`: one short phrase explaining the range -- derive from company stage, funding, location, and role seniority (e.g. "bootstrapped startup, India SRE market, 1-3yr exp")
- `{responsibilities}`: key responsibilities from JD as a bullet list, max 6 bullets, plain language
- `{technical_skills}`: bullet list of skills from resume that directly match the JD requirements, no prose
- `{delivered}`: bullet list of 3-5 key achievements from resume and context.md most relevant to this role -- one line each, include a number or observable result where available
- `{questions}`: the 3 questions from Step 5g, numbered, question only (no "why this is worth asking" annotation)
- `{logistics}`: the checklist from Step 5h

Write the file in this exact format. No em dashes anywhere in the file.

```
{Company}
{company_url}

Role: {role_name}
Experience: {experience_range}
Their salary range: {jd_salary_range}
My ask: {my_salary_range} ({my_salary_justification})

Responsibilities:
- [bullet 1]
- [bullet 2]
...

--- PREP NOTES ---

Technical skills:
- [skill matching JD requirement]
- [skill matching JD requirement]
...

What I've delivered:
- [achievement with number or result]
- [achievement with number or result]
...

Questions to ask:
1. [question]
2. [question]
3. [question]

Logistics:
[ ] Interviewer name confirmed: ___
[ ] Time zone and dial-in/link confirmed
[ ] Audio tested
[ ] Camera / background checked (if video)
[ ] Quiet space arranged
[ ] Resume open in front of you
[ ] This prep doc open in front of you
[ ] Join 3-5 minutes early
```

After writing, verify the file exists: `ls ~/fun/adv1k/interview-notes/interviews/{company-slug}.txt`. If the file is not found, report: "Save failed -- file not found at expected path. Check permissions." Otherwise print: `Saved -> ~/fun/adv1k/interview-notes/interviews/{company-slug}.txt`
