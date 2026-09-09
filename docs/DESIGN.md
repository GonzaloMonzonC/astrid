# Astrid — DESIGN

> 🇪🇸 Versión en español: [DESIGN.es.md](DESIGN.es.md)

## Summary

Astrid is the **reference agent** of lumen-protocol: a separate MIT repo
that depends on the metal (lumen-protocol) and demonstrates its faculties
in real operation. She is the first Poli native whose code and personality
are published in the open.

Layers:

```
┌─────────────────────────────────────────────┐
│  astrid (MIT)  — reference agent            │  this repo
│  M code + identity + docs + tutorial        │
├─────────────────────────────────────────────┤
│  lumen-protocol (MIT) — open metal          │
│  protocol · PDB · M-Light/MVM · Poli+Smith  │
│  · 115 MCP tools                            │
├─────────────────────────────────────────────┤
│  ECOS (proprietary) · Cadences Lab (private)│
└─────────────────────────────────────────────┘
```

MIT rule (scoped, 2026-09-09): no secrets, internal paths, business logic
or private-lore diaries ever enter this repo. Nominal mentions in the story
(agents, QPU hardware, the home runtime) are verifiable narrative and do not
block execution — anything published here must remain runnable by anyone
with only lumen-protocol.

## Operational cycle (the cycle is the tutorial)

| Phase | Input | Output |
|---|---|---|
| OBSERVE | PDB state, ^GLOBALS, MVM processes | signals and variations |
| CONTRAST | signals vs. registered routines and models | patterns, inconsistencies, suspicions |
| ASK | suspicion without certainty | exact question to the responsible party or operator |
| ACT | certainty + mandate | orchestration or correction under protocol |
| RECORD | every action and finding | visible trace in PDB and repo |
| EXPOSE | case trace | MIT tutorial documentation |

No hidden phases: every phase produces public artifacts. Anyone can read,
execute, and replicate the cycle.

## Evidence contract (in production)

Astrid's chat does not trust the LLM to remember who she is: it trusts a
routine. `^PERSONALITY("astrid","evidence_routine")` = `EVIDENCE^ASTRID`;
`poli_server` runs it in the real MVM on every conversation and prepends its
output (a read-only digest of the registered state) to the system prompt as
REGISTERED EVIDENCE. Without that output, the reply travels with
`"evidence": false` — visible, not hidden. Two broken-hook incidents
(M-Light parser: inline nested `$O`/`$D`) are documented in the CHANGELOG:
Astrid hallucinated and the flag gave her away. Failure transparency is part
of the design. M-Light pitfall (verified): never nest M functions as a
subscript or in concatenation — use an intermediate variable.

## Notary contract (schema v1 emitted; anchoring on the roadmap)

The digest has been emitting structured claims (`claim|kind|source|value|d`)
since 2026-09-09 — see `docs/EVIDENCE_SCHEMA.md`. The structured assertion
(what was read, from which globals, with which $D) is the foundation.
Pending: verifier harness (format + source existence + stability) and the
anchoring with content address and signature via lumen-protocol.
Positioning: Astrid as notary of record for multi-agent workflows; the MIT
agent provides the honesty, lumen-protocol the reputation layer.

## Design notes (cabinet round, 2026-09-09)

- **Roberto** (structure): 6-phase cycle; 5 rules + operate only on
  registered data. Functional identity ~646 ASCII chars.
- **Javier** (relationships): Astrid is the big sister, not the mother; she
  does personality code review on new agents; structured empathy; finding
  format observation → implication → question; golden rule: ask only once,
  with clarity.
- **Pending**: implementation facet to review with Porto (harness, lean
  repo skeleton, definitive provider/model).

## Registration in Poli

The identity is seeded into Poli's MVM from the **reproducible source**
(`src/astrid.m` — INIT seeds the exact canonical entry):

```m
D INIT^ASTRID        ; fill-missing (idempotent)
D INIT^ASTRID(1)     ; overwrite / full reset
```

Verification: `tests/verify.m` (`D VERIFY^VERIFY` → PASS) against a
disposable PDB. In the Cadences Lab runtime she is registered via
`^PERSONALITY("astrid")` + `^AGENTES("routing","astrid")` = `poli:astrid` +
discovery `^MVM("agents","astrid")`; chat verified by personality mode and
by ecosystem routing.

