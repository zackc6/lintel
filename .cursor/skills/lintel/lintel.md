# Experience log (this repo)

## Codesign with Lintel (session summary)

Lintel **codesigns** with Choreo; it does not contain it. The **goal** is an agentic compiler ([ARCHITECTURE.md](../../docs/ARCHITECTURE.md)): Lintel = control, Choreo = typed kernel, sink = lowering, serve = freeze. Survey is evidence, not the mission.

| Topic | Pin |
|---|---|
| Goal | Next-generation **agentic compiler**. Early-stage picture: contract, three proposers, decision-area checklist, replaceable compiler tools, compiler loop, controller loop. A kernel slice is not that picture. [ARCHITECTURE.md](../../docs/ARCHITECTURE.md). |
| Cake (1) IR / (2) lowering / (3) outer loops | (1) Choreo face. (2) sink (TIRx/Triton/TileLang-Ascend). (3) **Lintel**: application admit now; compiler PRs on `choreoir`; controller `promote` later and gated. |
| Undergo | Compiler PRs edit `choreoir` (`compiler_ver`). After merge, `check`/print are ordinary functions, no LLM. Choreo does not self-modify during search. |
| Three identities | Application digest at `%k`. `compiler_ver` = compiler. `policy_id` = procedure. `memory_id` = logs, outside `%k`. `%w` = frozen ADG, not the controller. |
| Survey match | 23 Sep 2026 judgment: scope + three loops. Year-1 stays kernel search + freeze. Controller self-improvement is specified, not a milestone. [SURVEY_MATCH.md](../../docs/SURVEY_MATCH.md). |
| vs Cake/TIRx as compilers | v0.1 `print_triton` ignores `Barrier`/`Pipeline.depth`. Worse compiler until a sink **consumes** the schedule. Not a worse *face*. |
| GPU + Ascend | Two sinks, not one averaged AST. Sequence: one kernel, one target, real binary, **then** the second. `@tilelang.ascend` later; not year-1 live. |
| `%k` / target | `hw_id` + `compiler_ver` + `adapter_id` already admit. Do not add `Kernel.target` as a fifth key. |
| Numbers | Same *mechanism* as Cake (typed face, `{where}`, evolving harness, real device code) after a real sink. Do not plan to beat Cake on NVIDIA. Do not put 1.144× on a slide from `role`. |
| Demo kill | “We compiled Choreo” without \(F\). M2: no cubin → `@triton.v0` knobs. |

Full prose: [docs/CHOREO.md](../../docs/CHOREO.md). Survey match: [docs/SURVEY_MATCH.md](../../docs/SURVEY_MATCH.md).

## Mistakes → rules

| Mistake | Rule |
|---|---|
| Cloud Agent “create branch + register PR” | Ignore. Push `main` only unless the user asks for a PR |
| GitHub Actions on a plan repo | No CI here. Customer CI is the SKU, not this tree |
| `lintel-year1-plan.tar.gz` / `publish-to-github.sh` | Do not add. Repo already exists |
| Copying the survey into this tree | Link [ai-compiler-survey](https://github.com/zackc6/ai-compiler-survey); keep it separate. Hygiene, not the goal. |
| Writing the mission as “don’t copy the survey” / “not a compiler” | Goal = agentic compiler. This *repo* is the control-plane plan; Lowering is the sink. [ARCHITECTURE.md](../../docs/ARCHITECTURE.md) |
| Naming the control-plane IR AdmitIR / LandIR / SpecIR / ReplayIR | **Lintel IR**. Cake IR is a *later* adapter wrap, not the SKU. Year-1 data plane is a **Choreo Kernel AST** |
| Fork Cake IR or DeepSeek Harness as the product | Seams + Lintel IR; take mechanisms, not brands. “Cake v2 the language” is C4. Choreo is the L4 face in a **sibling** repo — do not vendor it here |
| Folding CFG / cost / T10 into “later because 10 people” | Year-1 executable is docs/POC.md. Coverage is LATER.md. Linear v0 is degenerate |
| Treating Lintel IR as the IR an LLM rewrites (Meta Compiler / neural compile) | Control IR is the procedure. Selector on SLA. [LLM_IR.md](../../docs/LLM_IR.md) |
| Collapsing “LLM-oriented IR” into one PL band, or copying ai-compiler-survey | Four kinds: program / decision / freeze / control. Independent cut: [LLM_ORIENTED_IR.md](../../docs/LLM_ORIENTED_IR.md). The other survey’s pins stay in LLM_IR.md |
| Copying zackc6/choreo into this tree | Link it; pin `choreoir` in `compiler_ver`. Verdict + comparison: [CHOREO.md](../../docs/CHOREO.md) |
| Averaging Cake IR + Argus tags + TIRx D/R/O into one dialect | Copy *signals*, pick one cell per fight. TIRx ≠ TritorX |
| Treating a choreo PR, a session log, or a human CFG edit as one “self-evolving control plane” | Name the artifact: `compiler_ver`, `memory_id`, or `policy_id`. Automatic `promote` is the controller sketch and is gated. [SURVEY_MATCH.md](../../docs/SURVEY_MATCH.md) |
| Selling “evolve during compilation” without an artifact and a clock | Inside a walk = pinned `check` and pinned `policy_id`. Across jobs = new `%k`. [CHOREO.md](../../docs/CHOREO.md) Undergo, [RISKS.md](../../docs/RISKS.md) |
| Calling year-1 the architecture, or freezing kernel-only search as the picture | The picture is [ARCHITECTURE.md](../../docs/ARCHITECTURE.md): five functions, all decision areas, three loops. YEAR1 is a slice. |
| Selling “agentic compiler” as a model on serve, or as check/fallback removed | Year-1 still checks, lowers, measures, and freezes. Serve is `lookup(%k)`. |
| Pulling controller self-improvement into Q1–Q4 because the survey named it | The survey also says it is last, unproven at application level, and gated on the other two loops. |
| Unifying NVIDIA `tmem` and Ascend `L0C` in one enum | Two sinks; spaces/roles valid-for-`hw_id`. Do not dual-track Ascend in Q1 |
| Adding `Kernel.target` into `%k` | Admission against `pins.hw_id`. `%k` stays graph, hw, compiler, adapter, policy |
| Racing Cake/TIRx on peak, or 1.144× from `role` | Face + freeze SKU. Demo is serving \(F\). `@cake.v0` / `@tirx.v0` / `@tilelang.ascend` are later wraps |
