# La historia de Astrid — The Astrid Story

_Evidencia registrada, o silencio. / Registered evidence, or silence._

---

## La idea (EN)

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

## La historia (ES)

La mayoría de agentes están entrenados para ser útiles. Astrid está diseñada
para ser verificable.

Astrid es un agente M de referencia — licencia MIT, nacido dentro del MVM de
Poli, el runtime MUMPS de lumen-protocol. Su diferencia no es la
personalidad: es la arquitectura de su verdad.

**Su system prompt no es una biografía.** En cada conversación, el runtime
ejecuta su propia rutina `EVIDENCE^ASTRID` en la máquina real y antepone la
salida — un digest read-only de globales: métricas, routing, procesos,
experimentos. Responde solo con eso. Evidencia registrada, o silencio.

**Cuando el pipeline falla, se nota.** La respuesta viaja con
`"evidence": false`. Pasó dos veces en sus primeras semanas — bugs del parser
del runtime — y las dos veces el diseño la delató antes que cualquier
guardarraíl. Los dos incidentes están documentados en el CHANGELOG, con el
fix. Es la parte más honesta del repo.

### La prueba con trabajo real

Le pedimos auditar el registro de experimentos cuánticos del ecosistema —
115+ ejecuciones en QPU real (Tuna-9 / Tuna-17), QAOA en hardware, veto con
azar cuántico real:

- **Encontró las ramas derivadas del registro vacías.** Los contadores
  subían (`colapso=115`, `job=145`) pero las estructuras derivadas
  (`ultimo`, `stats`) nunca se habían poblado. Un bug real de escritura que
  nadie había visto hasta que ella hizo la pregunta exacta.
- **Señaló una incoherencia de conteos que nadie había visto** (12 agentes
  online frente a 6/4/7 en registros distintos).
- **Se negó a especular.** Ante un veredicto sobre datos que no estaban en su
  evidencia registrada, respondió: *"datos insuficientes — no registrados en
  mi runtime — confirmación requerida."* La pregunta exacta, no la respuesta
  inventada.

Cuando las ramas derivadas se poblaron desde la auditoría real, confirmó el
resultado contra su propia evidencia — e inmediatamente señaló la siguiente
discrepancia real (una nota estática frente a un contador vivo que ya se
había movido). El ciclo se cierra: observar → contrastar → preguntar →
registrar → exponer.

### Qué significa

Debajo de Astrid está lumen-protocol (MIT): el MVM, la PDB jerárquica,
M-Light — 115 tools MCP, sin API keys. El repo del agente es la puerta; el
protocolo es la casa.

Próximo paso: anclar su digest — con dirección de contenido y firma —
convirtiendo a Astrid en la notaria de registro de workflows multi-agente.
El MIT da la honestidad; el protocolo da la capa de reputación debajo. Ver
[`EVIDENCE_SCHEMA.md`](EVIDENCE_SCHEMA.md).
