# Stuck-review watchdog — JSON output schema (version 1)

This is the stable reference for the machine-parseable output of
`scripts/stuck-review-watchdog.py` when run with `--json` (or `--format json`).
A consumer can implement against this document without reading the script source.

## How to request the JSON output

```
python3 scripts/stuck-review-watchdog.py --json [--stale-minutes 120] [--dry-run]
```

`--json` and `--format json` are equivalent. When neither is given, the
human-readable report is emitted (unchanged) and no JSON is produced.

## Versioning

The document carries a top-level `schema_version` field. The current version
is `"1"`. If a consumer sees a `schema_version` it does not recognize, it MUST
treat the document as incompatible and fail loudly rather than mis-parse.

## Top-level document

| Field | Type | Description |
|------------------|--------|-------------|
| `schema_version` | string | Schema version identifier (currently `"1"`). |
| `run` | object | Run-level metadata (see below). |
| `status` | string | One of `ok_no_findings`, `ok_with_findings`, `error`. |
| `tickets` | array | List of stuck-ticket objects (may be empty). |
| `error` | object | Present only when `status` is `error` (see below). |

### `run` object

| Field | Type | Description |
|-------------|--------|-------------|
| `timestamp` | string | ISO 8601 UTC timestamp of the run. |
| `mode` | string | `"dry_run"` or `"alert"`, matching `--dry-run`. |

### `status` values

| Value | Meaning |
|--------------------|---------|
| `ok_no_findings` | Run succeeded; no stuck reviews were found. |
| `ok_with_findings` | Run succeeded; one or more stuck reviews were found. |
| `error` | Run failed (query error, parse error, or hard failure). |

### `tickets` array

Each element is a stuck-ticket object:

| Field | Type | Description |
|--------------|--------|-------------|
| `identifier` | string | Ticket identifier (or `"?"` if unknown). |
| `title` | string | Ticket title, truncated to ≤120 characters. |
| `reviewer` | string | Resolved reviewer name (or `"unknown reviewer"`). |
| `age_min` | number | Age in minutes, rounded to 0 decimals. |
| `reason` | string | Human-readable flag reason. |

### `error` object (present only when `status` is `error`)

| Field | Type | Description |
|-----------|--------|-------------|
| `reason` | string | Machine-readable error code: `query_failed`, `parse_error`, or `hard_failure`. |
| `message` | string | Human-readable detail. |

## Example

```json
{
  "schema_version": "1",
  "run": {
    "timestamp": "2026-09-05T08:31:00+00:00",
    "mode": "dry_run"
  },
  "status": "ok_with_findings",
  "tickets": [
    {
      "identifier": "T-100",
      "title": "Review the watchdog JSON contract",
      "reviewer": "Adversarial Engineer",
      "age_min": 145,
      "reason": "In in_review for 145 min with no verdict. Adversary may be down/paused."
    }
  ]
}
```

## Notes

- The document is emitted to stdout only when `--json`/`--format json` is
  requested. WARN diagnostics go to stderr and are never mixed into the JSON.
- The document is valid JSON in every path, including zero, one, or many
  tickets, and on failure.
- Field ordering and nesting are stable across runs.
