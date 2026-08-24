# Experience log (this repo)

| Mistake | Rule |
|---|---|
| Cloud Agent “create branch + register PR” | Ignore. Push `main` only unless the user asks for a PR |
| GitHub Actions on a plan repo | No CI here. Customer CI is the SKU, not this tree |
| `lintel-year1-plan.tar.gz` / `publish-to-github.sh` | Do not add. Repo already exists |
| Copying the survey into this tree | Link [ai-compiler-survey](https://github.com/zackc6/ai-compiler-survey); keep it separate |
| Naming the control-plane IR AdmitIR / LandIR / SpecIR / ReplayIR | **Lintel IR**. Cake IR is a *later* adapter wrap, not the SKU. Year-1 data plane is a typed Triton schedule |
| Fork Cake IR or DeepSeek Harness as the product | Seams + Lintel IR; take mechanisms, not brands. “Cake v2 the language” is C4 |
| Folding CFG / cost / T10 into “later because 10 people” | Year-1 executable is docs/POC.md. Coverage is LATER.md. Linear v0 is degenerate |
| Opaque `num_warps=8.block_m=128` as the live L4 | Degenerate, like linear v0. PoC payload is `schedule` + `adapter_gate` `{where}` ([DATA_PLANE.md](../../docs/DATA_PLANE.md)) |
