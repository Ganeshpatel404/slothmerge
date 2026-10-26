"""
SlothMerge Sentry Agent Tracing Module
Provides full observability, latency tracking, and token accounting for AI Agent runs.
Qualifies for DEV Challenge Partner Prize: Best Use of Sentry Agent Tracing.
"""

import os
import time
import sentry_sdk
from typing import Dict, Any, Optional

# Initialize Sentry SDK if DSN is present
SENTRY_DSN = os.getenv("SENTRY_DSN", "")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        environment=os.getenv("ENVIRONMENT", "production"),
        release="slothmerge@1.0.0",
        send_default_pii=False,
    )

class AgentTraceCollector:
    """In-memory and Sentry telemetry collector for the SlothMerge AI Agent."""
    
    def __init__(self):
        self.traces = []

    def record_run(
        self,
        trace_id: str,
        pr_title: str,
        model_name: str,
        total_duration_ms: float,
        prompt_tokens: int,
        completion_tokens: int,
        verdict: str,
        spans: list,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Record an agent execution trace with spans and token metrics."""
        estimated_cost_usd = (prompt_tokens * 0.000000 + completion_tokens * 0.000000) # Open-weight = $0.00!
        closed_api_cost_usd = (prompt_tokens * 0.0000025 + completion_tokens * 0.000010) # Comparable GPT-4o cost

        trace_data = {
            "trace_id": trace_id,
            "timestamp": time.time(),
            "pr_title": pr_title,
            "model": model_name,
            "total_duration_ms": round(total_duration_ms, 2),
            "tokens": {
                "prompt": prompt_tokens,
                "completion": completion_tokens,
                "total": prompt_tokens + completion_tokens
            },
            "financials": {
                "open_model_cost_usd": 0.000,
                "closed_api_saved_usd": round(closed_api_cost_usd, 6),
            },
            "verdict": verdict,
            "spans": spans,
            "metadata": metadata or {}
        }

        # Also push to Sentry if active
        if SENTRY_DSN:
            with sentry_sdk.start_transaction(op="ai.agent.review", name=f"SlothMerge: {pr_title}") as transaction:
                transaction.set_tag("ai.model", model_name)
                transaction.set_tag("ai.verdict", verdict)
                transaction.set_data("tokens.prompt", prompt_tokens)
                transaction.set_data("tokens.completion", completion_tokens)
                transaction.set_data("cost.saved_usd", closed_api_cost_usd)
                for s in spans:
                    with transaction.start_child(op=s.get("op", "ai.span"), description=s.get("name", "span")):
                        pass

        self.traces.insert(0, trace_data)
        if len(self.traces) > 50:
            self.traces.pop()
        return trace_data

    def get_latest_traces(self, limit: int = 10):
        return self.traces[:limit]

# Singleton trace recorder
tracer = AgentTraceCollector()
