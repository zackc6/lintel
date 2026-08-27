# Year-1 plan (doable, commercial)

**Goal:** ship a next-generation agentic compiler as a product: Lintel walks specialize, Choreo is the typed kernel, a sink emits the binary, serve is freeze ([ARCHITECTURE.md](ARCHITECTURE.md)).

**Clock:** 12 months from kickoff (~2026-09 → 2027-08).  
**IR:** Build the [PoC](POC.md) first — CFG + cost-as-gate + compile-to-ADG on one region, **and** a Choreo Kernel AST + `adapter_gate` `{where: W|L|S|V}` ([DATA_PLANE.md](DATA_PLANE.md), [CHOREO.md](CHOREO.md)). Linear `lintel-ir.v0` and Triton `num_warps` knobs are degenerate, not the Q1 target. Staffing does not cap that set.

## Definition of done (commercial, not demo)

Year 1 is **done** only if all of the following are true. Missing any one means we shipped a lab.

1. **Two design partners** (or one production deploy + one paid pilot) running Lintel in *their* CI on *their* traces.
2. **Frozen artifacts** they own in their VCS; serve path has **zero** LLM calls.
3. **Layered admit** with named false-negative owners; classical or last-good **fallback** exercised in a fire drill.
4. **Replay**: same cache key after a model swap produces the same admit decision or a hard fail (never a silent new kernel).
5. **Reported \(F\)** on partner traces: serving metric + quality parity + **$/compile** (tokens + GPU-hours). No hero-kernel press release as the SKU story.
6. **Support**: replay pack, spend cap, severity for oracle miss (survey §5.7 checklist #15).
7. **Contract**: customer owns outputs; telemetry opt-in (P13).

**Not** year-1 done: KernelBench rank, selling Choreo without a device sink, an AMD port, “agents are the default compiler,” linear-only interpret with no CFG/cost/ADG, opaque-string autotune with no `{where}`, a Lintel **IR-LLM** pretrained on LLVM IR.

## What 10 / 25 / 50 people actually do

Hire for **seams** and for the [PoC](POC.md) interpreter (ADG walk, cost, compile). Headcount tables below are overlays, not a reason to ship a linear script first.

| Role | 10 (GA-minimum) | 25 (two surfaces) | 50 (enterprise + 2nd vendor) |
|---|---|---|---|
| Control-plane / runtime (session, FSM, seams) | 2 | 4 | 6 |
| Compiler adapters + localized gates | 2 | 4 | 7 |
| Oracles + serving A/B | 2 | 4 | 6 |
| Artifact store, CI, replay, tenancy | 1 | 3 | 6 |
| Product + solutions (design partners) | 2 | 4 | 8 |
| Eng manager / founder-eng | 1 | 2 | 3 |
| Security / CODEOWNERS / on-prem | 0 (shared) | 2 | 5 |
| Second adapter (Tile or HIP) + AMD | 0 (stub only) | 2 | 6 |
| Job (c) lite / support | 0 | 0 | 3 |
| **Total** | **10** | **25** | **50** |

**Width (product cut, not a headcount cap).** Year 1 ships **one** GPU family, **one** agent surface, **one** serving engine. Default: NVIDIA + **Choreo** face + one GPU **sink** that consumes the schedule (not a `print_triton` stencil) + (SGLang *xor* vLLM, pick in week 1). If the home fleet is not NVIDIA, swap the **sink** — do not dual-track the face. Ascend (`@tilelang.ascend`) waits until one NVIDIA cubin has landed.

## Hiring order (the 10)

Do not hire “kernel researchers” first. Hire so Q1 can freeze one artifact.

| When | Role | Count | Why this week |
|---|---|---|---|
| Week 0 | Founder-eng | 1 | Pins week-1 decisions; owns kill switches |
| Week 0–2 | Control-plane | 2 | PoC schema, ADG compile, session log, seams |
| Week 2–6 | Adapter + localized gates | 2 | Choreo check + a GPU **sink** that consumes `Pipeline.depth` (or `@triton.v0` knobs if M2 kill) |
| Week 2–8 | Oracles | 2 | Golden + numerical first; serving A/B from Q2 |
| Week 4–8 | Artifact / CI / replay | 1 | Cache keys, partner replay pack |
| Week 1–12 | Product + solutions | 2 | Partners from week 1 — not after the demo |

If you only have **six** people: 1 founder-eng, 2 control-plane, 1 adapter, 1 oracle, 1 solutions. Delay the second adapter engineer and the second oracle until after M1.

## Week-1 decisions (write them down)

1. **Home GPU family** — NVIDIA default; swap if the team already serves on something else.
2. **Serving engine** — SGLang **or** vLLM, not both.
3. **Op family** — attention **or** GEMM; prefer the first partner’s hot path.
4. **SKU vs lab** — CLI `--mode=sku|lab` exists on day one. Lab is not the demo.

## Q1 week-by-week (months 0–3)

| Weeks | Build | Exit this slice |
|---|---|---|
| 1 | Pins above; [PoC](POC.md) schema + Acme CFG in-repo; sqlite session log | `lintel-ir.poc` frozen |
| 2–4 | Compile module → ADG; interpret ADG; sandbox runs `choreoir.check` on allowlisted Kernels | Walk `^try0` land **and** a revert edge on a toy kernel; one `{where: L}` → `^try1` |
| 5–8 | Choreo adapter: two allowlisted Kernels; `adapter_gate` `{where: W\|L\|S\|V}`; golden + numerical **if** printer exists; `cost` uses `last_good.F` | First **internal** freeze through the PoC CFG; Finding JSON in the session log |
| 9–10 | Cache key + replay after an intentional model-id swap; ADG digest pinned | Replay hard-fails on silent decision or ADG change |
| 11–12 | Fallback fire-drill; solutions has a named partner candidate | M1: freeze + fallback + replayable log + ADG + Kernel AST in the admit record |

**Do not build in Q1:** web IDE, multi-agent swarms, Cake IR as the SKU, SMT in lintel, AMD-as-second-live-adapter, a second live GPU vendor, an IR-LLM / neural compile path, vendoring `choreoir/` here. **Do** build CFG, cost, ADG compile, and the Choreo adapter_gate ([POC.md](POC.md), [DATA_PLANE.md](DATA_PLANE.md), [CHOREO.md](CHOREO.md)). Serving A/B nodes in the CFG may stub until Q2 / printer — do not stub `cond`, `cost`, or `adapter_gate`.

## Quarter plan (critical path)

### Q1 — Contract and one closed loop (months 0–3)

**Build**

- Admit-record schema v0 is **already in this repo**; Q1 implements session store + **PoC ADG interpreter** on top of it ([POC.md](POC.md)).
- Seams: `llm`, `tools`, `sandbox`, `adapter` (**Choreo** Kernel AST + `choreoir.check`; GPU sink must consume the schedule; home-fleet sink swap is week 1), `oracle={golden,numerical}`; `cost` is a control op, not a new seam. `adapter_gate` is the adapter seam, not a new IR.
- Control FSM = walk the Acme CFG (blocks + `cond`), not a single linear block.
- One internal model, one hot op family (attention **or** GEMM — pick by partner, not by paper).

**Do not build**

- Web IDE. Multi-agent swarms. Cake IR as the SKU. SMT in lintel. A *second* GPU vendor. Dual live L4. IR-LLM pretrain / neural compile. Vendoring `choreoir/` here.

**Exit**

- Internal CI compiles the PoC module to an ADG, walks it, and produces a frozen artifact that is numerically admitted **or** a documented revert edge **or** a documented `{where: L}` adapter fail, with a replayable log. Kernel AST is in the admit record. Fallback path demonstrated. Cubin/printer may wait M2.

### Q2 — Serving \(F\) and first partner (months 3–6)

**Build**

- Amdahl triage on a **warm** server (GEAK v4 pattern: do not burn search on cold kernels).
- Serving seam: shadow or A/B + **output parity** on the chosen engine.
- T5-lite: Lintel routes recurring `{where}` into a **choreo PR** (new `check` rule or a printer that consumes the schedule), human-merged, `compiler_ver` bumped ([CHOREO.md](CHOREO.md) Undergo).
- Artifact cache keys + partner-facing replay pack.

**Staffing note.** If you can hire toward 15, the extra five go to solutions + serving oracles, not a second IR.

**Exit**

- Design partner #1: Lintel job in their CI; they merge at least one frozen artifact to a non-prod serving canary. Written \(F\) and $/compile.

### Q3 — Productize (months 6–9)

**Build**

- Signed admit records, CODEOWNERS template, sandbox policy (T9 minimum).
- Flaky-speedup policy (HW noise); spend caps (P23).
- Second adapter as a **stub that compiles and is tested empty** (Tile *or* HIP) — proves seams, does not promise perf.
- Lab mode vs SKU mode clearly split in the UI/CLI (DSH Creator ≠ GA).

**Exit**

- Design partner #2 *or* partner #1 in production on a **named** hot path (not default-all).
- Sales SKU sheet: on-prem/VPC, CI quota, support tiers.
- Security review of generated-code path.

### Q4 — GA (months 9–12)

**Build**

- GA hardening: install, pins (compiler + HW + policy + model), runbooks, canary rollback.
- Public-facing *method* (how we measure \(F\)), not a fake p50 industry claim.
- Year-2 RFC: Argus-class SMT oracle plugin; second serving engine; optional DSH-bundle packaging. Coverage after PoC: [LATER.md](LATER.md) (`%w`, policy-hash, more edges).

**Exit (GA)**

- Commercial definition of done above.
- Written **no** list for year 2 so sales cannot sell job (d) or survey M3 (LLM-as-compiler). YEAR1 M3 (Q3 replay) is in-scope.

**25 / 50 overlays** (same year, only if funded — not an IR gate)

**25.** Parallel track from Q2: second `adapter` *or* second `serving` provider; dedicated on-prem; two more solutions engineers. Still one GPU vendor.

**50.** From Q2: NVIDIA + AMD (HIP/GEAK-class workflow as an adapter, not a rewrite); enterprise SSO/air-gap; a small job (c) “oracle comment on kernel PRs” — still not llvm-project replacement. Only do this if Q1 exit already happened with the core 10. A 50-person team that starts on Cake IR + a coding-agent UI will miss GA.

## Partner GTM (starts week 1)

Commercial DoD needs two design partners. Q1 is internal technically, **not** commercially idle.

| Quarter | Solutions work |
|---|---|
| Q1 | 10 conversations → 3 serious → 1 written pilot MoU (their traces, their CI, NVIDIA-or-home fleet, SGLang or vLLM already in prod) |
| Q2 | Partner #1: Lintel job in their CI; one frozen artifact on a non-prod canary |
| Q3 | Partner #2 **or** partner #1 production on a *named* hot path |
| Q4 | Support runbooks; SKU sheet; no extra logos as a substitute for freeze |

**Yes profile.** ≥1 kernel/compiler FTE, written SLO, artifacts allowed in git. **No.** “Write our compiler”; KernelBench-only labs; no serving stack.

## Budget shape (order-of-magnitude, USD, 2026 — not a quote)

| Line | Year-1 GA | Notes |
|---|---|---|
| People (fully loaded) | $2.5–4.5M | Mix of regions; 50 people is $12–20M and is not the default |
| Partner / lab GPU | $0.4–1.2M | Prefer customer GPU for the partner loop |
| Tokens + extra model APIs | **cap $150–400k** | OpEx per admitted %\(F\); not a research slush |
| **Total to GA** | **~$3.5–6M** | If Q2 cannot name $/admitted %\(F\), **stop hiring** |

Overnight/CI specialize is the default. Interactive search is a labeled lab tier (P18). That is the survey P23 envelope, not a vibe.

## Milestone table (falsifiable)

| When | Milestone | Survey hook |
|---|---|---|
| M1 (Q1) | PoC ADG walk on one op, freeze + fallback + Choreo `{where}` | T1/T2/T10-lite |
| M2 (Q2) | Warm-server A/B + parity on partner traces | T6, C2 *instrumented* |
| M3 (Q3) | Two artifacts in partner VCS; replay after model swap | T3, C5 *path* |
| M4 (Q4) | GA SKU; customer-owned outputs; support runbooks | P11–P15 |
| Kill | Any quarter ends without fallback fire-drill | C6-B |

## What we will say in the Q4 launch post

Honest: “Hot-path specialize with admit and freeze, on Choreo→Triton and [engine], for teams that already own their serving stack.”  
Forbidden: “We replace your compiler.” “Agents are now the default.” “Faster than cuBLAS on everything.”
