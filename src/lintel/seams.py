"""Capability seams. Swap a provider without rewriting the controller.

DeepSeek Harness idea, compiler-shaped: definition + provider + consumer.
Year-1 code implements these names. Cake IR, Tile, HIP, Argus, DSH bundles
are later *providers*, not a fork of this module.
"""

from __future__ import annotations

from typing import Final, Literal

SeamName = Literal["llm", "tools", "session", "sandbox", "adapter", "oracle", "serving"]

SEAMS: Final[tuple[SeamName, ...]] = (
    "llm",
    "tools",
    "session",
    "sandbox",
    "adapter",
    "oracle",
    "serving",
)

YEAR1_PROVIDERS: Final[dict[SeamName, str]] = {
    "llm": "one frontier + one small specialist",
    "tools": "propose / verify / bench / profile",
    "session": "append-only event log (sqlite ok)",
    "sandbox": "container or Landlock for generated code",
    "adapter": "triton (home-fleet swap is a kickoff decision, not a rewrite)",
    "oracle": "golden + numerical + shape-grid",
    "serving": "sglang XOR vllm — pick in week 1",
}
