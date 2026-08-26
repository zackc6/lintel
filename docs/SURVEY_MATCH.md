# Survey match — Horizon A direction, not the full stack

Evidence: [zackc6/ai-compiler-survey](https://github.com/zackc6/ai-compiler-survey) §5.1–5.1.4, §5.5, §5.8.4. This file does not copy that tree. Year-1 choices stay in [SURVEY_MAP.md](SURVEY_MAP.md). Band map and Acme walks: [ARCHITECTURE.md](ARCHITECTURE.md), [WHY.md](WHY.md). Codesign: [CHOREO.md](CHOREO.md) Undergo.

**Yes for the survey’s predicted *direction* (Horizon A, soft merge M1, hybrid C6-B).** No for the full predicted *stack* (joint search across L1–L7, four jobs, compiled control plane as Horizon B). The codesign is a **narrow year-1 productization** of that direction, not a new L-band and not “agents are the compiler.”

The parenthetical — *Choreo evolves during compilation, not a fixed dialect* — matches survey **T5 (Cake flavor)** only with **two clocks**. If “evolve” means the checker rewrites itself **inside one specialize walk**, that is the survey’s **M3** failure mode. Forbidden. [ARCHITECTURE.md](ARCHITECTURE.md), [CHOREO.md](CHOREO.md).

---

## 1. Does it match the predicted future?

| Survey claim | Codesign | Match? |
|---|---|---|
| Agents = control plane; compilers = data plane | Lintel IR walks CFG/ADG; `choreoir.check` + sink lower | **Yes** |
| **M1** one e2e controller over band *tools*; classical lower/admit stay | Lintel is the controller; Choreo+sink are L4 tools; serve is `lookup(%k)` | **Yes (narrow)** |
| **M3** agents *are* the compiler, no classical admit | Explicitly out; kill C6-A | **Yes (refuse)** |
| **T1+T2+T3** highest-leverage missing product | Typed Kernel + `{where}` gates + `%k` freeze/replay | **Yes as SKU shape** |
| **T6** serving \(F\) admits, not microbench | `gate serving_ab`; Walk B reverts +11% bench on parity fail | **Yes as law; not yet as evidence** |
| **T5** compiler/harness evolves from recurring fails (Cake) | Recurring `{where}` → choreo PR → bump `compiler_ver` → new `%k` | **Yes as T5-lite** |
| **T10** control plane compiles (ADG freeze) | PoC: module → ADG; later `%w` | **Lite** (Horizon B is full workflow IR) |
| **C3-B** constrain the action space | Two allowlisted Kernels; typed ≠ unbounded AST search | **Yes** |
| **C4** multi-DSL, no one vendor IR | One *face* (Choreo), Triton first *sink*; later wraps | **Partial** — year-1 re-bets Triton-first |
| **C5** freeze-before-serve, not default-on LLM compile | Specialize vs serve split; no LLM on serve | **Yes** |
| Jobs (b)(c)(d), L7, Magellan/MLGO | Out of year-1 | **Intentional miss** vs full prediction |

It matches **Horizon A job (a)** — CI specialize under \(F\), freeze, classical fallback — which is what the survey says ships first. It does **not** yet *be* §5.1.3: a joint policy over L2/L3 + L4/L5 + L6 + L7.

---

## 2. How it matches / reshapes the e2e controller and L1–L7

Survey §5.1.3: bands stay **legality/lower surfaces**; **search and admit** sit under one \(F\). Soft merge unifies the *optimizer*, not the execution substrate.

Year-1 Lintel×Choreo is that reshape **cut to one search band**:

```text
 F (tokens/s × parity × $/compile)
        │
   Lintel IR  ← e2e controller (budget, stop, land|revert|reject)
        │
   L1  fingerprint + Amdahl triage     searched?  NO (cut only)
   L2  graph_hash in %k                searched?  NO
   L3  Inductor/MLIR pinned            searched?  NO
   L4  Choreo Kernel AST               searched?  YES (only live surface)
   L5  PTX/SASS via sink               searched?  NO (classical lower)
   L6  SGLang xor vLLM A/B + freeze    searched?  NO — this is the *oracle*
   L7  place                           out
   L0  LLVM/CPU                        out
```

| Band | Survey job of the band | What codesign does | What it does *not* do |
|---|---|---|---|
| **L1** | capture / region cut | `triage` / `cond hot` skips cold regions (GEAK/P23) | No torch rewrite, no new graph IR |
| **L2** | portable graph | Identity in `%k` | No StableHLO face |
| **L3** | mid-IR | Pin `compiler_ver`; do not propose | No mlirAgent rewrite |
| **L4** | kernel DSL | Agent fills Kernel AST; `check` W/L/S/V is a **CFG edge** | Does not become the SKU (“we compiled Choreo”) |
| **L5** | ISA/backend | Hidden in the **sink** (must consume `Pipeline.depth`) | No PTX mutation, no ISA RFC company |
| **L6** | serving | \(F\)-admit + freeze; load cubin | No Event Tensor megakernel IR; no engine ownership |
| **Control** | e2e search | CFG + `cost` + ADG | Not a universal L1–L7 cost model |

That is **Amdahl-first under \(F\)** (survey §5.1.3 component 8), not yet **bilevel fusion+tile+serve+place**. The controller *owns* L4 search and L6 admit; it *talks to* L1–L3/L5 as pins and fingerprints. Calling it “the e2e-optimal-seeking architecture” would overclaim until proposals at L2/L3 or place exist and lose to rolled-up \(F\).

**C4 is an L4 *sink* fight**, not a Lintel-IR fight. Year-1: one face, one sink. A second DSL is a new `adapter_id` / `%k` — the survey’s plugin fallback when industry does not consolidate.

Worked walks (same `graph_hash`): [WHY.md](WHY.md), [ARCHITECTURE.md](ARCHITECTURE.md).

---

## 3. “Choreo evolves during compilation, not fixed”

Survey **T5** has two flavors:

1. **Cake:** recurring search failures → new verifier rules / IR primitives (corpus-gated, still classical `check`).
2. **TritorX / job (d):** sim+silicon pain → dialect/ISA *proposals* for humans/EDA. **Out** of year-1.

“Not a fixed Triton dialect” is **predicted**. The L4 compiler is an artifact that **undergoes T5**, while L1–L2 `graph_hash` can stay the same. The data-plane compiler is in the loop, not only the kernel text.

| Clock | What is allowed | Survey reading |
|---|---|---|
| **Inside one ADG walk** | `choreoir` **pinned** in `%k`. `check` / sink are ordinary functions. Agent fills allowlisted Kernels. Fail `{where: L}` → next kernel, **not** a new opcode. | Hybrid C6-B. Cake *using* a harness, not rewriting it mid-step. |
| **Across CI compiles / overnight specialize** | Recurring `{where}` → Lintel opens a **choreo PR** → human merge → bump `compiler_ver` → **new `%k`**, must re-land. Next night’s walk uses a different compiler on the **same** torch region. | **T5**. Compiler is not fixed. Replay still holds. |

If “evolve during compilation” means rewriting `check.py` while walking `^try0`→`^try1`, or the agent adding a keyword at runtime: **M3-adjacent, forbidden**. Survey T5 is still humans + corpus gate, not autonomous tape-out (C10).

**Gray zone (later, not year-1).** Cake-style *intra-session* tactic/verifier growth **as data** (allowlist, cost cal, extra Finding rules loaded from a versioned bundle), bundle hash in `%k` / `%w`, `check` still a pure function, no LLM in `check`. That is “compiler evolves *over* compilation,” not “compiler is an agent.” Year-1 routes that through a git PR instead. Safer for replay; slower than Cake’s 80M-token paper. Door: [LATER.md](LATER.md).

**Do not confuse:** Choreo v0.1 is a **committee AST**. Cake’s IR grew from a kernel corpus. Until Undergo has a real fail corpus, “not fixed” is a **process claim**, not an empirical one. Two allowlisted kernels are a weak T5 corpus.

---

## 4. Missing vs the survey — and unpredicted-good

### Missing (expected for a year-1 SKU; still real)

- **Joint / bilevel search.** No L2/L3 proposal surface; no place; no backtracking that revisits fusion after a kernel “win.” Year-1 can still ship a *great L4 kernel that is locally greedy*.
- **Money-grade T6.** Serving A/B is the *law*; partner p50/p90 + cost-to-compile (C2) is not produced yet. `serving_ab` is stub-able until a cubin sink exists.
- **A real L4 compiler.** v0.1 type-checks and stencils Triton; Cake/TIRx already consume schedule into a binary. Without a sink that honors `Pipeline.depth`, the face is a checker, not a data plane.
- **Portable T1 RFC.** Choreo JSON is *a* typed face, not the missing cross-stack schema (MLIR · Triton · TileLang · CuTe · Cake · TIRx).
- **Learned e2e surrogate** (survey §5.1.3 component 3) and **job (b)** encode-wins into heuristics (T4).
- **T5 full / job (d):** no ISA feedback sink; L5 `where` is a later oracle plugin, not TritorX.
- **T9** signing/CODEOWNERS as a product (Q3).
- **Energy / cluster** in \(F\); Event Tensor–class L6 fusion as a search surface.
- **Argus-depth L** (Z3 / thread-element CEX) and Cake-depth instruction admission (WGMMA vs `tcgen05`).

None of these mean the *direction* is wrong. Year-1 is **M1-lite on one band**, not Horizon B.

### Unpredicted-good (survey did not require this shape)

1. **Two-kind codesign as law.** Kind-4 control (Lintel) and kind-1 face (Choreo) in *separate repos*, with Choreo’s spec forbidding \(F\)/MCP/A/B. Survey said “don’t add an L-llm band.” This is an org chart.
2. **Public tree vs Cake.** Cake is the strongest *evidence* and has **no public compiler**. Choreo can be a worse compiler and still be a better *product face*.
3. **Triton is printer, not face.** Vendor DSLs are sinks. SLA: no agent-authored Triton/CUDA text. Matches LLM4IR (fluency ≠ CFG/exec).
4. **`{where}` is a CFG *edge*, not `reject`.** Cake diagnostics compiled into T10-lite. Opaque `enum_id` cannot say “mutate layout `c0`.”
5. **`%k` drops `model_id`.** Survey T3 said this product is missing. Graph/hw/compiler/adapter/policy; model swap is replay.
6. **Kind-2 kill switch.** No cubin sink by M2 → `@triton.v0` knobs. C3/C4: weak models often win on knobs.
7. **Layout third cell, not a glue language.** Refuse to average Cake (hide layout) with Argus (layout = spec + SMT).
8. **Two clocks for T5.** More replay-safe than a naive Cake reading. Dialect evolution *and* freeze/replay composed.

---

## 5. Pros and cons

**Pros**

- Directionally on the survey’s winning pattern: hybrid loop, \(F\) as win, freeze before serve, classical fallback drilled.
- Year-1 scope matches what the survey says is commercially missing (T1/T2/T3 as a product, not another kernel paper).
- L1–L7 stay bands; no fake L8; no PowerIR; economics as policy (`cost` gate).
- Evolving L4 compiler (T5-lite) without claiming M2 (“one IR for all vendors”) or M3.
- Small-team shape: one GPU family, one live adapter, one engine; C4 recoverable via `adapter_id`.
- Kill switches mapped to C2/C3/C4/C5/C6 instead of averaging conflicts.

**Cons**

- **Plan, not a compiler.** Control PoC without a Kernel is an opaque enum. Data plane without Lintel cannot freeze. Executable needs both, and Choreo still does not emit a cubin that preserves `Pipeline.depth`.
- **Owning an L4 language is the C4 trap** (“IR only we can compile”). Mitigation (face ≠ sink) is documented; the demo still has to be serving \(\Delta F\). TIRx can eat the *face* without touching `%k`.
- **Designed AST vs grown harness.** T5 does not start until fail classes exist. Two complete records is C3-B safety and a **weak evolution corpus**.
- **L4-only search** can reproduce the survey anti-pattern: great tile, bad fusion / serving. \(F\)-admit at L6 *catches* that if A/B is real; it does not *search* L3 to fix it.
- **Two IRs to pin** (`choreoir` + sink in `compiler_ver`). Replay is stricter; onboarding is heavier.
- **Kind-1 is harder for weak models** than five Triton integers. If kind 2 wins, Choreo was overbuilt (M2 kill).
- **“Evolve during compilation” is a slogan hazard.** Language that sounds like self-modifying compile will be read as C6-A even if the implementation is PR-gated T5.
- **Triton-first printer re-opens C4-A.** Gluon/TLX/TileLang/FlyDSL/CuTe remain later printers; year-1 does not learn whether the face ports.

---

## Bottom line

Treat Lintel×Choreo as **Horizon A, job (a), M1-lite**: an e2e *controller* that searches **only L4**, admits on **L6 \(F\)**, and lets the **L4 compiler undergo T5 across jobs** while remaining a pinned classical function **inside** a job.

That is the survey’s predicted *direction*. It is **not** yet the predicted *architecture* (joint policy over L2–L7, money-grade p50, compiled `%w` as Horizon B, codesign T5 into ISA). The unpredicted good is the **split itself** (public typed face + vendor printer + freeze SKU) and the **two-clock T5**. The load-bearing risk is not philosophical — it is whether a sink **consumes** the schedule before M2, and whether “evolve” stays **Undergo (PRs + new `%k`)** rather than mid-walk self-modify.
