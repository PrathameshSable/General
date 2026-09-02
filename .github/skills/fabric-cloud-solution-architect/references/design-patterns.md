# Fabric Design Patterns Reference

Implementation guidance for the 36 patterns summarised in `SKILL.md`. Each entry gives the intent, how to build it in
Fabric, when **not** to use it, and which Well-Architected pillars it serves
(**R** Reliability, **S** Security, **CO** Cost, **OE** Operational Excellence, **PE** Performance).

---

## Storage & Data Layout

### Medallion Layering — OE, R
- **Intent:** predictable data quality tiers; every consumer knows what a layer guarantees.
- **Build:** Bronze Lakehouse (raw, append-only, source-aligned, load-date partitioned) → Silver Lakehouse (typed,
  deduplicated, SCD, conformed keys) → Gold Warehouse or Lakehouse (star schema, business measures). Emory-style
  Platinum only when a curated review/submission layer is contractually required.
- **Avoid when:** a POV with one source and one dashboard — a Bronze + Gold two-layer is acceptable if stated.
- **SOW hook:** each layer becomes a workstream / SIT gate in the WBS.

### Shortcut over Copy — CO, OE
- **Intent:** one physical copy of data.
- **Build:** OneLake shortcuts to ADLS Gen2, S3, GCS, Dataverse, Iceberg tables, or tables in other workspaces.
  Use Trusted Workspace Access for firewalled storage accounts.
- **Avoid when:** the source is volatile and you need an immutable audit copy (then land into Bronze), or when
  cross-cloud egress cost exceeds storage cost.

### Mirroring over Pipelines — CO, OE, PE
- **Intent:** eliminate ingestion pipelines for supported OLTP sources.
- **Build:** Mirrored database item → tables appear as Delta in OneLake; query via SQL analytics endpoint or Direct Lake;
  shortcut mirrored tables into the Bronze/Silver Lakehouse for downstream transforms.
- **Avoid when:** source is unsupported, requires column-level filtering not offered by mirroring, or network policy
  blocks the required connectivity. Note the lift-and-shift caveat: mirroring replaces ingestion, not transformation.

### Delta Table Hygiene — PE, CO
- **Build:** enable V-Order on serving tables; schedule `OPTIMIZE` (weekly or after large loads) and `VACUUM`
  (7-day retention default); set Spark `optimizeWrite` / Auto Compaction; target 128 MB–1 GB files.
- **Avoid when:** never — but do not run OPTIMIZE on every micro-batch.

### Partition by Load Date, Cluster by Query Key — PE
- **Build:** Bronze partitioned by `ingest_date`; Silver/Gold either unpartitioned or coarsely partitioned (year/month)
  to keep Parquet file and row-group counts within Direct Lake guardrails.
- **Avoid when:** high-cardinality partition keys (customer ID) — creates the small-file antipattern.

### Schema Enforcement & Evolution — R, OE
- **Build:** Bronze accepts drift (schema-on-read, `mergeSchema` for additive columns); Silver enforces expected schema
  with a validation notebook; breaking changes route to quarantine and raise an Activator alert.

### Lakehouse Schemas — OE
- **Build:** enable schemas on Lakehouses (`bronze.sales_orders`, `silver.customer`); map to subject areas; simplifies
  security scoping and naming.

### Materialized Lake Views — OE, PE
- **Build:** `CREATE MATERIALIZED LAKE VIEW gold.fact_sales AS SELECT ...` in Spark SQL; Fabric manages the dependency
  graph, lineage and scheduled/incremental refresh.
- **Avoid when:** logic needs procedural steps or external calls — use a Notebook.

---

## Ingestion & Integration

### Watermark Incremental Load — PE, CO
- **Build:** control table `etl.watermark(source, table, last_value, last_run)`; pipeline Lookup → Copy with
  `WHERE modified > @last_value` → Stored procedure / notebook updates watermark on success only.
- **Avoid when:** source lacks a reliable modified column — use CDC or hash-compare full loads.

### CDC / Change Feed — PE, R
- **Build:** SQL Server CDC → Copy job (CDC mode) or Copy activity; Dataverse Link for D365; mirroring change feed for
  supported DBs. Apply changes into Silver with `MERGE` keyed on business key + operation type.

### Metadata-Driven Orchestration — OE, CO
- **Build:** config table listing sources, tables, load type, target, dependencies; one parent pipeline with `ForEach`
  over the config; child pipeline per pattern (full, incremental, file). Emory's "dependency framework" is this pattern.
- **Avoid when:** fewer than ~10 sources with different shapes — over-engineering.

### Copy Job for Simple Movement — OE
- **Build:** Copy job item for many-table SQL → Lakehouse/Warehouse moves with built-in incremental/CDC options.

### On-Prem Gateway Pattern — R, S
- **Build:** gateway cluster (2+ nodes) on VMs sized for throughput; dedicated service account; gateway per environment
  or shared with connection-level isolation. Record node sizing as a SOW assumption.

### Dead-Letter & Quarantine Zone — R, OE
- **Build:** `Files/quarantine/<source>/<run_id>/` plus a `etl.rejects` table with reason codes; nightly summary via
  Activator → Teams.

### Idempotent Re-run — R
- **Build:** overwrite-by-partition for Bronze, `MERGE` for Silver/Gold, run IDs in every row, watermark updated only
  on success, pipelines safe to re-execute from any activity.

---

## Transformation & Modelling

