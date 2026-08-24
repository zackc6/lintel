# Later: CFG, cost, T10

**Not year-1 GA.** These sketches are not `lintel-ir.v0`. Do not interpret them on the SLA path. Do not sell them in the Q4 launch post.

Year 1 still **interprets one linear block**, pins a kernel at `%k`, and serves `lookup(%k)`. The classical compiler still lowers the **adapter IR** (Triton, later Tile / HIP / Cake IR). Lintel IR stays a control-plane contract, not `opt`.

Survey **M3** (LLM replaces the compiler) stays out. YEAR1 **M3** (Q3: two artifacts in partner git + replay) is a different letter. Do not mix them.

Examples: [examples/later/](../examples/later/). v0 contract: [LINTEL_IR.md](LINTEL_IR.md).

## What the compiler does on this IR

| When | On Lintel IR | On adapter IR |
|---|---|---|
| **Year 1** | Type-check + interpret + lower to admit record | Lower enum → kernel, measure |
| **Cost (year 2)** | Evaluate a pinned \(F\)/budget predicate; may skip A/B | Same |
| **CFG (year 2)** | Walk policy-owned blocks; edges are `{where, seam}` | Same |
| **T10 (year 3)** | Compile the plan to a frozen ADG at `%w` | Same |

Compiling the plan compiles the **controller**, not the kernel. Serve never runs Lintel IR or the ADG.

## Do this in order

Do not staff CFG, cost, and T10 as one SKU. Each phase has a gate. Skip a gate → the next phase is fiction.

```text
year-1 v0 interpret ──► cost-as-gate ──► CFG ──► T10 compile-the-plan
         │                  │              │              │
         │                  └──────────────┴──────────────┘
         │                         still lookup(%k) on serve
         ▼
   partner freeze + replay + $/admitted %F
```

### Phase 0 — Year 1 prep (no new opcodes)

Must already be true before any sketch becomes code. This is ordinary YEAR1 work, not a side IR.

| Need | Where it lives now | Why later phases need it |
|---|---|---|
| Interpret v0; `store[%k]`; replay law | Q1 | CFG/T10 must not change `%k` |
| Named false-neg owners; fallback fire-drill | Q1–Q2 | CFG edges are localized rejects, not chat |
| Serving \(F\) + `$/compile` on partner traces | Q2 | `cost` is the same \(F\) with a budget, not a new metric |
| `last_good` digest **and** last \(F\) stored at `%k` | Artifact store | `cost` / `fitness` compare against a real prior |
| `policy_id` pins required gates and \(F\) | v0 `pins` | T10 freezes that policy as `%w` |
| Session log is the interpretation trace | DSH pattern | Compiled ADG must replay to the same events |

**Do not** put `cond`, `cost`, or `compile plan` in `lintel-ir.v0`. **Do not** hire a “workflow compiler” on the 10-person team.

**Exit (already YEAR1 DoD).** Two partners, freeze, replay, `$/admitted %F` named. If that miss, stop. Later sketches stay paper.

### Phase 1 — Cost as a gate (year 2, after Q2 \(F\))

Sketch: [examples/later/acme_attn_prefill.cost.lintel](../examples/later/acme_attn_prefill.cost.lintel).

**Idea.** Year 1 writes `usd` on `land` after the fact. Year 2 evaluates **the same pinned \(F\)** plus a **budget** *before* `gate serving_ab`. If it cannot pay back, `revert` and do not spend the canary.

**Not.** A universal L1–L7 analytical model ([ARCHITECTURE.md](ARCHITECTURE.md) non-goal). Not a fitness the agent may rewrite.

| Work | Owner (25-person overlay) | Exit |
|---|---|---|
| Pin `budget.usd` / `gpu_hours` on `policy_id` | Control-plane | Policy bump = new `%k` (and later `%w`) |
| `cost` op: inputs `%p`, `last_good.F`, budget; output `worth_measure` | Control-plane + serving oracle | One partner skip recorded in admit record |
| Static check: `cost.F` == `policy.F` | Control-plane | Agent cannot change \(F\) to force measure |
| Keep linear-or-tiny CFG (`^ab` / `^skip` only) | — | No enum-retry graph yet |

**Kill.** Cost becomes a second fitness; or skip-A/B ships as default without an audit record.

**Staff.** Not a new team. Same control-plane + serving oracles that already own Q2 A/B.

### Phase 2 — CFG (year 2, after localized reject is boring)

Sketch: [examples/later/acme_attn_prefill.cfg.lintel](../examples/later/acme_attn_prefill.cfg.lintel).

