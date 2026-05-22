# Implementation SOW – Template Structure

Reference docs:
- `09257774-Phase_1_Microsoft_Fabric_Migration_SOW_01132026.docx` (Lids Phase 1 – 13-week migration, $185K)
- `e964b982-Phase_2_Microsoft_Fabric_Migration_SOW_04042026.docx` (Lids Phase 2 – 28 weeks + 4 weeks Hypercare, $387K)
- `8a73a819-Emory_SOW__Data_Engineering_and_Power_BI_Modernization__Santor.docx` (Emory – 20 weeks dual workstream, $540K, Truviz-fronted)
- `a97a2378-ACME__Consulting_Services_SOW3__04_27_2026.docx` (ACME – ongoing T&M consulting extension, 3 months, $30K)

Implementation SOWs are 3-9 months, $30K–$540K+, with much deeper scope, formal release plans, hypercare, training, expense caps, and more granular responsibility matrices. ACME SOW3 is a T&M extension model (an outlier — full templates assume fixed-fee delivery).

---

## 1. Canonical Section Order

The two Lids SOWs (Phase 1, Phase 2) follow the most complete structure. Emory uses a workstream-first numbering (`1. Workstream 1: ...`, `2. Workstream 2: ...`) — a parallel-workstreams variant. ACME is heavily condensed (T&M).

| # | Section | Phase 1 | Phase 2 | Emory | ACME (T&M) |
|---|---|:-:|:-:|:-:|:-:|
| Cover | Title block + contact | yes | yes | yes | yes |
| 1 | Introduction | yes | yes | yes (MSA-anchored) | yes |
| 2 | Executive Summary | yes | yes | absorbed into WS Understanding | — |
| 2.1 | Business Drivers | yes | — | — | — |
| 2.2 | Current State Challenges | yes | — | — | — |
| 2.3 | Target State Benefits | yes | yes | — | — |
| 3 | Current State Inventory (Database Objects / AAS Models / EDW) | yes | yes | yes (32 reports inventory) | — |
| 4 | Target Architecture (Microsoft Fabric) | yes | yes | yes | implicit |
| 4.x | Architecture Components / Diagrams / Data Flow / Systems to be Decommissioned | yes | yes | yes | — |
| 5 | [Phase Name] – e.g., "Foundation & Core Analytics" / "Optimization & Expansion" / Workstream | yes | yes | yes | — |
| 5.x | Project Objectives / Scope (broken into 5-7 sub-scope blocks) | yes | yes | yes (Discovery, Source Validation, Architecture, Development, Dependency Framework, Governance, Testing) | — |
| 5.x.x | Modular Release Strategy (multi-release implementations) | — | yes (5 releases) | yes (5 releases) | — |
| 6 | Project Deliverables & Timelines (per release) | yes | yes | yes | — |
| 7 | Fabric Capacity Planning | yes | yes | — | — |
| 7.x | Data Volumes & Workloads / Recommended Capacity & Estimated Cost | yes | yes | — | — |
| 8 | Risk & Mitigation (table) | yes | yes | yes | — |
| 9 | Assumptions & Dependencies | yes | yes | yes (deep – 7+ sub-sections) | yes (combined) |
| 9.x | Project Assumptions / Required Access / Client Responsibilities / Collaboration | yes | yes | yes | yes |
| 10 | Project Team & Responsibilities | yes | yes | yes | yes (in pricing) |
| 10.x | Santor Team Structure / Responsibility Matrix | yes | yes | yes | — |
| 11 | Governance & Communication | yes | yes | — | — |
| 11.x | Project Governance / Communication Channels / Change Management | yes | yes | inline | — |
| 12 | Acceptance Criteria (+ Out of Scope) | yes | yes | inline per WS | — |
| 13 | Engagement Cost | yes | yes | yes | yes |
| 13.x | Implementation Cost / Training Cost / Hypercare Cost / Payment Schedule | yes | yes | yes | yes (rates only) |
| 14 | Expenses ($10K cap, per-diem clause) | yes | yes | yes | — |
| 15 | Change Order | yes | yes | yes | — |
| 16 | Payment Terms (Net 60) | yes | yes | Net 30 (Emory) / Net 15 (ACME) | yes (Net 15) |
| – | Acceptance (signatures) | yes | yes | yes | yes |
| Appendix A | Change Order template | yes | yes | yes | — |
| Appendix B | List of reports / Complexity scoring | — | — | yes | — |

