# Data plane — Cake-class adapter, not Cake v2 the company

**Control plane** (Lintel IR) is done as the year-1 PoC: CFG, `cost`, frozen ADG. That IR **does not compile kernels**. It only says *whether* to search, *which* adapter enum to try, *when* to stop, and *what* to pin.

**Data plane** is the stack that already exists: PyTorch graph → Inductor/Triton (or Tile/HIP) → PTX → engine. This doc is what we do **there** in year 1 vs later.

Cake v2 **as a new kernel language we own** is out. Cake v2 **as the adapter contract** (typed schedule + `{where}` reject + growing harness) is the year-1 data-plane PoC.

---

## What “Cake v2” would mean, and which one we take

Three readings of “do Cake v2”:

| Reading | What it is | Year-1 |
|---|---|---|
| **A. New IR / dialect** | Own Cake-like kernel language, CUDA/Tile backend, papers | **Out.** NVIDIA kill ([C4](RISKS.md)). Looks like progress ([RISKS.md](RISKS.md) “Cake IR only we can compile”). |
| **B. One agent IR for all vendors** | Same Cake-ish IR → NVIDIA + AMD + … | **Out.** Explicit non-goal. New vendor = new `adapter_id`. |
| **C. Cake *mechanisms* on the live L4** | Typed **schedule record** the agent fills; adapter **rejects with `{where}`**; harness **grows checks** from recurring fails; still **Triton** (year-1) lowers to GPU | **In.** This is the data-plane PoC. |

We take **C**. We do not take A or B.

Evidence we steal from (do not copy trees): Cake = typed agent-facing schedule + localized pre-compile fail + evolving harness. Argus = optional later **oracle**, not the compiler. GEAK = Amdahl on the **warm** path (already in Lintel `cost`).

---

## Year-1 data-plane PoC (build with the control PoC)

**Live L4:** one adapter, `@triton.v0` (Triton 3.x on the partner pin). Not Cake IR. Not Tile. Not HIP.

**What changes vs a dumb enum string:** the `propose` payload is a **typed schedule**, not `num_warps=8.block_m=128` as opaque text. Year-1 still **allowlists two complete records** (C3-B). Typed ≠ unbounded search. The type exists so a reject can name `{where, hint}` and so git can read warps/block.

```
propose %p.0, adapter @triton.v0, schedule {
  num_warps: 8,
  num_stages: 3,
  block_m: 128,
  block_n: 64,
  block_k: 64
}
```

**Adapter gate (Cake `{where}`):** before `nvcc`/Triton compile, reject with a **band**, not a blob. In Lintel IR this is `gate adapter` (same `gate` opcode; oracle name `adapter`). Not a new control-plane IR.

```
%s0 = gate adapter %p.0 owner @kernels.acme
cond %s0.ok, ^gold0, ^try1
  // fail { seam = adapter, where = smem, hint = block_m }
```

Fail is a CFG **edge** (`^try0` → `^try1`) with `{where: smem, hint: block_m}`, not terminator `reject` and not a 200-line Triton traceback. The next allowlisted record runs. Same idea as Cake localized reject; **implementation is Triton-legal fields only**. Year-1 still does not free-search integers — two records, typed so the edge can name a field.

**Lowering:** Triton compiler, as today. Lintel never emits PTX. Oracles (ncu, occupancy) run **after** adapter compile, same as control PoC.

**`%k`:** still `hash(graph, hw, compiler, adapter_id, policy)`. The **schedule record** is inside the artifact / admit-record, **not** a fifth key axis that includes model id. Two different schedules for the same graph+hw+compiler+adapter+policy are two artifacts; policy-hash later includes the ADG that chose them ([LATER.md](LATER.md)).

**Fitness:** still serving F on the pinned kernel, not Σ Triton microbench.

Worked examples: [examples/poc/acme_attn_prefill.triton-schedule.json](../examples/poc/acme_attn_prefill.triton-schedule.json) (`^try0`), [examples/poc/acme_attn_prefill.triton-schedule.try1.json](../examples/poc/acme_attn_prefill.triton-schedule.try1.json) (`^try1`), [examples/poc/acme_attn_prefill.adapter-reject.json](../examples/poc/acme_attn_prefill.adapter-reject.json) (`{where: smem}`). Schema: [schemas/adapter-proposal.v0.schema.json](../schemas/adapter-proposal.v0.schema.json). Wired into the control CFG: [examples/poc/acme_attn_prefill.poc.lintel](../examples/poc/acme_attn_prefill.poc.lintel).

---

## What we do **not** staff in year 1 (data plane)

- A Lintel CUDA / MLIR / Cake **dialect**.
- Compiling Cake IR in-house as the default path.
- Dual live adapters (Triton + Cake, or Triton + Tile) before first partner canary. Q3 = **empty stub** second `adapter_id` only ([YEAR1.md](YEAR1.md)).
- One cost model across L1–L7 ([ARCHITECTURE.md](ARCHITECTURE.md)). Adapter may expose **L4-only** cost hints to Lintel `cost` (later).
- Agent-written raw Triton **source** as the SKU. Enum/schedule in, compiler out. (Agent may propose source **inside** the adapter later; year-1 PoC is schedule fields.) The JSON schema **is** the grammar constraint; we do not constrained-decode CUDA ([LLM_IR.md](LLM_IR.md)).

---

## Coverage after the data-plane PoC

Same rule as control: **after** one partner graph lands with typed Triton schedule + `{where}` gates.

| Later | What | Why wait |
|---|---|---|
| `@tile.v0` / `@hip.v0` stub | Empty provider, same `propose` shape, different field names | Q3 hedge; not two live compilers |
| `@cake.v0` | **If** a public Cake tree exists **or** a customer funds it: wrap as adapter, map Cake schedule types → their compiler | Optional third provider. Not the SKU. C4 still applies if this becomes the product. |
| `@helion` / CuTe / CUTLASS | More `adapter_id`s | Same plugin seam |
| Argus-class SMT | `oracle` on layouts/indices, **after** or **beside** adapter, not instead of Triton | Research; not year-1 compile |
| Per-adapter cost model | Feeds Lintel `cost` (`worth_measure`) with L4 estimates | After F is honest on one graph |
| Agent-authored kernel text | Adapter ingests Triton/HIP **source** under the same gate+oracle | After schedule-only PoC works |

Sketch: [examples/later/cake-adapter.sketch.md](../examples/later/cake-adapter.sketch.md).

---

## How this sits under Lintel IR

```
Lintel IR (control)     propose / adapter_gate / oracle / land
        │
        ▼
adapter plugin          typed schedule → vendor compiler
        │
        ▼
L4 binary               Triton/Tile/Cake/HIP artifact
        │
        ▼
L6 serve                lookup(%k)  — no LLM
```

Control PoC without typed schedule still “works” (opaque `enum_id`). It just throws away Cake’s actual lesson: **the agent needs a typed, locally rejectable search space**, not a string.

Data-plane PoC without Lintel IR is a Triton autotune wrapper. It cannot freeze, replay, or sell the **decision**.

Year-1 executable = **both**: Lintel IR CFG+cost+ADG **and** Triton typed schedule + `{where}`.

---

## Buy test (data plane)

A partner should see:

1. Same engine, same graph, **schedule record** in git (readable: warps/block/stages).
2. A failed compile that says `{where: smem}` not a 200-line Triton traceback as the only signal.
3. Serving F move on that kernel (order **3–12%**, [WHY.md](WHY.md)) — not a new programming language to rewrite the model in.

If the demo is “we compiled Cake IR,” we failed the product test even if the kernel is fast.
