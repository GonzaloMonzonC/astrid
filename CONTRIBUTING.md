# Contributing

Astrid is a **reference agent**: her value is being a clean, MIT, readable
template for building agents on lumen-protocol.

## What helps

- **Bug reports** on the M routines (`src/`), the harness or `tests/` —
  with the failing M snippet and your lumen-protocol version.
- **Identity improvements** (voice, rules, capabilities) that keep her
  literal, non-speculative character — the design round notes live in
  `docs/DESIGN.md`.
- **Docs**: clearer BUILD_YOUR_OWN steps, better examples.
- **Derived agents**: if you build one, link it in the README "Sibling agents"
  section (do not fork this repo into a private agent).

## Conventions

- M routines: M-Light compatible subset (no vendor extensions), labels in
  UPPERCASE, one entry point per concern, comments explain *why*.
- **M-Light pitfall (verified)**: never nest M functions inline as a
  subscript or inside a concatenation (`$O(^G("x",$O(...)))` or
  `"_$D(^G(...))"` break the parser) — assign to an intermediate variable
  first, then use the variable.
- `EVIDENCE` claims follow the schema: `claim|<kind>|<source>|<value>|<d>`
  (see `docs/EVIDENCE_SCHEMA.md`). No claim without a source; the routine is
  read-only; the `evidence` flag is always part of the digest header.
- Identity line: ASCII, one line, 600–1400 chars, no accents
  (`^PERSONALITY` storage constraint) — the human-readable version with
  accents lives in `personalities/astrid.md` and must stay in sync.
- No private lore: nothing that references non-public systems, URLs, agents
  or business logic may enter this repo (MIT).
- Tests must pass on a **throwaway PDB** (temp file), no external services:
  ```bash
  python harness/astrid_harness.py status
  ```
- Semantic versioning: see `CHANGELOG.md`.

## Process

1. Open an issue or PR describing the change.
2. Run the verification (`tests/verify.m` via the harness) before asking for
   review.
3. Keep PRs small; the whole repo should stay reviewable in one sitting.
