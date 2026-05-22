# Common Patterns Across All SOWs and Project Plans

Cross-cutting patterns observed across the 6 SOWs and 4 project plans. These are the reusable building blocks an agent should know.

---

## 1. How Microsoft Fabric is Described

### Canonical architecture vocabulary

The SOWs converge on the following named layers and components:

**Storage / Compute Layers (Medallion Architecture):**
- **OneLake** — *"Unified data lake with Delta/Parquet open format storage"* (LIDS-1, LIDS-2). Always described as the storage foundation.
- **Bronze Lakehouse (Landing Layer)** — *"Raw data ingestion from D365 via Fabric Dataverse Link"* / *"Raw landing zone for source-aligned ingestion"* (Emory) / *"Raw, immutable, audit trail"* (APX-A).
- **Silver Lakehouse / Layer** — *"Cleansed, validated, reusable data layer"* (APX-A) / *"Standardized technical integration layer created through the ingestion framework"* (Emory).
- **Bronze Warehouse (Staging Layer)** — *"Cleansed, deduplicated, and business-rule-applied data layer"* (LIDS-1). Note: Lids uses "Bronze Warehouse" rather than "Silver" for their staging level.
- **Gold Warehouse / Layer** — *"Analytics-ready layer for Semantic Model & Power BI"* (APX-A) / *"Optimized star/snowflake schemas with aggregations"* (LIDS-2) / *"Harmonized business-rule transformation"* (Emory).
- **Platinum Layer** (Emory-specific 4th tier) — *"Curated data marts, review datasets, downstream-oriented outputs, and versioned snapshots."* Sits above Gold; presentation-ready curated data for shared semantic models.

**Compute / Workload Components:**
- **Fabric Dataverse Link** (D365 → Fabric direct connection)
- **Fabric Data Factory pipelines** (replaces Azure Data Factory)
- **Fabric Notebooks (PySpark / Python)** (replaces SSIS / R scripts / complex SQL stored procedures)
- **Fabric Data Pipelines** (orchestration, scheduling)
- **Fabric Data Warehouses** (T-SQL endpoint, used for Gold)
- **Fabric Lakehouses** (Delta tables, used for Bronze/Silver)
- **Fabric Semantic Models** (replaces SSAS / Azure Analysis Services cubes)
- **Direct Lake mode** (semantic model connectivity without import — *"Power BI: Connection to Gold Warehouse without intermediate data copies"* — LIDS-2)
- **Copilot in Fabric / Copilot in Power BI / Copilot in Data Factory** (always called out as AI value driver)
- **Data Agents** (mentioned as emerging capability — ACME, APX-A)
- **Fabric Planner** (mentioned in ACME)
- **Translytical workflows** (mentioned in ACME)
- **Mirroring / Real-time data replication** (training module reference)
- **Q&A / Natural language** (Copilot enablement scope)

### Capacity tiers (Fabric F-SKU)

Explicit capacity recommendations from real SOWs:

| Capacity | Monthly Cost | Use case | Source |
|---|---|---|---|
| **F4** | ~$300/mo | POV / Free Trial / Assessment scope | APX-A, NYU |
| **F64** (64 CU) | $5,002/mo | Single environment Dev/Test or single workload (D365, ETL data dev/test/prod) | LIDS-1, LIDS-2 |
| **F128** (128 CU) | $10,005/mo | Prod-All, Semantic Models Prod, or combined large workload | LIDS-1, LIDS-2 |

**Storage pricing (always quoted as a separate line item):**
- OneLake storage: $0.026 / GB / month
- OneLake BCDR storage: $0.0468 / GB / month
- OneLake cache: $0.20 / GB / month

**Combined production estate examples:**
- LIDS Phase 1: F128 Prod + F64 Dev/Test + F128 Semantic = $25,033/mo capacity + $819/mo storage
- LIDS Phase 2: 7×capacity SKUs (mix of F64 and F128) = $45,024/mo + $437/mo storage
- Yearly reserved: ~$310K (Phase 1) → ~$546K (Phase 2)

