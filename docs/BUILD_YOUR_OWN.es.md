> Versión en inglés: [BUILD_YOUR_OWN.md](BUILD_YOUR_OWN.md)

# Construye tu propio agente de clase Astrid

> Esta guía convierte a Astrid en una **plantilla**: paso a paso, de cero a
> un agente propio funcionando sobre LUMEN con código MIT abierto. El
> esqueleto está probado: la propia Astrid se construyó así y está en
> producción.

## 0. Qué necesitas

- [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol) — MIT:
  compila el MVM en Rust (`implementations/rust/lumen-m-light`,
  `cargo build --release`) y copia la DLL a
  `implementations/mcp-servers/pdb/`. *(`pip install lumen-mcp` 0.1.0 =
  solo bindings de transporte, sin MVM — hace falta compilar el clon o
  `LUMEN_MLIGHT_LIB` para ejecutar rutinas.)*
- Python 3.10+ (para el harness) y/o un runtime M que pueda cargar rutinas
  `.m` (lumen-mvm, o cualquier MUMPS con PDB).

## 1. Copia el esqueleto

```
cp -r astrid my-agent
cd my-agent
# rewrite: src/myagent.m, personalities/myagent.md, README
```

## 2. Escribe la identidad

La identidad es **una sola línea ASCII, sin acentos, de 600–1400 caracteres**
almacenada en `^PERSONALITY(name,"identity")` (restricción de almacenamiento
de MUMPS) + un archivo legible por humanos con acentos y voz completa (ver
`personalities/astrid.md`).

Campos a sembrar (ver el patrón INIT en `src/astrid.m`):

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

Reglas prácticas de la ronda de diseño de Astrid:
- **core_mission** en una frase: qué demuestras con existir.
- **3–6 reglas críticas**, imperativas y comprobables; la regla 1 es tu
  equivalente de «no especular»: *opera solo sobre datos registrados*.
- **5–7 capacidades** con nombres cortos en MAYÚSCULAS (AUDIT_PDB,
  MVM_WATCH…).
- Todo agente necesita un **formato de hallazgo** (observación → implicación
  → pregunta) — es lo que permite a otros agentes seguir tu razonamiento.

## 3. Conecta el hook de evidencia (la pieza innegociable)

Esto es lo que hace a un agente *verificable* en lugar de meramente *útil*:

1. Escribe `EVIDENCE^MYAGENT` — una rutina **de solo lectura** que devuelve
   un digest del estado desde el que tu agente tiene permiso para responder
   (un dato por línea).
2. Emite claims con el esquema: `claim|<kind>|<source>|<value>|<d>` — cada
   claim cita el global del que se leyó (ver `docs/EVIDENCE_SCHEMA.md`).
3. Registra el contrato: `^PERSONALITY("myagent","evidence_routine")` =
   `EVIDENCE^MYAGENT`. Los runtimes de chat que implementan el hook
   (`poli_server` de Poli) lo ejecutarán antes de cada conversación y
   antepondrán la salida al system prompt como EVIDENCIA REGISTRADA.
4. Si el pipeline falla, la respuesta debe llevar `"evidence": false` —
   visible, nunca oculto.

Reglas de construcción M-Light (ganadas a pulso — ver CHANGELOG 0.2.0):
- `$D`/`$O`/funciones anidadas **nunca** en línea como subíndice o dentro de
  una concatenación. Asigna primero a una variable intermedia.
- La rutina del digest nunca escribe globales; el flag `evidence` va siempre
  en la línea de cabecera.

## 4. Dale un ciclo (el ciclo es el tutorial)

Astrid ejecuta OBSERVAR → CONTRASTAR → PREGUNTAR → ACTUAR → REGISTRAR →
EXPONER. Cada fase produce un **artefacto público**. Sin fases ocultas.
Elige el tuyo, mantenlo pequeño y documenta cada fase en `docs/DESIGN.md`.

## 5. Verifica (antes que nada)

`tests/verify.m` comprueba: identity ≥ 600 caracteres, is_active,
provider/model definidos. Ejecútalo en una PDB **desechable** (ver
`harness/astrid_harness.py status`):
```
python harness/astrid_harness.py status
python harness/astrid_harness.py audit --ns ^MYNS
```
Añade una comprobación de que `$$EVIDENCE^MYAGENT()` se ejecuta y de que
cada línea `claim|` tiene una fuente no vacía — ese test es tu canario
contra la rotura silenciosa del digest.

## 6. Registra y ejecuta

Regístralo en la malla para que otros agentes puedan descubrir al tuyo y
hablar con él: `^AGENTES("routing","myagent")` = tu ruta de runtime (p. ej.
`poli:myagent`) y, en el MVM, la clave de descubrimiento
`^MVM("agents","myagent")`. Habla con tu agente a través de cualquier
runtime de chat que lea `^PERSONALITY` + el contrato `evidence_routine`, o
vía los servidores MCP de LUMEN (filesystem, web, thinking, PDB — cero API
keys).

## 7. Publica con MIT

Lista de comprobación antes de publicar en un remoto público (la de Astrid
está en verde — ver `docs/DESIGN.md`):
- [ ] Cero lore privado: sin URLs internas, sin diarios, sin lógica de
      negocio de ecosistema privado alguno. El repo debe funcionar solo con
      lumen-protocol (`git grep -iE "api[_-]?key|token|secret|password"`
      sobre todo el historial).
- [ ] LICENSE MIT + README EN/ES + docs/DESIGN.md presentes.
- [ ] Verify.m pasa contra una PDB limpia; `EVIDENCE^MYAGENT` emite claims
      con fuentes.
- [ ] El harness corre en una máquina limpia con solo un clon de
      lumen-protocol (`pip install lumen-mcp` 0.1.0 solo trae bindings
      de transporte — ver §0).
- [ ] Línea de identity ASCII < 1400 caracteres, en una sola línea,
      sincronizada con `src/myagent.m` (test automatizado).