---

## 2. Differences vs. Assessment/POV SOW

| Aspect | Assessment/POV | Implementation |
|---|---|---|
| Duration | 4–6 weeks | 13–28 weeks (per phase) + 4 weeks hypercare |
| Workstream count | 2 parallel (Assessment + POV) | 1–2; if 2, longer parallel build |
| Phase/Release structure | flat weekly milestones | multi-release (5 releases is common); each release scoped end-to-end |
| Inventory section | absent / lightweight | **mandatory** – counts of tables, views, stored procedures, AAS models, DAX measures (e.g., "227 tables, 226 views, 64 stored procedures, 3,993 DAX measures, 1,293 calculated columns") |
| Capacity Planning section | absent | **mandatory** – data volumes, workload patterns, recommended SKU stack (F64/F128 + storage costs) |
| Risk & Mitigation | absent | **mandatory** table (Functional Compatibility, Performance, Data Movement, Operational, Cost, BI Impact) |
| Training | absent | optional dedicated section (3-day curriculum, $3K/day) |
| Hypercare | absent | 4-week post-go-live support typical for Phase 2/final-cutover SOWs |
| Expenses clause | absent | "$10,000 cap" + per-diem boilerplate |
| Payment terms | Net 30 | Net 60 (Lids) – Net 30 (Emory) – Net 15 (ACME T&M) |
| Pricing structure | 1-line cost + funding | per-phase / per-release invoicing, training invoicing, hypercare invoicing |
| Team size | 3-4 roles, part-time PM | 7-10 roles, full-time delivery team with dedicated DevOps, Tester, Data Modeller, multiple Data Engineers |
| Acceptance Criteria | bulleted checklist | multi-dimensional (data validation tolerances – e.g., "100% record count match", UAT sign-off, decommissioning confirmation) |

---

## 3. Section-by-Section Content Guide

### Introduction
Same as Assessment SOW boilerplate. Second sentence states migration scope/path:
> *"This SOW outlines the comprehensive migration approach, deliverables, timelines, and resource requirements for migrating [Client]'s data platform from [legacy source – e.g., Azure Synapse Analytics Serverless and legacy SQL databases] to Microsoft Fabric."* (Lids Phase 1)

### Executive Summary
2–4 paragraphs:
- Para 1: business framing (transition from fragmented legacy → unified Fabric SaaS).
- Para 2: this phase's role (e.g., "Phase 1 establishes the foundational data infrastructure by migrating the Landing and Staging layers").
- Sub-sections (Phase 1 only): Business Drivers, Current State Challenges, Target State Benefits – each is a bulleted list.

### Current State Inventory
Heavy use of count tables. E.g. (Lids Phase 1):
| Objects | Landing (Synapse) | Staging | Total (Phase 1) |
|---|---|---|---|
| # Schemas | 1 | 14 | 15 |
| Tables | 227 | 229 | 456 |
| Views | 226 | 86 | 312 |
| Stored Procedures | 0 | 64 | 64 |

For Phase 2 / EDW migrations, add AAS Model Inventory table (Tables/Columns/Calculated Columns/Hierarchy/Measures per model) and EDW Inventory table.

