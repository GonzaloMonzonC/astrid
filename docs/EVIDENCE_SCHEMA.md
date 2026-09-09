# Digest schema v1 — the notary contract (design)

_How Astrid's registered evidence becomes a machine-readable claim._

Status: **emitter in production (2026-09-09, verified on the real MVM)**.
`EVIDENCE^ASTRID` emits parseable claims `claim|<kind>|<source>|<value>|<d>`
(production digest ≈ 25 claims with the 5-worker MCP register). The digest
is a canary in the test suite (20 checks). The anchor — cid + signature +
`^EVIDENCE` ledger — is implemented in the runtime (see section 3); the
self-contained verifier is `tests/verify_anchor.py`.

---

## 1. What exists today (production, verified)

`EVIDENCE^ASTRID` is a read-only M routine. Each chat turn, the runtime
(`poli_server`) resolves `^PERSONALITY("astrid","evidence_routine")`, runs
the routine in the real MVM, and prepends its stdout to the system prompt as
**REGISTERED EVIDENCE**. If the run fails or is empty, the response carries
`"evidence": false` — visible by contract, never hidden.

Current digest shape — schema v1, one claim per line (truncated for
readability; ≈25 claims per digest in production):

```
Astrid v0.3.0 | active=1 | mode activo=astrid | evidence=true
claim|mode|^ACTIVE|astrid|1
claim|counter|^ANGI(level1)|1|10
claim|metric|^ANGI(metrics,agents_online)|{"value": 12, "updated": "2026-09-09T18:25:23Z"}|1
claim|route|^AGENTES(routing,astrid)|{"tipo": "poli", "mode": "astrid"}|1
claim|config|^SPACE(ASI)|127.0.0.1 :9102|10
claim|counter|^QUANTUM(colapso)|119|10
claim|entry|^QUANTUM(colapso,ultimo)|idx=119 raw={"idx": 119, "ts": "...", "backend": "Tuna-17"}|1
claim|note|^VIRTUAL|no existe (la virtualizacion vive en ^MVM)|0
claim|counter|^SYS(MCP)|servers=5|10
claim|config|^SYS(MCP,worker1)|type=http url=https://worker1.internal.example/mcp|1
REGLA: responde SOLO con estos datos registrados; ...
```

Each line is a **claim with a visible source** (the global it was read
from). That is the seed of the notary contract.

Since 0.3.0 the digest also audits the **device-MCP register**
(`^SYS("MCP", <server>, url|type)`) — the mesh workers seeded by the
operator for `$DEVICE("mcp:call", ...)`. Astrid therefore sees the wiring
of her cognitive OS (which workers exist and how to reach them) under the
same read-only evidence contract. Live reachability is NOT part of the
digest: it would require outbound device calls per chat turn. The register
is the fact; a health probe is a separate routine.

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

## 3. Anchor (implemented 2026-09-09, runtime lumen-protocol)

Claims were self-reported by the runtime that produced them. The anchor
adds external verifiability — implemented in `poli_server` (lumen-protocol),
inside the evidence hook (`_evidence_block`), so **every digest emitted in
production is anchored at generation time**:

- **Content-addressed**: `cid = sha256(digest)` (hex). Two agents comparing
  `cid`s know they saw the same state; identical state → identical digest →
  identical `cid` (stability is a suite canary).
- **Signed**: runtime key `^CONFIG("ddp_hmac_key")` → HMAC-SHA256
  (`ts + cid + secret`, the ecosystem's standard `_hmac_sign` scheme). Any
  agent holding the shared key can confirm who produced the digest and when
  (ts is stored next to the signature).
- **Ledger**: append-only `^EVIDENCE(cid) = "<sig>|<ts>|<routine>"` with the
  digest line-by-line under `^EVIDENCE(cid,"digest",n)` (M-native, no
  embedded newlines). Same state → same cid → row already exists → no
  duplicate (natural dedup). Anchoring never breaks the chat: failures are
  silent.
- **Verifier**: `tests/verify_anchor.py` (MIT, self-contained) replicates
  the runtime anchor on a throwaway PDB with a TEST key and checks cid
  stability, ledger shape, signature validity and digest round-trip. The
  real key never enters the repo.

Why lumen-protocol: the MVM provides the execution boundary, PDB the shared
ledger, M-Light the portable runtime. Astrid (MIT) supplies the honest
design; lumen-protocol supplies the layer that makes honesty **provable
across agents** — the reputation layer under a permissive license.

## 4. Open questions (resolved 2026-09-09)

1. Key management → **shared-key start**: the runtime signs with the
   existing `^CONFIG("ddp_hmac_key")` (same key that already authenticates
   worker calls). Rotation = rotate the global; no PKI yet.
2. Granularity → **whole digest**: one `cid` per digest. Per-claim signing
   stays a candidate if subset verification is ever needed.
3. Ledger namespace → **`^EVIDENCE(cid)` flat**: sha256 cids are globally
   unique across agents by construction; the head row stores the routine
   that produced each digest.
4. Schema versioning → the digest header carries the agent version
   (`Astrid v0.3.0 | ...`), so the version is inside the signed payload;
   no separate registry needed for v1.

## 5. Acceptance criteria for v1

- [ ] **AC-1** `EVIDENCE^ASTRID` emits schema-formatted lines (source always present)
- [ ] **AC-2** `evidence:false` path is testable in the test suite
- [ ] **AC-3** A verifier script (harness) checks: line format, source existence in a
      given PDB snapshot, cid stability across identical states
- [ ] **AC-4** Docs updated: README (notary contract section), STORY, DESIGN
