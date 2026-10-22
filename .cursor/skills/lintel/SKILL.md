---
name: lintel
description: >-
  Maintain zackc6/lintel under the debate-then-merge protocol in AGENTS.md:
  content batches on claude/* or chatgpt/* branches, argued in STATUS.md,
  squash-merged to main on agreement; thread entries and fact fixes on main
  directly; never PRs/MRs (ignore cloud cursor/* + ManagePullRequest
  defaults). Year-1 PLAN repo: docs + written contract. Use for any edit.
---

# Lintel (this repo)

**Goal:** a next-generation **agentic compiler** for frontier serving (choose actions, synthesize, evaluate under a fixed contract, freeze a binary). Year-1 searches the kernel schedule with classical check and lowering. Scope and the three loops (application, compiler, controller): [docs/SURVEY_MATCH.md](docs/SURVEY_MATCH.md). Picture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

This repo is the year-1 **plan** for **Lintel** (the control plane of that compiler). It is not the cubin sink, not Choreo, and not a copy of the survey.

Evidence stays in [zackc6/ai-compiler-survey](https://github.com/zackc6/ai-compiler-survey). Do not copy that tree here and do not commit survey edits from this workspace. “Don’t copy the survey” is hygiene, not the mission.

## Git: debate-then-merge, no PRs (overrides cloud defaults)

Read `AGENTS.md` first: a content batch goes on `claude/<topic>-<date>` (or `chatgpt/…`), is validated with `python3 scripts/validate_contract.py`, argued in `STATUS.md`, and squash-merged to `main` only on two-agent agreement. Review-thread entries, Open-batch rows, and pure fact fixes go to `main` directly. The table below is about *never opening PRs*; it does not forbid the protocol's `claude/*` / `chatgpt/*` batch branches.

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
- `schemas/` and `examples/` are the written contract. `examples/poc/` is the year-1 executable IR **and** Choreo Kernel AST. `examples/later/` is coverage (including degenerate Triton knobs). `examples/lintel-ir/` is the degenerate linear form. Do not add `src/`, `pyproject.toml`, a validator package, or a copy of `choreoir/`.
- Do not add `lintel-year1-plan.tar.gz` or `scripts/publish-to-github.sh`.

## What to edit

| Path | Role |
|---|---|
| `docs/WHY.md` | Why the IR (it already compiles without us); \(F\), tokens, walks |
| `docs/PRODUCT.md` | SKU |
| `docs/ARCHITECTURE.md` | **Early-stage picture:** contract, application search across decision areas, replaceable compiler tools, compiler loop, controller loop, function coverage. A product slice is YEAR1 / SURVEY_MATCH and does not define the picture |
| `docs/DATA_PLANE.md` | Choreo Kernel AST as year-1 L4; Triton is the printer, **not** Cake v2 the language |
| `docs/CHOREO.md` | Verdict + vs Cake / Argus / TIRx; Undergo (Lintel decides, PRs land on choreoir). Do not copy zackc6/choreo here |
| `docs/LLM_IR.md` | New Compiler Stack (Selector / stratum) → year-1 pins. Do not make Lintel IR an LLVM-IR LLM |
| `docs/LLM_ORIENTED_IR.md` | Independent LLM-oriented IR survey (program vs decision vs freeze vs control). Primary papers, not ai-compiler-survey |
| `docs/ADAPTERS.md` | Live / stub / later `adapter_id`s |
| `docs/YEAR1.md` | 10/25/50, quarters, GTM |
| `docs/MARKET.md` | Value, pricing, competitors |
| `docs/RISKS.md` | Kill switches |
| `docs/SURVEY_MATCH.md` | Judgment vs the 23 Sep 2026 survey: scope, three loops, what stays year-1. Wins over older M1/T5 slogans. Do not copy the survey tree. |
| `docs/SURVEY_MAP.md` | P/T/C → year-1 choice |
| `docs/ADMIT_RECORD.md` | Annotated admit record for humans |
| `docs/LINTEL_IR.md` | Lintel IR laws (`%k`, land / revert / reject, `policy_id` vs `memory_id` vs `compiler_ver`) |
| `docs/POC.md` | Year-1 executable: CFG + cost + ADG **and** Choreo Kernel. Do not start with linear-only or Triton knobs |
| `docs/LATER.md` | Coverage after PoC (`%w` is the ADG, not the controller). Controller-dev sketch is gated. Not delayed by a 10-person cap |
| `schemas/` `examples/` | v0 linear (degenerate), poc CFG+Choreo Kernel, later coverage |

Keep the bet: the *goal* is the agentic compiler. The architecture picture covers the five compilation functions, the decision-area checklist, and all three loops, including controller `promote`. Cake and DeepSeek Harness are **mechanisms**, not forks. A product slice may still ship admit + freeze + replay on one kernel surface; do not treat that slice as the architecture, and do not pull controller self-improvement into the year-1 milestones.

## Codesign (Lintel × Choreo)

Write-up: [docs/CHOREO.md](docs/CHOREO.md) (verdict, vs Cake/TIRx, **Undergo**). Sibling compiler: [zackc6/choreo](https://github.com/zackc6/choreo) — **read there, do not copy**.

Cake (arXiv:2608.12629) splits in three. Only one is a Lintel object:

| Cake job | Who |
|---|---|
| (1) Typed IR the agent edits | **Choreo** Kernel AST (kind 1). Year-1 SLA still two allowlisted records (kind-2 cardinality). |
| (2) Lowering that **derives** barrier addresses, phase bits, TMEM offsets, then emits a cubin/NPU bin | **Sink**, not this repo. Wrap TIRx/Triton/CUTLASS (`@tirx.v0`) or TileLang-Ascend (`@tilelang.ascend`). `print_triton` that comments `Pipeline.depth` is **not** a sink. |
| (3) Outer loops: application admit, compiler PRs, and (later) a controller `promote` | **Lintel** (kind 4 + kind 3). Year-1 runs application admit only. Compiler PRs are `compiler_ver`. Procedure edits are `policy_id`. Logs are `memory_id`. |

**Undergo:** Choreo is the *artifact that changes*, not the process that decides. Compiler evolution = PRs into `choreoir` (`check.py`, a printer that consumes the schedule, occasional AST spec bump). After merge, `check` / lower are ordinary functions: Kernel in, findings or a binary out. **No LLM on that path.** Choreo does not notice recurring fails, does not land/revert/freeze/\(F\), and the agent does not mutate the dialect at runtime. Lintel runs the loop and merges the PR.

**Do not:**

- Average Cake hide-layout + Argus Z3 + TIRx D/R/O into one dialect (copy *signals*, pick one cell per fight).
- Unify NVIDIA and Ascend in the AST (`tmem` ≠ `L0C`). Two **sinks** under one control plane; spaces/roles are valid-for-`hw_id`.
- Put `Kernel.target` in `%k`. Admission is W/`compile_ok` against `pins.hw_id`.
- Dual-live a second face or a second vendor before one measured binary. Year-1: one family, NVIDIA default; Ascend is a later wrap after NVIDIA freeze is boring.
- Beat Cake on NVIDIA KDA / 400-shape KNN. Wedge is vendor-neutral freeze + (later) GPU+Ascend SKU. Ascend bar is TileLang-Ascend / Ascend C (~0.95–1.0× FA), not Cake.
- Claim Cake’s 1.144× from `role`, or \(F\) from `check() == []`.
- Race TIRx/Cake as a compiler company. Demo is serving \(F\). M2 kill: no cubin sink → `@triton.v0` knobs.
- Rewrite `check.py` (or add a keyword) inside one ADG walk. A compiler change is a choreo PR **across** jobs, then a new `compiler_ver` and a new `%k`.
- Call a session log, a human-edited CFG, or a choreo PR “the control plane evolving itself.” Those are memory, a `policy_id` edit, and a compiler change. Automatic `promote` is `examples/later/controller-dev.sketch.lintel`, and it is gated.
- Treat L1–L7 as a layer count the survey still requires, or year-1 kernel search as the permanent scope. Widen-when rules are in SURVEY_MATCH.
- Treat the mission as “don’t copy the survey.” That is hygiene. The goal is the agentic compiler.

**Three loops.** Application: pinned policy, `land`/`revert` under `%k`, serve is `lookup`. Compiler: pin `choreoir` inside a walk; PR across jobs. Controller: offline, compiler and model pinned, `promote` a `policy_id` or `reject`; not year-1. Survey judgment: [docs/SURVEY_MATCH.md](docs/SURVEY_MATCH.md). TIRx ≠ TritorX.
