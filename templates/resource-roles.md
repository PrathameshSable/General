# Consolidated Resource Roles Catalog

Cross-referenced inventory of every consultant / resource role mentioned across the 10 source documents (6 SOWs + 4 project plans). Roles are grouped by archetype. Each row notes the source document(s) the role appears in.

Source legend:
- **APX-A** = `004a3f7f-APEX_SOW_Assessment_and_POV__02242026.docx`
- **NYU** = `4e9b32d9-NYULH__POC_SOW_11_20_2025.docx`
- **LIDS-1** = `09257774-Phase_1_Microsoft_Fabric_Migration_SOW_01132026.docx`
- **LIDS-2** = `e964b982-Phase_2_Microsoft_Fabric_Migration_SOW_04042026.docx`
- **EMORY-SOW** = `8a73a819-Emory_SOW__Data_Engineering_and_Power_BI_Modernization__Santor.docx`
- **ACME** = `a97a2378-ACME__Consulting_Services_SOW3__04_27_2026.docx`
- **HLPP** = `1e955cb0-High_Level_Project_Plan_01052026.xlsx`
- **APX-P** = `b9b394b1-Apex_Project_Plan_V7.xlsx`
- **EMORY-P** = `9fbb80b0-Emory__TruvizFabric_ImplementationProject_Plan.xlsx`
- **PURV-P** = `4b5439c0-Emory__Purview__Project_Plan_v1.0.xlsx`

---

## 1. Vendor (Santor / Truviz) Roles

### Architects
| Role | Sources | Responsibilities |
|---|---|---|
| **Fabric Architect** | LIDS-1, LIDS-2, HLPP | Architecture design, technical leadership, capacity planning, governance framework, best practices implementation. Owns transformation logic framework and Fabric pipeline architecture design tasks. |
| **Fabric Principal Architect** | NYU | Lead the PoCs from a technical strategy and solution design perspective. Define the architecture, data integration approach, workspace structure, CI/CD model, and governance standards. Provide technical guidance, ensure POCs align with long-term scalability and enterprise standards. |
| **Solutions Architect** | EMORY-SOW | Owns target-state Fabric architecture, Lakehouse medallion design, Fabric Data Factory pipeline architecture, semantic model strategy, R-to-Notebook approach, review governance, technical design decisions. |
| **Solution Architect** | EMORY-SOW (WS1 R&R), ACME | Solution architecture, Gold/Platinum design leadership, dependency framework design leadership, technical decision support, quality oversight. In ACME T&M model: part-time (30 hrs/quarter at $90/hr) — solution design, oversight of special projects, ensuring architectural alignment. |
| **Data Architect** | APX-A | Current state documentation, source system assessment, data volume sizing, architecture design, implementation SOW (Discovery workstream). |

### Data Engineering
| Role | Sources | Responsibilities |
|---|---|---|
| **Fabric Consultant** | APX-A, NYU | Bronze/Silver/Gold build, pipelines, Semantic Model, Copilot setup (POV workstream). Builds sample pipelines in Fabric Data Factory, configures on-prem gateway, DevOps, naming/metadata frameworks, evaluates Fabric capacity and migration pathway. |
| **Fabric Data Engineer** | LIDS-1, LIDS-2 | Lakehouse/Warehouse implementation, pipeline development, stored procedure refactoring, data migration, CI/CD implementation, monitoring setup, environment management, ADF pipeline repointing, integration team coordination. |
| **Fabric Engineers** | EMORY-SOW | Lead FE (Fabric Engineer). Fabric workspace setup, FDF pipeline architecture and build, R-to-PySpark Notebook rebuilds, SQL FDF pipeline build, SharePoint/file-based FDF framework. |
| **Senior Data Engineer** | HLPP | Most common owner in detailed WBS — owns the bulk of dev tasks across Bronze configuration, Silver design, pipeline templates, incremental load, error handling, deduplication, historical tracking. |
| **Data Engineer / Data Engineering Team** | HLPP, ACME | "Data Engineering Team A" and "Data Engineering Team B" pattern in HLPP — parallel pods running concurrent workstreams. In ACME T&M: full-time consultant covers Data Engineer + Power BI Developer hybrid at $58/hr. |
| **Data Engineers** | EMORY-SOW (WS1) | Bronze/Silver validation, Gold/Platinum engineering, dependency framework implementation, SIT/UAT support, documentation assistance. |
| **BI Engineer** | APX-A | Validate Domo reports, usage, report inventory. Assessment-workstream-specific reporting platform analysis role. |

