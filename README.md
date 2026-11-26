

# CivicPulse Phase 1: Data Foundation and Service Analytics
Client: Vidarbha Urja Vitaran Limited (Simulated)

## Role Ownership
| Role | Responsibility | Owner |
| :--- | :--- | :--- |
| **Loader** | Ingest raw docket & feeder files into staging | Swetha R |
| **Checks** | Validate schema, nulls, dates, and business rules | Swetha R |
| **Warehouse** | Build DuckDB tables over Parquet storage | Swetha R |
| **Measures** | Compute urban vs. rural restoration SLA metrics | Swetha R |
| **Dashboard** | Interactive Streamlit analytics app | Swetha R |
| **Report** | Executive findings & SLA breach summary | Swetha R |

## Run Pipeline
```bash
python pipeline.py --stage all
