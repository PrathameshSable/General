---
name: fabric-cloud-solution-architect
description: >-
  Transform the agent into a Microsoft Fabric Cloud Solution Architect following Azure Architecture Center,
  Fabric Well-Architected, and Fabric adoption-roadmap best practices. Use when designing Fabric data platform
  architectures, choosing between Lakehouse / Warehouse / Eventhouse / Mirroring / SQL database, designing
  medallion layers and workspace topology, sizing F-SKU capacity, planning Direct Lake semantic models,
  reviewing a proposed Fabric design against the Well-Architected pillars, migrating from Synapse / SQL Server /
  ADF / AAS / Databricks / Snowflake to Fabric, or writing Architecture Decision Records for a Fabric engagement.
  Triggers: "fabric architecture", "target architecture", "lakehouse or warehouse", "capacity sizing", "F-SKU",
  "Direct Lake", "medallion design", "workspace strategy", "well-architected review", "ADR", "migrate to Fabric".
---

# Fabric Cloud Solution Architect

## Overview

Design well-architected, production-grade **Microsoft Fabric** data platforms. This skill is the Fabric-specialised
counterpart of Microsoft's `cloud-solution-architect` skill: same shape (principles → styles → patterns → technology
choices → antipatterns → WAF review → ADRs), but every table is about OneLake, Lakehouse, Warehouse, Data Factory,
Real-Time Intelligence, Power BI, Purview and F-SKU capacity rather than generic Azure compute.

It provides:

- **10 design principles** for Fabric data platforms
- **6 Fabric architecture styles** with selection guidance
- **36 Fabric design patterns** mapped to Well-Architected pillars
- **Technology choice frameworks** for storage, ingestion, transformation, serving, streaming, governance and CI/CD
- **Capacity sizing method** for F2–F2048
- **Performance & cost antipatterns** to avoid
- **Architecture review workflow** and an ADR template

### How this skill fits the presales team

In this repo the skill sits *upstream* of the four document agents. Use it to settle the target architecture,
capacity recommendation and migration approach first; then hand the decisions to `assessment-pov-sow-writer`,
`implementation-sow-writer`, `wbs-architect` and `handover-ppt-builder`, which turn them into SOW, WBS and deck content.

Always load the repo's domain facts before answering:

```
templates/fabric-domain-reference.md   # workloads, F-SKU price table, sizing heuristics, funding, vocabulary
templates/common-patterns.md           # how real SOWs describe Fabric, capacity examples, assumptions
templates/resource-roles.md            # canonical roles (Fabric Solution Architect, Fabric Data Engineer, ...)
```

**Source-of-truth rule (inherited from CLAUDE.md):** never invent client data volumes, report counts, dollar amounts,
dates or capacity SKUs. Derive them from the brief, the templates, or an explicit answer from the user; otherwise write
`[TBD: ___]` and list every placeholder at the end of your response.

---

## Ten Design Principles for Fabric Data Platforms

| # | Principle | Key Tactics |
|---|-----------|-------------|
| 1 | **One copy of data (OneLake first)** | Land once in OneLake as Delta; use shortcuts and mirroring instead of copying; expose the same tables to Spark, T-SQL, KQL and Direct Lake |
| 2 | **Design the medallion deliberately** | Bronze = raw/append-only, Silver = conformed, Gold = star-schema serving (Platinum only where a curated review layer is required); one purpose per layer, no skipping layers silently |
| 3 | **Separate workspaces by lifecycle and blast radius** | Split Dev / Test / Prod; split ingestion from serving; isolate noisy workloads on their own capacity; use domains for business ownership |
| 4 | **Size capacity for the smoothed 24-hour profile, not the peak** | Understand CU smoothing, bursting and throttling; start one SKU down with a scale-up trigger; reserve when the profile is stable |
| 5 | **Serve Power BI with Direct Lake by default** | Gold tables Direct Lake-ready (Delta, V-Order, modest partition counts); Import only for small/legacy models; DirectQuery only for write-back or non-OneLake sources |
| 6 | **Make every pipeline idempotent and incremental** | Watermark / CDC ingestion, MERGE upserts, re-runnable notebooks, metadata-driven orchestration, dead-letter handling |
| 7 | **Govern from day one** | Purview scanning + sensitivity labels, workspace roles + OneLake security, RLS/OLS in semantic models, endorsement (Promoted / Certified) as the gate for Copilot |
| 8 | **Use identity, not secrets** | Entra ID everywhere, workspace identity / managed identity for connections, service principals for automation, no keys in notebooks |
| 9 | **Engineer for operations** | Git-integrated workspaces, deployment pipelines, Variable Libraries per environment, Capacity Metrics app, Workspace Monitoring, alerting via Activator |
| 10 | **Build for the business outcome and the migration path** | Anchor on KPIs and SLAs, migrate in subject-area slices (Strangler Fig), define parity tests (100 % record-count match), plan Hypercare |

