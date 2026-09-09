# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/) and the repo uses semantic
versioning.

## [0.2.0] — 2026-09-09 (published on GitHub, main)

### Added
- Repo published: https://github.com/GonzaloMonzonC/astrid (public, MIT).
- README repositioned — **"Evidence, or silence"**: the agent that refuses
  to speculate. System prompt = live output of `EVIDENCE^ASTRID` executed on
  the MVM; "what happens when the evidence fails" section; the notary
  contract as the roadmap into lumen-protocol. EN + ES mirrors (`.es.md`).
- `docs/STORY.md` (+ ES) — the launch story: the real quantum audit, the
  hallucination incidents caught by the design.
- `docs/EVIDENCE_SCHEMA.md` (+ ES) — digest schema, notary contract,
  open questions, acceptance criteria.
- Digest extended with ^SPACE (binds), ^MVM (router/api/agents) and
  ^QUANTUM (collapse/job/latest) — Astrid audits data spaces and
  virtualization.
- **Schema v1 emitter**: `EVIDENCE^ASTRID` emits parseable claims
  `claim|<kind>|<source>|<value>|<d>` (18 claims per digest in production,
  verified on live state). Verified absences become claims with d=0.
- Team review pass (Lisa/Angi/Campo/Gon structural + devx + voice audits):
  i18n structure EN canonical + ES mirrors; MIT rule scoped (nominal story
  mentions allowed; secrets/paths/business logic never); harness got
  `seed` / `evidence` / `verify` modes so the digest is runnable by a
  documented path; test suite 12 → 16 checks.
- **Evidence canary in the suite**: `EVIDENCE^ASTRID` runs on the throwaway
  PDB; header must say `evidence=true`; every `claim|` line must have a
  source and exactly 5 fields; the `evidence_routine` contract must be
  seeded after INIT.
- **Ingest demo (source → PDB → audit)**: `INGEST^ASTRID(origen, raw)`
  appends external events to `^ASTRID("inbox", <origen>, <seq>)`; the
  digest emits inbox claims (`claim|counter|^ASTRID(inbox,github)|...`), so
  Astrid audits the incoming stream with her normal contract.
  `examples/ingest/ingest_demo.py` is a stdlib-only webhook (POST → PDB →
  digest); `docs/INGESTION.md` (+ ES) documents the pattern. The suite grew
  to 18 checks, covering the ingest loop (verified end-to-end: events POSTed
  to the demo webhook show up as inbox claims in the digest).

### Fixed
- `$O(...)` nested as a subscript broke EVIDENCE (M-Light parser limit):
  empty digest → chat without evidence → Astrid hallucinated quantum
  branches (`QAL/ENT_CTRL/TELEP`). Fix: intermediate variable `uk`.
  Verified: `evidence:true` and real audit of ^QUANTUM.
- `$D`/`$O` inline inside a concatenation broke EVIDENCE (same limit):
  hallucinated a verdict with invented `fidelity`/`^NORM`, exposed by
  `evidence:false`. Fix: `$D` only on SET RHS via an intermediate variable.
  **M-Light construction rule**: never nest M functions inline as a
  subscript or inside a concatenation — use an intermediate variable.
- `SEED` did not write `^PERSONALITY("astrid","evidence_routine")` — the
  hook contract was applied by hand in production. Now part of the
  reproducible seed (+ suite check).
- Removed a stale claim in EVIDENCE (`^QUANTUM(ultimo,stats)` with a
  hardcoded value, fixed date and a `$D` measured on the wrong node — it
  violated the schema it was emitted under).
- Identity version bumped to 0.2.0 (was drifting against the repo version);
  personality card (`personalities/astrid.md`) synced.

## [0.1.1] — 2026-09-09 (production fix)

