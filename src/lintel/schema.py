"""Validate admit records, session events, and replay cache keys."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator

SCHEMA_DIR = Path(__file__).resolve().parents[2] / "schemas"


class ReplayError(ValueError):
    """Same cache key produced a different admit decision — never serve."""


def _load_schema(name: str) -> dict[str, Any]:
    path = SCHEMA_DIR / name
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _validator(name: str) -> Draft202012Validator:
    return Draft202012Validator(_load_schema(name))


def validate_admit_record(record: Mapping[str, Any]) -> None:
    _validator("admit-record.v0.schema.json").validate(record)
    owners = [o.get("false_neg_owner", "") for o in record.get("oracles", [])]
    if any(not str(o).strip() for o in owners):
        raise ValueError("every oracle must name a false-negative owner")
    if "cache_key" in record:
        computed = cache_key_fields(record)
        if dict(record["cache_key"]) != computed:
            raise ValueError("cache_key does not match region+pins")
        if record.get("cache_key_digest") and record["cache_key_digest"] != cache_key(record):
            raise ValueError("cache_key_digest does not match cache_key")


def validate_session_event(event: Mapping[str, Any]) -> None:
    _validator("session-event.v0.schema.json").validate(event)
    if event.get("kind") == "gate" and not event.get("payload", {}).get("passed"):
        reject = event.get("payload", {}).get("reject")
        if not isinstance(reject, dict) or "where" not in reject:
            raise ValueError("failed gate must carry a localized reject (Cake contract)")


def cache_key_fields(record: Mapping[str, Any]) -> dict[str, str]:
    region = record["region"]
    pins = record["pins"]
    key = {
        "schema_version": "cache-key.v0",
        "graph_hash": region["graph_hash"],
        "hw_id": pins["hw_id"],
        "compiler_ver": pins["compiler_ver"],
        "adapter_id": pins["adapter_id"],
        "policy_id": pins["policy_id"],
    }
    _validator("cache-key.v0.schema.json").validate(key)
    return key


def cache_key(record: Mapping[str, Any]) -> str:
    payload = json.dumps(cache_key_fields(record), sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def assert_replay(previous: Mapping[str, Any], current: Mapping[str, Any]) -> None:
    """T3 invariant: same cache key ⇒ same decision, else hard fail."""
    if cache_key(previous) != cache_key(current):
        return
    if previous["decision"] != current["decision"]:
        raise ReplayError(
            f"cache key replayed with decision {previous['decision']!r} → {current['decision']!r}"
        )


def _iter_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Lintel contract artifacts")
    parser.add_argument("--admit", type=Path, help="admit-record JSON")
    parser.add_argument("--session", type=Path, help="session-event JSONL")
    args = parser.parse_args(argv)
    if not args.admit and not args.session:
        parser.error("pass --admit and/or --session")
    try:
        if args.admit:
            record = json.loads(args.admit.read_text(encoding="utf-8"))
            validate_admit_record(record)
            print(f"ok admit {args.admit} cache_key={cache_key(record)}")
        if args.session:
            events = _iter_jsonl(args.session)
            for event in events:
                validate_session_event(event)
            print(f"ok session {args.session} events={len(events)}")
    except Exception as exc:  # noqa: BLE001 — CLI boundary
        print(f"invalid: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
