# Data plane — Choreo Kernel AST, not a new compiler company

**Control plane** (Lintel IR) is the year-1 PoC: CFG, `cost`, frozen ADG. That IR **does not compile kernels**. It only says *whether* to search, *which* allowlisted kernel to try, *when* to stop, and *what* to pin.

**Data plane** is L4. Year-1 live face is **[Choreo IR](https://github.com/zackc6/choreo)** — a typed kernel choreography AST. Pros, cons, and remaining work: [CHOREO.md](CHOREO.md). Triton / Tile / HIP / Cake IR are **sinks or later adapters**, not the agent-facing IR.

---

## What we take

| Reading | What it is | Year-1 |
|---|---|---|
| **Choreo as the SKU** | Sell a kernel language; demo is “we compiled Choreo” | **Out.** Same kill as Cake v2 the company ([C4](RISKS.md)). |
| **One agent IR for all vendors** | Same Kernel AST → NVIDIA + AMD as one compiler | **Out.** New vendor = new sink / `adapter_id`. |
| **Choreo as the live L4 face** | Agent fills a **Kernel AST**; `choreoir.check` rejects with `{where: W\|L\|S\|V}`; classical **printer** lowers to Triton (first sink) | **In.** This is the data-plane PoC. |
| **Cake / Argus mechanisms** | Typed schedule, localized pre-compile fail, layout CEX, evolving harness | **In**, *implemented by Choreo*, not by forking Cake. |

We do not copy the `choreoir` package into this tree.

---

## Year-1 data-plane PoC (build with the control PoC)

**Live L4:** one adapter, `@choreo.v0` ([choreo](https://github.com/zackc6/choreo) `choreoir==0.1.0`). First **device sink:** Triton printer (choreo’s v1 choice, not this repo). Not Cake IR. Not Tile. Not HIP as a second live path.

**What the agent fills:** a complete **Kernel** (buffers, layout×stride, partitions/roles, Copy / Barrier / Mma / Pipeline). Year-1 still **allowlists two complete records** (C3-B). Typed ≠ unbounded AST search. The type exists so a reject can name `{where, hint}` and so git can read roles, barriers, and pipeline depth.

```
propose %p.0, adapter @choreo.v0, kernel choreo.attn.d3.w4
  // partitions: load(4), math(4); Pipeline.depth=3; Copy+Barrier+Mma
```

**Adapter gate:** `choreoir.check` **before** codegen. Fail is a Finding, not a blob. In Lintel IR this is `gate adapter` (same `gate` opcode; oracle name `adapter`).

```
%s0 = gate adapter %p.0 owner @kernels.acme
cond %s0.ok, ^gold0, ^try1
  // fail { seam = adapter, where = L, hint = c0 }
```

| Finding.gate | `{where}` | Typical `hint` |
|---|---|---|
| W | `W` | node / partition |
| L | `L` | `c0`, `buffer.SmQ`; optional `element` |
| S | `S` | node; `partition` |
| V | `V` | node / index |
| printer / nvcc | `compile_ok` | after a sink exists |

Fail is a CFG **edge** (`^try0` → `^try1`), not terminator `reject`. The next allowlisted Kernel runs.

**Lowering:** Choreo printer → Triton (or week-1 sink) → vendor compiler. Lintel never emits PTX. Until the printer exists, `serving_ab` may stub (Q2); **do not stub `adapter_gate`.** Golden/numerical run **after** adapter compile, same as control PoC.

**`%k`:** still `hash(graph, hw, compiler, adapter_id, policy)`. The Kernel AST is inside the artifact / admit-record, **not** a fifth key axis that includes model id. `compiler_ver` names **both** `choreoir` and the sink (`choreoir==0.1.0;triton==3.3.0+cu128`). Bump either → new `%k`.

**Fitness:** still serving F on the pinned kernel. `check() == []` is not F.

Worked examples: [examples/poc/acme_attn_prefill.choreo.json](../examples/poc/acme_attn_prefill.choreo.json) (`^try0`), [examples/poc/acme_attn_prefill.choreo.try1.json](../examples/poc/acme_attn_prefill.choreo.try1.json) (`^try1`), [examples/poc/acme_attn_prefill.adapter-reject.json](../examples/poc/acme_attn_prefill.adapter-reject.json) (`{where: L}`). Schema: [schemas/adapter-proposal.v0.schema.json](../schemas/adapter-proposal.v0.schema.json). Wired into the control CFG: [examples/poc/acme_attn_prefill.poc.lintel](../examples/poc/acme_attn_prefill.poc.lintel). Degenerate Triton *schedule* knobs: [examples/later/triton-schedule.json](../examples/later/triton-schedule.json).

---

## What we do **not** staff in year 1 (data plane)

- A Lintel CUDA / MLIR / Cake **dialect**, or vendoring `choreoir/` into this repo.
- Dual live adapters (Choreo-as-face **and** Triton-as-face) before first partner canary. Q3 = **empty stub** second `adapter_id` only ([YEAR1.md](YEAR1.md)).
- One cost model across L1–L7. Choreo V-sim is a tiny-tile filter, not serving F.
- Agent-written raw Triton / CUDA **source** as the SLA payload. Kernel AST in, printer+compiler out.
- Argus Z3 inside Lintel. That is Choreo v2, consumed as an `oracle` later.
- Claiming FA3-class peak from a straight-line Copy+Mma tile.

---

## Coverage after the data-plane PoC

Same rule as control: **after** one partner graph lands with an allowlisted Choreo Kernel + `{where}` gates **and** a device sink that can freeze a cubin.

| Later | What | Why wait |
|---|---|---|
| Triton / CUDA printer | choreo v1 deliverable | Without it, no serving F |
| `@tile.v0` / `@hip.v0` stub | Empty provider, same `propose` Kernel shape, different printer | Q3 hedge; not two live compilers |
| `@triton.v0` schedule knobs | Degenerate L4 (five integers) | Fallback if Choreo has no sink by M2 |
| `@cake.v0` | Wrap if a public Cake tree exists **or** a customer funds it | Optional; C4 still applies if this becomes the product |
| `@tirx.v0` | Wrap TVM TIRx if a partner already lives there | Same door as Cake; do not dual-live with `@choreo.v0` before first canary |
| Gluon / TLX / TileLang / HIP printers | Choreo v2 plugins | Same Lintel IR |
| Argus-class SMT | `oracle` on layouts, **after** or **beside** `check` | Research; not year-1 compile |
| Agent-authored kernel **text** | Adapter ingests Triton/HIP source under the same gate+oracle | After AST-only PoC works |

Cake wrap sketch (unchanged door): [examples/later/cake-adapter.sketch.md](../examples/later/cake-adapter.sketch.md).

---

## How this sits under Lintel IR

```
Lintel IR (control)     propose / adapter_gate / oracle / land
        │
        ▼
adapter @choreo.v0      Kernel AST → check W/L/S/V → printer → vendor compiler
        │
        ▼
L4 binary               cubin / Triton artifact
        │
        ▼
L6 serve                lookup(%k)  — no LLM, no Choreo interpret
```

Control PoC without a Kernel AST still “works” (opaque `enum_id`). It throws away the reason Choreo exists: **the agent needs a typed, locally rejectable L4**, not a string.

Data-plane PoC without Lintel IR is a `choreoir.check` wrapper. It cannot freeze, replay, or sell the **decision**.

Year-1 executable = **both**: Lintel IR CFG+cost+ADG **and** Choreo Kernel + `{where}`.

---

## Buy test (data plane)

A partner should see:

1. Same engine, same graph, **Kernel AST** in git (readable: partitions, barriers, pipeline depth, layouts).
2. A failed propose that says `{where: L, hint: c0}` (or S/W/V), not a 200-line Triton traceback as the only signal.
3. Serving F move on that kernel (order **3–12%**, [WHY.md](WHY.md)) once a printer exists — not a new programming language to rewrite the model in.

If the demo is “we compiled Choreo IR,” we failed the product test even if `check` is green.
