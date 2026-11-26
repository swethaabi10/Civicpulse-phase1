# CivicPulse Phase 1 — Technical Design Document

## 1. DuckDB Warehouse Tables
* **`raw_dockets`**: Raw ingested CSV/Parquet records for 12 months of consumer complaints.
* **`quarantine_dockets`**: Rejected rows failing validation checks, tagged with `reason_code`.
* **`dim_feeders`**: Master reference table of feeders, zones, and consumer area classification (`URBAN` / `RURAL`).
* **`fact_dockets`**: Cleaned dockets excluding planned shutdowns, joined with SLA targets and `is_sla_breached` flags.
* **`mart_sla_summary`**: Aggregated restoration times and breach rates by region, feeder, and urban/rural tier.

## 2. Row-Check Reason Codes
| Reason Code | Rule Description | Action |
| :--- | :--- | :--- |
| `ERR_NULL_ID` | `docket_id` or `consumer_id` is null/empty | Quarantine row |
| `ERR_INVALID_TS` | `restored_at` is earlier than `raised_at` | Quarantine row |
| `ERR_UNKNOWN_AREA` | Area type is neither `URBAN` nor `RURAL` | Quarantine row |
| `EXCL_PLANNED_SHUTDOWN` | Docket occurred during a scheduled maintenance window | Exclude from SLA KPI |
| `WARN_DUPLICATE_DOCKET` | Duplicate `docket_id` detected | Deduplicate keeping latest |
