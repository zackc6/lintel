# L-004 — An agent-authored CFG edge is not rejected before interpret

**Gap.** `docs/POC.md` says the policy owns the graph, but nothing enforces `hash(ADG) == policy.graph_digest`. A `.lintel` with an extra `paste_cuda` edge is interpretable today.

**Carrier.** `examples/later/acme_attn_prefill.cfg.lintel` plus a mutated copy with one added edge; the mutated copy must be `reject`ed at compile, with the edge named.

**Change.** Static check 8 in the PoC check list: ADG canonical JSON (sorted ids) digest must equal `policy.graph_digest`; mismatch → `reject {where: compile, reason: graph_digest}`.

**Falsifier.** Canonicalisation makes two semantically identical ADGs differ (false reject), or an added edge survives (false accept). Survey item: C3 (restricted actions), P22 (bounded LLM slots).

**Loop.** application (compile pass)

**Depends on.** L-003

**Status.** open
