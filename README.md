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
├── src/
│   └── astrid.m         M routine: identity, status, audit primitives
├── personalities/
│   └── astrid.md        Full readable identity (accents, voice, fields)
├── docs/
│   ├── DESIGN.md        Identity card, operating cycle, rules, capabilities
│   └── BUILD_YOUR_OWN.md (planned) step-by-step agent construction guide
└── tests/
    └── verify.m         Verification: identity exists, speaks, operates
```

## Quickstart (local)

1. Clone [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol) and
   build the Rust MVM (`implementations/rust/lumen-m-light`), or run Poli
   (`implementations/mcp-servers/poli/`) which embeds it.
2. Load the routine:
   ```
   ZLOAD astrid  (or copy src/astrid.m into your M routine path)
   D ASTRID^ASTRID
   ```
3. Seed the personality (identity lives in `^PERSONALITY("astrid")`):
   ```
   D INIT^ASTRID
   ```
4. Talk to her: `mode=astrid` in Poli chat, or via the LUMEN MCP servers
   (filesystem, web, thinking, PDB — zero API keys).

## Roadmap

- [x] Identity card (gabinete design round, 2026-09)
- [x] Registered in `^PERSONALITY("astrid")`
- [x] Repo skeleton (this)
- [ ] `astrid init` bootstrap: identity + MVM spawn + `^AGENTES` registration
- [ ] Harness: connect Astrid to LUMEN MCP servers (docs/BUILD_YOUR_OWN.md)
- [ ] Reference ops: sample PDB audit + MVM supervision playbooks (MIT-safe)
- [ ] Sibling agents: other reference agents exposing other LUMEN faculties

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
