# Product thesis

**Last updated:** 2026-08-25  
**Horizon:** year 1 lands ~2027-08 (survey Horizon A, 2027–28)

## The gap we sell

Vendors already ship **data planes** (Inductor, XLA, Triton, TensorRT-LLM, FlashInfer). They are starting to ship **fragments** of a control plane (CompileIQ ACFs, GEAK v4 e2e A/B, TRT-LLM agent skills). What nobody sells as a *vendor-neutral, money-grade product* is the joint of:

1. A **plugin agent runtime** (session log, seams, sandbox, replay) — DeepSeek Harness-class.
2. A **typed agent↔compiler contract** (**Lintel IR**: land / revert / reject + localized `gate`) — Cake-class *mechanism* on the **control** plane, not Cake IR.
3. A **typed L4 schedule** on the live adapter (year-1: Triton fields + `{where}`) — Cake-class *mechanism* on the **data** plane. Spec: [DATA_PLANE.md](DATA_PLANE.md). SLA role is **Selector**, not Translator ([LLM_IR.md](LLM_IR.md)).
4. A **layered admit + deterministic fallback** that release engineering will trust — survey T2 / C6-B / P5.
5. A **freeze-before-serve** artifact (control file / kernel / schedule) with cache keys — survey T3 / P4.

That joint is Lintel. The compiler stays classical. The agent stays a searcher. The **sold** layer is the control plane; year-1 data-plane work is the adapter contract under it, not a new compiler.

## Why not “fork Cake + fork DeepSeek Harness”

| Tempting merge | Why it is not a year-1 company |
|---|---|
| Ship Cake IR as *the* kernel language | Cake is NVIDIA Ampere–Blackwell research; no public tree; **C4** says Tile / Triton / CuTe / Argus will fragment the surface. Betting the company on one L4 IR is a 2028 kill shot. |
| Ship DeepSeek Harness as the product | DSH is a generic coding-agent runtime. Star count ≠ compiler-oracle evidence (**C7**). Customers will not put serve-path kernels on “the model looked at the diff.” |
| Fine-tune a kernel LLM and sell chat | One-shot KernelBench success stays low; fusion is hard; **C2** needs median/p50 on pinned traces + cost-to-compile. Chat is a *view*, not the SKU. |
| Replace `opt` / Inductor | Survey **rejects M3 through Horizon B**. Release eng will not buy it. |

**Take the mechanisms, not the brands.**

| Source | Mechanism we keep | What we discard |
|---|---|---|
| **Cake** | Typed agent-facing *schedule/contract*; localized pre-compile gates; harness evolves from recurring failures (new checks, not new silicon) | Cake IR as the only dialect; 80M-token clean-start as the product UX; NVIDIA lock-in |
| **DeepSeek Harness** | Everything-is-a-plugin; capability **seams** (definition / provider / consumer); append-only session log as the source of model-visible context; resume / fork / replay | Coding-agent UX as the SKU; unbounded tool-calling as the SLA path; no compiler oracles |
| **GEAK v4** (must add) | Amdahl triage on a *warm* serving stack; A/B + output parity; JS/FSM workflow not free chat | Instinct-only marketing; hero-kernel blogs as “default agent compile” |
| **Argus** (year 2 plugin, not year-1 critical path) | Tag/assert + compile-time SMT counterexamples | Claiming library-class peak on three families as C2 settlement |

## Year-1 SKU (what a customer can buy)

**Name:** Lintel Specialize (on-prem / VPC).  
**Job:** survey job **(a)** only — online/CI specialize. Jobs (b)(c)(d) are explicitly *out* of year-1 GA.

| The customer gets | The customer does *not* get |
|---|---|
| A CI job that ranks hot kernels (Amdahl / `gpu_time × headroom`) | Silent rewrite of their whole model graph |
| Agents proposing on a **constrained action space** (typed Triton **schedule record**, allowlisted; ACF-class knobs later) | Free CUDA/HIP/MLIR paste-and-pray as the default; Cake IR as the kernel language |
| Layered admit: unit/golden → numerical vs reference → shape-grid → optional serving A/B | “The LLM said it is correct” |
| Freeze: content-addressed artifact + admit record in *their* git | A SaaS that owns their kernels |
| Deterministic fallback to the last good artifact or classical path | LLM on the serve hot path |
| Replay pack: same cache key after model or compiler upgrade | A promise of unique global e2e optimum |

