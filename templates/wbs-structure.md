# Work Breakdown Structure (WBS) – Template Structure

Reference docs:
- `1e955cb0-High_Level_Project_Plan_01052026.xlsx` (Lids HLPP — most detailed WBS, 210-row Sheet1 + High Level Plan visualizations)
- `b9b394b1-Apex_Project_Plan_V7.xlsx` (Apex assessment plan — week-by-week schedule, day-wise activity log)
- `9fbb80b0-Emory__TruvizFabric_ImplementationProject_Plan.xlsx` (Emory implementation plan — 14 sheets, longest-running engagement view)
- `4b5439c0-Emory__Purview__Project_Plan_v1.0.xlsx` (Emory Purview governance plan — sub-engagement plan)

---

## 1. Workbook / Sheet Conventions

| Plan | Sheets | Purpose |
|---|---|---|
| Lids HLPP | High Level Plan, Sheet1, High Level Plan V2 | (a) visual phase/sprint Gantt-style ⭐ milestone grid (43-col W1-W42), (b) detailed sprint-by-sprint WBS with WBS IDs + dependencies + owner, (c) reissued V2 of high-level visual |
| Apex Project Plan | Schedule (baseline), Day wise activity, Risk, Assumptions, Issue Log, Dependencies | Multi-tab control workbook (schedule + the four mandatory governance logs) |
| Emory Truviz Implementation | Emory Plan (Old), Revised Plan (New), SOW - Planned Efforts, Remaining Efforts, Summary, Holidays, Project Milestones - Revised, Backlog Status, Tasks List & Efforts, Tasks List- Project Completion, Duplicate, Gantt chart, Risks & Challenges, New Plan 2 | Long-running engagement with replanning history (old plan + revised + new v2), efforts vs SOW reconciliation, holidays calendar, backlog, risks |
| Emory Purview | Plan, Depenendencies [sic], Additional Scope | Single-engagement plan + dependency tracker + out-of-scope items list with effort sizing |

**Common sheets to expect in any project plan:**
- **Schedule / Plan** – main WBS
- **Risk** / **Risks & Challenges** – risk log
- **Assumptions** – assumptions log
- **Issue Log** – defect / issue tracker
- **Dependencies** – cross-team or cross-vendor dependency tracker
- **Holidays** – PTO / public holiday calendar (Emory pattern – Diwali, Christmas, Gandhi Jayanti, New Year)
- **Summary** / **Project Milestones** – high-level rollup
- **Backlog** – follow-up items not in current sprint
- **Gantt chart** – visual scheduling view

---

## 2. Column Schemas

### Detailed WBS sheet (Lids HLPP Sheet1) – the "industrial" template
| Column | Type | Notes |
|---|---|---|
| WBS | text | Hierarchical ID (1, 1.1, 1.1.1, 1.1.2, …) – 3-4 levels deep |
| Phase | text | "PHASE 1 - Foundation & Core Analytics" / "PHASE 2 - Optimization & Expansion" |
| Sprint | text | "1", "2", … (sprint number) |
| Activity | text | Mid-level activity grouping (e.g., "Planning Activities & Architecture Design") |
| Task Name | text | The actual task |
| Duration (Days) | int | Workday count |
| Dependencies | text | Comma-separated WBS IDs (e.g., "1.1.1", "1.1.3,1.1.4") |
| Owner | text | Role name (e.g., "Senior Data Engineer", "Fabric Architect") |
| W1…W40 | empty/marker | Week-by-week effort or ⭐ milestone marker |

### Apex assessment WBS sheet (Schedule baseline)
| Column | Notes |
|---|---|
| Phase | "Workstream 1: Assessment" / "Workstream 2: POV" |
| Activities | Activity grouping (e.g., "Kick off & Assessment Launch", "Report Inventory") |
| Description | Specific task description |
| Estimated Start Date / Estimated Completion Date | Planned dates |
| Task Owner | Multi-line list of individual names (Apex pattern stores people, not roles) |
| Status | Completed / In progress / Yet to Start |
| RAG | Red/Amber/Green or commentary |
| Actual Start Date / Actual Completion Date | Tracking dates |
| Week 1 / Week 2 / Week 3 / Week 4 | Weekly columns with sub-date ranges |

### Emory Purview plan
| Column | Notes |
|---|---|
| # | WBS ID (1, 1.1, 1.1.1) |
| Tasks | Task description |
| Status | Completed / In Progress / TBD |
| Estimated Start Date / Estimated End Date | Planned dates |
| Task Owner | Individual name |
| No. of Days / No. of hours | Sizing |
| Effort (Man Days) | Total estimated effort |
| Consumed so far | Actuals against estimate |
| Actual Start Date / Actual End date | Tracking |
| Comments | Notes / dependencies |

