# SlothMerge: The Ghost PR Reviewer

[![DEV Challenge](https://img.shields.io/badge/DEV%20Challenge-Hacktoberfest%202026-brightgreen.svg)](https://dev.to/challenges/hacktoberfest-week3-2026-10-19)
[![Open Source AI](https://img.shields.io/badge/Model-Google%20Gemma%202-indigo.svg)](https://ai.google.dev/gemma)
[![Sentry](https://img.shields.io/badge/Tracing-Sentry%20Agent%20SDK-ff69b4.svg)](https://sentry.io)
[![Render](https://img.shields.io/badge/Deploy-Render%20Blueprint-blue.svg)](https://render.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **"Build something with open-weight models that rewards laziness."**  
> SlothMerge is an open-source AI agent powered by **Google Gemma 2** and instrumented with **Sentry Agent Tracing**. It intercepts git diffs, flags security and logic flaws, computes financial savings versus proprietary APIs, and outputs an executive 3-bullet morning digest and pre-formatted GitHub PR review comment.

---

## 01. Why Open Innovation Matters Here

1. **Zero Source Code Leaks:** Proprietary diffs, database schemas, and business logic stay on your laptop or inside your private VPC. No source code ever touches external AI providers.
2. **Zero Recurring API Costs:** Instead of paying $0.03 to $0.15 per multi-file PR review on closed APIs, SlothMerge runs on open-weight **Google Gemma 2** models (`gemma2:2b` or `gemma2:9b`) costing **$0.00**.
3. **Deterministic & Local:** Works completely offline on an airplane or when network connectivity is down.

---

## 02. Architecture & Pipeline

```text
[ Git Diff / PR Patch ]
          │
          ▼
┌─────────────────────────────────┐
│     SlothMerge Agent Core       │
│  ├─ Unified Diff Parser         │
│  ├─ Sentry Agent Tracing Span   │
│  └─ Security & Concurrency Scan │
└─────────────────┬───────────────┘
                  │
                  ▼
┌─────────────────────────────────┐
│     Google Gemma 2 Pipeline     │
│  (Local Ollama / Open-Weights)  │
│  ├─ Security vulnerabilities    │
│  ├─ Logic edge cases            │
│  └─ Laziness Verdict (Approve)  │
└─────────────────┬───────────────┘
                  │
                  ▼
┌─────────────────────────────────┐
│          Audit Output           │
│  ├─ 3-Bullet Morning Digest     │
│  ├─ Offending Line & Fix        │
│  ├─ Formatted GitHub Comment    │
│  └─ Sentry Latency & Cost Span  │
└─────────────────────────────────┘
