#!/usr/bin/env python3
"""local_memory.py - FAISS-based local memory/search, no API key needed"""
import os, json, pickle, hashlib
from datetime import datetime
import numpy as np

try:
    import faiss
except ImportError:
    print("faiss-cpu not installed"); sys.exit(1)

MEMORY_DIR = os.path.expanduser("~/.qclaw/workspace/memory_faiss")
os.makedirs(MEMORY_DIR, exist_ok=True)

INDEX_PATH = os.path.join(MEMORY_DIR, "index.faiss")
META_PATH = os.path.join(MEMORY_DIR, "meta.json")
DIM = 128  # embedding dimension for simple hash-based vectors

def _hash_embed(text, dim=DIM):
    """Simple hash-based embedding (no API needed). Good for exact/near-exact match."""
    vec = np.zeros(dim, dtype=np.float32)
    chunks = [text[i:i+8] for i in range(0, len(text), 8)]
    for chunk in chunks:
        h = int(hashlib.md5(chunk.encode()).hexdigest(), 16)
        idx = h % dim
        vec[idx] += 1.0
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec /= norm
    return vec

def _load_index():
    if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "r", encoding="utf-8") as f:
            meta = json.load(f)
    else:
        index = faiss.IndexFlatIP(DIM)
        meta = {"entries": []}
    return index, meta

def _save_index(index, meta):
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

def add(text, tag="general"):
    """Add a memory entry"""
    index, meta = _load_index()
    vec = _hash_embed(text).reshape(1, -1)
    entry = {
        "id": len(meta["entries"]),
        "text": text[:500],
        "tag": tag,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    meta["entries"].append(entry)
    index.add(vec)
    _save_index(index, meta)
    return entry["id"]

def search(query, top_k=5):
    """Search memory by query"""
    index, meta = _load_index()
    if index.ntotal == 0:
        return []
    vec = _hash_embed(query).reshape(1, -1)
    k = min(top_k, index.ntotal)
    scores, ids = index.search(vec, k)
    results = []
    for score, idx in zip(scores[0], ids[0]):
        if idx >= 0 and idx < len(meta["entries"]):
            r = meta["entries"][idx].copy()
            r["score"] = float(score)
            results.append(r)
    return results

def list_all():
    """List all entries"""
    _, meta = _load_index()
    return meta["entries"]

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: local_memory.py <command> [args]")
        print("  add <text> [tag]   - add memory")
        print("  search <query> [k] - search memory")
        print("  list               - list all")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "add" and len(sys.argv) > 2:
        tag = sys.argv[3] if len(sys.argv) > 3 else "general"
        mid = add(sys.argv[2], tag)
        print(f"Added memory #{mid}")
    elif cmd == "search" and len(sys.argv) > 2:
        k = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        results = search(sys.argv[2], k)
        for r in results:
            print(f"[{r['id']}] ({r['score']:.3f}) [{r['tag']}] {r['text'][:80]}")
    elif cmd == "list":
        for e in list_all():
            print(f"[{e['id']}] [{e['tag']}] {e['time']} - {e['text'][:80]}")
    else:
        print(f"Unknown: {cmd}")