### Emory Truviz implementation
- "Tasks List & Efforts" tab uses simpler shape: Task | Status | Days | Hours | (weekly day-of-week columns: M T W T F repeated × N weeks)
- "Project Milestones - Revised" uses: # | Milestone Name | Planned Start | Planned End | Actual Start | Actual End | Status | % Complete | Comments
- "SOW - Planned Efforts" reconciles WBS effort against SOW commitment

### Governance/control sheets (consistent across plans)
- **Risk log**: ID, Date Raised, Risk Description, Consequences, Likelihood, Impact, Severity, Mitigation Plan, Owner, Status, Date Closed
- **Assumptions log**: #, Date Raised, Assumption Description, Reason for Assumption, Action to Validate, Impact if Assumption Incorrect, Status
- **Issue log**: ID, Date Raised, Issue Description, Impact Description, Impact, Priority, Owner, Status, Resolution TAT
- **Dependencies log**: ID, Date Raised, Dependency Description, Owner, Impact, Status, Due Date, Remarks

---

## 3. Phase / Workstream Naming Conventions

### Implementation engagements (Lids HLPP)
- **PHASE 1 - Foundation & Core Analytics** (~13 weeks)
- **PHASE 2 - Optimization & Expansion** (~28 weeks)
- **Stages within phase**: Planning, Development, ADF Repoint, Power BI reporting, Production (Dev/Test/Prod sub-phases), SIT, UAT, Go Live, Hypercare, EDW Data Model Analysis, Env Configuration, Reports - Development, Reports - SIT, Reports - UAT, Reports - Go Live, DE - Development, DE - SIT, DE - UAT, DE - Go Live

### Assessment engagements (Apex)
- **Workstream 1: Assessment** with Activities = Kick off & Assessment Launch / Report Inventory / Assessment Draft & Semantic Model / Final Delivery & Sign-Off
- **Workstream 2: POV** with Activities = Kick off & Assessment Launch / Mid-Point Demo / Assessment Draft & Semantic Model / Final Delivery & Sign-Off

### Emory (parallel dual workstream)
- **Workstream 1: Data Engineering Process Automation**
- **Workstream 2: Power BI Reporting Migration & Modernization**
- Each WS broken into 5 Releases (Discovery → Bronze/Silver → Gold → Platinum/SIT → UAT/Deployment)

### Sprint / Release numbering
- Lids uses Sprint 1, Sprint 2, … (2-week sprints; ~10 sprints for Phase 1)
- Emory uses Release 1–Release 5 (4-week windows W1-W4, W5-W8, W9-W12, W13-W16, W17-W20)
- Apex uses Week 1–Week 4 (no sprints, weekly milestones)

---

## 4. Typical Task Hierarchy (Depth & Sizing)

### Lids HLPP – 3-level WBS (most rigorous)
```
1 PHASE 1 - Foundation & Core Analytics (65 days)
├── 1.1 Initial Planning & Architecture Design (15 days)
│   ├── 1.1.1 Project kickoff and team onboarding (2 days, Santor)
│   ├── 1.1.2 Project Planning Activities, Governance (3 days, Santor)
│   ├── 1.1.3 Architecture Design - High level Design (10 days, Santor)
│   ├── 1.1.4 Low-Level Design (LLD) documentation (10 days, Santor)
│   └── 1.1.5 Architecture review and sign-off (2 days, Santor)
├── 1.2 Environment Setup & Configuration (10 days, LIDS)
│   ├── 1.2.1 Access provisioning and security setup
│   ├── 1.2.2 Create Fabric workspaces (Dev, QA, Prod)
│   ├── 1.2.3 Configure OneLake storage structure
│   ├── 1.2.4 Setup CI/CD framework with Azure DevOps
│   └── 1.2.5 Environment validation and testing
├── 1.3 Bronze Lakehouse (Landing Layer) (10 days)
│   ├── 1.3.1 Configure Fabric Dataverse Link for D365 (Senior Data Engineer)
│   ├── 1.3.2 Create Bronze Lakehouse structure
│   ├── 1.3.3 Implement incremental ingestion patterns
│   ├── 1.3.4 Configure CDC handling for 224 tables (Data Engineering Team)
│   ├── 1.3.5 Create Delta Lake tables with partitioning
│   ├── 1.3.6 Migrate historical data to Bronze
│   ├── 1.3.7 Implement data quality checks
│   └── 1.3.8 Bronze layer validation - SIT (QA)
├── 1.4 Silver Warehouse (Staging Layer) (25 days)
│   ├── 1.4.1 Analyze 64 staging stored procedures
│   ├── 1.4.4 Refactor stored procedures to Fabric SQL
│   ├── 1.4.5 Develop PySpark notebooks for complex transforms
│   ├── 1.4.6 Create 329 tables in Silver Warehouse
│   ├── 1.4.7 Create 86 views in Silver Warehouse
│   ├── 1.4.8 Implement deduplication logic
│   ├── 1.4.9 Apply business rules and transformations
│   ├── 1.4.10 Implement historical tracking (SCD)
│   └── 1.4.11 Silver layer data validation (QA Team)
├── 1.5 Pipeline Migration (Bronze to Silver) (25 days)
├── 1.6 Sprint 9: SIT - Landing/Bronze Layer (5 days)
├── 1.7 Sprint 10: SIT - Staging/Silver Layer (5 days)
├── 1.8 Sprint 10: Power BI Report Migration (5 days)
├── 1.9 Sprint 11-12: User Acceptance Testing (10 days)
└── 1.10 Sprint 13: Phase 1 Production Go-Live (5 days, incl. 2-wk Hypercare)
```

