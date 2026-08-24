# Lintel IR — control plane

**Lintel IR** is the control-plane IR. Cake IR is a schedule IR. Triton / Tile / HIP / Cake IR plug in behind `adapter`. They are not Lintel IR.

A module is one specialize plan at a cache key `%k`. The agent fills enumerated slots. The compiler owns lowering, measurement, and fallback. Serve does not interpret Lintel IR. Serve is `lookup(%k)`.

Terminators are ordinary English verbs: **land**, **revert**, **reject**.

| Terminator | Compiler reflex | Lowers to admit-record |
|---|---|---|
| `land %p under %k` | The patch landed; pin the `.o` | `decision: freeze` |
| `revert last_good under %k` | Revert; keep last good | `decision: fallback` |
| `reject {where, reason}` | Reject in review | `decision: reject` |

E2E stack: [ARCHITECTURE.md](ARCHITECTURE.md). Merge ticket: [ADMIT_RECORD.md](ADMIT_RECORD.md).

```text
  Agent fills ENUMERATED slots only
              │
              ▼
     Lintel IR (this document)         ← control plane
              │  %k = cache_key(...)
              │  interpret (year 1)
              ▼
     admit record JSON                 ← lowering (what git reviews)
              │
              ▼
     store[ %k ] = artifact.digest     ← serve is lookup(%k)
              │
     adapter IR  Triton · Tile · HIP · Cake IR
              │
              ▼
     classical lowering → serve
```

**Invariant.** Lintel IR never lowers to CUDA/HIP/PTX.

## Opcodes (v0)

| Op | Role | Agent may… |
|---|---|---|
| **`cache_key`** | Bind `%k` = hash(graph, hw, compiler, adapter, policy) | Not add fields; not put `model` or `enum_id` in the key |
| `triage` | Amdahl cut | Allowlisted regions only |
| `propose` | Bind `enum_id` from the adapter | Pick from the enum. No `paste_cuda` |
| `gate` | Oracle; fail → `{where, reason, seam}` | Not skip a required gate |
| `measure` | Bench / serving A/B | Not invent a number |
| `fitness` | Score vs last_good under pinned \(F\) | Not change \(F\) on the SLA path |

**Terminators** (exactly one) — all **under `%k`**:

| Terminator | Meaning |
|---|---|
| `land %p, %f under %k or_else last_good\|classical` | `store[%k] = digest(%p)`; that is what serves |
| `revert last_good\|classical under %k` | Keep previous `store[%k]` (or classical); this module is audit |
| `reject {where, reason} under %k` | Illegal program; serve path unchanged |

## Cache key (first-class)

Same idea as a compile-cache key (`ccache` / ThinLTO), plus **agent policy**. Not the kernel text.

```text
%k = cache_key @region, pins
```

```text
cache-key.v0 = { graph_hash, hw_id, compiler_ver, adapter_id, policy_id }
cache_key_digest = sha256(canonical_json)
```

| In `%k` | Out of `%k` |
|---|---|
| This graph on this HW / compiler / adapter / policy | `model_id` (audit) |
| | `enum_id` / kernel bytes (value *at* the key) |
| | commentary, SSA temps, `$/compile` |

**Replay law.** Same `%k` ⇒ same terminator and, if `land`, same digest. Else **hard fail**. Model swap + same policy = same `%k`. Compiler bump = new `%k` (must re-land).

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
    compiler = "triton==3.3.0+cu128"
    adapter  = @triton.v0
    model    = "vendor.frontier.2026-10-20"    // NOT in %k
    policy   = @lintel.specialize.v0
  }

  plan @specialize {
  ^entry:
    %k  = cache_key @attn_prefill, pins
    %r  = triage @attn_prefill
    %p  = propose propose_schedule "triton.attn.num_warps=8.block_m=128"
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
3. `propose.enum_id` ∈ adapter enum.
4. Every SLA `gate` has `owner`.
5. No opcode writes kernel text.
6. `fitness.F` is pinned by `policy`.

## Agent rights

| SLA (`mode=sku`) | Lab (`mode=lab`) |
|---|---|
| Fill `enum_id` / triage from allowlists | Looser propose; still no `land` without gates |
| Commentary | Same |
| **Cannot** add opcodes, drop gates, rewrite `%k` | Still cannot `land` without the SLA plan |

## Year 1 vs later

| When | Work |
|---|---|
| **Now** | Spec + examples; record lowering includes `%k` |
| **Q1** | Interpret one block; `store[%k]`; replay law |
| **Q3** | Second adapter = new enum / `adapter_id` (new keys), not a new IR |
| **Year 2–3** | Optional compile-the-plan (T10). Same `%k` |

## Non-goals

- Not Cake IR, Tile IR, Triton AST, or `opt`.
- Not one agent IR for all vendors (**C4**).
- Not a year-1 MLIR dialect in this plan repo.
- Not putting the LLM in `lookup(%k)`.
- Not re-interpreting this IR on the serve path.