### Target Architecture (Microsoft Fabric)
- **Architecture Components** bullets — each layer: OneLake (with Delta/Parquet), Bronze Lakehouse (Landing), Bronze Warehouse (Staging) / Gold Warehouse (Analytics), Fabric Semantic Models (Direct Lake), Power BI, CI/CD Framework.
- **Architecture Diagrams** — placeholder for inserted images per phase.
- **Data Flow Transformation** — table mapping current flow → future flow:
  | Flow | Current (Synapse & SQL) | Future (Fabric) |
  |---|---|---|
  | D365 Extraction | Synapse Link | Fabric Dataverse Link |
  | Landing/Ingestion | Synapse → Landing SQL | Bronze Lakehouse |
  | Transformation | Landing → Staging SQL | Bronze Lakehouse → Bronze Warehouse |
  | Reporting | Power BI → Synapse | Repointed Power BI |
- **Systems to be Decommissioned** — explicit bulleted list (e.g., Synapse Analytics Serverless, Landing/Staging SQL DBs, AAS Cubes, redundant CDC views).

### Project Scope (broken into 5-7 sub-sections per workstream)
Each sub-section is a focused work package with bulleted activities. Lids Phase 1 pattern:
- **5.3.1 Bronze Lakehouse (Landing Layer) Migration** – Fabric Dataverse Link, 227 tables, 226 views, CDC handling, monitoring
- **5.3.2 Bronze Warehouse (Staging Layer) Migration** – Fabric Data Warehouses (Test/Prod Dev/Prod Test/Prod), 329 tables, 86 views, 64 stored procs refactored
- **5.3.3 Repoint ADF Pipelines** – analyze existing, update to source from Bronze
- **5.3.4 Power BI Reports Migration** – inventory, repoint connection strings, test, deploy
- **5.3.5 CI/CD Framework** – Git repo, deployment pipelines Dev→Test→Prod, automated testing

Phase 2 / Gold pattern adds:
- Gold Warehouse (EDW) Migration: dimensional models (star/snowflake), SCD Type 1/2/3, aggregation tables, historical migration
- Data Pipelines (Bronze→Gold): incremental load, transformation, orchestration, error handling
- Fabric Semantic Models (replacing AAS Cubes): N cubes → N semantic models, Direct Lake connectivity, X DAX measures migrated, Y calculated columns, RLS, incremental refresh
- Power BI Reports Optimization: connect to Fabric Semantic Models, Direct Lake optimization, DAX optimization
- Data Pipelines (Gold→downstream): incremental pipelines to downstream consumers

Emory / parallel-workstream pattern: each workstream has its own Discovery, Architecture/Design, Development, Testing/UAT/Deployment sub-sections (≈ 7 sub-blocks per WS).

### Modular Release Strategy (Phase 2 / Emory)
Releases are scoped end-to-end and overlap. Canonical 5-release pattern (Lids Phase 2):
- **Release 1** (Wk 11–20): Foundation, Planning, Reference & Master Data
- **Release 2** (Wk 19–29): Core EDW – Reference & Master Data, Sales, Pricing, Inventory
- **Release 3** (Wk 25–33): Semantic Layer + Power BI Reports – Sales, Pricing, Inventory
- **Release 4** (Wk 25–36): Core EDW + Reports – Vendor Orders
- **Release 5** (Wk 26–38): Core EDW + Reports – Store Traffic, Comp Traffic + Final Cutover
- **Hypercare** (Wk 38–41): Post Go-Live Support

Emory variant uses release naming by phase (Release 1 Discovery, Release 2 Bronze/Silver, Release 3 Gold, Release 4 Platinum/SIT, Release 5 UAT/Deployment).

Each release block lists: focus, sprint window, key activities (bulleted), and key milestones with target weeks (e.g., "UAT – EDW: Reference & Master Data, Sales, Pricing (W26 - Jul 26, 2026)", "GO LIVE – Sales and Inventory Power BI Reports (W33 - Aug 31, 2026)").

