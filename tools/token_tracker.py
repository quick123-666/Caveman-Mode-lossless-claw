#!/usr/bin/env python3
"""token_tracker.py - Auto token counter for every task/conversation"""
import tiktoken, json, sys, os
from datetime import datetime

TRACKER_DIR = os.path.expanduser("~/.qclaw/workspace/token_logs")
os.makedirs(TRACKER_DIR, exist_ok=True)

enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    return len(enc.encode(text))

def log_usage(input_text, output_text, task_name="default"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    in_tok = count_tokens(input_text)
    out_tok = count_tokens(output_text)
    total = in_tok + out_tok
    entry = {"time": now, "task": task_name, "in": in_tok, "out": out_tok, "total": total}
    log_file = os.path.join(TRACKER_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.jsonl")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry

def summary(days=7):
    """Show token usage summary for last N days"""
    total_in = total_out = total_tasks = 0
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(TRACKER_DIR, f"{today}.jsonl")
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                e = json.loads(line.strip())
                total_in += e["in"]
                total_out += e["out"]
                total_tasks += 1
    return {"tasks": total_tasks, "in_tokens": total_in, "out_tokens": total_out, "total_tokens": total_in + total_out}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: token_tracker.py <command> [args]")
        print("  count <text>        - count tokens in text")
        print("  log <input> <output> [task] - log token usage")
        print("  summary             - show today's summary")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "count" and len(sys.argv) > 2:
        print(count_tokens(sys.argv[2]))
    elif cmd == "summary":
        print(json.dumps(summary(), ensure_ascii=False, indent=2))
    elif cmd == "log" and len(sys.argv) > 3:
        task = sys.argv[4] if len(sys.argv) > 4 else "default"
        result = log_usage(sys.argv[2], sys.argv[3], task)
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"Unknown command: {cmd}")
