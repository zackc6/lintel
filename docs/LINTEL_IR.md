# Lintel IR — control plane

**Lintel IR** is the control-plane IR of a next-generation agentic compiler ([ARCHITECTURE.md](ARCHITECTURE.md)). The architecture’s function coverage and three loops live there. This document is the application-walk language: one job, pinned contract, pinned procedure, pinned compiler.

A representation the proposer may edit is a **[Choreo](https://github.com/zackc6/choreo) Kernel AST** ([DATA_PLANE.md](DATA_PLANE.md), [CHOREO.md](CHOREO.md)). A mapping to hardware consumes the schedule (roles, barriers, `Pipeline.depth`) and emits a binary. `print_triton` that comments those fields is not that mapping. Other representations plug in behind `adapter`. They are not Lintel IR.

A module is one application plan at a cache key `%k`. The [PoC](POC.md) is one executable module (CFG + `cost` + compile to ADG) on a kernel surface. A linear block is a CFG with one `^entry`. A proposer — agent, learned policy, or structured search — fills candidates. Gates, measurement, and fallback stay on this plan, and the plan **compiles to an ADG**. Deploy does not interpret Lintel IR. Deploy is `lookup(%k)`.

Terminators are ordinary English verbs: **land**, **revert**, **reject**.

| Terminator | Compiler reflex | Lowers to admit-record |
|---|---|---|
| `land %p under %k` | The patch landed; pin the `.o` | `decision: freeze` |
| `revert last_good under %k` | Revert; keep last good | `decision: fallback` |
| `reject {where, reason}` | Reject in review | `decision: reject` |

E2E stack: [ARCHITECTURE.md](ARCHITECTURE.md). Merge ticket: [ADMIT_RECORD.md](ADMIT_RECORD.md).

```text
  Proposer fills candidates
  (agent, learned policy, or structured search)
              │
              ▼
     Lintel IR (this document)         ← application walk
              │  %k = cache_key(...)
              ▼
     admit record JSON                 ← what git reviews
              │
              ▼
     store[ %k ] = artifact.digest     ← deploy is lookup(%k)
              │
     representation (Choreo Kernel, or another adapter)
              │
              ▼
     map to hardware → deploy
```

**Invariant.** Lintel IR does not lower to CUDA, HIP, or PTX. `propose` submits a candidate in a representation. Checks on that representation stay ordinary functions. Pins: [LLM_IR.md](LLM_IR.md). Compiler changes and procedure changes are the other two loops in [ARCHITECTURE.md](ARCHITECTURE.md), not extra opcodes on this walk.

## Opcodes (v0)

| Op | Role | A proposer may… |
|---|---|---|
| **`cache_key`** | Bind `%k`. Architecture: hash(workload, hw, compiler, adapter, policy, contract). v0 examples: graph, hw, compiler, adapter, policy, with the contract pinned in the module | Not put `model` or the candidate body in the key. Not move \(F\) by editing `policy_id` |
| `triage` | Choose scope from the profile | Open a decision area the contract allows |
| `propose` | Bind a candidate in the active representation | PoC: two allowlisted Choreo Kernels. Architecture: a configuration or a synthesized candidate, same gates. Triton knobs are a degenerate candidate |
| `gate` | Check matched to the action; fail → `{where, reason, seam}` | Not skip a required check |
| `measure` | Kernel time, application metric, and search cost | Not invent a number. Report speed and search cost apart |
| `fitness` | Score vs last_good under the pinned contract | Not change \(F\) |

**Terminators** (exactly one per path) — all **under `%k`**:

| Terminator | Meaning |
|---|---|
| `land %p, %f under %k or_else last_good\|classical` | `store[%k] = digest(%p)`; that is what serves |
| `revert last_good\|classical under %k` | Keep previous `store[%k]` (or classical); this module is audit |
| `reject {where, reason} under %k` | Illegal program; serve path unchanged |

PoC adds `cost`, `cond`, and named blocks. Spec: [POC.md](POC.md). Linear v0 is one block with a terminator.

## Cache key (first-class)

Same idea as a compile-cache key (`ccache` / ThinLTO), plus **agent policy**. Not the kernel text.

```text
%k = cache_key @region, pins
```

```text
cache_key = hash( workload_id, hw_id, compiler_ver, adapter_id, policy_id, contract_id )

cache-key.v0 examples = { graph_hash, hw_id, compiler_ver, adapter_id, policy_id }
cache_key_digest = sha256(canonical_json)
```

| In `%k` | Out of `%k` |
|---|---|
| This workload on this HW / compiler / adapter / policy / contract | `model_id` (audit) |
| `policy_id` versions the **decision procedure** (search rules, retrieval policy, which areas and slots exist, stopping). It does not version \(F\) or the required checks | `memory_id` — stored traces the same procedure reads. Audit on the admit record |
| `contract_id` versions the objective, tolerances, and required checks. v0 modules pin that text in the module; a procedure edit must not move it | `enum_id` / candidate bytes (value *at* the key) |
| | **`Kernel.target`** — admission is `pins.hw_id`, not another key field |
| | commentary, SSA temps, `$/compile` |

**Replay law.** Same `%k` ⇒ same terminator and, if `land`, same digest. Else hard-fail. Model swap + same policy + same contract = same `%k`. Compiler bump, `policy_id` bump, or `contract_id` change = new `%k` (must re-land). A new `memory_id` under the same `policy_id` is the same `%k`, and it does not authorize a second digest. Memory may change proposals only on a key that has not yet landed. A re-interpret that disagrees still hard-fails.

## Three artifacts the control plane versions

The opcodes in this document are the application loop. The compiler loop and the controller loop are not extra opcodes on that walk. Judgment: [SURVEY_MATCH.md](SURVEY_MATCH.md).

| Edit | Persists as | In the architecture |
|---|---|---|
| Next candidate after `{where}` | Application digest at `%k` | Application loop. The PoC uses two allowlisted kernels |
| Append a fail to the session log; same retrieval rule | `memory_id` (not in `%k`) | Memory. Not a new controller |
| Human edits the search rules, the allowlist, or the stopping rule | New `policy_id`, new `%k` | A procedure edit. Not the automatic loop |
| Automatic propose → freeze → holdout → `promote` of a `policy_id` | New `policy_id` | Controller loop. Sketch below. A product slice may wait to run it |
| New check, transform, or a mapping that consumes the schedule | New `compiler_ver`, new `%k` | Compiler loop ([CHOREO.md](CHOREO.md)). Not a mid-walk rewrite |
| Relax \(F\) or `max_abs_err` so a candidate passes | — | Illegal for every automatic loop. A human opens a new experiment with a new `contract_id` |

`promote` is not `land`. `land` stores an application digest. `promote` publishes a procedure that later application jobs may pin. Serve never interprets a controller-development module.

The first automatic delta is reusable **instructions** or the **retrieval policy**. It is not agent code, not a new opcode, not `check.py`, and not the contract. Compiler pin and model pin stay fixed for the comparison (attribution). Development traces exclude the holdout families. Four arms, matched per-job budget: fixed policy, fixed policy plus memory only, frozen procedure, conventional search on the same slots.

Sketch (not `lintel-ir.poc`, no schema change in year 1): [examples/later/controller-dev.sketch.lintel](../examples/later/controller-dev.sketch.lintel). Entry conditions: [LATER.md](LATER.md).

**Serve.** `lookup(%k)`. Miss or hard-fail → last_good or classical. No LLM.

## Acme example (`land`)

[examples/lintel-ir/acme_attn_prefill.lintel](../examples/lintel-ir/acme_attn_prefill.lintel) → [examples/admit-record.json](../examples/admit-record.json).

```text
module @rec_acme_attn_prefill_014 version "lintel-ir.v0" {

  region @attn_prefill {
    region_id = "attn.prefill.qkv"
    graph     = sha256:bbcd57f9162e8a42bbf26df28a6b2a3ac2f8793061c036e198afeaf4f65d6db0
    op_family = attention
  }

  pins {
    hw       = "nvidia.b200.80gb"
    compiler = "choreoir==0.1.0;triton==3.3.0+cu128"
    adapter  = @choreo.v0
    model    = "vendor.frontier.2026-10-20"    // NOT in %k
    policy   = @lintel.specialize.v0
  }

  plan @specialize {
  ^entry:
    %k  = cache_key @attn_prefill, pins
    %r  = triage @attn_prefill
    %p  = propose propose_kernel "choreo.attn.d3.w4"
    %g0 = gate golden     %p owner @kernels.acme
    %g1 = gate numerical  %p owner @kernels.acme { max_abs_err = 1e-3 }
    %g2 = gate serving_ab %p owner @serving.acme
    %f  = fitness %g2 vs last_good { F = "serving.tokens_per_s * quality_parity" }
    land %p, %f under %k { usd = 38.4 } or_else last_good
  }
}
```

`%k` digest: `sha256:ec25e38a28d690828ecd63234173704d013c7062aa3e919ba5d31765831c35d7`.

Revert (parity fail) — same `%k`, terminator `revert`: [examples/lintel-ir/acme_attn_prefill.revert.lintel](../examples/lintel-ir/acme_attn_prefill.revert.lintel).

```text
    %g2 = gate serving_ab %p owner @serving.acme
      // fail { where = serving.output_parity, reason = "3/1000 mismatch" }
    revert last_good under %k
```

Serve still `lookup(%k)` → previous digest.

## Static checks

1. `cache_key` fields are exactly the v0 set. `model` or `enum_id` in the key → `reject`.
2. Every terminator names `%k`.
3. `propose.enum_id` ∈ adapter allowlist; `propose.kernel` matches the slot (PoC). Linear v0 may omit `kernel` (degenerate).
4. Every SLA `gate` has `owner`.
5. No opcode writes kernel text.
6. `fitness.F` is pinned by `policy`.

## Agent rights

| SLA (`mode=sku`) | Lab (`mode=lab`) |
|---|---|
| Fill `enum_id` / `kernel` / triage from allowlists | Looser propose; still no `land` without gates |
| Commentary | Same |
| **Cannot** add opcodes, drop gates, rewrite `%k` | Still cannot `land` without the SLA plan |

## Year 1 vs later

| When | Work |
|---|---|
| **Now** | Linear v0 (degenerate) + [PoC](POC.md) CFG/cost/ADG + Choreo Kernel AST. Humans own `policy_id` |
| **Q1** | Compile PoC module → ADG; interpret ADG; `store[%k]`; replay; `adapter_gate` `{where: W\|L\|S\|V}` |
| **Q3** | Second adapter = new enum / `adapter_id` (new keys), not a new IR |
| **After the gate in SURVEY_MATCH** | Controller-development sketch may be run. Not a schema bump of `lintel-ir.poc` |
| **After PoC exit** | Coverage: `%w` as the ADG digest, policy-hash, more edges ([LATER.md](LATER.md)). Same kernel `%k` fields |

## Non-goals

- Not Cake IR as the SKU (year-1 L4 is Choreo; [DATA_PLANE.md](DATA_PLANE.md), [CHOREO.md](CHOREO.md)).
- Not one agent IR for all vendors (**C4**). Choreo is the face; sinks are per vendor.
- Not a year-1 MLIR dialect in this plan repo. Not vendoring `choreoir/` here.
- Not putting the LLM in `lookup(%k)`.
- Not re-interpreting this IR **or Choreo** on the serve path.
- Not shipping linear-only interpret as the year-1 IR. The executable contract is [POC.md](POC.md). Coverage is [LATER.md](LATER.md).
