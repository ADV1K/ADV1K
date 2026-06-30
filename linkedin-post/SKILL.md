---
name: linkedin-post
description: Turns Advik's raw content — blog drafts, project updates, scripts, hacks, demos — into short professional LinkedIn posts that match his personal brand voice. No corporate fluff. Use when you want to post about a project, hack, or technical find. Invoke with /linkedin-post and paste your raw content.
allowed-tools: Read
argument-hint: "[paste: raw content — blog, project update, script, hack, etc.]"
---

# LinkedIn Post Writer

Turns raw technical content into LinkedIn posts that sound like Advik — direct, specific, no fluff.

## Advik's Voice

Study these examples to calibrate:

**Example 1 (project update with diagram):**
```
Lately I've been building a Linux playground, a platform to spin up lightweight VMs with terminal access in the browser.
Each VM runs a custom Go-based init system and exposes a gRPC server over vsock.
The WebApp is built with Go + Templ + Tailwind + HTMX + xterm.js
A separate Go service manages Firecracker VMs, proxies commands over WebSocket, and handles VM lifecycle.

Let me know what you think!
```

**Example 2 (demo with features):**
```
After a short break, I'm back on my Linux playground project. It's finally coming together, so here's a short demo.

The idea: Boot temporary or permanent VMs from Docker images with both web and SSH access.

It has:
- Instant boot (1–2 seconds)
- Ingress & egress networking
- Unique IPv6 per VM (Airtel BTW)

And yes, this all runs on my potato home server.

Tech stack: Go, Firecracker, Templ, Tailwind, HTMX, xterm.js
```

**Voice rules — internalize these:**
- Lead with what it does, not what you feel about it
- Name the actual tech (gRPC over vsock, Firecracker, not "microservice architecture")
- One or two short paragraphs, then bullets if listing features
- End with tech stack as a one-liner OR a casual sign-off, not both
- Self-deprecating asides are good ("my potato home server", "Airtel BTW")
- No "excited to share", "thrilled to announce", "game-changer", "leverage"
- No hashtag walls — zero to two hashtags max, only if they add genuine discoverability
- No rhetorical questions as openers ("Have you ever wondered...")
- No call-to-action pressure ("Like and repost if you found this useful!")
- Numbers are good when real: boot time, lines of code, request latency

## Step 1 — Parse the input

Read the user's content. It may be:
- A rough brain-dump / notes
- A blog post draft (if it's announcing the blog, use format C; if it contains a standalone project or hack, extract and use format A or B)
- A project README section
- A short description of a script or hack
- A multi-part update about a project

If the content is very long (blog post, README), identify the ONE core thing worth posting about. Multiple features of the same project are NOT distinct — they belong in one post. Distinct means separate projects, unrelated hacks, or topics that would confuse a reader if combined. If there are multiple distinct post-worthy things, ask: "I see [X] and [Y] here — which should I focus on, or should I write one post covering both?" Then HALT and wait for the answer.

If the input is empty or fewer than ~15 words, ask: "Can you share more detail about what you built or did?" Then HALT.

## Step 2 — Extract the signal

Identify:
- **What was built / done / discovered** — the main fact
- **Why it's interesting / hard / unusual** — the hook
- **How it works** — specific technical details (protocols, tools, architecture decisions)
- **Stack / tools used**
- **Any numbers** — latency, size, count, duration
- **Personal color** — constraints, environment, self-deprecating context

Discard: vague adjectives, filler motivation, anything that sounds like a press release.

## Step 3 — Write the post

Structure options — pick whichever fits the content:

**A) Project update / demo:**
```
[One or two sentences: what it is and what it does — no preamble]

[Optional: "The idea:" or "How it works:" as a short paragraph]

It has:
- [feature with specifics]
- [feature with specifics]
- [feature with specifics]

[Optional one-liner aside — constraints, environment, funny detail]

Tech stack: [comma-separated list]
```

**B) Hack / technique / find:**
```
[What problem / what you noticed — one sentence]

[How you solved or approached it — 2-3 sentences, name the actual tools/APIs/approaches]

[Optional: result or takeaway as a single punchy line]
```

**C) Blog / article announcement (reluctant):**
```
[What the post is about in concrete terms — not "I wrote about X"]

[The ONE most surprising or useful thing from it — a real insight, not a tease]

[Link placeholder: drop your link here]
```

Use structure C when the user explicitly says they're sharing a blog post, or when the input is a blog draft without a standalone project/hack embedded in it. Otherwise default to A or B.

## Step 4 — Self-check before outputting

Before printing, confirm each of these and fix any failures in the post:
- Does it contain "excited", "thrilled", "game-changer", "leverage", "synergy", "journey"? → Remove or replace
- Does it open with a question? → Rewrite to open with a statement of fact
- Does the first sentence say what was built/done? → If not, restructure
- Are there more than 2 hashtags? → Cut to 2 or 0
- Does the tech stack appear? → Always include it unless the post is purely an observation or debugging find with no new tools
- Is it under ~200 words? → If over, cut aggressively: remove adjectives, context sentences, and asides before cutting specific technical nouns or numbers

## Step 5 — Output

Print the post in a code block so it's easy to copy, then one line below:

```
---
Word count: ~[N]
```

If you made any structural choices (e.g. used format B instead of A, cut a section), note it in one sentence after the word count — no more.

Do not ask "does this look good?" or offer multiple versions unprompted. Output one post. If the user wants changes, they'll say so.
