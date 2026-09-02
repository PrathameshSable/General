# Fabric Technology Choice Decision Frameworks

Decision tables for selecting the right Microsoft Fabric item in each category. Use them to narrow to two or three
candidates, then validate against the engagement's constraints (skills, latency, compliance, budget, decommission date).

## Decision Approach

1. **Start with requirements** — latency, volume, query language, consumers, team skills
2. **Use the comparison tables** — narrow to 2–3 candidates
3. **Follow the quick-decision trees** — one per category
4. **Validate with constraints** — funding, compliance, existing estate, migration deadline
5. **Record an ADR** — one per non-obvious choice

---

## 1. Analytical Storage

| Item | Best For | Query Surface | Transactions | Complexity | Notes |
|---|---|---|---|---|---|
| **Lakehouse** | Bronze/Silver, files + tables, Spark workloads, semi-structured | Spark, SQL analytics endpoint (read-only T-SQL), Direct Lake | Single-table ACID (Delta) | Low–Medium | Default landing and conformance store |
| **Warehouse** | Gold star-schema marts, T-SQL stored procedures, Synapse dedicated-pool migrations | Full T-SQL (DDL/DML), Direct Lake | Multi-table ACID | Medium | Best when the team is T-SQL-native |
| **Eventhouse / KQL Database** | Telemetry, logs, IoT, time-series, high-cardinality events | KQL, T-SQL subset, OneLake availability | Append | Medium | Sub-second ingestion-to-query |
| **SQL database in Fabric** | Operational / transactional apps, write-back targets, small reference data | Full T-SQL OLTP | Full OLTP | Low | Auto-mirrored to OneLake for analytics |
| **Mirrored database** | Near-real-time replica of external OLTP (Azure SQL, SQL MI, SQL Server 2016+, Cosmos DB, Snowflake, PostgreSQL, Oracle, Open Mirroring) | SQL analytics endpoint, Direct Lake | Read-only replica | Very Low | No pipelines; mirroring compute is free within limits — verify current terms |

### Quick decision

- Need T-SQL writes / stored procedures / multi-table transactions → **Warehouse**
- Spark transforms, files, semi-structured, Bronze/Silver → **Lakehouse**
- Streams, logs, time-series, KQL heritage → **Eventhouse**
- Source is a supported OLTP database and latency in minutes is fine → **Mirrored database** (skip pipelines)
- App needs to write data that reports also read → **SQL database in Fabric**
- Undecided on Gold → start with **Gold Lakehouse**; move to Warehouse only if T-SQL DML is required

---

## 2. Ingestion

| Option | Best For | Latency | Transform at Ingest | Cost Profile | Notes |
|---|---|---|---|---|---|
| **Data Pipeline – Copy activity** | Bulk and incremental batch from 100+ connectors; orchestration | Minutes–hours | None (copy only) | CU per run | Backbone for metadata-driven frameworks |
| **Copy job** | Simple full/incremental copies without pipeline authoring | Minutes–hours | None | CU per run | Good for many-table SQL sources; supports CDC on some sources |
| **Dataflow Gen2** | Low-code Power Query shaping into Lakehouse/Warehouse | Minutes–hours | Yes (Power Query) | Higher CU per GB | Keep to small/medium volumes |
| **Mirroring** | Continuous replication from supported databases | Near-real-time | None | Included compute (limits apply) | Preferred when the source is supported |
| **OneLake Shortcut** | Reference data in ADLS Gen2, S3, GCS, Dataverse, Iceberg, another workspace | Zero-copy | None | Storage stays at source; egress may apply | Not a copy; respects source permissions |
| **Eventstream** | Event Hubs, IoT Hub, Kafka, CDC streams, custom apps | Seconds | Light (filter, aggregate) | Continuous CU | Route to Eventhouse or Lakehouse |
| **Notebook (Spark)** | APIs, complex file formats, custom auth, high-volume parallel loads | Minutes | Full | CU per session | Use when connectors fall short |
| **Dataverse Link to Fabric** | Dynamics 365 / Power Platform data | Near-real-time | None | Included | Standard for D365 estates |

### Quick decision