**Standard cost-variability footnote** (verbatim-usable):
> *"The cost may vary in the future depending on consumption of Fabric which includes increase in data size leading to more data ingestions via pipelines/copy activities /Data Flows Gen2 usage & creation of more reports/semantic models & AI consumption (Copilot/ Data agents etc.)"*

### Microsoft Funding Mechanics

Three funding vehicles named in SOWs:
1. **Microsoft Partner Led Funding** — assessment / POV engagements. Typical: $15K offset against a ~$25K total cost. (APX-A)
2. **Microsoft Azure Accelerate Partner Led Funding** — implementation engagements. Typical: $75K against client annual commitment of >$250K ACR consumption. (LIDS-1)
3. **Microsoft ACMA** (Azure Consumption Microsoft Account) — pending-approval funding model applied via amendment. Significant offsets (Phase 2: $250K). Standard clause:
> *"Microsoft funding associated with this engagement is currently pending approval. Upon written confirmation of approval, the applicable funding will be applied to this Statement of Work and reflected through a formal amendment."* (LIDS-2)

**Partner Investment** is a separate line — Santor/Truviz absorbs ~30% of the net cost via "Partner Investment" to make pricing competitive.

---

## 2. Common Assumptions / Exclusions Language

### Standard project assumption clauses (verbatim-usable)

**Access / SLA:**
> *"Project timelines assume timely availability of prerequisites from [Client] team"*
> *"[Client] will provide access to the [resource] within [N] business day(s) of project kickoff"*
> *"Access credentials for [source systems] (read-only) will be provisioned within 2 business days of kick-off"*
> *"A Microsoft Fabric capacity (F-[N] SKU or equivalent) will be provisioned and accessible to Santor by Day 1"*
> *"Santor team will have Fabric workspace Admin access for the duration of the engagement"*
> *"[Client] IT/data team will be available for knowledge transfer sessions during the assessment (estimated 2-3 hours per week)"*

**Delivery model:**
> *"Migration will be executed remotely with virtual collaboration"*
> *"[Client] will provision timely access to all Fabric components and source systems"*
> *"[Client] team will be available for discovery sessions, validation, and UAT"*

**Documentation / Knowledge:**
> *"Current inventory (tables, pipelines, cubes) is accurate as per assessment findings"*
> *"Existing documentation and code repositories are accessible"*
> *"It is assumed that there isn't much documentation available outside of the Code repository"* (LIDS-1)
> *"Business requirements and transformation logic will be derived by Santor from existing code repositories, AAS models, ADF pipelines, and collaborative working sessions with the [Client] team — [Client] does not have formal documentation beyond what has already been shared and reviewed."* (LIDS-2)

**UAT / Sign-off:**
> *"UAT will be conducted by [Client] SMEs and sign-off will be provided within the [N]-week timeline"*
> *"UAT will be treated as validation of agreed scope, not first-time requirements discovery."* (Emory)
> *"Business KPI definitions and expected values will be validated by [Client] during Week [N]"*

**Change-control trigger:**
> *"Any additional scope beyond what is defined will be addressed via a Change Order"*
> *"Any additional work beyond the scope above will be charged on a time and material basis."* (LIDS-2)

### Standard Out-of-Scope exclusions

Items routinely excluded:

**POV / Assessment SOWs:**
- Production deployment or DevOps/CI-CD pipeline setup
- Row Level Security (RLS) implementation (scoped for implementation phase)
- Mobile layout optimization
- Ongoing support or maintenance post-engagement
- Full migration beyond demonstrated scope
- Enterprise data modeling beyond demonstration purposes
- Custom application / UI / portal development
- Performance tuning for production scale
- Integration with non-agreed systems
- User training programs beyond basic demonstrations or KT sessions
- New report development beyond auto-generated Copilot reports

**Implementation SOWs:**
- Power BI report redesign / new visuals, pages, KPIs
- Mobile layout optimization
- Custom visual development
- Source system modifications or enhancements
- Net-new reporting use cases outside the agreed target process
- Source-system remediation owned by Client or third parties
- Platform-wide DevOps redesign (unless Discovery confirms)
- Enterprise governance operating-model redesign
- Post-deployment hypercare (sometimes included as separate scope)
- New KPI definition or net-new business logic (unless approved via change control)

