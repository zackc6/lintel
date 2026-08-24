# Admit record (what you actually review)

This is the **merge ticket** for one specialize attempt. The kernel file is an attachment. If a field is not here, it did not happen.

The JSON is the **lowering** of a [LandIR](LAND_IR.md) module (`land` → `freeze`, `revert` → `fallback`). Machine JSON: [`examples/admit-record.json`](../examples/admit-record.json) (landed) · [`examples/admit-record.fallback.json`](../examples/admit-record.fallback.json) (reverted). Schema: [`schemas/admit-record.v0.schema.json`](../schemas/admit-record.v0.schema.json).

## Freeze (this one ships)

Partner already serves Llama-class decode on SGLang. Attention prefill is ~40% of GPU time. Overnight CI proposed one **enumerated** Triton schedule. Oracles passed. Serving \(F\) is up ~8% with quality parity. They merge the digest, not the chat.

```json
{
  "schema_version": "admit-record.v0",
  "record_id": "rec_acme_attn_prefill_014",
  "prev_hash": "sha256:87930123062e3573ae3c9fa5f8662e25981b9b140ddc27a5eb158969f8dfa66d",
  "created_at": "2026-11-03T04:12:08Z",
  "commentary": "Optional prose for humans. Oracles, digest, and decision are the contract — not this sentence.",
  "region": {
    "region_id": "attn.prefill.qkv",
    "graph_hash": "sha256:bbcd57f9162e8a42bbf26df28a6b2a3ac2f8793061c036e198afeaf4f65d6db0",
    "op_family": "attention"
  },
  "pins": {
    "hw_id": "nvidia.b200.80gb",
    "compiler_ver": "triton==3.3.0+cu128",
    "adapter_id": "triton.v0",
    "model_id": "vendor.frontier.2026-10-20",
    "policy_id": "lintel.specialize.v0"
  },
  "actions": [
    {
      "kind": "propose_schedule",
      "enum_id": "triton.attn.num_warps=8.block_m=128"
    }
  ],
  "oracles": [
    {
      "name": "golden",
      "version": "0.1.0",
      "result": "pass",
      "false_neg_owner": "kernels@acme"
    },
    {
      "name": "numerical",
      "version": "0.1.0",
      "result": "pass",
      "false_neg_owner": "kernels@acme",
      "detail": "max_abs_err<1e-3 on shape_grid.attn.prefill.v3 (12 shapes)"
    },
    {
      "name": "serving_ab",
      "version": "0.1.0",
      "result": "pass",
      "false_neg_owner": "serving@acme",
      "detail": "sglang canary: output_parity=1, tokens_per_s +8.1% vs last_good, n=4h"
    }
  ],
  "artifact": {
    "digest": "sha256:0e0ecbefe475d49eb85f80e704642376a3e52371d08ca370cd0071d9736290f9",
    "kind": "triton_kernel",
    "uri": "git://acme/serving-kernels.git@c0ffee / kernels/attn_prefill_qkv.py"
  },
  "fitness": {
    "F_name": "serving.tokens_per_s * quality_parity",
    "baseline": 1.0,
    "delta": 0.081,
    "usd_per_compile": 38.4,
    "traces": ["acme.prod.decode.2026-10.sample", "acme.shape_grid.attn.prefill.v3"]
  },
  "decision": "freeze",
  "fallback": "last_good"
}
```

## How to read it (compiler team)

| Field | Meaning | Why it is not “just a cubin in git” |
|---|---|---|
| `region.graph_hash` | Which IR/region this applies to | Revert and bisect target this hash, not a Slack thread |
| `pins` | HW + Triton + adapter + **model** + **policy** | Compiler bump or model swap is a new attempt, not a silent retune |
| `actions[].enum_id` | The only legal move | Not free CUDA paste. If it is not in the enum, it is not on the SLA path |
| `oracles[].false_neg_owner` | Who gets paged if this gate was wrong | Unnamed owner ⇒ that oracle cannot gate GA |
| `artifact.digest` | Bytes they serve | Serve path loads this. No LLM |
| `fitness` | Serving \(F\) vs last freeze, plus **$/compile** | Kernel microbench cannot freeze by itself |
| `cache_key` / `cache_key_digest` | Address of the specialize job (`%k`) | Serve is `lookup(%k)`. Model id is not in the key |
| `decision` / `fallback` | LandIR `land` / `revert` | Searcher death does not change serve |

**Cache key** `%k` is in the record (`cache_key` + `cache_key_digest`). Same key after a model swap must yield the same `decision` or **hard fail**. `model_id` is audit. Serve is `lookup(%k)`, not “run the agent again.”

## Fallback (this one does *not* ship)

Same region, different enum (`num_warps=16`). Kernel bench looked faster. Serving parity failed. `decision: fallback` — they keep serving the previous digest.

See [`examples/admit-record.fallback.json`](../examples/admit-record.fallback.json). The record still exists (audit). The serve path does not change.

## What you do *not* put here

```text
actions: [{ "kind": "paste_cuda", "enum_id": "void kernel() { ... }" }]   // illegal
oracles: [{ "name": "llm_said_ok", "result": "pass" }]                  // illegal (no owner, not an oracle)
fitness: { "delta": 2.1, "traces": ["one_hero_shape"] }                 // not a freeze
```

Chat, prompts, and “the model thought it was fine” can live in the session log. They are not this object.
