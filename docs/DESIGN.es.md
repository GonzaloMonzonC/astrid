# Astrid — DESIGN

> 🇬🇧 English version: [DESIGN.md](DESIGN.md)

## Resumen

Astrid es el **agente de referencia** de lumen-protocol: un repo MIT separado
que depende del metal (lumen-protocol) y demuestra sus facultades en
operación real. Es la primera nativa de Poli cuyo código y personalidad se
publican en abierto.

Capas:

```
┌─────────────────────────────────────────────┐
│  astrid (MIT)  — agente de referencia       │  este repo
│  código M + identidad + docs + tutorial     │
├─────────────────────────────────────────────┤
│  lumen-protocol (MIT) — open metal          │
│  protocolo · PDB · M-Light/MVM · Poli+Smith │
│  · 115 tools MCP                            │
├─────────────────────────────────────────────┤
│  ECOS (propietario) · Cadences Lab (privado)│
└─────────────────────────────────────────────┘
```

Regla MIT (acotada, 2026-09-09): en este repo **nunca** entran claves, rutas
internas, lógica de negocio ni diarios de lore privado. Las menciones
nominales en la historia (agentes, hardware QPU, el runtime de origen) son
narrativa verificable y no impiden la ejecución — lo publicado debe poder
ejecutarlo cualquiera con solo lumen-protocol.

## Ciclo operativo (el ciclo es el tutorial)

| Fase | Entrada | Salida |
|---|---|---|
| OBSERVAR | estado de PDB, ^GLOBALES, procesos MVM | señales y variaciones |
| CONTRASTAR | señales vs rutinas y modelos registrados | patrones, incoherencias, sospechas |
| PREGUNTAR | sospecha sin certeza | pregunta exacta al responsable u operador |
| ACTUAR | certeza + mandato | orquestación o corrección bajo protocolo |
| REGISTRAR | toda acción y hallazgo | trazo visible en PDB y repo |
| EXPONER | trazo del caso | documentación tutorial MIT |

Sin fases ocultas: cada fase produce artefactos públicos. Cualquiera puede
leer, ejecutar y replicar el ciclo.

## Contrato de evidencia (en producción)

El chat de Astrid no confía en el LLM para recordar quién es: confía en una
rutina. `^PERSONALITY("astrid","evidence_routine")` = `EVIDENCE^ASTRID`;
`poli_server` la ejecuta en el MVM real en cada conversación y antepone su
salida (digest read-only del estado registrado) al system prompt como
EVIDENCIA REGISTRADA. Sin esa salida, la respuesta viaja con
`"evidence": false` — visible, no oculto. Dos incidentes de hook roto
(parser M-Light: `$O`/`$D` anidados en línea) están documentados en el
CHANGELOG: Astrid alucinó y el flag la delató. La transparencia del fallo es
parte del diseño. Pitfall M-Light (verificado): nunca funciones M anidadas
como subíndice o en concatenación — usar variable intermedia.

## Contrato de notaría (schema v1 emitido; anclaje en roadmap)

El digest ya emite claims estructuradas (`claim|kind|source|value|d`) desde
2026-09-09 — ver `docs/EVIDENCE_SCHEMA.md`. La afirmación estructurada (qué
se leyó, de qué globales, con qué $D) es el cimiento. Pendiente: verifier
harness (formato + existencia de fuentes + estabilidad) y el anclaje con
dirección de contenido y firma vía lumen-protocol. Posicionamiento: Astrid
como notaria de registro para workflows multi-agente; el agente MIT da la
honestidad, lumen-protocol la capa de reputación.

## Notas de diseño (ronda gabinete, 2026-09-09)

- **Roberto** (estructura): ciclo de 6 fases; 5 reglas + operar solo sobre
  datos registrados. Identidad funcional ~646 chars ASCII.
- **Javier** (relaciones): Astrid es la hermana mayor, no la madre; hace code
  review de personalidad a agentes nuevos; empatía estructurada; formato de
  hallazgo observación → implicación → pregunta; regla de oro: pregunta una
  sola vez, con claridad.
- **Decisión 2026-09-09 (revisión del equipo)**: el descriptor clínico
  "autismo-coded" se eliminó del identity público (etiqueta de
  neurodivergencia usada como adorno en un repo MIT abierto). La voz
  observable ya está descrita en "Voz" (literal, formato de hallazgo,
  empatía estructurada). Queda registrada aquí como nota interna.
- **Pendiente**: faceta de implementación a revisar con Porto (harness,
  esqueleto fino del repo, provider/model definitivo).

## Registro en Poli

La identidad se siembra en el MVM de Poli desde la **fuente reproducible**
(`src/astrid.m` — INIT siembra la entrada canónica exacta):

```m
D INIT^ASTRID        ; fill-missing (idempotente)
D INIT^ASTRID(1)     ; overwrite / reset completo
```

