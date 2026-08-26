# LLM-oriented IRs (independent survey)

This is **not** a SKU, and it is **not** copied from [ai-compiler-survey](https://github.com/zackc6/ai-compiler-survey). That other tree maps *The New Compiler Stack* ([arXiv:2601.02045](https://arxiv.org/abs/2601.02045)) onto Lintel pins in [LLM_IR.md](LLM_IR.md). Their NL / PL / LLVM-IR cut is too coarse: CUDA, Triton, Cake IR, a 170-line knob DSL, and a JSON freeze schema are not one “PL.”

This note is an independent cut from **primary papers**: what the model is asked to emit or consume, who owns legality, and what a reject looks like. Year-1 product choices stay in [DATA_PLANE.md](DATA_PLANE.md) / [LINTEL_IR.md](LINTEL_IR.md). Do not fork Cake IR, staff dual live L4, or start an LLVM-IR rewrite product because a paper exists.

---

## Four kinds (do not mix)

“LLM-oriented IR” is four different objects. Mixing them is how a control-plane company accidentally becomes a kernel language.

| Kind | What the model emits / sees | Who lowers | Fail looks like | Examples |
|---|---|---|---|---|
| **1. Agent-authored program** | A full kernel or schedule the compiler then lowers | Compiler / backend | Compiler error, hang, or a traceback | Cake IR, Triton Python, CUDA, HIP, LLVM IR, Argus tile DSL |
| **2. Agent-authored decision surface** | Typed knobs; compiler completes legality | Compiler fills and legalizes | Named field / bucket reject | Zomboss mapping intent, µCUTLASS spec, HintPilot pragmas, CompileIQ ACF, Triton `num_warps` / `block_*`, CUDA Tile `occupancy` / `num_ctas` |
| **3. Summary / freeze schema** | A record of *what landed*, not an executable | Nothing; engines `apply()` or git pins | Schema miss, replay fail | FlashInfer Trace, mlirAgent fingerprints, admit record, ACF in git |
| **4. Control-plane / tool IR** | Which step to run, which oracle, when to stop | Orchestrator, not `nvcc` | Illegal opcode, skipped gate | ACCLAIM tool calls; AgentFlow-style graphs; **Lintel IR** |

Kind 1 is a language. Kind 2 is a form. Kind 3 is a receipt. Kind 4 is a workflow. Fluency at one does not transfer.

**mlirAgent negative result.** Gemini 2.5 Pro scores **11.9% below identity** when asked to rewrite MLIR ([ucb-bar/mlirAgent](https://github.com/ucb-bar/mlirAgent)). The model is fluent; free IR rewrite is still a worse policy than “leave it alone.” That is why kind 1 as *Translator* (paste CUDA / rewrite LLVM / rewrite MLIR) is the wrong SLA, and why kind 2 + classical lower is the near-term product surface.

---

## Properties that actually matter

Papers that work for agents share a small set of IR properties. They are not “the IR looks like Python.”

| Property | Why it matters | Counterexample |
|---|---|---|
| **Bounded named decisions** | The model fills a finite typed set, not an open program | Raw CUDA / CUTLASS templates |
| **Compiler owns legality and lowering** | Workload-invariant machine rules are compiled once | KernelCraft-style per-workload ISA reconstruction (Zomboss’s foil) |
| **Localized reject** | Fail names `{where}` / thread / field, not a 200-line backend dump | `nvcc` traceback as the only signal |
| **Cheap filter before GPU** | Verifier / cost / SOL / SMT before occupancy of the device | Measure-every-candidate autotune |
| **Hide the wrong details** | Layout algebra, barrier phase bits, template plumbing — *some* of these should be derived | CuTe as the agent surface; also Cake’s bet the other way (show warps, hide layout) |
| **Fits in context (or is a corpus)** | 170-line grammar in the prompt *or* 546B tokens of LLVM-IR. Pick one. Do not pretend both. | “Just dump the dialect into chat” |
| **Headroom / stop** | SOL, Candidate-0, `cost` — a reason to *not* spend the next trial | Open-ended KernelBench loops |
| **Freeze something replayable** | Git can pin a schedule, ACF, or Trace; serve does not re-ask the model | Transcript as the artifact |

Raising the agent from CUDA/CUTLASS text to a small typed surface improves **correctness and tokens**. Localized pre-compile feedback is the differentiator, not a new ISA. SOL / cost-before-measure is **control**, not a dialect. A freeze schema is independent of Cake vs Triton vs Tile.

---

## Families (primary sources)

### A. Hardware-explicit schedule (kind 1)

[Cake](https://arxiv.org/abs/2608.12629) (*CAKE: Compiler–Agent Co-Design for Frontier Kernel Evolution*). Agents author **Cake IR**: typed ops, declared resources, named warp roles, explicit barriers and pipelines. Lowering derives addresses, phase bits, TMEM offsets, warp identity. **No first-class layout algebra** — storage and access sit in the schedule; the compiler checks producer/consumer compatibility. The harness returns localized correctness and performance diagnostics and **grows verifier rules** from recurring fails.

Clean-start Flash-KMeans on B200 at an 80M-token budget: Cake IR median **1.144×** the tuned FlashML baseline vs CUDA/PTX **0.928×**. Beyond that: Kimi Delta Attention **2.05×** geometric mean vs official FlashKDA, validated in serving. NVIDIA Ampere–Blackwell only. The IR **evolves from a kernel corpus**, not from a committee language design.

Year-1 Lintel take: the **mechanisms** (typed schedule, `{where}` reject, growing harness). The live face is **Choreo** (Cake ∪ Argus-lite ∪ TIRx), not Cake v2 the language ([DATA_PLANE.md](DATA_PLANE.md), [CHOREO.md](CHOREO.md)).

### B. Tile DSL + invariants (kind 1, opposite layout bet)

[Argus](https://arxiv.org/abs/2604.18616) (*ARGUS: Agentic GPU Optimization Guided by Data-Flow Invariants*). Triton-like Python with **tag functions / tag assertions**. Lowered to an MLIR dialect that **encodes layout algebra**; Z3 discharges invariants at compile time, **zero runtime**. Counterexamples name **thread, data element, and program point**.

AMD MI300X GEMM / flash attention / MoE (the families that dominate LLM inference GPU time): **99–104%** of hand-optimized assembly throughput; **2–1543×** geomean vs prior agentic systems on those families. KernelBench: **100%** Level 1, **90%** Level 2.

**Opposite Cake bet:** layout algebra *is* the agent-facing math. Cake hides it. Do not average these into “one GPU IR.”

### C. Mapping / library knobs (kind 2)

[Zomboss](https://arxiv.org/abs/2608.00894) (*Rethinking Agentic Kernel Generation for Emerging Accelerators*). Machine semantics compiled once (TAIDL / ACT); the agent searches a **typed mapping surface**. Intent roles: **hard / preferred / automatic**. Compiler completes and legalizes. **Candidate-0** is the verified compiler default and the fallback. PLENA surfaces expose 8–18 knobs (algorithm, matrix/vector decomposition, placement, SRAM residency, prefetch/overlap, precision, loop structure). Result: **56/56** correct verified kernels vs **26/56** for direct neural generation; **3.34×** geomean vs Candidate-0 on Gemmini, **1.10×** on PLENA; **71.2% / 54.2%** fewer inference tokens than Neural. This is job-(d) hardware, not the year-1 SKU — the *boundary* is the lesson.

[µCUTLASS](https://arxiv.org/abs/2603.29010) (*Improving Efficiency of GPU Kernel Optimization Agents…*). ~**170-line** EBNF knob DSL over CUTLASS (config, epilogue fusion, pipelines). Same iteration budget, GPT-5-mini: raw CUDA/CUTLASS **0.40×** PyTorch → DSL **1.27×**; + Speed-of-Light (SOL) steering **1.56×**. SOL also flags benchmark gaming (reported speedups inflate up to **1.9×** without integrity checks). Token-budget policies save **19–43%** while keeping ≥95% of geomean. Grammar in the prompt, not a 546B-token IR-LLM.

Same family, smaller: TensorIR / MetaSchedule sampling instructions; Triton `num_warps` / `num_stages` / `block_*`; CUDA Tile backend (`ENABLE_TILE=1`) knobs **`occupancy`** (1–32) and **`num_ctas`** — CUDA 13.1 Tile IR does **not** take `num_warps`. Portable Triton→PTX and Tile IR are **two backends**, not one schedule type.

### D. Hints / control files (kind 2, applied to an existing compiler)

[HintPilot](https://arxiv.org/abs/2604.15041): LLM synthesizes **semantics-preserving pragmas** (not a rewrite of the program). Up to **6.88×** geomean vs `-Ofast` on PolyBench / HumanEval-CPP in their setting. The model’s output is an annotation the compiler already understands.

[CompileIQ](https://github.com/NVIDIA/CompileIQ): search emits an Advanced Controls File; `nvcc` / `ptxas --apply-controls` applies it (CUDA 13.3+). Teams commit the ACF next to the kernel. On already-optimized workloads, published gains are often **2–3%** — a freeze of compiler knobs, not a new kernel language.

[Compiler-R1](https://arxiv.org/abs/2506.15701) and Meta [LLM Compiler](https://arxiv.org/abs/2407.02524) **flag / pass lists**: the model emits an `opt` sequence (or emulates one). Compiler-R1: **8.46%** IR instruction-count reduction vs `opt -Oz` on their suites. This is CPU/`opt` autotune, not GPU peak.

### E. IR-as-corpus (kind 1 as *training data*, not as SLA payload)

Meta [LLM Compiler](https://arxiv.org/abs/2407.02524): 7B / 13B, pretrained on **546B** tokens of LLVM-IR + assembly. Fine-tunes: **77%** of an autotuning search’s code-size potential with no extra compiles; disassembly round-trip **45%** correct (**14%** exact match). Useful as a **provider** that already speaks LLVM. It is not proof that Lintel IR should be LLVM IR, and it does not beat classical `opt` as a replacement compiler.

[ACCLAIM](https://arxiv.org/abs/2604.04238) (*Agentic Code Optimization via Compiler-LLM Cooperation*): guiding agent with **compiler constituents as tools**; rewrites C / LLVM IR / asm with a test agent. Up to **1.25×** vs `clang -O3` on CPU C programs. Multi-level *tool IR* (kind 4) wrapped around kind-1 rewrites. Not GPU serving \(F\).

### F. Freeze schemas (kind 3)

[FlashInfer-Bench / Trace](https://arxiv.org/abs/2601.00227): JSON **Definition × Workload × Solution × Evaluation**, plus `apply()` into SGLang / vLLM. Orthogonal to which kernel IR produced the Solution. mlirAgent’s **structural fingerprints** are the same kind: a digest the agent or a classifier consumes, not a program it executes.

Lintel’s admit record is this family. Serve is still `lookup(%k)`, not “re-run the Trace producer.”

### G. Human kernel languages agents still dump (kind 1, not co-designed)

Triton, CuTe, Helion, CUDA, HIP, FlyDSL (KernelEvolve). These are real L4 surfaces. They were designed for humans (or for a classical autotuner), not for localized reject. Agents can emit them; the compiler error is usually a blob. Year-1 Lintel does **not** take agent-authored Triton *source* as the SLA payload — it takes a **Choreo Kernel AST** ([DATA_PLANE.md](DATA_PLANE.md), [CHOREO.md](CHOREO.md)). Triton is the first **printer**.

---

## Open fights (do not average)

| Fight | Side A | Side B |
|---|---|---|
| What the model should see | Warp / barrier / pipeline, **no** layout algebra (**Cake**) | Layout algebra **is** the spec (**Argus**) |
| What the model should author | A **program** (Cake / Triton / CUDA / Argus DSL) | A **decision record** (Zomboss / µCUTLASS / ACF / Triton schedule JSON) |
| Where the surface comes from | Grows from a **kernel corpus** (Cake) | Generated from **TAIDL / ACT** (Zomboss) |
| How the model learns the IR | **Train weights** on LLVM IR (Meta Compiler, 546B tokens) | **170-line grammar in the prompt** (µCUTLASS) |
| Which NVIDIA tile backend | Portable Triton TTIR → **PTX** (`num_warps`) | CUDA **Tile IR** (`ENABLE_TILE=1`; `occupancy` / `num_ctas`, not `num_warps`) |

These are live disagreements. A year-1 product picks **one** cell per row and writes it on an adapter, not a blended dialect.

---

## Measurements that survive contact with a SKU

| Claim in the papers | What to keep | What not to productize as \(F\) |
|---|---|---|
| Typed surface ≫ CUDA text (µCUTLASS 0.40× → 1.27×; Zomboss 26 → 56/56) | Year-1 `propose` is a **schema**, not a chat dump | KernelBench vs eager as GA |
| Localized pre-compile feedback (Cake `{where}`, Argus thread/element/point) | Adapter `gate` names `{where, hint}` | “The model will read the nvcc log” |
| SOL / Candidate-0 / cost skip the next trial | Lintel `cost` before `serving_ab`; last_good / classical | Measure every enum on the GPU |
| Freeze schema ≠ kernel IR (FlashInfer Trace, ACF) | Admit record + `%k`; engines `apply()` | New dialect so git has something to pin |
| mlirAgent 11.9% *below* identity | No Translator on SLA | Neural compile / decompile (survey **M3**) |
| Meta Compiler 546B LLVM-IR tokens | Later `llm` **provider** | Lintel IR = LLVM IR |
| Cake 1.144× vs CUDA 0.928× on one clean-start family | Evidence for typed + localized reject | Cake IR as the company (C4) |
| Argus 99–104% of MI300X hand asm | Evidence for invariants + layout algebra *as an oracle/adapter later* | Dual live L4 before first partner canary |

Serving **\(F\)** (tokens/s or TTFT · quality parity · $/compile) is still the year-1 metric ([WHY.md](WHY.md)). None of the papers above sell that SKU. They sell a **representation bet**.

---

## What Lintel already picked

Do not reread this survey as a reason to change the PoC.

| Kind | Year-1 | Where |
|---|---|---|
| **1** Program (structured AST) | Allowlisted **Choreo Kernel** (`adapter-proposal.v0`). Two records, not unbounded search (C3-B). Kind-2 Triton knobs are degenerate. | [DATA_PLANE.md](DATA_PLANE.md), [CHOREO.md](CHOREO.md) |
| **4** Control / tool IR | Lintel IR CFG + `cost` + ADG. Terminators `land` \| `revert` \| `reject`. Serve = `lookup(%k)`. | [POC.md](POC.md), [LINTEL_IR.md](LINTEL_IR.md) |
| **3** Freeze | Admit record in partner git. FlashInfer-style Trace is a cousin, not a second controller. | [ADMIT_RECORD.md](ADMIT_RECORD.md) |
| **1 unstructured / 2 knobs as face** | **Out of SLA.** Triton/CUDA *source*, Cake IR, Tile/HIP as agent face. Printers and later wraps only. LLVM-IR rewrite and neural compile stay out. | [LATER.md](LATER.md), [LLM_IR.md](LLM_IR.md) |

Selector on SLA; JSON schema is the grammar constraint; verify at the same stratum as `propose` — those pins are in [LLM_IR.md](LLM_IR.md) (from the *other* survey). This file is why those pins are not a random taste: the independent literature already split program vs decision vs freeze vs control, and the failures concentrate on free rewrite of the wrong stratum.

---

## Primary sources

| Paper / artifact | arXiv / URL | Kind |
|---|---|---|
| Cake | [2608.12629](https://arxiv.org/abs/2608.12629) | 1 |
| Choreo IR | [github.com/zackc6/choreo](https://github.com/zackc6/choreo) | 1 (year-1 Lintel face) |
| Argus | [2604.18616](https://arxiv.org/abs/2604.18616) | 1 |
| Zomboss | [2608.00894](https://arxiv.org/abs/2608.00894) | 2 |
| µCUTLASS | [2603.29010](https://arxiv.org/abs/2603.29010) | 2 |
| HintPilot | [2604.15041](https://arxiv.org/abs/2604.15041) | 2 |
| Compiler-R1 | [2506.15701](https://arxiv.org/abs/2506.15701) | 2 / `opt` |
| Meta LLM Compiler | [2407.02524](https://arxiv.org/abs/2407.02524) | 1 corpus / 2 flags |
| ACCLAIM | [2604.04238](https://arxiv.org/abs/2604.04238) | 4 + 1 |
| FlashInfer-Bench | [2601.00227](https://arxiv.org/abs/2601.00227) | 3 |
| mlirAgent | [github.com/ucb-bar/mlirAgent](https://github.com/ucb-bar/mlirAgent) | 1 fail + 3 fingerprints |
| CompileIQ ACF | [github.com/NVIDIA/CompileIQ](https://github.com/NVIDIA/CompileIQ) | 2 + 3 |
| CUDA Tile Triton backend | [triton-lang/Triton-to-tile-IR](https://github.com/triton-lang/Triton-to-tile-IR) | 2 knobs |
| *The New Compiler Stack* | [2601.02045](https://arxiv.org/abs/2601.02045) | coarse map; pins in [LLM_IR.md](LLM_IR.md) |
