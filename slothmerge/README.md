# 🦥 SlothMerge: The Ghost PR Reviewer

[![DEV Challenge](https://img.shields.io/badge/DEV%20Challenge-Hacktoberfest%202026-brightgreen.svg)](https://dev.to/challenges/hacktoberfest-week3-2026-10-19)
[![Open Source AI](https://img.shields.io/badge/Model-Google%20Gemma%202-indigo.svg)](https://ai.google.dev/gemma)
[![Sentry](https://img.shields.io/badge/Tracing-Sentry%20Agent%20SDK-ff69b4.svg)](https://sentry.io)
[![Render](https://img.shields.io/badge/Deploy-Render%20Blueprint-blue.svg)](https://render.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **"Build something with open-weight models that rewards laziness."**  
> SlothMerge is an open-source AI agent that intercepts git diffs and audits pull requests overnight. It flags security vulnerabilities (SQLi, leaked secrets, unhandled network rejections), generates an executive 3-bullet morning digest, and formats a copy-pasteable GitHub PR review comment — so you can stay in bed.

---

## 💡 Why Open Innovation Matters Here

1. **Zero Source Code Leaks:** Proprietary diffs, database schemas, and business logic stay on your laptop or inside your private VPC. No source code ever touches external AI providers.
2. **Zero Recurring API Costs:** Instead of paying $0.03 to $0.15 per multi-file PR review on closed APIs, SlothMerge runs on open-weight **Google Gemma 2** models (`gemma2:2b` or `gemma2:9b`) costing **$0.00**.
3. **Deterministic & Local:** Works offline on an airplane or when the Wi-Fi is down.

---

## 🚀 Architecture

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
│  ├─ 📋 3-Bullet Morning Digest  │
│  ├─ 🚨 Offending Line & Fix     │
│  ├─ 💬 Formatted GitHub Comment │
│  └─ 📊 Sentry Latency & Cost    │
└─────────────────────────────────┘
```

---

## 🛠️ Quickstart

### 1. Clone & Install
```bash
git clone https://github.com/your-username/slothmerge.git
cd slothmerge
pip install -r requirements.txt
```

### 2. Run the Interactive Web Dashboard
```bash
python app.py
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

### 3. Run from CLI / Git Hooks
```bash
# Review a local diff file
python cli.py samples/pr1_sql_injection.diff

# Review uncommitted git changes in current repo
git diff | python cli.py
```

### 4. Optional: Run with Local Gemma via Ollama
```bash
ollama run gemma2:2b
```
SlothMerge automatically detects local Ollama instances at `http://localhost:11434`.

---

## 🔍 Sentry Agent Tracing

SlothMerge natively integrates Sentry Agent Tracing to monitor:
- Total end-to-end audit latency
- Token accounting (prompt tokens vs. completion tokens)
- Granular spans: `diff.parse`, `ai.inference`, `output.format`
- Cost savings vs. closed commercial APIs

To enable live Sentry telemetry, set:
```bash
export SENTRY_DSN="your_sentry_dsn_here"
```

---

## ☁️ Deploy to Render

Deploy with one click using the included `render.yaml` blueprint:
1. Connect this repo to [Render](https://render.com).
2. Choose **Blueprint** deployment.
3. SlothMerge will build and deploy automatically!

---

## 📄 License
MIT © 2026. Built for DEV Challenge: Hacktoberfest 2026 (Week 3: Slow and Steady).