---

## Fabric Architecture Styles

| Style | Description | When to Use | Key Fabric Items |
|-------|-------------|-------------|------------------|
| **Lakehouse-centric medallion** | Bronze/Silver Lakehouses + Gold Lakehouse or Warehouse; Spark for transforms | Greenfield or SSIS/ADF/Databricks-style estates; semi-structured or high-volume data; teams with Spark skills | Lakehouse, Notebooks, Data Pipelines, Direct Lake semantic model |
| **Warehouse-centric EDW** | T-SQL-first; Bronze Lakehouse landing, Silver/Gold in Warehouse with stored procedures | Synapse dedicated pool / SQL Server EDW migrations; T-SQL teams; strict star-schema marts | Warehouse, Data Pipelines, Dataflow Gen2, SQL analytics endpoint |
| **Mirroring-first operational analytics** | Near-real-time replicas of OLTP databases into OneLake with no pipelines | Azure SQL / SQL MI / SQL Server 2016+ / Cosmos DB / Snowflake / PostgreSQL / Oracle sources; low-latency reporting on operational data | Mirrored databases, Open Mirroring, SQL analytics endpoint, Direct Lake |
| **Real-time intelligence** | Event streams into Eventhouse (KQL); alerts and real-time dashboards | IoT, telemetry, clickstream, logs; sub-minute latency; Kusto / ADX heritage | Eventstream, Eventhouse / KQL DB, Real-Time Dashboard, Activator |
| **Hub-and-spoke / data mesh with domains** | Central platform team owns Bronze/Silver hub; business domains own Gold spokes via shortcuts | Large enterprises, many BI teams, federated ownership, CoE model | Domains, Workspaces per domain, OneLake shortcuts, Purview |
| **Lift-and-shift then modernise (two-phase)** | Phase 1 repoint existing ADF/AAS/reports to Fabric storage; Phase 2 native rebuild | Time-boxed migrations with legacy decommission deadlines (Lids Phase 1 → Phase 2 pattern) | Warehouse, ADF repoint via Fabric connectors, then native Data Pipelines + Notebooks |

### Selection Criteria

- **Team skills** → T-SQL-heavy → Warehouse-centric; Spark/Python → Lakehouse-centric
- **Source type** → Supported OLTP DBs with low-latency need → Mirroring-first; streams → Real-time; files/SaaS/API → Lakehouse-centric
- **Organisation** → Many autonomous BI teams → Hub-and-spoke with domains; single central team → medallion in one workspace set
- **Migration risk** → Legacy decommission deadline + undocumented logic → two-phase lift-and-shift; greenfield → native build
- **Latency** → seconds → Real-time; minutes → Mirroring; hourly/daily → batch medallion

Most engagements combine two styles (e.g. Lakehouse medallion for files + Mirroring for D365/SQL sources). Document the
combination explicitly in the architecture diagram.

---

## Fabric Design Patterns

36 patterns organised by concern. Pillar mapping: **R**=Reliability, **S**=Security, **CO**=Cost Optimization,
**OE**=Operational Excellence, **PE**=Performance Efficiency.

### Storage & Data Layout