Typical sizing: most leaf tasks are **2-5 days**, large work packages are **10-15 days**. WBS rarely goes deeper than 3 levels (Phase → Activity → Task).

### Apex assessment – flat 2-level WBS
```
Workstream 1: Assessment
├── Kick off & Assessment Launch (3 tasks, Wk 1)
├── Report Inventory (4 tasks, Wk 2)
├── Assessment Draft & Semantic Model (6 tasks, Wk 3)
└── Final Delivery & Sign-Off (4 tasks, Wk 4)
```

### Emory Purview – 3-level WBS
```
1. Data Maps
├── 1.1 Domains, Collection, Sub-Collections (4 tasks)
├── 1.2 Scanning (4 tasks)
└── 1.3 Lineage (5 tasks)
2. User Management (4 tasks)
3. Data Governance (UDP) (16+ tasks: business domains, data products, classifications, sensitivity labels, glossary, workflows, monitoring, alerts, change management)
```

---

## 5. Resource Role Catalog (from project plans)

Roles appearing in Owner / Task Owner / Resource columns:

**Lids HLPP (Sheet1)** – role-based ownership:
- Senior Data Engineer (most common — bulk of dev work)
- Data Engineer
- Data Engineering Team
- Data Engineering Team A / Data Engineering Team B (parallel pods)
- Fabric Architect (architecture design, framework decisions)
- Power BI Developer / Power BI Specialist
- Data Modeller
- DevOps Engineer (pipeline scheduling, CI/CD)
- QA / QA Team / Tester
- Project Manager
- Santor (when scoped to vendor team broadly)
- LIDS (when scoped to client team — environment provisioning, workspace creation)

**Apex / Emory plans** – use individual names rather than roles (e.g., Sanjay, Toral, Sudhakar, Ashwini, Chirag, Kalyani, Prashant, Prathamesh, Jitender, Anas, Dhaval, Gourav, James, Shreya, Mandar, Kushang, Khushboo, Swati, Kajal, Pranab, Priyanka, Nakul, Thousiff, Nitesh). For agent encoding, generalize to roles.

**Apex SOW pricing table maps individuals to roles:**
- Fabric Consultant
- Data Architect
- BI Engineer
- Project Manager

See `resource-roles.md` for the consolidated cross-document role catalog.

---

## 6. Sample Tasks per Fabric Workstream

Drawn from real WBS data. These can be used as the seed library for an agent's task generator.

### Ingestion / Bronze
- Configure Fabric Dataverse Link for D365
- Implement Fabric Dataverse Link to D365 for Test & Prod F&O environments
- Create Bronze Lakehouse structure
- Configure ingestion of N tables from source system
- Implement Change Data Capture (CDC) handling
- Configure CDC handling for N tables
- Implement incremental ingestion patterns
- Create Delta Lake tables with partitioning
- Migrate historical data to Bronze
- Implement data quality checks
- Bronze layer validation - SIT
- Ingest Clarity tables into Fabric for data analysis
- Ingest Caboodle tables for data analysis
- Bronze Layer development for File Ingestion Architecture (NHSN / EHP / HL7 / RScript)
- Set up monitoring and alerting

