# Choreo IR — data-plane face, not this product

Sibling tree: [zackc6/choreo](https://github.com/zackc6/choreo) (`choreoir` 0.1.0). Read it there. **Do not copy that package into this repo.**

Choreo is the year-1 **L4 object** the agent may fill. **Lintel IR** stays the control plane (CFG, `cost`, ADG, `%k`, `land` / `revert` / `reject`). Choreo’s own spec forbids control-plane work in that tree. The split is the product.

```text
 searcher  ──fills──►  Choreo Kernel AST     ← data plane (this adapter)
                             │
                       check W→L→S→V         ← choreoir.check  (localized Finding)
                             │
                       Triton printer (sink) ← classical; not in lintel
                             │
 Lintel IR ──compile──► ADG ──walk──► admit  ← control plane (this repo)
 serve = lookup(%k)                            no LLM, no Choreo interpret
```

Spec in that repo: AST (kernel, buffers, layout×stride, partitions/roles, Copy / Mma / Barrier / Pipeline) and admit **W / L / S / V**. Findings name `gate`, `node`, optional `partition` / `thread` / `element`. Not scraped `nvcc` stdout.

---

## Verdict (is it good design?)

**Yes as a typed L4 *face* for Lintel. No as a compiler company, and no as “Cake IR + Argus + TIRx in one dialect.”**

What is good is the *split* and the *admit shape*: closed Kernel AST, localized `Finding`, classical `check` / printer, control plane forbidden in that tree. That matches the hybrid bet ([LLM_IR.md](LLM_IR.md), C6-B) and the mlirAgent lesson (free rewrite of the wrong stratum loses to identity).

What is not yet design — it is a **0.1.0 sketch** — is lowering. `choreoir.print_triton` is a deterministic comment+`@triton.jit` stencil for copy/GEMM-tile, explicitly *not* an execution compiler. TIRx already compiles to CUDA C++/PTX with published B200 numbers. Cake already has serving-validated KDA. Choreo does not. Kill switch stays: no cubin sink by M2 → degenerate Triton *schedule* knobs ([RISKS.md](RISKS.md)).

The “union” is of **admit mechanisms**, not of languages. [LLM_ORIENTED_IR.md](LLM_ORIENTED_IR.md) still forbids averaging Cake’s hide-layout IR with Argus’s SMT tile DSL. Choreo **picks one cell per open fight** and copies the *signal* (roles, `{where}`, cheap layout fail, FFI+CPU sim). Comparison below.

---

## Pros

| Strength | Why Lintel cares |
|---|---|
| **Right band.** L4 kernel choreography, not HLO, not LLVM, not an agent DAG. | We already refused to make Lintel IR a kernel language. The hole Cake / Argus / TIRx each occupy a piece of. |
| **Structured, not fluency.** AST is the mutation API. Closed enums for ops, spaces, roles. | Selector on SLA: allowlisted Kernel records, not paste Triton/CUDA ([LLM_IR.md](LLM_IR.md)). |
| **Localized admit before GPU.** W wellformed, L layout, S sync/race, V tiny-tile sim. | `adapter_gate` `{where: W\|L\|S\|V, hint: node}` is a CFG **edge**, same as Cake `{where}`. Cheap filter before occupancy of the device. |
| **Mechanisms, not a fork.** Cake roles/barriers; Argus-shaped finding fields; TIRx-style FFI + CPU sim. | We do not fork Cake IR or wait for a public Cake tree. We also do not staff TVM. |
| **Control plane stays out.** That README forbids F, MCP, workflow compile, serving A/B. | Lintel’s SKU is exactly those. Two repos, two IRs, one loop. |
| **Fits the hybrid bet.** Searcher mutates the AST; classical `check` / printer / measure own legality. | C6-B. Survey M3 still out. |
| **Check runs without a GPU.** CPU interpreter for V (`Copy` / `Mma` / `Reduce` in choreoir; year-1 gate may stay Copy-first). | CI can fail-closed on layout/sync before a partner machine is attached. |

---

## Cons

| Weakness | What it costs |
|---|---|
| **No cubin sink in v0.1.** `print_triton` is a stencil, not `nvcc`. Interpreter + W/L/S are real. | Serving **\(F\)** needs a cubin. Until a printer *executes*, `serving_ab` stays stub-able (already Q2). **Do not stub `adapter_gate`.** Kill switch: no sink by M2 → fall back to degenerate Triton *schedule* knobs so a partner can still freeze. |
| **We own an L4 language.** Cake reading A / C4 was “IR only we can compile.” | Mitigate: Choreo is the *face*; sinks are vendor DSLs (Triton first, then Gluon/TLX/TileLang/HIP). Lintel never emits PTX. Demo is still F, not “we compiled Choreo.” |
| **Designed, not grown.** Cake IR evolved from a kernel corpus; the harness grows verifier rules from recurring fails. Choreo v0.1 is a committee AST. | We do not get Cake’s 1.144× / 2.05× evidence by copying roles. T5-lite (recurring `{where}` → new `check` rule in choreo) is the only evolution loop we own. |
| **Straight-line body.** No unstructured CFG; Pipeline is a region, not a full FA3 program. | Acme PoC is a **tile choreography** (Copy+Barrier+Mma), not a complete FlashAttention clone. Peak kernels stay behind the printer + vendor compiler. |
| **Layout is a third cell, cheaper than both papers.** Shape×stride cover + copy/MMA rank. No Z3, no thread/element CEX in v0.1 (schema fields exist; mostly unused). | Agents still fill strides (Cake said hide that) without Argus CEX. `{where: L}` is a cheap filter. Do not staff Z3 in *lintel*. |
| **V is tiny-tile CPU, not a GPU oracle.** choreoir can sim `Copy` / `Mma` / `Reduce`; year-1 may still gate Copy-first. | Numerical oracle on the cubin still required after lower. V is not serving parity. |
| **SLA still allowlists two complete kernels (C3-B).** Enumerated mutation is what the IR *allows*; year-1 SKU does not free-search the AST. | Typed ≠ unbounded. Same law as the old Triton schedule records. |
| **Second repo to pin.** `compiler_ver` must name `choreoir` **and** the sink. | Replay: bump either pin → new `%k`. Do not vendor `choreoir/` here. |
| **Kind-1 program, not kind-2 knobs.** Agents author a Kernel, not five integers. | Harder for a weak model than `num_warps`/`block_m`. That is the point of Cake/Argus; it is also more surface to allowlist. |
| **Public substitute already exists (TIRx).** TVM FFI, real backend, W/S/race/sim, B200 GEMM/FA4 numbers. | If agents standardize on TIRx, Choreo is a smaller JSON face or a wrap (`@tirx.v0` later). Do not race TVM on peak. |

Do not average Choreo with Lintel IR. Do not average Choreo with Triton *source*. Triton is a **printer**, not the agent-facing IR.

---

## vs existing works (do not mix kinds)

Choreo is **kind 1** (agent-authored program). Lintel IR is **kind 4** (control). The admit record is **kind 3** (freeze). Year-1 SLA *cardinality* is **kind 2** (two allowlisted records). Fluency at one kind does not transfer ([LLM_ORIENTED_IR.md](LLM_ORIENTED_IR.md)).

### Open fights — cells Choreo actually picked

| Fight | Cake | Argus | TIRx | Choreo v0.1 | Lintel year-1 |
|---|---|---|---|---|---|
| What the model sees | Warp / barrier / pipeline; **no** layout algebra | Layout algebra **is** the spec (tags + Z3) | Storage-first layout (D/R/O, named axes) + orchestration in source | **Third cell:** `Layout {shape, stride}`; no Z3; no CuTe work-partition | Same; `{where: L}` is the cheap gate |
| What the model authors | A **program** (Cake IR) | A **program** (tile DSL) | A **program** (TIR + tile primitives) | A **program** (Kernel AST / JSON) | Program payload, **two** allowlisted slots (C3-B) |
| Where the surface comes from | Grows from a **kernel corpus** | Research DSL + MLIR + Z3 | TVM core; intrinsics first, primitives later | **Spec-designed** closed enums | Do not grow a Lintel dialect; T5-lite in choreo |
| How the model learns it | Agents + evolving harness (not a 546B IR-LLM) | Tags in the Python DSL | TVM FFI (Py/C++/Rust) + docs/course | JSON schema in the prompt | Schema is the grammar constraint |
| NVIDIA lowering | CUDA/PTX (their compiler; **no public tree**) | n/a (MI300X) | CUDA C++/PTX (`tir_pipeline="tirx"`) | Triton **sketch** printer | Printer must become a cubin sink or we flip to `@triton.v0` knobs |

That is a pick per row, not Cake IR syntax glued to Argus assertions glued to TIRx D/R/O layouts.

### vs Cake IR ([arXiv:2608.12629](https://arxiv.org/abs/2608.12629))

Cake is the strongest *evidence* that typed schedule + localized pre-compile `{where}` beats CUDA/PTX paste (Flash-KMeans clean-start median **1.144×** vs **0.928×** at 80M tokens; Kimi Delta Attention **2.05×** geomean vs FlashKDA, serving-validated). The secret in that paper is the **evolving harness**, not the keyword `role`.

| | Cake | Choreo |
|---|---|---|
| Agent face | Cake IR (Python decorator schedule) | Kernel AST / JSON |
| Layout | Hidden; compiler checks producer/consumer | Explicit shape×stride |
| Lowering | CUDA/PTX, Ampere–Blackwell | Triton sketch → hoped vendor compiler |
| Harness evolution | Recurring fail → verifier / primitive / cost cal | T5-lite only (new `check` rule, test-gated) |
| Public tree | **No** | **Yes** (`zackc6/choreo`) |
| Peak claim | Published, serving-validated | Forbidden until F on a cubin |

**Take:** typed ops, named roles, explicit barriers/pipelines, `{where}` before GPU. **Do not take:** Cake as the company, 80M-token clean-start as UX, NVIDIA-only compiler. `@cake.v0` remains a later **wrap** if they open the tree ([examples/later/cake-adapter.sketch.md](../examples/later/cake-adapter.sketch.md)).

### vs Argus ([arXiv:2604.18616](https://arxiv.org/abs/2604.18616))

Opposite layout bet. 99–104% of MI300X hand asm on GEMM / flash attention / MoE; CEX names **thread, element, program point**.

Choreo copies the *finding shape* (`thread` / `element` fields) and a cheap L-gate. It does not copy Z3 or the tile DSL. Year-2 `oracle` plugin if we need that CEX — not year-1 compile.

### vs TIRx ([tvm.apache.org/2026/06/22/tirx](https://tvm.apache.org/2026/06/22/tirx))

**Closest public competitor, and the one that can eat the face.** TIRx is TVM’s hardware-native L4: orchestration stays in source (pipeline, roles, sync, intrinsics); layout is a storage contract; tile primitives dispatch to TMA / WGMMA / `tcgen05`. Agent story is the same shape as Choreo: FFI construct/inspect/mutate + dense pre-benchmark feedback (wellformed, sync, race, value-sim). Difference: TIRx **already lowers** and posts B200 GEMM / FA4 numbers vs cuBLASLt / DeepGEMM / CuTeDSL.

| | TIRx | Choreo |
|---|---|---|
| Mutation API | TVM FFI (Py/C++/Rust); still a **DSL** agents write | Closed JSON/AST; four live ops in the Lintel schema |
| Layout | Shard / replica / offset on named hardware axes | Rank-matched `shape`/`stride` ints |
| Sim / admit | Wellformed, sync, race, value-sim | W/L/S + tiny-tile V |
| Backend | CUDA C++/PTX (and a path under TileLang) | Triton stencil |
| Megakernel | Explicit (Event Tensor / task IR) | Out of spec (L6, other repo) |
| Control plane | Search rungs L1–L4 *in the TIRx write-up* | **Forbidden** in the choreo tree |

Choreo’s remaining wedge vs wrapping TIRx today: **smaller closed AST**, JSON as the SLA payload, **no TVM in the pin**, Triton-first (Inductor default), and a hard split so Lintel can sell freeze/`%k` without becoming a TVM distro. If a partner already lives in TVM, `@tirx.v0` is the same door as `@cake.v0` — wrap, new `%k`, do not dual-live before the first canary.

Do not confuse **TIRx** (Apache TVM, public) with **TritorX** (Meta internal bring-up, [MARKET.md](MARKET.md) job (d)).

### vs the rest of the LLM-oriented IR map

| Family | Kind | Relation to Choreo |
|---|---|---|
| *The New Compiler Stack* NL / PL / LLVM-IR | too coarse | Choreo is not “PL.” CUDA, Triton, Cake IR, a 170-line knob DSL are not one band. Pins stay in [LLM_IR.md](LLM_IR.md): Selector, same-stratum verify, no LLVM-IR LLM. |
| mlirAgent (Gemini 2.5 Pro **11.9% below identity** on MLIR rewrite) | 1 fail | Why Choreo is an AST + allowlist, not “the model rewrites the dialect.” |
| µCUTLASS / Zomboss / CompileIQ ACF / Triton `num_warps` | **2** knobs | Stronger *near-term* evidence for weak models (µCUTLASS 0.40× → 1.27×). Degenerate `@triton.v0` *and* C3-B allowlists exist because kind 2 can win the SKU even if kind 1 is the face. |
| Meta LLM Compiler (546B LLVM-IR tokens) | 1 corpus | Later `llm` provider. Not a reason to make Lintel IR or Choreo into LLVM IR. |
| FlashInfer Trace / ACF-in-git | **3** freeze | Cousin of the admit record. Independent of Cake vs Choreo vs TIRx. |
| ACCLAIM / AgentFlow | **4** tools / graphs | Lintel IR’s family. Not Choreo. |
| Triton / CuTe / Helion / CUDA / HIP as *face* | 1, human-designed | Sinks or later adapters. Agent-authored *source* is out of SLA. |

**Near-future substitutes (12–24 months), ranked by how much they threaten the *face* (not the control plane):**

1. **TIRx as the default agent L4** — already public, already a compiler. Threaten Choreo; not `%k`.
2. **NVIDIA ships Cake or CompileIQ+Tile as the agent contract** — distribution + HW. `@cake.v0` / ACF as plugin; stay vendor-neutral freeze.
3. **Kind 2 wins** (ACF, Tile `occupancy`/`num_ctas`, Triton knobs, µCUTLASS-class DSLs) — Choreo was overbuilt; flip live adapter to degenerate knobs (already the M2 kill).
4. **Gluon / TLX / TileLang / CUDA Tile IR** — sinks Choreo should print *into*, not second live faces.
5. **Argus opens** — SMT `oracle`, not a second year-1 compiler.
6. **Helion / KernelEvolve / TritorX productize** — Meta-shaped job (d); out of year-1 SKU.
7. **Generic coding agents** (DSH, Cursor, AlphaEvolve Cloud) — C7; they do not have W/L/S/`%k`.

The control plane (admit, freeze, replay, serving \(F\)) is still unoccupied as a vendor-neutral SKU. That is why Choreo can be a *good face* while being a *worse compiler* than Cake and TIRx.

---

## Map onto Lintel

| Choreo | Lintel |
|---|---|
| `Kernel` AST (JSON encoding) | `propose` payload; admit-record `actions[].kernel` |
| `check` Finding `gate=W\|L\|S\|V` | `gate adapter` fail `{where, hint=node, partition, element}` |
| CPU interpreter | Optional V before compile; not an L6 oracle |
| Triton printer (choreo v1, not here) | Adapter compile → cubin; then golden / numerical / `serving_ab` |
| Forbidden: F, ADG, MCP, `%k` | **This** repo |

Live `adapter_id`: **`@choreo.v0`**. Year-1 still **one** live adapter. `@triton.v0` schedule fields are the **degenerate** L4 (like linear v0 on the control plane). `@tile.v0` / `@hip.v0` remain Q3 empty stubs. `@cake.v0` and `@tirx.v0` remain later wraps, not the SKU.

`%k` = `hash(graph, hw, compiler, adapter, policy)`. Kernel AST is the value *at* the key. `compiler_ver` example: `choreoir==0.1.0;triton==3.3.0+cu128`.

---

## What Lintel still has to do

Control CFG + ADG + `%k` laws are already the PoC. Choreo does not replace them. Remaining work is the **adapter seam** and the **sink**, not a third IR.

### In this plan repo (now)

- Written contract: Kernel JSON schema, two allowlisted Acme kernels, one L-fail payload, CFG/`adapter_gate` edges labeled `W|L|S|V`.
- Do **not** add `src/`, `choreoir/`, or a validator package.

### Q1 (lintel runtime — not this tree)

1. **Adapter plugin** that deserializes Kernel JSON → `choreoir.Kernel`, runs `check`, maps each error Finding onto the CFG edge. Timeout / import fail → fail closed.
2. **Pin** `choreoir` by git SHA / version in `compiler_ver`. Same pin on replay.
3. **Session log** stores Finding JSON (`gate`, `node`, `msg`, optional `partition`/`element`), not a Triton traceback as the only signal.
4. **Two allowlisted slots** (`choreo.attn.d3.w4`, `choreo.attn.d2.w8`). Lab may mutate enumerated fields; SLA `land` still only those records (C3-B).
5. **T5-lite:** recurring `{where: L|S}` → new `check` rule *in choreo* (test-gated) or a tighter allowlist here. Do not grow a Lintel layout dialect.

### Blocked on choreo (do in that repo, consume here)

| Choreo gap | Lintel effect until it ships |
|---|---|
| Triton (or CUDA) **printer that emits runnable code** | `print_triton` is a stencil today. No cubin → stub `serving_ab` (already allowed). Golden/numerical wait on a real sink. |
| MMA / attention **V as a year-1 gate** | Interpreter can sim `Mma`/`Reduce`; still not a GPU oracle. Numerical stays after lower. |
| Pipeline lowering (depth → stages) | `Pipeline.depth` is an AST field git can read; the sink must honor it. |
| JSON serde | This schema *is* the encoding until choreo publishes one. Keep them aligned. |
| Z3 / thread CEX (their v2) | Optional later `oracle`, not year-1 compile. |

### Q2 (once a printer exists)

- Lower allowlisted kernels → Triton (or the week-1 sink) → cubin.
- Golden + numerical on the cubin; `cost`; `serving_ab` on one engine.
- Artifact in partner git: Kernel AST **and** cubin digest. Serve loads the cubin (`lookup(%k)`), never re-checks Choreo on the hot path.
- Kill switch: printer missing or only we can run it → C4. Swap live adapter to degenerate Triton schedule rather than ship a language without a sink. Same kill if the only runnable path is “we compile Choreo” while TIRx/Cake already emit cubins.

### Never (still)

- Interpret Lintel IR, ADG, or Choreo on the serve path.
- Dual live L4 (Choreo + Triton-as-agent-face, or Choreo + TIRx-as-face) before first partner canary.
- Copy choreo into lintel; make Lintel IR a Kernel AST; neural compile; survey M3.
- Claim library-class TFLOPS because `check` returned `[]`, or race Cake/TIRx on peak as the SKU.

Year-1 executable remains **both** planes: [POC.md](POC.md) ADG walk **and** Choreo Kernel + `{where}` ([DATA_PLANE.md](DATA_PLANE.md)).