### Power BI / Semantic Layer
| Role | Sources | Responsibilities |
|---|---|---|
| **Power BI Specialist** | LIDS-1, LIDS-2 | Semantic model development, AAS migration, DAX optimization, report migration, Direct Lake implementation. |
| **Power BI Consultant** | NYU | Assist designing Power BI semantic/report layer for PoC, prepping data for AI/Copilot consumption, evaluates write-back, connectors, sharing, licensing, RLS, subscriptions, embedding. Admin / governance / performance best practices. |
| **Power BI Developer** | HLPP, ACME, EMORY-SOW (referenced) | Direct Lake semantic model reconnection, complex DAX validation, regression baseline creation, report rebuilds, measure parity testing, visual layer validation, UAT support, sign-off documentation. ACME: hybrid Data Engineer + Power BI Developer at $58/hr. |
| **Power BI Developers** (plural) | EMORY-SOW | Lead PBI. Phase 3 report rebuilds (KP CMC, Mortality, Infection Prevention). Phase 1 and Phase 2 PBI reconnection. |

### Modelling
| Role | Sources | Responsibilities |
|---|---|---|
| **Data Modeller** | LIDS-1, LIDS-2, EMORY-SOW | Study the AAS models, map data for Fabric semantic modelling per subject area. (Emory variant) Owns source-to-target mapping for all 32 reports, Lakehouse Bronze/Silver schema design, Gold fact/dimension structures per clinical subject area, data model handover to FE team at W12. |

### QA / Testing
| Role | Sources | Responsibilities |
|---|---|---|
| **Tester** | LIDS-1, LIDS-2 | Create test cases, validate data flowing in via Lakehouse, warehouse, pipelines, semantic model validation. |
| **Tester QA** | EMORY-SOW (WS1) | SIT/UAT planning, test execution, reconciliation support, defect validation, release-readiness testing. |
| **QA Engineer** | EMORY-SOW (WS2) | Functional test execution, regression suite, clinical data validation, defect management across all three phase UAT gates. |
| **QA / QA Team** | HLPP | Bronze layer validation - SIT; Silver layer data validation; Pipeline orchestration testing. |

### Business / Functional
| Role | Sources | Responsibilities |
|---|---|---|
| **Business Analyst** | EMORY-SOW | Discovery facilitation, requirements capture, source/object inventory, rule catalog, design documentation, UAT coordination and traceability. (WS2) Requirements intake for all 32 reports, UAT acceptance criteria, source-to-target mapping support, data dictionary review. |

### Project Management
| Role | Sources | Responsibilities |
|---|---|---|
| **Project Manager** | APX-A, NYU, LIDS-1, LIDS-2, EMORY-SOW, HLPP | Overall project management, stakeholder coordination, risk management, timeline tracking, sprint planning. (Emory) RAID ownership, cadence management, reporting and dependency escalation, sprint cadence, clinical UAT scheduling, stakeholder communications, change coordination. Typical allocation: 25% in POV SOWs; full-time in implementation SOWs. |

### DevOps / Platform
| Role | Sources | Responsibilities |
|---|---|---|
| **DevOps Engineer** | LIDS-2, HLPP | CI/CD implementation, deployment automation, monitoring setup, environment management. In HLPP: owns pipeline scheduling and monitoring setup. |

---

## 2. Client-Side Roles

| Role | Sources | Responsibilities |
|---|---|---|
| **Client SME / Data Owner** | APX-A | Source data access, business KPI validation, stakeholder interviews, UAT sign-off. |
| **IT / Data Team Lead** | APX-A | System access provisioning, SSIS/pipeline documentation, source schema support. |
| **Subject Matter Expert (SME)** | All implementation SOWs | Discovery interviews, validation sessions, UAT review, business logic clarification. |
| **Business Stakeholders** | LIDS-2, EMORY-SOW | Data model validation sessions, Semantic Model walkthroughs by Department, UAT decision-makers. |
| **Single Point of Contact (SPOC)** | EMORY-SOW, LIDS-1 | (Risk mitigation) One SPOC per side to ensure timely availability of resources and responses. Coordinates all access, credentials, and network-related dependencies. |
| **Power BI Administrator** | EMORY-SOW | Coordinates production deployment, manages deployment process. |
| **Integration Teams** | LIDS-1 | SPOCs from downstream/integration teams that ADF pipelines feed; coordinate end-to-end functional validation. |
| **Report Owners** | EMORY-SOW | Lead UAT, business and clinical validation, formal acceptance for migrated outputs. |
| **Process Owners** | EMORY-SOW | Primary UAT reviewers and approvers for downstream outputs in WS1 (Data Engineering Process Automation). |
| **Project Management Organization (PMO)** | All SOWs (Change Order Appendix) | Tracks and reviews scope changes through Scope Change Request process. |
| **Change Control Board (CCB)** | EMORY-SOW (risk mitigation) | Joint Emory and Truviz CCB to monitor scope-change impact, prioritize and approve. |

---

## 3. Hybrid / Combined Roles (ACME T&M model)

ACME's T&M-extension SOW collapses delivery work into 2 roles:

| Role | Rate | Allocation | Responsibilities |
|---|---|---|---|
| **Data Engineer / Power BI Developer** (combined) | $58/hr | 3 months full-time | Dev/maintenance/enhancement of Fabric platform, integration of new tables, Semantic Model design in Gold layer, redirect Power BI reports from legacy to Gold Layer, troubleshooting/performance optimization/user support, POCs for emerging Fabric capabilities (Planner, Data Agents, translytical workflows) |
| **Solution Architect** | $90/hr | Part-time, 30 hrs over 3 months | Solution design, oversight of special projects, architectural alignment with data & AI strategy |