Verificación: `tests/verify.m` (`D VERIFY^VERIFY` → PASS) contra un PDB
desechable. En el runtime de Cadences Lab quedó registrada vía
`^PERSONALITY("astrid")` + `^AGENTES("routing","astrid")` = `poli:astrid` +
descubrimiento `^MVM("agents","astrid")`; chat verificado por modo de
personalidad y por routing del ecosistema.

## Interfaz del agente con lumen (contrato)

| Entry point | Entrada | Salida | Uso |
|---|---|---|---|
| `ASTRID^ASTRID` | — (lee `^PERSONALITY("astrid",*)`) | estado: versión, active, identity_len, counts, provider/model | health check |
| `INIT^ASTRID` / `INIT^ASTRID(1)` | opcional force=1 | siembra `^PERSONALITY("astrid")` | registro reproducible |
| `VERIFY^VERIFY` | — | PASS/FAIL (identity ≥600, active, provider/model) | test |
| `EVIDENCE^ASTRID` | devuelve digest de estado registrado | evidencia para el chat (hook `evidence_routine`) | |
| `AUDIT^ASTRID` | `^ASTRID("audit_ns")` o default `^ANGI` | observación → implicación → pregunta | demo de auditoría (solo lectura) |
| `$$COUNT^ASTRID(ns)` | nombre de lista (capabilities, critical_rules…) | número de subnodos | helper |

Facultades lumen por capa (revisión técnica 2026-09): **mínimo viable** =
MVM directo (núcleo M + PDB del operador); **producción** = servidores MCP
por perfil auditor con este orden de prioridad: PDB (memoria/evidencia) →
thinking (razonamiento largo) → filesystem/web (insumos externos,
restringidos). `pip lumen-mcp` solo cuando un orquestador externo deba
invocarla.

## Modelo y temperatura

- Chat/operación: `deepseek-v4-flash`, temp 0.3 (verificado).
- Auditorías largas: mismo provider con **variante de mayor contexto**
  configurable vía `^PERSONALITY("astrid","model")` o env por despliegue;
  temp 0.2 si exige comparaciones numéricas literales. Nunca hardcodear la
  decisión en código.

## Roadmap

1. ~~Tarjeta de identidad (ronda gabinete)~~ ✅
2. ~~Registro ^PERSONALITY~~ ✅  (identity_len=631 tras la revisión 2026-09-09, active=1)
3. ~~Esqueleto repo~~ ✅  (INIT reproducible + verify.m + harness, verificado en MVM local)
4. ~~Revisión técnica (roberto/pamies, smith_5)~~ ✅ — checklist MIT-clean en este doc
5. `astrid init` — bootstrap: identity + spawn MVM + registro ^AGENTES (ya registrada en runtime Cadences; pendiente versión standalone)
6. Harness LUMEN fino + docs/BUILD_YOUR_OWN.md ✅ (validado en venv limpio 2026-09)
7. ~~`template/` + agente derivado~~ ✅ — `examples/echo` generado con template/render.py y verificado (INIT + VERIFY PASS)
8. ~~Publicar GitHub (MIT)~~ ✅ — público en main (2026-09-09), checklist MIT-clean verde
9. ~~Evidence hook en producción~~ ✅ — chat responde solo de `EVIDENCE^ASTRID`; `evidence:false` visible (incidentes en CHANGELOG)
10. ~~README reposicionado~~ ✅ — "Evidence, or silence": agente que se niega a especular; docs STORY + EVIDENCE_SCHEMA
11. ~~Schema v1 emisor~~ ✅ — digest con claims `claim|kind|source|value|d` verificado en runtime
12. ~~Verifier harness~~ ✅ — tests/verify_claims.py (AC-1..AC-4): formato de claims, existencia de fuentes, kinds conocidos, estabilidad; integrado en la suite como canario
13. Anclaje notaría — cid + firma + ledger `^EVIDENCE` vía lumen-protocol (pendiente, ver EVIDENCE_SCHEMA.md §3)

## Checklist de publicación (MIT-clean)

- [x] `git grep` secretos historia completa → vacío (2026-09-09)
- [x] Sin rutas absolutas de la máquina de origen en src/docs/tests
- [x] Sin lore privado (URLs internas, agentes internos, diarios, lógica de negocio)
- [x] verify.m pasa en PDB desechable desde entorno limpio (sin servicios externos)
- [x] Harness corre en venv limpio con solo clone lumen-protocol (validado 2026-09: status+audit OK)
- [x] Suite completa `python tests/run_tests.py` → 12/12 verde (2026-09-09)
- [x] README EN/ES + LICENSE + SECURITY + CONTRIBUTING + CHANGELOG presentes
- [x] Dependencia lumen-protocol declarada (MIT) + versión/commit de referencia
- [x] Identity ASCII 646 chars sincronizada entre src/astrid.m y personalities/astrid.md (test automatizado)
