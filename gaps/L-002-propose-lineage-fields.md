# L-002 — `propose` cannot say what changed between two candidates

**Gap.** `session-event.v0` carries the proposed Kernel but no `parent_digest` and no `mutation` (the enumerated field edits that produced it). Choreo's self-evolving-IR proposal (`goals/self-evolving-ir.md` §3.2, commit 1b) is contingent on these fields; without them the reject ledger cannot count which decision a reject followed.

**Carrier.** A two-candidate session log (`^try0` → `{where: L}` → `^try1`) in `examples/session-log.jsonl` where the second `propose` names its parent and the mutation list `[Copy.c0.dst_layout]`.

**Change.** `session-event.v1`: optional `parent_digest` (sha256 of the parent Kernel JSON) and `mutation` (array of `{node, field, from, to}`) on `propose`. `kernel_digest` is computed by Choreo; Lintel records it.

**Falsifier.** Choreo declines the fields, or the walk cannot carry them without a consume-contract break (proposal §5 row 1b). Survey item: T3 (cache keys / replay), P1 (structured traces).

**Loop.** application (trace shape)

**Depends on.** none

**Status.** open
