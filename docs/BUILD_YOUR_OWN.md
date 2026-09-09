# Build your own Astrid-class agent (planned — draft)

> This guide turns Astrid into a **template**: step by step, from zero to an
> agent of your own running on LUMEN with open MIT code. Sections marked
> *(pending)* are the remaining harness work before publishing.

## 0. What you need

- [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol) — MIT:
  build the Rust MVM (`implementations/rust/lumen-m-light`,
  `cargo build --release`) and copy the DLL to
  `implementations/mcp-servers/pdb/`. *(`pip install lumen-mcp` 0.1.0 = transport
  bindings only, no MVM — a clone build or `LUMEN_MLIGHT_LIB` is required to
  run routines.)*
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

Seed fields (see `poli-personalities` / `mvm-native-agents`):

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

## 3. Give it a cycle (the cycle is the tutorial)

Astrid runs OBSERVAR → CONTRASTAR → PREGUNTAR → ACTUAR → REGISTRAR → EXPONER.
Each phase produces a **public artifact**. No hidden phases. Pick yours, keep
it small, and document every phase in `docs/DESIGN.md`.

## 4. Verify (before anything else)

`tests/verify.m` checks: identity ≥ 600 chars, is_active, provider/model set.
Run it in a **throwaway PDB** (see `harness/astrid_harness.py status`):
```
python harness/astrid_harness.py status
python harness/astrid_harness.py audit --ns ^MYNS
```

## 5. Connect the faculties (harness) *(pending — being wired)*

Astrid connects to LUMEN's MCP servers (filesystem, web, thinking, PDB —
zero API keys) and to the MVM. The harness in this repo shows the pattern:
M routine executed against a local PDB → output through the personality.
When the router wiring lands (registration in `^AGENTES`/`^MVM(agents)` so
other agents can discover and talk to yours), this section becomes the
step-by-step.

## 6. Publish MIT

Checklist before publishing (see `docs/DESIGN.md`):
- [ ] Zero private lore: no internal URLs, no diaries, no business logic of
      any private ecosystem. The repo must run with only lumen-protocol.
- [ ] LICENSE MIT + README EN/ES + docs/DESIGN.md present.
- [ ] Verify.m passes against a fresh PDB.
- [ ] Harness runs on a clean machine with only `pip install lumen-mcp`.
- [ ] Identity line ASCII < 1400 chars, single line.