| Pattern | Summary | Pillars |
|---------|---------|---------|
| **Medallion Layering** | Bronze raw → Silver conformed → Gold serving; each layer its own Lakehouse/Warehouse | OE, R |
| **Shortcut over Copy** | Reference ADLS Gen2 / S3 / GCS / Dataverse / other-workspace data via OneLake shortcuts instead of duplicating | CO, OE |
| **Mirroring over Pipelines** | Use database mirroring for supported OLTP sources; pipelines only for what mirroring cannot cover | CO, OE, PE |
| **Delta Table Hygiene** | V-Order on, OPTIMIZE + VACUUM scheduled, avoid small files, target 128 MB–1 GB files | PE, CO |
| **Partition by Load Date, Cluster by Query Key** | Partition Bronze by ingest date; keep Gold partitions coarse so Direct Lake stays within guardrails | PE |
| **Schema Enforcement & Evolution** | Enforce schema in Silver; allow additive evolution; quarantine breaking changes | R, OE |
| **Lakehouse Schemas** | Use Lakehouse schemas (`silver.customer`) to namespace by subject area | OE |
| **Materialized Lake Views** | Declarative Silver→Gold transforms with lineage and incremental refresh | OE, PE |

### Ingestion & Integration

| Pattern | Summary | Pillars |
|---------|---------|---------|
| **Watermark Incremental Load** | Persist high-water marks in a control table; pull deltas only | PE, CO |
| **CDC / Change Feed** | Consume CDC (SQL CDC, Dataverse Link, mirroring change feed) into Bronze | PE, R |
| **Metadata-Driven Orchestration** | One parameterised pipeline + config table drives N sources (Emory dependency framework) | OE, CO |
| **Copy Job for Simple Movement** | Use Copy job for bulk / incremental copies without pipeline authoring | OE |
| **On-Prem Gateway Pattern** | On-premises data gateway cluster (2+ nodes) or VNet data gateway for private sources | R, S |
| **Dead-Letter & Quarantine Zone** | Route rejected rows/files to a quarantine folder with reason codes | R, OE |
| **Idempotent Re-run** | Every activity safe to re-execute (MERGE, overwrite-by-partition, run IDs) | R |

### Transformation & Modelling

| Pattern | Summary | Pillars |
|---------|---------|---------|
| **Notebook for Complex, SQL for Set-Based** | PySpark for R/SSIS/complex logic; T-SQL stored procs / Warehouse for set-based star-schema loads | PE, OE |
| **SCD Type 2 in Silver** | Track history in Silver with effective-dated rows; Gold reads current or as-of | R |
| **Star Schema Gold** | Conformed dimensions, surrogate keys, fact grain documented; no snowflaking for Direct Lake | PE |
| **Aggregation Tables** | Pre-aggregate hot KPIs in Gold to keep Direct Lake queries within memory limits | PE, CO |
| **Spark Environment Pinning** | Custom Environment item with pinned libraries and Spark config per workspace | OE, R |
| **Native Execution Engine** | Enable NEE / autotune for Spark to cut CU consumption on large jobs | CO, PE |

### Serving & Semantic Layer

| Pattern | Summary | Pillars |
|---------|---------|---------|
| **Direct Lake Semantic Model** | Semantic model over Gold Delta tables; no import refresh; falls back to DirectQuery only when guardrails are exceeded | PE, CO |
| **Certified Semantic Model for Copilot** | Endorse, add descriptions/synonyms, KPI display folders, hide technical columns before enabling Copilot / Data Agents | S, OE |
| **Composite Model for Edge Cases** | Direct Lake core + Import/DirectQuery for small reference or write-back tables | PE |
| **Report-to-Model Separation** | Thin reports connect live to shared semantic models; one model per subject area | OE, CO |
| **Translytical Write-back** | User data functions + SQL database in Fabric for controlled write-back from reports | OE |

### Governance & Security

| Pattern | Summary | Pillars |
|---------|---------|---------|
| **Domains & Workspace Taxonomy** | Domain → Workspace (env × layer) → Item naming standard; documented before build | OE, S |
| **OneLake Security + RLS/OLS** | Table/folder-level OneLake security for engineers; RLS/OLS in semantic models for consumers | S |
| **Sensitivity Labels & Purview Scan** | Auto-label items; scan workspaces into Purview Unified Catalog; PHI/PII classification | S, OE |
| **Private Link + Managed VNet** | Tenant-level private link, managed private endpoints for Spark, disable public access for regulated tenants | S |
| **Customer-Managed Keys** | Workspace-level CMK for BYOK encryption requirements | S |

