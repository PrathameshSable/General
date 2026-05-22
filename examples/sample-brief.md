# Sample Engagement Brief — Contoso Health Analytics Modernization

## Client
**Contoso Health Systems** — large regional healthcare network with 12 hospitals and 80+ outpatient clinics across the Northeast US.

## Business context
Contoso currently operates a fragmented analytics estate:
- On-premises SQL Server data warehouse (10+ years old) feeding 200+ SSRS reports
- A mix of Tableau and Power BI Pro for departmental dashboards
- Manual Excel-based reporting for executive leadership
- No formal data governance; sensitive PHI data lacks proper classification

Leadership has approved a multi-year modernization initiative to consolidate on Microsoft Fabric, with Power BI as the single BI tool and Purview as the governance layer.

## Strategic objectives
1. Migrate the on-prem warehouse to Fabric Lakehouse/Warehouse on OneLake
2. Establish a Medallion architecture (Bronze/Silver/Gold) for clinical, operational, and financial data
3. Implement Purview for data catalog, lineage, and PHI classification
4. Retire Tableau; consolidate on Power BI Premium / Fabric capacity
5. Build a center of excellence (CoE) for self-service analytics

## Data sources in scope
- Epic EHR (clinical encounters, labs, medications) — ~50M rows/day delta
- Workday HCM (HR, payroll) — daily full extract, ~2GB
- Salesforce Health Cloud (patient outreach) — API ingestion
- 4 finance systems (Lawson, Strata, custom AR/AP) — overnight batch
- 30+ departmental SQL Server databases

## Compliance & security
- HIPAA, HITRUST, state privacy regulations
- PHI must be classified, masked in non-prod, audit-logged
- Private endpoint architecture preferred for all Fabric workloads

## Current ask
Contoso has approved budget for:
- **Phase 0:** Assessment & POV — 8 weeks, defines target architecture, validates Fabric on 2 high-value use cases (ED throughput dashboard + revenue cycle KPIs)
- **Phase 1:** Implementation (assuming POV success) — 9-12 months, full migration of clinical and financial domains

## Stakeholders
- **Executive sponsor:** CIO (Jane Smith)
- **Business sponsor:** CFO (operational), CMIO (clinical)
- **Technical lead:** VP Data & Analytics (David Park)
- **Daily contact:** Director of Data Engineering (Sarah Lee)

## Known constraints
- No existing Fabric capacity — needs sizing recommendation
- Internal team: 3 data engineers (legacy SSIS skills), 2 Power BI developers, no Spark experience
- Hard deadline: ED throughput dashboard must be live before flu season (Sep 2026)
- Budget guidance: Assessment ≤ $350K, Implementation $4-6M

## Success criteria for assessment
- Validated target architecture (signed off by CIO + VP D&A)
- Functional POV: ED dashboard refreshing daily from Epic on Fabric Lakehouse
- Capacity sizing recommendation with TCO model
- Implementation roadmap with phased delivery plan
- Skills gap analysis and training/hiring recommendations
