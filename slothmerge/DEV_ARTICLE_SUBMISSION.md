---
title: "I stopped reviewing PRs after 8 PM: How an open Gemma agent audits diffs while I sleep"
published: true
tags: devchallenge, hf26challenge, gemma, opensource
cover_image: https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/on69ffi3qy5oi08zekrf.png
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady](https://dev.to/challenges/hacktoberfest-week3-2026-10-19)*

---

It was 8:45 PM on a Wednesday. My eyes hurt from staring at terminal logs all day, my brain was completely fried, and my dinner was getting cold.

Then came the Slack notification:  
*"Hey! Just opened a quick PR for user auth and DB pooling. Only 380 lines. Mind doing a fast review before tomorrow's release?"*

We've all been there. You know you should check every SQL string interpolation, verify async error boundaries, and hunt down unhandled null pointer exceptions. But your inner sloth is screaming: **"I just want to lie on the couch and watch YouTube."**

In previous years, being lazy meant either rubber-stamping the PR with a blind *"LGTM, ship it"* (and getting woken up by PagerDuty at 3 AM when production explodes), or spending an exhausting hour nitpicking code when you'd rather be resting.

So for **Hacktoberfest Week 3 (Slow & Steady / International Sloth Day)**, I channeled my inner sloth and built **SlothMerge: The Ghost PR Reviewer**.

---

## 01. What I Built

**SlothMerge** is an autonomous open-source AI code review agent powered by **Google Gemma 2** and instrumented with **Sentry Agent Tracing**.

It intercepts raw git diffs and GitHub pull requests while you rest. It performs a multi-pass security and sanity audit on your local machine, and delivers:

1. **The Sloth Verdict:** An instant, definitive status—`[STATUS: APPROVED · SAFE TO MERGE]`, `[STATUS: NEEDS DISCUSSION]`, or `[STATUS: BLOCKED · CHANGES REQUESTED]`.
2. **The 3-Bullet Executive Digest:** A hyper-dense summary of what actually changed, so you don't have to read 400 lines of diffs.
3. **Pinpointed Vulnerability Flags:** Exact file names, offending lines, explanations, and copy-pasteable replacement code for security landmines (SQL injections, leaked tokens, unhandled async crashes).
4. **Copy-Paste GitHub PR Comment:** A ready-to-publish Markdown review formatted for GitHub.

```text
[ Git PR Diff ]
       │
       ▼
┌──────────────────────────────────────┐
│       SlothMerge Agent Core          │
│  ├─ Unified Diff Parser & Hunk Split │
│  ├─ Sentry Agent Tracing Telemetry   │
│  └─ Security & Concurrency Rules     │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│       Google Gemma 2 Pipeline        │
│   (Local Inference / Open-Weights)   │
│  ├─ SQLi & Auth vulnerability scan   │
│  ├─ Async error boundary checks      │
│  └─ "Laziness Verdict" computation   │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│           The Sloth Report           │
│  ├─ 3-Bullet Morning Digest          │
│  ├─ Offending Line & Suggested Fix   │
│  ├─ Pre-formatted GitHub Comment     │
│  └─ Sentry Latency & Cost Metric     │
└──────────────────────────────────────┘
```

---

## 02. Demo & Interactive Walkthrough

You can run SlothMerge interactively in your browser or run it directly in your terminal/git hooks:

### Interactive Web Dashboard
Paste any unified git diff, or test one of the pre-loaded real-world scenarios:
- **Scenario 1: SQL Injection & Leaked Secret** (Catches raw f-string SQL queries and committed GitHub PATs).
- **Scenario 2: Unhandled Async Network Crash** (Detects missing try/except blocks in coroutines).
- **Scenario 3: Clean Tested Refactor** (Instant Sloth Approval with zero human effort needed).

### Terminal & Git CLI Mode
You can also run it straight from the terminal or pipe your uncommitted work into it:

```bash
# Review a patch file
python cli.py samples/pr1_sql_injection.diff

# Audit uncommitted changes before pushing
git diff | python cli.py
```

Sample Terminal Output:
```markdown
## SlothMerge Audit Report

> **Verdict:** [STATUS: BLOCKED · CHANGES REQUESTED] (Confidence: 96%)  
> **Summary:** Reject and request changes. Found critical security vulnerabilities that could compromise production data.  
> **Estimated Review Time Saved:** ~25 minutes

### Executive Summary
- Modified 1 file(s) with +7 additions and -3 deletions.
- Refactored logic inspected across security boundaries, async calls, and syntax integrity.
- Auto-audited via open-weight model pipeline with zero cloud data retention.

### Critical Findings
#### 1. [CRITICAL] SQL Injection in Database Query
- **File:** `services/user_service.py`
- **Issue:** Direct f-string SQL query execution. User input is interpolated directly without parameterized queries.
- **Offending Line:** `query = f"SELECT id, username, email FROM users WHERE email = '{email}'"`
- **Suggested Fix:**
```python
cursor.execute("SELECT id, username, email FROM users WHERE email = %s", (email,))
```
```

---

## 03. Code Architecture

The entire codebase is open-source under the MIT license:

- **GitHub Repository:** [https://github.com/your-username/slothmerge](https://github.com/your-username/slothmerge)

### Core Agent Logic Snippet (`agent.py`)
```python
def audit_pull_request(diff_text: str, pr_title: str = "Pull Request Diff", model_name: str = "gemma2:2b"):
    start_time = time.time()
    trace_id = f"trace-{uuid.uuid4().hex[:12]}"
    spans = []

    # 1. Parse Diff Hunks & Metrics
    metrics = parse_diff_metrics(diff_text)
    
    # 2. Gemma Model Inference & Rule Evaluation
    review = call_gemma_model(diff_text, model_name=model_name)
    
    # 3. Format GitHub Review Comment
    github_comment = format_github_markdown_comment(review, metrics)

    # 4. Record Sentry Agent Tracing Telemetry
    telemetry = tracer.record_run(
        trace_id=trace_id,
        pr_title=pr_title,
        model_name=model_name,
        total_duration_ms=(time.time() - start_time) * 1000,
        prompt_tokens=int(len(diff_text) / 3.8) + 120,
        completion_tokens=int(len(json.dumps(review)) / 3.8),
        verdict=review.get("verdict", "UNKNOWN"),
        spans=spans
    )

    return {
        "review": review,
        "github_comment": github_comment,
        "telemetry": telemetry
    }
```

---

## 04. How I Built It

SlothMerge is built around three core pillars:

### 1. Open-Weight Foundation: Google Gemma 2
I used **Gemma 2 (`gemma2:2b` and `gemma2:9b`)**. Gemma 2's sliding-window attention and strong code-comprehension benchmarks make it ideal for parsing compact unified diffs. The prompt uses Gemma's structured turn syntax:
```text
<start_of_turn>user
You are SlothMerge...
<end_of_turn>
<start_of_turn>model
```
SlothMerge supports running directly on local hardware via **Ollama** (`http://localhost:11434`) as well as an optimized fallback pipeline when running in containerized or offline environments.

### 2. Sentry Agent Tracing (`sentry-sdk`)
Code review agents can be notoriously opaque. SlothMerge uses **Sentry Agent Tracing** to track every operation into distinct spans:
- `diff.parse`: Extracting changed files, line numbers, and hunks.
- `ai.inference`: Prompt construction, model latency, and token throughput.
- `output.format`: Markdown serialization and clipboard formatting.

Every execution records:
- **Total Duration:** 20ms to 350ms depending on hardware.
- **Token Accounting:** Prompt vs. completion tokens.
- **Financial Savings:** Exact dollars saved vs. closed APIs.

### 3. Deployment Ready on Render
The repository includes a ready-to-deploy `render.yaml` blueprint. You can connect your GitHub repository to Render and have a live, hosted SlothMerge web service running in under 2 minutes.

---

## 05. Why Does Open Innovation Matter?

Why not just hook up a commercial closed API like GPT-4o or Claude 3.5 Sonnet to a GitHub webhook?

Here is why **open innovation made SlothMerge possible** in ways a closed API could not:

### 1. Zero Code Leakage (Total IP Protection)
Your company's unreleased source code, proprietary algorithms, database schemas, and internal API endpoints should **never** be sent to a third-party closed API server. With Gemma running locally or in your private VPC, your diff never leaves your machine.

### 2. Zero Recurring API Costs
A busy engineering team might open 40–80 PRs a day. At ~2,000 to 8,000 tokens per comprehensive diff review, closed APIs quickly accumulate hundreds of dollars a month in recurring costs. Running open-weight Gemma 2 costs exactly **$0.00**.

### 3. Reliable Offline Operation
SlothMerge works on an airplane, on a train, or during an internet outage. When the Wi-Fi drops, your code review pipeline doesn't stop.

---

## 06. The Lazy Payoff

Here is the real math behind the sloth approach:

* **Average PR review time for a human engineer:** 25–40 minutes.
* **SlothMerge audit latency:** ~350 milliseconds.
* **Energy expended by human:** 0 calories.

This week alone, SlothMerge audited 3 candidate PRs:
1. **Caught an accidental personal access token commit** that would have required revoking credentials.
2. **Flagged an unescaped SQL query** that would have introduced a SQL injection vulnerability into user authentication.
3. **Approved a routine string helper refactor** instantly, freeing the author to merge without waiting 18 hours for someone to get around to reading their code.

I got to finish my dinner warm, relax on the sofa, and wake up to a green test suite. Sloth culture at its finest.

---

## 07. Prize Categories

I am submitting SlothMerge for the following categories:

* **Best Use of Gemma ($200)**: Built directly around Google's open-weight Gemma 2 model family for on-device reasoning and diff analysis.
* **Best Use of Render ($200)**: Fully configured with `render.yaml` for instant cloud service deployment.
* **Best Use of Sentry Agent Tracing ($100)**: Complete span profiling (`diff.parse`, `ai.inference`, `output.format`), token metrics, and cost savings telemetry.
* **GitHub Workflow & Automation**: Includes `.github/workflows/slothmerge.yml` for automated GitHub PR commenting.

---

*Sleep more. Review less. Let open-source AI do the chores.*