**Idea.** Named blocks + `cond` on `hot` / `ok` / `pay`. A golden fail is an **edge** to the next allowlisted enum (or `revert`), not a prompt retry. The **policy owns the graph**. The agent still only fills `enum_id` / allowlisted triage.

**Not.** Agent-authored CFG (that is free rewrite of the controller — C3-A on the wrong plane). Not kernel CFG / Cake IR.

| Work | Owner | Exit |
|---|---|---|
| `lintel-ir.v1` sketch: blocks, `cond`, every path a terminator `under %k` | Control-plane | Spec + examples only until Phase 0 exit |
| Interpreter: block walk; no `goto` from the model | Control-plane | Enum retry on golden fail without chat |
| Static: agent cannot add blocks or edges | Control-plane | Reject module if plan text ≠ policy graph |
| Map `{where, seam, reason}` → edge | Adapter + oracles | Same reject shape as v0 gates |

**Kill.** LLM emits the CFG. Or serve starts interpreting blocks.

**Depends on.** Phase 0 reject strings; Phase 1 optional but `cost`/`cond` is the smallest CFG — ship that first if staffing is tight.

### Phase 3 — T10 compile the plan (year 3 / Horizon B)

Sketches: [examples/later/wf_acme_specialize.compile.lintel](../examples/later/wf_acme_specialize.compile.lintel), [examples/later/wf_acme_specialize.adg.json](../examples/later/wf_acme_specialize.adg.json).

**Idea.** Freeze the **controller** as an ADG/FSM artifact at a **workflow key `%w`**. Partner CI runs that ADG. A prompt cannot reorder gates. Kernel jobs still land at **`%k`**. Serve is still `lookup(%k)`.

`%w` is not `%k`:

| Key | Fields | Artifact |
|---|---|---|
| `%k` | graph, hw, compiler, adapter, policy | Kernel digest (year 1) |
| `%w` | controller, policy, oracle bundle, \(F\) | ADG / workflow (T10) |

Compiler bump of **Triton** → new `%k`. Change of **required gates / \(F\) / budget** → new `%w` (and new `%k` because `policy_id` is already in `%k`).

| Work | Owner (year-3 / 25–50 overlay) | Exit |
|---|---|---|
| `lintel-workflow.v1` sketch: `compile plan` → ADG | Control-plane | JSON ADG is what git reviews for the controller |
| Interpreter of frozen ADG (no `.lintel` text on SLA) | Control-plane | Partner CI pin `@wf…` digest |
| Replay: same `%w` ⇒ same ADG; same `%k` ⇒ same kernel terminator | Artifact / replay | Hard fail on either |
| Optional: pack interpreter as `dsh-plugin` if that ABI won | Runtime | Distribution, not a rewrite |
| Placement / multi-SKU only **after** ADG freeze is boring | Product | MARKET year-3 line; not this sketch |

**Kill.** ADG lowers to CUDA. Serve runs the ADG. Workflow compile sold as “we replace Inductor” (survey M3). Year 1 DoD never happened.

**Staff.** Do not take this from the 10-person GA team. Control-plane 4 at 25 people can start Phase 1–2. T10 is after adapter #2 or serving engine #2 is not on fire.

## Concrete checklist

**This plan repo (now)**

- [x] v0 linear examples + admit-record lowering
- [x] Later sketches under `examples/later/` (this doc)
- [ ] Do **not** add `cond` / `cost` / `compile` to `schemas/lintel-ir.v0.schema.json`

**Product repo, year 1 (the 10)**

- [ ] Interpret v0 only
- [ ] Persist `last_good.F` next to digest at `%k`
- [ ] Every failed gate carries `{where, seam, reason}`
- [ ] Q2: name `$/admitted %F`

**Product repo, year 2 (only if year 1 DoD)**

- [ ] Phase 1 `cost` behind the existing serving oracle
- [ ] Phase 2 CFG = policy graph; agent slots unchanged
- [ ] Second adapter still a new `adapter_id`, not a new control IR

**Product repo, year 3**

- [ ] Phase 3: freeze ADG at `%w`; SLA path runs ADG
- [ ] Same kernel `%k`; same serve `lookup(%k)`

## Non-goals (still)

- Survey M3 / C6-A / LLM-as-`opt`.
- One cost model for L1–L7.
- Cake IR / Tile as the control IR.
- Interpreting Lintel IR or ADG on the serve path.
- Agent-written CFG or agent-written `%k` / `%w` fields.
