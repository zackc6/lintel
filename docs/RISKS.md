# Risks and kill switches

These are product policy, not a risk register for a slide. Each row is a survey checkpoint or commercial problem. If the trigger hits, we **change the SKU** or **stop selling that sentence**. We do not average the conflict away.

## Architecture bets we are making

| Bet | Survey | If we are wrong |
|---|---|---|
| Hybrid control plane (C6-B) | Agents search; compilers lower/admit/fallback. The **goal** is this loop as an agentic compiler. | We are in the wrong business. Do not pivot to survey M3 (LLM-as-compiler). |
| Two-clock T5 (Cake flavor) | Compiler evolves **across** jobs; `check` is pinned **inside** a walk | If “evolve during compilation” is read as mid-walk self-modify, we look like C6-A. Keep Undergo. |
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
| Sales/roadmap says “compiler evolves during compilation” without two clocks | Pull the sentence. Say: pin `check` inside a walk; choreo PR + new `%k` across jobs. Mid-walk `check.py` rewrite stays **forbidden** ([SURVEY_MATCH.md](SURVEY_MATCH.md)). |
| Slide claims “e2e-optimal-seeking” / joint L1–L7 search | Delete. Year-1 is M1-lite: search L4, admit L6. |
| “Agentic compiler” sold without classical check/lower, or with a model on serve | Pull the sentence. Goal is C6-B. M3 stays out ([ARCHITECTURE.md](ARCHITECTURE.md)). |

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
- Intra-session `check.py` rewrite sold as T5 (that is M3-adjacent).
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