### Fabric Capacity Planning
- **Data Volumes & Workloads** bullets: Database size (TB), AAS Model size (GB), concurrent user count, batch load window, peak concurrency %, report developer count, active hours.
- **Recommended Capacity & Estimated Cost** table:
  | Name | Region | Description | Estimated monthly cost |
  |---|---|---|---|
  | Prod - All | East US | F128, 128 Capacity units | $10,005 |
  | Dev/Test | East US | F64, 64 Capacity units | $5,002 |
  | Semantic Models (Prod) | East US | F128 | $10,005 |
- **Storage** table: OneLake storage ($0.026/GB), BCDR storage ($0.0468/GB), Cache ($0.20/GB) × current data size (GB).
- Mandatory footnote: *"The cost may vary in the future depending on consumption of Fabric which includes increase in data size leading to more data ingestions via pipelines/copy activities /Data Flows Gen2 usage & creation of more reports/semantic models & AI consumption (Copilot/ Data agents etc.)"*

### Risk & Mitigation (table)
Canonical 6-row risk table (Lids Phase 1 + Phase 2, identical content):
| Risk | Description | Mitigation Strategy |
|---|---|---|
| Functional Compatibility | Fabric T-SQL not full Azure Synapse parity | Replace external tables with Lakehouse shortcuts, refactor complex SQL to PySpark |
| Performance Risk | Azure Synapse vs Fabric SaaS execution model | Incremental loads, partitioned writes, move heavy logic to Spark |
| Data Movement Risk | External table dependencies | Fabric shortcuts and pipelines, refactor procedures |
| Operational Risk | Different monitoring and error handling | Fabric Pipelines scheduling, notebook orchestration, comprehensive monitoring & logging |
| Cost Risk | Capacity-based pricing model | Optimize procedures, move heavy logic to Spark, capacity monitoring |
| BI Impact | Report connectivity changes | Run Azure Synapse + Microsoft Fabric in parallel during transition |

Emory uses a simpler 3-row risk table (resource availability, environment access, scope creep / CCB).

### Assumptions & Dependencies
Far deeper than assessment SOW. Lids Phase 1 has 15+ project assumptions; Emory's are split into 7 sub-categories:
- Discovery and Scope Baseline
- Bronze/Silver and Source Availability
- Business Logic and Design Availability
- Dependency Framework Assumptions
- Approvals and UAT
- Data and Environment Readiness
- Engagement Scope Boundary

Common assumption clauses (verbatim-usable templates):
> *"Project timelines assume timely availability of prerequisites from [Client] team"*
> *"[Client] will provision timely access to all Fabric components and source systems"*
> *"Migration will be executed remotely with virtual collaboration"*
> *"Business requirements and transformation logic will be derived by Santor from existing code repositories, AAS models, ADF pipelines, and collaborative working sessions with the [Client] team — [Client] does not have formal documentation beyond what has already been shared and reviewed."* (Lids Phase 2 – useful for "no documentation" engagements)
> *"Any additional work beyond the scope above will be charged on a time and material basis."* (Lids Phase 2)

**Required Access** bullets: Microsoft Fabric workspaces (Dev/QA/Prod), OneLake/Lakehouse/Warehouse RW, source DB read-only, AAS read-only (with Tabular Editor), Power BI workspaces (admin), Azure DevOps/GitHub.

**Client Responsibilities**: provision access, assign SMEs, coordinate downstream system teams, conduct UAT and sign off, approve cutover plans, execute production deployment jointly.

**Collaboration sub-section** (Lids – unique to implementation): bilateral team obligations including knowledge-sharing sessions and dev tasks transitioning to client team during the engagement.

