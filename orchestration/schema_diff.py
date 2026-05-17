"""Detect breaking changes between helios-provenance-spec versions.

Run on every PR that modifies the schema. If a breaking change is detected
(per the JSON Schema 2020-12 compatibility rules), opens follow-up issues
in helios-spaceweather-connectors and helios-fusion-engine with migration
notes.

Implementation deferred to provenance-spec v0.2 (first non-RFC release).
"""
from __future__ import annotations

def diff(old_schema_path: str, new_schema_path: str) -> dict[str, list[str]]:
    raise NotImplementedError("Schema diff implementation pending v0.2 release of provenance-spec.")
