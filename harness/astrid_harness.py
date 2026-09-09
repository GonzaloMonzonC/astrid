#!/usr/bin/env python3
"""🧬 Astrid harness — connect the reference agent to LUMEN (MIT).

Three modes (run what you have):

  1. STATUS   — run ASTRID^ASTRID against any lumen-m-light MVM (needs the DLL
                or the published lumen-mcp package). Prints identity status.
  2. AUDIT    — demo audit: count first-level nodes of a namespace in the PDB
                (same M routine used in src/astrid.m).
  3. CHAT     — (optional) point HOST_MCP to any LUMEN MCP server that exposes
                a chat personality mode (e.g. Poli's mode=astrid); not needed
                for a standalone install.

Requirements: a lumen M runtime to execute the M routines. Two options:
  1. local lumen-protocol clone (https://github.com/GonzaloMonzonC/lumen-protocol)
     with the Rust MVM built (`cargo build --release` → lumen_mlight.dll,
     copied to implementations/mcp-servers/pdb/), or
  2. `LUMEN_MLIGHT_LIB` pointing at an existing lumen_mlight.dll.
NOTE: `pip install lumen-mcp` (0.1.0) ships the transport/framing bindings
only — it does NOT include the MVM. A clone build or DLL is required to run
routines.

Usage:
    python astrid_harness.py status
    python astrid_harness.py audit --ns ^ANGI
    ASTRID_LIB=C:/path/to/lumen_mlight.dll python astrid_harness.py status
"""

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_ROUTINES = {"ASTRID": (ROOT / "src" / "astrid.m").read_text(encoding="utf-8")}


def _mvm() -> object:
    """Load the lumen m-light python wrapper (published lumen-mcp or local clone)."""
    try:
        from lumen_mlight import execute  # published/local wrapper

        return execute
    except ImportError:
        pass
    # local lumen-protocol clone fallback
    here = Path(__file__).resolve()
    for cand in here.parents:
        p = cand / "lumen-protocol" / "implementations" / "mcp-servers" / "pdb"
        if (p / "lumen_mlight.py").exists():
            sys.path.insert(0, str(p))
            from lumen_mlight import execute  # type: ignore

            return execute
    raise SystemExit(
        "No lumen-mcp found. Install `pip install lumen-mcp` or clone lumen-protocol "
        "next to this repo (https://github.com/GonzaloMonzonC/lumen-protocol)."
    )


def _run(execute, src: str, db: str):
    r = execute(src, routines=SRC_ROUTINES, sqlite_path=db, gas_limit=100000)
    out = ((r.get("state") or {}).get("output") or "") if isinstance(r, dict) else ""
    print(out.strip() or r)
    return r


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["status", "audit"])
    ap.add_argument("--ns", default="^ANGI", help="namespace to audit (audit mode)")
    ap.add_argument("--db", default=os.path.join(os.environ.get("TEMP", "."), "astrid_pdb.db"))
    args = ap.parse_args()

    execute = _mvm()
    if args.mode == "status":
        _run(execute, "D ASTRID^ASTRID", args.db)
    elif args.mode == "audit":
        src = f'S ^ASTRID("audit_ns")="{args.ns}" D AUDIT^ASTRID'
        _run(execute, src, args.db)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
