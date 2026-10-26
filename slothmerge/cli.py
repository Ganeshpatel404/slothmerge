#!/usr/bin/env python3
"""
SlothMerge CLI
Run automated open-weight code reviews from your terminal or git hooks.
"""

import sys
import argparse
from agent import audit_pull_request

def main():
    parser = argparse.ArgumentParser(description="🦥 SlothMerge: The Lazy Offline Code Reviewer")
    parser.add_argument("file", nargs="?", help="Path to a diff file (e.g. pr.diff). If omitted, reads from stdin.")
    parser.add_argument("--model", default="gemma2:2b", help="Open-weight model name (default: gemma2:2b)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of markdown")
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                diff_text = f.read()
        except Exception as e:
            print(f"Error reading file {args.file}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        if sys.stdin.isatty():
            print("Usage: slothmerge <diff_file> or git diff | python cli.py", file=sys.stderr)
            sys.exit(1)
        diff_text = sys.stdin.read()

    if not diff_text.strip():
        print("Empty diff supplied. Nothing to review! Go relax. 🦥")
        sys.exit(0)

    result = audit_pull_request(diff_text, pr_title="Terminal Diff Audit", model_name=args.model)

    if args.json:
        import json
        print(json.dumps(result, indent=2))
    else:
        print(result["github_comment"])

if __name__ == "__main__":
    main()
