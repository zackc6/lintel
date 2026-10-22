"""Validation gate for this contract repo (see AGENTS.md).

Every schemas/*.schema.json is a valid JSON Schema 2020-12, and every examples/**/*.json
parses. It does not assert that every example validates against a schema: examples/later/
and examples/poc/ carry known drift (see agentic-compiler docs/DRIFT.md). Exit 1 on failure.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
rc = 0
try:
    import jsonschema
except ImportError:  # keep the gate runnable without extras
    jsonschema = None
    print("note: jsonschema not installed; checking JSON parse only (pip install jsonschema)")

for p in sorted((ROOT / "schemas").glob("*.schema.json")):
    try:
        doc = json.loads(p.read_text())
        if jsonschema is not None:
            jsonschema.Draft202012Validator.check_schema(doc)
        print("ok  ", p.relative_to(ROOT))
    except Exception as e:
        rc = 1
        print("FAIL", p.relative_to(ROOT), e)

for p in sorted((ROOT / "examples").rglob("*.json")):
    try:
        json.loads(p.read_text())
    except Exception as e:
        rc = 1
        print("FAIL", p.relative_to(ROOT), e)
for p in sorted((ROOT / "examples").rglob("*.jsonl")):
    for i, line in enumerate(p.read_text().splitlines(), 1):
        if line.strip():
            try:
                json.loads(line)
            except Exception as e:
                rc = 1
                print("FAIL", f"{p.relative_to(ROOT)}:{i}", e)
print("examples parse:", "ok" if rc == 0 else "FAIL")
sys.exit(rc)