- Supported OLTP DB → **Mirroring**; else supported connector + batch → **Copy activity / Copy job**
- D365 → **Dataverse Link**; SaaS APIs → connector via **Copy activity**, else **Notebook**
- Data already in a lake (ADLS/S3/GCS) → **Shortcut**, never copy
- Events / streams → **Eventstream**
- Business-user shaping of small data → **Dataflow Gen2**
- On-prem sources → any of the above through an **on-premises data gateway** (cluster of 2+ nodes for Prod)

---

## 3. Transformation

| Option | Best For | Skills | Volume | Lineage | Incremental |
|---|---|---|---|---|---|
| **Notebook – PySpark / Spark SQL** | Complex logic, R/SSIS/Databricks conversions, ML features, large volumes | Python/Scala/SQL | Very high | Via OneLake lineage | Manual (MERGE / watermarks) |
| **Warehouse T-SQL (stored procedures)** | Set-based star-schema loads, Synapse migrations | T-SQL | High | Via lineage view | Manual (MERGE) |
| **Materialized Lake Views** | Declarative Silver → Gold with dependency graph | Spark SQL | High | Built-in | Built-in (Spark SQL MLVs) |
| **Dataflow Gen2** | Low-code shaping, citizen developers | Power Query | Low–Medium | Built-in | Incremental refresh supported |
| **Spark Job Definition** | Scheduled batch Spark applications as code | Python/Scala | Very high | Via lineage | Manual |

### Quick decision

- Team is T-SQL-native and Gold is a Warehouse → **stored procedures**
- Complex / procedural / large → **Notebooks** (enable Native Execution Engine)
- Standard Silver→Gold aggregations wanting lineage and scheduled refresh → **Materialized Lake Views**
- Analyst-owned, small → **Dataflow Gen2**

---

## 4. Serving & Semantic Layer

| Option | Best For | Refresh | Latency to Data | Limits |
|---|---|---|---|---|
| **Direct Lake semantic model** | Default for OneLake-backed Gold | None (framing on Delta commit) | Minutes | Per-SKU guardrails (rows/table, model size); falls back to DirectQuery |
| **Import** | Small models, legacy PBIX, sources outside OneLake | Scheduled (CU cost) | Refresh cadence | Model memory per SKU |
| **DirectQuery** | Write-back scenarios, non-OneLake sources, real-time on SQL DB | None | Seconds | Query performance depends on source |
| **Composite** | Direct Lake core + Import/DirectQuery satellites | Mixed | Mixed | Complexity |
| **SQL analytics endpoint** | External BI tools, SSMS, ad-hoc T-SQL | n/a | Minutes (sync lag) | Read-only |
| **GraphQL API / User Data Functions** | Apps consuming Gold; write-back logic | n/a | Seconds | Governance of app access |
| **Real-Time Dashboard** | Operational KQL views | n/a | Seconds | KQL only |

### Quick decision

- Gold on OneLake → **Direct Lake**; if the model exceeds guardrails → aggregation tables first, then Import for the aggregate layer
- Write-back required → **Translytical (User Data Functions + SQL database)** or DirectQuery to SQL database
- Third-party BI (Tableau in transition) → **SQL analytics endpoint**
- Streaming operational view → **Real-Time Dashboard**

---

## 5. Streaming & Real-Time

| Option | Best For | Retention | Consumers |
|---|---|---|---|
| **Eventstream → Eventhouse** | Telemetry, logs, IoT, clickstream; KQL analytics | Hot cache + OneLake | Real-Time Dashboards, Power BI (KQL), Activator |
| **Eventstream → Lakehouse** | Streams that only need batch analytics later | Delta | Spark, SQL endpoint, Direct Lake |
| **Activator** | Alerts and actions on thresholds, patterns, Power BI visuals | n/a | Teams, email, Power Automate, Fabric items |
| **Real-Time Hub** | Discovery of streams across the tenant | n/a | All of the above |

### Quick decision

- Need seconds latency and ad-hoc exploration → **Eventhouse**
- Only need the stream landed for daily reporting → **Eventstream → Lakehouse**
- "Notify me when…" → **Activator**

---

## 6. AI & Copilot

