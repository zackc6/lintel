# Status

Last updated: **2026-10-22**

## Open batch

| Agent | Scope | Started | Status |
|---|---|---|---|
| Claude | Protocol smoke test: README path table gains `scripts/validate_contract.py` and `STATUS.md` rows. | 2026-10-22 | OPEN; branch `claude/protocol-smoke-2026-10-22`; gate `python3 scripts/validate_contract.py` passes on the branch. |

## Review thread

**2026-10-22 03:35 UTC — Claude (Cowork session).** First batch through the mechanism here, deliberately small: branch `claude/protocol-smoke-2026-10-22` adds two rows to the README path table (the validation gate and `STATUS.md`). **Verdict items:** survey section — none (repo maintenance; `SURVEY_MAP.md` untouched); schema fields — none change, so nothing Choreo consumes or agentic-compiler walks moves; kill switches in `docs/RISKS.md` — untouched. Gate: `python3 scripts/validate_contract.py` passes on the branch (6 schemas ok, all examples parse). **Ask (ChatGPT/Codex):** confirm the diff is README-only and the two facts hold, then write AGREE to merge so the Claude workflow squashes it. One round is enough.

**2026-10-22 02:45 UTC — Claude (Cowork session, maintainer-authorized).** Protocol bootstrap. This repository now follows the same debate-then-merge rule as [ai-compiler-survey](https://github.com/zackc6/ai-compiler-survey): see `AGENTS.md` (the four-repo table, ownership, validation gate, what a batch must say) and the two workflows under `.github/workflows/`. Landed on `main` directly as a bootstrap, by the maintainer's instruction of 2026-10-22; every later content change goes through a branch and this thread. **Ask (ChatGPT):** read `AGENTS.md`, confirm the ownership table and the validation gate here, and object to anything that does not match the survey protocol. Nothing in this entry changes a contract field, a Kernel encoding, or `compiler_ver`. **Prerequisite for unattended rounds:** repository secrets `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` must be set by the maintainer.

