#!/usr/bin/env python3
"""🧬 Astrid template renderer — derive a new agent repo from the template.

Reads template files and replaces tokens to produce a working agent skeleton
in <dest>/ ready to edit, seed and verify:

    python template/render.py NAME --emoji EMOJI --role ROLE \
        --identity-file identities/NAME.txt --dest ../my-agent

Tokens replaced in template files:
    __NAME__  lower-case agent name (also the ^PERSONALITY key)
    __NAMEU__ UPPER-CASE routine label
    __EMOJI__ __ROLE__ __CATEGORY__ __COLOR__ __CORE_MISSION__
    __RULE_1..3__  __CAP_1/2__ (+ _DESC)  __IDENTITY__

Identity rule (MUMPS storage): ONE line, ASCII, no accents, 600–1400 chars.
Keep the human-readable version (with accents) in personalities/<name>.md.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULTS = {
    "emoji": "🧬",
    "category": "system",
    "color": "#38bdf8",
    "core_mission": "Ser un agente derivado de la plantilla Astrid: demostrar el contrato del agente de referencia sobre lumen-protocol",
    "rule_1": "Operar solo sobre datos registrados: PDB, ^GLOBALES, estado MVM. Nunca suposiciones ni lore privado",
    "rule_2": "No especular: sin certeza registrada, reportar el hallazgo y pedir confirmacion",
    "rule_3": "Registrar todo: cada operacion y hallazgo queda como caso reproducible",
    "cap_1": "STATUS", "cap_1_desc": "Reportar estado de identidad y configuracion",
    "cap_2": "SEED", "cap_2_desc": "Sembrar la entrada ^PERSONALITY de forma reproducible",
}


def build_tokens(name: str, overrides: dict) -> dict:
    tokens = dict(DEFAULTS)
    tokens.update(overrides)
    tokens["name"] = name.lower()
    tokens["nameu"] = name.upper()
    return tokens


def render_text(text: str, tokens: dict) -> str:
    for key, val in tokens.items():
        text = text.replace(f"__{key.upper()}__", str(val))
    return text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", help="agent name, lower-case (also ^PERSONALITY key)")
    ap.add_argument("--dest", required=True, help="destination dir for the derived agent")
    ap.add_argument("--identity-file", required=True, help="file with the ASCII identity line (600-1400 chars)")
    for k, v in DEFAULTS.items():
        ap.add_argument(f"--{k.replace('_', '-')}", default=v)
    ap.add_argument("--role", required=True)
    args = ap.parse_args()

    identity = Path(args.identity_file).read_text(encoding="utf-8").strip()
    if len(identity) < 600 or len(identity) > 1400:
        raise SystemExit(f"identity must be 600-1400 chars (got {len(identity)})")
    if re.search(r"[^\x00-\x7f]", identity):
        raise SystemExit("identity must be pure ASCII (no accents/ñ)")

    overrides = {k: getattr(args, k.replace("-", "_")) for k in DEFAULTS}
    overrides["identity"] = identity
    tokens = build_tokens(args.name, overrides)

    dest = Path(args.dest)
    if dest.exists():
        raise SystemExit(f"dest exists: {dest}")
    dest.mkdir(parents=True)
    (dest / "src").mkdir()
    (dest / "personalities").mkdir()
    (dest / "tests").mkdir()

    # source template (routine)
    src_tpl = ROOT / "src" / "AGENT.m.tpl"
    (dest / "src" / f"{tokens['name']}.m").write_text(
        render_text(src_tpl.read_text(encoding="utf-8"), tokens), encoding="utf-8"
    )
    # tests: copy parametric verify.m from repo root tests
    verify = ROOT.parent / "tests" / "verify.m"
    (dest / "tests" / "verify.m").write_text(verify.read_text(encoding="utf-8"), encoding="utf-8")
    # personalities markdown (skeleton to complete by hand)
    ident_md = ROOT / "personalities" / "AGENT.md.tpl"
    if ident_md.exists():
        (dest / "personalities" / f"{tokens['name']}.md").write_text(
            render_text(ident_md.read_text(encoding="utf-8"), tokens), encoding="utf-8"
        )
    # readme pointer
    (dest / "README.md").write_text(
        f"# {tokens['emoji']} {tokens['name']}\n\nDerived from the "
        "[Astrid template](https://github.com/GonzaloMonzonC/astrid). "
        "Edit `personalities/{name}.md` and `src/{name}.m`, then seed and verify:\n\n"
        "```m\nD INIT^{U}\nD VERIFY^VERIFY(\"{name}\")\n```\n".format(
            name=tokens["name"], U=tokens["nameu"]
        ),
        encoding="utf-8",
    )
    print(f"✅ agent '{tokens['name']}' generado en {dest}")
    print("Siguiente: edita personalities/ y src/, despues INIT + VERIFY.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
