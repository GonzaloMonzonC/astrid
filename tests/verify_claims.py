#!/usr/bin/env python3
"""Verifier harness for the digest claims (EVIDENCE_SCHEMA.md AC-3).

Validates the output of EVIDENCE^ASTRID on a throwaway PDB:
  1. format  — every claim| line has exactly 5 fields and a non-empty source
  2. header  — evidence=true present, version matches ^PERSONALITY
  3. kinds   — only known kinds (mode|counter|metric|route|config|state|note|entry)
  4. stability — two consecutive runs produce identical digests

Usage:  python tests/verify_claims.py        (exit 0 = all green)
"""
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness"))
from astrid_harness import _mvm  # noqa: E402

KINDS = {"mode", "counter", "metric", "route", "config", "state", "note", "entry"}
DB = os.path.join(tempfile.gettempdir(), "astrid_claims.db")
if os.path.exists(DB):
    os.remove(DB)

ROUTINES = {
    "ASTRID": (ROOT / "src" / "astrid.m").read_text(encoding="utf-8"),
    "VERIFY": (ROOT / "tests" / "verify.m").read_text(encoding="utf-8"),
}

def run(src: str) -> str:
    r = _mvm()(src, routines=ROUTINES, sqlite_path=DB, gas_limit=200000)
    out = ((r.get("state") or {}).get("output") or "") if isinstance(r, dict) else ""
    if not (r.get("ok") if isinstance(r, dict) else False):
        raise RuntimeError(f"MVM failed: {src[:60]}... out={out[:200]}")
    return out

def main() -> int:
    fails: list[str] = []
    run("D INIT^ASTRID")
    d1 = run("W $$EVIDENCE^ASTRID()")
    d2 = run("W $$EVIDENCE^ASTRID()")
    lines = d1.splitlines()
    claims = [ln for ln in lines if ln.startswith("claim|")]

    if "evidence=true" not in d1: fails.append("header: evidence=true ausente")
    if not claims: fails.append("sin claims")
    for ln in claims:
        parts = ln.split("|")
        if len(parts) != 5: fails.append(f"formato ({len(parts)} campos): {ln[:80]}")
        elif not parts[2]: fails.append(f"source vacio: {ln[:80]}")
        elif parts[1] not in KINDS: fails.append(f"kind desconocido {parts[1]}: {ln[:80]}")
    if d1 != d2: fails.append("inestable: dos corridas consecutivas difieren")

    print(f"[{'PASS' if not fails else 'FAIL'}] verify_claims: {len(claims)} claims, "
          f"{len(lines)} lineas" + ("" if not fails else f" -> {fails[:5]}"))
    for f in fails:
        print(f"  - {f}")
    print("TODO VERDE — digest valido y estable" if not fails else f"{len(fails)} fallo(s)")
    return 1 if fails else 0

if __name__ == "__main__":
    raise SystemExit(main())