### Project Team & Responsibilities
**Santor Team Structure table** — sample (Lids Phase 1):
| Role | # of Resources | Responsibilities |
|---|---|---|
| Project Manager | 1 | Overall project management, stakeholder coordination, risk, sprint planning |
| Fabric Architect | 1 | Architecture design, technical leadership, capacity planning, governance |
| Fabric Data Engineer | 3 | Lakehouse/Warehouse implementation, pipelines, stored proc refactoring, migration, CI/CD |
| Power BI Specialist | 2 | Semantic model dev, AAS migration, DAX optimization, report migration, Direct Lake |
| Data Modeller | 1 | Study AAS models, map for Fabric semantic modelling |
| Tester | 1 | Test cases, validate Lakehouse/Warehouse/pipelines/semantic model |
| DevOps Engineer | 1 (Phase 2) | CI/CD, deployment automation, monitoring, environment management |

**Responsibility Matrix table** — Activity / Client / Santor columns with P/H/A codes. Typical 12-13 rows: Requirements & Discovery, Architecture Design, Environment Access Provisioning, Fabric Setup & Configuration, Data Migration & Transformation, Pipeline Development, Semantic Model Development, Power BI Migration, UAT, Go-Live & Cutover, System Decommissioning.

### Governance & Communication
- **Project Governance** bullets (more cadenced than POV): Daily Stand-ups (30 min), Weekly Status Reports, Bi-Weekly Sprint Reviews, Monthly Steering Committee, Issue Log, Risk Register.
- **Communication Channels** bullets: Client Microsoft Teams (primary), Client Email (formal), Client Azure DevOps Boards (sprint planning), Client SharePoint (artifacts).
- **Change Management** — 5-step structured process (vs. 3-bullet in POV): Submit written change request → Assess impact → Joint discussion → Formal approval and sign-off → Update project plan.

### Acceptance Criteria
- Bullet list of phase-specific completion criteria. Includes hard data validation thresholds, e.g.:
  - *"Data validation: 100% record count match between legacy and Fabric"* (Lids Phase 1)
  - *"All Stored procedures refactored and functioning correctly"*
  - *"UAT sign-off from [Client] business stakeholders"*
  - *"Azure Synapse Analytics Landing and Staging databases successfully decommissioned"*
- **Out of Scope** sub-section explicitly defers downstream work to subsequent phases (e.g., "Gold layer migration", "Fabric Semantic Models development in EDW", "Power BI report redesign").

### Engagement Cost
- Opening line states total cost net of partner funding:
  > *"The Total Estimated Cost to [Client] for Phase [N] Implementation & Training after Microsoft Funding is $[X]."*
- **Phase Implementation Cost** sub-section: Duration in weeks, Estimated Cost (gross), Microsoft Azure Accelerate Partner Led Funding (with annual commitment clause: *"$75,000 with an annual commitment of over $250,000 in ACR consumption by Lids"*), Net Customer Cost.
- **Training Cost** sub-section (optional): 3-day Fabric training, $3,000/day, Day-1 environment, Day-2 data engineering, Day-3 advanced (Git integration, optimization).
- **Hypercare Cost** sub-section (Phase 2 final-cutover only): 4 weeks, partial team, $20K-$30K range.

### Pricing tables (canonical):
**Total cost breakdown:**
| Phase 1 | Total Estimated Cost | Partner Led Funding* | Total Cost to [Client] |
|---|---|---|---|
| Implementation | $176,040 | ($75,000) | $101,040 |
| Training | $9,000 | | $9,000 |
| Total Estimated Cost | $185,040 | ($75,000) | $110,040 |

**Phase 2 pricing with ACMA (Azure Consumption Microsoft Account):**
| Phase 2 | Total Project Cost | Partner Investment | Net Project Cost | Microsoft Estimated ACMA* | Estimated Customer Cost |
|---|---|---|---|---|---|
| Implementation & Hypercare | $387,200 | $116,160 | $271,040 | $250,165 | $20,875 |

**Payment Schedule** — multi-invoice schedule tied to release milestones:
| Invoice # | Milestone | Timeline | Amount (USD) |
|---|---|---|---|
| INV01 | Completion of Planning | End of Week 2 | $25,260 |
| INV02 | Completion of Test Lakehouse & Warehouse | End of Week 7 | $25,260 |
| INV03 | Completion of Production Lakehouse & Warehouse | End of Week 10 | $25,260 |
| INV04 | Completion of Phase 1 | End of Week 13 | $25,260 |

