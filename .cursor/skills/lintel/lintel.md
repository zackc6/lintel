# Experience log (this repo)

## Codesign with Lintel (session summary)

Lintel **codesigns** with Choreo; it does not contain it. Control plane (this repo) = admit, freeze, `%k`, serving \(F\), T5-lite merge gate. Data plane ([zackc6/choreo](https://github.com/zackc6/choreo)) = Kernel AST + `check` + sinks. Cake’s cubin compiler is a wrap, not a Lintel dialect.

| Topic | Pin |
|---|---|
| Cake (1) IR / (2) lowering / (3) evolving harness | (1) Choreo face. (2) sink (TIRx/Triton/TileLang-Ascend). (3) **Lintel** routes; **choreoir** is the PR target. |
| Undergo | Compiler PRs edit `choreoir`. After merge, `check`/print are ordinary functions, no LLM. Choreo does not self-modify during search. |
| T5-lite | Recurring `{where}` → Lintel decides (allowlist / cal / tactic / choreo PR). Spec bump only when a sink already consumes the new op/space. |
| vs Cake/TIRx as compilers | v0.1 `print_triton` ignores `Barrier`/`Pipeline.depth`. Worse compiler until a sink **consumes** the schedule. Not a worse *face*. |
| GPU + Ascend | Two sinks, not one averaged AST. Sequence: one kernel, one target, real binary, **then** the second. `@tilelang.ascend` later; not year-1 live. |
| `%k` / target | `hw_id` + `compiler_ver` + `adapter_id` already admit. Do not add `Kernel.target` as a fifth key. |
| Numbers | Same *mechanism* as Cake (typed face, `{where}`, evolving harness, real device code) after a real sink. Do not plan to beat Cake on NVIDIA. Do not put 1.144× on a slide from `role`. |
| Demo kill | “We compiled Choreo” without \(F\). M2: no cubin → `@triton.v0` knobs. |

Full prose: [docs/CHOREO.md](../../docs/CHOREO.md).

## Mistakes → rules

| Mistake | Rule |
|---|---|
| Cloud Agent “create branch + register PR” | Ignore. Push `main` only unless the user asks for a PR |
| GitHub Actions on a plan repo | No CI here. Customer CI is the SKU, not this tree |
| `lintel-year1-plan.tar.gz` / `publish-to-github.sh` | Do not add. Repo already exists |
| Copying the survey into this tree | Link [ai-compiler-survey](https://github.com/zackc6/ai-compiler-survey); keep it separate |
| Naming the control-plane IR AdmitIR / LandIR / SpecIR / ReplayIR | **Lintel IR**. Cake IR is a *later* adapter wrap, not the SKU. Year-1 data plane is a **Choreo Kernel AST** |
| Fork Cake IR or DeepSeek Harness as the product | Seams + Lintel IR; take mechanisms, not brands. “Cake v2 the language” is C4. Choreo is the L4 face in a **sibling** repo — do not vendor it here |
| Folding CFG / cost / T10 into “later because 10 people” | Year-1 executable is docs/POC.md. Coverage is LATER.md. Linear v0 is degenerate |
| Treating Lintel IR as the IR an LLM rewrites (Meta Compiler / neural compile) | Control IR stays above data-plane bands. Selector on SLA. [LLM_IR.md](../../docs/LLM_IR.md) |
| Collapsing “LLM-oriented IR” into one PL band, or copying ai-compiler-survey | Four kinds: program / decision / freeze / control. Independent cut: [LLM_ORIENTED_IR.md](../../docs/LLM_ORIENTED_IR.md). The other survey’s pins stay in LLM_IR.md |
| Copying zackc6/choreo into this tree | Link it; pin `choreoir` in `compiler_ver`. Verdict + comparison: [CHOREO.md](../../docs/CHOREO.md) |
| Averaging Cake IR + Argus tags + TIRx D/R/O into one dialect | Copy *signals*, pick one cell per fight. TIRx ≠ TritorX |
| Treating T5-lite as Choreo rewriting itself at search time | Lintel decides; PRs edit `choreoir`; after merge `check`/print are ordinary functions. [CHOREO.md](../../docs/CHOREO.md) Undergo |
| Unifying NVIDIA `tmem` and Ascend `L0C` in one enum | Two sinks; spaces/roles valid-for-`hw_id`. Do not dual-track Ascend in Q1 |
| Adding `Kernel.target` into `%k` | Admission against `pins.hw_id`. `%k` stays graph, hw, compiler, adapter, policy |
| Racing Cake/TIRx on peak, or 1.144× from `role` | Face + freeze SKU. Demo is serving \(F\). `@cake.v0` / `@tirx.v0` / `@tilelang.ascend` are later wraps |