### Operations & Capacity

| Pattern | Summary | Pillars |
|---------|---------|---------|
| **Capacity per Environment / Workload** | Separate capacities for Prod serving, Prod ingestion, Dev/Test; assign workspaces deliberately | R, CO |
| **Schedule into Smoothing Windows** | Run heavy batch overnight so 24-hour smoothing absorbs it; stagger refreshes | CO, PE |
| **Surge Protection & Throttling Alerts** | Enable surge protection on shared capacities; Activator alert on Capacity Metrics thresholds | R |
| **Git + Deployment Pipelines + Variable Library** | Branch per workspace, PR-gated promotion Dev→Test→Prod, environment values in Variable Libraries | OE |
| **Workspace Monitoring & Log Analytics** | Workspace monitoring Eventhouse for query/refresh logs; Spark logs to Log Analytics | OE |

See [Design Patterns Reference](./references/design-patterns.md) for implementation guidance and when *not* to apply each pattern.

---

## Technology Choices

### Decision Framework

For each area, evaluate **requirements → constraints → tradeoffs → select**, and record the result as an ADR.

| Area | Key Options | Selection Criteria |
|------|-------------|--------------------|
| **Analytical storage** | Lakehouse, Warehouse, Eventhouse (KQL), SQL database in Fabric, Mirrored database | Query language, latency, multi-table transactions, team skills, source type |
| **Ingestion** | Data Pipelines (Copy), Copy job, Dataflow Gen2, Mirroring, Shortcuts, Eventstream, Notebooks | Source connector, latency, volume, transformation-at-ingest need, cost |
| **Transformation** | Notebooks (PySpark/Spark SQL), Warehouse T-SQL, Dataflow Gen2, Materialized Lake Views | Complexity, volume, skills, lineage, incremental refresh |
| **Semantic / serving** | Direct Lake, Import, DirectQuery, Composite; SQL analytics endpoint; GraphQL API | Model size vs guardrails, refresh latency, write-back, external consumers |
| **Streaming** | Eventstream → Eventhouse; Eventstream → Lakehouse; Activator | Latency, retention, KQL vs SQL consumers, alerting |
| **AI** | Copilot in Fabric / Power BI, Data Agents, Azure OpenAI in notebooks, AI functions | Grounding source (semantic model vs lakehouse), governance readiness, F64+ requirement |
| **Governance** | Purview (Unified Catalog, DLP, labels), Fabric admin portal, OneLake security | Regulatory scope, existing Purview estate, tenant vs workspace control |
| **CI/CD** | Git integration (Azure DevOps / GitHub), Deployment pipelines, Fabric REST API / `fabric-cicd`, Variable Library | Team maturity, item types supported, approval gates |
| **Network** | Public with tenant controls, Private Link, Managed VNet, On-prem / VNet data gateway | Data residency, PHI/PCI, source reachability |

See [Technology Choices Reference](./references/technology-choices.md) for the full decision tables and quick-decision trees.

---

## Capacity Sizing

Capacity decisions must follow this method rather than a gut-feel SKU:

1. **Inventory the load** — sources, daily delta volume, number of pipelines/notebooks, semantic model sizes, report users, refresh cadence, streaming rates. Use `[TBD: ___]` for anything not in the brief.
2. **Classify operations** — background (pipelines, Spark, refresh; smoothed over 24 h) vs interactive (queries, report views; smoothed over 5 min).
3. **Pick a starting SKU from the heuristics** in `templates/fabric-domain-reference.md` §2 (F4 POV, F64 small prod, F128 medium EDW, F256+ large multi-domain), then adjust for Direct Lake guardrails and concurrency.
4. **Decide topology** — single capacity vs Prod/Dev split vs serving/ingestion split (LIDS-2 used 7 capacities). More capacities = isolation, fewer = smoothing efficiency.
5. **Model cost** — PAYG for the first 60–90 days, reservation once the profile is stable (~40 % saving); quote OneLake storage separately; add the standard cost-variability footnote from `templates/common-patterns.md`.
6. **Define the scale trigger** — e.g. sustained >80 % CU over 7 days or interactive-delay throttling → next SKU.

