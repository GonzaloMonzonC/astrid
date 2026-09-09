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
- **Derived agents**: if you build one, link it in the README ecosystem
  section (do not fork this repo into a private agent).

## Conventions

- M routines: M-Light compatible subset (no vendor extensions), labels in
  UPPERCASE, one entry point per concern, comments explain *why*.
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
