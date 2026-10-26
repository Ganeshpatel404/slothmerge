"""
SlothMerge Web Dashboard & API
FastAPI backend powering the interactive PR review agent and Sentry Agent Tracing visualizer.
"""

import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, Response
from pydantic import BaseModel
from typing import Optional
from agent import audit_pull_request
from sentry_tracer import tracer

app = FastAPI(title="SlothMerge: The Ghost PR Reviewer", version="1.0.0")

class AuditRequest(BaseModel):
    diff: str
    title: Optional[str] = "Feature Branch Review"
    model: Optional[str] = "gemma2:2b"

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>SlothMerge Agent Running</h1>")

@app.post("/api/audit")
async def handle_audit(req: AuditRequest):
    if not req.diff.strip():
        return JSONResponse(status_code=400, content={"error": "Empty diff provided."})
    
    result = audit_pull_request(
        diff_text=req.diff,
        pr_title=req.title or "Pull Request Diff",
        model_name=req.model or "gemma2:2b"
    )
    return JSONResponse(content=result)

@app.get("/api/traces")
async def get_traces():
    return JSONResponse(content={"traces": tracer.get_latest_traces(10)})

@app.get("/api/samples/{sample_id}")
async def get_sample(sample_id: str):
    sample_map = {
        "sql": "pr1_sql_injection.diff",
        "async": "pr2_missing_tests.diff",
        "clean": "pr3_clean_refactor.diff"
    }
    file_name = sample_map.get(sample_id)
    if not file_name:
        return JSONResponse(status_code=404, content={"error": "Sample not found"})
    
    file_path = os.path.join(os.path.dirname(__file__), "samples", file_name)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return JSONResponse(content={"diff": f.read(), "id": sample_id})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