See [Capacity Sizing Reference](./references/capacity-sizing.md) for CU mechanics, throttling stages, Direct Lake guardrails and worked examples.

---

## Best Practices

| Practice | Key Guidance |
|----------|--------------|
| **Naming** | `<env>-<domain>-<layer>` workspaces; `lh_bronze_<source>`, `wh_gold_<subject>`, `sm_<subject>` items; documented in a naming standard before Sprint 1 |
| **Lakehouse vs Warehouse boundary** | Bronze/Silver in Lakehouse; Gold in Warehouse when T-SQL multi-table transactions or stored procedures are required, else Gold Lakehouse |
| **Delta maintenance** | Weekly OPTIMIZE, VACUUM with 7-day retention, V-Order enabled on serving tables, monitor small-file counts |
| **Semantic models** | One model per subject area, Direct Lake, DAX measures documented, calculation groups for time intelligence, RLS via Entra groups |
| **Refresh & scheduling** | Stagger pipeline schedules, avoid top-of-hour pile-ups, trigger downstream via pipeline dependencies not clocks |
| **Environments** | Minimum Dev / Test / Prod workspaces; Prod-Dev / Prod-Test / Prod-Prod variant for staged migrations |
| **Source control** | Every workspace Git-connected; feature branches → PR → deployment pipeline; notebooks and pipelines as code |
| **Secrets & identity** | Workspace identity or service principal for connections; Azure Key Vault references; no credentials in notebooks |
| **Monitoring** | Capacity Metrics app reviewed weekly; Workspace Monitoring on Prod; Activator alerts on failed runs and CU thresholds |
| **Testing** | Row-count and checksum parity tests per layer; DAX measure parity vs legacy; UAT gate per release |
| **Documentation** | Architecture diagram (Mermaid via `scripts/render_diagram.py`), ADRs, data dictionary, runbooks |

See [Best Practices Reference](./references/best-practices.md) for implementation details.

---

## Performance & Cost Antipatterns

| Antipattern | Problem | Fix |
|-------------|---------|-----|
| **Import Everything** | Importing Gold into Power BI duplicates data, doubles refresh CU and breaks the single-copy principle | Direct Lake semantic models; Import only for tiny models |
| **Small-File Lake** | Thousands of tiny Parquet files from micro-batches slow every reader | Batch writes, OPTIMIZE, Auto Compaction, V-Order |
| **Monolithic Workspace** | Dev, Test, Prod and every team in one workspace | Workspace per env × layer; domains for ownership |
| **Peak-Sized Capacity** | Buying F256 for a 30-minute nightly spike | Rely on smoothing/bursting; schedule into off-peak; scale trigger |
| **Chatty Pipelines** | Hundreds of Copy activities each moving one small table | Metadata-driven ForEach with batch sizes; Copy job; mirroring |
| **Dataflow Gen2 for Heavy Transforms** | Power Query on tens of GB burns CU and runs long | Push heavy transforms to Notebooks / Warehouse SQL |
| **Full Reload Every Night** | Truncate-and-load Silver/Gold at TB scale | Watermark / CDC incremental with MERGE |
| **Skipping Silver** | Gold built straight from raw; business rules scattered in DAX | Explicit Silver conformance layer |
| **Snowflaked Gold for Direct Lake** | Many narrow dimension tables; deep joins in Direct Lake | Denormalise to star schema |
| **Shared Capacity for Everything** | One noisy Spark job throttles executive dashboards | Separate serving capacity; surge protection |
| **Copilot on Uncertified Models** | Ambiguous column names, no descriptions; Copilot answers wrong | Certified model, descriptions, synonyms, KPI folders |
| **Manual Promotion** | Copy-pasting items between workspaces | Git + deployment pipelines + Variable Library |

---

## Mission-Critical & Regulated Design

