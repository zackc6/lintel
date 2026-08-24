# Coverage after the PoC

The [PoC](POC.md) is the hard kernel on **one** graph. This file is how that kernel grows. Not survey M3. Serve stays `lookup(%k)`. Staffing does not delay these; sequence them by **dependency**, not by headcount.

## Already in the PoC (do not redo)

CFG with `cond`, `cost` as a gate, compile module → ADG, interpret ADG, `%k` replay, two enums, one region.

## Extend in this order

### 1. Controller key `%w` (next)

PoC freezes an ADG digest beside the admit record. Coverage makes that a first-class key:

| Key | Fields | Artifact |
|---|---|---|
| `%k` | graph, hw, compiler, adapter, policy | Kernel digest |
| `%w` | controller, policy, oracle bundle, \(F\), budget | ADG |

Triton bump → new `%k`. Gate set / \(F\) / budget bump → new `%w` (and new `%k`, because `policy_id` is in `%k`).

Sketch (fuller compile module): [examples/later/wf_acme_specialize.compile.lintel](../examples/later/wf_acme_specialize.compile.lintel).

**Need.** PoC ADG freeze is boring. **Exit.** Partner CI pins `@wf…` digest; same `%w` ⇒ same ADG or hard fail.

### 2. Policy hash = graph hash

PoC says the policy owns the CFG; coverage **enforces** it: `hash(ADG)` must equal `policy.graph_digest`. Extra blocks or edges from the model → `reject`.

**Need.** `%w`. **Exit.** A mutated `.lintel` that adds a `paste_cuda` edge is rejected before interpret.

### 3. More edges, same laws

| Add | Still illegal |
|---|---|
| `cond` on numerical fail → next enum (not only golden) | Agent-authored edges |
| Triage ranks N regions; CFG per region or a dispatcher block | One mega-CFG the model writes |
| `or_else classical` as well as `last_good` | Dropping a required gate |
| Depth > 2 enum tries, still allowlisted | Unbounded search |

CFG sketch with the richer retry shape is already in [examples/later/acme_attn_prefill.cfg.lintel](../examples/later/acme_attn_prefill.cfg.lintel) (same graph as PoC; keep it as the coverage source of truth when PoC and coverage diverge).

### 4. Cost that is still not L1–L7

| Add | Still a non-goal |
|---|---|
| Budget from partner SLO, not a constant `usd=50` | Universal analytical model for every IR level |
| `worth_measure` uses last_good.F **and** canary GPU quote | Agent-chosen \(F\) |
| Record skip vs spend on the admit record | Silent skip with no audit |

Cost-only slice: [examples/later/acme_attn_prefill.cost.lintel](../examples/later/acme_attn_prefill.cost.lintel).

### 5. Second adapter / engine (width, not a new control IR)

New `adapter_id` or serving provider → new `%k`. Same Lintel IR, same ADG opcodes, new enum table. Q3 stub adapter still valid; live second surface when a partner needs it.

### 6. Placement / multi-SKU (after `%w` is boring)

MARKET year-3 line: workflow freeze + placement. Only after partner CI runs frozen ADGs for one SKU. Still classical kernel lowering. Still not LLM-as-`opt`.

## Compiler passes on Lintel IR (coverage)

PoC: check + lower to ADG. Coverage can add, still on the **control** graph:

- Unreachable-block reject (already implied by PoC checks)
- Dominates: `cache_key` before any terminator
- Edge labels must be `{where, seam}` from a real gate
- ADG canonical JSON (sorted ids) so `%w` is stable

No pass lowers Lintel IR to CUDA. No pass is InstCombine on Triton.

## Non-goals (still)

- Survey M3 / C6-A / LLM-as-`opt`.
- One cost model for L1–L7.
- Cake IR / Tile as the control IR.
- Interpreting Lintel IR or ADG on the serve path.
- Agent-written CFG or agent-written `%k` / `%w` fields.
- Deferring this list until a 10-person team “finishes linear v0.”
