# Digest schema v1 — the notary contract (design)

_How Astrid's registered evidence becomes a machine-readable claim._

Status: **emisor en producción (2026-09-09, verificado en el MVM real)**.
`EVIDENCE^ASTRID` emite claims `claim|<kind>|<source>|<value>|<d>`
parseables (19 claims por digest). Pendiente: verifier harness (AC-2..AC-4)
y el anclaje (sección 3).

---

## 1. What exists today (production, verified)

`EVIDENCE^ASTRID` is a read-only M routine. Each chat turn, the runtime
(`poli_server`) resolves `^PERSONALITY("astrid","evidence_routine")`, runs
the routine in the real MVM, and prepends its stdout to the system prompt as
**REGISTERED EVIDENCE**. If the run fails or is empty, the response carries
`"evidence": false` — visible by contract, never hidden.

Current digest shape — schema v1, one claim per line (truncated for
readability; 19 claims per digest in production):

```
Astrid v0.1.0 | active=1 | mode activo=astrid | evidence=true
claim|mode|^ACTIVE|astrid|1
claim|counter|^ANGI(level1)|1|10
claim|metric|^ANGI(metrics,agents_online)|{"value": 12, "updated": "2026-09-09T18:25:23Z"}|1
claim|route|^AGENTES(routing,astrid)|{"tipo": "poli", "mode": "astrid"}|1
claim|config|^SPACE(ASI)|127.0.0.1 :9102|10
claim|counter|^QUANTUM(colapso)|119|10
claim|entry|^QUANTUM(colapso,ultimo)|idx=119 raw={"idx": 119, "ts": "...", "backend": "Tuna-17"}|1
claim|note|^VIRTUAL|no existe (la virtualizacion vive en ^MVM)|0
REGLA: responde SOLO con estos datos registrados; ...
```

Each line is a **claim with a visible source** (the global it was read
from). That is the seed of the notary contract.

## 2. Schema v1 (emitting in production)

The digest is line-oriented, one fact per line. Every claim is emitted as:

```
claim|<kind>|<source>|<value>|<d>
```

| Field | Meaning | Example |
|---|---|---|
| `kind` | claim type | `metric` / `entry` / `config` / `route` / `counter` / `note` |
| `source` | global + subscripts read | `^ANGI(metrics,agents_online)` |
| `value` | raw value or digest of it | `{"value":12,...}` |
| `d` | `$D`-style presence code | `0` / `1` / `10` / `11` |

Note: there is no separate `ts` field — timestamps live inside the raw
`value` when the source data carries them (e.g. `"updated"` in `^ANGI`
metrics). A machine-readable `ts` per claim is a candidate for the anchored
version (section 3).

Rules:

1. **No claim without a source.** A line with no `source` is not evidence;
   it must not be produced (and if it appears, downstream treats it as
   `evidence:false`).
2. **The routine never writes.** Digest generation is read-only by design;
   any write attempt aborts the run (defense in depth for the notary role).
3. **`evidence:true|false` is part of the payload**, always present.

## 3. Anchor (next step, lumen-protocol)

Formalized claims are still self-reported by the runtime that produced them.
The anchor adds external verifiability:

- **Content-addressed**: digest → stable hash (`cid`). Two agents comparing
  `cid`s know they saw the same state.
- **Signed**: runtime key → signature over `cid + ts`. A verifier (any other
  agent in the mesh, or a cron) can confirm who produced the digest and
  when.
- **Ledger**: append the `cid` to the shared PDB (e.g. `^EVIDENCE(cid)`)
  so the trail is inspectable, not just asserted.

Why lumen-protocol: the MVM already provides the execution boundary, PDB the
shared ledger, M-Light the portable runtime. Astrid (MIT) supplies the
honest design; lumen-protocol supplies the layer that makes honesty
**provable across agents** — the reputation layer under a permissive
license.

## 4. Open questions (for the team)

1. Key management: which runtime key signs digests, and how do workers
   (Hermes, Tom, cron) verify without a PKI? (HMAC shared-key start, rotate
   per host?)
2. Granularity: sign the whole digest, or per-claim (so a verifier can
   accept subset claims)?
3. Does `^EVIDENCE` belong in the public lumen-protocol namespace or a
   per-agent namespace?
4. Schema versioning: `AstridSchema.v1` — where does the registry live?

## 5. Acceptance criteria for v1

- [ ] `EVIDENCE^ASTRID` emits schema-formatted lines (source always present)
- [ ] `evidence:false` path is testable in the test suite
- [ ] A verifier script (harness) checks: line format, source existence in a
      given PDB snapshot, cid stability across identical states
- [ ] Docs updated: README (notary contract section), STORY, DESIGN
