# L-005 — Only golden and adapter failures can route to the next kernel

**Gap.** PoC `cond` edges exist for `hot`, `ok`, `worth_measure`; a *numerical* failure and a depth>2 retry are listed in `docs/LATER.md` §3 but the CFG grammar (`lintel-ir.poc.schema.json`) has no edge label for them.

**Carrier.** A CFG with `^try0 … gate numerical fail {where: numerical, seam: tol} → ^try1 → ^try2` (three allowlisted kernels) that compiles and interprets.

**Change.** Edge labels `{where, seam}` are an open set drawn from real gates (`adapter`, `golden`, `numerical`, `serving_ab`, `cost`); the allowlist depth is a policy field, not a constant 2.

**Falsifier.** A retry depth that is not bounded by the policy (unbounded search), or an edge whose `{where}` is not a gate the module declares. Survey item: C3, P5 (layered oracles).

**Loop.** application

**Depends on.** none

**Status.** open
