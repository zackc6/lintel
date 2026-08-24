# PoC — jump to the hard kernel

Linear `lintel-ir.v0` is too simple: the compiler only type-checks and interprets one block. **Year 1 builds the hard kernel first**, on a small set, then [extends coverage](LATER.md). Headcount is not a scope cap.

Serve is still `lookup(%k)`. Survey **M3** (LLM replaces the compiler) stays out. The classical compiler still lowers the **adapter IR**. This PoC is what the control-plane compiler *does* to Lintel IR: **walk a CFG, evaluate cost, compile the plan to an ADG**. Why that is worth doing: [WHY.md](WHY.md).

## Small set (proof)

One region, two allowlisted enums, three hard mechanisms:

| Mechanism | PoC cut | Why this is not a script |
|---|---|---|
| **CFG** | `cond` on `hot` / `ok` / `worth_measure`; golden fail → next enum | Localized reject is an **edge**. Policy owns the graph. Agent fills `enum_id` only |
| **Cost** | Same pinned \(F\) + budget **before** `serving_ab` | Can skip the canary. Agent cannot rewrite \(F\) |
| **Compile (T10 lite)** | Lower the module to a frozen ADG; SLA interprets the ADG | Git reviews the ADG. A prompt cannot reorder gates |

Examples:

- Source: [examples/poc/acme_attn_prefill.poc.lintel](../examples/poc/acme_attn_prefill.poc.lintel)
- JSON: [examples/poc/acme_attn_prefill.poc.json](../examples/poc/acme_attn_prefill.poc.json)
- Compiled ADG: [examples/poc/acme_attn_prefill.poc.adg.json](../examples/poc/acme_attn_prefill.poc.adg.json)
- Schema: [schemas/lintel-ir.poc.schema.json](../schemas/lintel-ir.poc.schema.json)

Degenerate linear land/revert stays under [examples/lintel-ir/](../examples/lintel-ir/) as one-block CFGs. Do not implement those first.

## What Q1 must build

1. **Well-formedness (compile).** Every block ends in `cond` or a terminator `under %k`. `cost.F` == `policy.F`. Agent slots ⊆ `{enum_id, triage.region}`. No kernel text. Output = ADG JSON + digest.
2. **Interpret the ADG**, not the `.lintel` text, on the SLA path. Fill slots → walk edges → `land` / `revert` / `reject`.
3. **Persist** `store[%k] = digest` on land; persist `last_good.F` next to it (cost needs a prior).
4. **Replay.** Same `%k` ⇒ same terminator and, if land, same digest. Same ADG digest ⇒ same graph. Else hard fail.
5. **Session log** is the walk (block id, edge, `{where, seam, reason}`).

Adapter work is unchanged: Triton lowers the chosen `enum_id`. Oracles own `ok` / fail. Serving A/B is Q2 on this same CFG (`^ab0` / `^ab1`); Q1 may stub `serving_ab` as skip-or-pass if the engine is not wired — **do not stub `cost` or `cond`**.

## Static checks (PoC)

1. `entry` reachable; every block reachable from `entry`; every path hits a terminator.
2. `cond` targets are block ids in this module.
3. Every terminator names `%k`.
4. `propose.enum_id` ∈ the two-enum allowlist for this policy.
5. Every `gate` has `owner`.
6. `cost.F` is pinned by `policy_id`; budget is on the policy, not the model.

## What the compiler does here

| Pass | On Lintel IR (PoC) | On adapter IR |
|---|---|---|
| Check | Well-formed CFG + `%k` laws | Enum is a legal schedule |
| Lower | Module → ADG (this is T10 lite) | Enum → kernel / PTX |
| Run | Walk ADG in CI | Measure / A/B |
| Serve | Nothing — `lookup(%k)` | Load frozen cubin |

Not InstCombine. Not Cake IR. Enough that “the IR is just a script” is false.

## Exit (PoC done)

- Internal run of the Acme graph: at least one **land** and one **revert** through different edges (golden fail → `^try1`, or cost skip, or parity fail).
- ADG digest in git next to the admit record.
- Replay after a model-id swap (same `%k`) holds.
- Fallback fire-drill still required.

Then extend coverage: [LATER.md](LATER.md). Do not wait for a headcount gate.
