# Esquema del digest v1 — el contrato de notaría (diseño)

> Versión en inglés: [EVIDENCE_SCHEMA.md](EVIDENCE_SCHEMA.md)

_Cómo la evidencia registrada de Astrid se convierte en un claim legible por máquina._

Status: **emisor en producción (2026-09-09, verificado en el MVM real)**.
`EVIDENCE^ASTRID` emite claims `claim|<kind>|<source>|<value>|<d>`
parseables (digest de producción ≈ 25 claims con el registro MCP de 5 workers). El digest es canario de la suite (20 checks). El anclaje — cid + firma +
ledger `^EVIDENCE` — está implementado en el runtime (ver sección 3); el
verificador autocontenido es `tests/verify_anchor.py`.

---

## 1. Qué existe hoy (producción, verificado)

`EVIDENCE^ASTRID` es una rutina M de solo lectura. En cada turno de chat, el
runtime (`poli_server`) resuelve `^PERSONALITY("astrid","evidence_routine")`,
ejecuta la rutina en el MVM real y antepone su stdout al prompt de sistema
como **EVIDENCIA REGISTRADA**. Si la ejecución falla o queda vacía, la
respuesta lleva `"evidence": false` — visible por contrato, nunca oculto.

Forma actual del digest — schema v1, un claim por línea (truncado para
legibilidad; ≈25 claims por digest en producción):

```
Astrid v0.3.0 | active=1 | mode activo=astrid | evidence=true
claim|mode|^ACTIVE|astrid|1
claim|counter|^ANGI(level1)|1|10
claim|metric|^ANGI(metrics,agents_online)|{"value": 12, "updated": "2026-09-09T18:25:23Z"}|1
claim|route|^AGENTES(routing,astrid)|{"tipo": "poli", "mode": "astrid"}|1
claim|config|^SPACE(ASI)|127.0.0.1 :9102|10
claim|counter|^QUANTUM(colapso)|119|10
claim|entry|^QUANTUM(colapso,ultimo)|idx=119 raw={"idx": 119, "ts": "...", "backend": "Tuna-17"}|1
claim|note|^VIRTUAL|no existe (la virtualizacion vive en ^MVM)|0
claim|counter|^SYS(MCP)|servers=5|10
claim|config|^SYS(MCP,worker1)|type=http url=https://worker1.internal.example/mcp|1
REGLA: responde SOLO con estos datos registrados; ...
```

Cada línea es un **claim con una fuente visible** (el global del que se leyó).
Esa es la semilla del contrato de notaría.

Desde 0.3.0 el digest también audita el **registro del device MCP**
(`^SYS("MCP", <server>, url|type)`) — los workers de la malla que el
operador siembra para `$DEVICE("mcp:call", ...)`. Astrid ve así el cableado
de su cognitive OS (qué workers existen y cómo alcanzarlos) bajo el mismo
contrato read-only de evidencia. La alcanzabilidad en vivo NO forma parte
del digest: exigiría llamadas salientes por turno de chat. El registro es
el hecho; una sonda de salud es una rutina aparte.

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

## 3. Anclaje (implementado 2026-09-09, runtime lumen-protocol)

Los claims formalizados eran auto-reportados por el runtime que los produjo.
El anclaje añade verificabilidad externa — implementado en `poli_server`
(lumen-protocol), dentro del hook de evidencia (`_evidence_block`), de modo
que **cada digest emitido en producción queda anclado en el momento de
generarse**:

- **Direccionado por contenido**: `cid = sha256(digest)` (hex). Dos agentes
  que comparan sus `cid` saben que vieron el mismo estado; estado idéntico →
  digest idéntico → `cid` idéntico (la estabilidad es canario de la suite).
- **Firmado**: clave del runtime `^CONFIG("ddp_hmac_key")` → HMAC-SHA256
  (`ts + cid + secret`, el esquema estándar `_hmac_sign` del ecosistema).
  Cualquier agente con la clave compartida puede confirmar quién produjo el
  digest y cuándo (el ts se guarda junto a la firma).
- **Ledger**: append-only `^EVIDENCE(cid) = "<sig>|<ts>|<rutina>"` con el
  digest línea a línea en `^EVIDENCE(cid,"digest",n)` (M-nativo, sin saltos
  de línea incrustados). Mismo estado → mismo cid → la fila ya existe → sin
  duplicados (dedup natural). El anclaje nunca rompe el chat: los fallos son
  silenciosos.
- **Verificador**: `tests/verify_anchor.py` (MIT, autocontenido) replica el
  anclaje del runtime en una PDB desechable con una clave DE PRUEBA y
  comprueba estabilidad del cid, forma del ledger, validez de la firma y
  round-trip del digest. La clave real nunca entra en el repo.

Por qué lumen-protocol: el MVM aporta el límite de ejecución, la PDB el
ledger compartido y M-Light el runtime portable. Astrid (MIT) aporta el
diseño honesto; lumen-protocol aporta la capa que hace la honestidad
**demostrable entre agentes** — la capa de reputación bajo una licencia
permisiva.

## 4. Preguntas abiertas (resueltas 2026-09-09)

1. Gestión de claves → **arranque con clave compartida**: el runtime firma
   con la `^CONFIG("ddp_hmac_key")` existente (la misma que ya autentica las
   llamadas a workers). Rotación = rotar el global; sin PKI por ahora.
2. Granularidad → **digest completo**: un `cid` por digest. La firma por
   claim sigue siendo candidata si algún día se necesita verificación por
   subconjuntos.
3. Namespace del ledger → **`^EVIDENCE(cid)` plano**: los cids sha256 son
   únicos entre agentes por construcción; la fila cabecera guarda la rutina
   que produjo cada digest.
4. Versionado del esquema → el header del digest lleva la versión del agente
   (`Astrid v0.3.0 | ...`), así que la versión viaja dentro del payload
   firmado; sin registro separado para v1.

## 5. Criterios de aceptación para v1

- [ ] **AC-1** `EVIDENCE^ASTRID` emite líneas con el formato del esquema (la fuente
      siempre presente)
- [ ] **AC-2** el camino `evidence:false` es comprobable en la suite de pruebas
- [ ] **AC-3** Un script verificador (harness) comprueba: formato de línea,
      existencia de la fuente en un snapshot dado de la PDB, estabilidad
      del cid ante estados idénticos
- [ ] **AC-4** Documentación actualizada: README (sección del contrato de notaría),
      STORY, DESIGN
