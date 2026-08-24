# Lintel

**A commercial compiler control plane for a 10–50 person team, deliverable in 12 months.**

Lintel is **not** a new `opt` / Inductor / Triton, and **not** a generic coding agent. It is the missing product between them: agents search and synthesize; classical compilers lower, measure, and fall back; Lintel owns the **typed contract, layered admit, freeze, and replay** so that loop can be sold.

This repo is a **year-1 plan**, not source code. It is derived from the 2026 agentic-compiler survey lean (hybrid control plane; jobs a–d; conflicts C1–C10; techniques T1–T10). Primary mechanisms come from [Cake](https://arxiv.org/abs/2608.12629) (typed agent-facing schedule + evolving harness) and [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (plugin kernel + append-only session log) — **composed as seams, not forked as the product**.

| Doc | What it answers |
|---|---|
| [docs/PRODUCT.md](docs/PRODUCT.md) | What we sell in year 1, and why Cake+DSH alone is the wrong SKU |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | How it is built so year 2–3 survey shifts are adapters, not rewrites |
| [docs/YEAR1.md](docs/YEAR1.md) | Quarterly plan, staffing 10 / 25 / 50, definition of done |
| [docs/MARKET.md](docs/MARKET.md) | Business value and competitors over 1–3 years |
| [docs/RISKS.md](docs/RISKS.md) | Kill switches tied to survey checkpoints |

**Year-1 SKU in one line.** CI/hot-path specialize on Amdahl-ranked kernels → layered admit → freeze a content-addressed artifact → serving A/B on one engine → classical fallback. Customer owns the artifact. No LLM on the serve path.

**What we refuse to sell in year 1.** “LLM replaces the compiler.” “Default-on for every build.” “One agent IR for all vendors.” Those fail the survey’s Horizon A ship column and will not survive release engineering.
