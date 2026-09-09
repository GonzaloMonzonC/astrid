# La historia de Astrid

_Evidencia registrada, o silencio._

> 🇬🇧 English version: [STORY.md](STORY.md)

---

## La historia

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
`"evidence": false`. Pasó dos veces en su primer día en producción — bugs del
parser del runtime — y las dos veces el diseño la delató antes que cualquier
guardarraíl. Hubo un tercer incidente anterior al hook: inventó
`$DATA(^ANGI)=0` y lore de `%SYS` con ^ANGI vivo — ese es el motivo por el
que el hook existe (CHANGELOG 0.1.1). Los tres están documentados en el
[CHANGELOG](../CHANGELOG.md), con la corrección. Es la parte más honesta
del repo.

### La prueba con trabajo real

Le pedimos auditar el registro de experimentos cuánticos del ecosistema —
115+ ejecuciones en QPU real (Tuna-9 / Tuna-17), QAOA en hardware, veto con
azar cuántico real:

- **Encontró las ramas derivadas del registro vacías.** Los contadores
  subían (`colapso=115`, `job=145` en el momento de la auditoría,
  2026-09-09 — el registro siguió vivo: 119 al cierre del día) pero las
  estructuras derivadas (`ultimo`, `stats`) nunca se habían poblado. Un bug
  real de escritura que nadie había visto hasta que ella hizo la pregunta
  exacta.
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
[`EVIDENCE_SCHEMA.es.md`](EVIDENCE_SCHEMA.es.md).