**Training invoice** (when applicable):
| Invoice | Activity | Timeline | Amount |
|---|---|---|---|
| INV-Training | Training – Data Engineering on Fabric | Completion of Training | $9,000 |

**Emory's alt-pattern**: percentage-based milestone billing (50% at signing, 25% at 4 weeks, 15% at 10 weeks, 10% at closure).

### Expenses (implementation-only)
Standard $10K cap clause (verbatim-usable):
> *"Santor consultants shall charge reasonable expenses to Customer. The submitted expenses will be reviewed & approved by Customer. The total expenses shall not exceed $10,000. Such expenses will include, but not be limited to, mileage to and from the place of work, coach airfare for out-of-town travel, lodging, parking, bus or train fares, and meals and incidental expenses for out-of-town trips. Meals and incidental expenses will be reimbursed on a per diem basis using the applicable Internal Revenue Service rate."*

### Change Order
Same 3-paragraph clause as POV SOW.

### Payment Terms
- **Net 60** standard for Lids implementations
- **Net 30** for Emory implementations (per Truviz/Emory MSA)
- **Net 15** for ACME T&M extension
- Start Date is stated immediately above the Net term.

### Appendix B (Emory-only)
- **List of Reports to be Migrated** – table mapping reports to migration phase and t-shirt size (XS/S/M/L).
- **Complexity Scoring** – table explaining the t-shirt size methodology (Tables, Columns, Measures, Connection Types, Avg PQ Steps, SQL DBs, R script flag).

---

## 4. Timeline / Phasing Patterns

| Engagement | Total Duration | Phases / Releases | Hypercare |
|---|---|---|---|
| Lids Phase 1 | 13 weeks | 1 phase, ~10 sprints | not in Phase 1 |
| Lids Phase 2 | 28 weeks + 4 wks Hypercare | 5 releases (modular, overlapping) | 4 weeks |
| Emory (dual WS) | 20 weeks | 3 wks Discovery + 17 wks Execution; 5 releases per WS | not included |
| ACME SOW3 | 3 months | T&M ongoing support | n/a |

**Implementation timeline conventions:**
- Stated explicitly: "Phase 1 Duration: 13 weeks", "Phase 2 Duration: 27 weeks development + 4 weeks Hypercare"
- Milestones tagged "W[N] - [Date]" format throughout release descriptions
- Major checkpoints: Architecture sign-off (Wk 2-4), Bronze SIT, Silver SIT, Gold SIT, Semantic Model Walkthrough, UAT per release, Go-Live, Hypercare
- 5-release pattern overlaps releases substantially (Release 2 starts Wk 19 while Release 1 ends Wk 20)

---

## 5. Resource Roles (Implementation-specific)

Implementation teams are 2-3x larger than POV teams. See `resource-roles.md` for full catalog. Implementation-only roles:
- DevOps Engineer (Lids Phase 2)
- Data Modeller (separate from Architect, focuses on AAS → semantic model mapping)
- Senior Data Engineer (vs. just "Data Engineer" in POVs)
- Data Engineering Team A / Team B (parallel pods in HLPP plan)
- Solutions Architect (Emory – synonymous with Fabric Architect; "Solution Architect" in ACME)
- Business Analyst (Emory – Discovery facilitation, requirements capture, UAT coordination)
- Fabric Engineers (Emory – plural; pipeline & notebook builds)
- Power BI Developers (Emory; plural)
- QA Engineer / Tester / QA Team

---

## 6. Notable Patterns to Encode

