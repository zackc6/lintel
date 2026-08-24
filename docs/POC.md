# PoC — jump to the hard kernel

Linear `lintel-ir.v0` is too simple: the compiler only type-checks and interprets one block. Opaque `enum_id` strings are the same trap on **L4**. **Year 1 builds both hard kernels first**, on a small set, then [extends coverage](LATER.md). Headcount is not a scope cap.

Serve is still `lookup(%k)`. Survey **M3** (LLM replaces the compiler) stays out. The classical compiler still lowers the **adapter IR** (Triton). This PoC is:

1. **Control:** walk a CFG, evaluate `cost`, compile the plan to an ADG.
2. **Data plane:** typed Triton **schedule record** + `adapter_gate` `{where}` — Cake *mechanisms*, not Cake IR. Spec: [DATA_PLANE.md](DATA_PLANE.md).

Why the control IR is worth doing: [WHY.md](WHY.md).

## Small set (proof)

One region, two allowlisted **schedule records**, four hard mechanisms:

| Mechanism | PoC cut | Why this is not a script |
|---|---|---|
| **CFG** | `cond` on `hot` / `ok` / `worth_measure`; adapter or golden fail → next schedule | Localized reject is an **edge**. Policy owns the graph. Agent fills allowlisted schedule fields only |
| **Cost** | Same pinned \(F\) + budget **before** `serving_ab` | Can skip the canary. Agent cannot rewrite \(F\) |
| **Compile (T10 lite)** | Lower the module to a frozen ADG; SLA interprets the ADG | Git reviews the ADG. A prompt cannot reorder gates |
| **Typed L4 (Cake-class)** | `propose` carries `schedule {num_warps, block_*, num_stages}`; `gate adapter` fails with `{where, hint}` | Not an opaque string. Not a new kernel language. Triton still lowers |

Examples:

- Control source: [examples/poc/acme_attn_prefill.poc.lintel](../examples/poc/acme_attn_prefill.poc.lintel)
- JSON: [examples/poc/acme_attn_prefill.poc.json](../examples/poc/acme_attn_prefill.poc.json)
- Compiled ADG: [examples/poc/acme_attn_prefill.poc.adg.json](../examples/poc/acme_attn_prefill.poc.adg.json)
- Triton schedule (`^try0`): [examples/poc/acme_attn_prefill.triton-schedule.json](../examples/poc/acme_attn_prefill.triton-schedule.json)
- Triton schedule (`^try1`): [examples/poc/acme_attn_prefill.triton-schedule.try1.json](../examples/poc/acme_attn_prefill.triton-schedule.try1.json)
- Adapter `{where: smem}` reject: [examples/poc/acme_attn_prefill.adapter-reject.json](../examples/poc/acme_attn_prefill.adapter-reject.json)
- Schemas: [schemas/lintel-ir.poc.schema.json](../schemas/lintel-ir.poc.schema.json), [schemas/adapter-proposal.v0.schema.json](../schemas/adapter-proposal.v0.schema.json)

Degenerate linear land/revert stays under [examples/lintel-ir/](../examples/lintel-ir/) as one-block CFGs. Opaque `num_warps=8.block_m=128` strings are the degenerate L4 form. Do not implement those first.

## What Q1 must build

1. **Well-formedness (compile).** Every block ends in `cond` or a terminator `under %k`. `cost.F` == `policy.F`. Agent slots ⊆ `{enum_id, schedule fields, triage.region}`. No kernel text. Output = ADG JSON + digest.
2. **Interpret the ADG**, not the `.lintel` text, on the SLA path. Fill slots → walk edges → `land` / `revert` / `reject`.
3. **Persist** `store[%k] = digest` on land; persist `last_good.F` next to it (cost needs a prior).
4. **Replay.** Same `%k` ⇒ same terminator and, if land, same digest. Same ADG digest ⇒ same graph. Else hard fail.
5. **Session log** is the walk (block id, edge, `{where, seam, reason, hint}`).
6. **Triton adapter.** Two allowlisted schedule records; `adapter_gate` before compile; `{where: smem|occupancy|compile_ok}` + optional `hint` field name. Triton lowers. Do not stub `adapter_gate`.

Oracles own golden / numerical `ok`. Serving A/B is Q2 on this same CFG (`^ab0` / `^ab1`); Q1 may stub `serving_ab` as skip-or-pass if the engine is not wired — **do not stub `cost`, `cond`, or `adapter_gate`**.

## Static checks (PoC)

1. `entry` reachable; every block reachable from `entry`; every path hits a terminator.
2. `cond` targets are block ids in this module.
3. Every terminator names `%k`.
4. `propose.enum_id` ∈ the two-slot allowlist; `propose.schedule` matches that slot’s record and the adapter schema.
5. Every `gate` has `owner`.
6. `cost.F` is pinned by `policy_id`; budget is on the policy, not the model.
7. `gate adapter` fail labels `{where}` from `{smem, occupancy, tma_align, compile_ok}`.

## What the compiler does here

| Pass | On Lintel IR (PoC) | On adapter IR |
|---|---|---|
| Check | Well-formed CFG + `%k` laws | Schedule fields are Triton-legal; `adapter_gate` `{where}` |
| Lower | Module → ADG (this is T10 lite) | Schedule → kernel / PTX (Triton) |
| Run | Walk ADG in CI | Measure / A/B |
| Serve | Nothing — `lookup(%k)` | Load frozen cubin |

Not InstCombine. Not Cake IR. Enough that “the IR is just a script” and “the adapter is just a string” are both false.

## Exit (PoC done)

- Internal run of the Acme graph: at least one **land**, one **revert** through a different edge (golden / parity / cost skip), and one **adapter_gate** fail with `{where: smem}` → `^try1`.
- ADG digest in git next to the admit record. Schedule record in the admit-record `actions[]`.
- Replay after a model-id swap (same `%k`) holds.
- Fallback fire-drill still required.

Then extend coverage: control [LATER.md](LATER.md); data plane [DATA_PLANE.md](DATA_PLANE.md) (Tile/HIP stub, optional `@cake.v0` wrap). Do not wait for a headcount gate.
