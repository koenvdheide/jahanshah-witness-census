# Search Artifact Status

This directory preserves historical search-session JSON files. Older files do not all share the same top-level schema: v1.0 sweeps often wrap details under `search_session`, while v1.1 probes usually use top-level `session_label`, `session_id`, `date`, and `summary` fields.

Use `index.json` for current-status questions. Each record declares whether the artifact is a current authority, whether it is superseded by another file, and whether it leaves a release blocker open. The historical files remain useful as evidence, but `index.json` is the routing layer for resolving apparent contradictions between intermediate probes and later syntheses.
