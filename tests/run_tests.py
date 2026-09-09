#!/usr/bin/env python3
"""🧬 Astrid — full test suite (MIT, single command).

Runs every check against a REAL lumen MVM on a throwaway PDB. No external
services, no credentials, no Poli needed — only a lumen M runtime (see
harness/astrid_harness.py for how to provide one).

Checks:
  1. INIT seeds the canonical personality (idempotent + force)
  2. ASTRID status: active, identity_len, 7 capabilities, 6 rules
  3. VERIFY PASS (astrid) and FAIL for an unknown agent
  4. AUDIT demo runs (read-only)
  5. EVIDENCE canary: the digest runs, header says evidence=true, every
     claim| line has a source and exactly 5 fields (schema v1)
  6. evidence_routine contract seeded: ^PERSONALITY("astrid","evidence_routine")
     == "EVIDENCE^ASTRID" after INIT
  7. Identity sync: src/astrid.m identity line == personalities/astrid.md
     ASCII block; pure ASCII; 600–1400 chars
  8. Template regression: render a scratch agent → INIT → VERIFY PASS
  9. examples/echo regression: INIT → VERIFY PASS

Usage:  python tests/run_tests.py          (exit 0 = all green)
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HARNESS = ROOT / "harness"
sys.path.insert(0, str(HARNESS))
from astrid_harness import _mvm  # noqa: E402  (shared loader)

DB = os.path.join(tempfile.gettempdir(), "astrid_tests.db")
if os.path.exists(DB):
    os.remove(DB)

FAILURES: list[str] = []


def check(label: str, cond: bool, detail: str = ""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {label}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        FAILURES.append(label)


def run(src: str, expect_ok: bool = True) -> str:
    r = _mvm()(src, routines=_ROUTINES, sqlite_path=DB, gas_limit=200000)
    out = ((r.get("state") or {}).get("output") or "") if isinstance(r, dict) else ""
    ok = r.get("ok") if isinstance(r, dict) else False
    if expect_ok and not ok:
        raise RuntimeError(f"MVM ejecución falló: {src[:80]}… out={out[:200]}")
    return out


def _load_routines() -> dict:
    out = {}
    for name, rel in [("ASTRID", "src/astrid.m"), ("VERIFY", "tests/verify.m"),
                      ("ECHO", "examples/echo/src/echo.m")]:
        out[name] = (ROOT / rel).read_text(encoding="utf-8")
    return out


_ROUTINES = _load_routines()


def identity_from_m() -> str:
    m = (ROOT / "src" / "astrid.m").read_text(encoding="utf-8")
    hit = re.search(r'SETIF\^ASTRID\("identity","(.*)"\)', m)
    return hit.group(1) if hit else ""


def identity_from_md() -> str:
    md = (ROOT / "personalities" / "astrid.md").read_text(encoding="utf-8")
    parts = md.split("```")
    return parts[1].strip() if len(parts) >= 3 else ""


def main() -> int:
    print("🧬 Astrid test suite — MVM real, PDB temporal")
    # 1-2. INIT (empty / idempotent / force) + status
    run('D INIT^ASTRID')
    run('D INIT^ASTRID')
    run('D INIT^ASTRID(1)')
    out = run('D ASTRID^ASTRID')
    check("INIT+status activo", "active=1" in out, out[:120])
    exp_len = str(len(identity_from_m()))
    check(f"identity_len {exp_len}", f"identity_len={exp_len}" in out, out[:120])
    check("7 capabilities / 6 rules", "capabilities=7 rules=6" in out, out[:120])
    check("provider/model", "deepseek-v4-flash" in out, out[:120])
    # 3. VERIFY PASS astrid + FAIL desconocido
    out = run('D VERIFY^VERIFY')
    check("VERIFY astrid PASS", "PASS astrid" in out, out[:120])
    out = run('D VERIFY^VERIFY("nadie")')
    check("VERIFY nadie FAIL", "PASS nadie" not in out, out[:120])
    # 4. AUDIT demo (read-only)
    out = run('D AUDIT^ASTRID')
    check("AUDIT demo", "[ASTRID] observacion" in out, out[:120])
    # 5. EVIDENCE canary (schema v1: header + claims con source)
    out = run('W $$EVIDENCE^ASTRID()')
    check("EVIDENCE header evidence=true", "evidence=true" in out, out[:120])
    claims = [ln for ln in out.splitlines() if ln.startswith("claim|")]
    check("EVIDENCE emite claims", len(claims) >= 15, f"{len(claims)} claims")
    bad = [ln for ln in claims if len(ln.split("|")) != 5 or not ln.split("|")[2]]
    check("claims formato+source", not bad, (bad[0][:100] if bad else ""))
    # estabilidad: mismo estado -> mismo digest (AC-3 base)
    out2 = run('W $$EVIDENCE^ASTRID()')
    check("digest estable ante estado identico", out == out2, "los digests difieren")
    # 6. evidence_routine contract seeded by INIT
    out = run('W $G(^PERSONALITY("astrid","evidence_routine"))')
    check("evidence_routine sembrado", "EVIDENCE^ASTRID" in out, out[:120])
    # 7. Identity sync (M ↔ MD), ASCII, longitud
    im, imd = identity_from_m(), identity_from_md()
    check("identity M == MD", im == imd, f"M len={len(im)} MD len={len(imd)}")
    check("identity ASCII", bool(im) and all(ord(c) < 128 for c in im), "no-ASCII")
    check("identity 600-1400", 600 <= len(im) <= 1400, f"len={len(im)}")
    # 8. Template regression: scratch agent
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        idf = tdp / "id.txt"
        idf.write_text(("Agente de prueba generado por run_tests para validar que la plantilla es reusable. " * 12).strip(), encoding="utf-8")
        dest = tdp / "probe"
        subprocess.run([sys.executable, str(ROOT / "template" / "render.py"), "probe",
                        "--dest", str(dest), "--identity-file", str(idf),
                        "--role", "probe", "--emoji", "🧪"], check=True, capture_output=True)
        probe_src = (dest / "src" / "probe.m").read_text(encoding="utf-8")
        _ROUTINES["PROBE"] = probe_src
        run('D INIT^PROBE')
        out = run('D VERIFY^VERIFY("probe")')
        check("template render + INIT + VERIFY", "PASS probe" in out, out[:120])
    # 9. examples/echo regression
    run('D INIT^ECHO')
    out = run('D VERIFY^VERIFY("echo")')
    check("echo (derivado real) VERIFY", "PASS echo" in out, out[:120])

    print("\n" + ("🎉 TODO VERDE — astrid lista para cerrar ciclo" if not FAILURES
                  else f"❌ {len(FAILURES)} fallo(s): {FAILURES}"))
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
