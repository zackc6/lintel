# Year-1 plan (doable, commercial)

**Clock:** 12 months from kickoff (~2026-09 → 2027-08).  
**Staffing:** designed for **10**, with a clean scale-up to **25** and **50**. Do not hire 50 on day one.

## Definition of done (commercial, not demo)

Year 1 is **done** only if all of the following are true. Missing any one means we shipped a lab.

1. **Two design partners** (or one production deploy + one paid pilot) running Lintel in *their* CI on *their* traces.
2. **Frozen artifacts** they own in their VCS; serve path has **zero** LLM calls.
3. **Layered admit** with named false-negative owners; classical or last-good **fallback** exercised in a fire drill.
4. **Replay**: same cache key after a model swap produces the same admit decision or a hard fail (never a silent new kernel).
5. **Reported \(F\)** on partner traces: serving metric + quality parity + **$/compile** (tokens + GPU-hours). No hero-kernel press release as the SKU story.
6. **Support**: replay pack, spend cap, severity for oracle miss (survey §5.7 checklist #15).
7. **Contract**: customer owns outputs; telemetry opt-in (P13).

**Not** year-1 done: KernelBench rank, a public Cake-class IR, an AMD port, “agents are the default compiler.”

## What 10 / 25 / 50 people actually do

Hire for **seams**, not for “more kernel researchers.”

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

**Rule.** A 10-person team ships **one** GPU family, **one** agent surface, **one** serving engine. Default: NVIDIA + Triton + (SGLang *xor* vLLM, pick in week 1). If the home fleet is not NVIDIA, swap the adapter — do not dual-track. A 25-person team adds the second surface *or* the second engine, not both in the same quarter. A 50-person team is year-1 only if Q1 already exited with the core 10; otherwise it is year 2.

## Hiring order (the 10)

Do not hire “kernel researchers” first. Hire so Q1 can freeze one artifact.

| When | Role | Count | Why this week |
|---|---|---|---|
| Week 0 | Founder-eng | 1 | Pins week-1 decisions; owns kill switches |
| Week 0–2 | Control-plane | 2 | Schema, session log, FSM, seams |
| Week 2–6 | Adapter + localized gates | 2 | Triton (or home-fleet equivalent) |
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
| 1 | Pins above; admit schema freeze (already v0 in this repo); sqlite session log | `lintel-validate` in CI |
| 2–4 | FSM + seams + sandbox that can run generated Triton | One propose → gate → fallback path on a toy kernel |
| 5–8 | Triton adapter + golden + numerical oracles on a pinned shape grid | First **internal** freeze (faster on the grid or documented miss) |
| 9–10 | Cache key + replay after an intentional model-id swap | Replay hard-fails on silent decision change |
| 11–12 | Fallback fire-drill; solutions has a named partner candidate | M1: freeze + fallback + replayable log |

**Do not build in Q1:** web IDE, multi-agent swarms, Cake IR, SMT, AMD-as-second-live-adapter, serving A/B (that is Q2).

## Quarter plan (10-person critical path)

### Q1 — Contract and one closed loop (months 0–3)

**Build**

- Admit-record schema v0 is **already in this repo**; Q1 implements the session store + FSM on top of it.
- Seams: `llm`, `tools`, `sandbox`, `adapter` (Triton default; home-fleet swap is week 1), `oracle={golden,numerical}`.
- FSM: triage (manual allowlist of ops) → propose → gate → measure → freeze | fallback.
- One internal model, one hot op family (attention **or** GEMM — pick by partner, not by paper).

**Do not build**

- Web IDE. Multi-agent swarms. Cake IR. SMT. A *second* GPU vendor.

**Exit**

- Internal CI produces a frozen Triton artifact that is numerically admitted and **faster on a pinned shape grid**, with a replayable log. Fallback path demonstrated.

### Q2 — Serving \(F\) and first partner (months 3–6)

**Build**

- Amdahl triage on a **warm** server (GEAK v4 pattern: do not burn search on cold kernels).
- Serving seam: shadow or A/B + **output parity** on the chosen engine.
- Localized reject strings (Cake-class diagnostics) on the Triton adapter.
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
- Year-2 RFC: Argus-class SMT oracle plugin; second serving engine; optional DSH-bundle packaging.

**Exit (GA)**

- Commercial definition of done above.
- Written **no** list for year 2 so sales cannot sell job (d) or M3.

## 25- and 50-person overlays (same year, only if funded)

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

| Line | 10-person year | Notes |
|---|---|---|
| People (fully loaded) | $2.5–4.5M | Mix of regions; 50 people is $12–20M and is not the default |
| Partner / lab GPU | $0.4–1.2M | Prefer customer GPU for the partner loop |
| Tokens + extra model APIs | **cap $150–400k** | OpEx per admitted %\(F\); not a research slush |
| **Total to GA** | **~$3.5–6M** | If Q2 cannot name $/admitted %\(F\), **stop hiring** |

Overnight/CI specialize is the default. Interactive search is a labeled lab tier (P18). That is the survey P23 envelope, not a vibe.

## Milestone table (falsifiable)

| When | Milestone | Survey hook |
|---|---|---|
| M1 (Q1) | Closed loop on one op, freeze + fallback | T1/T2 |
| M2 (Q2) | Warm-server A/B + parity on partner traces | T6, C2 *instrumented* |
| M3 (Q3) | Two artifacts in partner VCS; replay after model swap | T3, C5 *path* |
| M4 (Q4) | GA SKU; customer-owned outputs; support runbooks | P11–P15 |
| Kill | Any quarter ends without fallback fire-drill | C6-B |

## What we will say in the Q4 launch post

Honest: “Hot-path specialize with admit and freeze, on Triton and [engine], for teams that already own their serving stack.”  
Forbidden: “We replace your compiler.” “Agents are now the default.” “Faster than cuBLAS on everything.”
