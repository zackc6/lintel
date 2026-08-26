# Admit record (what you actually review)

This is the **merge ticket** for one specialize attempt. The kernel file is an attachment. If a field is not here, it did not happen.

The JSON is the **lowering** of a [Lintel IR](LINTEL_IR.md) module (`land` → `freeze`, `revert` → `fallback`). Machine JSON: [`examples/admit-record.json`](../examples/admit-record.json) (landed) · [`examples/admit-record.fallback.json`](../examples/admit-record.fallback.json) (reverted). Schema: [`schemas/admit-record.v0.schema.json`](../schemas/admit-record.v0.schema.json).

## Freeze (this one ships)

Partner already serves Llama-class decode on SGLang. Attention prefill is ~40% of GPU time. Overnight CI proposed one **allowlisted** [Choreo](https://github.com/zackc6/choreo) **Kernel AST** (partitions, layouts, Copy/Barrier/Mma, pipeline depth — not an opaque string). `choreoir.check` `{where}` gates passed. Oracles passed. Serving \(F\) is up ~8% with quality parity. They merge the digest, not the chat.

The machine JSON (full Kernel AST in `actions[]`) is [`examples/admit-record.json`](../examples/admit-record.json). Excerpt:

```json
{
  "schema_version": "admit-record.v0",
  "record_id": "rec_acme_attn_prefill_014",
  "pins": {
    "hw_id": "nvidia.b200.80gb",
    "compiler_ver": "choreoir==0.1.0;triton==3.3.0+cu128",
    "adapter_id": "choreo.v0",
    "model_id": "vendor.frontier.2026-10-20",
    "policy_id": "lintel.specialize.v0"
  },
  "actions": [
    {
      "kind": "propose_kernel",
      "enum_id": "choreo.attn.d3.w4",
      "kernel": { "name": "acme_attn_prefill_try0" }
    }
  ],
  "oracles": [
    { "name": "adapter.WLS", "result": "pass", "false_neg_owner": "kernels@acme" },
    { "name": "golden", "result": "pass", "false_neg_owner": "kernels@acme" },
    { "name": "numerical", "result": "pass", "false_neg_owner": "kernels@acme" },
    { "name": "serving_ab", "result": "pass", "false_neg_owner": "serving@acme",
      "detail": "sglang canary: output_parity=1, tokens_per_s +8.1% vs last_good" }
  ],
  "artifact": {
    "digest": "sha256:0e0ecbefe475d49eb85f80e704642376a3e52371d08ca370cd0071d9736290f9",
    "kind": "choreo_kernel",
    "uri": "git://acme/serving-kernels.git@c0ffee / kernels/attn_prefill_qkv.py"
  },
  "decision": "freeze",
  "fallback": "last_good"
}
```

## How to read it (compiler team)

| Field | Meaning | Why it is not “just a cubin in git” |
|---|---|---|
| `region.graph_hash` | Which IR/region this applies to | Revert and bisect target this hash, not a Slack thread |
| `pins` | HW + `choreoir` + sink + adapter + **model** + **policy** | Compiler bump or model swap is a new attempt, not a silent retune |
| `actions[].enum_id` + `kernel` | Allowlist slot + Choreo Kernel AST | Not free CUDA paste. Triton `num_warps` knobs are degenerate. If the slot is not allowlisted, it is not on the SLA path |
| `oracles[].false_neg_owner` | Who gets paged if this gate was wrong | Unnamed owner ⇒ that oracle cannot gate GA |
| `artifact.digest` | Bytes they serve | Serve path loads this. No LLM |
| `fitness` | Serving \(F\) vs last freeze, plus **$/compile** | Kernel microbench cannot freeze by itself |
| `cache_key` / `cache_key_digest` | Address of the specialize job (`%k`) | Serve is `lookup(%k)`. Model id is not in the key |
| `decision` / `fallback` | Lintel IR `land` / `revert` | Searcher death does not change serve |

**Cache key** `%k` is in the record (`cache_key` + `cache_key_digest`). Same key after a model swap must yield the same `decision` or **hard fail**. `model_id` is audit. Serve is `lookup(%k)`, not “run the agent again.”

## Fallback (this one does *not* ship)

Same region, different Kernel (`choreo.attn.d2.w8`). Kernel bench looked faster. Serving parity failed. `decision: fallback` — they keep serving the previous digest.

See [`examples/admit-record.fallback.json`](../examples/admit-record.fallback.json). The record still exists (audit). The serve path does not change.

## What you do *not* put here

```text
actions: [{ "kind": "paste_cuda", "enum_id": "void kernel() { ... }" }]   // illegal
oracles: [{ "name": "llm_said_ok", "result": "pass" }]                  // illegal (no owner, not an oracle)
fitness: { "delta": 2.1, "traces": ["one_hero_shape"] }                 // not a freeze
```

Chat, prompts, and “the model thought it was fine” can live in the session log. They are not this object.
