# Assessment / POV / POC SOW – Template Structure

Reference docs:
- `004a3f7f-APEX_SOW_Assessment_and_POV__02242026.docx` (APEX – 4-week parallel Assessment + POV)
- `4e9b32d9-NYULH__POC_SOW_11_20_2025.docx` (NYULH – 6-week parallel Data Factory + Power BI POC)

These engagements share the same DNA: short (4-6 weeks), 2 parallel workstreams, lighter governance, lower commercial value ($10K-$30K customer cost typical, often subsidized by Microsoft Partner Funding or delivered at no cost as a proof of value).

---

## 1. Canonical Section Order

The two assessment/POV SOWs converge on this skeleton. APEX uses formal numbered headings (1–12 + Appendix); NYULH uses unnumbered H1s but follows the same flow.

| # | Section | Required? |
|---|---|---|
| Cover page | Title block: "Statement of Work (SOW) for / [Engagement Name] / Presented to [Client] / [Date]" + Santor contact card | yes |
| 1 | Introduction | yes – party names, addresses, effective date |
| 2 | Executive Summary | yes (APEX) / merged into Scope (NYULH) – business context and workstream summary |
| 3 | Workstream 1: [Assessment / Discovery / Data Factory POC] | yes |
| 3.x | Deliverables & Timeline (per workstream) | yes |
| 4 | Workstream 2: [POV / Power BI POC] | yes |
| 4.x | Source / Target Architecture (Medallion: Bronze/Silver/Gold) | yes for POV; describes Fabric components |
| 4.x.x | Architecture Layers / Data Flow / AI-Readiness for Copilot / Semantic Model | yes |
| 4.x | Deliverables & Timeline (per workstream) | yes |
| 5 | Project Team & Responsibilities | yes |
| 5.x | Responsibility Matrix (per workstream) | yes – uses P/H/A scheme |
| 6 | Governance & Communication | yes |
| 6.x | Project Governance / Communication Channels / Change Management | yes |
| 7 | Assumptions, Access & Client Responsibilities | yes |
| 7.x | Project Assumptions / Required Access / Client Responsibilities | yes |
| 8 | Acceptance Criteria (incl. Out of Scope) | yes |
| 9 | Engagement Cost (table with Microsoft Funding column) | yes |
| 10 | Payment Schedule | yes |
| 11 | Payment Terms (Net 30 typical; N/A for no-cost POC) | yes |
| 12 | Change Order (process language) | yes |
| – | Acceptance (signature block) | yes |
| Appendix A | Change Order template (Item/Description table) | yes |

---

## 2. Section-by-Section Content Guide

### Introduction
- Single short paragraph. Names both parties, addresses, and the SOW effective date.
- Pattern: *"This Statement of Work (SOW) is dated [DATE], between [CLIENT NAME], having an address at [ADDRESS] ("[CLIENT]") and Santor Technologies, LLC. having an address of 371 Hoes Lane, Suite 200, Piscataway, NJ 08854, USA ("Santor")."* (APEX, NYULH – identical phrasing)
- Second paragraph states what the SOW outlines: scope, exclusion, assumptions, solutioning approach for the POC/Assessment.

### Executive Summary
- 2–4 sentences of business context: existing state pain points (legacy systems, manual processes, urgency drivers).
- Restates the workstreams as a bullet pair (a 2-row table titled "Workstream / Goal" is the canonical visualization – used in both APEX and NYULH).

### Workstream 1 (Assessment / Discovery)
Typical sub-elements:
- "Scope" table with **Assessment Area | Scope** columns. APEX uses: Current State Documentation, Source System Assessment, Data Volume Assessment, Data Quality Assessment, Report Inventory, Future State Architecture, Implementation Roadmap.
- "Deliverables & Timeline" table with **Week | Milestone | Activities** columns. Each row lists bulleted activities and a "Deliverable:" line.
- Outputs always include: Current State Assessment Report; Report Inventory; Future State Architecture Design; Phased Implementation Roadmap & follow-on SOW.

### Workstream 2 (POV / POC)
- "Source" subsection – describes the input dataset (e.g., "Flash Reporting Excel first page"). Includes a table with **Table Name | Key Columns | Description | Granularity**.
- "Target Architecture" subsection – describes the Fabric Medallion (Bronze / Silver / Gold). Standard table: **Layer | Fabric Component | Contents | Purpose**.
- "Data Flow" – one-liner showing the path: *"[Source] → Bronze Lakehouse (Raw Ingestion via Fabric Data Pipeline) → Silver Lakehouse (Transformation via Spark Notebooks) → Gold Warehouse (Star Schema via SQL) → Semantic Model (Direct Lake) → Power BI Copilot & Reports"* (APEX – verbatim, useful template).
- "AI-Readiness for Copilot in Power BI" subsection – bulleted list covering Certified Semantic Model with linguistic schema, KPI definitions in display folders, Q&A field mappings, Copilot enablement, Copilot summary visuals.
- "Semantic Model with N KPIs" subsection – grid table listing the KPI measures (3 columns × N rows).
- Deliverables & Timeline table same shape as WS1.