---

## 4. Role Resolution Notes for the Agent

When the agent encounters a role-name variant, map to the canonical role using these synonymy rules:

| Canonical Role | Variants Seen | Notes |
|---|---|---|
| **Fabric Solution Architect** | Fabric Architect, Solutions Architect, Solution Architect, Fabric Principal Architect, Data Architect | "Principal" is used for advisory POV roles; "Solutions/Solution Architect" is a Truviz/Emory naming; "Data Architect" appears in lighter assessment SOWs and is functionally equivalent. |
| **Fabric Data Engineer** | Fabric Data Engineer, Fabric Engineers, Senior Data Engineer, Data Engineer, Data Engineering Team, Data Engineering Team A/B, Fabric Consultant (POV) | "Fabric Consultant" appears in POV SOWs as a hybrid (architect+engineer); "Senior Data Engineer" is the WBS-level owner; "Team A/B" is the parallelization mechanism. |
| **Power BI Developer** | Power BI Specialist, Power BI Consultant, Power BI Developer, Power BI Developers | "Specialist" = implementation SOW; "Consultant" = POV SOW; "Developer" = WBS / T&M label. |
| **Data Modeller** | Data Modeller, Data Modeler | Spelling variants — same role. |
| **Project Manager** | Project Manager | Always the same name across docs. |
| **DevOps Engineer** | DevOps Engineer | Always the same. Appears only in implementation SOWs (Phase 2+). |
| **QA / Tester** | Tester, Tester QA, QA Engineer, QA Team, QA | Standardize on "QA Engineer" for individual; "QA Team" for plural pod. |
| **Business Analyst** | Business Analyst | Emory-specific. Not present in Lids SOWs. |
| **BI Engineer** | BI Engineer | Apex-assessment-specific (validates DOMO reports / usage). Equivalent to Power BI Consultant scope but on the assessment side. |

---

## 5. Sizing Heuristics by Engagement Type

| Engagement Type | Typical Team | Total Resources |
|---|---|---|
| **Assessment / POV (4 weeks)** | Fabric Consultant ×1 (2 wks), Data Architect ×1 (4 wks), BI Engineer ×1 (4 wks), PM ×1 (25%) | 3.25 FTE-equivalent |
| **PoC dual workstream (6 weeks)** | Fabric Consultant ×1, Power BI Consultant ×1, Fabric Principal Architect ×1 | 3 FTE |
| **Implementation Phase 1 (13 weeks)** | PM ×1, Fabric Architect ×1, Fabric Data Engineer ×3, Power BI Specialist ×2, Data Modeller ×1, Tester ×1 | 9 resources |
| **Implementation Phase 2 (28 weeks + Hypercare)** | PM ×1, Fabric Architect ×1, Fabric Data Engineer ×2, Power BI Specialist ×2, Data Modeller ×1, Tester ×1, DevOps Engineer ×1 | 9 resources |
| **Parallel dual workstream (20 weeks, Emory)** | PM, Solutions Architect, Business Analyst, Data Engineers, Tester QA (WS1) + Solution Architect, PM, Data Modeller, Fabric Engineers, Power BI Developers, QA Engineer, Business Analyst (WS2) | 10-12 resources |
| **T&M ongoing support (3 months)** | Data Engineer/Power BI Developer ×1 (full-time), Solution Architect (30 hrs) | 1.1 FTE |

---

## 6. Total Distinct Roles Found

**33 distinct named roles** across 10 documents (counting all variants):

Vendor-side delivery roles (24):
1. Fabric Architect
2. Fabric Principal Architect
3. Solutions Architect
4. Solution Architect
5. Data Architect
6. Fabric Consultant
7. Fabric Data Engineer
8. Fabric Engineers (lead FE)
9. Senior Data Engineer
10. Data Engineer
11. Data Engineering Team
12. Data Engineering Team A
13. Data Engineering Team B
14. Data Engineers (Emory plural)
15. BI Engineer
16. Power BI Specialist
17. Power BI Consultant
18. Power BI Developer
19. Power BI Developers (Emory plural)
20. Data Modeller
21. Tester
22. Tester QA
23. QA Engineer
24. QA Team
25. Business Analyst
26. Project Manager
27. DevOps Engineer

Client-side / interface roles (8):
28. Client SME / Data Owner
29. IT / Data Team Lead
30. Business Stakeholder
31. Single Point of Contact (SPOC)
32. Power BI Administrator
33. Integration Teams (SPOC)
34. Report Owners / Process Owners
35. Change Control Board (CCB)

Combined-role (ACME T&M):
- Data Engineer / Power BI Developer (hybrid)

(After canonicalizing synonyms per Section 4, this collapses to **~11 distinct canonical roles** for agent encoding.)
