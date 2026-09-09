# Astrid — DESIGN

## Resumen

Astrid es el **agente de referencia** de lumen-protocol: un repo MIT separado
que depende del metal (lumen-protocol) y demuestra sus facultades en
operación real. Es la primera nativa de Poli (vive en el MVM como roberto y
javier) cuyo código y personalidad se publican en abierto.

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

Regla MIT: en este repo **nunca** entra lore privado del ecosistema (rutas
internas, agentes internos con criterio de negocio, claves, diarios). Lo que
se publique aquí debe poder ejecutarlo cualquiera con solo lumen-protocol.

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

## Notas de diseño (ronda gabinete, 2026-09-09)

- **Roberto** (estructura): ciclo de 6 fases; 5 reglas + operar solo sobre
  datos registrados. Identidad funcional ~646 chars ASCII.
- **Javier** (relaciones): Astrid es la hermana mayor, no la madre; hace code
  review de personalidad a agentes nuevos; empatía estructurada; formato de
  hallazgo observación → implicación → pregunta; regla de oro: pregunta una
  sola vez, con claridad.
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
2. ~~Registro ^PERSONALITY~~ ✅  (identity_len=646, active=1)
3. ~~Esqueleto repo~~ ✅  (INIT reproducible + verify.m + harness, verificado en MVM local)
4. ~~Revisión técnica (roberto/pamies, smith_5)~~ ✅ — checklist MIT-clean en este doc
5. `astrid init` — bootstrap: identity + spawn MVM + registro ^AGENTES (ya registrada en runtime Cadences; pendiente versión standalone)
6. Harness LUMEN fino + docs/BUILD_YOUR_OWN.md ✅ (validado en venv limpio 2026-09)
7. ~~`template/` + agente derivado~~ ✅ — `examples/echo` generado con template/render.py y verificado (INIT + VERIFY PASS)
8. Publicar GitHub (MIT) — SOLO cuando el checklist de publicación esté verde

## Checklist de publicación (MIT-clean)

- [ ] `git grep -iE "api[_-]?key|token|secret|password|BEGIN .*PRIVATE" HEAD $(git rev-list --all)` → vacío
- [ ] Sin rutas absolutas de la máquina de origen en src/docs/tests
- [ ] Sin lore privado (URLs internas, agentes internos, diarios, lógica de negocio)
- [ ] verify.m pasa en PDB desechable desde entorno limpio (sin servicios externos)
- [ ] Harness corre en venv limpio con solo clone lumen-protocol (validado 2026-09: status+audit OK)
- [ ] README EN/ES + LICENSE + SECURITY + CONTRIBUTING + CHANGELOG presentes
- [ ] Dependencia lumen-protocol declarada (MIT) + versión/commit de referencia
- [ ] Identity ASCII ≤1400 chars sincronizada entre src/astrid.m y personalities/astrid.md
