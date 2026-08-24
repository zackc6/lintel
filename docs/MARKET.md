# Business value and competition (1–3 years)

## The value in cash language

Inference labs already pay three bills Lintel is meant to cut. Year-1 sales conversations should use these, not “AI compiler” as a slogan.

| Bill today | What Lintel changes | How we prove it in year 1 |
|---|---|---|
| **Kernel engineer-weeks** on each model drop / HW SKU | Amdahl-ranked specialize + freeze; humans review admit records, not 200 raw diffs | Time-to-admitted-kernel on partner traces vs their last quarter |
| **$/token** (or TTFT / tokens/s) on hot serving paths | Search under product \(F\), not kernel microbench | Serving A/B + parity (GEAK v4-class), cost-to-compile beside the gain |
| **Release risk** from silent bad codegen | Layered admit + last-good/classical fallback; no LLM at serve | Fire-drill + signed admit records |
| **Vendor lock-in tax** | Seams: Triton now, Tile/HIP/Cake-class later without a rewrite | Empty second-adapter stub in Q3 is the proof |

**What we do not claim as year-1 value.** Median default-path compile for *all* builds (**C2** open industry-wide). Beating vendor libraries on every family (Argus/Cake are *color*, not a SKU promise). Replacing NVIDIA/AMD compiler teams.

**Pricing sketch (to stress-test the SKU, not a quote).** Charge for **CI quota + admit/freeze platform + support**, optionally GPU-hours if we host. Do not charge primarily per chat turn. If the only meter is tokens, we have packaged a coding agent (C7) and will lose to DeepSeek Harness + Claude Code on price.

## Where the money is in 1 / 2 / 3 years

Survey Horizon A is 2027–28; Horizon B ~2029–31. Lintel year 1 ≈ late Horizon A entry. Years 2–3 are “control plane becomes how orgs survive O(ops × devices × generations)” — still hybrid, still not M3.

| Window | What customers will pay for | Lintel offer | What we refuse |
|---|---|---|---|
| **Year 1 (now→~2027-08)** | Hot-path specialize they can freeze and audit | Lintel Specialize (Triton + one engine) | Default-all, new mega-IR |
| **Year 2 (~2027-09→2028-08)** | Second surface (Tile/HIP) + on-prem + reported p50 on *their* fleet | Adapter #2; optional SMT/oracle plugin; DSH-bundle if that ABI wins | Claiming C2 industry settlement |
| **Year 3 (~2028-09→2029-08)** | Compiled control plane: workflow freeze, placement, multi-SKU | T10 productization (ADG/FSM configs as artifacts); still classical lowering | Autonomous tape-out; LLM-as-`opt` |

If year 1 does not produce frozen customer-owned artifacts, year 2–3 stories are fiction.

## Competitive map

### Incumbents who can crush a confused startup

These are **not** “we are better at CUDA than NVIDIA.” Compete on **cross-tool admit/freeze** and **customer-owned artifacts**, or do not compete.

| Player | What they are | 1-year threat | 3-year threat | Lintel wedge |
|---|---|---|---|---|
| **NVIDIA CompileIQ + Tile + TRT-LLM agents + Cake (research)** | Best funded control-plane *on NVIDIA* | High if we only sell “Triton autotune for CUDA” | Existential on NVIDIA-only SKU | Vendor-neutral admit record + freeze + serving \(F\); Cake-class IR as a *plugin* if they open it |
| **AMD GEAK v4** | Only named vendor **warm A/B** loop | Medium (Instinct shops) | High on AMD-first buyers | Same wedge; GEAK workflow as an `adapter`/`serving` provider, not an enemy |
| **Meta TritorX / KernelEvolve / Helion** | Internal bring-up + DSL | Low externally (little public SKU) | High if they productize | We are not job (d) in year 1 |
| **PyTorch Inductor / Triton / Helion** | Default data plane | They stay the host | They stay the host | We attach; we do not replace |
| **FlashInfer + FlashInfer-Bench** | Kernel library + serving-trace ladder | Partner, not enemy | Standard oracle rung | Consume `apply()` as an oracle plugin |
| **Google Magellan / MLGO / AlphaEvolve Cloud** | Offline heuristics + cloud algo search | Different job (b) / different buyer | Could eat “evolve any code” budget | Stay job (a) specialize; do not become AlphaEvolve |

### Agent runtimes (easy to confuse with us — do not)

| Player | Why people mention them | Why they are not the same SKU |
|---|---|---|
| **DeepSeek Harness** | Plugin kernel, session log, huge attention | No compiler oracles; C7. We may **mount on** it later. |
| **Claude Code / Cursor / Copilot** | Engineers already live there | SCM UX. Miscompile risk. We sell admit/freeze, not tab-complete. |
| **Auto / FlowCompile / AgentFlow** | Workflow compile / ADG / freeze spans | Substrate ideas for year 2–3 T10; not a kernel admit product today. |

### Kernel-agent specialists (direct feature overlap)

| Player | Overlap | How we differ in 12 months |
|---|---|---|
| **AutoKernel, Kernel Forge / KForge, KernelBlaster, CuTeGen, KernelAgent** | Search loops, some Amdahl, some DSLs | Most are papers/tools. We sell **replay + fallback + serving \(F\) + customer-owned freeze** as the product. |
| **KernelBench solvers** | Leaderboard theater | We refuse that as the GA metric. |
| **Argus** | Peak on selected MI300X families via SMT | Year-2 oracle plugin. Do not claim 99–104% of assembly as our year-1 SKU. |

### Who beats us

| Failure mode | Who wins | Prevention |
|---|---|---|
| We become “open Cake” | NVIDIA (distribution + HW) | Seams; Cake-class is optional |
| We become “compiler Claude” | DSH / Cursor / Anthropic | C7 discipline; oracles in the merge path |
| We become “NVIDIA-only autotuner” | CompileIQ | Second-adapter stub + admit schema |
| We claim default-path agents | Reality (C2) + customer IR | Honest SKU language |
| We take 50 people into job (d) | Meta internal tools | Year-1 job (a) only |

## Positioning sentence

> Lintel is the **admit-and-freeze control plane** for teams that already have a compiler and a serving stack. Agents propose; compilers lower; oracles decide; git owns the artifact.

If a slide cannot say that sentence, it is selling the wrong company.

## Design-partner profile (year 1)

**Yes:** serving team with ≥1 full-time kernel/compiler person, SGLang or vLLM in production, NVIDIA fleet, a written SLO, willingness to put artifacts in git.

**No:** “we want an agent to write our compiler”; pre-product model labs with no serving stack; companies whose only metric is KernelBench `fast_p`.

Two such partners are enough to GA. Ten logos with chat pilots are not.
