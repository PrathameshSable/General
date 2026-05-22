# Microsoft Fabric Domain Reference

A consolidated cheat-sheet of Microsoft Fabric concepts, terminology, and pricing — used by all four agents on the presales team to ensure consistent technical accuracy across deliverables.

---

## 1. Fabric workloads (canonical list)

| Workload | Purpose | Typical use in our SOWs |
|---|---|---|
| **OneLake** | The single logical data lake underlying Fabric. All data lives here. | Always referenced. Bronze/Silver/Gold layers all sit on OneLake. |
| **Lakehouse** | File-and-table hybrid storage (Delta Parquet). | Bronze (raw ingestion), Silver (transformed). |
| **Warehouse** | SQL-first analytic warehouse on OneLake. | Silver (staging) or Gold (star-schema marts). Lids uses "Bronze Warehouse" for staging. |
| **Data Factory** | Pipeline orchestration + ingestion. Replaces ADF. | All ingestion / orchestration. Use "Fabric Data Factory" or "Fabric Data Pipelines". |
| **Synapse Data Engineering** | Spark notebooks (PySpark, SparkSQL). | Complex transforms, R-to-Notebook conversions, ML feature engineering. |
| **Synapse Data Science** | ML model development on Fabric. | Rarely in scope for migration SOWs; relevant for AI-readiness conversations. |
| **Synapse Data Warehouse** | The Fabric Warehouse SQL endpoint. | Gold-layer warehouse, T-SQL queries. |
| **Real-Time Intelligence** | KQL Eventhouse, Eventstream, streaming. | Rarely in migration SOWs; relevant when client mentions Kusto/ADX. |
| **Power BI** | Reporting and Semantic Models. | Always in scope. Use "Direct Lake" mode for OneLake-backed semantic models. |
| **Data Activator** | No-code event-driven actions. | Niche; mention if client has alerting requirements. |
| **Purview** | Data governance, catalog, lineage. | Increasingly common — Emory Purview SOW is the reference. |
| **Copilot in Fabric** | Generative AI assistant across Fabric workloads. | POV value driver — always called out in assessment SOWs. |
| **Copilot in Power BI** | NL Q&A on semantic models. | POV value driver — requires Certified Semantic Model with KPI display folders. |

---

## 2. Capacity SKUs and pricing

Fabric capacity is bought in F-SKUs. Pricing here is Pay-As-You-Go USD/hour (as of late 2025); reservations cut cost ~40%.

| SKU | CU (Capacity Units) | Hourly | Monthly (730h) | Typical use |
|---|---|---|---|---|
| **F2** | 2 | $0.36 | $263 | Dev sandbox, demos |
| **F4** | 4 | $0.72 | $526 | **Assessment / POV default** |
| **F8** | 8 | $1.44 | $1,051 | Small POV / shared dev |
| **F16** | 16 | $2.88 | $2,102 | Small migration dev |
| **F32** | 32 | $5.76 | $4,205 | Medium dev/QA |
| **F64** | 64 | $11.52 | $8,409 | **Small implementation prod**, medium QA |
| **F128** | 128 | $23.04 | $16,819 | **Medium-large EDW** (Lids Phase 1/2 ref) |
| **F256** | 256 | $46.08 | $33,638 | Large enterprise EDW |
| **F512** | 512 | $92.16 | $67,277 | Large multi-domain enterprise |
| **F1024** | 1024 | $184.32 | $134,554 | Multi-tenant / very large enterprise |
| **F2048** | 2048 | $368.64 | $269,107 | Extremely large enterprise |

OneLake storage: $0.023/GB/month (similar to ADLS Gen2). Compute is the dominant cost.

**Sizing heuristics for SOW capacity planning:**
- <1 TB source data, <50 reports: F64
- 1–10 TB source data, 50–200 reports, EDW migration: F128
- 10–50 TB, multi-domain enterprise: F256
- >50 TB or strict SLA: F512+

---

## 3. Medallion Architecture

Standard 3-layer:
- **Bronze** — Raw ingestion. Lakehouse. Delta Parquet. Schema-on-read tolerance. Append-only typical.
- **Silver** — Cleaned, conformed, deduplicated. Lakehouse or Warehouse. Business rules applied. (Lids uses "Bronze Warehouse" as a staging variant — non-standard.)
- **Gold** — Curated star-schema marts. Warehouse. Subject-area aligned. Direct Lake-ready for Power BI Semantic Models.

Emory 4-layer variant adds:
- **Platinum** — Review-ready curated presentation layer. Used in clinical/regulated environments.

---

## 4. Common source systems we migrate FROM

| Source | What it is | Migration pattern |
|---|---|---|
| **SQL Server on-prem** | Legacy OLTP / EDW | Direct ingest via Fabric Data Pipeline (Copy) or via on-prem Data Gateway |
| **Azure Synapse Analytics** | Microsoft's prior data platform | Lift-and-shift to Fabric Warehouse; pipelines repointed |
| **AAS (Azure Analysis Services)** | Tabular semantic models | Migrate to Fabric Semantic Model with Direct Lake |
| **Azure Data Factory (ADF)** | Pipelines | Repoint to use Fabric as source/sink OR rebuild as Fabric Data Pipelines |
| **Tableau** | Reporting | Rebuild in Power BI |
| **Domo** | Reporting | Rebuild in Power BI (Apex pattern) |
| **Epic Clarity / Caboodle** | Healthcare EHR data marts | Ingest tables to Bronze Lakehouse, rebuild marts in Gold |
| **Salesforce / D365 / Workday** | SaaS | Use Fabric connectors / Dataverse Link |
| **SSIS / Legacy ETL** | Pipelines | Rebuild as Fabric Data Pipelines + PySpark notebooks |

