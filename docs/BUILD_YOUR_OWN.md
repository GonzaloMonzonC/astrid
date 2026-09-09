# Build your own Astrid-class agent

> This guide turns Astrid into a **template**: step by step, from zero to an
> agent of your own running on LUMEN with open MIT code. The skeleton is
> proven: Astrid herself was built this way and is running in production.

## 0. What you need

- [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol) — MIT:
  build the Rust MVM (`implementations/rust/lumen-m-light`,
  `cargo build --release`) and copy the DLL to
  `implementations/mcp-servers/pdb/`. *(`pip install lumen-mcp` 0.1.0 =
  transport bindings only, no MVM — a clone build or `LUMEN_MLIGHT_LIB` is
  required to run routines.)*
- Python 3.10+ (for the harness) and/or an M runtime that can load `.m`
  routines (lumen-mvm, or any MUMPS with PDB).

## 1. Copy the skeleton

```
cp -r astrid my-agent
cd my-agent
# rewrite: src/myagent.m, personalities/myagent.md, README
```

## 2. Write the identity

Identity is **one ASCII line, no accents, 600–1400 chars** stored in
`^PERSONALITY(name,"identity")` (MUMPS storage constraint) + a human-readable
file with accents and full voice (see `personalities/astrid.md`).

Seed fields (see the INIT pattern in `src/astrid.m`):

```
^PERSONALITY("myagent","name")        = "myagent"
^PERSONALITY("myagent","identity")    = "<ascii line>"
^PERSONALITY("myagent","core_mission")= "..."
^PERSONALITY("myagent","critical_rules","1") = "..."
^PERSONALITY("myagent","capabilities","NAME") = "..."
^PERSONALITY("myagent","provider")    = "deepseek"
^PERSONALITY("myagent","model")       = "deepseek-v4-flash"
^PERSONALITY("myagent","is_active")   = "1"
```

Rules of thumb from Astrid's design round:
- **core_mission** in one sentence: what you prove by existing.
- **3–6 critical rules**, imperative, testable; rule 1 is your "no speculation"
  equivalent: *operate only on registered data*.
- **5–7 capabilities** with short UPPER_CASE names (AUDIT_PDB, MVM_WATCH…).
- Every agent needs a **hallazgo format** (observation → implication →
  question) — it is what makes other agents able to follow your reasoning.

## 3. Wire the evidence hook (the non-negotiable piece)

This is what makes an agent *verifiable* instead of merely *helpful*:

1. Write `EVIDENCE^MYAGENT` — a **read-only** routine that returns a digest
   of the state your agent is allowed to answer from (one fact per line).
2. Emit claims in the schema: `claim|<kind>|<source>|<value>|<d>` — every
   claim cites the global it was read from (see
   `docs/EVIDENCE_SCHEMA.md`).
3. Register the contract: `^PERSONALITY("myagent","evidence_routine")` =
   `EVIDENCE^MYAGENT`. Chat runtimes that implement the hook (Poli's
   `poli_server`) will execute it before every conversation and prepend the
   output to the system prompt as REGISTERED EVIDENCE.
4. If the pipeline fails, the response must carry `"evidence": false` —
   visible, never hidden.

M-Light construction rules (hard-won — see CHANGELOG 0.2.0):
- `$D`/`$O`/nested functions **never** inline as a subscript or inside a
  concatenation. Assign to an intermediate variable first.
- The digest routine never writes globals; the `evidence` flag is always in
  the header line.

## 4. Give it a cycle (the cycle is the tutorial)

Astrid runs OBSERVAR → CONTRASTAR → PREGUNTAR → ACTUAR → REGISTRAR → EXPONER.
Each phase produces a **public artifact**. No hidden phases. Pick yours, keep
it small, and document every phase in `docs/DESIGN.md`.

## 5. Verify (before anything else)

`tests/verify.m` checks: identity ≥ 600 chars, is_active, provider/model set.
Run it in a **throwaway PDB** (see `harness/astrid_harness.py status`):
```
python harness/astrid_harness.py status
python harness/astrid_harness.py audit --ns ^MYNS
```
Add a check that `$$EVIDENCE^MYAGENT()` runs and every `claim|` line has a
non-empty source — that test is your canary against silent digest breakage.

## 6. Register and run

Register in the mesh so other agents can discover and talk to yours:
`^AGENTES("routing","myagent")` = your runtime route (e.g. `poli:myagent`)
and, on the MVM, the discovery key `^MVM("agents","myagent")`. Talk to your
agent through any chat runtime that reads `^PERSONALITY` + the
`evidence_routine` contract, or via LUMEN's MCP servers (filesystem, web,
thinking, PDB — zero API keys).

## 7. Publish MIT

Checklist before pushing to a public remote (Astrid's is green — see
`docs/DESIGN.md`):
- [ ] Zero private lore: no internal URLs, no diaries, no business logic of
      any private ecosystem. The repo must run with only lumen-protocol
      (`git grep -iE "api[_-]?key|token|secret|password"` over full history).
- [ ] LICENSE MIT + README EN/ES + docs/DESIGN.md present.
- [ ] Verify.m passes against a fresh PDB; `EVIDENCE^MYAGENT` emits claims
      with sources.
- [ ] Harness runs on a clean machine with only `pip install lumen-mcp`.
- [ ] Identity line ASCII < 1400 chars, single line, synced with
      `src/myagent.m` (automated test).
