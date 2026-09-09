# Ingest: external sources → PDB → audited by Astrid

> 🇪🇸 Versión en español: [INGESTION.es.md](INGESTION.es.md)

The digest proves Astrid answers only from registered data. This demo closes
the other half of the loop: **getting external data registered in the first
place**, through lumen's own machinery (MVM + PDB), so the agent can audit
an incoming stream with her normal contract.

```
external source ──POST──▶ ingest_demo.py (webhook, stdlib)
                              │  D INGEST^ASTRID(origen, raw)
                              ▼
                    ^ASTRID("inbox", <origen>, <seq>) = raw JSON
                              │  (next chat / digest run)
                              ▼
              EVIDENCE^ASTRID emits inbox claims:
              claim|counter|^ASTRID(inbox,github)|eventos=2|1
```

Nothing new is needed to audit the stream: the inbox is a PDB global like
any other, so the registered digest already covers it. The agent sees the
events arrive and can flag schema breaks, duplicates, or missing sources —
or refuse to answer when the data is not there.

## Run it

```bash
# terminal 1 — the webhook
python examples/ingest/ingest_demo.py --db /tmp/astrid_ingest.db

# terminal 2 — fire events
curl -X POST "http://127.0.0.1:8787/hook?origen=github" \
     -H "Content-Type: application/json" \
     -d '{"event": "push", "repo": "astrid", "ref": "main"}'
curl -X POST "http://127.0.0.1:8787/hook?origen=github" \
     -H "Content-Type: application/json" \
     -d '{"event": "push", "repo": "astrid", "ref": "docs"}'
curl -X POST "http://127.0.0.1:8787/hook?origen=webhook" \
     -H "Content-Type: application/json" \
     -d '{"event": "ping"}'

# inspect what the agent will see next time she is asked
curl "http://127.0.0.1:8787/digest" | python -m json.tool
```

The digest output includes the inbox claims:

```
claim|counter|^ASTRID(inbox,github)|eventos=2|1
claim|counter|^ASTRID(inbox,webhook)|eventos=1|1
```

## The contract (keep it honest)

- **`INGEST^ASTRID(origen, raw)`** appends one event: `origen` is a short
  source label (≤ 32 chars, no spaces), `raw` is the original payload kept
  as received. The sequence number is per source.
- The inbox is **append-only** for external writers — no in-place edits.
  Auditing and corrections are Astrid's job, not the webhook's.
- A `POST` whose body is not JSON is rejected with `400` before it touches
  the PDB: the gate is at the door, not in the audit.
- The webhook is deliberately dependency-free (stdlib only) so the pattern
  is readable; route it behind your own auth (token, network policy) when
  you deploy it — lumen's access control is the envelope.

## What this demonstrates

1. **Lumen ingests**: an HTTP → MVM → PDB path with ~40 lines of stdlib.
2. **The agent audits arrivals**: same digest, same schema, same
   `evidence:true|false` contract — no special mode for external data.
3. **The notary loop is now complete**: source → registration → audit →
   (next step) signed anchor, so any agent can verify *what* arrived,
   *when*, and *that Astrid saw it*.

See `src/astrid.m` (`INGEST` tag and the inbox block of `EVIDENCE`) and
`docs/EVIDENCE_SCHEMA.md` for the claim schema. The suite covers the loop
(`python tests/run_tests.py`, checks "INGEST escribe inbox" / "digest ve
inbox …").