| Option | Best For | Prerequisites |
|---|---|---|
| **Copilot in Power BI** | NL Q&A and report generation on semantic models | F64+ (or Fabric Copilot capacity), Certified model with descriptions/synonyms, tenant setting on |
| **Copilot in Fabric (Data Factory, Data Engineering, RTI)** | Authoring assistance for pipelines, notebooks, KQL | Same capacity/tenant prerequisites |
| **Data Agents** | Conversational agent over Lakehouse / Warehouse / KQL / semantic models | Curated schemas, instructions, example queries; F64+ |
| **Azure OpenAI / AI functions in notebooks** | Enrichment, classification, summarisation in pipelines | Azure OpenAI resource or Fabric-managed AI endpoint; PHI/PII review |
| **Fabric IQ / Ontology** | Shared business semantics across agents and analytics | Emerging — scope carefully, mark as POV |

### Quick decision

- Business users asking questions of KPIs → **Copilot in Power BI** on a Certified model
- Multi-source conversational analytics → **Data Agents**
- Enrichment during ingestion → **AI functions / Azure OpenAI in Notebooks**
- Never promise "answers any question"; scope to Certified measures (see `templates/fabric-domain-reference.md` §11)

---

## 7. Governance

| Option | Best For | Scope |
|---|---|---|
| **Purview Unified Catalog** | Catalog, lineage, glossary, data quality, classification across Fabric and non-Fabric | Tenant |
| **Sensitivity labels + DLP** | PHI/PII/confidential labelling, export controls | Tenant policy, item-level labels |
| **Fabric admin portal / tenant settings** | Feature enablement, export controls, Copilot, external sharing | Tenant / capacity / domain delegation |
| **Domains & sub-domains** | Business ownership, delegated settings, discoverability | Tenant |
| **Endorsement (Promoted / Certified)** | Trusted-content signal, Copilot gating | Item |
| **OneLake security** | Table / folder / row / column access for engineers and shortcuts | Item |
| **RLS / OLS** | Consumer-level filtering in semantic models and Warehouse | Item |

### Quick decision

- Regulated data → Purview scan + labels + DLP before Prod go-live, not after
- Many business units → Domains with delegated tenant settings
- Copilot in scope → Certified endorsement is mandatory

---

## 8. CI/CD & DevOps

| Option | Best For | Notes |
|---|---|---|
| **Git integration (Azure DevOps / GitHub)** | Source control of workspace items | Branch per workspace; not all item types supported — check list |
| **Deployment pipelines** | Dev → Test → Prod promotion with rules | Native; supports deployment rules for connections/parameters |
| **Variable Library** | Environment-specific values (lakehouse IDs, connection names) | Replaces hard-coded IDs in pipelines/notebooks |
| **Fabric REST API / `fabric-cicd` / Terraform provider** | Scripted deployment, capacity/workspace provisioning | Use for enterprise pipelines and IaC |
| **Environment item (Spark)** | Pinned libraries and Spark settings | Promote with the workspace |

### Quick decision

- Small team, few workspaces → Git + Deployment pipelines + Variable Library
- Enterprise platform team → add REST API / `fabric-cicd` in Azure DevOps or GitHub Actions, Terraform for capacities/workspaces

---

## 9. Networking & Connectivity

| Option | Best For | Notes |
|---|---|---|
| **Public endpoints with tenant controls** | Default for most commercial tenants | Conditional Access, export controls |
| **Tenant-level Private Link** | Regulated tenants blocking public access | Impacts some features (check current limitations) |
| **Managed VNet + managed private endpoints** | Spark reaching private Azure sources | Per workspace |
| **On-premises data gateway (cluster)** | Pipelines / Dataflows / semantic models reaching on-prem | 2+ nodes in Prod; size VM for throughput |
| **VNet data gateway** | Private Azure sources for Dataflows / semantic models without VMs | Managed |
| **Trusted workspace access** | Shortcuts to firewalled ADLS Gen2 | Workspace identity |

### Quick decision

- Healthcare / finance with "no public access" policy → Private Link + Managed VNet + gateways; budget extra setup time in the SOW
- On-prem SQL Server → gateway cluster; document node sizing as an assumption

---

## Related Microsoft Learn Decision Guides

- Fabric decision guide: Lakehouse vs Warehouse vs Eventhouse vs SQL database
- Fabric decision guide: Copy activity vs Dataflow Gen2 vs Spark vs Copy job
- Direct Lake overview and guardrails
- Mirroring supported sources and limitations
- Fabric CI/CD (Git integration, deployment pipelines) supported item types

Names and limits change; confirm each against Microsoft Learn before quoting in a deliverable.
