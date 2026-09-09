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

La identidad se siembra en el MVM de Poli (ver `poli-personalities` skill):

```m
S ^PERSONALITY("astrid","identity")="..."
S ^PERSONALITY("astrid","provider")="deepseek"
S ^PERSONALITY("astrid","model")="deepseek-v4-flash"
S ^PERSONALITY("astrid","is_active")="1"
```

Para convertirla en agente M-native de pleno derecho (chat/inbox propios):
registro en `^MVM("agents","astrid",...)` con rutina (ver skill
`mvm-native-agents`). Ese paso usará `src/astrid.m` de este repo como rutina.

## Roadmap

1. ~~Tarjeta de identidad (ronda gabinete)~~ ✅
2. ~~Registro ^PERSONALITY~~ ✅  (identity_len=646, active=1)
3. ~~Esqueleto repo~~ ✅
4. `astrid init` — bootstrap: identity + spawn MVM + registro ^AGENTES
5. Harness LUMEN (MCP servers) + docs/BUILD_YOUR_OWN.md
6. Ops de referencia: auditoría PDB de ejemplo + supervisión MVM
7. Agentes hermanos: otros agentes de referencia con otras facultades
