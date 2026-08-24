# Why Lintel IR (discussion, with examples)

The data plane already compiles and serves without us. This note is what the **control-plane IR** is for, what cash it moves, and how the Acme PoC shows that on survey L1–L7.

E2E stack and the band map: [ARCHITECTURE.md](ARCHITECTURE.md). Unit economics: [MARKET.md](MARKET.md). Executable IR: [POC.md](POC.md).

## 1. It already works without this IR

Torch → Inductor / Triton → PTX → SGLang or vLLM already lowers, serves, and falls back. Autotune, a YAML job, CompileIQ ACFs, GEAK workflows, or a coding agent in a sandbox can all propose a faster kernel.

**Without Lintel IR you still have a compiler.** You do not have a product you can freeze, replay, and sell when an LLM is on the *specialize* path. If you never put an agent in CI, you do not need this IR.

| Without Lintel IR | With it |
|---|---|
| Classical compile + serve | Unchanged — we do not replace L1–L7 |
| Agent is a script or chat: skip a gate, paste CUDA, reorder steps | Closed opcodes. Agent fills `enum_id` only |
| Cache key is informal; model swap silently retunes | `%k` first-class. Same key ⇒ same terminator or **hard fail** |
| Easy to re-run the agent on the serve path | Serve is `lookup(%k)` |
| Git reviews a kernel diff or a transcript | Module **lowers** to an admit record |
| Fail is an exit code | `{where, seam, reason}` is a CFG **edge** |
| Cost is a comment after the fact | `cost` can skip L6 A/B before spend |
| Plan is whatever the prompt emitted | Compile to ADG; policy owns the graph |

The IR is **T1 + T2 + T3** (typed interface, layered admit, pin-at-`%k` + replay). It is not “how kernels compile.” Cake IR / Triton still do **L4**. `opt` still does **L3/L5**.

**Survey M3** (LLM replaces the compiler) is out. **YEAR1 M3** (Q3: two artifacts in partner git + replay) is a milestone, not that cell.

## 2. What we benefit (cash language)

Win condition is product **\(F\)**: serving tokens/s (or TTFT) × quality parity × **$/compile**. Not KernelBench.

| Lever | What moves | Honest year-1 size |
|---|---|---|
| **Serving performance** | Hot-path specialize under \(F\), then freeze | **3–12%** tokens/s (or TTFT) on the hot kernel, parity → ~**1–5% e2e** if Amdahl is honest. Hero 2× on one shape is not the sale |
| **Token / compile spend** | Serve has **zero** LLM tokens. Specialize spends only on hot regions that pass `cost` | Big win is *not* a cheaper chat. It is no agent on every request, no search on cold kernels, no silent re-search on model swap |
| **Kernel engineer-weeks** | Humans review an admit record, not 200 diffs | Target: **1–3 days** to admitted kernel vs ~two-week Triton archaeology. Partner bill today: ~6–10 weeks/drop × 4 drops/year |
| **Release risk** | Layered oracles + last_good / classical; fire-drill | A faster microbench that fails parity **does not serve** |
| **Replay / upgrades** | Same `%k` after compiler or model pin change | Same decision or hard fail — never a silent new kernel |
| **Lock-in** | L4 DSL is an `adapter` | Triton now; Tile / HIP / Cake IR later; same Lintel IR |

**Buy test.** Price < ~0.5 kernel FTE **and** a serving delta they can put on a dashboard. If we only move a microbench, they should not buy.

We do **not** claim: default-on for every build, beat cuBLAS on all families, unique global e2e optimum, or cheaper chat than Copilot. If the only meter is tokens, we have packaged a coding agent and we lose on price.

## 3. E2E (two paths, same `%k`)

```text
 L1–L2 graph ── triage / graph_hash
 L3–L5 classical lower of L4 enum (Triton …)
 L6 serve lookup(%k)
 L7 place (not in PoC)
        │
        ▼
 Lintel IR ── compile → ADG ── walk in CI ── admit record
 serve never walks the ADG
```

