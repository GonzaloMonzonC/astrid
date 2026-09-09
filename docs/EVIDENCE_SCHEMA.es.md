# Esquema del digest v1 — el contrato de notaría (diseño)

> Versión en inglés: [EVIDENCE_SCHEMA.md](EVIDENCE_SCHEMA.md)

_Cómo la evidencia registrada de Astrid se convierte en un claim legible por máquina._

Status: **emisor en producción (2026-09-09, verificado en el MVM real)**.
`EVIDENCE^ASTRID` emite claims `claim|<kind>|<source>|<value>|<d>`
parseables (15 + k, k = entradas de ^SPACE; 18 en producción). El digest es canario de la suite (16 checks). Pendiente: verifier harness (AC-2..AC-4)
y el anclaje (sección 3).

---

## 1. Qué existe hoy (producción, verificado)

`EVIDENCE^ASTRID` es una rutina M de solo lectura. En cada turno de chat, el
runtime (`poli_server`) resuelve `^PERSONALITY("astrid","evidence_routine")`,
ejecuta la rutina en el MVM real y antepone su stdout al prompt de sistema
como **EVIDENCIA REGISTRADA**. Si la ejecución falla o queda vacía, la
respuesta lleva `"evidence": false` — visible por contrato, nunca oculto.

Forma actual del digest — schema v1, un claim por línea (truncado para
legibilidad; 19 claims por digest en producción):

```
Astrid v0.2.0 | active=1 | mode activo=astrid | evidence=true
claim|mode|^ACTIVE|astrid|1
claim|counter|^ANGI(level1)|1|10
claim|metric|^ANGI(metrics,agents_online)|{"value": 12, "updated": "2026-09-09T18:25:23Z"}|1
claim|route|^AGENTES(routing,astrid)|{"tipo": "poli", "mode": "astrid"}|1
claim|config|^SPACE(ASI)|127.0.0.1 :9102|10
claim|counter|^QUANTUM(colapso)|119|10
claim|entry|^QUANTUM(colapso,ultimo)|idx=119 raw={"idx": 119, "ts": "...", "backend": "Tuna-17"}|1
claim|note|^VIRTUAL|no existe (la virtualizacion vive en ^MVM)|0
REGLA: responde SOLO con estos datos registrados; ...
```

Cada línea es un **claim con una fuente visible** (el global del que se leyó).
Esa es la semilla del contrato de notaría.

## 2. Esquema v1 (emisión en producción)

El digest está orientado a líneas, un dato por línea. Cada claim se emite como:

```
claim|<kind>|<source>|<value>|<d>
```

| Campo | Significado | Ejemplo |
|---|---|---|
| `kind` | tipo de claim | `metric` / `entry` / `config` / `route` / `counter` / `note` |
| `source` | global + subíndices leídos | `^ANGI(metrics,agents_online)` |
| `value` | valor crudo o su digest | `{"value":12,...}` |
| `d` | código de presencia estilo `$D` | `0` / `1` / `10` / `11` |

Nota: no hay campo `ts` separado — la marca de tiempo vive dentro del
`value` crudo cuando el dato fuente la trae (p. ej. `"updated"` en las
métricas de `^ANGI`). Un `ts` por claim legible por máquina es candidato
para la versión anclada (sección 3).

Reglas:

1. **Ningún claim sin fuente.** Una línea sin `source` no es evidencia; no
   debe producirse (y si aparece, el downstream la trata como
   `evidence:false`).
2. **La rutina nunca escribe.** La generación del digest es de solo lectura
   por diseño; cualquier intento de escritura aborta la ejecución (defensa
   en profundidad para el rol de notaría).
3. **`evidence:true|false` forma parte del payload**, siempre presente.

## 3. Anclaje (siguiente paso, lumen-protocol)

Los claims formalizados siguen siendo auto-reportados por el runtime que los
produjo. El anclaje añade verificabilidad externa:

- **Direccionado por contenido**: digest → hash estable (`cid`). Dos agentes
  que comparan sus `cid` saben que vieron el mismo estado.
- **Firmado**: clave del runtime → firma sobre `cid + ts`. Un verificador
  (cualquier otro agente del mesh, o un cron) puede confirmar quién produjo
  el digest y cuándo.
- **Ledger**: añadir el `cid` a la PDB compartida (p. ej. `^EVIDENCE(cid)`)
  para que el rastro sea inspeccionable, no solo afirmado.

Por qué lumen-protocol: el MVM ya aporta el límite de ejecución, la PDB el
ledger compartido y M-Light el runtime portable. Astrid (MIT) aporta el
diseño honesto; lumen-protocol aporta la capa que hace la honestidad
**demostrable entre agentes** — la capa de reputación bajo una licencia
permisiva.

## 4. Preguntas abiertas (para el equipo)

1. Gestión de claves: ¿qué clave del runtime firma los digests y cómo
   verifican los workers (Hermes, Tom, cron) sin una PKI? (¿arrancar con
   HMAC de clave compartida, rotar por host?)
2. Granularidad: ¿firmar el digest completo o por claim (para que un
   verificador pueda aceptar subconjuntos de claims)?
3. ¿Pertenece `^EVIDENCE` al namespace público de lumen-protocol o a un
   namespace por agente?
4. Versionado del esquema: `AstridSchema.v1` — ¿dónde vive el registro?

## 5. Criterios de aceptación para v1

- [ ] **AC-1** `EVIDENCE^ASTRID` emite líneas con el formato del esquema (la fuente
      siempre presente)
- [ ] **AC-2** el camino `evidence:false` es comprobable en la suite de pruebas
- [ ] **AC-3** Un script verificador (harness) comprueba: formato de línea,
      existencia de la fuente en un snapshot dado de la PDB, estabilidad
      del cid ante estados idénticos
- [ ] **AC-4** Documentación actualizada: README (sección del contrato de notaría),
      STORY, DESIGN
