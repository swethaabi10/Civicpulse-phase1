# CivicPulse Phase 1 — Technical Design Document
Client: Vidarbha Urja Vitaran Limited (VUVL) | Due: 1 December 2026

## 1. DuckDB Warehouse Tables (over Parquet)
* **`quarantine_dockets`**: Rows failing structure/business checks, preserved with `reason_code` and `source_file` so `rows_read = rows_loaded + rows_set_aside` (36,518 rows).
* **`dim_subdivisions`**: Master list of the 14 VUVL subdivisions plus `"Unallocated"`, mapped to `URBAN` / `RURAL` / `MIXED` tier.
* **`dim_categories`**: Valid complaint natures joined with allowed SLA hours from `VUVL_dockets_targets.csv` (excluding billing & new-connection).
* **`dim_calendar`**: Date dimension supporting daily, weekly (Monday review), and monthly regulatory reporting cuts.
* **`fact_dockets`**: Deduplicated, cleaned complaints (`DOCKET_NO`, `LOGGED_AT` adjusted to IST, `CLOSED_AT`, `NATURE`, `SUBDIVISION`, `FEEDER`, `CONS_CAT`, `is_planned_shutdown`, `is_batch_closed`, `is_sla_breached`). Personal data (`CONSUMER_NAME`, `CONTACT`) is dropped prior to storage.
* **`fact_feeder_events`**: Grouped no-supply dockets on the same `FEEDER` within a 30-minute window.
* **`fact_daily_backlog`**: Daily snapshot table recording dockets opened, closed, and still open (with age) at end of day by category and subdivision.

## 2. Row-Check Reason Codes & Handling Rules
| Reason Code | Rule / Condition | Action |
| :--- | :--- | :--- |
| `ERR_INVALID_TS` | `CLOSED_AT < LOGGED_AT` or unparseable timestamp | Quarantine row |
| `ERR_UNKNOWN_CAT` | `NATURE` does not match any known category | Quarantine row |
| `ERR_UNKNOWN_SUBDIV` | `SUBDIVISION` is not a valid VUVL subdivision (non-blank) | Quarantine row |
| `EXCL_TEST_ROW` | `NATURE = 'TEST'` | Exclude (not a valid docket) |
| `EXCL_OUT_OF_SCOPE` | `NATURE` is Billing or New Connection | Exclude per Section 5.2 |
| `EXCL_PLANNED_SHUTDOWN` | Docket logged during a scheduled feeder maintenance window | Flag & exclude from SLA KPI |
| `WARN_DUPLICATE_DOCKET` | Same `DOCKET_NO` logged via multiple channels | Deduplicate into 1 docket |
| `FIX_UNALLOCATED_SUBDIV` | `SUBDIVISION` is blank (~4% of rows) | Map to `"Unallocated"` (keep) |
| `FLAG_BATCH_CLOSURE` | No-supply `CLOSED_AT` at exact `08:00`, `16:00`, or `00:00` | Flag; report KPIs with & without |

## 3. Key Measures & Transformation Rules
* **August 2026 Timezone Fix:** Add `+5 hours 30 minutes` to `VUVL_dockets_2026_08.csv` timestamps (UTC to IST).
* **Restoration Clock:** Runs 24x7 from `LOGGED_AT` to `CLOSED_AT`; reopened dockets retain original `LOGGED_AT`.
* **SLA Metrics:** Median and 90th percentile restoration time (hours), plus `% restored within standard` (1 decimal on dashboard, 2 decimals on monthly statement).

## 4. Risks & Remaining Open Points
* **Pending Client Clarifications (Due 2–4 Dec):** Classification rule for the 3 mixed urban/rural subdivisions, agricultural (`AG`) consumer SLA tier, feeder-less event grouping, and exact restoration % threshold for multi-docket feeder events.
* **Data Quality Risks:** ~50% of no-supply rows have blank `FEEDER` codes, and shift-end batch closures inflate measured restoration times.
