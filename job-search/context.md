---
resume_path: ~/fun/adv1k/resume.toml
blog_urls: []
generated: 2026-07-01
---

# Job Search Context

## Resume Narrative
<!-- auto-generated — rebuilt by REFRESH-CONTEXT -->

### SRE-1 at One2N (Dec 2025 – July 2026)

At One2N I built the infrastructure testing platform for Sherlocks.ai, an AI SRE product. The core challenge was making the AI's test environment indistinguishable from a real production incident — so I provisioned ephemeral EKS, ECS, and EC2 stacks via Terraform, broke them in controlled ways (crash loops, OOM kills, network partitions, cert failures), and wired up the same distributed tracing, metrics, and logs the AI would see on a real incident. The goal was not just to test the AI's detection but its ability to diagnose and remediate — so the signal quality had to be production-grade.

### SRE Intern at Aftershoot AI (Feb 2024 – June 2024)

Aftershoot is an AI photo editing tool for photographers. My biggest win there was profiling their Python image processing pipeline with flamegraphs and finding that thumbnail generation was synchronously blocking the upload queue. Parallelizing it with a thread pool cut end-to-end workflow time by 20%. I also set up their full observability stack — Prometheus, Grafana, Loki, OpenTelemetry — across their Go microservices and wrote integration tests against Staging Postgres and Redis that brought coverage to 85% and measurably reduced post-deployment support tickets.

### SDE Intern at Credible Informatics (May 2023 – Jan 2024)

I built an AI stock research dashboard where retail investors could ask free-form questions about any company and get GPT answers grounded in real earnings transcripts, financial news, and YouTube commentary. The interesting part was the data layer: Scrapy crawlers ingesting 10+ financial sources on a cron schedule, OpenAI embeddings stored in a vector DB, and Redis caching to keep API latency under 200ms. I also shipped a Telegram bot for daily AI-generated portfolio digests and deployed the whole stack to fly.io via GitHub Actions with Sentry for production error tracking.

### SDE Intern at The One World (Apr 2022 – Oct 2022)

My first real production backend work. I migrated 12 REST endpoints from AWS Amplify to FastAPI — the main motivation was eliminating cold start overhead, which cut infrastructure costs by 35% and API latency by 60%. The most technically interesting part was a PostGIS query with GIST indexing over 5,000+ shop locations for proximity-based discovery, hitting sub-500ms under concurrent load. I also implemented JWT and Google OAuth 2.0 for a neighborhood society app with 1,000+ residents.

## Projects Deep Dive
<!-- auto-generated — rebuilt by REFRESH-CONTEXT -->

### Linux Playground

Linux Playground lets you spin up lightweight Linux VMs in the browser with full terminal access, booting in 1-2 seconds using Firecracker microVMs. The interesting part was the Go init system I wrote for the microVM — it runs inside the VM and handles gRPC commands sent over vsock from the host. A separate Go service on the host manages VM lifecycle and proxies terminal I/O over WebSocket to the xterm.js frontend. The fun constraint was that vsock is the only communication channel between host and guest — everything has to go through it.

### Protohacks

Protohacks is a set of network programming challenges from protohackers.com — I solved them in Go and Python. The real output wasn't just the solutions: I ended up writing a small framework for building async TCP/UDP servers with route handling and multiple dispatch strategies, and a binary serialization library in Python using type hints to define message layouts. It's a good example of how I learn — I don't just solve the problem, I look for the reusable abstraction underneath.

## Blog Posts
<!-- auto-generated — rebuilt by REFRESH-CONTEXT from blog_urls in frontmatter -->

(none — add blog URLs via: /job-search REFRESH-CONTEXT blog=URL)

## Additional Material
<!-- human-owned — REFRESH never modifies this section -->
<!-- Add: talks, certs, open source contributions, POCs, anything not in resume.toml -->
