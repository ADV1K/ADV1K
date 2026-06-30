---
name: job-search
description: Analyzes a job description against Advik's resume, extracts what the company is looking for, and generates polished human-sounding answers to job portal screening questions. Use when applying to a job and need to answer portal questions or assess fit. Invoke with /job-search and paste the JD, then ===, then numbered questions.
allowed-tools: Read, Write, Bash
argument-hint: "[paste: job description === questions]"
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
3. Tell us about a time you improved system reliability.
```

If you only paste a JD (no `===`), ask: "No questions found — should I just do the fit analysis, or also write a short pitch?"

## Step 1 — Parse input

Split the user's message on a line containing only `===` (trim surrounding whitespace).
- **Block 1** (before `===`): job description
- **Block 2** (after `===`): screening questions — parse as a numbered list

**If no `===` line is found:** HALT. Ask the user: "No questions found — should I just do the fit analysis, or also write a short pitch?" Do not proceed to Step 2 until they answer.

## Step 2 — Read resume

Read the resume from: `~/fun/adv1k/resume.toml`

If the file is missing, halt and say: "Resume not found at ~/fun/adv1k/resume.toml — please check the path."

## Step 3 — What they're looking for

Analyze the JD. Extract the real signal: ignore filler ("fast-paced environment", "passion for excellence"), focus on:
- Hard skills and tools explicitly named
- Seniority signals (owns, leads, designs, mentors)
- Domain context (infra, backend, ML, fintech, etc.)
- Soft-skill intent (ownership, on-call, cross-functional)

Output a tight list — no more than 10 items, keyword + 2-4 word intent:

```
**What they're looking for:**
- Kubernetes — owns cluster ops in prod
- Terraform — provisions infra, not just reads it
- On-call / incident response — actual ownership
- Observability (metrics, traces, logs) — not just setup, tuning too
- Go or Python — primary service language
```

## Step 4 — Resume match

Map each requirement against the resume silently:

| Match type | How to handle |
|---|---|
| **Direct match** | Use it confidently in answers |
| **Adjacent/partial** | Bridge: frame related experience + emphasize speed of ramp-up |
| **No coverage** | Skip in answers, log the gap |

**Bridging rules:**
- Never invent a job title, company, or metric that isn't in the resume
- Never claim direct production use of something never mentioned
- DO frame adjacent tools as "related work": e.g. Envoy experience → "service mesh concepts from working with Envoy directly apply to Istio"
- DO invoke the fast-learner framing where real: Advik has shipped across infra, backend, and observability stacks quickly — that's a real pattern, use it

## Step 5 — Tone detection

Scan the JD for register markers and set `{tone}`:
- Emoji, "we move fast", "you'll own", "no fluff" → **startup casual**: direct, first-person, energetic
- "The successful candidate", "responsibilities include", compliance/legal language → **enterprise formal**: polished, third-person-aware, measured
- Default to professional but human when ambiguous

Record the detected tone label (e.g. "startup casual") — it will be saved in the log.

## Step 6 — Write answers

For each numbered question, write one answer block.

**Format rules:**
- Open-ended / behavioral questions → prose, 2-4 sentences, first person, no bullet points
- "Describe your skills / tools / stack" questions → prose intro + bullet list of relevant items
- Keep answers focused — no padding, no generic claims without backing
- Sound like a sharp engineer writing for a human recruiter, not a bot filling a form

**Answer template:**

```
**Q1: [question text]**

[answer]

---
```

## Step 7 — Output

Print in this order:

1. `**What they're looking for:**` list (Step 3 output)
2. Blank line + `---`
3. Each answer block (Step 6), separated by `---`

## Step 8 — Log the session

After outputting answers, write a log file.

**Infer company name** from the JD (look for company name in the first paragraph or job title line). Slugify it (lowercase, hyphens). If unclear, use `unknown`.

**Log path:** `~/fun/adv1k/job-search/logs/`

**Filename:** run `date +%Y-%m-%d-%H%M%S` to get a timestamp, then `{timestamp}-{company}.md`.

**Log format:**

```markdown
# Job Application Log — {Company} — {Date}

## Job Description

{full JD text}

## Questions

{full questions text}

## What They're Looking For

{Step 3 output}

## Tone

{tone label from Step 5}

## Answers

{Step 6 output — all answer blocks}

## Gaps (not surfaced in answers)

{list of requirements with no resume coverage, or "none"}
```

**Before writing:** run `ls ~/fun/adv1k/job-search/logs/{filename} 2>/dev/null` — if the file already exists (same-second re-run), append `-2`, `-3`, etc. to the filename until the path is free.

Create `~/fun/adv1k/job-search/logs/` if it doesn't exist (`mkdir -p`).

After writing the log, print one line: `Log saved → ~/fun/adv1k/job-search/logs/{filename}`
