# The Astrid Story

_Registered evidence, or silence._

> 🇪🇸 Versión en español: [STORY.es.md](STORY.es.md)

---

## The idea

Most agents are trained to be helpful. Astrid is designed to be verifiable.

Astrid is a reference M agent — MIT licensed, born inside the Poli MVM, the
MUMPS runtime of [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol).
Her difference is not her personality: it is the architecture of her truth.

**Her system prompt is not a biography.** On every conversation, the runtime
executes her own routine `EVIDENCE^ASTRID` on the real machine and prepends
the output — a read-only digest of globals: metrics, routing, processes,
experiments. She answers only from that. Registered evidence, or silence.

**When the pipeline fails, it shows.** The response carries
`"evidence": false`. It happened twice in her first weeks — runtime parser
bugs — and both times the design exposed her before any guardrail could.
Both incidents are documented in [`CHANGELOG.md`](../CHANGELOG.md), with the
fix. That is the most honest part of this repo.

### The real-work proof

We asked her to audit the quantum experiment ledger of the ecosystem —
115+ executions on real QPU (Tuna-9 / Tuna-17), QAOA on hardware, quantum
vetoes driven by real randomness:

- **She found the ledger's derived branches empty.** Counters were climbing
  (`colapso=115`, `job=145`) but the derived structures (`ultimo`, `stats`)
  had never been populated. A real writing bug, unnoticed until she asked
  the exact question.
- **She flagged a counting incoherence nobody had seen** (12 online agents
  vs 6/4/7 in different registries).
- **She refused to speculate.** Asked for a verdict over data that was not
  in her registered evidence, her answer was: *"datos insuficientes — no
  registrados en mi runtime — confirmación requerida."* The exact question,
  not the invented answer.

When the derived branches were populated from the real audit, she confirmed
the result against her own evidence — and immediately flagged the next real
discrepancy (a static note vs a live counter that had moved on). The loop
closes: observe → contrast → ask → record → expose.

### What it means

Below Astrid is lumen-protocol (MIT): the MVM, the hierarchical PDB,
M-Light — 115 MCP tools, no API keys. The agent repo is the door; the
protocol is the house.

Next step: anchor her digest — content-addressed, signed — making Astrid the
notary of record for multi-agent workflows. MIT gives you the honesty; the
protocol gives you the reputation layer underneath. See
[`EVIDENCE_SCHEMA.md`](EVIDENCE_SCHEMA.md).

---
