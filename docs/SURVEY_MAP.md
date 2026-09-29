# Survey → year-1 decisions

Evidence source: [zackc6/ai-compiler-survey](https://github.com/zackc6/ai-compiler-survey) (`docs/SURVEY.md`). This file does not copy the survey. It records **what Lintel does** when a survey cell is still open. If a conflict settles, change the row — not the controller.

The **goal** is an agentic compiler ([ARCHITECTURE.md](ARCHITECTURE.md)). Scope and the three loops, judged against the **23 September 2026** rewrite: [SURVEY_MATCH.md](SURVEY_MATCH.md). That file wins when it disagrees with a row below.

The tables under Jobs, Conflicts, and Techniques use the **pre-rewrite identifiers** (Horizon A, C1–C10, T1–T10, P1–P23). They are the decision log. Current readings that replace them:

| Old identifier | Governing reading |
|---|---|
| Horizon A / M1, “search only L4” | Year-1 kernel-schedule search for frontier serving. Other decision areas open on a profile, not on a calendar. |
| M3 / C6-A “refused through 2031” | Year-1 keeps check, lower, and fallback. Later replacement is one component on a corpus. |
| T5 as the control plane evolving | T5’s compiler half is the choreo PR (`compiler_ver`). The procedure half is `policy_id`. Memory is `memory_id`. |
| T10 / `%w` as “the controller” | `%w` freezes one job’s ADG. `policy_id` is the procedure. |
| C3 | Start restricted (two Kernels). Compare with wider synthesis before growing the AST. |
| Joint L2–L7 as the architecture | A 2029 experiment, and only if it beats local search and a non-agent joint search. |

## Jobs

| Job | Survey | Year 1 | Why |
|---|---|---|---|
| **(a) online/CI specialize** | 2027 forecast: integrate with existing toolchains; not silent default | **GA SKU** | Only job we sell in year 1 with serving \(F\) |
| **(b) offline heuristic synthesis** | Magellan vs MLGO (**C1**) | Out | Different buyer; Google's fight |
| **(c) oracle PR review** | C7; llvm-harness / Archer | Out of GA; 50-person overlay comments on *kernel* PRs only | Generic SCM review is the wrong SKU |
| **(d) ASIC bring-up / codesign** | C9; TritorX / Zomboss | Out | Needs a second shipping vendor and a coverage SLA; not Cake+DSH |

## Conflicts (do not average)

| ID | If it settles this way | Lintel change |
|---|---|---|
| **C1** Magellan vs MLGO | Either path becomes the CPU/LLVM default | Ignore for the SKU. Do not staff job (b). |
| **C2** vendor headlines vs p50 | Someone publishes default-path p50/p90 + cost | Report *partner* traces in that format. Do not fake it earlier. |
| **C3-A** free rewrite wins a public suite | Widen action enums *behind admit* | Oracles stay. Free CUDA paste is still not the demo. |
| **C3-B** constrained actions hold (current lean) | Keep narrow enums | Sell as the safety story. |
| **C4** Triton vs Tile vs Cake IR vs Argus | Surface fragments | Year-1 live L4 **face** is **Choreo**; Triton is the first **sink**. Another vendor = another printer / `adapter_id`, not a new Lintel IR. |
| **C5** online vs freeze-before-serve | Vendors name ACF workflows in release notes | Integrate; we remain the cross-vendor admit/freeze layer. |
| **C6-A** agents replace compilers | The 23 Sep 2026 question is component-by-component, not a permanent ban | Year-1 keeps check, lower, fallback. One later component, one corpus. No model on serve ([SURVEY_MATCH.md](SURVEY_MATCH.md)). |
| **C6-B** hybrid (current lean) | — | Year-1 application loop. Kill switch if fallback is never drilled. |
| **C7** SCM AI vs compiler-oracle review | llvm-project grows oracle review | Optional year-2 plugin. Not year-1 GA. |
| **C8** “AI compiler” sense | — | We are control plane, not a new Inductor. |
| **C9** coverage vs peak | Second-vendor TritorX-class | Year 2+ if a 50-person overlay exists. |
| **C10** autonomous tape-out | — | Out of scope forever for this SKU. |

## Techniques (T1–T10)

The current guide’s first priorities (§5.8.4, 23 September 2026) are a trustworthy application benchmark, a strong baseline, and a candidate/evaluation interface. The rows below are the older technique list. Year-1 still builds the typed interface (T1), layered admit (T2), replay (T3), and serving measurement (T6), plus compiler PRs into `choreoir` (the compiler half of T5). Controller self-improvement is not a T-row we ship; see [SURVEY_MATCH.md](SURVEY_MATCH.md).

Band names in [ARCHITECTURE.md](ARCHITECTURE.md) are our stack vocabulary.

| T | Year-1 | Year-2 door |
|---|---|---|
| **T1** typed agent↔compiler interface | **Lintel IR** + [PoC](POC.md) CFG/`cost`/ADG **and** Choreo Kernel + `{where}` ([DATA_PLANE.md](DATA_PLANE.md), [CHOREO.md](CHOREO.md)) | Coverage [LATER.md](LATER.md); `@cake.v0` wrap only; still one Lintel IR |
| **T2** admit / fallback | Layered oracles + last_good / classical | SMT / Alive2 as `oracle` providers |
| **T3** freeze + replay | Lintel IR `%k = cache_key(...)`; serve is `lookup(%k)` | Policy bundles |
| **T4** in-tree advisors | Out | Out unless a customer funds job (b) |
| **T5** dialect/ISA feedback | **Compiler half only:** inside a walk, `choreoir` is pinned; across jobs, recurring `{where}` → choreo PR → new `compiler_ver`. A procedure edit is a new `policy_id`, not this row. Not mid-walk `check.py` rewrite ([SURVEY_MATCH.md](SURVEY_MATCH.md)). | Verifier **bundle** classified as compiler, memory, or procedure ([LATER.md](LATER.md)); still not ISA RFCs |
| **T6** serving A/B | One engine, partner traces | Second engine |
| **T7** open multi-IR corpora | Out (not a data company) | Consume KernelBook-class data if it helps the Choreo adapter |
| **T8** unified ladder | Refuse KernelBench as GA metric; partner ladder + cost-to-compile | Public method note, not a fake industry p50 |
| **T9** provenance / CODEOWNERS | Q3 | Air-gap / SSO at 25–50 people |
| **T10** workflow compile | [PoC](POC.md): compile one CFG to ADG; interpret ADG | [LATER.md](LATER.md): `%w`, policy-hash, more edges; still `lookup(%k)` on serve |

## Commercial problems (P1–P23)

Survey lean is the default. Year-1 choice is the productization of that lean.

| P | Survey lean | Year-1 product choice |
|---|---|---|
| P1 contract | Typed tools + structured traces; NL at human edge | `admit-record.v0` + tool kinds `propose/verify/bench/profile` |
| P2 memory | Scratchpad ≪ skills ≪ **VCS** | Frozen artifacts in customer git |
| P3 topology | Specialists + orchestrator + trace bus | FSM on SLA path; no swarms |
| P4 when agents run | CI / hot-path → freeze | Default overnight; lab tier labeled |
| P5 oracles | Layered + named false-neg owners | Schema requires `false_neg_owner` |
| P6 supply chain | CODEOWNERS + signed provenance + sandbox | Template in `.github/CODEOWNERS.template`; Q3 signing |
| P7 multi-DSL | Multi-skill; IR is substrate | One live adapter; empty second adapter in Q3 |
| P8 packaging | Flag/SKU + frozen artifacts | Lintel Specialize (on-prem / VPC) |
| P9 eval | Public p50/p90 + private canaries; always $/compile | Private canaries in year 1; public *method* in Q4 |
| P10 pricing | Artifact + CI quota; not token burn | See [MARKET.md](MARKET.md) |
| P11 tenancy | Customer-owned CI | No multi-tenant SaaS searcher in year 1 |
| P12 model lock-in | Pluggable + golden replay | `llm` seam; replay invariant in code |
| P13 IP | Customer owns outputs; telemetry opt-in | Contract requirement in GA DoD |
| P14 versioning | Pins in admit records | `pins` object: hw, compiler, adapter, model, policy |
| P15 cold-start HW | Coverage SLA then perf SLA | Not a year-1 SKU (job d) |
| P16 HITL capacity | Oracle auto-merge narrow; humans own rewrites | Auto-merge only enumerated actions that passed admit |
| P17 flywheel | Closed for hetero prod | No silent training on customer graphs |
| P18 latency SLO | Lab vs product tiers | CLI flag `mode=sku\|lab` from Q1 |
| P19 DR | Allowlist + canary rollback | Fallback fire-drill every quarter |
| P20 A/B platform | Shadow/replay before “production default” | Q2 serving seam; never claim default-all |
| P21 compliance | Customer-hosted manuals | Customer CI; no vendor-cloud ISA RAG |
| P22 orchestration | FSM/plan + bounded LLM slots | `lintel.fsm` |
| P23 tokens | Freeze + Amdahl + route/distill | Q2 kill: unknown $/admitted %\(F\) → hiring freeze |

## Survey commercial checklist (16)

| # | Item | Where it lands |
|---|---|---|
| 1 | Typed contract, not NL | schemas + P1 |
| 2 | VCS as product truth | freeze URI in admit record |
| 3 | Orchestrator + FSM | `lintel.fsm` |
| 4 | CI/hot-path → freeze | YEAR1 Q1–Q2 |
| 5 | Layered oracles + owners | schema required field |
| 6 | CODEOWNERS + sign + sandbox + rollback | Q3 + RISKS |
| 7 | Joint version pins | `pins` |
| 8 | Eval + cost-to-compile | fitness.usd_per_compile |
| 9 | A/B before “default” marketing | MARKET / RISKS |
| 10 | HITL capacity plan | P16 above |
| 11 | SKU = artifacts + CI quota | PRODUCT / MARKET |
| 12 | Customer owns outputs; pluggable models | GA DoD |
| 13 | Multi-DSL; coverage then perf for new Si | stub adapter; P15 out |
| 14 | Tenancy/residency | on-prem / customer CI |
| 15 | Support: replay packs, spend caps, oracle-miss severity | YEAR1 Q3–Q4 |
| 16 | Resource envelope | YEAR1 Q2 kill switch |

If this map and the code disagree, **the map is wrong** — fix the doc, do not weaken replay.

## LLM-oriented IR survey → Lintel pins

Source: survey §0.2 + §5.1.1–5.1.2, from *The New Compiler Stack* (arXiv:2601.02045). Design write-up: [LLM_IR.md](LLM_IR.md). Do not collapse Lintel IR to their NL / PL / LLVM-IR map.

A **separate** independent survey (primary papers, four kinds: program / decision / freeze / control) lives in [LLM_ORIENTED_IR.md](LLM_ORIENTED_IR.md). Do not merge those families into this table.

| Their claim | Year-1 product choice |
|---|---|
| Selector is the safe LLM role | SLA `propose` = allowlisted **Choreo Kernel**. Widen only behind admit (**C3-A**). |
| Translator has the correctness problem | `paste_cuda` / free IR rewrite **illegal** on SLA. Lab may be looser; still no `land` without gates. |
| Generator of *inspectable* artifacts beats chat | Payload is `adapter-proposal.v0` + admit record. Commentary is not truth. Magellan Generator (new passes) stays job (b) **out**. |
| Train an IR-LLM (Meta Compiler on LLVM IR) | Later `llm` **provider**. Not a new Lintel dialect. P12. |
| Intra-level rewrite at LLVM IR / ASM | Classical **L0/L5**. No `propose` there in year 1. |
| Cross-level neural compile / decompile | Survey **M3**. Out. |
| KernelBench / CA@k / `-Oz` size as SOTA | Not GA. Serving **\(F\)** + $/compile. |
| Constrained decoding / grammar-guided CUDA | JSON **schema** on the Choreo Kernel is the constraint. |
| LEGO-style basic-block split for LLM compile | Out. Scale = Amdahl `triage`, not neural compile. |
| Hybrid systems are the near-term path | Already the company. Kill switch: fallback never drilled (**C6-B**). |
