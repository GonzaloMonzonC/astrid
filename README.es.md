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

Esta es la parte que los demás agentes no documentan. Durante sus primeros
días en producción, dos bugs distintos rompieron su hook de evidencia (un
límite del parser de M-Light con llamadas `$O`/`$D` anidadas — ambos
corregidos). Cada vez, Astrid **alucinó una respuesta segura de sí misma**, y
cada vez la respuesta llevaba el flag `"evidence": false`. La alucinación no
la atrapó un guardarraíl, sino el propio diseño: *la ausencia de evidencia
forma parte de la respuesta*.

El registro de incidentes está en [`CHANGELOG.md`](CHANGELOG.md). Léelo: es
la parte más honesta de este repo. Un sistema que puede mostrarte cuándo no
es de fiar es un sistema sobre el que puedes construir.

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
│   └── astrid_harness.py  Runner de status/audit (lumen-mcp o clon local)
├── docs/
│   ├── DESIGN.md        EN — ficha de identidad, contrato de agente, ciclo, checklist de publicación
│   ├── DESIGN.es.md     ES — diseño, contrato de agente, ciclo
│   ├── STORY.md         EN — la historia de lanzamiento: evidence hook, auditoría real, incidentes
│   ├── STORY.es.md      ES — la historia de lanzamiento
│   ├── EVIDENCE_SCHEMA.md       EN — digest schema v1 + contrato de notaría
│   ├── EVIDENCE_SCHEMA.es.md    ES — esquema del digest + contrato de notaría
│   ├── BUILD_YOUR_OWN.md        EN — guía paso a paso para construir un agente derivado
│   └── BUILD_YOUR_OWN.es.md     ES — guía paso a paso para un agente derivado
└── tests/
    └── verify.m         Verificación: la identidad existe, habla, opera
```

Política de idiomas: el EN es canónico para el código y los docs raíz
(README.md, CHANGELOG, SECURITY, CONTRIBUTING). El ES vive como espejo
`.es.md` junto al fichero en inglés. La ficha de personalidad
(`personalities/astrid.md`) es ES por diseño — es la versión legible de la
línea de identidad ASCII.

## Inicio rápido (local)

**Dependencia**: [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol)
(MIT) — protocolo, PDB, M-Light/MVM, Poli+Smith, 115 herramientas MCP. Astrid
es el agente de referencia **encima** de él; fija un release/commit cuando
hagas fork. Referencia para esta versión: lumen-protocol `main` (2026-09).

1. Consigue un runtime M: compila el Rust MVM desde un clon de lumen-protocol
   (`implementations/rust/lumen-m-light`, `cargo build --release`, la DLL en
   `implementations/mcp-servers/pdb/`), o apunta `LUMEN_MLIGHT_LIB` a un
   `lumen_mlight.dll` existente. *(`pip install lumen-mcp` solo incluye
   bindings de transporte — sin MVM — a partir de 0.1.0.)*
2. Carga la rutina y siémbrala (identidad → `^PERSONALITY("astrid")`):
   ```m
   ; carga src/astrid.m en tu ruta de rutinas M
   D INIT^ASTRID      ; rellena lo que falta, idempotente
   D ASTRID^ASTRID    ; estado
   W $$EVIDENCE^ASTRID()  ; el digest registrado — léelo, luego háblale
   ```
3. Verifica (PDB desechable, sin servicios externos) — **suite completa, un
   solo comando**:
   ```bash
   python tests/run_tests.py    # 12 checks: INIT/status/VERIFY/AUDIT + identidad
                                # regresiones sync + template + echo → todo verde
   ```
   o los checks M individuales:
   ```m
   D VERIFY^VERIFY    ; → PASS astrid verificado
   ```
   o mediante el harness (status / auditoría demo contra cualquier PDB local):
   ```bash
   python harness/astrid_harness.py status
   python harness/astrid_harness.py audit --ns ^MYNS
   ```
4. Háblale: el modo de personalidad `astrid` en cualquier runtime de chat
   LUMEN que lea `^PERSONALITY` + el contrato `evidence_routine` (p. ej.
   Poli), o mediante los MCP servers de LUMEN (filesystem, web, thinking, PDB
   — cero API keys).

## Roadmap

- [x] Ficha de identidad (ronda de diseño de gabinete + revisión técnica, 2026-09)
- [x] Registrada en `^PERSONALITY("astrid")` + routing del ecosistema (poli:astrid)
- [x] Esqueleto del repo: INIT reproducible, verify.m (paramétrico), harness, docs (EN/ES)
- [x] Template validado: `examples/echo` derivado con `template/render.py` + verificado en el MVM
- [x] Harness validado en venv limpio (solo el clon de lumen-protocol)
- [x] **Publicado en GitHub (MIT)** — público, main
- [x] Evidence hook en producción: el chat responde desde el output de `EVIDENCE^ASTRID`;
      `evidence:false` es visible cuando el pipeline falla (incidentes en CHANGELOG)
- [ ] Inbox standalone completo (bucle de agente nativo del MVM)
- [ ] Digest firmado y con dirección de contenido, anclado vía lumen-protocol (contrato de notaría)

## Agentes hermanos

Astrid es el primer **agente de referencia**. Los hermanos planeados
expondrán otras facultades de LUMEN (p. ej., uno centrado en la supervisión
de procesos del MVM, otro en operaciones de PDB). Cada uno es su propio repo
MIT con el mismo esqueleto — ver `docs/BUILD_YOUR_OWN.md`.

---

Repos MIT relacionados: [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol) · [Poli](https://github.com/GonzaloMonzonC/poli)