**Fitness \(F\) we optimize (survey §5.1.3).** Not \(\sum\) local microbench. Year-1 \(F\) is a constrained front the customer names: typically **serving tokens/s (or TTFT) · quality parity · $/compile**. Energy and cluster util are recorded, not required for GA.

**Commercial packaging (survey §5.7 checklist).**

- Contract = typed tools + structured admit traces (P1: C+B). Chat is a view.
- Memory: scratchpad ≪ skill cache ≪ **VCS artifacts** (P2).
- Topology: orchestrator + specialists + shared trace bus; **FSM/plan** on the SLA path, not unbounded tool-calling (P3/P22).
- Agents run in CI or hot-path trigger → **freeze** (P4). Interactive lab mode is opt-in and labeled as such.
- SKU = regressable artifacts + CI quota, not chat sessions (P11).

## Who pays, and for what

Primary buyer: **inference platform / compiler / kernel** leads at labs and mid-size serving companies who already burn engineer-weeks on Triton/FlashAttention-class kernels and cannot wait for the next vendor library drop.

They pay for:

1. **Time-to-admitted-kernel** on *their* traces (not KernelBench theater).
2. **Cost-to-compile** they can put in a budget (tokens + GPU-hours per % \(F\)).
3. **Audit**: who admitted what, with which oracles, under which compiler/HW pin (T9).
4. **No-LLM serve path** after freeze (P23).

Worked examples (land / revert / cost skip / cold / replay): [WHY.md](WHY.md).

They will not pay for: a better chat window, a research IR, or “we beat hipBLASLt on three shapes.”

## Scope we will not expand in year 1

- Job (b) Magellan-class LLVM heuristic evolution (**C1** is Google’s fight).
- Job (c) llvm-harness / Archer as a product (different buyer; true-fix still &lt;22%).
- Job (d) ASIC bring-up / Zomboss-class mapping (**C9** needs a second shipping vendor; out of this SKU).
- Autonomous tape-out (**C10** — survey rejects).
- Multi-month *default-path* A/B as a marketing claim (**C2** still open industry-wide; we *instrument* it, we do not claim settlement).
- Coverage items in [LATER.md](LATER.md) (`%w` as a second key, placement, multi-SKU) before the [PoC](POC.md) ADG walk is real.

## Survey commercial checklist (year-1 status)

From survey §5.7. Full P/T/C map: [SURVEY_MAP.md](SURVEY_MAP.md).

| # | Checklist | Year-1 status |
|---|---|---|
| 1 | Typed tools + admit traces | **v0 + poc schemas in-repo** |
| 2 | VCS artifacts as product truth | Freeze URI in admit record; customer git |
| 3 | Orchestrator + specialists + FSM | `lintel.fsm`; no swarms |
| 4 | CI/hot-path → freeze | Q1 internal, Q2 partner |
| 5 | Layered oracles + false-neg owners | Required field; unnamed owner ⇒ not a GA gate |
| 6 | CODEOWNERS + signed provenance + sandbox + rollback | Template now; signing Q3; fire-drill every quarter |
| 7 | Joint pins (policy + compiler + HW + model) | `pins` object |
| 8 | Eval + cost-to-compile | `fitness.usd_per_compile`; partner traces |
| 9 | A/B before “production default” | Q2 seam; marketing never says default-all |
| 10 | HITL capacity | Auto-merge only narrow enums that passed admit |
| 11 | SKU = artifacts + CI quota | Specialize SKU; not chat |
| 12 | Customer owns outputs; pluggable models + replay | GA DoD; `llm` seam |
| 13 | Multi-DSL; coverage then perf for new silicon | One live adapter; stub #2 in Q3; coverage SKU is job (d) — out |
| 14 | Tenancy / residency | Customer CI / VPC; no multi-tenant searcher |
| 15 | Support: replay packs, spend caps, oracle-miss severity | Q3–Q4 |
| 16 | Token envelope (P23) | Q2 kill switch if $/admitted %\(F\) unknown |
