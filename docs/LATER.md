# Coverage after the PoC

The [PoC](POC.md) is the hard kernel on **one** graph. This file is how that kernel grows. Serve stays `lookup(%k)`. The controller-development module is item 7 and stays behind the gate in [SURVEY_MATCH.md](SURVEY_MATCH.md). Staffing does not delay the earlier items; sequence them by **dependency**, not by headcount.

## Already in the PoC (do not redo)

CFG with `cond`, `cost` as a gate, compile module → ADG, interpret ADG, `%k` replay, two **Choreo Kernels**, `adapter_gate` `{where: W|L|S|V}`.

## Extend in this order

### 1. Workflow key `%w` (next)

PoC freezes an ADG digest beside the admit record. Coverage makes that a first-class key. `%w` is the **compiled application workflow**, not the controller and not the memory snapshot.

| Key | Fields | Artifact |
|---|---|---|
| `%k` | graph, hw, compiler, adapter, `policy_id` | Application digest |
| `%w` | that same procedure, oracle bundle, \(F\), budget | ADG |
| `memory_id` | session / retrieval snapshot the procedure read | Audit only. Outside `%k` and `%w` |

`policy_id` **is** the controller procedure version. It already sits inside `%k`. Do not invent a second name for it and call that `%w`.

Triton/choreoir bump → new `compiler_ver` → new `%k`. A procedure bump (gates, \(F\), stopping rule, retrieval policy) → new `policy_id` → new `%w` and new `%k`. A longer log under the same retrieval rule → new `memory_id` only.

Sketch (fuller compile module): [examples/later/wf_acme_specialize.compile.lintel](../examples/later/wf_acme_specialize.compile.lintel).

**Need.** PoC ADG freeze is boring. **Exit.** Partner CI pins `@wf…` digest; same `%w` ⇒ same ADG or hard fail.

### 2. Policy hash = graph hash

PoC says the policy owns the CFG; coverage **enforces** it: `hash(ADG)` must equal `policy.graph_digest`. Extra blocks or edges from the model → `reject`.

**Need.** `%w`. **Exit.** A mutated `.lintel` that adds a `paste_cuda` edge is rejected before interpret.

### 3. More edges, same laws

| Add | Still illegal |
|---|---|
| `cond` on numerical fail → next kernel (not only golden / adapter) | Agent-authored edges |
| Triage ranks N regions; CFG per region or a dispatcher block | One mega-CFG the model writes |
| `or_else classical` as well as `last_good` | Dropping a required gate |
| Depth > 2 kernel tries, still allowlisted | Unbounded search / free AST search |

CFG sketch with the richer retry shape is already in [examples/later/acme_attn_prefill.cfg.lintel](../examples/later/acme_attn_prefill.cfg.lintel) (same graph as PoC; keep it as the coverage source of truth when PoC and coverage diverge).

### 4. Cost that is still not L1–L7

| Add | Still a non-goal |
|---|---|
| Budget from partner SLO, not a constant `usd=50` | Universal analytical model for every IR level |
| `worth_measure` uses last_good.F **and** canary GPU quote | Agent-chosen \(F\) |
| Record skip vs spend on the admit record | Silent skip with no audit |

Cost-only slice: [examples/later/acme_attn_prefill.cost.lintel](../examples/later/acme_attn_prefill.cost.lintel).

### 5. Second adapter / engine (width, not a new control IR)

New `adapter_id` or serving provider → new `%k`. Same Lintel IR, same ADG opcodes, new **Kernel schema** per adapter. Q3 stub adapter still valid; live second surface when a partner needs it.

Data-plane coverage (not a new Lintel IR): [DATA_PLANE.md](DATA_PLANE.md). Choreo remaining work: [CHOREO.md](CHOREO.md). `@cake.v0` / `@tirx.v0` / `@tilelang.ascend` are **wraps** — sketches: [cake-adapter.sketch.md](../examples/later/cake-adapter.sketch.md), [tilelang-ascend.sketch.md](../examples/later/tilelang-ascend.sketch.md). Sequence: one NVIDIA binary that **consumes** `Pipeline.depth`, then the second sink. Never the SKU.

