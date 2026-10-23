# L-012 — Triage ranks one region; the CFG has no dispatcher

**Gap.** PoC triage is `cond %r.hot` on one region. `docs/LATER.md` §3 wants N regions ranked by Amdahl share with a CFG per region or a dispatcher block; the grammar has no block kind for it, and a one-mega-CFG the model writes is forbidden.

**Carrier.** A module with three regions where only the top-ranked one reaches `propose`; the other two take `^cold`.

**Change.** `triage` returns a ranked list; a `dispatch` block fans out to per-region sub-modules, each with its own `%k`; the dispatcher itself is policy-owned (L-004).

**Falsifier.** Per-region keys collide, or the dispatcher needs an agent-written edge. Survey item: P23 (Amdahl), addressable-fraction evidence in the survey (§4.1).

**Loop.** application

**Depends on.** L-004

**Status.** open