### Silver / Staging
- Create Fabric Data Warehouses (Test, Prod Dev, Prod Test, Prod)
- Analyze N staging stored procedures
- Create Silver Warehouse structure
- Design transformation logic framework
- Refactor stored procedures to Fabric SQL
- Develop PySpark notebooks for complex transforms
- Create N tables in Silver Warehouse
- Create N views in Silver Warehouse
- Implement deduplication logic
- Apply business rules and transformations
- Implement historical tracking (SCD)
- Silver layer data validation
- Silver Layer development for File Ingestion Architecture (per source)

### Pipeline Migration / Orchestration
- Analyze N existing ADF pipelines
- Design Fabric pipeline architecture
- Develop pipeline templates and patterns
- Rebuild pipelines as Fabric Data Pipelines
- Configure incremental load with watermarking
- Implement error handling and logging
- Setup pipeline scheduling and monitoring
- Pipeline orchestration testing
- Repoint ADF for Non-BI Systems using Fabric Bronze Lakehouse as source
- Repoint ADF for EDW using Fabric Bronze Warehouse as source
- Implement Fabric Data Factory Copy pipelines (per SQL source)
- Implement Fabric Data Factory Incremental Copy with watermark-based incremental refresh

### EDW / Gold
- Conceptual and logical data model walkthrough for [subject area]
- Pipeline Development – [Subject Area: Reference & Master Data / Sales / Pricing / Inventory / Vendor Orders / Store Traffic / Comp Traffic]
- Historical Data Migration – Scripts, Data load, testing
- Orchestration Planning, Documentation
- SIT – [Subject Area]
- UAT – Datawarehouse – [Subject Area]
- GO LIVE – [Subject Area] EDW
- Performance Testing & Optimization, Back-dated Corrections programs
- Configuration - QA (EDW + PowerBI)
- Configuration - Prod (EDW + PowerBI)

### Semantic Modeling
- Build canonical structures in Gold (fact + dimension)
- Migrate N AAS cubes to Fabric Semantic Models
- Migrate N DAX measures
- Migrate N calculated columns
- Implement Direct Lake connectivity
- Configure Row Level Security (RLS)
- Implement incremental refresh strategies
- Optimize for performance and scalability
- Semantic Models Walkthrough with business Stakeholders
- Semantic Model build with N KPI DAX measures
- Direct Lake configuration
- Shared semantic model design and implementation

### Power BI
- Repoint Power BI reports to Bronze Lakehouse, Warehouse
- Update reports to connect to Fabric Semantic Models
- Refactor Power Query transformations
- Optimize DAX measures and calculations
- Test and validate report functionality
- Validate data accuracy and performance
- Report Development – [Subject Area]
- SIT – Reports – [Subject Area]
- UAT – Reports – [Subject Area]
- GO LIVE – [Subject Area] Power BI Reports
- Power BI dashboard for Presentation
- Copilot integration / Q&A setup
- Copilot workspace setup & Q&A
- Copilot-powered auto-report generation
- Apply Emory-approved report branding, theme, layout

### Migration / Repoint
- Inventory all Power BI reports connected to legacy source
- Update connection strings to Fabric Bronze Lakehouse/Warehouse
- Validate report functionality and data accuracy
- Deploy to production
- Repoint 2 Sample reports in Power BI to Test Bronze Lakehouse and Warehouse - testing SQL endpoint connections

### Discovery / Assessment
- Project kickoff with stakeholders
- Source system access provisioning (SQL Server, UKG, HubSpot, etc.)
- Data volume & lineage baseline assessment
- Stakeholder interviews (Finance & CSW leads)
- Deep dive: source schema (Vantage Point / Caboodle / Clarity)
- API / integration assessment (UKG / HubSpot / REDCap)
- Source usage audit (Domo dashboards: active vs. abandoned)
- Report inventory & rationalization
- Data quality issue log
- Fabric capacity sizing recommendation (SKU, cost estimate)
- Draft future state architecture (Medallion, pipelines, RLS)
- Microsoft & legacy licensing comparison
- Phased implementation roadmap
- Risk register & dependency matrix
- Implementation SOW draft for full engagement
- Reassess identified N reports — confirm subject area, t-shirt size, migration wave, sequencing
- R-to-Python Notebook execution validation prototype spike

### CI/CD / DevOps
- Set up Git repository structure
- Implement deployment pipelines (Dev → Test → Prod)
- Configure automated testing
- Document deployment procedures
- Setup CI/CD framework with Azure DevOps
- Configure OneLake storage structure
- Create Fabric workspaces (Dev, QA, Prod)
- Environment validation and testing
- CI/CD framework and deployment procedures

