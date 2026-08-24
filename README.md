# Lintel

**A commercial compiler control plane for a 10–50 person team, deliverable in 12 months.**

Lintel is **not** a new `opt` / Inductor / Triton, and **not** a generic coding agent. Agents search and synthesize; classical compilers lower, measure, and fall back; Lintel owns the **typed contract, layered admit, freeze, and replay** so that loop can be sold.

This repository is a **year-1 plan** (plus a written v0 contract in `schemas/` / `examples/`). It is not a compiler and it does not run CI. It does not fork [Cake](https://arxiv.org/abs/2608.12629) or [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness). It takes Cake’s **typed schedule contract + localized reject + evolving harness** and DSH’s **plugin seams + append-only session log**, and composes them as the product kernel. Evidence: [ai-compiler-survey](https://github.com/zackc6/ai-compiler-survey) (read in place; this repo does not copy it).

**Year-1 SKU.** CI/hot-path specialize on Amdahl-ranked kernels → layered admit → freeze a content-addressed artifact → serving A/B on one engine → classical fallback. Customer owns the artifact. No LLM on the serve path.

**What we refuse to sell in year 1.** “LLM replaces the compiler.” “Default-on for every build.” “One agent IR for all vendors.”

**Maintainer git.** Commit and push `main` directly. No feature branches, no PRs — see [`.cursor/skills/lintel/SKILL.md`](.cursor/skills/lintel/SKILL.md). This repo has no GitHub Actions.

## Start Monday

Week-1 decisions are in [docs/YEAR1.md](docs/YEAR1.md). Read the docs; `schemas/` and `examples/` are the written contract, not a package to test in this repo.

| Path | What it is |
|---|---|
| [docs/PRODUCT.md](docs/PRODUCT.md) | What we sell, and why Cake+DSH alone is the wrong SKU |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Seams, FSM, repo layout; year 2–3 survey shifts are adapters |
| [docs/YEAR1.md](docs/YEAR1.md) | Quarters, 10/25/50 staffing, week-by-week Q1, hiring order, GTM |
| [docs/MARKET.md](docs/MARKET.md) | Business value, unit economics, competitors over 1–3 years |
| [docs/RISKS.md](docs/RISKS.md) | Kill switches tied to survey checkpoints |
| [docs/SURVEY_MAP.md](docs/SURVEY_MAP.md) | Jobs, C1–C10, T1–T10, P1–P23 → year-1 choice |
| [docs/ADMIT_RECORD.md](docs/ADMIT_RECORD.md) | Annotated admit record (landed + reverted) |
| [docs/LINTEL_IR.md](docs/LINTEL_IR.md) | Lintel IR: land / revert / reject + cache_key |
| `schemas/` | Lintel IR, admit record, session event, cache key (v0) |
