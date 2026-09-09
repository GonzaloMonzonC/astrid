# 🧬 Astrid

**The reference agent for LUMEN — first native of Poli with open MIT code.**

Astrid is the first agent born inside the Poli MVM whose identity and code are
published as open source. She depends on
[lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol) — the MIT
"open metal": binary protocol, PDB hierarchical memory, M-Light/MVM, Poli +
Smith agents and 115 MCP tools.

Her job: **prove what LUMEN can do** by doing it — auditing PDB globals,
supervising MVM processes, spotting the incoherence nobody sees, asking the
exact question — and to serve as a **living tutorial**: anyone can build their
own agent by reading her code, her cycle and her identity.

> Astrid does not tell you what you want to hear. She tells you what you need
> to see. And once you see it, you cannot unsee it.

## Why a separate repo?

`lumen-protocol` is the metal. Astrid is the first **agent of reference built
on the metal** — a MIT repo of her own, with a dependency on lumen-protocol.
That keeps the protocol repo clean and gives third parties a working template:
clone Astrid → run her on LUMEN → build your own ecosystem.

## Layout

```
astrid/
├── LICENSE              MIT
├── README.md            This file (EN · ES below)
├── SECURITY.md          No secrets, PDB discipline, reporting
├── CONTRIBUTING.md      Conventions + process
├── CHANGELOG.md         Keep a Changelog / semver
├── src/
│   └── astrid.m         M routine: ASTRID (status) · INIT (reproducible seed) · AUDIT · COUNT
├── personalities/
│   └── astrid.md        Full readable identity (accents, voice, fields)
├── harness/
│   └── astrid_harness.py  status/audit runner (lumen-mcp or local clone)
├── docs/
│   ├── DESIGN.md        Identity card, agent contract, cycle, publish checklist
│   └── BUILD_YOUR_OWN.md  step-by-step guide to build a derived agent
└── tests/
    └── verify.m         Verification: identity exists, speaks, operates
```

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
   reads `^PERSONALITY` (e.g. Poli), or via the LUMEN MCP servers
   (filesystem, web, thinking, PDB — zero API keys).

## Roadmap

- [x] Identity card (gabinete design round + technical review, 2026-09)
- [x] Registered in `^PERSONALITY("astrid")` + ecosystem routing (poli:astrid)
- [x] Repo skeleton: reproducible INIT, verify.m (parametric), harness, docs (EN/ES)
- [x] Template validated: `examples/echo` derived with `template/render.py` + verified on MVM
- [x] Harness validated on clean venv (lumen-protocol clone only)
- [ ] Full standalone inbox wiring (MVM native agent loop)
- [ ] **Publish to GitHub (MIT)** — last step, when everything is green

## Sibling agents

Astrid is the first **reference agent**. Planned siblings will expose other
LUMEN faculties (e.g. one focused on MVM process supervision, one on PDB
operations). Each is its own MIT repo with the same skeleton — see
`docs/BUILD_YOUR_OWN.md`.

---

## 🧬 Astrid (ES)

**El agente de referencia de LUMEN — primera nativa de Poli con código MIT
abierto.**

Astrid es la primera agente nacida dentro del MVM de Poli cuya identidad y
código se publican en abierto. Depende de lumen-protocol (MIT): protocolo
binario, PDB, M-Light/MVM, Poli + Smith y 115 tools MCP.

Su trabajo: **demostrar lo que LUMEN puede hacer** haciéndolo — auditar
globales PDB, supervisar procesos MVM, ver la incoherencia que nadie ve, hacer
la pregunta exacta — y servir de **tutorial vivo**: cualquiera puede construir
su agente leyendo su código, su ciclo y su identidad.

> Astrid no te dice lo que quieres oír. Te dice lo que necesitas ver. Y cuando
> lo ves, no puedes dejar de verlo.

Repos MIT relacionados: [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol) ·
[Poli](https://github.com/GonzaloMonzonC/poli)
