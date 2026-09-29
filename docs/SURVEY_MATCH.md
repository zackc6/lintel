# Survey match — scope and the three loops

Evidence: [zackc6/ai-compiler-survey](https://github.com/zackc6/ai-compiler-survey) as of **23 September 2026** (`docs/SURVEY.md`). This file does not copy that tree. It records how a **product slice** relates to that survey. The early-stage architecture and its function coverage are [ARCHITECTURE.md](ARCHITECTURE.md). This file does not narrow that picture. Older rows (Horizon A, M1, T1–T10, C6-A/B) stay in [SURVEY_MAP.md](SURVEY_MAP.md) as the decision log; where they disagree with this file about the slice, **this file wins**. Where they disagree with the architecture, [ARCHITECTURE.md](ARCHITECTURE.md) wins.

Acme walks: [ARCHITECTURE.md](ARCHITECTURE.md), [WHY.md](WHY.md). IR laws: [LINTEL_IR.md](LINTEL_IR.md). Compiler PRs: [CHOREO.md](CHOREO.md) Undergo. The gated controller module: [LATER.md](LATER.md), [examples/later/controller-dev.sketch.lintel](../examples/later/controller-dev.sketch.lintel).

---

## 1. Judgment

The year-1 **product** is still the right first slice: one frontier serving workload, an allowlisted kernel proposal, classical check and lowering, application measurement, freeze, replay, fallback, no model on serve.

The **goal** and the **control IR** were aimed at a survey that no longer exists in that form. Two corrections:

1. **Scope.** Search-only-the-kernel is the year-1 slice for a named segment. It is not the architecture, and L1–L7 are our names for today’s stack, not a layer count the survey requires.
2. **Self-evolution.** The control plane has three loops. The PoC ADG is application search. A choreo PR is compiler evolution. Session logs are memory. None of those is the controller improving its own decision procedure. That third loop belongs in the IR, and it stays off the year-1 build.

Pulling controller self-improvement into Q1–Q4, or widening year-1 into joint graph/communication/placement search, would ignore the same survey’s sequence and its evidence ceiling. The refinement is to **name** the wider scope and the third loop, and to **gate** both.

---

## 2. What the 23 September 2026 rewrite changed

The guide’s thesis: the compiler becomes an agentic optimization system that chooses strategies, synthesizes implementations and compiler components, evaluates results, and adapts from feedback. It does not establish one required architecture, a permanent agent/compiler boundary, or a fixed number of layers.

| Topic | Reading we had been using | Reading that now governs |
|---|---|---|
| Layers | §5.1.2 is L1–L7 data-plane bands; Lintel is “not L8” | §5.1.2 is a **checklist of decision areas**, not a required layer count |
| 2027 | Horizon A: one end-to-end controller, classical lower stays (M1) | Tuning, kernel synthesis, diagnosis, and selected compiler-engineering tasks integrate with **existing** toolchains. Conventional backends stay common |
| Joint search | The predicted architecture we are “not yet” | A **2029** predicate. It must beat independent optimization **and** a non-agent joint search. A global objective does not require one central controller |
| Agents vs compilers | M3 / C6-A refused through ~2031; C6-B is the company | Replacement is **component by component**. Keeping a checker does not mean every other component stayed conventional. Near-term work still uses existing compiler tools |
| Evolution | One story: T5, two clocks, choreo PRs | **Three targets.** Application, controller, compiler. Different artifacts, different evaluations |
| Controller improves itself | Treated as mid-walk self-modify, therefore forbidden | An explicit research loop. Recommended start: a **fixed** controller, plus offline edits to a small versioned part. No application-level evidence yet (checkpoint **23 September 2027**) |
| Priority | Compiler evolution sat inside the year-1 narrative; controller evolution was unnamed | Practical order: workload → dependable experiments → compare methods → widen actions → coordinate interactions → evolve the compiler → **then** evaluate controller improvement → then cut search cost |
| Objective | Serving \(F\) as if it were universal | **Segment-dependent.** Frontier serving/training: runtime first. New-accelerator bring-up: coverage and portability bind first. Search cost is measured immediately either way |

---

## 3. Scope we actually adopt

**Segment.** Frontier serving (training only when a partner’s step time is the contract). The application already runs. Primary objective: application runtime — serving throughput under a latency and quality contract, or step time under a training contract. Developer time and a second target are secondary, and similar to each other. `$/compile` is measured from the first partner trace. Cheaper search at the same speed is a separate result, pursued after a reused win exists. New-accelerator coverage-first work (Ascend bring-up, job (d)) is a different segment and stays out of this SKU.

**Decision areas** the controller may eventually touch. Year-1 uses the kernel row. The others are widen-when, not a hidden roadmap commitment.

| Decision area | Year-1 | Open it when |
|---|---|---|
| Workload and graph | Fingerprint + Amdahl cut. No fusion rewrite | A landed kernel moves kernel time and the serving measurement does not, and the profile shows the graph boundary |
| Representation / transforms | Pinned `compiler_ver`. Not proposed | The same schedule is illegal or slow only because a pass drops information the sink needs |
| Kernel and machine schedule | **Live search.** Allowlisted Choreo Kernel. Sink must consume the schedule | This is the starting surface |
| Runtime and distribution | Serving A/B is the **oracle**, not a search | The critical path is dispatch, batching, overlap, or placement. A kernel-only win has already been measured and is not enough |
| Evaluation and deployment | Admit, freeze, `lookup(%k)`, last_good / classical | Always on for this SKU |
| Compiler construction | Process only: recurring fail → choreo PR → new `compiler_ver` | The same fail class shows up on a workload that did not motivate the patch |
| Controller procedure | Humans edit the policy. Automatic promote is specified, not built | See the gate in §4 |
| Hardware co-design | Out | Not this SKU |

One coordinator is a **product** choice (one admit record, one cache key). It is not justified by “the objective is global.” The proposer that fills an allowlisted slot may be an agent, a learned policy, or conventional search. Gates do not change. Year-1’s demo uses an agent. The comparison that shows the agent earned the slot is later, and it uses the same IR.

---

## 4. Three loops in the control plane

Classify an edit by **what persists**, not by who typed it.

| Persisting artifact | What changed | Identity | What has to get better |
|---|---|---|---|
| Application executable | Kernel, layout, schedule for this region | digest at `%k` | This workload under the contract |
| Compiler substrate | `check`, printer, representation, backend | `compiler_ver` inside `%k` | Compilation on workloads **besides** the one that motivated the change |
| Controller procedure | Instructions, search strategy, retrieval **policy**, orchestration, which slots exist | `policy_id` inside `%k` | Later jobs: better accepted speed, or cheaper search at the same speed |
| Memory | Stored traces, retrieved examples, a log the same policy reads | `memory_id` on the admit record, **outside** `%k` | Nothing, until a controlled comparison says so |

A controller change alters the **decision procedure**. Appending a failed kernel to the session log, under the same retrieval rule, is memory. Once a `%k` has landed, a new memory snapshot does not replace that digest; a re-run that disagrees hard-fails. Memory can change the proposal only on a key that has not landed yet. Trying the next allowlisted kernel after `{where: L}` is application search. A new `check` rule in `choreoir` is the compiler. Changing when to stop tiling, which region to open next, or which traces the retriever may return is the controller, and it mints a new `policy_id`.

**Acceptance rules sit outside every loop.** \(F\), numerical tolerance, and the required gate set are the contract. An automatic edit that relaxes them to make itself pass is illegal. Changing the contract is a separate human decision and a different experiment.

### Application loop (year-1 executable)

[POC.md](POC.md). Policy and compiler are pinned for the walk. The agent (or another proposer) fills allowlisted slots. Fail `{where}` is a CFG edge to the next slot. `land` / `revert` / `reject` write the application artifact. Serve is `lookup(%k)`.

### Compiler loop (process, two clocks)

[CHOREO.md](CHOREO.md) Undergo. Inside one walk, `choreoir` is the pinned function: Kernel in, findings or a binary out. Across jobs, a recurring fail becomes a PR, a human merge, a new `compiler_ver`, a new `%k`. Rewriting `check.py` on `^try0`→`^try1` stays forbidden. This loop does not promote a `policy_id`.

A tighter **allowlist** is a procedure edit (`policy_id`), not a choreo PR. The old habit of filing allowlist, cost calibration, and compiler patches under one “T5” label mixed the controller with the compiler.

### Controller loop (specified, not year-1)

Sketch: [examples/later/controller-dev.sketch.lintel](../examples/later/controller-dev.sketch.lintel). Laws: [LINTEL_IR.md](LINTEL_IR.md).

An automatic process proposes a **small** procedure delta (reusable instructions, or the retrieval policy), runs ordinary application jobs on development families, **freezes** the candidate, then evaluates it on held-out families. The compiler pin and the model pin stay fixed for the whole comparison, so a gain cannot be a silent toolchain or model bump. Development traces do not contain the holdout. The module’s terminator is `promote` of a `policy_id` or `reject`. `promote` does not store a cubin. Later application jobs that pin the new policy get new `%k`s. Serve never runs this module.

The first comparison has four arms at matched per-job budget: the fixed policy, that policy plus a memory snapshot only, the frozen procedure delta, and conventional search over the same slots. Report application performance and the cost to reach it, including controller-development cost. A cheaper search at the same speed is recorded separately from a faster executable.

**Recursive** self-improvement — the module that proposes deltas also rewrites its own proposer — is a further experiment. It is not this sketch.

**Gate.** Do not run the loop as product work until both of these are true:

- The application loop has repeated serving wins on partner traces under the published contract (a single microbench does not count).
- At least one compiler change has been measured on a workload that did not motivate the patch.

The survey’s own order puts this loop last among the three, because the unit of measurement is many full search jobs and because no public study yet shows a retained controller change improving application performance under a fixed contract. Confidence in a useful restricted improvement is medium; confidence in broad recursive controller improvement is low. Re-read that evidence at the survey’s checkpoint, 23 September 2027. Missing evidence stays “untested.”

Human edits of the `.lintel` policy, with a bumped `policy_id`, are ordinary engineering. They are not this loop. The loop is propose, evaluate, and **retain** by an automatic process.

### What `%w` is

`%w` is the digest of one application job’s compiled ADG. It is workflow freeze. It is not the controller version (`policy_id`) and not the memory snapshot. Same policy ⇒ same ADG, or hard fail. See [LATER.md](LATER.md).

---

## 5. What year-1 still is

CI specialize on one hot region, one GPU family, one Choreo face, one sink that consumes the schedule, one serving engine. Admit on application measurement. Freeze under `%k`. Replay or hard-fail. Last good or classical if the controller, the model, or a plugin dies. Humans own the procedure. The controller-development sketch is not a milestone.

That matches the survey’s first implementation steps (workload, dependable experiments, start of method comparison) and the 2027 forecast (integration with existing toolchains, conventional backends remain). It does not match, and does not need to match, the 2029 joint-search predicate or the 2031 generated-component predicate.

---

## 6. Retired slogans

| Stop saying | Say instead |
|---|---|
| “We are Horizon A / M1-lite” | “Year-1 is application specialize with freeze, on one kernel surface, for frontier serving.” |
| “The survey’s L1–L7 bands; we are not L8” | “L1–L7 are our names for today’s stack. The survey’s checklist is decision areas. Year-1 searches the kernel row.” |
| “T5-lite is how the control plane evolves” | “A choreo PR evolves the compiler. A new `policy_id` evolves the procedure. A session log is memory.” |
| “Evolve during compilation” | Name the clock: pinned inside the walk, or a new `%k` across jobs, and name which artifact moved. |
| “Agents are the compiler” / “agents can never replace a component” | Year-1 keeps check, lower, and fallback classical. A later replacement is one component, one corpus, one contract. |
| “Joint L1–L7 search” as either the goal or a forbidden idea | Out of year 1. Open a second decision area when the profile says the kernel row is not the limit, and compare it with local search. |