### Project Team & Responsibilities
- Role table (**Role | Allocation | Responsibilities | Owner** – APEX format) lists 4-6 named roles. See `resource-roles.md` for catalog. Typical assessment/POV team:
  - Fabric Consultant (2-4 weeks)
  - Data Architect (4 weeks)
  - BI Engineer or Power BI Consultant (2-4 weeks)
  - Project Manager (part-time, 25% allocation)
  - Fabric Principal Architect (NYULH only – PoC technical strategy)
- Responsibility Matrix tables (one per workstream) with **Activity | Client | Santor** columns. Cell values are codes: P=Perform, H=Help, A=Approve (or compound codes like P/A, A/H).
- Legend immediately above each matrix: *"P = Perform | H = Help/Assist | A = Approve"*.

### Governance & Communication
- 3 bulleted sub-sections:
  - Project Governance: weekly status calls (30-min), mid-engagement demo, assessment checkpoint, final demo & UAT, issue log
  - Communication Channels: Teams or email; SharePoint for formal documents; weekly written status update (typically Friday)
  - Change Management: brief 3-bullet pattern – *"Any modification to scope, timeline, or budget will require a written Change Order; Both parties will assess impact and agree on revised terms before proceeding; All approved Change Orders become amendments to this SOW."* (APEX – verbatim)

### Assumptions, Access & Client Responsibilities
- **Project Assumptions** (10-12 bullets): access SLAs (e.g., "Apex will provide access to the Flash Reporting Excel file within 1 business day"), Fabric capacity provisioning ("F-4 SKU or equivalent will be provisioned and accessible by Day 1"), Santor workspace Admin access, IT/data team availability (2-3 hrs/week), UAT timeline, remote execution, change-order clause.
- **Required Access** (bulleted): Fabric workspace Admin, OneLake/Lakehouse/Warehouse read-write, Power BI workspace Admin, Copilot in Fabric enabled on tenant, source system credentials.
- **Client Responsibilities**: assign SME for KPI validation, provision Fabric capacity, facilitate source access, make IT available, conduct UAT.

### Acceptance Criteria
- Bullet list per workstream describing what "done" looks like (e.g., "Flash Reporting source tables loaded into Bronze Lakehouse with checked row counts", "Copilot in Power BI enabled and responsive to natural language on the Semantic Model", "UAT sign-off obtained from Client SME").
- Sub-section **Out of Scope** with 6-8 explicit exclusions (e.g., production deployment, DevOps/CI-CD setup, RLS, mobile layouts, ongoing support, full report migration deferred to implementation SOW).

### Engagement Cost
- Opening sentence: *"The estimated value for this engagement is $[X] with an anticipated duration of [N] weeks. The engagement is scheduled to commence on [DATE]."*
- Microsoft Partner Funding line: *"The Total Estimated Cost to customer for [Engagement] after Microsoft Funding & Partner Investment is $[X]."*
- T&M overage clause: *"Any services required beyond the outlined scope will be billed on a time-and-materials basis and must be approved and signed off by both [Client] & Santor."*
- For no-cost POCs (NYULH): *"This is a no-cost engagement for [Client], intended to showcase Santor's capabilities and proof of value. However, the estimates below provide transparency on the value being delivered."*

### Pricing Table Structure (canonical)
| Activities | Total Project Cost | Microsoft Partner Led Funding | Estimated Customer Cost |
|---|---|---|---|
| Assessment & POV | $25,760 | $15,000 | $10,760 |

Followed by a resource breakdown:
| Role | Number of Resources | Duration |
|---|---|---|
| Fabric Consultant | 1 | 2 weeks |
| Data Architect | 1 | 4 weeks |
| BI Engineer | 1 | 4 weeks |
| Project Manager | 1 | 4 weeks (25% allocation) |

### Payment Schedule
Single-row invoice table:
| Invoice # | Milestone | Timeline | Customer Cost |
|---|---|---|---|
| INV01 | Completion of Engagement | Week 4 | $10,760 |

### Payment Terms
- "Net 30 from date of invoice." (APEX)
- "N/A" for no-cost POCs (NYULH)