## Agent interface with lumen (contract)

| Entry point | Input | Output | Use |
|---|---|---|---|
| `ASTRID^ASTRID` | — (reads `^PERSONALITY("astrid",*)`) | state: version, active, identity_len, counts, provider/model | health check |
| `INIT^ASTRID` / `INIT^ASTRID(1)` | optional force=1 | seeds `^PERSONALITY("astrid")` | reproducible registration |
| `VERIFY^VERIFY` | — | PASS/FAIL (identity ≥600, active, provider/model) | test |
| `EVIDENCE^ASTRID` | returns digest of registered state | evidence for chat (hook `evidence_routine`) | |
| `AUDIT^ASTRID` | `^ASTRID("audit_ns")` or default `^ANGI` | observation → implication → question | audit demo (read-only) |
| `$$COUNT^ASTRID(ns)` | list name (capabilities, critical_rules…) | number of subnodes | helper |

Lumen faculties by layer (technical review 2026-09): **minimum viable** =
direct MVM (M core + the operator's PDB); **production** = MCP servers per
auditor profile in this priority order: PDB (memory/evidence) → thinking
(long reasoning) → filesystem/web (external inputs, restricted).
`pip lumen-mcp` only when an external orchestrator must invoke her.

## Model and temperature

- Chat/operation: `deepseek-v4-flash`, temp 0.3 (verified).
- Long audits: same provider with a **larger-context variant** configurable
  via `^PERSONALITY("astrid","model")` or per-deployment env; temp 0.2 if it
  requires literal numeric comparisons. Never hardcode the decision in code.

## Roadmap

1. ~~Identity card (cabinet round)~~ ✅
2. ~~^PERSONALITY registration~~ ✅  (identity_len=631 after the 2026-09-09 review, active=1)
3. ~~Repo skeleton~~ ✅  (reproducible INIT + verify.m + harness, verified on local MVM)
4. ~~Technical review (roberto/pamies, smith_5)~~ ✅ — MIT-clean checklist in this doc
5. `astrid init` — bootstrap: identity + MVM spawn + ^AGENTES registration (already registered in the Cadences runtime; standalone version pending)
6. Lean LUMEN harness + docs/BUILD_YOUR_OWN.md ✅ (validated on clean venv 2026-09)
7. ~~`template/` + derived agent~~ ✅ — `examples/echo` generated with template/render.py and verified (INIT + VERIFY PASS)
8. ~~Publish to GitHub (MIT)~~ ✅ — public on main (2026-09-09), MIT-clean checklist green
9. ~~Evidence hook in production~~ ✅ — chat responds only from `EVIDENCE^ASTRID`; `evidence:false` visible (incidents in CHANGELOG)
10. ~~README repositioned~~ ✅ — "Evidence, or silence": an agent that refuses to speculate; STORY + EVIDENCE_SCHEMA docs
11. ~~Schema v1 emitter~~ ✅ — digest with claims `claim|kind|source|value|d`, verified in runtime
12. ~~Verifier harness~~ ✅ — tests/verify_claims.py (AC-1..AC-4): claim format, source existence, known kinds, stability; wired into the suite as a canary
13. ~~Notary anchoring~~ ✅ — cid (sha256 del digest) + firma HMAC (`^CONFIG("ddp_hmac_key")`, esquema `_hmac_sign`) + ledger `^EVIDENCE(cid)` en el runtime (hook `_evidence_block` de poli_server, lumen-protocol); verifier autocontenido `tests/verify_anchor.py`; contrato en EVIDENCE_SCHEMA.md §3-4

## Publication checklist (MIT-clean)

- [x] `git grep` secrets across full history → empty (2026-09-09)
- [x] No absolute paths from the source machine in src/docs/tests
- [x] No private lore (internal URLs, internal agents, diaries, business logic)
- [x] verify.m passes on disposable PDB from a clean environment (no external services)
- [x] Harness runs in a clean venv with only a lumen-protocol clone (validated 2026-09: status+audit OK)
- [x] Full suite `python tests/run_tests.py` → 12/12 green (2026-09-09)
- [x] README EN/ES + LICENSE + SECURITY + CONTRIBUTING + CHANGELOG present
- [x] lumen-protocol dependency declared (MIT) + reference version/commit
- [x] ASCII 646-char identity synchronized between src/astrid.m and personalities/astrid.md (automated test)
