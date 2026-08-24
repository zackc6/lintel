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
6. **Support**: replay pack, spend cap, severity for oracle miss (survey P15).
7. **Contract**: customer owns outputs; telemetry opt-in (P12).

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

**Rule.** A 10-person team ships **one** GPU family (NVIDIA), **one** agent surface (Triton), **one** serving engine (pick SGLang *or* vLLM in week 1). A 25-person team adds the second surface *or* the second engine, not both in the same quarter. A 50-person team is year-1 only if you already have pipeline and partners; otherwise it is year 2.

## Quarter plan (10-person critical path)

### Q1 — Contract and one closed loop (months 0–3)

**Build**

- Admit-record schema v0 + session log (append-only; fork/resume).
- Seams: `llm`, `tools`, `sandbox`, `adapter=triton`, `oracle={golden,numerical}`.
- FSM: triage (manual allowlist of ops) → propose → gate → measure → freeze | fallback.
- One internal model, one hot op family (attention **or** GEMM — pick by partner, not by paper).

**Do not build**

- Web IDE. Multi-agent swarms. Cake IR. SMT. AMD.

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

## Budget shape (order-of-magnitude, not a finance model)

For a 10-person year: most cash is **people + partner GPU**. Token spend must be treated as **OpEx per admitted %\(F\)**, with a published cap. Overnight/CI specialize is the default; interactive search is a labeled lab tier (P18).

If tokens per admitted percent cannot be shown by end of Q2, **stop hiring** and fix Amdahl cut + freeze. That is the survey P23 envelope, not a vibe.

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
