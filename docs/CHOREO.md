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

## Pros

| Strength | Why Lintel cares |
|---|---|
| **Right band.** L4 kernel choreography, not HLO, not LLVM, not an agent DAG. | We already refused to make Lintel IR a kernel language. Choreo occupies the hole Cake ∪ Argus ∪ TIRx pointed at. |
| **Structured, not fluency.** AST is the mutation API. Closed enums for ops, spaces, roles. | Selector on SLA: allowlisted Kernel records, not paste Triton/CUDA ([LLM_IR.md](LLM_IR.md)). |
| **Localized admit before GPU.** W wellformed, L layout, S sync/race, V tiny-tile sim. | `adapter_gate` `{where: W\|L\|S\|V, hint: node}` is a CFG **edge**, same as Cake `{where}`. Cheap filter before occupancy of the device. |
| **Union, not a new religion.** Cake roles/barriers; Argus layout + (thread, element) CEX; TIRx FFI + CPU sim. | We do not fork Cake IR or wait for a public Cake tree. |
| **Control plane stays out.** That README forbids F, MCP, workflow compile, serving A/B. | Lintel’s SKU is exactly those. Two repos, two IRs, one loop. |
| **Fits the hybrid bet.** Searcher mutates the AST; classical `check` / printer / measure own legality. | C6-B. Survey M3 still out. |
| **Check runs without a GPU.** CPU interpreter for V (Copy today). | CI can fail-closed on layout/sync before a partner machine is attached. |

---

## Cons

| Weakness | What it costs |
|---|---|
| **No device sink in v0.1.** Interpreter + W/L/S; Triton printer is “chosen later.” | Serving **\(F\)** needs a cubin. Until the printer exists, `serving_ab` stays stub-able (already Q2). **Do not stub `adapter_gate`.** Kill switch: no sink by M2 → fall back to degenerate Triton *schedule* knobs so a partner can still freeze. |
| **We own an L4 language.** Cake reading A / C4 was “IR only we can compile.” | Mitigate: Choreo is the *face*; sinks are vendor DSLs (Triton first, then Gluon/TLX/TileLang/HIP). Lintel never emits PTX. Demo is still F, not “we compiled Choreo.” |
| **Straight-line body.** No unstructured CFG; Pipeline is a region, not a full FA3 program. | Acme PoC is a **tile choreography** (Copy+Barrier+Mma), not a complete FlashAttention clone. Peak kernels stay behind the printer + vendor compiler. |
| **Layout algebra is cheap, not Argus SMT.** Shape×stride cover + copy/MMA rank checks. No Z3, no thread/element CEX in v0.1 (schema fields exist; mostly unused). | `{where: L}` is weaker than Argus until Choreo v2. Do not staff Z3 in *lintel*. |
| **V is Copy-only.** `simulate_copy`; MMA is shape-checked, not value-simulated. | Numerical oracle on the cubin still required after lower. V is not serving parity. |
| **SLA still allowlists two complete kernels (C3-B).** Enumerated mutation is what the IR *allows*; year-1 SKU does not free-search the AST. | Typed ≠ unbounded. Same law as the old Triton schedule records. |
| **Second repo to pin.** `compiler_ver` must name `choreoir` **and** the sink. | Replay: bump either pin → new `%k`. Do not vendor `choreoir/` here. |
| **Kind-1 program, not kind-2 knobs.** Agents author a Kernel, not five integers. | Harder for a weak model than `num_warps`/`block_m`. That is the point of Cake/Argus; it is also more surface to allowlist. |

Do not average Choreo with Lintel IR. Do not average Choreo with Triton *source*. Triton is a **printer**, not the agent-facing IR.

---

## Map onto Lintel

| Choreo | Lintel |
|---|---|
| `Kernel` AST (JSON encoding) | `propose` payload; admit-record `actions[].kernel` |
| `check` Finding `gate=W\|L\|S\|V` | `gate adapter` fail `{where, hint=node, partition, element}` |
| CPU interpreter | Optional V before compile; not an L6 oracle |
| Triton printer (choreo v1, not here) | Adapter compile → cubin; then golden / numerical / `serving_ab` |
| Forbidden: F, ADG, MCP, `%k` | **This** repo |

Live `adapter_id`: **`@choreo.v0`**. Year-1 still **one** live adapter. `@triton.v0` schedule fields are the **degenerate** L4 (like linear v0 on the control plane). `@tile.v0` / `@hip.v0` remain Q3 empty stubs. `@cake.v0` remains a later wrap, not the SKU.

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
| Triton (or CUDA) **printer** | No cubin → stub `serving_ab` (already allowed). Golden/numerical wait on the sink. |
| MMA / attention **V** | Adapter V-gate is Copy-only; numerical oracle stays after lower. |
| Pipeline lowering (depth → stages) | `Pipeline.depth` is an AST field git can read; the sink must honor it. |
| JSON serde | This schema *is* the encoding until choreo publishes one. Keep them aligned. |
| Z3 / thread CEX (their v2) | Optional later `oracle`, not year-1 compile. |

### Q2 (once a printer exists)

- Lower allowlisted kernels → Triton (or the week-1 sink) → cubin.
- Golden + numerical on the cubin; `cost`; `serving_ab` on one engine.
- Artifact in partner git: Kernel AST **and** cubin digest. Serve loads the cubin (`lookup(%k)`), never re-checks Choreo on the hot path.
- Kill switch: printer missing or only we can run it → C4. Swap live adapter to degenerate Triton schedule rather than ship a language without a sink.

### Never (still)

- Interpret Lintel IR, ADG, or Choreo on the serve path.
- Dual live L4 (Choreo + Triton-as-agent-face) before first partner canary.
- Copy choreo into lintel; make Lintel IR a Kernel AST; neural compile; survey M3.
- Claim library-class TFLOPS because `check` returned `[]`.

Year-1 executable remains **both** planes: [POC.md](POC.md) ADG walk **and** Choreo Kernel + `{where}` ([DATA_PLANE.md](DATA_PLANE.md)).