Full diagram: [ARCHITECTURE.md](ARCHITECTURE.md) (stack + L1–L7 table).

## 4. Concrete walks (Acme attn prefill)

Same region `attn.prefill.qkv`, same graph hash `sha256:bbcd57f9…`, same `%k` digest `sha256:ec25e38a…` (model id is **not** in the key).

Source: [examples/poc/acme_attn_prefill.poc.lintel](../examples/poc/acme_attn_prefill.poc.lintel).  
Compiled: [examples/poc/acme_attn_prefill.poc.adg.json](../examples/poc/acme_attn_prefill.poc.adg.json).

### Walk A — land (serving \(F\) up, then zero LLM)

Lowering: [examples/admit-record.json](../examples/admit-record.json).

```text
^entry  triage hot
^try0   propose num_warps=8.block_m=128     ← L4 enum only
        gate golden, numerical              ← after L5 cubin
        cost worth_measure
^ab0    serving_ab pass  (+8.1% tokens/s, parity=1)
^fit0   land under %k    usd_per_compile=38.4
serve   lookup(%k) → sha256:0e0ecbef…       ← L6, no LLM
```

**Benefit.** ~8% on this hot kernel (plan: 3–12% class) with parity; **serve path burns no tokens**. Humans merge the admit record, not the chat.

### Walk B — revert (risk: faster bench, bad parity)

Lowering: [examples/admit-record.fallback.json](../examples/admit-record.fallback.json).

```text
^try1   propose num_warps=16.block_m=64
        golden + numerical pass
^ab1    serving_ab fail { where = serving.output_parity, reason = "3/1000" }
        → revert last_good under %k
serve   still lookup(%k) → previous digest
```

**Benefit.** Kernel bench looked faster (+11% in the record). We **do not serve it**. That is the risk lever. The module is audit.

### Walk C — cost skip (token / GPU, not a new \(F\))

PoC CFG: after numerical, `cond %c.worth_measure, ^ab0, ^try1` (or `^giveup`).

```text
^num0   cost vs last_good { F = tokens/s × parity, budget.usd = 50 }
        worth_measure = false  →  ^try1   // do not run L6 A/B
```

**Benefit.** Same pinned \(F\); we refuse to spend the canary. Not a universal L1–L7 cost model.

### Walk D — cold region (Amdahl / tokens)

```text
^entry  cond %r.hot, ^try0, ^cold
^cold   revert last_good under %k
```

**Benefit.** No propose, no LLM search, no A/B on a kernel that is not the hot path (P23).

### Walk E — model swap, same `%k` (replay)

`model = "vendor.frontier.…"` is on `pins` for audit. It is **out of `%k`**. Re-walk the same ADG after a searcher swap: terminator and landed digest must match or **hard fail — do not serve**.

**Benefit.** No silent retune. Compiler bump (`triton==3.3.0` → next) is a **new** `%k` and must re-land.

## 5. Band cheat-sheet (same walks)

| Walk step | Band | IR |
|---|---|---|
| `region` / `graph` | L1→L2 | identity in `%k` |
| `triage` / `^cold` | L1 cut | skip search |
| `propose` enum | L4 | Triton schedule, not CUDA text |
| `gate golden/numerical` | L4 after L5 | cubin oracles |
| `cost` | control | skip L6 spend |
| `gate serving_ab` / `land` | L6 | freeze; serve = lookup |
| `place` | L7 | not in PoC |

Lintel IR never lowers to CUDA. L3/L5 stay classical. L0 / job (b) never appears.

## 6. What “the compiler does” on *this* IR

| Pass | Control IR | Adapter (L4→L5) |
|---|---|---|
| Check | Well-formed CFG, `%k` laws, `cost.F` == policy | Enum is a legal schedule |
| Lower | Module → ADG | Enum → kernel / PTX |
| Run | Walk ADG in CI | Measure / A/B |
| Serve | Nothing | Load frozen cubin |

Enough that the IR is not a shell script. Not InstCombine. Not survey M3.
