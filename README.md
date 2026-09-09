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

This is the part other agents do not document. During her first days in
production, two different bugs broke her evidence hook (a M-Light parser
limit on nested `$O`/`$D` calls — both fixed). Each time, Astrid **hallucinated
a confident answer**, and each time the response carried the flag
`"evidence": false`. The hallucination was caught not by a guardrail but by
the design itself: *the absence of evidence is part of the response*.

The incident log is in [`CHANGELOG.md`](CHANGELOG.md). Read it: it is the
most honest part of this repo. A system that can show you when it is
untrustworthy is a system you can build on.

## The notary contract

The digest emits structured claims — `claim|<kind>|<source>|<value>|<d>`,
schema v1 (see [`docs/EVIDENCE_SCHEMA.md`](docs/EVIDENCE_SCHEMA.md)): what
was read, from which globals, with which presence code. The natural next
step — and the reason this repo depends on
[lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol) — is to
anchor it: a content-addressed, signed digest that makes Astrid the
**notary of record for multi-agent workflows**. Cloning the MIT agent gives
you the honesty; the protocol gives you the reputation layer under it.

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
│   └── astrid_harness.py  status/audit runner (lumen-mcp or local clone)
├── docs/
│   ├── DESIGN.md        EN — identity card, agent contract, cycle, publish checklist
│   ├── DESIGN.es.md     ES — diseño, contrato de agente, ciclo
│   ├── STORY.md         EN — the launch story: evidence hook, real-work audit, incidents
│   ├── STORY.es.md      ES — la historia de lanzamiento
│   ├── EVIDENCE_SCHEMA.md       EN — digest schema v1 + notary contract
│   ├── EVIDENCE_SCHEMA.es.md    ES — esquema del digest + contrato de notaría
│   ├── BUILD_YOUR_OWN.md        EN — step-by-step guide to build a derived agent
│   └── BUILD_YOUR_OWN.es.md     ES — guía paso a paso para un agente derivado
└── tests/
    └── verify.m         Verification: identity exists, speaks, operates
```

Language policy: EN is canonical for code and root docs (README.md,
CHANGELOG, SECURITY, CONTRIBUTING). ES mirrors live as `.es.md` next to the
English file. The personality card (`personalities/astrid.md`) is ES by
design — it is the readable version of the ASCII identity line.

## Quickstart (local)

**Dependency**: [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol)
(MIT) — protocol, PDB, M-Light/MVM, Poli+Smith, 115 MCP tools. Astrid is the
reference agent **on top** of it; pin a release/commit when you fork.
Reference for this version: lumen-protocol `main` (2026-09).

1. Get an M runtime: build the Rust MVM from a lumen-protocol clone
   (`implementations/rust/lumen-m-light`, `cargo build --release`, DLL into
   `implementations/mcp-servers/pdb/`), or point `LUMEN_MLIGHT_LIB` at an
   existing `lumen_mlight.dll`. *(`pip install lumen-mcp` ships transport
   bindings only — no MVM — as of 0.1.0.)*
2. Load the routine and seed her (identity → `^PERSONALITY("astrid")`):
   ```m
   ; load src/astrid.m into your M routine path
   D INIT^ASTRID      ; fill-missing, idempotent
   D ASTRID^ASTRID    ; status
   W $$EVIDENCE^ASTRID()  ; the registered digest — read it, then talk to her
   ```
3. Verify (throwaway PDB, no external services) — **full suite, one command**:
   ```bash
   python tests/run_tests.py    # 12 checks: INIT/status/VERIFY/AUDIT + identity
                                # sync + template + echo regressions → all green
   ```
   or the individual M checks:
   ```m
   D VERIFY^VERIFY    ; → PASS astrid verificado
   ```
   or via the harness (status / demo audit against any local PDB):
   ```bash
   python harness/astrid_harness.py status
   python harness/astrid_harness.py audit --ns ^MYNS
   ```
4. Talk to her: personality mode `astrid` in any LUMEN chat runtime that
   reads `^PERSONALITY` + the `evidence_routine` contract (e.g. Poli), or via
   the LUMEN MCP servers (filesystem, web, thinking, PDB — zero API keys).

## Roadmap

- [x] Identity card (gabinete design round + technical review, 2026-09)
- [x] Registered in `^PERSONALITY("astrid")` + ecosystem routing (poli:astrid)
- [x] Repo skeleton: reproducible INIT, verify.m (parametric), harness, docs (EN/ES)
- [x] Template validated: `examples/echo` derived with `template/render.py` + verified on MVM
- [x] Harness validated on clean venv (lumen-protocol clone only)
- [x] **Published to GitHub (MIT)** — public, main
- [x] Evidence hook in production: chat answers from `EVIDENCE^ASTRID` output;
      `evidence:false` is visible when the pipeline fails (incidents in CHANGELOG)
- [ ] Full standalone inbox wiring (MVM native agent loop)
- [ ] Signed, content-addressed digest anchored via lumen-protocol (notary contract)

## Sibling agents

Astrid is the first **reference agent**. Planned siblings will expose other
LUMEN faculties (e.g. one focused on MVM process supervision, one on PDB
operations). Each is its own MIT repo with the same skeleton — see
`docs/BUILD_YOUR_OWN.md`.

---
