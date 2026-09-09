# Security

Astrid is a reference agent that runs **on top of lumen-protocol**. This repo
ships no credentials, no secrets and no private ecosystem data.

## Principles

1. **No secrets in the repo.** API keys, tokens, passwords and PDB files never
   belong here. If you fork this repo, keep your credentials in environment
   variables or a local `.env` (git-ignored) — never in code, docs or commits.
2. **The PDB is a shared memory.** Astrid's rules forbid speculative writes:
   she audits, she does not mutate consensus state without a registered
   mandate (see `critical_rules` in `personalities/astrid.md`).
3. **Audit before you publish.** Before pushing anything derived from this
   repo to a public remote, run:
   ```bash
   git grep -iE "api[_-]?key|token|secret|password|BEGIN .*PRIVATE" HEAD $(git rev-list --all)
   ```
   If it returns anything, clean the history (filter-repo) **before** the
   first public push — history rewrites after publication are unreliable.

## Permissions model

- This repo: read-only template + identity. No runtime permissions.
- When you run Astrid on your own lumen-protocol install, access control is
  lumen's (macaroons, filesystem allowlists, PDB namespaces). Apply the
  least privilege your use case needs; Astrid's demo routines only read.

## Reporting a vulnerability

For issues in this repo: open an issue with the tag `security`. For
lumen-protocol itself, follow the security process of that repository
(https://github.com/GonzaloMonzonC/lumen-protocol).
