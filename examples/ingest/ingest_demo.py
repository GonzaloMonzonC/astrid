#!/usr/bin/env python3
"""Astrid ingest demo — external source -> PDB -> audited by the digest.

A minimal webhook (stdlib only) that receives POSTed JSON events and appends
them to the Astrid inbox in a lumen PDB via the real M routine:

    INGEST^ASTRID(origen, raw)  ->  ^ASTRID("inbox", origen, seq) = raw

The next EVIDENCE^ASTRID digest run emits inbox claims (counters per
source), so Astrid audits the incoming stream with her normal contract:
registered data only.

Usage:
    python examples/ingest/ingest_demo.py --db <path> [--port 8787]

    curl -X POST "http://127.0.0.1:8787/hook?origen=github" \
         -H "Content-Type: application/json" \
         -d '{"event": "push", "repo": "astrid", "ref": "main"}'
    curl "http://127.0.0.1:8787/digest"

Requirements: same as the harness — a lumen M runtime (sibling
lumen-protocol clone or LUMEN_MLIGHT_LIB). No external dependencies.
"""
import argparse
import json
import os
import sys
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "harness"))
from astrid_harness import _mvm  # noqa: E402

ROUTINES = {"ASTRID": (ROOT / "src" / "astrid.m").read_text(encoding="utf-8")}
_EXECUTE = None  # module-level (no bound-method surprises)


class HookHandler(BaseHTTPRequestHandler):
    db = ""

    def _run(self, src: str) -> tuple[str, bool]:
        r = _EXECUTE(src, routines=ROUTINES, sqlite_path=self.db, gas_limit=200000)
        out = ((r.get("state") or {}).get("output") or "") if isinstance(r, dict) else ""
        ok = r.get("ok") if isinstance(r, dict) else False
        return out.strip(), ok

    def _json(self, code: int, obj: dict):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if not self.path.startswith("/hook"):
            self._json(404, {"error": "use POST /hook?origen=<source>"})
            return
        q = self.path.split("?", 1)
        origen = "webhook"
        if len(q) > 1:
            for kv in q[1].split("&"):
                k, _, v = kv.partition("=")
                if k == "origen":
                    origen = v[:32]
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8", "replace")
        try:
            json.loads(raw)  # reject non-JSON payloads
        except json.JSONDecodeError as e:
            self._json(400, {"error": f"payload no es JSON: {e}"})
            return
        # M string escaping: double the quotes, strip newlines (single-line M)
        raw_m = raw.replace("\r", " ").replace("\n", " ").replace('"', '""')
        seq, ok = self._run(f'W $$INGEST^ASTRID("{origen}", "{raw_m}")')
        if not ok:
            self._json(500, {"error": f"INGEST fallo: {seq[:200]}"})
            return
        self._json(200, {"ok": True, "origen": origen, "seq": int(seq.strip() or 0)})

    def do_GET(self):
        if not self.path.startswith("/digest"):
            self._json(404, {"error": "use GET /digest"})
            return
        out, ok = self._run('D INIT^ASTRID W !,$$EVIDENCE^ASTRID()')
        if not ok:
            self._json(500, {"error": f"digest fallo: {out[:200]}"})
            return
        self._json(200, {"ok": True, "digest": out})

    def log_message(self, *args):  # silence request logging
        pass


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=os.path.join(tempfile.gettempdir(), "astrid_ingest.db"),
                    help="PDB file to use (default: temp astrid_ingest.db)")
    ap.add_argument("--port", type=int, default=8787)
    args = ap.parse_args()

    if os.path.exists(args.db):
        os.remove(args.db)  # fresh inbox for the demo
    global _EXECUTE
    HookHandler.db = args.db
    _EXECUTE = _mvm()
    # seed the personality so the digest header is truthful
    _EXECUTE("D INIT^ASTRID", routines=ROUTINES, sqlite_path=args.db, gas_limit=200000)

    srv = ThreadingHTTPServer(("127.0.0.1", args.port), HookHandler)
    print(f"🧬 Astrid ingest demo escuchando en http://127.0.0.1:{args.port}")
    print(f"   POST /hook?origen=<source>  (body: JSON)   -> append al inbox")
    print(f"   GET  /digest                              -> EVIDENCE^ASTRID con claims del inbox")
    print(f"   PDB: {args.db}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