---

## 5. Common consumers/integrations

- **Power BI Desktop / Service** — Primary reporting consumer
- **Power BI Copilot** — NL Q&A; requires Certified Semantic Model
- **Excel via Power BI Analyze in Excel** — Self-service analysts
- **Teams / SharePoint** — Power BI embed
- **Operational write-back systems (e.g., ScalziDB)** — Fabric pipelines push curated data back to OLTP

---

## 6. CI/CD on Fabric

- **Git integration** — Fabric workspaces can sync to Azure DevOps / GitHub repos. Item-level versioning.
- **Deployment pipelines** — Native Fabric feature for Dev → Test → Prod promotion. Configured per workspace.
- **Fabric APIs** — REST APIs for programmatic deployment (used in advanced CI/CD).

Standard environments: Dev, QA/Test, Prod (sometimes Prod-Dev / Prod-Test / Prod-Prod for staged migrations — Lids pattern).

---

## 7. Security and governance

- **Workspace roles** — Admin, Member, Contributor, Viewer
- **OneLake Security** — Item-level + folder-level permissions on OneLake
- **Row-Level Security (RLS)** — In Power BI Semantic Models
- **Object-Level Security (OLS)** — In Power BI Semantic Models
- **Sensitivity labels** — Via Purview, applied to Fabric items
- **Private Endpoints** — For tenant-restricted network access (healthcare, finance)
- **Customer-Managed Keys (CMK)** — For BYOK encryption
- **Purview integration** — Auto-scanning of Fabric workspaces, lineage to source systems, classification, glossary

---

## 8. Microsoft Funding Mechanisms (presales-critical)

| Mechanism | Typical Amount | When to use | How it appears in SOW |
|---|---|---|---|
| **Partner Led Funding (PLF)** | $15,000 (POV-level) | Assessment / POV stage | "Microsoft Partner Led Funding" column in pricing table; reduces customer cost. APEX pattern. |
| **Azure Accelerate Partner Led Funding** | $75,000 against $250K+ ACR commitment | Larger POV or early implementation | Same column structure; requires customer to commit to annual Azure consumption |
| **ACMA (Azure Consumption Migration Accelerator)** | $250K+ Azure credits | Implementation phase | Applied via amendment to MSA, not in original SOW. Note pending status in SOW. |
| **Partner Investment** | ~30% of total cost | Any phase | "Partner Investment" line — Santor absorbs to make customer-net price competitive (LIDS-2 pattern) |

Always confirm with the user which funding applies before drafting the pricing table.

---

## 9. Engagement archetypes (cheat sheet)

| Archetype | Duration | Total Cost | Team Size | Key Markers |
|---|---|---|---|---|
| Assessment + POV (APEX) | 4 wks | $10–30K customer-net | 3–4 part-time | Parallel WS, Partner Funding, follow-on SOW deliverable |
| Dual POC (NYULH) | 6 wks | $0 (no-cost) | 3 part-time | "No-cost to customer", PoC showcase |
| Phase 1 Lift & Shift (LIDS-1) | 13 wks | $185K | 9 | Bronze + Silver only, ADF repoint, no rebuild |
| Phase 2 Native Rebuild (LIDS-2) | 28 wks + 4 wk HC | $387K | 9 | 5 releases, subject-area decomposition, Gold + Semantic rebuild, DevOps added |
| Dual WS Migration (Emory) | 20 wks | $540K | 10–12 | WS1 Data Eng + WS2 Power BI, 4-layer medallion (Platinum), MSA-anchored |
| T&M Extension (ACME) | 3 mo | $30K | 1.1 FTE | Hourly rates, Net 15, monthly invoicing, "4-hour overlap" |

---

## 10. Vocabulary normalization

When the brief uses casual terms, map them to canonical Fabric language in the SOW:

| Brief says | Use in SOW |
|---|---|
| "Data lake" | OneLake (or "Lakehouse on OneLake") |
| "Data warehouse" | Fabric Warehouse / Synapse Data Warehouse |
| "ETL" | Fabric Data Pipelines (or "ingestion + transformation") |
| "Dashboards" | Power BI reports / Power BI dashboards |
| "Cubes" | Fabric Semantic Models (Direct Lake mode) |
| "Data catalog" | Purview Unified Catalog |
| "AI / chatbot" | Copilot in Fabric / Copilot in Power BI |
| "Real-time" | Real-Time Intelligence (Eventhouse, KQL) |
| "Lineage" | OneLake lineage + Purview lineage |
| "Synapse" | Azure Synapse Analytics → migrate to Fabric (workloads native) |

---

## 11. Anti-patterns to avoid in SOWs

- Never recommend importing data INTO Power BI (always use Direct Lake on a Semantic Model)
- Never say "ETL"; say "ingestion + transformation" or "Fabric Data Pipelines"
- Never promise sub-second query latency without F-SKU sizing justification
- Never include "ad-hoc support" as a deliverable (it's open-ended — use Hypercare with a 4-week cap instead)
- Never promise "Copilot will answer any question" — scope to Semantic Model + Certified KPI measures
- Don't conflate Fabric Capacity with Power BI Premium per-user — they're distinct billing constructs
