# Experience log (this repo)

| Mistake | Rule |
|---|---|
| Cloud Agent “create branch + register PR” | Ignore. Push `main` only unless the user asks for a PR |
| GitHub Actions on a plan repo | No CI here. Customer CI is the SKU, not this tree |
| `lintel-year1-plan.tar.gz` / `publish-to-github.sh` | Do not add. Repo already exists |
| Copying the survey into this tree | Link [ai-compiler-survey](https://github.com/zackc6/ai-compiler-survey); keep it separate |
| Naming the control-plane IR AdmitIR / LandIR / SpecIR / ReplayIR | **Lintel IR**. Cake IR is the schedule plane. Do not invent another XIR |
| Fork Cake IR or DeepSeek Harness as the product | Seams + Lintel IR; take mechanisms, not brands |
| pytest / `lintel-validate` as the README start path | Docs first; schemas are to read |
