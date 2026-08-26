# LLM-oriented IRs — what we take

Evidence (read in place, do not copy): [ai-compiler-survey](https://github.com/zackc6/ai-compiler-survey) §0.2 taxonomy and §5.1.1–5.1.2 bands, from *The New Compiler Stack* ([arXiv:2601.02045](https://arxiv.org/abs/2601.02045)). That paper surveys **which IR an LLM touches**. It is not a SKU. This file is what Lintel **pins** from it.

Independent cut from primary papers (Cake, Argus, Zomboss, µCUTLASS, …), not from that survey: [LLM_ORIENTED_IR.md](LLM_ORIENTED_IR.md). Keep the two files separate.

Their three strata (NL / high-level PL / LLVM IR+ASM) are **too coarse** for us. CUDA, Triton, and Python are not one “PL.” LLVM IR is not our agent surface. If we designed Lintel IR as “the IR LLMs like” from that map, we would mix the control plane with Meta-LLM-Compiler rewrite and KernelBench CUDA paste.

---

## Four axes → year-1 pins

| Their axis | Their cut | Lintel pin |
|---|---|---|
| **Design philosophy** | Selector / Translator / Generator | SLA `propose` is **Selector** (allowlisted **Choreo Kernel**). Translator (`paste_cuda`, free LLVM/Triton rewrite) is **illegal on SLA**. Generator-lite = the **inspectable Kernel JSON**, then `check` + printer. Magellan-class Generator (new passes) is job (b) — **out**. |
| **LLM methodology** | Training-required (IR-LLM, SFT/RL) vs training-free (prompt/agent) | Year-1 `llm` seam is **training-free**. A Meta-Compiler-class IR model is a later **provider**, not a new Lintel IR. Their “locked-in to one IR task” warning is our **P12**. |
| **Abstraction** | NL · PL · LLVM IR/ASM; intra-level vs cross-level (compile/decompile) | Lintel IR sits **above** all three. NL = commentary only. PL payload year-1 = **Choreo Kernel AST**, not CUDA/Triton source. LLVM IR/PTX = classical **L0/L5**. Cross-level “LLM is the compiler” (C→x86, decompile) is **survey M3** — out. |
| **Task / metric** | Transpile CA@k, KernelBench vs eager, LLVM `-Oz` size, BLEU | SKU metric stays serving **\(F\)** ([WHY.md](WHY.md)). Their own §4: LLM-as-`opt` on LLVM IR still does **not** beat classical compilers on perf/cost/scale. |

---

## Design laws (keep)

1. **Verify at the same stratum as `propose`.** A Kernel proposal is gated by `adapter_gate` `{where: W|L|S|V}` (`choreoir.check`) then golden/numerical on the cubin. Alive2-on-LLVM is the wrong oracle for that payload. If lab later allows Translator of Triton **source**, that is a new gate set, not a reuse of layout checks.

2. **The grammar constraint is the Kernel JSON schema**, not xgrammar over CUDA. Typed `kernel` already forces a legal Selector action. Constrained decoding of kernel text is a Translator tax we do not pay in year 1.

3. **Interpretability is the admit record + Kernel AST**, not Chain-of-Thought. The paper’s best Generator pattern is “LLM emits a script a compiler then runs.” That script is `adapter-proposal.v0` (Choreo Kernel), not chat.

4. **Do not import LEGO-Compiler decomposition** (basic-block split for neural compile). That helps translation, not joint \(F\)-search. Our scale cut is Amdahl `triage` on a **region**, already in the PoC CFG.

5. **Self-improving = T5-lite, not a new `opt`.** Recurring `{where}` → tighter allowlist or a new `choreoir.check` rule (test-gated in choreo). Do not staff “Translator finds a trick → we emit a new LLVM pass.”

---

## Take / discard

| Take | Discard |
|---|---|
| Hybrid: LLM proposes, classical compiler admits | LLM replaces `opt` / Inductor / Triton |
| Selector as the safe default (C3-B) | Translator as the demo (KernelBench theater); unbounded Choreo mutation on SLA |
| Inspectable artifact before execute | BLEU / CA@k / `-Oz` size as GA |
| Training-free + pluggable model | Pretrain a Lintel IR-LLM in year 1 |
| Correctness is the production gap | Neural compile / decompile opcodes |
| Cost must beat search time saved | Always-on frontier model per kernel |

---

## Map onto existing IRs

```text
 NL commentary          admit-record.commentary     ← not a contract
 Lintel IR              CFG · cost · land           ← control; not LLM-consumed data plane
 Choreo Kernel JSON     adapter-proposal.v0         ← year-1 LLM-facing L4 (Selector)
 Triton / Tile / HIP    printer / later adapter_id  ← sinks; still not Lintel IR
 Cake IR                later wrap                  ← still not Lintel IR
 LLVM IR / PTX          classical L0 / L5           ← oracles after lower; no propose
```

Year-1 executable is still [POC.md](POC.md) + [DATA_PLANE.md](DATA_PLANE.md). Choreo is the L4 face, not a third *control* IR.