1. **Inventory counts drive pricing.** Real numbers from Lids: "227 tables ingestion from D365", "226 views in Bronze Lakehouse", "329 tables migrated from D365", "64 stored procedures refactored to Fabric-compliant T-SQL or PySpark", "8 AAS cubes migrated", "3,993 DAX measures", "1,293 calculated columns". Always quote these explicitly in scope subsections — they justify resource counts and duration.
2. **Multi-environment scope.** Implementation SOWs always cover Dev/Test/Prod (sometimes Test/Prod-Dev/Prod-Test/Prod). Environment access provisioning is a Project Assumption AND a Required Access bullet AND a Responsibility Matrix line item.
3. **Decommissioning is part of scope.** Implementation SOWs explicitly list legacy systems to be decommissioned (Synapse, Staging SQL, AAS cubes) and treat decommissioning as a final-release activity with its own milestone and matrix row.
4. **Microsoft funding mechanics:** Two funding vehicles appear: (a) **Microsoft Azure Accelerate Partner Led Funding** (~$75K against annual ACR commitment ~$250K) – Phase 1 model. (b) **Microsoft ACMA** (Azure Consumption Microsoft Account / pending approval, applied via amendment) – Phase 2 model with much larger funding. Partner Investment from Santor is also a line item (~30% of net cost).
5. **Capacity SKU recommendations are F-tier based on workload tier:**
   - F4 = POV / dev evaluation (~$300/mo)
   - F64 = single environment workload (~$5K/mo)
   - F128 = production all + semantic models (~$10K/mo)
   - Combined production estate often $25K-$45K/mo + storage ($150-$700/mo).
6. **Data validation tolerance is "100% record count match"** between legacy and Fabric — explicit acceptance criterion in Phase 1.
7. **Discovery is mandatory and re-baselining is gated.** Emory's SOW formalizes this: a 3-week mandatory Discovery period at start, followed by a re-baselining checkpoint where any material variance triggers Change Request before execution proceeds.
8. **Modular release strategy** rather than linear waterfall: releases overlap, each is end-to-end (data + semantic + reports + UAT + Go-Live for its subject area).
9. **Domain-based release decomposition** is standard for EDW migrations: Reference & Master Data → Sales/Pricing/Inventory → Vendor Orders → Store Traffic/Comp Traffic → Final Cutover. Each domain gets its own EDW build + Semantic Model + Power BI release.
10. **Two payment-schedule patterns:**
    - **Milestone-pegged** (Lids): equal invoices tied to deliverable completion (~25% × 4)
    - **Percentage-pegged** (Emory): 50% at signing, 25% mid-engagement, 15% later, 10% at closure
11. **T&M extension SOW** (ACME pattern): minimal SOW (~2 pages of substance), defines hourly rates, monthly invoicing, minimum 8 hrs/day & 40 hrs/week, 4-hour overlap window stated explicitly (until 12 PM EST), Net 15 payment.
12. **Training is a separate cost line** that customer can elect: 3-day virtual instructor-led ($9K total at $3K/day, up to 12 participants), with a 14-module curriculum covering Fabric environment → Data Engineering → Advanced (Mirroring, Query Insights, Git integration).
13. **Emory's "Platinum Layer"** is a notable extension to the standard medallion architecture: Bronze (Landing) → Silver (Standardized) → Gold (Curated/Harmonized) → **Platinum (Curated marts, review datasets, downstream-oriented outputs, versioned snapshots)**. This is a 4-layer pattern agents should recognize when scoping Emory-type engagements.
14. **Emory dependency-based refresh framework** is a non-standard but reusable scope element: a metadata-driven control system that holds release of Gold/Platinum refreshes until upstream readiness, freshness, and validation gates pass. Worth encoding as an optional scope module.
15. **"Lift-and-shift" vs. "Native rebuild"** is an explicit design decision called out in Phase 2 SOWs: *"All components are redesigned natively on Fabric rather than lifted-and-shifted from existing environments"* (Lids Phase 2). Phase 1 SOWs are typically lift-and-shift (Bronze layer); Phase 2 SOWs are native rebuild (Gold + Semantic).
