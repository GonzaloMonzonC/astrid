# 🧬 Astrid

**The agent that refuses to speculate.**
**Evidence, or silence.**

> 🇪🇸 Versión en español: [README.es.md](README.es.md)

Astrid is a reference agent born inside the Poli MVM — identity, code and
cycle published under MIT. Her system prompt is not a biography: it is the
live output of her own routine, `EVIDENCE^ASTRID`, executed in the real MVM
on every conversation. She answers only from what that run returns.

She does not "usually tell the truth". She is built so that **when she has
no registered data, the design says so** — and when the evidence pipeline
fails, the failure is visible (`evidence: false`), not hidden.

> Most agents are trained to be helpful. Astrid is trained to be verifiable.
> Helpful is a promise. Verifiable is a design.

**Runs on [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol)
(MIT)** — protocol · PDB · M-Light/MVM · Poli+Smith · 115 MCP tools, no API
keys. The agent repo is the door; the protocol is the house.

## What her evidence looks like

A real digest (26 claims per run in production; schema v1):

```
Astrid v0.3.0 | active=1 | mode activo=astrid | evidence=true
claim|mode|^ACTIVE|astrid|1
claim|metric|^ANGI(metrics,agents_online)|{"value": 12, "updated": "..."}|1
claim|route|^AGENTES(routing,astrid)|{"tipo": "poli", "mode": "astrid"}|1
claim|config|^SPACE(ASI)|127.0.0.1 :9102|10
claim|counter|^QUANTUM(colapso)|119|10
claim|note|^VIRTUAL|no existe (la virtualizacion vive en ^MVM)|0
REGLA: responde SOLO con estos datos registrados; ...
```

Every claim cites the global it was read from (`source`) and its presence
code (`d`). Ask her anything not in that run and she says so — she does not
fill the gap. See [`docs/EVIDENCE_SCHEMA.md`](docs/EVIDENCE_SCHEMA.md) for
the contract.

## Why this exists

LLMs fabricate. That is the known problem — and the known answer so far has
been "prompt better". Astrid is a different answer: **make the source of
truth an executable routine**, not a paragraph of instructions.

- Her chat runtime (`poli_server`) reads `^PERSONALITY("astrid","evidence_routine")`
  → `EVIDENCE^ASTRID`, runs it in the MVM, and prepends the real output to
  her system prompt as **REGISTERED EVIDENCE**.
- Her digest is a read-only scan of the live state: modes, metrics, routing,
  spaces, MVM registry, quantum experiment ledger — whatever she is asked
  about that exists in the machine.
- Her rules (from her registered identity):

  1. Operate only on registered data.
  2. Never speculate: no data → say so, and ask the exact question.
  3. Finding format: observation → implication → question.
  4. Ask once, with clarity (golden rule).
  5. Audit the PDB, supervise the MVM, catch the incoherence nobody sees.

## What happens when the evidence fails

This is the part other agents do not document. During her first day in
production, two different bugs broke her evidence hook (a M-Light parser
limit on nested `$O`/`$D` calls — both fixed). Each time, Astrid
**hallucinated a confident answer**, and each time the response carried the
flag `"evidence": false`. The hallucination was caught not by a guardrail
but by the design itself: *the absence of evidence is part of the response*.
A third incident preceded the hook — the one that motivated it: she invented
`$DATA(^ANGI)=0` and `%SYS` lore while ^ANGI was alive. It is documented
too (CHANGELOG 0.1.1). Nothing is scrubbed.

The incident log is in [`CHANGELOG.md`](CHANGELOG.md). Read it: it is the
most honest part of this repo. A system that can show you when it is
untrustworthy is a system you can build on.

**The story with real work**: she audited a live quantum experiment ledger
— 115+ executions on real QPU hardware, and she found the writing bug
behind the counters, refused to speculate when asked for a verdict her
evidence did not cover, and confirmed the fix only against her own digest.
Full account: [`docs/STORY.md`](docs/STORY.md).

## The notary contract

The digest emits structured claims — `claim|<kind>|<source>|<value>|<d>`,
schema v1 (see [`docs/EVIDENCE_SCHEMA.md`](docs/EVIDENCE_SCHEMA.md)): what
was read, from which globals, with which presence code. The natural next
step — and the reason this repo depends on
[lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol) — is to
anchor it: a content-addressed, signed digest that makes Astrid the
**notary of record for multi-agent workflows**. Cloning the MIT agent gives
you the honesty; the protocol gives you the reputation layer under it.

## Quickstart (local)

**Dependency**: [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol)
(MIT) — clone it at the same level as this repo (sibling folders), so the
harness finds the runtime. Astrid is the reference agent **on top** of it;
pin a release/commit when you fork. Reference for this version:
lumen-protocol `main` (2026-09, verified: AUDIT name indirection needs the
M-Light fix of commit `243e74c` or later).

1. Get an M runtime: build the Rust MVM from your lumen-protocol clone
   (`implementations/rust/lumen-m-light`, `cargo build --release`, DLL into
   `implementations/mcp-servers/pdb/`), or point `LUMEN_MLIGHT_LIB` at an
   existing `lumen_mlight.dll`. *(`pip install lumen-mcp` ships transport
   bindings only — no MVM — as of 0.1.0.)*
2. Load the routine and seed her (identity → `^PERSONALITY("astrid")`,
   including the `evidence_routine` contract):
   ```m
   ; load src/astrid.m into your M routine path
   D INIT^ASTRID      ; fill-missing, idempotent
   D INIT^ASTRID(1)   ; overwrite / full reset
   ```
