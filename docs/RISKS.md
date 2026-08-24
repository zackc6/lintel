# Risks and kill switches

These are product policy, not a risk register for a slide. Each row is a survey checkpoint or commercial problem. If the trigger hits, we **change the SKU** or **stop selling that sentence**. We do not average the conflict away.

## Architecture bets we are making

| Bet | Survey | If we are wrong |
|---|---|---|
| Hybrid control plane (C6-B) | Agents search; compilers lower/admit/fallback | We are in the wrong business. Do not pivot to survey M3 (LLM-as-compiler). |
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
| Home fleet is not NVIDIA and we still staff Cake IR | Swap the Q1 adapter; do not dual-track. |
| Sales demo uses free CUDA rewrite as the happy path | Pull the demo. Constrained actions only. |
| Roadmap slide says “replace Inductor” | Delete the slide. |

## Things that look like progress and are not

- KernelBench rank without cost-to-compile.
- A Cake IR prototype that only we can compile.
- A DeepSeek Harness skin with no `verify` seam.
- “15% vendor-headline” charts (survey C2 tension).
- Headcount 50 before M2 (partner A/B).
- Two live adapters before the first partner canary.
- A second GPU vendor in Q1 because the org chart asked for it.

## Year-2 doors we leave open (not commitments)

- Argus-class SMT as an `oracle` provider.
- Cake-class schedule IR as an `adapter` if a tree exists or a customer funds it.
- DSH bundle packaging if `dsh-plugin` is the distribution ABI.
- CFG / cost-as-gate / T10 compile-the-plan after year-1 DoD ([LATER.md](LATER.md)).
- Job (c) comments on kernel PRs (never “we review llvm-project”).
- Second vendor (AMD) after NVIDIA freeze is boring.

Leaving a door open means a **seam exists**. It does not mean we staff it in Q1.
