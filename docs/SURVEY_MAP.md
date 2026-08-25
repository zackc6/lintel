# Survey → year-1 decisions

Evidence source: [zackc6/ai-compiler-survey](https://github.com/zackc6/ai-compiler-survey) (`docs/SURVEY.md`). This file does not copy the survey. It records **what Lintel does** when a survey cell is still open. If a conflict settles, change the row — not the controller.

## Jobs

| Job | Survey | Year 1 | Why |
|---|---|---|---|
| **(a) online/CI specialize** | Horizon A ships for *some* products, not silent default | **GA SKU** | Only job we sell in year 1 with serving \(F\) |
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
| **C4** Triton vs Tile vs Cake IR vs Argus | Surface fragments | Ship another `adapter` provider. Year-1 live L4 is a **typed Triton schedule**, not Cake IR. Portable schema was the year-1 bet. |
| **C5** online vs freeze-before-serve | Vendors name ACF workflows in release notes | Integrate; we remain the cross-vendor admit/freeze layer. |
| **C6-A** agents replace compilers | — | **Do not follow.** Wrong company. |
| **C6-B** hybrid (current lean) | — | Stay. Kill switch if fallback is never drilled. |
| **C7** SCM AI vs compiler-oracle review | llvm-project grows oracle review | Optional year-2 plugin. Not year-1 GA. |
| **C8** “AI compiler” sense | — | We are control plane, not a new Inductor. |
| **C9** coverage vs peak | Second-vendor TritorX-class | Year 2+ if a 50-person overlay exists. |
| **C10** autonomous tape-out | — | Out of scope forever for this SKU. |

## Techniques (T1–T10)

Survey §5.8.4 highest-leverage missing parts: money-grade oracles (T2+T6), replayable artifacts (T3), portable agent compile interface (T1). Lintel year 1 **is those three**, not a new IR.

| T | Year-1 | Year-2 door |
|---|---|---|
| **T1** typed agent↔compiler interface | **Lintel IR** + [PoC](POC.md) CFG/`cost`/ADG **and** typed Triton schedule + `{where}` ([DATA_PLANE.md](DATA_PLANE.md)) | Coverage [LATER.md](LATER.md); `@cake.v0` wrap only; still one Lintel IR |
| **T2** admit / fallback | Layered oracles + last_good / classical | SMT / Alive2 as `oracle` providers |
| **T3** freeze + replay | Lintel IR `%k = cache_key(...)`; serve is `lookup(%k)` | Policy bundles |
| **T4** in-tree advisors | Out | Out unless a customer funds job (b) |
| **T5** dialect/ISA feedback | **Lite:** PoC `adapter_gate` `{where}`; recurring fails → new check or tighter schedule bound (test-gated) | Not ISA RFCs; L5 `where` is an oracle plugin |
| **T6** serving A/B | One engine, partner traces | Second engine |
| **T7** open multi-IR corpora | Out (not a data company) | Consume KernelBook-class data if it helps the Triton adapter |
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

| Their claim | Year-1 product choice |
|---|---|
| Selector is the safe LLM role | SLA `propose` = allowlisted Triton **schedule**. Widen only behind admit (**C3-A**). |
| Translator has the correctness problem | `paste_cuda` / free IR rewrite **illegal** on SLA. Lab may be looser; still no `land` without gates. |
| Generator of *inspectable* artifacts beats chat | Payload is `adapter-proposal.v0` + admit record. Commentary is not truth. Magellan Generator (new passes) stays job (b) **out**. |
| Train an IR-LLM (Meta Compiler on LLVM IR) | Later `llm` **provider**. Not a new Lintel dialect. P12. |
| Intra-level rewrite at LLVM IR / ASM | Classical **L0/L5**. No `propose` there in year 1. |
| Cross-level neural compile / decompile | Survey **M3**. Out. |
| KernelBench / CA@k / `-Oz` size as SOTA | Not GA. Serving **\(F\)** + $/compile. |
| Constrained decoding / grammar-guided CUDA | JSON **schema** on the schedule is the constraint. |
| LEGO-style basic-block split for LLM compile | Out. Scale = Amdahl `triage`, not neural compile. |
| Hybrid systems are the near-term path | Already the company. Kill switch: fallback never drilled (**C6-B**). |