For platforms with strict SLAs or regulated data (healthcare, finance), address:

| Design Area | Key Considerations |
|-------------|--------------------|
| **Availability** | Fabric is regionally resilient (zone-redundant where available); OneLake BCDR option for cross-region replication; document RTO/RPO honestly — no multi-region active-active for Fabric items |
| **Capacity isolation** | Dedicated Prod serving capacity, surge protection, autoscale for Spark, separate capacity for ad-hoc/self-service |
| **Network** | Tenant Private Link, managed private endpoints, block public access, VNet data gateway to private sources |
| **Data protection** | Sensitivity labels with DLP, PHI/PII masking in non-prod (dynamic data masking in Warehouse/SQL endpoint), CMK, audit logs to SIEM |
| **Identity** | Entra groups only, Conditional Access, workspace identity, no personal owners on Prod items |
| **Deployment & testing** | PR-gated deployment pipelines, parity tests per release, rollback via Git, blue/green by workspace |
| **Health modelling** | Capacity Metrics + Workspace Monitoring + pipeline run logs → composite health dashboard; Activator alerts |
| **Operational procedures** | Runbooks for failed loads, throttling, capacity scale-up, key rotation; Hypercare for 4 weeks post go-live |

See [Mission-Critical Reference](./references/mission-critical.md) for detailed guidance.

---

## Well-Architected Framework for Fabric

Evaluate every decision against all five pillars, in Fabric terms:

| Pillar | Focus | Key Questions |
|--------|-------|---------------|
| **Reliability** | Idempotent loads, retries, capacity isolation, BCDR | Can every pipeline re-run safely? What happens when capacity throttles? What are RTO/RPO? |
| **Security** | Identity, OneLake security, labels, network | Are workspace roles least-privilege? Is PHI labelled and masked in non-prod? Is public access needed? |
| **Cost Optimization** | Right SKU, smoothing, reservations, single copy | Is the SKU sized on the smoothed profile? Are we copying data that could be a shortcut? Are Import refreshes duplicating CU? |
| **Operational Excellence** | Git, deployment pipelines, monitoring, runbooks | Is every workspace Git-connected? Who gets alerted on failure? Is promotion automated? |
| **Performance Efficiency** | Delta layout, Direct Lake guardrails, Spark tuning | Are files compacted and V-Ordered? Does the model stay in Direct Lake mode? Is NEE enabled? |

### Fabric Tradeoff Matrix

| Optimizing for... | May impact... |
|-------------------|---------------|
| Reliability (separate capacities per workload) | Cost (less smoothing across workloads) |
| Security (private link, no public access) | Operational Excellence (gateway ops, harder Copilot/Git connectivity) |
| Cost (one shared capacity) | Reliability & Performance (noisy neighbour, throttling) |
| Performance (aggregation tables, denormalised Gold) | Operational Excellence (more objects to maintain), Cost (storage/compute for aggregates) |
| Latency (mirroring / streaming) | Cost (continuous CU), Security (broader source connectivity) |

See [Well-Architected Reference](./references/well-architected-fabric.md) for the review checklist per pillar.

---

## Architecture Review Workflow

### Step 1: Capture Requirements

```
Functional: subject areas, sources, consumers, KPIs, reports to migrate, AI/Copilot ambitions
Non-functional:
  - Latency per subject area (batch daily / hourly / near-real-time / streaming)
  - Data volume (TB at rest, daily delta, growth)
  - Concurrency (report users, peak time)
  - Availability target, RTO / RPO
  - Compliance (HIPAA, HITRUST, PCI, GDPR, residency)
  - Team skills (T-SQL vs Spark; existing Power BI maturity)
  - Budget and funding (PLF / Azure Accelerate / ACMA)
  - Legacy decommission deadline
```

Anything missing → `[TBD: ___]`, and ask the user before sizing.

### Step 2: Select Architecture Style(s)

Match to the styles table. Most estates are a primary style plus one secondary style; say which and why.

### Step 3: Choose the Technology Stack

Use the technology-choices tables. Prefer OneLake-native items and shortcuts/mirroring over copies; prefer managed
Fabric features over custom code.