### Emory's structured Change Request triggers (a useful checklist)
- Addition of source systems, source instances, or required entities after Discovery sign-off
- Changes to logic, mappings, review model, or submission requirements
- Previously unidentified Bronze/Silver gaps requiring materially higher ingestion or remediation effort
- Redesign of Gold or Platinum structures after approval
- Dependency-framework redesign or additional exception handling beyond approved baseline
- Non-representative dev/test data requiring materially higher remediation
- Delayed approvals, SME unavailability, or access delays that materially affect schedule
- New downstream use cases beyond the approved scope
- Discovery finding that a file source originates from or requires sourcing from a live transactional system (Emory's "most frequently anticipated" CR trigger)
- File schema instability identified during pipeline development
- PHI or sensitive clinical data identified in SharePoint or CSV files

---

## 3. Acceptance Criteria Patterns

### Standard pattern: bulleted checklist with hard validation thresholds

**POV / Assessment** (APX-A pattern):
- Source tables loaded into Bronze Lakehouse **with checked row counts**
- Silver layer tables meet data quality standards (**key fields complete, correct types, no duplicates**)
- Gold Warehouse star schema active with FactMetrics and DimCalendar filled
- Semantic Model's N KPI DAX measures **validated against source**
- Copilot in Power BI enabled and responsive to natural language on the Semantic Model
- At least one Copilot-generated Power BI report produced
- UAT sign-off obtained from [Client] SME
- Technical documentation and handover provided

**Implementation** (LIDS-1 pattern):
- Bronze Lakehouse fully operational with all D365 tables ingested
- Bronze Warehouse contains N tables N views with correct data
- All Stored procedures refactored and functioning correctly
- **Data validation: 100% record count match between legacy and Fabric**
- Power BI reports connected to Bronze Lakehouse, Warehouse with accurate data
- ADF pipelines for downstream systems repointed using Fabric as source
- UAT sign-off from [Client] business stakeholders
- Complete documentation delivered and reviewed
- Legacy databases successfully decommissioned

**Phase 2 / Native rebuild** (LIDS-2 pattern):
- Conceptual data model rationalization
- Logical data model changes (table structures, columns, keys, constraints)
- Dimensional model optimization (star/snowflake schemas)
- Slowly Changing Dimension (SCD Type 1/2/3) implementations
- Aggregation table design and summary tables
- Data quality validations and business rules implementation
- Physical model optimizations (partitioning, distribution, indexing for Fabric)
- Power Query transformation modifications for Direct Lake compatibility
- Incremental refresh configuration
- Row Level Security (RLS) implementation
- DAX optimization and calculation groups

---

## 4. Change Request Process Language

### The canonical 3-paragraph clause (LIDS / APX / NYU – used verbatim)

> *"Either [Client] or Santor may request changes to the SOW for Services and/or any other aspect of the SOW through a written change request as set forth in Exhibit A to the Agreement ("Change Order"). Both the parties shall discuss and negotiate in good faith the impact of the Change Request on the services, pricing, timing, and other terms of the applicable SOW.*
>
> *Any changes to the SOW agreed upon by the parties will result in a Change Order signed by the parties. Once a Change Order is signed, it shall become a part of the applicable SOW.*
>
> *Please refer to Appendix A for the Change Order template."*

### 5-step structured change management process (implementation SOWs)

Lids implementation SOWs add a 5-step process bullet list separate from the Change Order clause:
1. Submission of a written change request by either party
2. Assessment of the impact on scope, effort, cost, and schedule
3. Joint discussion and alignment on proposed changes
4. Formal approval and sign-off of the change order
5. Updates to the project plan and supporting documentation

### Change Order Appendix template (consistent across all SOWs)

Two-column Item/Description table:
- Requester
- Change Order Origination Date
- Change Order Number
- Change Order Description
- Change Order Details
- Cost Estimate and Impact
- Schedule Impact
- Comments

Followed by signature blocks for both parties.

### CCB (Emory-specific addition)

Emory introduces a joint Change Control Board for active monitoring:
> *"Constitute a joint Emory and Truviz change control board (CCB) to closely monitor the impact of such changes, prioritize and approve them. Deploying a robust change management process."*

---

## 5. Governance & Communication Patterns

### Implementation SOW governance cadence

Standard 6-bullet pattern (Lids):
- **Daily Stand-ups**: 30-minute team sync to review progress, blockers, and priorities
- **Weekly Status Reports**: Updates on accomplishments, upcoming activities, risks, and issues
- **Bi-Weekly Sprint Reviews**: Demonstrations of completed work with stakeholders and gather feedback
- **Monthly Steering Committee**: Executive updates on progress, budget, timelines, and key decisions
- **Issue Log**: Centralized tracking of issues including severity, ownership, and resolution timelines
- **Risk Register**: Ongoing risk identification, assessment, and mitigation planning

### POV SOW governance (lighter)
- Weekly Status Calls (30-min client sync)
- Mid-Engagement Demo (end of Week 2)
- Assessment Checkpoint (end of Week 3)
- Final Demo & UAT (Week 4)
- Issue Log

### Communication Channels (consistent)
- **Primary collaboration**: Microsoft Teams
- **Formal documentation**: Email / SharePoint
- **Sprint planning / task tracking**: Client Azure DevOps Boards (implementation) or just email/SharePoint (POV)
- **Repository for artifacts**: SharePoint
- **Weekly written status update**: delivered Friday (POV pattern)

---

## 6. Term & Termination / Legal Framework

### MSA-anchored SOWs

Some SOWs are issued under a pre-existing Master Services Agreement and explicitly defer:
> *"This SOW is subject to the terms and conditions contained in the Agreement between [Client] and Supplier and is made a part thereof. Any term not otherwise defined herein shall have the meaning specified in the Agreement. In the event of any conflict or inconsistency between the terms of this SOW and the terms of this Agreement, the terms of this SOW shall govern and prevail."* (Emory)

### Pass-through / sub-supplier structure

Emory's SOW is uniquely fronted by Truviz with Santor as sub-supplier:
> *"This Statement of Work ("SOW") is issued by Santor Technologies, LLC ("Santor") to Truviz Inc. ("Truviz") for delivery of the project scope outlined herein for Emory Healthcare ("Customer"). All terms and conditions remain unchanged from those provided to the Customer."*
>
> *"Truviz agrees to pay Santor in accordance with the Payment Schedule set forth in Section 5. Payment will be made within five (5) business days from the date Truviz receives payment from the Customer."*

### Acceptance language (standard)
> *"By signing below, both parties agree to the terms and conditions outlined in this Statement of Work for the [project name] project."*

The Acceptance section is always at the end and contains a 2-column signature block: Client (Signature/Name/Title/Date) × Vendor (Signature/Name/Title/Date).

---

## 7. Payment / Invoicing Patterns

### Payment terms by engagement type

| Engagement | Net Term | Notes |
|---|---|---|
| Assessment / POV (APX-A) | **Net 30** | Standard |
| POC (NYU) | **N/A** | No-cost engagement |
| Implementation (LIDS-1, LIDS-2) | **Net 60** | Standard for Santor-direct |
| Implementation pass-through (EMORY-SOW) | **30 days from invoice** to Emory; **5 business days** from Truviz to Santor after receipt | Sub-supplier pattern |
| T&M support (ACME) | **Net 15** | Faster cycle for retainer-style |

### Invoicing structure variants

**1. Single-invoice (POV)**:
- One invoice at completion of engagement.

**2. Milestone-pegged (Lids implementation)**:
- 4 equal invoices tied to delivery checkpoints (Planning, Test environment, Prod environment, Phase Complete).
- Each invoice ~25% of total.

**3. Percentage-pegged (Emory implementation)**:
- 50% at start of project / signing of SOW
- 25% upon completion of 4 weeks (or specific calendar date)
- 15% upon completion of 10 weeks (or specific calendar date)
- 10% project closure

**4. T&M monthly (ACME)**:
- *"Santor will invoice monthly based on actual hours worked by the assigned resources."*
- Minimum 8 hrs/day, 40 hrs/week.

**5. Training invoice (when included)**:
- Single invoice at completion of training program ($9K typical at $3K/day × 3 days).

### Expenses clause (implementation SOWs only)

Standard $10K-capped expenses clause with per-diem boilerplate:
> *"Santor consultants shall charge reasonable expenses to Customer. The submitted expenses will be reviewed & approved by Customer. The total expenses shall not exceed $10,000. Such expenses will include, but not be limited to, mileage to and from the place of work, coach airfare for out-of-town travel, lodging, parking, bus or train fares, and meals and incidental expenses for out-of-town trips. Meals and incidental expenses will be reimbursed on a per diem basis using the applicable Internal Revenue Service rate."*

Emory variant omits the $10K cap; ACME and POV SOWs omit the expenses section entirely (remote-only).

---

## 8. Other Cross-Cutting Patterns

### Responsibility Matrix legend (P/H/A)
Used in 100% of SOWs that have a matrix:
- **P = Perform.** The designated Party will perform the service.
- **H = Help.** The designated Party will provide the assistance to enable the performer to complete the designated service.
- **A = Approve.** The performance of the service is subject to the designated Party's approval.

Compound codes are allowed (P/A, A/H, H/A, H, P) and frequently appear when both parties co-execute (e.g., "Production deployment" or "User Acceptance Testing").

### Standard SOW cover page
Title block in this order:
1. "Statement of Work (SOW) for" / "Statement of Work (SOW)"
2. Engagement name (e.g., "Microsoft Fabric Migration / Phase 1 Implementation")
3. "Presented to"
4. (Client logo / blank space)
5. Date (e.g., "January 13, 2026")
6. Contact info block (right-aligned table cell): name, title, email, mobile.

### Standard date / address format
- Date in SOW header: "January 13, 2026" (full month name, day, year)
- Addresses: "[Co Name] having an address at [Street, Suite #, City, State ZIP]"

### Standard Santor identity boilerplate
> *"Santor Technologies, LLC. having an address of 371 Hoes Lane, Suite 200, Piscataway, NJ 08854, USA ("Santor")."*

(Note: ACME SOW uses a different address: 4 Peak Lane, Suite 104, Hillsborough, NJ 08844. Likely an older / branch address.)

### Fabric-specific training curriculum (when training is in scope)
3-day virtual curriculum (LIDS-1):
- **Day 1 — Microsoft Fabric Environment**: Introduction to Microsoft Fabric, OneLake and Direct Lake, Lakehouse architectures (medallion) - Bronze/Silver/Gold layers, Data Flows Gen2, Apache Spark
- **Day 2 — Data Engineering in Microsoft Fabric**: Fabric Notebooks, Deep Dive on Lakehouses, Direct Lake, Building Efficient Data Pipelines, Loading Data Flows Gen2/Power Query into Fabric Lakehouse
- **Day 3 — Advanced Data Engineering**: Data Mirroring (Real-time data replication), Query Insights and Optimization, Data Engineering Best Practices, Fabric GIT Integration with Azure DevOps

Pricing: $3,000/day × 3 = $9,000 standard. Includes hands-on labs, up to 12 participants, materials. Customized training and in-person delivery incur additional cost.

### Standard Data Flow narrative (for POV)
> *"[Source] → Bronze Lakehouse (Raw Ingestion via Fabric Data Pipeline) → Silver Lakehouse (Transformation via Spark Notebooks) → Gold Warehouse (Star Schema via SQL) → Semantic Model (Direct Lake) → Power BI Copilot & Reports"*

### Discovery as a formal gate (Emory pattern)
> *"Discovery is mandatory and will be used to validate the true baseline before full execution is locked."*
> *"At the end of Discovery, [Client] and the implementation team will confirm the approved execution baseline. Any material variance in source scope, landed data readiness, business logic, dependency complexity, or required remediation will impact timeline and cost and will be documented and processed through the Change Request mechanism."*

This 3-week mandatory Discovery + Re-baselining checkpoint is a reusable scope pattern for any engagement where source/legacy complexity is uncertain at SOW signing.

### Hypercare structure (Phase 2 / final-cutover SOWs)
4-week post-go-live period with:
- Daily monitoring and issue resolution
- Performance tuning and optimization
- User support and training reinforcement
- Documentation updates based on lessons learned
- Partial team allocation (Fabric Data Engineers primarily)
- Cost: ~$20K-$30K (1/12 of total project cost approximate)
