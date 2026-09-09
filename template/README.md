# 🧬 Astrid template — build your own agent

This directory is a **copyable, renderable skeleton** for deriving a new agent
on lumen-protocol with the same contract as Astrid (status / seed / verify).

## Derive (render)

```bash
# 1. prepare the identity: ONE line, ASCII, no accents, 600–1400 chars
cat > /tmp/identity.txt <<'EOF'
<your identity line here>
EOF

# 2. render (creates <dest> with src/, personalities/, tests/, README)
python template/render.py myagent \
  --dest ../myagent \
  --identity-file /tmp/identity.txt \
  --role "your role" \
  --emoji 🧬 \
  --color "#38bdf8"

# 3. edit the generated files (personalities/myagent.md, src/myagent.m, README)
```

## Seed + verify

```m
D INIT^MYAGENT            ; fill-missing seed of ^PERSONALITY("myagent")
D ASTRID^MYAGENT          ; status (generated as MYAGENT^MYAGENT)
D VERIFY^VERIFY("myagent") ; → PASS myagent verificado
```

Run against a **throwaway PDB** first (see harness in repo root).

## Contract

Every derived agent keeps the same entry points so the ecosystem can treat
any agent uniformly:

| Entry | What it does |
|---|---|
| `<NAME>^<NAME>` | status: identity_len, active, provider/model |
| `INIT^<NAME>` / `INIT^<NAME>(1)` | reproducible seed of `^PERSONALITY(name)` |
| `VERIFY^VERIFY("name")` | PASS/FAIL checks (shared parametric test) |

## Token reference

| Token | Meaning |
|---|---|
| `__NAME__` / `__NAMEU__` | lower-case name (`^PERSONALITY` key) / upper-case routine label |
| `__IDENTITY__` | ASCII one-line identity (600–1400 chars) |
| `__ROLE__ __EMOJI__ __CATEGORY__ __COLOR__` | profile fields |
| `__RULE_1..3__ __CAP_1/2__ __CAP_1_DESC__…` | seed content |

## Real example

`examples/echo/` in this repo was generated with this template and verified —
it proves the template is reusable (identity-only change).
