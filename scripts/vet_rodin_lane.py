#!/usr/bin/env python3
"""vet_rodin_lane.py — Hyper3D Rodin batch generator for tierarztapp.

Reuses the battle-tested pipeline from pferdehof/scripts/rodin_batch_generate.py
(submit/poll/download/compress/validate) with tierarztapp-specific output paths.

Usage:
  python3 scripts/vet_rodin_lane.py \
    --queue _multi/2026-06-10-hyper3d-credit-burn/queue_T1.json \
    --state _multi/2026-06-10-hyper3d-credit-burn/rodin_state_T1.json \
    --out-dir assets/models/organs \
    --max-credits 27 --reserve 0

  python3 scripts/vet_rodin_lane.py --queue <queue.json> --dry-run
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

# Import battle-tested functions from pferdehof pipeline
_PFERDEHOF_SCRIPTS = Path("/Users/cardrevolution/Desktop/coding/pferdehof/scripts")
if str(_PFERDEHOF_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_PFERDEHOF_SCRIPTS))

from rodin_batch_generate import (  # noqa: E402
    GLB_MAGIC,
    CREDIT_PER_JOB,
    get_api_key,
    check_balance,
    submit_generation,
    poll_until_done,
    download_glb,
    compress_glb,
    validate_glb,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_json(path: Path):
    return json.loads(path.read_text()) if path.exists() else None


def load_state(path: Path) -> dict:
    s = load_json(path)
    if s:
        return s
    return {
        "lane": path.stem,
        "project": "tierarztapp",
        "summary": {"accepted": 0, "failed": 0, "credits_used": 0},
        "models": {},
    }


def save_state(path: Path, state: dict) -> None:
    state["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def main() -> int:
    p = argparse.ArgumentParser(description="Tierarztapp Hyper3D Rodin batch generator")
    p.add_argument("--queue", required=True, help="JSON queue file [{name, prompt}, ...]")
    p.add_argument("--state", default=None, help="State JSON (default: <queue>.state.json)")
    p.add_argument("--out-dir", default="assets/models", help="Output directory for GLBs")
    p.add_argument("--max-credits", type=float, default=None, help="Hard credit cap for this lane")
    p.add_argument("--reserve", type=float, default=0.0, help="Never go below this balance (default: 0)")
    p.add_argument("--max-attempts", type=int, default=2, help="Retries per model")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true", help="Regenerate even if GLB exists")
    args = p.parse_args()

    queue_path = Path(args.queue)
    if not queue_path.is_absolute():
        queue_path = PROJECT_ROOT / queue_path
    jobs = load_json(queue_path)
    if not isinstance(jobs, list) or not jobs:
        print(f"ERROR: empty or invalid queue {queue_path}")
        return 1

    state_path = Path(args.state) if args.state else queue_path.with_suffix(".state.json")
    if not state_path.is_absolute():
        state_path = PROJECT_ROOT / state_path
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = PROJECT_ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        print(f"=== DRY RUN ({queue_path.name}) — {len(jobs)} jobs ===")
        for j in jobs:
            name = j["name"]
            out_path = out_dir / f"{name}.glb"
            exists = "EXISTS" if out_path.exists() else "NEW"
            print(f"  [{exists}] {name:<40} {j.get('prompt', '')[:60]}...")
        new_count = sum(1 for j in jobs if not (out_dir / f"{j['name']}.glb").exists())
        print(f"\nTotal: {len(jobs)} jobs, {new_count} new, ~{new_count * CREDIT_PER_JOB} credits")
        return 0

    api_key = get_api_key()
    balance = check_balance(api_key)
    print(f"[{state_path.stem}] Balance: {balance} | Reserve: {args.reserve} | Cap: {args.max_credits}")
    if balance <= args.reserve:
        print(f"STOP: Balance {balance} <= Reserve {args.reserve}")
        return 1

    state = load_state(state_path)
    credits_used = 0.0
    consec_fail = 0

    for i, job in enumerate(jobs):
        name = job["name"]
        out_path = out_dir / f"{name}.glb"
        prev = state["models"].get(name, {})

        # Skip existing
        if not args.force and (prev.get("status") == "ACCEPTED" or out_path.exists()):
            print(f"[{i+1}/{len(jobs)}] skip {name} (exists)")
            continue

        # Pre-flight checks
        bal = check_balance(api_key)
        if bal <= args.reserve:
            print(f"STOP: Balance {bal} <= Reserve {args.reserve}")
            break
        if args.max_credits is not None and credits_used >= args.max_credits:
            print(f"STOP: Cap reached ({credits_used}/{args.max_credits})")
            break
        if consec_fail >= 3:
            print("STOP: 3 consecutive failures — check prompts/API")
            break

        print(f"[{i+1}/{len(jobs)}] {name}  (bal {bal}, used {credits_used})")
        ok = False
        for attempt in range(1, args.max_attempts + 1):
            try:
                task_uuid, sub_key = submit_generation(api_key, job["prompt"])
                credits_used += CREDIT_PER_JOB
                print(f"  submit {task_uuid} (try {attempt})")
                poll_until_done(api_key, sub_key)
                download_glb(api_key, task_uuid, out_path)
                if not out_path.exists() or out_path.read_bytes()[:4] != GLB_MAGIC:
                    raise RuntimeError("invalid GLB")
                comp_ok, cmsg = compress_glb(out_path)
                print(f"  {cmsg}")
                vok, vmsg = validate_glb(out_path)
                if vok:
                    print(f"  PASS {vmsg}")
                    ok = True
                    state["models"][name] = {
                        "status": "ACCEPTED",
                        "attempts": attempt,
                        "output": str(out_path.relative_to(PROJECT_ROOT)),
                        "size_kb": out_path.stat().st_size // 1024,
                        "at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    }
                    break
                print(f"  FAIL {vmsg}")
                out_path.unlink(missing_ok=True)
            except Exception as e:
                print(f"  ERROR {e}")
        if ok:
            consec_fail = 0
        else:
            consec_fail += 1
            state["models"][name] = {
                "status": "FAILED",
                "at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }
        state["summary"] = {
            "accepted": sum(1 for m in state["models"].values() if m.get("status") == "ACCEPTED"),
            "failed": sum(1 for m in state["models"].values() if m.get("status") == "FAILED"),
            "credits_used": credits_used,
        }
        save_state(state_path, state)

    final = check_balance(api_key)
    print(f"\n[{state_path.stem}] done — accepted {state['summary']['accepted']}, "
          f"failed {state['summary']['failed']}, credits {credits_used}, balance {final} (start {balance})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
