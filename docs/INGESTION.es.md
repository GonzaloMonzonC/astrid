# Ingest: fuentes externas → PDB → auditadas por Astrid

> 🇬🇧 English version: [INGESTION.md](INGESTION.md)

El digest demuestra que Astrid responde solo desde datos registrados. Esta demo
cierra la otra mitad del bucle: **conseguir que los datos externos se registren
en primer lugar**, con la maquinaria propia de lumen (MVM + PDB), para que el
agente pueda auditar un flujo entrante con su contrato habitual.

```
external source ──POST──▶ ingest_demo.py (webhook, stdlib)
                              │  D INGEST^ASTRID(origen, raw)
                              ▼
                    ^ASTRID("inbox", <origen>, <seq>) = raw JSON
                              │  (next chat / digest run)
                              ▼
              EVIDENCE^ASTRID emits inbox claims:
              claim|counter|^ASTRID(inbox,github)|eventos=2|1
```

No hace falta nada nuevo para auditar el flujo: el inbox es un global de la PDB
como cualquier otro, así que el digest registrado ya lo cubre. El agente ve
llegar los eventos y puede señalar rupturas de esquema, duplicados o fuentes
ausentes — o negarse a responder cuando los datos no están.

## Ejecútalo

```bash
# terminal 1 — el webhook
python examples/ingest/ingest_demo.py --db /tmp/astrid_ingest.db

# terminal 2 — dispara eventos
curl -X POST "http://127.0.0.1:8787/hook?origen=github" \
     -H "Content-Type: application/json" \
     -d '{"event": "push", "repo": "astrid", "ref": "main"}'
curl -X POST "http://127.0.0.1:8787/hook?origen=github" \
     -H "Content-Type: application/json" \
     -d '{"event": "push", "repo": "astrid", "ref": "docs"}'
curl -X POST "http://127.0.0.1:8787/hook?origen=webhook" \
     -H "Content-Type: application/json" \
     -d '{"event": "ping"}'

# inspecciona lo que el agente verá la próxima vez que le pregunten
curl "http://127.0.0.1:8787/digest" | python -m json.tool
```

La salida del digest incluye los claims del inbox:

```
claim|counter|^ASTRID(inbox,github)|eventos=2|1
claim|counter|^ASTRID(inbox,webhook)|eventos=1|1
```

## El contrato (mantenerlo honesto)

- **`INGEST^ASTRID(origen, raw)`** añade un evento: `origen` es una etiqueta
  corta de fuente (≤ 32 caracteres, sin espacios), `raw` es el payload original
  conservado tal como se recibió. El número de secuencia es por fuente.
- El inbox es **de solo añadido** para los escritores externos — sin ediciones
  in-place. Auditar y corregir es trabajo de Astrid, no del webhook.
- Un `POST` cuyo cuerpo no sea JSON se rechaza con `400` antes de tocar la PDB:
  el control está en la puerta, no en la auditoría.
- El webhook es deliberadamente libre de dependencias (solo stdlib) para que el
  patrón sea legible; ponlo detrás de tu propia autenticación (token, política
  de red) cuando lo despliegues — el control de acceso de lumen es el sobre.

## Qué demuestra esto

1. **Lumen hace la ingesta**: un camino HTTP → MVM → PDB con ~40 líneas de
   stdlib.
2. **El agente audita lo que llega**: mismo digest, mismo schema, mismo
   contrato `evidence:true|false` — sin modo especial para los datos externos.
3. **El bucle de notaría ya está completo**: fuente → registro → auditoría →
   (siguiente paso) anclaje firmado, para que cualquier agente pueda verificar
   *qué* llegó, *cuándo* y *que Astrid lo vio*.

Ver `src/astrid.m` (la etiqueta `INGEST` y el bloque de inbox de `EVIDENCE`) y
`docs/EVIDENCE_SCHEMA.md` para el schema de los claims. La suite cubre el bucle
(`python tests/run_tests.py`, checks "INGEST escribe inbox" / "digest ve
inbox …").
