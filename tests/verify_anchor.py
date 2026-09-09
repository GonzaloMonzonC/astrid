#!/usr/bin/env python3
"""Anchor verifier — notary contract (EVIDENCE_SCHEMA.md §3, AC-3).

Validates the runtime anchor contract WITHOUT the runtime. Given the digest
produced by EVIDENCE^ASTRID on a throwaway PDB it:

  1. cid      — computes sha256(digest), the content address the runtime uses
  2. stable   — two consecutive runs on identical state yield the same cid
  3. ledger   — writes the row the runtime writes: ^EVIDENCE(cid) = sig|ts|routine
                and the digest line-by-line under ^EVIDENCE(cid,"digest",n)
  4. verify   — recomputes the signature from the stored ts and a known key

Signature scheme (same as poli_server._hmac_sign in lumen-protocol):
HMAC-SHA256(ts + cid + secret), hex. The real runtime signs with
^CONFIG("ddp_hmac_key"); this verifier uses a throwaway TEST key — the
contract is what is tested, never a real secret.

Usage:  python tests/verify_anchor.py     (exit 0 = all green)
"""
import hashlib
import hmac
import os
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness"))
from astrid_harness import _mvm  # noqa: E402

TEST_KEY = "test-anchor-key-not-a-secret"
DB = os.path.join(tempfile.gettempdir(), "astrid_anchor.db")
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


def sign(cid: str, ts: str, secret: str) -> str:
    return hmac.new(secret.encode("utf-8"), (ts + cid + secret).encode("utf-8"),
                    hashlib.sha256).hexdigest()


def anchor(cid: str, digest: str, routine: str, secret: str) -> tuple[str, str]:
    """Replica el anclaje del runtime: firma + ledger por lineas (M-natural)."""
    ts = str(int(time.time()))
    sig = sign(cid, ts, secret)
    lines = [ln for ln in digest.split("\n") if ln]
    sets = [f'S ^EVIDENCE("{cid}")="{sig}|{ts}|{routine}"']
    for i, ln in enumerate(lines, start=1):
        sets.append(f'S ^EVIDENCE("{cid}","digest",{i})="{ln.replace(chr(34), chr(34) * 2)}"')
    run("\n".join(sets))
    return sig, ts


def main() -> int:
    fails: list[str] = []
    run("D INIT^ASTRID")
    run('S ^CONFIG("ddp_hmac_key")="' + TEST_KEY + '"')
    d1 = run("W $$EVIDENCE^ASTRID()")
    d2 = run("W $$EVIDENCE^ASTRID()")

    # 1-2. cid estable
    cid1, cid2 = hashlib.sha256(d1.encode()).hexdigest(), hashlib.sha256(d2.encode()).hexdigest()
    if cid1 != cid2:
        fails.append("cid inestable: dos corridas en estado identico difieren")
    if len(cid1) != 64:
        fails.append(f"cid no es sha256 hex: {cid1[:20]}")
    cid = cid1

    # 3. ledger
    sig, ts = anchor(cid, d1, "EVIDENCE^ASTRID", TEST_KEY)
    d = run(f'W $D(^EVIDENCE("{cid}"))')
    if "11" not in d:
        fails.append(f"ledger: ^EVIDENCE({cid[:12]}...) no existe o sin digest ($D={d.strip()})")
    # dedup: anclar dos veces no duplica (append-only por cid)
    anchor(cid, d1, "EVIDENCE^ASTRID", TEST_KEY)
    out = run(f'W $O(^EVIDENCE("{cid}","digest",""),-1)')
    nd = int(out.strip() or "0")
    expect = len([ln for ln in d1.split("\n") if ln])
    if nd != expect:
        fails.append(f"ledger: digest guardado con {nd} lineas, esperaba {expect}")

    # 4. firma verificable + digest round-trip
    head = run(f'W $G(^EVIDENCE("{cid}"))')
    parts = head.strip().split("|")
    if len(parts) != 3:
        fails.append(f"ledger head malformado: {head.strip()[:80]}")
    else:
        stored_sig, stored_ts, routine = parts
        if sign(cid, stored_ts, TEST_KEY) != stored_sig:
            fails.append("firma no verifica con el ts guardado")
        if routine != "EVIDENCE^ASTRID":
            fails.append(f"rutina en ledger inesperada: {routine}")
    rec = run(f'F i=1:1:{expect} W $G(^EVIDENCE("{cid}","digest",i)),!')
    if rec.rstrip("\n") != d1.rstrip("\n"):
        fails.append("digest no hace round-trip desde el ledger")

    print(f"[{'PASS' if not fails else 'FAIL'}] verify_anchor: cid={cid[:16]}… "
          f"ledger_lines={expect}" + ("" if not fails else f" -> {fails[:4]}"))
    for f in fails:
        print(f"  - {f}")
    print("TODO VERDE — contrato de anclaje valido (cid + firma + ledger)"
          if not fails else f"{len(fails)} fallo(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