### Governance / Purview
- Gather requirements on Domains, Collection and Sub-Collections
- Setup Domains, Collections and Sub-collections
- Define scan scope and schedule for Fabric
- Register 'Fabric' source and perform scanning
- Analyze and validate scanning results in Purview
- Configure roles and permissions in Purview for Data Maps
- Configure roles and permissions in Purview for Unified Catalog
- Create AD groups
- Discuss and create Business domains
- Data Products creation
- Gather requirements on classification & sensitivity labels and implement
- Review built-in classification with client
- Validate classification results
- Implement sensitivity labels integration
- Define business glossary terms
- Establish term relationships and hierarchies
- Assign glossary terms to data assets
- Build workflows for Data Maps and Unified Catalog
- Enable scan logs in Azure Monitor / Log Analytics
- Setup alerts for failures (email notifications)
- Implement change management process

### Testing / SIT / UAT
- Bronze SIT sign-off
- Silver SIT sign-off
- Staging to Silver migration validation
- Transformation logic validation
- Data quality and deduplication testing
- End-to-end pipeline testing
- CDC and incremental load testing
- Performance and capacity testing
- UAT planning and test case preparation
- Business user training sessions
- Execute UAT - Bronze layer / Silver layer / Power BI reports
- Defect resolution and retesting
- Performance optimization
- Parallel run with legacy systems
- UAT sign-off

### Cutover / Go-Live / Decommission
- Cutover runbook preparation
- Production deployment readiness review
- Execute production cutover
- Post go-live monitoring (Day 1-2)
- Hypercare support (4 weeks)
- Issue tracking and resolution
- Decommission Synapse Landing database
- Decommission Staging SQL database
- EDW + Reporting Cut Over
- ScalziDB Load – Fabric Pipelines from Gold EDW to ScalziDB operational
- Documentation, KT Training
- Phase lessons learned documentation

---

## 7. Notable Patterns to Encode

1. **Three-level WBS depth** is the implementation standard (Phase → Sprint/Activity → Task). Anything deeper becomes noise.
2. **Owner column is role-based** in the most mature plan (HLPP) but **person-based** in Apex/Emory. Encode roles; allow person-mapping as a second pass.
3. **Dependencies field is comma-separated WBS IDs**, no other syntax. Multiple predecessors joined by comma (e.g., "1.1.3,1.1.4").
4. **Week-level Gantt visualization** uses ⭐ characters in W1…W42 columns to mark milestone weeks; full bar painting is not used in the source data (formatting only).
5. **Sprint windows are 2 weeks** in Lids implementation plans; **release windows are 4 weeks** in Emory plans (W1-W4, W5-W8, …).
6. **Environment-stratified ownership pattern** (Lids HLPP): the same Activity (e.g., "Repoint ADF for Non-BI Systems using Fabric Bronze Lakehouse as source") appears multiple times — once per environment (Test, Prod-DEV, Prod-TEST, Prod-PROD) — each with its own milestone week.
7. **Subject-area-stratified release pattern** (Lids Phase 2): the same release activity (Pipeline Development, Historical Data Migration, SIT, UAT, Go-Live) repeats for each domain (Reference & Master Data, Sales, Pricing, Inventory, Vendor Orders, Store Traffic, Comp Traffic).
8. **Replanning history is kept in the workbook** rather than version control (Emory keeps "Emory Plan (Old)" + "Revised Plan (New)" + "New Plan 2" + "Duplicate" + "Backlog Status" all in one file). When generating, expect the plan to evolve and accommodate the re-baselining workflow.
9. **The four mandatory governance tabs** for any active engagement: Risk, Assumptions, Issue Log, Dependencies. Each has its own consistent column schema (see Section 2 above). These are auditable artifacts and should always be present.
10. **Effort vs. SOW reconciliation tab** (Emory pattern, "SOW - Planned Efforts"): tracks committed-vs-consumed effort against the original SOW. Used to inform Change Request decisions.
11. **Holidays sheet** captures India/US-blended holiday calendar — Diwali (Oct 20-21), Gandhi Jayanti (Oct 2), Christmas (Dec 25), New Year (Jan 1) — material to onshore/offshore delivery schedules.
12. **Status vocabulary**: Completed, In Progress, Yet to Start, TBD, NA, In progress (lowercase). Standardize on "Completed | In Progress | Yet to Start | TBD | NA".
13. **Apex "Day wise activity" tab** is a unique pattern: detailed agenda + output/deliverable + required participant table — a daily standup log used during 4-week assessments to drive structured discovery cadence. Includes Date, Day-of-week, Agenda (with multi-line discussion topics), Output/Deliverable, Apex Required Team (Yes/No), Santor Participants (multi-name), Status, Completion Date.