### Change Order
Standard 3-paragraph clause (use verbatim from APEX/NYULH):
> *"Either [Client] or Santor may request changes to the SOW for Services and/or any other aspect of the SOW through a written change request as set forth in Exhibit A to the Agreement ("Change Order"). Both the parties shall discuss and negotiate in good faith the impact of the Change Request on the services, pricing, timing, and other terms of the applicable SOW. Any changes to the SOW agreed upon by the parties will result in a Change Order signed by the parties. Once a Change Order is signed, it shall become a part of the applicable SOW. Please refer to Appendix A for the Change Order template."*

### Acceptance Signature Block
Two-column 1-row table with stacked Signature/Name/Title/Date for each party.

### Appendix A – Change Order Template
Two-column table:
| Item | Description |
|---|---|
| Requester | |
| Change Order Origination Date | |
| Change Order Number | |
| Change Order Description | |
| Change Order Details | |
| Cost Estimate and Impact | |
| Schedule Impact | |
| Comments | |

Followed by signature lines for both parties.

---

## 3. Timeline Patterns

- **Duration:** 4 weeks (APEX combined assessment+POV) or 6 weeks (NYULH 2-workstream POC).
- **Cadence:** Weekly milestones; activities listed bulleted per week.
- **Common week names:**
  - Week 1: "Kick off & Assessment Launch" / "Environment & Access Setup"
  - Week 2: "Report Inventory" / "Connector & Pipeline Build"
  - Week 3: "Assessment Draft & Semantic Model" / "On-Prem Gateway / Write-back & Copilot Testing"
  - Week 4 (final): "Final Delivery & Sign-Off"
- **Checkpoints:** Mid-engagement live demo (end of Week 2), Assessment checkpoint (end of Week 3), Final demo + UAT (Week 4/6).

---

## 4. Deliverables Pattern

Each workstream produces 3-6 documented deliverables, typically:

**Assessment workstream:**
- Current State Assessment Report (architecture diagrams, data lineage, volume analysis, quality findings)
- Report Inventory with rationalization recommendations
- Data Quality Log + source remediation steps
- Future State Architecture Design (Fabric Medallion, pipelines, RLS framework)
- Phased Implementation Roadmap (effort, resources, risks)
- SOW draft for full Fabric migration (sets up the implementation engagement)

**POV / POC workstream:**
- Working Fabric pipelines (sample set aligned to use cases)
- Bronze / Silver / Gold layer artifacts (Lakehouses, Warehouse star schema)
- Semantic Model with DAX measures (validated against source)
- Copilot setup + Q&A configuration
- Working demo of the use case
- Technical documentation & knowledge transfer
- Capacity & cost recommendation document
- CI/CD process recommendation document (where applicable)

---

## 5. Resource Roles (Assessment/POV-specific)

Roles seen across the 2 assessment/POV SOWs (full consolidated list in `resource-roles.md`):

| Role | Document | Allocation pattern |
|---|---|---|
| Fabric Consultant | APEX, NYULH | 1 FTE, 2-6 weeks |
| Data Architect | APEX | 1 FTE, full engagement duration |
| BI Engineer | APEX | 1 FTE, full engagement duration |
| Power BI Consultant | NYULH | 1 FTE, full engagement duration |
| Fabric Principal Architect | NYULH | 1 part-time, PoC technical strategy |
| Project Manager | APEX, NYULH | 25% allocation typical |
| Client SME / Data Owner | APEX | As needed |
| IT / Data Team Lead | APEX | As needed |

---

## 6. Notable Patterns to Encode

1. **Two parallel workstreams** is the default shape (Assessment + POV; or two POC workstreams). Each gets its own scope, deliverables/timeline, and Responsibility Matrix.
2. **Microsoft Partner Funding line item** is standard in the pricing table — assessments are routinely partner-led-funded ($15K typical) to deliver to customer at heavily reduced cost ($10-11K net).
3. **F-4 or Free Trial capacity** is the default Fabric SKU mentioned for assessment/POV scope ("A Microsoft Fabric Capacity (or an equivalent evaluation SKU) shall be provisioned for the duration of the PoC, with all necessary administrative privileges granted." – NYULH).
4. **Copilot + AI-readiness** is consistently called out as a POV value driver, with a dedicated "AI-Readiness for Copilot in Power BI" sub-section listing semantic-layer prerequisites.
5. **The assessment SOW always commits to producing the follow-on implementation SOW** as a deliverable. This is the bridge to the implementation engagement.
6. **Out-of-Scope sub-section under Acceptance Criteria** (not a standalone section in assessments) — explicitly defers production deployment, CI/CD setup, RLS, mobile, support, and full report migration to the implementation SOW.
7. **No expenses clause** in assessment SOWs (vs. implementation SOWs which include a $10K expense cap). Engagement is assumed fully remote.
8. **Net 30** payment terms (vs. Net 60 in implementation SOWs).