### Fixed
- `AUDIT^ASTRID` counted 0 entries on real Poli: it used the TWO-at
  indirection form `$O(@ns@(k))`, which is not canonical MSM. The correct
  form is ONE at-sign (`@ns(k)` with `ns="^ANGI"`), implemented in the
  M-Light runtime (lumen-protocol commit `243e74c`: name indirection in
  `$O`/`$D`/`$G`/SET/KILL + the `X`/`XECUTE` command, which did not exist
  either). Verified on Poli production: first real dynamic audit (^ANGI →
  1 first-level entry — `metrics`).
- The personality chat invented evidence (said `$DATA(^ANGI)=0` and
  `%SYS`/`M67`/`ZALLOCATE` lore while ^ANGI was alive). Fix in two parts:
  1. `EVIDENCE^ASTRID` — read-only digest of registered state (QUIT
     string): active, ^ANGI (entries + raw metrics), astrid routing + the
     usage rule.
  2. poli_server: generic `evidence_routine` hook per personality
     (`^PERSONALITY(mode,"evidence_routine")`): before the `llm:call` it
     runs the real M routine and prepends its output to the system prompt
     as REGISTERED EVIDENCE. Verified: Astrid audits with real data
     (agents_online=12, mode-vs-routing incoherence detected) — zero
     invention.
  This is the third documented hallucination incident: the one that
  *motivated* the hook. The other two (0.2.0) were caught by the hook's
  `evidence:false` flag.

## [0.1.0] — 2026-09-09 (pre-publication)

### Added
- `tests/run_tests.py` — full suite, one command (12 checks, all green):
  INIT (empty/idempotent/force) + status, VERIFY PASS/FAIL parametric,
  AUDIT demo, identity sync M↔MD (ASCII, 600–1400), template render
  regression (scratch agent) and examples/echo regression. Runs against a
  real MVM on a throwaway PDB (no external services).
- `template/` + `template/render.py`: derive a new agent with one command
  (tokens: name, identity file, role, emoji, color…). Validated in-repo
  with `examples/echo` (generated by the renderer; INIT + VERIFY PASS on
  MVM).
- `tests/verify.m` now parametric: `D VERIFY^VERIFY("name")` checks any
  agent (default astrid).
- Harness validated on a clean venv (no Poli): status + audit OK using only
  a lumen-protocol clone; docs clarified that `pip install lumen-mcp` 0.1.0
  ships transport bindings only (no MVM — clone build or DLL required).
- Identity card for Astrid, designed in a multi-personality round
  (gabinete: estructura/relaciones + technical review) and registered in
  `^PERSONALITY("astrid")`: identity line (646 chars ASCII), core_mission,
  6 critical rules, 7 capabilities, peers, provider/model deepseek-v4-flash,
  temperature 0.3, `is_active=1`.
- `src/astrid.m` — M routine with agent contract entry points:
  `ASTRID` (status), `INIT` (reproducible seed, idempotent, `INIT(1)` forces),
  `AUDIT` (demo audit: observation → implication → question),
  `$$COUNT` (helper). Verified against a real lumen MVM on a throwaway PDB
  (INIT empty/idempotent/force + VERIFY + AUDIT: all ok).
- `tests/verify.m` — identity ≥ 600 chars, is_active, provider/model checks.
- `harness/astrid_harness.py` — status/audit runner against lumen-mcp or a
  local lumen-protocol clone.
- Docs: README (EN/ES), `personalities/astrid.md`, `docs/DESIGN.md`,
  `docs/BUILD_YOUR_OWN.md` (template guide), SECURITY.md,
  CONTRIBUTING.md, LICENSE (MIT).
- Ecosystem registration (Cadences Lab runtime): `^AGENTES("routing","astrid")`
  → `poli:astrid` and discovery key `^MVM("agents","astrid")`; chat verified
  via personality mode and via ecosystem routing.

### Pending (before/after first public release)
- Full inbox wiring (MVM native agent loop) for standalone installs.
- Verifier harness for the digest claims (AC-2..AC-4 in
  `docs/EVIDENCE_SCHEMA.md`).
- Notary anchor: content-addressed, signed digest (cid + signature +
  `^EVIDENCE` ledger via lumen-protocol).
