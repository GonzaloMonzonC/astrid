# 🧬 Astrid

**El agente que se niega a especular.**
**Evidencia, o silencio.**

> 🇬🇧 English version: [README.md](README.md)

Astrid es un agente de referencia nacido dentro del MVM de Poli — identidad,
código y ciclo publicados bajo MIT. Su system prompt no es una biografía: es
la salida en vivo de su propia rutina, `EVIDENCE^ASTRID`, ejecutada en el MVM
real en cada conversación. Responde solo con lo que esa ejecución devuelve.

No es que "normalmente diga la verdad". Está construida para que **cuando no
tiene datos registrados, el diseño lo diga** — y cuando el pipeline de
evidencia falla, el fallo es visible (`evidence: false`), no se oculta.

> La mayoría de los agentes están entrenados para ser útiles. Astrid está
> entrenada para ser verificable. Útil es una promesa. Verificable es un
> diseño.

**Corre sobre [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol)
(MIT)** — protocolo · PDB · M-Light/MVM · Poli+Smith · 115 herramientas MCP,
sin claves de API. El repo del agente es la puerta; el protocolo es la casa.

> Parte de la **tríada A·I·E**: Astrid *(¿es verdad?)* · [Iris](https://github.com/GonzaloMonzonC/iris) *(¿y si…?)* · [Elena](https://github.com/GonzaloMonzonC/elena) *(¿y ahora qué?)* — tres agentes MIT, un protocolo.

## Así se ve su evidencia

Un digest real (26 afirmaciones por ejecución en producción; schema v1):

```
Astrid v0.3.0 | active=1 | mode activo=astrid | evidence=true
claim|mode|^ACTIVE|astrid|1
claim|metric|^ANGI(metrics,agents_online)|{"value": 12, "updated": "..."}|1
claim|route|^AGENTES(routing,astrid)|{"tipo": "poli", "mode": "astrid"}|1
claim|config|^SPACE(ASI)|127.0.0.1:<port>|10
claim|counter|^QUANTUM(colapso)|119|10
claim|note|^VIRTUAL|no existe (la virtualizacion vive en ^MVM)|0
REGLA: responde SOLO con estos datos registrados; ...
```

Cada afirmación cita el global del que se leyó (`source`) y su código de
presencia (`d`). Pregúntale cualquier cosa que no esté en esa ejecución y te
lo dice — no rellena el hueco. Ver
[`docs/EVIDENCE_SCHEMA.es.md`](docs/EVIDENCE_SCHEMA.es.md) para el contrato.

## Por qué existe esto

Los LLM fabrican. Ese es el problema conocido — y la respuesta conocida hasta
ahora ha sido "prompt mejor". Astrid es una respuesta distinta: **convertir la
fuente de verdad en una rutina ejecutable**, no en un párrafo de
instrucciones.

- Su runtime de chat (`poli_server`) lee `^PERSONALITY("astrid","evidence_routine")`
  → `EVIDENCE^ASTRID`, la ejecuta en el MVM y antepone la salida real a su
  system prompt como **EVIDENCIA REGISTRADA**.
- Su digest es un escaneo de solo lectura del estado vivo: modos, métricas,
  routing, espacios, registro del MVM, libro de contabilidad de los
  experimentos cuánticos — lo que exista en la máquina sobre lo que se le
  pregunte.
- Sus reglas (de su identidad registrada):

  1. Operar solo sobre datos registrados.
  2. Nunca especular: sin datos → decirlo, y hacer la pregunta exacta.
  3. Formato del hallazgo: observación → implicación → pregunta.
  4. Preguntar una sola vez, con claridad (regla de oro).
  5. Auditar la PDB, supervisar el MVM, detectar la incoherencia que nadie ve.

## Qué pasa cuando la evidencia falla

Esta es la parte que los demás agentes no documentan. Durante su primer día en
producción, dos bugs distintos rompieron su hook de evidencia (un límite del
parser de M-Light con llamadas `$O`/`$D` anidadas — ambos corregidos). Cada
vez, Astrid **alucinó una respuesta segura de sí misma**, y cada vez la
respuesta llevaba el flag `"evidence": false`. La alucinación no la atrapó un
guardarraíl, sino el propio diseño: *la ausencia de evidencia forma parte de
la respuesta*. Un tercer incidente precedió al hook — el que lo motivó: se
inventó `$DATA(^ANGI)=0` y una historia de `%SYS` mientras ^ANGI estaba viva.
También está documentado (CHANGELOG 0.1.1). Nada se borra.

El registro de incidentes está en [`CHANGELOG.md`](CHANGELOG.md). Léelo: es
la parte más honesta de este repo. Un sistema que puede mostrarte cuándo no
es de fiar es un sistema sobre el que puedes construir.

**La historia con trabajo real**: auditó un libro de contabilidad vivo de
experimentos cuánticos — más de 115 ejecuciones en hardware QPU real — y
encontró el bug de escritura detrás de los contadores, se negó a especular
cuando le pidieron un veredicto que su evidencia no cubría, y confirmó el
arreglo solo contra su propio digest. Relato completo:
[`docs/STORY.es.md`](docs/STORY.es.md).

## El contrato de notaría

El digest emite afirmaciones estructuradas — `claim|<kind>|<source>|<value>|<d>`,
schema v1 (ver [`docs/EVIDENCE_SCHEMA.es.md`](docs/EVIDENCE_SCHEMA.es.md)):
qué se leyó, de qué globales, con qué código de presencia. El siguiente paso
natural — y la razón de que este repo dependa de
[lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol) — es
anclarlo: un digest con dirección de contenido y firmado que convierta a
Astrid en la **notaria de registro de los workflows multi-agente**. Clonar el
agente MIT te da la honestidad; el protocolo te da la capa de reputación
debajo.

## Inicio rápido (local)

**Dependencia**: [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol)
(MIT) — clónalo al mismo nivel que este repo (carpetas hermanas), para que el
harness encuentre el runtime. Astrid es el agente de referencia **encima** de
él; fija un release/commit cuando hagas fork. Referencia para esta versión:
lumen-protocol `main` (2026-09, verificado: la indirección de nombres de AUDIT
necesita el fix de M-Light del commit `243e74c` o posterior).

1. Consigue un runtime M: compila el Rust MVM desde tu clon de lumen-protocol
   (`implementations/rust/lumen-m-light`, `cargo build --release`, la DLL en
   `implementations/mcp-servers/pdb/`), o apunta `LUMEN_MLIGHT_LIB` a un
   `lumen_mlight.dll` existente. *(`pip install lumen-mcp` solo incluye
   bindings de transporte — sin MVM — a partir de 0.1.0.)*
2. Carga la rutina y siémbrala (identidad → `^PERSONALITY("astrid")`, incluido
   el contrato `evidence_routine`):
   ```m
   ; carga src/astrid.m en tu ruta de rutinas M
   D INIT^ASTRID      ; rellena lo que falta, idempotente
   D INIT^ASTRID(1)   ; sobrescribe / reset completo
   ```
3. Verifica y ejecuta el digest registrado — el canario del hook de evidencia:
   ```m
   D VERIFY^VERIFY          ; PASS astrid (identidad, activo, provider/model)
   W $$EVIDENCE^ASTRID()    ; el digest: afirmaciones con fuentes + evidence=true
   ```
   O con el harness (hace el seed + digest por ti, sobre una PDB desechable):
   ```bash
   python harness/astrid_harness.py seed
   python harness/astrid_harness.py evidence
   ```
   La salida esperada empieza con `Astrid v0.3.0 | active=1 | ... | evidence=true`
   seguida de líneas `claim|...` (ver la muestra más arriba).
4. Suite completa contra un MVM real sobre una PDB desechable — sin servicios
   externos, **20 checks** (bucle de inbox de INGEST + registro MCP):
   ```bash
   python tests/run_tests.py
   ```
5. Demo de ingest (fuente externa → PDB → auditado):
   ```bash
   python examples/ingest/ingest_demo.py --db /tmp/ingest.db
   curl -X POST "http://127.0.0.1:8787/hook?origen=github" \
        -H "Content-Type: application/json" -d '{"event": "push", "ref": "main"}'
   curl "http://127.0.0.1:8787/digest"
   ```
   Ver [`docs/INGESTION.es.md`](docs/INGESTION.es.md).

## Roadmap

- [x] Repo público, MIT — publicado el 2026-09-09
- [x] Evidence hook en producción — el chat responde solo desde `EVIDENCE^ASTRID`;
      `evidence:false` visible (incidentes en CHANGELOG)
- [x] Emisor de schema v1 — digest como afirmaciones parseables (listo para verificador)
- [x] Canario de evidencia en la suite de tests (20 checks)
- [x] Harness verificador — `tests/verify_claims.py` (AC-1..AC-4): formato de
      claims, fuentes, kinds conocidos, estabilidad ante estados idénticos
- [x] Anclaje de notaría (0.3.1) — digest firmado con dirección de contenido (cid +
      firma + libro `^EVIDENCE`) vía lumen-protocol; verificador `tests/verify_anchor.py`,
      anclaje runtime en `poli_server._evidence_block`
- [ ] Cableado completo de inbox standalone (bucle de agente nativo del MVM)

## Agentes hermanos

- **Echo** — el agente derivado generado por `template/render.py`
  (`examples/echo`), usado como regresión del template en la suite.
- [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol) — el
  metal bajo Astrid: protocolo MIT, PDB, M-Light/MVM, Poli+Smith, 115
  herramientas MCP. Construye uno como el suyo y publícalo en abierto — mismo
  esqueleto, tu identidad.

## Estructura

```
astrid/
├── LICENSE              MIT
├── README.md            Este fichero (EN)
├── README.es.md         Español — mismo contenido (ES)
├── SECURITY.md          Sin secretos, disciplina de PDB, cómo reportar (EN)
├── CONTRIBUTING.md      Convenciones + proceso (EN)
├── CHANGELOG.md         Keep a Changelog / semver (EN) — incl. los incidentes de fallo de evidencia
├── src/
│   └── astrid.m         Rutina M: ASTRID (estado) · INIT (seed reproducible) ·
│                        AUDIT · COUNT · EVIDENCE (digest registrado, schema v1)
├── personalities/
│   └── astrid.md        Identidad completa legible (ES) — acentos, voz, campos
├── harness/
│   └── astrid_harness.py  Runner de status/seed/evidence/verify/audit
├── template/            Deriva un nuevo agente: render.py + AGENT.*.tpl
├── examples/echo        Agente derivado generado por el template (regresión)
├── examples/ingest      Demo webhook: fuente externa → PDB → claims de inbox en el digest
├── docs/
│   ├── DESIGN.md        EN — ficha de identidad, contrato de agente, ciclo, checklist de publicación
│   ├── DESIGN.es.md     ES — diseño, contrato de agente, ciclo
│   ├── STORY.md         EN — la historia de lanzamiento: evidence hook, auditoría real, incidentes
│   ├── STORY.es.md      ES — la historia de lanzamiento
│   ├── EVIDENCE_SCHEMA.md       EN — digest schema v1 + contrato de notaría
│   ├── EVIDENCE_SCHEMA.es.md    ES — esquema del digest + contrato de notaría
│   ├── INGESTION.md     EN — fuentes externas → PDB → auditadas por Astrid (demo)
│   ├── INGESTION.es.md  ES — fuentes externas → PDB → auditadas por Astrid
│   ├── BUILD_YOUR_OWN.md        EN — guía paso a paso para construir un agente derivado
│   └── BUILD_YOUR_OWN.es.md     ES — guía paso a paso para un agente derivado
└── tests/
    ├── run_tests.py     Suite completa, 20 checks, un comando
    ├── verify_claims.py Harness verificador de los claims del digest (AC-1..AC-4)
    └── verify.m         Verificación: la identidad existe, habla, opera
```

**Más lecturas**: [DESIGN.es.md](docs/DESIGN.es.md) (por qué está construida
así) · [STORY.es.md](docs/STORY.es.md) (la historia de lanzamiento con la
auditoría cuántica real) · [INGESTION.es.md](docs/INGESTION.es.md) (fuentes
externas → PDB → auditadas) · [EVIDENCE_SCHEMA.es.md](docs/EVIDENCE_SCHEMA.es.md)
(el contrato de notaría) · [BUILD_YOUR_OWN.es.md](docs/BUILD_YOUR_OWN.es.md)
(construye un agente derivado).

## Política de idiomas

El EN es canónico para el código y los docs raíz (README, CHANGELOG,
SECURITY, CONTRIBUTING). El ES vive como espejo `.es.md` junto al fichero en
inglés. La ficha de personalidad (`personalities/astrid.md`) es ES por diseño
— es la versión legible de la línea de identidad ASCII.

## Licencia

MIT — Copyright (c) 2026 Gonzalo Monzón · Cadences Lab