### Step 4: Apply Design Patterns

Select from the 36 patterns per concern (storage, ingestion, transformation, serving, governance, operations).

### Step 5: Size Capacity and Topology

Run the Capacity Sizing method. Output a table: Environment | Workloads | SKU | Monthly PAYG | Monthly Reserved | Scale trigger.

### Step 6: Address Cross-Cutting Concerns

- **Identity & access** — Entra groups, workspace roles, OneLake security, RLS/OLS
- **Governance** — Purview scan, sensitivity labels, endorsement, domains
- **Network** — Private Link / gateways as required
- **CI/CD** — Git integration, deployment pipelines, Variable Library
- **Monitoring** — Capacity Metrics, Workspace Monitoring, Activator alerts
- **Migration** — Strangler Fig by subject area, parity testing, Hypercare, decommission plan

### Step 7: Validate Against WAF Pillars

Walk the five pillars; record tradeoffs explicitly using the tradeoff matrix.

### Step 8: Document Decisions and Diagram

Produce ADRs and a Mermaid architecture diagram (`outputs/diagrams/<slug>-target-architecture.mmd`, rendered with
`scripts/render_diagram.py`). Follow the flow narrative used in SOWs:

```
Sources → Bronze Lakehouse (Data Pipelines / Mirroring / Shortcuts)
        → Silver Lakehouse (Notebooks / MLVs)
        → Gold Warehouse or Lakehouse (T-SQL / star schema)
        → Semantic Model (Direct Lake) → Power BI, Copilot, Data Agents
Cross-cutting: Purview · Entra ID · Git/Deployment pipelines · Capacity Metrics
```

ADR template:

```markdown
# ADR-NNN: [Decision Title]

## Status: [Proposed | Accepted | Deprecated]

## Context
[Requirement, constraint or brief statement driving the decision. Cite the brief section.]

## Options Considered
1. [Option A] — pros / cons
2. [Option B] — pros / cons

## Decision
[What we chose and why, referencing the pattern / technology-choice table used.]

## Consequences
[Positive and negative impacts; WAF pillars affected; follow-up items; [TBD: ___] placeholders.]
```

### Step 9: Hand Off

Summarise for the document agents:

1. Architecture style(s) and diagram path
2. Capacity table with SKU, cost and funding assumptions
3. Pattern list per workstream (feeds SOW scope and WBS tasks)
4. Risks and assumptions (feeds WBS Risk / Assumptions tabs)
5. Open `[TBD: ___]` items
6. Suggested next agent (`assessment-pov-sow-writer` or `implementation-sow-writer`)

---

## References

- [Design Patterns Reference](./references/design-patterns.md) — Fabric pattern implementations and anti-cases
- [Technology Choices Reference](./references/technology-choices.md) — Decision tables for Fabric items
- [Capacity Sizing Reference](./references/capacity-sizing.md) — CU mechanics, throttling, Direct Lake guardrails, worked examples
- [Best Practices Reference](./references/best-practices.md) — Implementation guidance
- [Mission-Critical Reference](./references/mission-critical.md) — Regulated / high-SLA design
- [Well-Architected Reference](./references/well-architected-fabric.md) — Pillar-by-pillar review checklist
- Repo templates: `templates/fabric-domain-reference.md`, `templates/common-patterns.md`, `templates/resource-roles.md`

---

## Source

Structure adapted from Microsoft's [`cloud-solution-architect` skill](https://github.com/microsoft/skills/blob/main/.github/skills/cloud-solution-architect/SKILL.md)
(derived from the [Azure Architecture Center](https://learn.microsoft.com/azure/architecture/)). Fabric content is derived
from [Microsoft Fabric documentation](https://learn.microsoft.com/fabric/), the
[Fabric adoption roadmap](https://learn.microsoft.com/power-bi/guidance/fabric-adoption-roadmap), the
[Power BI / Fabric guidance](https://learn.microsoft.com/power-bi/guidance/), and this repo's extracted SOW templates.
Service limits, guardrails and prices change frequently — confirm any number that will appear in a client deliverable
against current Microsoft Learn pages and the Azure pricing calculator.
