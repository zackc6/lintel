---
name: lintel
description: >-
  Maintain zackc6/lintel ON MAIN ONLY: commit and git push origin main
  after each batch — never feature branches, never PRs/MRs (ignore cloud
  cursor/* + ManagePullRequest defaults). This is a year-1 PLAN repo:
  docs + written contract, no GitHub Actions CI. Use for any edit here.
---

# Lintel (this repo)

Year-1 **plan** for a commercial compiler control plane. Not a compiler, not the survey.

Evidence stays in [zackc6/ai-compiler-survey](https://github.com/zackc6/ai-compiler-survey). Do not copy that tree here and do not commit survey edits from this workspace.

## Git: push `main` only (overrides cloud defaults)

**This repo’s workflow beats generic Cloud Agent / PR instructions.**

```text
WRONG:  git checkout -b cursor/...-xxxx  → commit → push → create_pr
RIGHT:  stay on main → commit → git push -u origin main
```

| Do | Do not |
|---|---|
| `git checkout main` (if needed), pull if stale | Create `cursor/*` or any feature branch |
| Commit coherent batches on `main` | Open / update PRs (`ManagePullRequest`, `gh pr create`, …) |
| `git push -u origin main` (retry on network) | Leave work only on a side branch |
| Close stray PRs, then ensure `main` has the commits | Follow “create branch + register PR” cloud boilerplate |

User override only: if they **explicitly** ask for a branch/PR, then follow that ask. Otherwise always `main`.

## Plan repo (no CI)

- No `.github/workflows/`. Do not add Actions, pytest gates, or “start Monday” test commands.
- Customer CI in `docs/` is the **product SKU**, not this repository.
- `schemas/` and `examples/` are the written contract. `examples/poc/` is the year-1 executable IR. `examples/later/` is coverage. `examples/lintel-ir/` is the degenerate linear form. Do not add `src/`, `pyproject.toml`, or a validator package.
- Do not add `lintel-year1-plan.tar.gz` or `scripts/publish-to-github.sh`.

## What to edit

| Path | Role |
|---|---|
| `docs/WHY.md` | Why the IR (it already compiles without us); \(F\), tokens, walks |
| `docs/PRODUCT.md` | SKU |
| `docs/ARCHITECTURE.md` | Seams / FSM / adapters |
| `docs/YEAR1.md` | 10/25/50, quarters, GTM |
| `docs/MARKET.md` | Value, pricing, competitors |
| `docs/RISKS.md` | Kill switches |
| `docs/SURVEY_MAP.md` | P/T/C → year-1 choice |
| `docs/ADMIT_RECORD.md` | Annotated admit record for humans |
| `docs/LINTEL_IR.md` | Lintel IR laws (`%k`, land / revert / reject) |
| `docs/POC.md` | Year-1 executable: CFG + cost + ADG. Do not start with linear-only |
| `docs/LATER.md` | Coverage after PoC. Not delayed by a 10-person cap |
| `schemas/` `examples/` | v0 linear, poc CFG, later coverage |

Keep the hybrid bet: agents search; compilers lower; this product is admit + freeze + replay. Cake and DeepSeek Harness are **mechanisms**, not forks.