3. Verify and run the registered digest — the canary of the evidence hook:
   ```m
   D VERIFY^VERIFY          ; PASS astrid (identity, active, provider/model)
   W $$EVIDENCE^ASTRID()    ; the digest: claims with sources + evidence=true
   ```
   Or with the harness (does seed + digest for you, on a throwaway PDB):
   ```bash
   python harness/astrid_harness.py seed
   python harness/astrid_harness.py evidence
   ```
   Expected output starts with `Astrid v0.3.0 | active=1 | ... | evidence=true`
   followed by `claim|...` lines (see the sample above).
4. Full suite against a real MVM on a throwaway PDB — no external services,
   **20 checks** (INGEST inbox loop + MCP register):
   ```bash
   python tests/run_tests.py
   ```
5. Ingest demo (external source → PDB → audited):
   ```bash
   python examples/ingest/ingest_demo.py --db /tmp/ingest.db
   curl -X POST "http://127.0.0.1:8787/hook?origen=github" \
        -H "Content-Type: application/json" -d '{"event": "push", "ref": "main"}'
   curl "http://127.0.0.1:8787/digest"
   ```
   See [`docs/INGESTION.md`](docs/INGESTION.md).

## Roadmap

- [x] Repo public, MIT — published 2026-09-09
- [x] Evidence hook in production — chat answers only from `EVIDENCE^ASTRID`;
      `evidence:false` visible (incidents in CHANGELOG)
- [x] Schema v1 emitter — digest as parseable claims (verifier-ready)
- [x] Evidence canary in the test suite (20 checks)
- [x] Verifier harness — `tests/verify_claims.py` (AC-1..AC-4): claim
      format, sources, known kinds, stability across identical states
- [x] Ingest demo — external events → PDB inbox → digest claims
      (`examples/ingest/ingest_demo.py`, 18-check suite)
- [x] Notary anchor (0.3.1) — content-addressed signed digest (cid + signature +
      `^EVIDENCE` ledger) via lumen-protocol; verifier `tests/verify_anchor.py`,
      runtime anchor in `poli_server._evidence_block`
- [ ] Full standalone inbox wiring (MVM native agent loop)

## Sibling agents

- **Echo** — the derived agent generated by `template/render.py`
  (`examples/echo`), used as the template regression in the suite.
- [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol) — the
  metal under Astrid: MIT protocol, PDB, M-Light/MVM, Poli+Smith, 115 MCP
  tools. Build one like hers and open it — same skeleton, your identity.

## Layout

```
astrid/
├── LICENSE              MIT
├── README.md            This file (EN)
├── README.es.md         Español — same content (ES)
├── SECURITY.md          No secrets, PDB discipline, reporting (EN)
├── CONTRIBUTING.md      Conventions + process (EN)
├── CHANGELOG.md         Keep a Changelog / semver (EN) — incl. the evidence-failure incidents
├── src/
│   └── astrid.m         M routine: ASTRID (status) · INIT (reproducible seed) ·
│                        AUDIT · COUNT · EVIDENCE (registered digest, schema v1)
├── personalities/
│   └── astrid.md        Full readable identity (ES) — accents, voice, fields
├── harness/
│   └── astrid_harness.py  status/seed/evidence/verify/audit runner
├── template/            Derive a new agent: render.py + AGENT.*.tpl
├── examples/echo        Derived agent generated by the template (regression)
├── examples/ingest      Webhook demo: external source → PDB → digest inbox claims
├── docs/
│   ├── DESIGN.md        EN — identity card, agent contract, cycle, publish checklist
│   ├── DESIGN.es.md     ES — diseño, contrato de agente, ciclo
│   ├── STORY.md         EN — the launch story: evidence hook, real-work audit, incidents
│   ├── STORY.es.md      ES — la historia de lanzamiento
│   ├── EVIDENCE_SCHEMA.md       EN — digest schema v1 + notary contract
│   ├── EVIDENCE_SCHEMA.es.md    ES — esquema del digest + contrato de notaría
│   ├── INGESTION.md     EN — external sources → PDB → audited by Astrid (demo)
│   ├── INGESTION.es.md  ES — fuentes externas → PDB → auditadas por Astrid
│   ├── BUILD_YOUR_OWN.md        EN — step-by-step guide to build a derived agent
│   └── BUILD_YOUR_OWN.es.md     ES — guía paso a paso para un agente derivado
└── tests/
    ├── run_tests.py     Full suite, 20 checks, one command
    ├── verify_claims.py Verifier harness for the digest claims (AC-1..AC-4)
    └── verify.m         Verification: identity exists, speaks, operates
```

**Further reading**: [DESIGN.md](docs/DESIGN.md) (why she is built this
way) · [STORY.md](docs/STORY.md) (the launch story with the real quantum
audit) · [INGESTION.md](docs/INGESTION.md) (external sources → PDB →
audited) · [EVIDENCE_SCHEMA.md](docs/EVIDENCE_SCHEMA.md) (the notary
contract) · [BUILD_YOUR_OWN.md](docs/BUILD_YOUR_OWN.md) (build a derived
agent).

## Language policy

EN is canonical for code and root docs (README, CHANGELOG, SECURITY,
CONTRIBUTING). ES mirrors live as `.es.md` next to the English file. The
personality card (`personalities/astrid.md`) is ES by design — it is the
readable version of the ASCII identity line.