### 6. Placement / multi-SKU (after `%w` is boring)

MARKET year-3 line: workflow freeze, then placement only when a profile shows the kernel row is not the limit ([SURVEY_MATCH.md](SURVEY_MATCH.md)). Only after partner CI runs frozen ADGs for one SKU. Kernel lowering stays classical. Serve stays `lookup(%k)`.

### 7. Controller-development module (after application wins and one compiler change)

This is the self-evolving loop of the **control** IR. It is not the PoC, and it is not item 1. Specify it so the procedure can be proposed and retained without pretending a session log already does that. Run it only after the gate in [SURVEY_MATCH.md](SURVEY_MATCH.md): repeated serving wins on partner traces, and at least one compiler change measured on a workload that did not motivate the patch.

Sketch: [examples/later/controller-dev.sketch.lintel](../examples/later/controller-dev.sketch.lintel). Laws: [LINTEL_IR.md](LINTEL_IR.md).

| Required | Forbidden in this first experiment |
|---|---|
| Delta is instructions or the retrieval **policy** | Editing \(F\), tolerances, or the required gate set |
| Compiler pin and model pin fixed for every arm | Bumping `choreoir` in the same comparison |
| Dev families and holdout families disjoint | Holdout traces in the proposer’s context |
| Freeze the candidate before holdout | Mid-walk rewrite of the ADG being evaluated |
| `promote` publishes `policy_id` only | `promote` calling `land` or writing a cubin |
| Four arms: fixed policy, memory-only, frozen procedure, conventional search | Recursive edit of the promoter itself |

**Exit.** On held-out families, at matched per-job budget, the frozen procedure beats the fixed policy on application performance or on search cost at the same performance, after development cost is disclosed. Otherwise `reject`, and the old `policy_id` stays what application jobs pin.

### 8. Intra-session verifier bundle (compiler data, not a controller)

Cake grows tactic/verifier rules inside a long session as data. Classify the bundle before hashing it:

| Bundle contents | Artifact | Identity |
|---|---|---|
| Extra `check` rules the pure function executes | Compiler | Hash beside `compiler_ver`, inside `%k` |
| A longer retrieval corpus, same retrieval rule | Memory | `memory_id` only |
| A new rule for which slot to try next | Controller | New `policy_id` |

Allowed later only if `check` stays a pure function with no LLM, the bundle hash is in the identity above, and nothing rewrites `check.py` while walking `^try0`→`^try1`. Until a real `{where}` corpus exists, route compiler changes through choreo PRs. Two allowlisted kernels are not that corpus.

## Compiler passes on Lintel IR (coverage)

PoC: check + lower to ADG. Coverage can add, still on the **control** graph:

- Unreachable-block reject (already implied by PoC checks)
- Dominates: `cache_key` before any terminator
- Edge labels must be `{where, seam}` from a real gate
- ADG canonical JSON (sorted ids) so `%w` is stable

No pass lowers Lintel IR to CUDA. No pass is InstCombine on Triton. Choreo `check` runs **in the adapter**, not as a Lintel IR pass.

## Non-goals (still)

- A model on the serve path, or dropping check and fallback.
- Mid-walk `check.py` rewrite. A verifier bundle is data with an identity, and `check` stays pure.
- Running the controller-development module before the gate, or calling a session log a self-improved controller.
- One cost model for L1–L7.
- Cake IR / Tile as the control IR, or as the year-1 live **face** (Choreo is the face; Triton is the printer).
- “Cake v2 the company” or “Choreo the company.” The adapter contract is already in the PoC.
- Interpreting Lintel IR, ADG, or Choreo on the serve path.
- Agent-written CFG or agent-written `%k` / `%w` fields.
- Deferring this list until a 10-person team “finishes linear v0.”
