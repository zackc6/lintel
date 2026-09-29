# Risks and kill switches

These are product policy, not a risk register for a slide. Each row is a survey checkpoint or commercial problem. If the trigger hits, we **change the SKU** or **stop selling that sentence**. We do not average the conflict away.

## Architecture bets we are making

| Bet | Survey | If we are wrong |
|---|---|---|
| Application loop with classical check, lower, and fallback | Year-1 of the agentic compiler. The goal also allows later, measured component replacement | Dropping the fallback to sound more agentic. Keep last_good. |
| Compiler loop, two clocks | `check` is pinned **inside** a walk; a choreo PR changes `compiler_ver` **across** jobs | “Evolve during compilation” with no clock and no artifact name. Keep Undergo. |
| Controller loop stays gated | Procedure changes are human `policy_id` edits until partner \(F\) and one compiler change exist | Selling self-evolving control IR in year 1. A log is memory, not a promote. |
| Narrow actions (C3-B) | Cake/Argus/HintPilot beat free rewrite | Widen enums *behind* admit; keep oracles |
| Multi-DSL (C4 open) | Triton stays primary; Tile/Cake/Argus rise | Adapters; portable schema was the hedge |
| Freeze-before-serve (C5 path) | Commercial default is CI → artifact | If customers demand always-on LLM compile, charge lab-tier only |
| Oracles ≠ coding agents (C7) | DSH/Copilot are weak compiler evidence | Never drop admit to ship faster |

## Operational kill switches (year 1)

| Trigger | Action this quarter |
|---|---|
| Cannot name a **false-negative owner** for an oracle we ship | That oracle does not gate GA. It is lab-only. |
| Replay after model swap is flaky | **No GA.** Fix T3 cache keys. |
| Partner gain is only a microbench | Do not publish. Require serving \(F\) or drop the claim. |
| Fallback never exercised | Schedule a fire-drill or we are lying about C6-B. |
| Token/$ per admitted %\(F\) unknown by end of Q2 | Hiring freeze on net-new roles. |
| Home fleet is not NVIDIA and we still staff a CUDA-only printer | Swap the Q1 **sink**; do not dual-track. Choreo check still runs on CPU. |
| Sales demo uses free CUDA rewrite **or** “we compiled Choreo” without F | Pull the demo. Constrained Kernel AST + serving delta. |
| Choreo has no device sink by M2 | Live adapter falls back to degenerate Triton schedule knobs so a partner can still freeze. |
| Roadmap slide says “replace Inductor” | Delete the slide. |
| Sales/roadmap says “evolves during compilation” without naming the artifact and the clock | Pull the sentence. Compiler: pin `check` inside a walk; choreo PR + new `%k` across jobs. Controller: new `policy_id` after holdout, or a human edit. Memory: `memory_id`, same `%k`. |
| Slide claims joint search over graph, kernel, communication, and placement as the year-1 product | Delete. Year-1 searches the kernel schedule and admits on serving measurement ([SURVEY_MATCH.md](SURVEY_MATCH.md)). |
| “The controller improves itself” on a year-1 slide, or a session log presented as that result | Pull it. The module is [examples/later/controller-dev.sketch.lintel](../examples/later/controller-dev.sketch.lintel), behind the gate. |
| “Agentic compiler” sold with a model on serve, or with no check and no fallback | Pull the sentence. Year-1 still checks, lowers, measures, and freezes ([ARCHITECTURE.md](ARCHITECTURE.md)). |

## Things that look like progress and are not

- KernelBench rank without cost-to-compile.
- A Cake IR **or Choreo** prototype that only we can compile (no public sink).
- “Cake v2” / “Choreo the company” as a new kernel language (the adapter contract is already the PoC).
- Designing Lintel IR as a Meta-LLM-Compiler **LLVM IR** rewrite surface, or adding neural compile / decompile opcodes ([LLM_IR.md](LLM_IR.md)).
- A DeepSeek Harness skin with no `verify` seam.
- “15% vendor-headline” charts (survey C2 tension).
- Headcount 50 before M2 (partner A/B).
- Two live adapters before the first partner canary.
- A second GPU vendor in Q1 because the org chart asked for it.
- Intra-session `check.py` rewrite sold as compiler evolution.
- A session log, a retrieved example, or a human-edited CFG sold as controller self-improvement.
- A controller comparison that also bumps the model or `choreoir` (the gain is not attributable).
- “Not a fixed dialect” with only two allowlisted kernels and no fail corpus (process claim, not evidence).

## Year-2 doors we leave open (not commitments)

- Argus-class SMT as an `oracle` provider.
- `@cake.v0` **wrap** (their compiler) if a public tree exists or a customer funds it — not a Lintel Cake dialect. Year-1 L4 face is **Choreo** ([DATA_PLANE.md](DATA_PLANE.md), [CHOREO.md](CHOREO.md)).
- `@tirx.v0` **wrap** if a partner already lives in Apache TVM / TIRx. GPU sink; not a second live face in year 1.
- `@tilelang.ascend` **wrap** after one NVIDIA cubin and a partner who serves on NPU. Second sink, not a second AST (`tmem` ≠ `L0C`).
- DSH bundle packaging if `dsh-plugin` is the distribution ABI.
- CFG / cost-as-gate / T10 **coverage** (`%w`, policy-hash, placement) after the [PoC](POC.md) ADG walk is real ([LATER.md](LATER.md)).
- Job (c) comments on kernel PRs (never “we review llvm-project”).
- Second vendor (AMD) after NVIDIA freeze is boring.

Leaving a door open means a **seam exists**. It does not mean we staff it in Q1.