### Notebook for Complex, SQL for Set-Based — PE, OE
- **Build:** decide per workload: R scripts, SSIS script tasks, procedural SQL → PySpark; set-based joins/aggregations
  into Warehouse → T-SQL stored procedures. Document the rule so the team does not mix arbitrarily.

### SCD Type 2 in Silver — R
- **Build:** `effective_from`, `effective_to`, `is_current`, hash of tracked columns; `MERGE` with close-and-insert.
  Gold dimensions read `is_current = true` unless as-of reporting is required.

### Star Schema Gold — PE
- **Build:** conformed dimensions with surrogate keys, facts at a documented grain, date dimension, no snowflaking.
  Direct Lake performs best on wide, flat dimensions.

### Aggregation Tables — PE, CO
- **Build:** pre-aggregated Gold tables for hot KPIs (daily sales by store) so common visuals never scan billion-row facts;
  keep base fact for drill-through.

### Spark Environment Pinning — OE, R
- **Build:** Environment item with pinned Python libraries, Spark version, pool sizing; attach as workspace default;
  promote through deployment pipelines.

### Native Execution Engine — CO, PE
- **Build:** enable NEE in the Environment / session; validate compatibility of UDFs; measure CU savings on the
  largest jobs.

---

## Serving & Semantic Layer

### Direct Lake Semantic Model — PE, CO
- **Build:** create the model over Gold tables (Lakehouse or Warehouse); keep tables within per-SKU guardrails
  (see `capacity-sizing.md`); avoid computed columns and views; monitor fallback with Performance Analyzer / DAX Studio.
- **Avoid when:** model requires features unsupported by Direct Lake (calculated tables, some RLS on views) — use
  composite.

### Certified Semantic Model for Copilot — S, OE
- **Build:** descriptions on every table/column/measure, synonyms, KPI display folders, hidden technical columns,
  "Prep data for AI" settings, endorsement = Certified. This is the deliverable that makes Copilot POVs succeed.

### Composite Model for Edge Cases — PE
- **Build:** Direct Lake storage-mode tables + Import for small reference tables or DirectQuery to SQL database for
  live/write-back tables.

### Report-to-Model Separation — OE, CO
- **Build:** one shared semantic model per subject area in a "models" workspace; reports live-connect from consumer
  workspaces/apps; no duplicated models per report.

### Translytical Write-back — OE
- **Build:** User Data Function invoked from a Power BI button/slicer writes to SQL database in Fabric; SQL database is
  mirrored back to OneLake for analytics.

---

## Governance & Security

### Domains & Workspace Taxonomy — OE, S
- **Build:** Domain per business area (Clinical, Finance…); workspaces `prd-clinical-gold`, `dev-clinical-bronze` etc.;
  item naming standard; owners = Entra groups.

### OneLake Security + RLS/OLS — S
- **Build:** OneLake security roles restrict tables/folders for engineers and shortcuts; semantic-model RLS/OLS for
  consumers; Warehouse RLS via security predicates when T-SQL consumers exist.

### Sensitivity Labels & Purview Scan — S, OE
- **Build:** default label policy; auto-labelling by classification; Purview scans Fabric tenant for lineage and catalog;
  PHI classification review before Prod.

### Private Link + Managed VNet — S
- **Build:** tenant Private Link; managed private endpoints from Spark to private Azure sources; block public access;
  verify feature limitations before committing in the SOW.

### Customer-Managed Keys — S
- **Build:** workspace-level CMK with Azure Key Vault; key rotation runbook; scope to workspaces that hold regulated data.

---

## Operations & Capacity

### Capacity per Environment / Workload — R, CO
- **Build:** at minimum Prod vs Non-Prod; add a serving-only capacity for executive/regulated dashboards; assign
  workspaces deliberately; document in the capacity table.

### Schedule into Smoothing Windows — CO, PE
- **Build:** run batch 00:00–05:00 local; stagger refreshes; avoid top-of-hour; use pipeline dependencies instead of
  clock schedules downstream.

### Surge Protection & Throttling Alerts — R
- **Build:** capacity admin sets surge protection thresholds for background operations; Activator alert on Capacity
  Metrics (>80 % sustained) and on throttling events.

### Git + Deployment Pipelines + Variable Library — OE
- **Build:** Dev workspace ↔ `main`/feature branches; PR merges; deployment pipeline Dev → Test → Prod with deployment
  rules; Variable Library for lakehouse/warehouse IDs and connection names per stage.

### Workspace Monitoring & Log Analytics — OE
- **Build:** enable Workspace Monitoring on Prod (query logs, refresh logs to an Eventhouse); send Spark logs to Log
  Analytics; dashboards for failed runs, long queries, CU by item.

---

## Pattern selection by engagement archetype

| Archetype (see `templates/fabric-domain-reference.md` §9) | Patterns to include by default |
|---|---|
| Assessment + POV (4–6 wk) | Medallion (2–3 layer), Watermark load, Direct Lake, Certified model for Copilot, Git basic, naming taxonomy |
| Phase 1 Lift & Shift (13 wk) | Medallion Bronze/Silver, CDC / Dataverse Link, Idempotent re-run, Capacity per env, Git + Deployment pipelines |
| Phase 2 Native Rebuild (28 wk) | Full medallion, SCD2, Star schema Gold, Aggregation tables, Direct Lake, RLS/OLS, MLVs, Workspace Monitoring, Surge protection |
| Dual workstream (Emory) | Metadata-driven orchestration, Platinum layer, Quarantine zone, Purview scan + labels, CMK/Private Link if PHI |
| T&M extension | Delta hygiene, Report-to-model separation, Translytical write-back POV, Data Agents POV |
